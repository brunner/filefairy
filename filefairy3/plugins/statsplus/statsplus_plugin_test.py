#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mock
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(_path)
_root = re.sub(r'/plugins/statsplus', '', _path)
sys.path.append(_root)
from enums.activity.activity_enum import ActivityEnum  # noqa
from plugins.statsplus.statsplus_plugin import StatsplusPlugin  # noqa
from utils.jinja2.jinja2_util import env  # noqa
from utils.json.json_util import dumps  # noqa
from utils.test.test_util import main, TestUtil  # noqa

DATA = StatsplusPlugin._data()
LIVE_EMPTY = '0-0'
LIVE_FINISHED = '3-3'


class StatsplusPluginTest(TestUtil):
    def setUp(self):
        patch_open = mock.patch(
            'apis.serializable.serializable_api.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]

    def reset_mocks(self):
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()

    def create_plugin(self, data):
        self.init_mocks(data)
        plugin = StatsplusPlugin(e=env())

        self.mock_open.assert_called_once_with(DATA, 'r')
        self.mock_handle.write.assert_not_called()

        self.reset_mocks()
        self.init_mocks(data)

        return plugin

    def test_notify__with_file(self):
        live = {t: LIVE_EMPTY for t in range(31, 61)}
        read = {'finished': False, 'live': live}
        plugin = self.create_plugin(read)
        ret = plugin._notify_internal(activity=ActivityEnum.FILE)
        self.assertFalse(ret)

        write = {'finished': True, 'live': live}
        self.mock_open.assert_called_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    def test_notify__with_none(self):
        live = {t: LIVE_EMPTY for t in range(31, 61)}
        read = {'finished': False, 'live': live}
        plugin = self.create_plugin(read)
        ret = plugin._notify_internal(activity=ActivityEnum.NONE)
        self.assertFalse(ret)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(StatsplusPlugin, '_clear')
    def test_on_message__with_finished_true(self, mock_clear):
        obj = {
            'channel': 'C7JSGHW8G',
            'text': 'text',
            'ts': '1000.789',
            'user': 'U1234',
            'bot_id': 'B7KJ3362Y'
        }
        live = {t: LIVE_EMPTY for t in range(31, 61)}
        read = {'finished': True, 'live': live}
        plugin = self.create_plugin(read)
        ret = plugin._on_message_internal(obj=obj)
        self.assertEqual(ret, ActivityEnum.BASE)

        write = {'finished': False, 'live': live}
        mock_clear.assert_called_once_with()
        self.mock_open.assert_called_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch.object(StatsplusPlugin, '_clear')
    def test_on_message__with_finished_false(self, mock_clear):
        obj = {
            'channel': 'C7JSGHW8G',
            'text': 'text',
            'ts': '1000.789',
            'user': 'U1234',
            'bot_id': 'B7KJ3362Y'
        }
        live = {t: LIVE_EMPTY for t in range(31, 61)}
        read = {'finished': False, 'live': live}
        plugin = self.create_plugin(read)
        ret = plugin._on_message_internal(obj=obj)
        self.assertEqual(ret, ActivityEnum.BASE)

        mock_clear.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(StatsplusPlugin, '_clear')
    def test_on_message__with_invalid_bot_id(self, mock_clear):
        obj = {
            'channel': 'G3SUFLMK4',
            'text': 'text',
            'ts': '1000.789',
            'user': 'U1234',
        }
        live = {t: LIVE_EMPTY for t in range(31, 61)}
        read = {'finished': True, 'live': live}
        plugin = self.create_plugin(read)
        ret = plugin._on_message_internal(obj=obj)
        self.assertEqual(ret, ActivityEnum.NONE)

        mock_clear.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(StatsplusPlugin, '_clear')
    def test_on_message__with_invalid_channel(self, mock_clear):
        obj = {
            'channel': 'G3SUFLMK4',
            'text': 'text',
            'ts': '1000.789',
            'user': 'U1234',
            'bot_id': 'B7KJ3362Y'
        }
        live = {t: LIVE_EMPTY for t in range(31, 61)}
        read = {'finished': True, 'live': live}
        plugin = self.create_plugin(read)
        ret = plugin._on_message_internal(obj=obj)
        self.assertEqual(ret, ActivityEnum.NONE)

        mock_clear.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    def test_run(self):
        live = {t: LIVE_EMPTY for t in range(31, 61)}
        read = {'finished': False, 'live': live}
        plugin = self.create_plugin(read)
        ret = plugin._run_internal()
        self.assertEqual(ret, ActivityEnum.NONE)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    def test_setup(self):
        live = {t: LIVE_EMPTY for t in range(31, 61)}
        read = {'finished': False, 'live': live}
        plugin = self.create_plugin(read)
        plugin._setup_internal()

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()


if __name__ in ['__main__', 'plugins.statsplus.statsplus_plugin_test']:
    _main = __name__ == '__main__'
    _pkg = 'plugins.statsplus'
    _pth = 'plugins/statsplus'
    main(StatsplusPluginTest, StatsplusPlugin, _pkg, _pth, {}, _main)
