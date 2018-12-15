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

from api.registrable.registrable import Registrable  # noqa
from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.datetime_.datetime_ import datetime_now  # noqa
from common.datetime_.datetime_ import decode_datetime  # noqa
from common.datetime_.datetime_ import encode_datetime  # noqa
from common.datetime_.datetime_ import suffix  # noqa
from common.datetime_.datetime_ import timestamp  # noqa
from common.elements.elements import anchor  # noqa
from common.elements.elements import card  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import table  # noqa
from common.re_.re_ import find  # noqa
from common.secrets.secrets import secrets_sub  # noqa
from common.slack.slack import chat_post_message  # noqa
from common.slack.slack import files_upload  # noqa
from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa

LINK = 'https://github.com/brunner/filefairy/blob/master/'


class Dashboard(Registrable):
    """Logging framework for all tasks and the main app."""

    def __init__(self, **kwargs):
        """Create a Dashboard object.

        Attributes:
            warnings: List of handled warning logs and their count.
        """
        super(Dashboard, self).__init__(**kwargs)
        self.warnings = []

    @staticmethod
    def _data():
        """Store Dashboard information.

        Attributes:
            logs: List of stored info and error logs.
        """
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _href():
        return '/dashboard/'

    @staticmethod
    def _info():
        return 'Tails exceptions and log messages.'

    @staticmethod
    def _title():
        return 'dashboard'

    def _notify_internal(self, **kwargs):
        notify = kwargs['notify']
        if notify == Notify.FILEFAIRY_DAY:
            self._cleanup(**kwargs)
        return Response()

    def _on_message_internal(self, **kwargs):
        return Response()

    def _render_internal(self, **kwargs):
        _index_html = self._index_html(**kwargs)
        return [('dashboard/index.html', '', 'dashboard.html', _index_html)]

    def _run_internal(self, **kwargs):
        return Response()

    def _setup_internal(self, **kwargs):
        self._render(**dict(kwargs, log=False))
        return Response()

    def _shadow_internal(self, **kwargs):
        return []

    def _cleanup(self, **kwargs):
        data = self.data
        original = copy.deepcopy(data)

        d = kwargs['date'] - datetime.timedelta(days=7)
        rounded = datetime_datetime_pst(d.year, d.month, d.day)

        for date in list(data['logs'].keys()):
            if decode_datetime(date) <= rounded:
                del data['logs'][date]

        self.warnings = []

        if data != original:
            self.write()
            self._render(**dict(kwargs, log=False))

    def _emit(self, **kwargs):
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
            self._alert(record, **kwargs)
        if levelname in ['INFO', 'ERROR']:
            self._log(record)
        if levelname == 'WARNING':
            self._warning(record, **kwargs)

    def _log(self, record):
        d = decode_datetime(record['date'])
        rounded = datetime_datetime_pst(d.year, d.month, d.day)

        date = encode_datetime(rounded)
        if date not in self.data['logs']:
            self.data['logs'][date] = []
        self.data['logs'][date].append(record)

        module = find('^Reloaded (\w+).$', record['msg'])
        if module:
            disabled = 'Disabled {}.'.format(module)
            logs = self.data['logs']
            for date in logs:
                for record in list(logs[date]):
                    if disabled == record['msg']:
                        logs[date].remove(record)

        self._render(date=d, log=False)
        self.write()

    def _warning(self, record, **kwargs):
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
                        self._alert(record, **kwargs)
                    break
        else:
            warning = copy.deepcopy(record)
            warning['count'] = 1
            warning['date'] = d
            self.warnings.append(warning)

    def _index_html(self, **kwargs):
        ret = {
            'breadcrumbs': [{
                'href': '/',
                'name': 'Fairylab'
            }, {
                'href': '',
                'name': 'Dashboard'
            }],
            'exceptions': [],
            'logs': []
        }

        for date in sorted(self.data['logs']):
            d = decode_datetime(date)
            head_content = d.strftime('%A, %B %-d{}, %Y').format(suffix(d.day))

            body = []
            logs = self.data['logs'][date]
            for record in sorted(logs, key=self._sort):
                link = self._record_link(record)
                title = self._record_title(record)

                date = record['date']
                levelname = record['levelname']
                msg = record['msg']

                if levelname == 'ERROR':
                    exc = record['exc']
                    ts = timestamp(decode_datetime(date))
                    c = card(href=link, title=title, info=msg, code=exc, ts=ts)
                    ret['exceptions'].insert(0, c)

                a = anchor(link, title)
                time = decode_datetime(date).strftime('%H:%M')
                r = [cell(content=a), cell(content=msg), cell(content=time)]
                body.insert(0, r)

            t = table(
                hcols=[col(colspan='3')],
                bcols=[None, None, col(clazz='text-right w-75p')],
                head=[cell(content=head_content)],
                body=body)
            ret['logs'].insert(0, t)

        return ret

    @staticmethod
    def _alert(record, **kwargs):
        title = Dashboard._record_title(record)
        chat_post_message('testing', title + ': ' + record['msg'])

        for key in ['exc', 'stderr', 'stdout']:
            value = record.get(key, kwargs.get(key, ''))
            if value:
                content = secrets_sub(value)
                filename = kwargs.get('module', '') + '.' + key + '.txt'
                files_upload(content, filename, 'testing')

    @staticmethod
    def _record_line(record):
        lineno = record['lineno']
        return '#L' + str(lineno)

    @staticmethod
    def _record_link(record):
        pathname = record['pathname']
        if 'filefairy/' in pathname:
            _, end = pathname.split('filefairy/', 1)
        else:
            end = pathname
        return LINK + end + Dashboard._record_line(record)

    @staticmethod
    def _record_title(record):
        pathname = record['pathname']
        if '/' in pathname:
            _, end = pathname.rsplit('/', 1)
        else:
            end = pathname
        return end + Dashboard._record_line(record)

    @staticmethod
    def _sort(record):
        return (record['date'], record['pathname'], record['lineno'])


class LoggingHandler(logging.Handler):
    def __init__(self, dashboard):
        super().__init__()
        self.dashboard = dashboard

    def emit(self, record):
        self.dashboard._emit(**vars(record))
