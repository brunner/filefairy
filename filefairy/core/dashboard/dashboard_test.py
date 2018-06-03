#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import logging
import os
import re
import sys
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(_path)
_root = re.sub(r'/core/dashboard', '', _path)
sys.path.append(_root)
from core.dashboard.dashboard import Dashboard  # noqa
from core.dashboard.dashboard import LoggingHandler  # noqa
from util.component.component import anchor  # noqa
from util.component.component import card  # noqa
from util.component.component import table  # noqa
from util.jinja2_.jinja2_ import env  # noqa
from util.json_.json_ import dumps  # noqa
from util.test.test import Test  # noqa
from util.test.test import main  # noqa

_data = Dashboard._data()
_env = env()
_exc = Exception('foo')
_now = datetime.datetime(1985, 10, 26, 20, 18, 45)
_now_date_encoded = '1985-10-26T20:18:45'
_then = datetime.datetime(1985, 10, 26, 0, 2, 30)
_then_date_encoded = '1985-10-26T00:02:30'
_then_day_encoded = '1985-10-26T00:00:00'
_yesterday = datetime.datetime(1985, 10, 25, 0, 2, 30)
_yesterday_date_encoded = '1985-10-25T12:55:00'
_yesterday_day_encoded = '1985-10-25T00:00:00'
_details = {'trace': 'Lorem ipsum'}
_record_error = {
    'pathname': '/home/user/filefairy/path/to/file.py',
    'lineno': 123,
    'levelname': 'ERROR',
    'msg': 'foo',
    'exc': 'Traceback [foo] ...',
}
_record_info = {
    'pathname': '/home/user/filefairy/path/to/file.py',
    'lineno': 456,
    'levelname': 'INFO',
    'msg': 'bar',
    'exc': '',
}
_record_warning = {
    'pathname': '/home/user/filefairy/path/to/file.py',
    'lineno': 789,
    'levelname': 'WARNING',
    'msg': 'baz',
    'exc': 'Traceback [baz] ...',
}
_cols = ['', ' class="text-right w-75p"']
_link = 'https://github.com/brunner/orangeandblueleague/blob/master/filefairy/'
_breadcrumbs = [{
    'href': '/fairylab/',
    'name': 'Home'
}, {
    'href': '',
    'name': 'Dashboard'
}]
_exceptions = [card(
    href=(_link + 'path/to/file.py#L123'),
    title='file.py#L123',
    table=table(clazz='table-sm mb-2', bcols=_cols, body=[['foo', '(1)']]),
    code='Traceback [foo] ...',
    ts='1d ago')]
_warnings = [card(
    href=(_link + 'path/to/file.py#L789'),
    title='file.py#L789',
    table=table(clazz='table-sm mb-2', bcols=_cols, body=[['baz', '(2)']]),
    code='Traceback [baz] ...',
    ts='20h ago')]
_logs = [
    table(
        clazz='border mt-3 table-fixed',
        hcols=_cols,
        bcols=_cols,
        head=['Saturday, October 26th, 1985', ''],
        body=[[
            anchor(_link + 'path/to/file.py#L789', 'file.py#L789') + '<br>baz',
            '00:02<br>(2)'
        ]]),
    table(
        clazz='border mt-3 table-fixed',
        hcols=_cols,
        bcols=_cols,
        head=['Friday, October 25th, 1985', ''],
        body=[[
            anchor(_link + 'path/to/file.py#L456', 'file.py#L456') + '<br>bar',
            '12:55<br>(5)'
        ], [
            anchor(_link + 'path/to/file.py#L123', 'file.py#L123') + '<br>foo',
            '12:55<br>(1)'
        ]])
]


class DashboardTest(Test):
    def setUp(self):
        patch_open = mock.patch(
            'api.serializable.serializable.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]

    def reset_mocks(self):
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()

    def create_dashboard(self, data):
        self.init_mocks(data)
        dashboard = Dashboard(date=_then, e=_env)

        self.mock_open.assert_called_once_with(_data, 'r')
        self.mock_handle.write.assert_not_called()
        self.assertEqual(dashboard.data, data)

        self.reset_mocks()
        self.init_mocks(data)

        return dashboard

    @mock.patch.object(Dashboard, '_log')
    def test_emit__exception(self, mock_log):
        read = {'records': {}}
        dashboard = self.create_dashboard(read)

        handler = LoggingHandler(dashboard)
        logger_ = logging.getLogger('fairylab')
        logger_.addHandler(handler)
        logger_.setLevel(logging.DEBUG)

        try:
            raise _exc
        except:
            extra = {'date': _then}
            logger_.log(logging.ERROR, 'msg', exc_info=True, extra=extra)

        self.assertTrue(mock_log.called)
        args, kwargs = mock_log.call_args
        self.assertFalse(args)
        self.assertEqual(kwargs['date'], _then)
        e = (Exception, _exc, _exc.__traceback__)
        self.assertEqual(kwargs['exc_info'], e)
        self.assertEqual(kwargs['levelname'], 'ERROR')
        self.assertEqual(kwargs['msg'], 'msg')
        self.assertEqual(kwargs['name'], 'fairylab')

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(Dashboard, '_log')
    def test_emit__info(self, mock_log):
        read = {'records': {}}
        dashboard = self.create_dashboard(read)

        handler = LoggingHandler(dashboard)
        logger_ = logging.getLogger('fairylab')
        logger_.addHandler(handler)
        logger_.setLevel(logging.DEBUG)

        logger_.log(logging.INFO, 'msg', extra={'date': _then})

        self.assertTrue(mock_log.called)
        args, kwargs = mock_log.call_args
        self.assertFalse(args)
        self.assertEqual(kwargs['date'], _then)
        self.assertFalse(kwargs['exc_info'])
        self.assertEqual(kwargs['levelname'], 'INFO')
        self.assertEqual(kwargs['msg'], 'msg')
        self.assertEqual(kwargs['name'], 'fairylab')

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    def test_home(self):
        error = dict(_record_error, count=1, date=_yesterday_date_encoded)
        info = dict(_record_info, count=5, date=_yesterday_date_encoded)
        warning = dict(_record_warning, count=2, date=_then_date_encoded)
        read = {
            'records': {
                _yesterday_day_encoded: [error, info],
                _then_day_encoded: [warning]
            }
        }
        dashboard = self.create_dashboard(read)
        actual = dashboard._home(date=_now)
        expected = {
            'breadcrumbs': _breadcrumbs,
            'exceptions': _exceptions,
            'warnings': _warnings,
            'logs': _logs
        }
        self.assertEqual(actual, expected)

    @mock.patch.object(Dashboard, '_record')
    @mock.patch('core.dashboard.dashboard.logging.Formatter.formatException')
    @mock.patch('core.dashboard.dashboard.os.getcwd')
    def test_log__error(self, mock_cwd, mock_format, mock_record):
        mock_cwd.return_value = '/home/user/filefairy'
        mock_format.return_value = 'Traceback [foo] ...'

        read = {'records': {}}
        dashboard = self.create_dashboard(read)
        e = (Exception, _exc, None)
        dashboard._log(
            date=_then,
            exc_info=e,
            levelname='ERROR',
            lineno=123,
            msg='foo',
            pathname='path/to/file.py')

        mock_cwd.assert_called_once_with()
        mock_format.assert_called_once_with(dashboard, e)
        mock_record.assert_called_once_with(_then, _record_error)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(Dashboard, '_record')
    @mock.patch('core.dashboard.dashboard.logging.Formatter')
    @mock.patch('core.dashboard.dashboard.os.getcwd')
    def test_log__info(self, mock_cwd, mock_formatter, mock_record):
        mock_cwd.return_value = '/home/user/filefairy'

        read = {'records': {}}
        dashboard = self.create_dashboard(read)
        dashboard._log(
            date=_then,
            exc_info=None,
            levelname='INFO',
            lineno=456,
            msg='bar',
            pathname='path/to/file.py')

        mock_cwd.assert_called_once_with()
        mock_formatter.format_exception.assert_not_called()
        mock_record.assert_called_once_with(_then, _record_info)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(Dashboard, '_record')
    @mock.patch('core.dashboard.dashboard.logging.Formatter.formatException')
    @mock.patch('core.dashboard.dashboard.os.getcwd')
    def test_log__warning(self, mock_cwd, mock_format, mock_record):
        mock_cwd.return_value = '/home/user/filefairy'
        mock_format.return_value = 'Traceback [baz] ...'

        read = {'records': {}}
        dashboard = self.create_dashboard(read)
        e = (Exception, _exc, None)
        dashboard._log(
            date=_then,
            exc_info=e,
            levelname='WARNING',
            lineno=789,
            msg='baz',
            pathname='path/to/file.py')

        mock_cwd.assert_called_once_with()
        mock_format.assert_called_once_with(dashboard, e)
        mock_record.assert_called_once_with(_then, _record_warning)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(Dashboard, '_render')
    def test_record__with_empty(self, mock_render):
        read = {'records': {}}
        dashboard = self.create_dashboard(read)
        dashboard._record(_then, _record_error)

        record_new = dict(_record_error, count=1, date=_then_date_encoded)
        write = {'records': {_then_day_encoded: [record_new]}}
        mock_render.assert_called_once_with(date=_then)
        self.mock_open.assert_called_once_with(_data, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch.object(Dashboard, '_render')
    def test_record__with_new(self, mock_render):
        record_old = dict(_record_info, count=1, date=_then_date_encoded)
        read = {'records': {_then_day_encoded: [record_old]}}
        dashboard = self.create_dashboard(read)
        dashboard._record(_then, _record_error)

        record_new = dict(_record_error, count=1, date=_then_date_encoded)
        write = {'records': {_then_day_encoded: [record_old, record_new]}}
        mock_render.assert_called_once_with(date=_then)
        self.mock_open.assert_called_once_with(_data, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch.object(Dashboard, '_render')
    def test_record__with_old(self, mock_render):
        record_old = dict(_record_error, count=1, date=_then_date_encoded)
        read = {'records': {_then_day_encoded: [record_old]}}
        dashboard = self.create_dashboard(read)
        dashboard._record(_now, _record_error)

        record_new = dict(_record_error, count=2, date=_now_date_encoded)
        write = {'records': {_then_day_encoded: [record_new]}}
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_called_once_with(_data, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')


if __name__ in ['__main__', 'core.dashboard.dashboard_test']:
    _main = __name__ == '__main__'
    _pkg = 'core.dashboard'
    _pth = 'core/dashboard'
    main(DashboardTest, Dashboard, _pkg, _pth, {}, _main, date=_then, e=_env)
