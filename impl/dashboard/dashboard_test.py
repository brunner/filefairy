#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for dashboard.py."""

import os
import re
import sys
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.extend((_path, re.sub(r'/impl/dashboard', '', _path)))

from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.datetime_.datetime_ import encode_datetime  # noqa
from common.elements.elements import anchor  # noqa
from common.elements.elements import card  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import table  # noqa
from common.jinja2_.jinja2_ import env  # noqa
from common.json_.json_ import dumps  # noqa
from common.test.test import Test  # noqa
from common.test.test import main  # noqa
from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa
from impl.dashboard.dashboard import Dashboard  # noqa

ENV = env()

DATE_10190000 = datetime_datetime_pst(1985, 10, 19)
DATE_10250000 = datetime_datetime_pst(1985, 10, 25)
DATE_10250007 = datetime_datetime_pst(1985, 10, 25, 0, 7)
DATE_10260000 = datetime_datetime_pst(1985, 10, 26)
DATE_10260602 = datetime_datetime_pst(1985, 10, 26, 6, 2, 30)
DATE_10260604 = datetime_datetime_pst(1985, 10, 26, 6, 4)

EXC = (Exception, Exception(), Exception().__traceback__)
PATH = '/home/pi/filefairy/path/to/module.py'
STDOUT = 'stdout'
STDERR = 'stderr'


def _data(logs=None):
    if logs is None:
        logs = {}
    return {'logs': logs}


def _kwargs(pathname, lineno, levelname, msg, exc_info):
    return {
        'pathname': pathname,
        'lineno': lineno,
        'levelname': levelname,
        'msg': msg,
        'exc_info': exc_info,
        'module': 'module',
        'stdout': STDOUT,
        'stderr': STDERR
    }


def _record(pathname, lineno, levelname, msg, exc, date):
    return {
        'pathname': pathname,
        'lineno': lineno,
        'levelname': levelname,
        'msg': msg,
        'exc': exc,
        'date': encode_datetime(date)
    }


def _warning(pathname, lineno, levelname, msg, exc, date, count):
    return {
        'pathname': pathname,
        'lineno': lineno,
        'levelname': levelname,
        'msg': msg,
        'exc': exc,
        'date': date,
        'count': count,
    }


class DashboardTest(Test):
    def setUp(self):
        patch_chat = mock.patch('impl.dashboard.dashboard.chat_post_message')
        self.addCleanup(patch_chat.stop)
        self.mock_chat = patch_chat.start()

        patch_open = mock.patch(
            'api.serializable.serializable.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

        patch_upload = mock.patch('impl.dashboard.dashboard.files_upload')
        self.addCleanup(patch_upload.stop)
        self.mock_upload = patch_upload.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]

    def reset_mocks(self):
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()

    def create_dashboard(self, data, warnings=None):
        self.init_mocks(data)
        dashboard = Dashboard(date=DATE_10250007, e=ENV)

        self.mock_open.assert_called_once_with(Dashboard._data(), 'r')
        self.assertNotCalled(self.mock_chat, self.mock_handle.write,
                             self.mock_upload)
        self.assertEqual(dashboard.data, data)

        self.reset_mocks()
        self.init_mocks(data)

        if warnings:
            dashboard.warnings = warnings

        return dashboard

    def test_init(self):
        dashboard = self.create_dashboard(_data())

        self.assertFalse(len(dashboard.warnings))
        self.assertNotCalled(self.mock_chat, self.mock_open,
                             self.mock_handle.write, self.mock_upload)

    @mock.patch.object(Dashboard, '_cleanup')
    def test_notify__fairylab_day(self, mock_cleanup):
        dashboard = self.create_dashboard(_data())
        response = dashboard._notify_internal(
            date=DATE_10260602, notify=Notify.FILEFAIRY_DAY)
        self.assertEqual(response, Response())

        mock_cleanup.assert_called_once_with(
            date=DATE_10260602, notify=Notify.FILEFAIRY_DAY)
        self.assertNotCalled(self.mock_chat, self.mock_open,
                             self.mock_handle.write, self.mock_upload)

    @mock.patch.object(Dashboard, '_cleanup')
    def test_notify__with_other(self, mock_cleanup):
        dashboard = self.create_dashboard(_data())
        response = dashboard._notify_internal(
            date=DATE_10260602, notify=Notify.OTHER)
        self.assertEqual(response, Response())

        self.assertNotCalled(mock_cleanup, self.mock_chat, self.mock_open,
                             self.mock_handle.write, self.mock_upload)

    @mock.patch.object(Dashboard, '_index_html')
    def test_render(self, mock_index):
        index_html = {'breadcrumbs': []}
        mock_index.return_value = index_html

        dashboard = self.create_dashboard(_data())
        actual = dashboard._render_internal(date=DATE_10260602)
        expected = [('dashboard/index.html', '', 'dashboard.html', index_html)]
        self.assertEqual(actual, expected)

        self.assertNotCalled(self.mock_chat, self.mock_open,
                             self.mock_handle.write, self.mock_upload)

    @mock.patch.object(Dashboard, '_render')
    def test_cleanup(self, mock_render):
        old = encode_datetime(DATE_10190000)
        new = encode_datetime(DATE_10260000)
        error = _record(PATH, 123, 'ERROR', 'foo', '...', DATE_10260602)
        info = _record(PATH, 456, 'INFO', 'bar', '', DATE_10250007)
        warning = _warning(PATH, 789, 'WARNING', 'baz', '...', DATE_10260602,
                           1)

        data = _data({old: [info], new: [error]})
        dashboard = self.create_dashboard(data, [warning])
        dashboard._cleanup(date=DATE_10260602)
        self.assertEqual(dashboard.warnings, [])

        data = _data({new: [error]})
        mock_render.assert_called_once_with(date=DATE_10260602, log=False)
        self.mock_open.assert_called_once_with(Dashboard._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(data) + '\n')
        self.assertNotCalled(self.mock_chat, self.mock_upload)

    @mock.patch.object(Dashboard, '_warning')
    @mock.patch('impl.dashboard.dashboard.datetime_now')
    @mock.patch.object(Dashboard, '_log')
    @mock.patch('impl.dashboard.dashboard.os.getcwd')
    @mock.patch.object(Dashboard, '_alert')
    def test_emit__debug(self, mock_alert, mock_cwd, mock_log, mock_now,
                         mock_warning):
        mock_cwd.return_value = '/home/pi/filefairy/'
        mock_now.return_value = DATE_10260602

        kwargs = _kwargs('path/to/module.py', 55, 'DEBUG', 'foo', None)
        dashboard = self.create_dashboard(_data())
        dashboard._emit(**kwargs)

        path = '/home/pi/filefairy/path/to/module.py'
        record = _record(path, 55, 'DEBUG', 'foo', '', DATE_10260602)
        mock_alert.assert_called_once_with(record, **kwargs)
        self.assertNotCalled(mock_log, mock_warning, self.mock_chat,
                             self.mock_open, self.mock_handle.write,
                             self.mock_upload)

    @mock.patch.object(Dashboard, '_warning')
    @mock.patch('impl.dashboard.dashboard.datetime_now')
    @mock.patch.object(Dashboard, '_log')
    @mock.patch('impl.dashboard.dashboard.os.getcwd')
    @mock.patch.object(Dashboard, '_alert')
    def test_emit__error(self, mock_alert, mock_cwd, mock_log, mock_now,
                         mock_warning):
        mock_cwd.return_value = '/home/pi/filefairy/'
        mock_now.return_value = DATE_10260602

        kwargs = _kwargs('path/to/module.py', 123, 'ERROR', 'foo', EXC)
        dashboard = self.create_dashboard(_data())
        dashboard._emit(**kwargs)

        path = '/home/pi/filefairy/path/to/module.py'
        record = _record(path, 123, 'ERROR', 'foo', 'Exception', DATE_10260602)
        mock_alert.assert_called_once_with(record, **kwargs)
        mock_log.assert_called_once_with(record)
        self.assertNotCalled(mock_warning, self.mock_chat, self.mock_open,
                             self.mock_handle.write, self.mock_upload)

    @mock.patch.object(Dashboard, '_warning')
    @mock.patch('impl.dashboard.dashboard.datetime_now')
    @mock.patch.object(Dashboard, '_log')
    @mock.patch('impl.dashboard.dashboard.os.getcwd')
    @mock.patch.object(Dashboard, '_alert')
    def test_emit__info(self, mock_alert, mock_cwd, mock_log, mock_now,
                        mock_warning):
        mock_cwd.return_value = '/home/pi/filefairy/'
        mock_now.return_value = DATE_10260602

        kwargs = _kwargs('path/to/module.py', 456, 'INFO', 'bar', None)
        dashboard = self.create_dashboard(_data())
        dashboard._emit(**kwargs)

        path = '/home/pi/filefairy/path/to/module.py'
        record = _record(path, 456, 'INFO', 'bar', '', DATE_10260602)
        mock_log.assert_called_once_with(record)
        self.assertNotCalled(mock_alert, mock_warning, self.mock_chat,
                             self.mock_open, self.mock_handle.write,
                             self.mock_upload)

    @mock.patch.object(Dashboard, '_warning')
    @mock.patch('impl.dashboard.dashboard.datetime_now')
    @mock.patch.object(Dashboard, '_log')
    @mock.patch('impl.dashboard.dashboard.os.getcwd')
    @mock.patch.object(Dashboard, '_alert')
    def test_emit__warning(self, mock_alert, mock_cwd, mock_log, mock_now,
                           mock_warning):
        mock_cwd.return_value = '/home/pi/filefairy/'
        mock_now.return_value = DATE_10260602

        kwargs = _kwargs('path/to/module.py', 789, 'WARNING', 'baz', EXC)
        dashboard = self.create_dashboard(_data())
        dashboard._emit(**kwargs)

        path = '/home/pi/filefairy/path/to/module.py'
        record = _record(path, 789, 'WARNING', 'baz', 'Exception',
                         DATE_10260602)
        mock_warning.assert_called_once_with(record, **kwargs)
        self.assertNotCalled(mock_alert, mock_log, self.mock_chat,
                             self.mock_open, self.mock_handle.write,
                             self.mock_upload)

    @mock.patch.object(Dashboard, '_render')
    def test_log__other(self, mock_render):
        new = encode_datetime(DATE_10260000)
        error = _record(PATH, 123, 'ERROR', 'foo', '...', DATE_10260602)

        data = _data({new: [error]})
        record = _record(PATH, 456, 'INFO', 'bar', '', DATE_10260602)
        dashboard = self.create_dashboard(data)
        dashboard._log(record)

        data = _data({new: [error, record]})
        mock_render.assert_called_once_with(date=DATE_10260602, log=False)
        self.mock_open.assert_called_once_with(Dashboard._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(data) + '\n')
        self.assertNotCalled(self.mock_chat, self.mock_upload)

    @mock.patch.object(Dashboard, '_render')
    def test_log__reloaded(self, mock_render):
        new = encode_datetime(DATE_10260000)
        error = _record(PATH, 123, 'ERROR', 'Disabled foo.', '', DATE_10260602)

        data = _data({new: [error]})
        record = _record(PATH, 456, 'INFO', 'Reloaded foo.', '', DATE_10260602)
        dashboard = self.create_dashboard(data)
        dashboard._log(record)

        data = _data({new: [record]})
        mock_render.assert_called_once_with(date=DATE_10260602, log=False)
        self.mock_open.assert_called_once_with(Dashboard._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(data) + '\n')
        self.assertNotCalled(self.mock_chat, self.mock_upload)

    @mock.patch.object(Dashboard, '_alert')
    def test_warning__alert(self, mock_alert):
        kwargs = _kwargs('path/to/module.py', 789, 'W', 'baz', EXC)
        record = _record(PATH, 789, 'W', 'baz', 'E', DATE_10260604)
        warning = _warning(PATH, 789, 'W', 'baz', 'E', DATE_10260602, 9)
        dashboard = self.create_dashboard(_data(), [warning])
        dashboard._warning(record, **kwargs)

        warning = _warning(PATH, 789, 'W', 'baz', 'E', DATE_10260604, 10)
        self.assertEqual(dashboard.warnings, [warning])
        mock_alert.assert_called_once_with(record, **kwargs)
        self.assertNotCalled(self.mock_chat, self.mock_open,
                             self.mock_handle.write, self.mock_upload)

    @mock.patch.object(Dashboard, '_alert')
    def test_warning__multiple(self, mock_alert):
        kwargs = _kwargs('path/to/module.py', 789, 'W', 'baz', EXC)
        record = _record(PATH, 789, 'W', 'baz', 'E', DATE_10260604)
        warning = _warning(PATH, 789, 'W', 'baz', 'E', DATE_10260602, 1)
        dashboard = self.create_dashboard(_data(), [warning])
        dashboard._warning(record, **kwargs)

        warning = _warning(PATH, 789, 'W', 'baz', 'E', DATE_10260604, 2)
        self.assertEqual(dashboard.warnings, [warning])
        self.assertNotCalled(mock_alert, self.mock_chat, self.mock_open,
                             self.mock_handle.write, self.mock_upload)

    @mock.patch.object(Dashboard, '_alert')
    def test_warning__single(self, mock_alert):
        kwargs = _kwargs('path/to/module.py', 789, 'W', 'baz', EXC)
        record = _record(PATH, 789, 'W', 'baz', 'E', DATE_10260602)
        dashboard = self.create_dashboard(_data(), [])
        dashboard._warning(record, **kwargs)

        warning = _warning(PATH, 789, 'W', 'baz', 'E', DATE_10260602, 1)
        self.assertEqual(dashboard.warnings, [warning])
        self.assertNotCalled(mock_alert, self.mock_chat, self.mock_open,
                             self.mock_handle.write, self.mock_upload)

    def test_index_html(self):
        old = encode_datetime(DATE_10250000)
        new = encode_datetime(DATE_10260000)
        path = '/home/pi/filefairy/path/to/module.py'
        error = _record(path, 123, 'ERROR', 'foo', '...', DATE_10260602)
        info = _record(path, 456, 'INFO', 'bar', '', DATE_10250007)

        data = _data({old: [info], new: [error]})
        dashboard = self.create_dashboard(data)

        link = 'https://github.com/brunner/filefairy/blob/master/'
        breadcrumbs = [{
            'href': '/',
            'name': 'Fairylab'
        }, {
            'href': '',
            'name': 'Dashboard'
        }]
        logs = [
            table(
                clazz='border mt-3',
                hcols=[col(colspan='3')],
                bcols=[None, None, col(clazz='text-right w-75p')],
                head=[cell(content='Saturday, October 26th, 1985')],
                body=[[
                    cell(
                        content=anchor(link + 'path/to/module.py#L123',
                                       'module.py#L123')),
                    cell(content='foo'),
                    cell(content='06:02')
                ]]),
            table(
                clazz='border mt-3',
                hcols=[col(colspan='3')],
                bcols=[None, None, col(clazz='text-right w-75p')],
                head=[cell(content='Friday, October 25th, 1985')],
                body=[[
                    cell(
                        content=anchor(link + 'path/to/module.py#L456',
                                       'module.py#L456')),
                    cell(content='bar'),
                    cell(content='00:07')
                ]]),
        ]
        exceptions = [
            card(
                href=link + 'path/to/module.py#L123',
                title='module.py#L123',
                info='foo',
                code='...',
                ts='06:02:30 PDT (1985-10-26)')
        ]
        actual = dashboard._index_html(date=DATE_10260602)
        expected = {
            'breadcrumbs': breadcrumbs,
            'logs': logs,
            'exceptions': exceptions
        }
        self.assertEqual(actual, expected)
        self.assertNotCalled(self.mock_chat, self.mock_open,
                             self.mock_handle.write, self.mock_upload)

    def test_alert(self):
        path = '/home/pi/filefairy/path/to/module.py'
        record = _record(path, 55, 'DEBUG', 'foo', '', DATE_10260602)
        kwargs = _kwargs('path/to/module.py', 55, 'DEBUG', 'foo', None)

        dashboard = self.create_dashboard(_data())
        dashboard._alert(record, **kwargs)

        self.mock_chat.assert_called_once_with('testing', 'module.py#L55: foo')
        self.mock_upload.assert_has_calls([
            mock.call('stderr', 'module.stderr.txt', 'testing'),
            mock.call('stdout', 'module.stdout.txt', 'testing'),
        ])
        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    def test_record_link(self):
        link = 'https://github.com/brunner/filefairy/blob/master/'
        path = '/home/pi/filefairy/path/to/module.py'
        record = _record(path, 55, 'DEBUG', 'foo', '', DATE_10260602)

        dashboard = self.create_dashboard(_data())
        actual = dashboard._record_link(record)
        expected = link + 'path/to/module.py#L55'
        self.assertEqual(actual, expected)
        self.assertNotCalled(self.mock_chat, self.mock_open,
                             self.mock_handle.write, self.mock_upload)

    def test_record_title(self):
        path = '/home/pi/filefairy/path/to/module.py'
        record = _record(path, 55, 'DEBUG', 'foo', '', DATE_10260602)

        dashboard = self.create_dashboard(_data())
        actual = dashboard._record_title(record)
        expected = 'module.py#L55'
        self.assertEqual(actual, expected)
        self.assertNotCalled(self.mock_chat, self.mock_open,
                             self.mock_handle.write, self.mock_upload)

    def test_sort(self):
        path1 = '/home/pi/filefairy/path/to/a.py'
        path2 = '/home/pi/filefairy/path/to/b.py'
        record1 = _record(path1, 55, 'DEBUG', 'foo', '', DATE_10260602)
        record2 = _record(path1, 110, 'DEBUG', 'foo', '', DATE_10260604)
        record3 = _record(path1, 110, 'DEBUG', 'foo', '', DATE_10260602)
        record4 = _record(path2, 110, 'DEBUG', 'foo', '', DATE_10260604)
        record5 = _record(path2, 55, 'DEBUG', 'foo', '', DATE_10260602)
        records = [record1, record2, record3, record4, record5]

        dashboard = self.create_dashboard(_data())
        actual = list(sorted(records, key=dashboard._sort))
        expected = [record1, record3, record5, record2, record4]
        self.assertEqual(actual, expected)


if __name__ in ['__main__', 'impl.dashboard.dashboard_test']:
    main(
        DashboardTest,
        Dashboard,
        'impl.dashboard',
        'impl/dashboard', {},
        __name__ == '__main__',
        date=DATE_10260602,
        e=ENV)
