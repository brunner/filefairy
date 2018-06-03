#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import logging
import os
import re
import string
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/core/dashboard', '', _path))
from api.registrable.registrable import Registrable  # noqa
from api.renderable.renderable import Renderable  # noqa
from util.datetime_.datetime_ import encode_datetime  # noqa
from util.slack.slack import chat_post_message  # noqa
from util.slack.slack import files_upload  # noqa


class StringFormatter(string.Formatter):
    def get_value(self, key, args, kwargs):
        return kwargs.get(key, '{{{0}}}'.format(key))


class Dashboard(Registrable, Renderable):
    def __init__(self, **kwargs):
        super(Dashboard, self).__init__(**kwargs)
        self.formatter = StringFormatter()

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _href():
        return '/fairylab/dashboard/'

    @staticmethod
    def _info():
        return 'Tails exceptions and log messages.'

    @staticmethod
    def _title():
        return 'dashboard'

    def _render_internal(self, **kwargs):
        html = 'html/fairylab/dashboard/index.html'
        _home = self._home(**kwargs)
        return [(html, '', 'dashboard.html', _home)]

    def _home(self, **kwargs):
        ret = {
            'breadcrumbs': [{
                'href': '/fairylab/',
                'name': 'Home'
            }, {
                'href': '',
                'name': 'Dashboard'
            }]
        }
        return ret

    def _log(self, **kwargs):
        record = {k: kwargs[k] for k in ['levelname', 'lineno', 'msg']}

        cwd = os.getcwd()
        record['pathname'] = os.path.join(cwd, kwargs['pathname'])

        e = kwargs['exc_info']
        record['exc'] = logging.Formatter.formatException(self, e) if e else ''

        date = kwargs.get('date') or datetime.datetime.now()
        self._record(date, record)

    def _record(self, date, record):
        encoded_date = encode_datetime(date)

        day = datetime.datetime(date.year, date.month, date.day)
        encoded_day = encode_datetime(day)
        if encoded_day not in self.data['records']:
            self.data['records'][encoded_day] = []

        found = False
        for r in self.data['records'][encoded_day]:
            if record.items() <= r.items():
                c = r.get('count', 0)
                r['count'] = c + 1
                r['date'] = encoded_date
                found = True

        if not found:
            record.update({'count': 1, 'date': encoded_date})
            self.data['records'][encoded_day].append(record)

        self.write()

        s = '{pathname}#{lineno}: {msg}'
        msg = self.formatter.format(s, **record)
        if record.get('v'):
            chat_post_message('testing', msg)
            if record.get('c'):
                flog = record.get('module') + '.log.txt'
                files_upload(record['c'], flog, 'testing')


class LoggingHandler(logging.Handler):
    def __init__(self, dashboard):
        super().__init__()
        self.dashboard = dashboard

    def emit(self, record):
        self.dashboard._log(**vars(record))
