#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import re
import string
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/core/dashboard', '', _path))
from api.registrable.registrable import Registrable  # noqa
from api.renderable.renderable import Renderable  # noqa
from util.slack.slack import chat_post_message  # noqa
from util.slack.slack import files_upload  # noqa


class Dashboard(Registrable, Renderable):
    def __init__(self, **kwargs):
        super(Dashboard, self).__init__(**kwargs)

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


class StringFormatter(string.Formatter):
    def get_value(self, key, args, kwargs):
        return kwargs.get(key, '{{{0}}}'.format(key))


class LoggingHandler(logging.Handler):
    def __init__(self, dashboard):
        super().__init__()
        self.dashboard = dashboard
        self.formatter = StringFormatter()

    def emit(self, record):
        vars_ = vars(record)

        s = '{pathname}#{lineno}: {msg}'
        msg = self.formatter.format(s, **vars(record))

        if vars_.get('v'):
            chat_post_message('testing', msg)
            if vars_.get('c'):
                flog = vars_.get('module') + '.log.txt'
                files_upload(vars_['c'], flog, 'testing')
