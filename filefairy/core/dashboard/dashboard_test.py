#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
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
from core.notify.notify import Notify  # noqa
from core.response.response import Response  # noqa
from util.component.component import anchor  # noqa
from util.component.component import card  # noqa
from util.component.component import table  # noqa
from util.jinja2_.jinja2_ import env  # noqa
from util.json_.json_ import dumps  # noqa
from util.test.test import Test  # noqa
from util.test.test import main  # noqa

_data = Dashboard._data()
_env = env()
_exc = Exception('Disabled foo.')
_now = datetime.datetime(1985, 10, 26, 20, 18, 45)
_now_day = datetime.datetime(1985, 10, 26)
_now_date_encoded = '1985-10-26T20:18:45'
_soon = datetime.datetime(1985, 10, 26, 0, 2, 35)
_soon_day = datetime.datetime(1985, 10, 26)
_soon_date_encoded = '1985-10-26T00:02:35'
_then = datetime.datetime(1985, 10, 26, 0, 2, 30)
_then_day = datetime.datetime(1985, 10, 26)
_then_date_encoded = '1985-10-26T00:02:30'
_then_day_encoded = '1985-10-26T00:00:00'
_yesterday = datetime.datetime(1985, 10, 25, 0, 2, 30)
_yesterday_date_encoded = '1985-10-25T12:55:00'
_yesterday_day_encoded = '1985-10-25T00:00:00'
_cut_day_encoded = '1985-10-19T00:00:00'
_details = {'trace': 'Lorem ipsum'}
_record_error = {
    'pathname': '/home/user/filefairy/path/to/file.py',
    'lineno': 123,
    'levelname': 'ERROR',
    'msg': 'Disabled foo.',
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
_exceptions = [
    card(
        href=(_link + 'path/to/file.py#L123'),
        title='file.py#L123',
        info='Disabled foo.',
        code='Traceback [foo] ...',
        ts='1d ago')
]
_warnings = [
    card(
        href=(_link + 'path/to/file.py#L789'),
        title='file.py#L789',
        info='baz (x6).',
        code='Traceback [baz] ...',
        ts='20h ago')
]
_logs = [
    table(
        clazz='border mt-3 table-fixed',
        hcols=_cols,
        bcols=_cols,
        head=['Saturday, October 26th, 1985', ''],
        body=[[
            '<div class="d-inline-block pr-1">' +
            anchor(_link + 'path/to/file.py#L789', 'file.py#L789') + '</div>' +
            '<div class="d-inline-block">baz (x6).</div>', '00:02'
        ]]),
    table(
        clazz='border mt-3 table-fixed',
        hcols=_cols,
        bcols=_cols,
        head=['Friday, October 25th, 1985', ''],
        body=[[
            '<div class="d-inline-block pr-1">' +
            anchor(_link + 'path/to/file.py#L456', 'file.py#L456') + '</div>' +
            '<div class="d-inline-block">bar (x5).</div>', '12:55'
        ], [
            '<div class="d-inline-block pr-1">' +
            anchor(_link + 'path/to/file.py#L123', 'file.py#L123') + '</div>' +
            '<div class="d-inline-block">Disabled foo.</div>', '12:55'
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
        dashboard = Dashboard(date=_yesterday, e=_env)

        self.mock_open.assert_called_once_with(_data, 'r')
        self.mock_handle.write.assert_not_called()
        self.assertEqual(dashboard.data, data)

        self.reset_mocks()
        self.init_mocks(data)

        return dashboard

    @mock.patch.object(Dashboard, '_log')
    def test_emit__debug(self, mock_log):
        read = {'records': {}}
        dashboard = self.create_dashboard(read)

        handler = LoggingHandler(dashboard)
        logger_ = logging.getLogger('fairylab')
        logger_.addHandler(handler)
        logger_.setLevel(logging.DEBUG)

        logger_.log(logging.DEBUG, 'msg', extra={'output': 'data'})

        self.assertTrue(mock_log.called)
        args, kwargs = mock_log.call_args
        self.assertFalse(args)
        self.assertFalse(kwargs['exc_info'])
        self.assertEqual(kwargs['levelname'], 'DEBUG')
        self.assertEqual(kwargs['msg'], 'msg')
        self.assertEqual(kwargs['name'], 'fairylab')
        self.assertEqual(kwargs['output'], 'data')

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

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
            logger_.log(logging.ERROR, 'msg', exc_info=True)

        self.assertTrue(mock_log.called)
        args, kwargs = mock_log.call_args
        self.assertFalse(args)
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

        logger_.log(logging.INFO, 'msg')

        self.assertTrue(mock_log.called)
        args, kwargs = mock_log.call_args
        self.assertFalse(args)
        self.assertFalse(kwargs['exc_info'])
        self.assertEqual(kwargs['levelname'], 'INFO')
        self.assertEqual(kwargs['msg'], 'msg')
        self.assertEqual(kwargs['name'], 'fairylab')

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(Dashboard, '_retire')
    def test_notify__with_day(self, mock_retire):
        read = {'records': {}}
        dashboard = self.create_dashboard(read)
        response = dashboard._notify_internal(notify=Notify.FAIRYLAB_DAY)
        self.assertEqual(response, Response())

        mock_retire.assert_called_once_with(notify=Notify.FAIRYLAB_DAY)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(Dashboard, '_retire')
    def test_notify__with_other(self, mock_automate):
        read = {'records': {}}
        dashboard = self.create_dashboard(read)
        response = dashboard._notify_internal(notify=Notify.OTHER)
        self.assertEqual(response, Response())

        mock_automate.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    def test_on_message(self):
        read = {'records': {}}
        dashboard = self.create_dashboard(read)
        response = dashboard._on_message_internal(date=_now)
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(Dashboard, '_render')
    def test_setup(self, mock_render):
        read = {'records': {}}
        dashboard = self.create_dashboard(read)
        response = dashboard._setup_internal(date=_now)
        self.assertEqual(response, Response())

        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    def test_shadow(self):
        read = {'records': {}}
        dashboard = self.create_dashboard(read)
        value = dashboard._shadow_internal()
        self.assertEqual(value, [])

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(Dashboard, '_render')
    def test_resolve__with_error(self, mock_render):
        record_old = dict(_record_error, count=1, date=_then_date_encoded)
        read = {'records': {_then_day_encoded: [record_old]}}
        dashboard = self.create_dashboard(read)
        actual = dashboard.resolve('foo', date=_now)
        expected = Response()
        self.assertEqual(actual, expected)

        record_new = dict(
            _record_error, count=1, date=_then_date_encoded, levelname='INFO')
        write = {'records': {_then_day_encoded: [record_new]}}
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_called_once_with(_data, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch.object(Dashboard, '_render')
    def test_resolve__with_info(self, mock_render):
        record_old = dict(_record_info, count=1, date=_then_date_encoded)
        read = {'records': {_then_day_encoded: [record_old]}}
        dashboard = self.create_dashboard(read)
        actual = dashboard.resolve('file', date=_now)
        expected = Response()
        self.assertEqual(actual, expected)

        mock_render.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(Dashboard, '_render')
    def test_resolve__with_warning(self, mock_render):
        record_old = dict(_record_warning, count=1, date=_then_date_encoded)
        read = {'records': {_then_day_encoded: [record_old]}}
        dashboard = self.create_dashboard(read)
        actual = dashboard.resolve('file', date=_now)
        expected = Response()
        self.assertEqual(actual, expected)

        record_new = dict(
            _record_warning,
            count=1,
            date=_then_date_encoded,
            levelname='INFO')
        write = {'records': {_then_day_encoded: [record_new]}}
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_called_once_with(_data, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    def test_home(self):
        error = dict(_record_error, count=1, date=_yesterday_date_encoded)
        info = dict(_record_info, count=5, date=_yesterday_date_encoded)
        warning_yesterday = dict(
            _record_warning, count=2, date=_yesterday_date_encoded)
        warning_then = dict(_record_warning, count=6, date=_then_date_encoded)
        read = {
            'records': {
                _yesterday_day_encoded: [error, info, warning_yesterday],
                _then_day_encoded: [warning_then]
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

    @mock.patch('core.dashboard.dashboard.files_upload')
    @mock.patch.object(Dashboard, '_record')
    @mock.patch('core.dashboard.dashboard.logging.Formatter.formatException')
    @mock.patch('core.dashboard.dashboard.os.getcwd')
    @mock.patch('core.dashboard.dashboard.chat_post_message')
    def test_log__debug(self, mock_chat, mock_cwd, mock_format, mock_record,
                        mock_upload):
        mock_cwd.return_value = '/home/user/filefairy'

        read = {'records': {}}
        dashboard = self.create_dashboard(read)
        e = (Exception, _exc, None)
        dashboard._log(
            exc_info=e,
            levelname='DEBUG',
            lineno=123,
            module='file',
            msg='Call completed.',
            pathname='path/to/file.py',
            output='data')

        mock_chat.assert_called_once_with('testing',
                                          'file.py#L123: Call completed.')
        mock_cwd.assert_called_once_with()
        mock_format.assert_not_called()
        mock_record.assert_not_called()
        mock_upload.assert_called_once_with('data', 'file.log.txt', 'testing')
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch('core.dashboard.dashboard.files_upload')
    @mock.patch.object(Dashboard, '_record')
    @mock.patch('core.dashboard.dashboard.logging.Formatter.formatException')
    @mock.patch('core.dashboard.dashboard.os.getcwd')
    @mock.patch('core.dashboard.dashboard.chat_post_message')
    def test_log__error(self, mock_chat, mock_cwd, mock_format, mock_record,
                        mock_upload):
        mock_cwd.return_value = '/home/user/filefairy'
        mock_format.return_value = 'Traceback [foo] ...'

        read = {'records': {}}
        dashboard = self.create_dashboard(read)
        e = (Exception, _exc, None)
        dashboard._log(
            exc_info=e,
            levelname='ERROR',
            lineno=123,
            module='file',
            msg='Disabled foo.',
            pathname='path/to/file.py')

        mock_chat.assert_called_once_with('testing',
                                          'file.py#L123: Disabled foo.')
        mock_cwd.assert_called_once_with()
        mock_format.assert_called_once_with(dashboard, e)
        mock_record.assert_called_once_with(_record_error)
        mock_upload.assert_called_once_with('Traceback [foo] ...',
                                            'file.log.txt', 'testing')
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch('core.dashboard.dashboard.files_upload')
    @mock.patch.object(Dashboard, '_record')
    @mock.patch('core.dashboard.dashboard.logging.Formatter.formatException')
    @mock.patch('core.dashboard.dashboard.os.getcwd')
    @mock.patch('core.dashboard.dashboard.chat_post_message')
    def test_log__info(self, mock_chat, mock_cwd, mock_format, mock_record,
                       mock_upload):
        mock_cwd.return_value = '/home/user/filefairy'

        read = {'records': {}}
        dashboard = self.create_dashboard(read)
        dashboard._log(
            exc_info=None,
            levelname='INFO',
            lineno=456,
            module='file',
            msg='bar',
            pathname='path/to/file.py')

        mock_chat.assert_not_called()
        mock_cwd.assert_called_once_with()
        mock_format.assert_not_called()
        mock_record.assert_called_once_with(_record_info)
        mock_upload.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch('core.dashboard.dashboard.files_upload')
    @mock.patch.object(Dashboard, '_record')
    @mock.patch('core.dashboard.dashboard.logging.Formatter.formatException')
    @mock.patch('core.dashboard.dashboard.os.getcwd')
    @mock.patch('core.dashboard.dashboard.chat_post_message')
    def test_log__warning_once(self, mock_chat, mock_cwd, mock_format,
                               mock_record, mock_upload):
        mock_cwd.return_value = '/home/user/filefairy'
        mock_format.return_value = 'Traceback [baz] ...'
        mock_record.return_value = 1

        read = {'records': {}}
        dashboard = self.create_dashboard(read)
        e = (Exception, _exc, None)
        dashboard._log(
            exc_info=e,
            levelname='WARNING',
            lineno=789,
            module='file',
            msg='baz',
            pathname='path/to/file.py')

        mock_chat.assert_not_called()
        mock_cwd.assert_called_once_with()
        mock_format.assert_called_once_with(dashboard, e)
        mock_record.assert_called_once_with(_record_warning)
        mock_upload.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch('core.dashboard.dashboard.files_upload')
    @mock.patch.object(Dashboard, '_record')
    @mock.patch('core.dashboard.dashboard.logging.Formatter.formatException')
    @mock.patch('core.dashboard.dashboard.os.getcwd')
    @mock.patch('core.dashboard.dashboard.chat_post_message')
    def test_log__warning_repeated(self, mock_chat, mock_cwd, mock_format,
                                   mock_record, mock_upload):
        mock_cwd.return_value = '/home/user/filefairy'
        mock_format.return_value = 'Traceback [baz] ...'
        mock_record.return_value = 5

        read = {'records': {}}
        dashboard = self.create_dashboard(read)
        e = (Exception, _exc, None)
        dashboard._log(
            exc_info=e,
            levelname='WARNING',
            lineno=789,
            module='file',
            msg='baz',
            pathname='path/to/file.py')

        mock_chat.assert_called_once_with('testing', 'file.py#L789: baz')
        mock_cwd.assert_called_once_with()
        mock_format.assert_called_once_with(dashboard, e)
        mock_record.assert_called_once_with(_record_warning)
        mock_upload.assert_called_once_with('Traceback [baz] ...',
                                            'file.log.txt', 'testing')
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(Dashboard, '_render')
    @mock.patch('core.dashboard.dashboard.datetime')
    def test_record__with_empty(self, mock_datetime, mock_render):
        mock_datetime.datetime.return_value = _then_day
        mock_datetime.datetime.now.return_value = _then

        read = {'records': {}}
        dashboard = self.create_dashboard(read)
        count = dashboard._record(copy.deepcopy(_record_error))
        self.assertEqual(count, 1)

        record_new = dict(_record_error, count=1, date=_then_date_encoded)
        write = {'records': {_then_day_encoded: [record_new]}}
        mock_datetime.datetime.assert_called_once_with(_then.year, _then.month,
                                                       _then.day)
        mock_datetime.datetime.now.assert_called_once_with()
        mock_render.assert_called_once_with(date=_then)
        self.mock_open.assert_called_once_with(_data, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.assertEqual(dashboard.date, _then)

    @mock.patch.object(Dashboard, '_render')
    @mock.patch('core.dashboard.dashboard.datetime')
    def test_record__with_new(self, mock_datetime, mock_render):
        mock_datetime.datetime.return_value = _then_day
        mock_datetime.datetime.now.return_value = _then

        record_old = dict(_record_info, count=1, date=_then_date_encoded)
        read = {'records': {_then_day_encoded: [record_old]}}
        dashboard = self.create_dashboard(read)
        count = dashboard._record(copy.deepcopy(_record_error))
        self.assertEqual(count, 1)

        record_new = dict(_record_error, count=1, date=_then_date_encoded)
        write = {'records': {_then_day_encoded: [record_old, record_new]}}
        mock_datetime.datetime.assert_called_once_with(_then.year, _then.month,
                                                       _then.day)
        mock_datetime.datetime.now.assert_called_once_with()
        mock_render.assert_called_once_with(date=_then)
        self.mock_open.assert_called_once_with(_data, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.assertEqual(dashboard.date, _then)

    @mock.patch.object(Dashboard, '_render')
    @mock.patch('core.dashboard.dashboard.datetime')
    def test_record__with_old_now(self, mock_datetime, mock_render):
        mock_datetime.datetime.return_value = _now_day
        mock_datetime.datetime.now.return_value = _now

        record_old = dict(_record_error, count=1, date=_then_date_encoded)
        read = {'records': {_then_day_encoded: [record_old]}}
        dashboard = self.create_dashboard(read)
        count = dashboard._record(copy.deepcopy(_record_error))
        self.assertEqual(count, 1)

        record_new = dict(_record_error, count=1, date=_now_date_encoded)
        write = {'records': {_then_day_encoded: [record_old, record_new]}}
        mock_datetime.datetime.assert_called_once_with(_now.year, _now.month,
                                                       _now.day)
        mock_datetime.datetime.now.assert_called_once_with()
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_called_once_with(_data, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.assertEqual(dashboard.date, _now)

    @mock.patch.object(Dashboard, '_render')
    @mock.patch('core.dashboard.dashboard.datetime')
    def test_record__with_old_soon(self, mock_datetime, mock_render):
        mock_datetime.datetime.return_value = _soon_day
        mock_datetime.datetime.now.return_value = _soon

        record_old = dict(_record_error, count=1, date=_then_date_encoded)
        read = {'records': {_then_day_encoded: [record_old]}}
        dashboard = self.create_dashboard(read)
        count = dashboard._record(copy.deepcopy(_record_error))
        self.assertEqual(count, 2)

        record_soon = dict(_record_error, count=2, date=_soon_date_encoded)
        write = {'records': {_then_day_encoded: [record_soon]}}
        mock_datetime.datetime.assert_called_once_with(_soon.year, _soon.month,
                                                       _soon.day)
        mock_datetime.datetime.now.assert_called_once_with()
        mock_render.assert_called_once_with(date=_soon)
        self.mock_open.assert_called_once_with(_data, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.assertEqual(dashboard.date, _soon)

    @mock.patch.object(Dashboard, '_render')
    def test_retire__with_cut(self, mock_render):
        record_new = dict(_record_info, count=1, date=_then_day_encoded)
        record_old = dict(_record_info, count=1, date=_cut_day_encoded)
        read = {
            'records': {
                _then_day_encoded: [record_new],
                _cut_day_encoded: [record_old]
            }
        }
        dashboard = self.create_dashboard(read)
        dashboard._retire(date=_now)

        write = {'records': {_then_day_encoded: [record_new]}}
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_called_once_with(_data, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch.object(Dashboard, '_render')
    def test_retire__without_cut(self, mock_render):
        record_new = dict(_record_info, count=1, date=_then_day_encoded)
        record_old = dict(_record_info, count=1, date=_yesterday_day_encoded)
        read = {
            'records': {
                _then_day_encoded: [record_new],
                _yesterday_day_encoded: [record_old]
            }
        }
        dashboard = self.create_dashboard(read)
        dashboard._retire(date=_now)

        mock_render.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()


if __name__ in ['__main__', 'core.dashboard.dashboard_test']:
    _main = __name__ == '__main__'
    _pkg = 'core.dashboard'
    _pth = 'core/dashboard'
    main(DashboardTest, Dashboard, _pkg, _pth, {}, _main, date=_then, e=_env)
