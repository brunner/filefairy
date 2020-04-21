#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Logging framework for all tasks and the main app. Non-reloadable.

The framework collects several different classifications of log statements.

    * Debug: Post a message to the Slack test channel.
    * Error: Post a message to the Slack test channel and display in Fairylab.
    * Info: Display in Fairylab.
    * Warning: Post a message to the Slack test channel if threshold exceeded.

For warning log statements, no action is taken until there has been ten
consecutive logs each occurring within three minutes of each other. Once this
threshold is exceeded, a message is posted to the test channel. This is
intended to alert when some repetitive task is not functioning as expected,
e.g. network issues hindering an HTTP requesting task.

For error log statements, the message is displayed in a special area of the
Fairylab page until the module which triggered the error is reloaded. Once the
module is reloaded, any error logs attributed to it are cleared from history.
"""

import copy
import datetime
import logging
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/impl/dashboard', '', _path))

from api.renderable.renderable import Renderable  # noqa
from api.runnable.runnable import Runnable  # noqa
from api.serializable.serializable import Serializable  # noqa
from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.datetime_.datetime_ import datetime_now  # noqa
from common.datetime_.datetime_ import decode_datetime  # noqa
from common.datetime_.datetime_ import encode_datetime  # noqa
from common.datetime_.datetime_ import suffix  # noqa
from common.datetime_.datetime_ import timestamp  # noqa
from common.elements.elements import anchor  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import pre  # noqa
from common.elements.elements import row  # noqa
from common.elements.elements import table  # noqa
from common.re_.re_ import search  # noqa
from common.secrets.secrets import secrets_sub  # noqa
from common.slack.slack import chat_post_message  # noqa
from common.slack.slack import files_upload  # noqa
from types_.notify.notify import Notify  # noqa
from types_.response.response import Response  # noqa

LINK = 'https://github.com/brunner/filefairy/blob/master/'
DATA_DIR = re.sub(r'/impl/dashboard', '', _path) + '/resources/data/dashboard'


class Dashboard(Renderable, Runnable, Serializable):
    """Logging framework for all tasks and the main app."""
    def __init__(self, **kwargs):
        """Create a Dashboard object.

        Attributes:
            warnings: List of handled warning logs and their count.
        """
        super(Dashboard, self).__init__(**kwargs)
        self.warnings = []

    @staticmethod
    def _href():
        return '/fairylab/dashboard/'

    @staticmethod
    def _title():
        return 'Dashboard'

    def _render_data(self, **kwargs):
        dashboard_html = self.get_dashboard_html(**kwargs)
        return [('dashboard/index.html', '', 'dashboard.html', dashboard_html)]

    def _notify_internal(self, **kwargs):
        notify = kwargs['notify']
        if notify == Notify.FILEFAIRY_DAY:
            self.cleanup(**kwargs)
        return Response()

    def cleanup(self, **kwargs):
        data = self.data
        original = copy.deepcopy(data)

        d = kwargs['date'] - datetime.timedelta(days=3)
        rounded = datetime_datetime_pst(d.year, d.month, d.day)

        for date in list(data['logs'].keys()):
            if decode_datetime(date) <= rounded:
                data['logs'].pop(date, None)

        self.warnings = []

        if data != original:
            self._write()
            self._render(**dict(kwargs, log=False))

    def emit(self, **kwargs):
        cwd = os.getcwd()
        record = {k: kwargs[k] for k in ['levelname', 'lineno', 'msg']}
        record['pathname'] = os.path.join(cwd, kwargs['pathname'])

        d = datetime_now()
        record['date'] = encode_datetime(d)

        if kwargs['exc_info']:
            exc = logging.Formatter.formatException(self, kwargs['exc_info'])
            record['exc'] = secrets_sub(exc)
        else:
            record['exc'] = ''

        levelname = record['levelname']
        if levelname in ['DEBUG', 'ERROR']:
            self.emit_alert(record, **kwargs)
        if levelname in ['INFO', 'ERROR']:
            self.emit_log(record)
        if levelname == 'WARNING':
            self.emit_warning(record, **kwargs)

    def emit_alert(self, record, **kwargs):
        title = Dashboard.get_record_title(record)
        chat_post_message('testing', title + ': ' + record['msg'])

        for key in ['exc', 'stderr', 'stdout']:
            value = record.get(key, kwargs.get(key, ''))
            if value:
                content = secrets_sub(value)
                filename = kwargs.get('module', '') + '.' + key + '.txt'
                files_upload(content, filename, 'testing')

    def emit_log(self, record):
        d = decode_datetime(record['date'])
        rounded = datetime_datetime_pst(d.year, d.month, d.day)

        date = encode_datetime(rounded)
        if date not in self.data['logs']:
            self.data['logs'][date] = []
        self.data['logs'][date].append(record)

        self._render(date=d, log=False)
        self._write()

    def emit_warning(self, record, **kwargs):
        d = decode_datetime(record['date'])

        for warning in list(self.warnings):
            items = {k: v for k, v in record.items() if k != 'date'}
            if items.items() <= warning.items():
                date = warning['date']
                diff = d - date
                if diff.days == 0 and diff.seconds < 180:
                    warning['count'] += 1
                    warning['date'] = d
                    if warning['count'] == 10:
                        self.emit_alert(record, **kwargs)
                    break
        else:
            warning = copy.deepcopy(record)
            warning['count'] = 1
            warning['date'] = d
            self.warnings.append(warning)

    def get_dashboard_html(self, **kwargs):
        ret = {'logs': []}

        for date in sorted(self.data['logs']):
            d = decode_datetime(date)
            head_content = d.strftime('%A, %B %-d{}, %Y').format(suffix(d.day))

            body = []
            logs = self.data['logs'][date]
            for record in sorted(logs, key=self.sort_records):
                link = self.get_record_link(record)
                title = self.get_record_title(record)

                date = record['date']
                levelname = record['levelname']
                msg = record['msg']

                a = anchor(link, title)
                time = decode_datetime(date).strftime('%H:%M')
                row_ = row(cells=[
                    cell(content=a),
                    cell(content=msg),
                    cell(content=time)
                ])

                if levelname == 'ERROR':
                    if body:
                        t = self.create_table(head_content, body, None)
                        ret['logs'].insert(0, t)

                    foot = [row(cells=[cell(content=pre(record['exc']))])]
                    t = self.create_table(head_content, [row_], foot)
                    ret['logs'].insert(0, t)
                else:
                    body.insert(0, row_)

            if body:
                t = self.create_table(head_content, body, None)
                ret['logs'].insert(0, t)

        return ret

    @staticmethod
    def create_table(head_content, body, foot):
        fcols = [col(colspan='3')] if foot else None
        return table(
            clazz='border mb-3',
            hcols=[col(clazz='font-weight-bold text-dark', colspan='3')],
            bcols=[col(clazz='css-style-w-150px'),
                   col(),
                   col(clazz='text-right css-style-w-75px')],
            fcols=fcols,
            head=[row(cells=[cell(content=head_content)])],
            body=body,
            foot=foot)

    @staticmethod
    def get_record_line(record):
        lineno = record['lineno']
        return '#L' + str(lineno)

    @staticmethod
    def get_record_link(record):
        pathname = record['pathname']
        if 'filefairy/' in pathname:
            _, end = pathname.split('filefairy/', 1)
        else:
            end = pathname
        return LINK + end + Dashboard.get_record_line(record)

    @staticmethod
    def get_record_title(record):
        pathname = record['pathname']
        if '/' in pathname:
            _, end = pathname.rsplit('/', 1)
        else:
            end = pathname
        return end + Dashboard.get_record_line(record)

    @staticmethod
    def sort_records(record):
        return (record['date'], record['pathname'], record['lineno'])


class LoggingHandler(logging.Handler):
    def __init__(self, dashboard):
        super().__init__()
        self.dashboard = dashboard

    def emit(self, record):
        # TODO: uncomment after finishing refactors.
        # self.dashboard.emit(**vars(record))
        print(record)
