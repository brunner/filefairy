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
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import pre  # noqa
from common.elements.elements import row  # noqa
from common.elements.elements import table  # noqa
from common.jinja2_.jinja2_ import env  # noqa
from common.json_.json_ import dumps  # noqa
from common.test.test import Test  # noqa
from common.test.test import main  # noqa
from impl.dashboard.dashboard import Dashboard  # noqa
from types_.notify.notify import Notify  # noqa
from types_.response.response import Response  # noqa

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


def create_kwargs(pathname, lineno, levelname, msg, exc_info):
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


def create_record(pathname, lineno, levelname, msg, exc, date):
    return {
        'pathname': pathname,
        'lineno': lineno,
        'levelname': levelname,
        'msg': msg,
        'exc': exc,
        'date': encode_datetime(date)
    }


def create_warning(pathname, lineno, levelname, msg, exc, date, count):
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
        chat_post_message_patch = mock.patch(
            'impl.dashboard.dashboard.chat_post_message')
        self.addCleanup(chat_post_message_patch.stop)
        self.chat_post_message_ = chat_post_message_patch.start()

        files_upload_patch = mock.patch(
            'impl.dashboard.dashboard.files_upload')
        self.addCleanup(files_upload_patch.stop)
        self.files_upload_ = files_upload_patch.start()

        open_patch = mock.patch('common.io_.io_.open', create=True)
        self.addCleanup(open_patch.stop)
        self.open_ = open_patch.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.open_handle_ = mo()
        self.open_.side_effect = [mo.return_value]

    def reset_mocks(self):
        self.open_handle_.write.reset_mock()

    def create_dashboard(self, data, warnings=None):
        self.init_mocks(data)
        dashboard = Dashboard(date=DATE_10250007, e=ENV)

        self.assertEqual(dashboard.data, data)

        self.reset_mocks()
        self.init_mocks(data)

        if warnings:
            dashboard.warnings = warnings

        return dashboard

    def test_init(self):
        data = {'logs': {}}
        dashboard = self.create_dashboard(data)

        self.assertFalse(len(dashboard.warnings))
        self.assertNotCalled(self.chat_post_message_, self.files_upload_,
                             self.open_handle_.write)

    @mock.patch.object(Dashboard, 'get_dashboard_html')
    def test_render_data(self, get_dashboard_html_):
        dashboard_html = {'exceptions': []}
        get_dashboard_html_.return_value = dashboard_html

        data = {'logs': {}}
        dashboard = self.create_dashboard(data)
        actual = dashboard._render_data(date=DATE_10260602)
        expected = [('dashboard/index.html', '', 'dashboard.html',
                     dashboard_html)]
        self.assertEqual(actual, expected)

        get_dashboard_html_.assert_called_once_with(date=DATE_10260602)
        self.assertNotCalled(self.chat_post_message_, self.files_upload_,
                             self.open_handle_.write)

    @mock.patch.object(Dashboard, 'cleanup')
    def test_notify__fairylab_day(self, cleanup_):
        data = {'logs': {}}
        dashboard = self.create_dashboard(data)
        response = dashboard._notify_internal(date=DATE_10260602,
                                              notify=Notify.FILEFAIRY_DAY)
        self.assertEqual(response, Response())

        cleanup_.assert_called_once_with(date=DATE_10260602,
                                         notify=Notify.FILEFAIRY_DAY)
        self.assertNotCalled(self.chat_post_message_, self.files_upload_,
                             self.open_handle_.write)

    @mock.patch.object(Dashboard, 'cleanup')
    def test_notify__with_other(self, cleanup_):
        data = {'logs': {}}
        dashboard = self.create_dashboard(data)
        response = dashboard._notify_internal(date=DATE_10260602,
                                              notify=Notify.OTHER)
        self.assertEqual(response, Response())

        self.assertNotCalled(cleanup_, self.chat_post_message_,
                             self.open_handle_.write, self.files_upload_)

    @mock.patch.object(Dashboard, '_render')
    def test_cleanup(self, _render_):
        old_date = encode_datetime(DATE_10190000)
        new_date = encode_datetime(DATE_10260000)
        error = create_record(PATH, 123, 'ERROR', 'foo', '...', DATE_10260602)
        info = create_record(PATH, 456, 'INFO', 'bar', '', DATE_10250007)
        warning = create_warning(PATH, 789, 'WARNING', 'baz', '...',
                                 DATE_10260602, 1)

        old_data = {'logs': {old_date: [info], new_date: [error]}}
        dashboard = self.create_dashboard(old_data, [warning])
        dashboard.cleanup(date=DATE_10260602)
        self.assertEqual(dashboard.warnings, [])

        new_data = {'logs': {new_date: [error]}}
        _render_.assert_called_once_with(date=DATE_10260602, log=False)
        self.open_handle_.write.assert_called_once_with(dumps(new_data) + '\n')
        self.assertNotCalled(self.chat_post_message_, self.files_upload_)

    @mock.patch('impl.dashboard.dashboard.os.getcwd')
    @mock.patch.object(Dashboard, 'emit_warning')
    @mock.patch.object(Dashboard, 'emit_log')
    @mock.patch.object(Dashboard, 'emit_alert')
    @mock.patch('impl.dashboard.dashboard.datetime_now')
    def test_emit__debug(self, datetime_now_, emit_alert_, emit_log_,
                         emit_warning_, getcwd_):
        datetime_now_.return_value = DATE_10260602
        getcwd_.return_value = '/home/pi/filefairy/'

        data = {'logs': {}}
        kwargs = create_kwargs('path/to/module.py', 55, 'DEBUG', 'foo', None)
        dashboard = self.create_dashboard(data)
        dashboard.emit(**kwargs)

        path = '/home/pi/filefairy/path/to/module.py'
        record = create_record(path, 55, 'DEBUG', 'foo', '', DATE_10260602)
        emit_alert_.assert_called_once_with(record, **kwargs)
        self.assertNotCalled(emit_log_, emit_warning_, self.chat_post_message_,
                             self.open_handle_.write, self.files_upload_)

    @mock.patch('impl.dashboard.dashboard.os.getcwd')
    @mock.patch.object(Dashboard, 'emit_warning')
    @mock.patch.object(Dashboard, 'emit_log')
    @mock.patch.object(Dashboard, 'emit_alert')
    @mock.patch('impl.dashboard.dashboard.datetime_now')
    def test_emit__error(self, datetime_now_, emit_alert_, emit_log_,
                         emit_warning_, getcwd_):
        getcwd_.return_value = '/home/pi/filefairy/'
        datetime_now_.return_value = DATE_10260602

        data = {'logs': {}}
        kwargs = create_kwargs('path/to/module.py', 123, 'ERROR', 'foo', EXC)
        dashboard = self.create_dashboard(data)
        dashboard.emit(**kwargs)

        path = '/home/pi/filefairy/path/to/module.py'
        record = create_record(path, 123, 'ERROR', 'foo', 'Exception',
                               DATE_10260602)
        emit_alert_.assert_called_once_with(record, **kwargs)
        emit_log_.assert_called_once_with(record)
        self.assertNotCalled(emit_warning_, self.chat_post_message_,
                             self.open_handle_.write, self.files_upload_)

    @mock.patch('impl.dashboard.dashboard.os.getcwd')
    @mock.patch.object(Dashboard, 'emit_warning')
    @mock.patch.object(Dashboard, 'emit_log')
    @mock.patch.object(Dashboard, 'emit_alert')
    @mock.patch('impl.dashboard.dashboard.datetime_now')
    def test_emit__info(self, datetime_now_, emit_alert_, emit_log_,
                        emit_warning_, getcwd_):
        getcwd_.return_value = '/home/pi/filefairy/'
        datetime_now_.return_value = DATE_10260602

        data = {'logs': {}}
        kwargs = create_kwargs('path/to/module.py', 456, 'INFO', 'bar', None)
        dashboard = self.create_dashboard(data)
        dashboard.emit(**kwargs)

        path = '/home/pi/filefairy/path/to/module.py'
        record = create_record(path, 456, 'INFO', 'bar', '', DATE_10260602)
        emit_log_.assert_called_once_with(record)
        self.assertNotCalled(emit_alert_, emit_warning_,
                             self.chat_post_message_, self.open_handle_.write,
                             self.files_upload_)

    @mock.patch('impl.dashboard.dashboard.os.getcwd')
    @mock.patch.object(Dashboard, 'emit_warning')
    @mock.patch.object(Dashboard, 'emit_log')
    @mock.patch.object(Dashboard, 'emit_alert')
    @mock.patch('impl.dashboard.dashboard.datetime_now')
    def test_emit__warning(self, datetime_now_, emit_alert_, emit_log_,
                           emit_warning_, getcwd_):
        getcwd_.return_value = '/home/pi/filefairy/'
        datetime_now_.return_value = DATE_10260602

        data = {'logs': {}}
        kwargs = create_kwargs('path/to/module.py', 789, 'WARNING', 'baz', EXC)
        dashboard = self.create_dashboard(data)
        dashboard.emit(**kwargs)

        path = '/home/pi/filefairy/path/to/module.py'
        record = create_record(path, 789, 'WARNING', 'baz', 'Exception',
                               DATE_10260602)
        emit_warning_.assert_called_once_with(record, **kwargs)
        self.assertNotCalled(emit_alert_, emit_log_, self.chat_post_message_,
                             self.open_handle_.write, self.files_upload_)

    def test_emit_alert(self):
        path = '/home/pi/filefairy/path/to/module.py'
        record = create_record(path, 55, 'DEBUG', 'foo', '', DATE_10260602)
        kwargs = create_kwargs('path/to/module.py', 55, 'DEBUG', 'foo', None)

        data = {'logs': {}}
        dashboard = self.create_dashboard(data)
        dashboard.emit_alert(record, **kwargs)

        self.chat_post_message_.assert_called_once_with(
            'testing', 'module.py#L55: foo')
        self.files_upload_.assert_has_calls([
            mock.call('stderr', 'module.stderr.txt', 'testing'),
            mock.call('stdout', 'module.stdout.txt', 'testing'),
        ])
        self.assertNotCalled(self.open_handle_.write)

    @mock.patch.object(Dashboard, '_render')
    def test_emit_log__other(self, _render_):
        new = encode_datetime(DATE_10260000)
        error = create_record(PATH, 123, 'ERROR', 'foo', '...', DATE_10260602)

        old_data = {'logs': {new: [error]}}
        record = create_record(PATH, 456, 'INFO', 'bar', '', DATE_10260602)
        dashboard = self.create_dashboard(old_data)
        dashboard.emit_log(record)

        new_data = {'logs': {new: [error, record]}}
        _render_.assert_called_once_with(date=DATE_10260602, log=False)
        self.open_handle_.write.assert_called_once_with(dumps(new_data) + '\n')
        self.assertNotCalled(self.chat_post_message_, self.files_upload_)

    @mock.patch.object(Dashboard, 'emit_alert')
    def test_emit_warning__alert(self, emit_alert_):
        data = {'logs': {}}
        kwargs = create_kwargs('path/to/module.py', 789, 'W', 'baz', EXC)
        record = create_record(PATH, 789, 'W', 'baz', 'E', DATE_10260604)
        warning = create_warning(PATH, 789, 'W', 'baz', 'E', DATE_10260602, 9)
        dashboard = self.create_dashboard(data, [warning])
        dashboard.emit_warning(record, **kwargs)

        warning = create_warning(PATH, 789, 'W', 'baz', 'E', DATE_10260604, 10)
        self.assertEqual(dashboard.warnings, [warning])
        emit_alert_.assert_called_once_with(record, **kwargs)
        self.assertNotCalled(self.chat_post_message_, self.files_upload_,
                             self.open_handle_.write)

    @mock.patch.object(Dashboard, 'emit_alert')
    def test_emit_warning__multiple(self, emit_alert_):
        data = {'logs': {}}
        kwargs = create_kwargs('path/to/module.py', 789, 'W', 'baz', EXC)
        record = create_record(PATH, 789, 'W', 'baz', 'E', DATE_10260604)
        warning = create_warning(PATH, 789, 'W', 'baz', 'E', DATE_10260602, 1)
        dashboard = self.create_dashboard(data, [warning])
        dashboard.emit_warning(record, **kwargs)

        warning = create_warning(PATH, 789, 'W', 'baz', 'E', DATE_10260604, 2)
        self.assertEqual(dashboard.warnings, [warning])
        self.assertNotCalled(emit_alert_, self.chat_post_message_,
                             self.open_handle_.write, self.files_upload_)

    @mock.patch.object(Dashboard, 'emit_alert')
    def test_emit_warning__single(self, emit_alert_):
        data = {'logs': {}}
        kwargs = create_kwargs('path/to/module.py', 789, 'W', 'baz', EXC)
        record = create_record(PATH, 789, 'W', 'baz', 'E', DATE_10260602)
        dashboard = self.create_dashboard(data, [])
        dashboard.emit_warning(record, **kwargs)

        warning = create_warning(PATH, 789, 'W', 'baz', 'E', DATE_10260602, 1)
        self.assertEqual(dashboard.warnings, [warning])
        self.assertNotCalled(emit_alert_, self.chat_post_message_,
                             self.open_handle_.write, self.files_upload_)

    def test_get_dashboard_html(self):
        old = encode_datetime(DATE_10250000)
        new = encode_datetime(DATE_10260000)
        path = '/home/pi/filefairy/path/to/module.py'
        error = create_record(path, 123, 'ERROR', 'foo', '...', DATE_10260602)
        info = create_record(path, 456, 'INFO', 'bar', '', DATE_10250007)

        data = {'logs': {old: [info], new: [error]}}
        dashboard = self.create_dashboard(data)

        link = 'https://github.com/brunner/filefairy/blob/master/'
        logs = [
            table(clazz='border mb-3',
                  hcols=[col(clazz='font-weight-bold text-dark', colspan='3')],
                  bcols=[
                      col(clazz='css-style-w-150px'),
                      col(),
                      col(clazz='text-right css-style-w-75px')
                  ],
                  fcols=[col(colspan='3')],
                  head=[
                      row(cells=[cell(content='Saturday, October 26th, 1985')])
                  ],
                  body=[
                      row(cells=[
                          cell(content=anchor(link + 'path/to/module.py#L123',
                                              'module.py#L123')),
                          cell(content='foo'),
                          cell(content='06:02')
                      ])
                  ],
                  foot=[row(cells=[cell(content=pre('...'))])]),
            table(
                clazz='border mb-3',
                hcols=[col(clazz='font-weight-bold text-dark', colspan='3')],
                bcols=[
                    col(clazz='css-style-w-150px'),
                    col(),
                    col(clazz='text-right css-style-w-75px')
                ],
                head=[row(cells=[cell(content='Friday, October 25th, 1985')])],
                body=[
                    row(cells=[
                        cell(content=anchor(link + 'path/to/module.py#L456',
                                            'module.py#L456')),
                        cell(content='bar'),
                        cell(content='00:07')
                    ])
                ])
        ]
        actual = dashboard.get_dashboard_html(date=DATE_10260602)
        expected = {'logs': logs}
        self.assertEqual(actual, expected)
        self.assertNotCalled(self.chat_post_message_, self.files_upload_,
                             self.open_handle_.write)

    def test_get_record_link(self):
        link = 'https://github.com/brunner/filefairy/blob/master/'
        path = '/home/pi/filefairy/path/to/module.py'
        record = create_record(path, 55, 'DEBUG', 'foo', '', DATE_10260602)

        data = {'logs': {}}
        dashboard = self.create_dashboard(data)
        actual = dashboard.get_record_link(record)
        expected = link + 'path/to/module.py#L55'
        self.assertEqual(actual, expected)
        self.assertNotCalled(self.chat_post_message_, self.files_upload_,
                             self.open_handle_.write)

    def test_get_record_title(self):
        path = '/home/pi/filefairy/path/to/module.py'
        record = create_record(path, 55, 'DEBUG', 'foo', '', DATE_10260602)

        data = {'logs': {}}
        dashboard = self.create_dashboard(data)
        actual = dashboard.get_record_title(record)
        expected = 'module.py#L55'
        self.assertEqual(actual, expected)
        self.assertNotCalled(self.chat_post_message_, self.files_upload_,
                             self.open_handle_.write)

    def test_sort_records(self):
        path1 = '/home/pi/filefairy/path/to/a.py'
        path2 = '/home/pi/filefairy/path/to/b.py'
        record1 = create_record(path1, 55, 'DEBUG', 'foo', '', DATE_10260602)
        record2 = create_record(path1, 110, 'DEBUG', 'foo', '', DATE_10260604)
        record3 = create_record(path1, 110, 'DEBUG', 'foo', '', DATE_10260602)
        record4 = create_record(path2, 110, 'DEBUG', 'foo', '', DATE_10260604)
        record5 = create_record(path2, 55, 'DEBUG', 'foo', '', DATE_10260602)
        records = [record1, record2, record3, record4, record5]

        data = {'logs': {}}
        dashboard = self.create_dashboard(data)
        actual = list(sorted(records, key=dashboard.sort_records))
        expected = [record1, record3, record5, record2, record4]
        self.assertEqual(actual, expected)


if __name__ in ['__main__', 'impl.dashboard.dashboard_test']:
    main(DashboardTest,
         Dashboard,
         'impl.dashboard',
         'impl/dashboard', {},
         __name__ == '__main__',
         date=DATE_10260602,
         e=ENV)
