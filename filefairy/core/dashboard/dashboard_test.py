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
from util.jinja2_.jinja2_ import env  # noqa
from util.json_.json_ import dumps  # noqa
from util.test.test import Test  # noqa
from util.test.test import main  # noqa

_data = Dashboard._data()
_env = env()
_exc = Exception('foo')
_now = datetime.datetime(2018, 1, 29, 15, 1, 30)
_now_encoded = '2018-01-29T15:01:30'
_then = datetime.datetime(1985, 10, 26, 0, 2, 30)
_then_encoded = '1985-10-26T00:02:30'
_details = {'trace': 'Lorem ipsum'}
_record_error = {
    'pathname': '/home/path/to/file.py',
    'lineno': 123,
    'levelname': 'ERROR',
    'msg': 'foo',
    'exc': 'Traceback [foo] ...',
}
_record_error_encoded = {
    'pathname': '/home/path/to/file.py',
    'lineno': '123',
    'levelname': 'ERROR',
    'msg': 'foo',
    'exc': 'Traceback [foo] ...',
}
_record_info = {
    'pathname': '/home/path/to/file.py',
    'lineno': 456,
    'levelname': 'INFO',
    'msg': 'bar',
    'exc': '',
}
_record_info_encoded = {
    'pathname': '/home/path/to/file.py',
    'lineno': '456',
    'levelname': 'INFO',
    'msg': 'bar',
    'exc': '',
}
_record_warning = {
    'pathname': '/home/path/to/file.py',
    'lineno': 789,
    'levelname': 'WARNING',
    'msg': 'baz',
    'exc': 'Traceback [baz] ...',
}
_record_warning_encoded = {
    'pathname': '/home/path/to/file.py',
    'lineno': '789',
    'levelname': 'WARNING',
    'msg': 'baz',
    'exc': 'Traceback [baz] ...',
}


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
        dashboard = Dashboard(date=_now, e=_env)

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

    @mock.patch.object(Dashboard, '_record')
    @mock.patch('core.dashboard.dashboard.logging.Formatter.formatException')
    @mock.patch('core.dashboard.dashboard.os.getcwd')
    def test_log__error(self, mock_cwd, mock_format, mock_record):
        mock_cwd.return_value = '/home'
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
        mock_record.assert_called_once_with(_record_error)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(Dashboard, '_record')
    @mock.patch('core.dashboard.dashboard.logging.Formatter')
    @mock.patch('core.dashboard.dashboard.os.getcwd')
    def test_log__info(self, mock_cwd, mock_formatter, mock_record):
        mock_cwd.return_value = '/home'

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
        mock_record.assert_called_once_with(_record_info)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(Dashboard, '_record')
    @mock.patch('core.dashboard.dashboard.logging.Formatter.formatException')
    @mock.patch('core.dashboard.dashboard.os.getcwd')
    def test_log__warning(self, mock_cwd, mock_format, mock_record):
        mock_cwd.return_value = '/home'
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
        mock_record.assert_called_once_with(_record_warning)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()


if __name__ in ['__main__', 'core.dashboard.dashboard_test']:
    _main = __name__ == '__main__'
    _pkg = 'core.dashboard'
    _pth = 'core/dashboard'
    main(DashboardTest, Dashboard, _pkg, _pth, {}, _main, date=_now, e=_env)
