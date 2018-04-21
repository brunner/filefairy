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
DATE_ENCODED = '2022-10-28T00:00:00'
SCORES = '10/28/2022 MAJOR LEAGUE BASEBALL Final Scores\n*<a href=\"' + \
         'https://orangeandblueleaguebaseball.com/StatsLab/reports/news/' + \
         'html/box_scores/game_box_25041.html\">Los Angeles 5, Seattle 3</a>*'


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

    def test_notify__with_download(self):
        read = {'finished': False, 'scores': {}, 'updated': False}
        plugin = self.create_plugin(read)
        ret = plugin._notify_internal(activity=ActivityEnum.DOWNLOAD)
        self.assertFalse(ret)

        write = {'finished': True, 'scores': {}, 'updated': False}
        self.mock_open.assert_called_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    def test_notify__with_none(self):
        read = {'finished': False, 'scores': {}, 'updated': False}
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
        read = {'finished': True, 'scores': {}, 'updated': False}
        plugin = self.create_plugin(read)
        ret = plugin._on_message_internal(obj=obj)
        self.assertEqual(ret, ActivityEnum.BASE)

        write = {'finished': False, 'scores': {}, 'updated': False}
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
        read = {'finished': False, 'scores': {}, 'updated': False}
        plugin = self.create_plugin(read)
        ret = plugin._on_message_internal(obj=obj)
        self.assertEqual(ret, ActivityEnum.BASE)

        mock_clear.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(StatsplusPlugin, '_scores')
    def test_on_message__with_scores(self, mock_scores):
        obj = {
            'channel': 'C7JSGHW8G',
            'text': SCORES,
            'ts': '1000.789',
            'user': 'U1234',
            'bot_id': 'B7KJ3362Y'
        }
        read = {'finished': False, 'scores': {}, 'updated': False}
        plugin = self.create_plugin(read)
        ret = plugin._on_message_internal(obj=obj)
        self.assertEqual(ret, ActivityEnum.BASE)

        mock_scores.assert_called_once_with(SCORES)
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
        read = {'finished': True, 'scores': {}, 'updated': False}
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
        read = {'finished': True, 'scores': {}, 'updated': False}
        plugin = self.create_plugin(read)
        ret = plugin._on_message_internal(obj=obj)
        self.assertEqual(ret, ActivityEnum.NONE)

        mock_clear.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    def test_run__with_updated_true(self):
        read = {'finished': False, 'scores': {}, 'updated': True}
        plugin = self.create_plugin(read)
        ret = plugin._run_internal()
        self.assertEqual(ret, ActivityEnum.NONE)

        write = {'finished': False, 'scores': {}, 'updated': False}
        self.mock_open.assert_called_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    def test_run__with_updated_false(self):
        read = {'finished': False, 'scores': {}, 'updated': False}
        plugin = self.create_plugin(read)
        ret = plugin._run_internal()
        self.assertEqual(ret, ActivityEnum.NONE)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    def test_setup(self):
        read = {'finished': False, 'scores': {}, 'updated': False}
        plugin = self.create_plugin(read)
        plugin._setup_internal()

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    def test_clear(self):
        read = {
            'finished': False,
            'scores': {
                DATE_ENCODED: SCORES
            },
            'updated': False
        }
        plugin = self.create_plugin(read)
        plugin._clear()

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.assertEqual(plugin.data['scores'], {})

    def test_scores(self):
        read = {'finished': False, 'scores': {}, 'updated': False}
        plugin = self.create_plugin(read)
        plugin._scores(SCORES)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.assertEqual(plugin.data['scores'], {DATE_ENCODED: SCORES})
        self.assertTrue(plugin.data['updated'])


if __name__ in ['__main__', 'plugins.statsplus.statsplus_plugin_test']:
    _main = __name__ == '__main__'
    _pkg = 'plugins.statsplus'
    _pth = 'plugins/statsplus'
    main(StatsplusPluginTest, StatsplusPlugin, _pkg, _pth, {}, _main)
