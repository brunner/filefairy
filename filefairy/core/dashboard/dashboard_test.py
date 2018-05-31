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
_now = datetime.datetime(2018, 1, 29, 15, 1, 30)
_dates = [['1985-10-26T00:02:30', 3], ['1985-10-25T00:00:00', 1]]
_details = {'trace': 'Lorem ipsum', 'dates': _dates}
_record = {
    'pathname': 'path/to/file.py',
    'lineno': '456',
    'levelname': 'ERROR',
    'msg': 'FooError',
    'details': {
        '789': _details
    }
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
    def test_emit(self, mock_log):
        read = {'records': {'123': _record}}
        dashboard = self.create_dashboard(read)

        handler = LoggingHandler(dashboard)
        logger_ = logging.getLogger('fairylab')
        logger_.addHandler(handler)
        logger_.setLevel(logging.DEBUG)

        logger_.log(logging.ERROR, 'msg', extra={'a': 1})

        self.assertTrue(mock_log.called)
        args, kwargs = mock_log.call_args
        self.assertFalse(args)
        self.assertEqual(kwargs['name'], 'fairylab')
        self.assertEqual(kwargs['levelname'], 'ERROR')
        self.assertEqual(kwargs['msg'], 'msg')
        self.assertEqual(kwargs['a'], 1)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()


if __name__ in ['__main__', 'core.dashboard.dashboard_test']:
    _main = __name__ == '__main__'
    _pkg = 'core.dashboard'
    _pth = 'core/dashboard'
    main(DashboardTest, Dashboard, _pkg, _pth, {}, _main, date=_now, e=_env)
