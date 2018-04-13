#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import mock
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(_path)
_root = re.sub(r'/plugins/leaguefile', '', _path)
sys.path.append(_root)
from enums.activity.activity_enum import ActivityEnum  # noqa
from plugins.leaguefile.leaguefile_plugin import LeaguefilePlugin  # noqa
from utils.component.component_util import card, table  # noqa
from utils.jinja2.jinja2_util import env  # noqa
from utils.json.json_util import dumps  # noqa
from utils.test.test_util import main, TestUtil  # noqa

_data = LeaguefilePlugin._data()
DATA = LeaguefilePlugin._data()
CHECK_FILEPART = ('100000', 'Jan 29 14:00',
                  'orange_and_blue_league_baseball.tar.gz.filepart', True)
CHECK_UP_FALSE = ('328706052', 'Jan 29 15:55',
                  'orange_and_blue_league_baseball.tar.gz', False)
CHECK_UP_TRUE = ('345678901', 'Jan 27 12:00',
                 'orange_and_blue_league_baseball.tar.gz', True)
FILEPART = {
    'start': 'Jan 29 14:00',
    'size': '100000',
    'end': 'Jan 29 14:00',
    'now': '2018-01-29T15:01:30'
}
UP_FILEPART = {
    'start': 'Jan 29 14:00',
    'size': '328706052',
    'end': 'Jan 29 14:00',
    'date': 'Jan 29 15:55'
}
UP_NOW = {
    'start': 'Jan 29 15:55',
    'size': '328706052',
    'end': 'Jan 29 15:55',
    'date': 'Jan 29 15:55'
}
UP_THEN = {
    'start': 'Jan 27 12:00',
    'size': '345678901',
    'end': 'Jan 27 12:00',
    'date': 'Jan 27 12:00'
}
HOME = {'breadcrumbs': [], 'fp': {}, 'up': {}}
INDEX = 'html/fairylab/leaguefile/index.html'
NOW = datetime.datetime(2018, 1, 29, 15, 1, 30)
THEN = datetime.datetime(2018, 1, 27, 12, 0, 0)
LS_WITH_FILEPART = """total 321012
-rwxrwxrwx 1 user user       421 Aug 19 13:48 index.html
-rwxrwxrwx 1 user user 345678901 Jan 27 12:00 orange_and_blue_league_baseball.tar.gz
-rwxrwxrwx 1 user user 100000 Jan 29 14:00 orange_and_blue_league_baseball.tar.gz.filepart
"""
LS_WITHOUT_FILEPART = """total 321012
-rwxrwxrwx 1 user user       421 Aug 19 13:48 index.html
-rwxrwxrwx 1 user user 328706052 Jan 29 15:55 orange_and_blue_league_baseball.tar.gz
"""
BREADCRUMBS = [{
    'href': '/fairylab/',
    'name': 'Home'
}, {
    'href': '',
    'name': 'Leaguefile'
}]


class LeaguefilePluginTest(TestUtil):
    def setUp(self):
        patch_open = mock.patch(
            'apis.serializable.serializable_api.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()
        patch_chat = mock.patch(
            'plugins.leaguefile.leaguefile_plugin.chat_post_message')
        self.addCleanup(patch_chat.stop)
        self.mock_chat = patch_chat.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]

    def reset_mocks(self):
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()
        self.mock_chat.reset_mock()

    def create_plugin(self, data):
        self.init_mocks(data)
        plugin = LeaguefilePlugin(e=env())

        self.mock_open.assert_called_once_with(DATA, 'r')
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.assertEqual(plugin.data, data)

        self.reset_mocks()
        self.init_mocks(data)

        return plugin

    def test_notify(self):
        read = {'fp': None, 'up': []}
        plugin = self.create_plugin(read)
        ret = plugin._notify_internal()
        self.assertFalse(ret)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

    def test_on_message(self):
        read = {'fp': None, 'up': []}
        plugin = self.create_plugin(read)
        ret = plugin._on_message_internal()
        self.assertEqual(ret, ActivityEnum.NONE)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

    @mock.patch.object(LeaguefilePlugin, '_render')
    @mock.patch.object(LeaguefilePlugin, '_check')
    def test_run__with_valid_input(self, mock_check, mock_render):
        mock_check.return_value = iter([CHECK_FILEPART, CHECK_UP_TRUE])

        read = {'fp': None, 'up': []}
        plugin = self.create_plugin(read)
        ret = plugin._run_internal(date=NOW)
        self.assertEqual(ret, ActivityEnum.UPLOAD)

        write = {'fp': FILEPART, 'up': []}
        mock_check.assert_called_once_with()
        mock_render.assert_called_once_with(date=NOW)
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_called_with(
            'fairylab',
            'File upload started.',
            attachments=plugin._attachments())

    @mock.patch.object(LeaguefilePlugin, '_render')
    @mock.patch.object(LeaguefilePlugin, '_check')
    def test_run__with_no_filepart_change(self, mock_check, mock_render):
        mock_check.return_value = iter([CHECK_FILEPART, CHECK_UP_TRUE])

        read = {'fp': FILEPART, 'up': [UP_THEN]}
        plugin = self.create_plugin(read)
        ret = plugin._run_internal(date=NOW)
        self.assertEqual(ret, ActivityEnum.BASE)

        mock_check.assert_called_once_with()
        mock_render.assert_called_once_with(date=NOW)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

    @mock.patch.object(LeaguefilePlugin, '_render')
    @mock.patch.object(LeaguefilePlugin, '_check')
    def test_run__with_no_up_change(self, mock_check, mock_render):
        mock_check.return_value = iter([CHECK_UP_FALSE])

        read = {'fp': None, 'up': [UP_THEN]}
        plugin = self.create_plugin(read)
        ret = plugin._run_internal(date=NOW)
        self.assertEqual(ret, ActivityEnum.NONE)

        mock_check.assert_called_once_with()
        mock_render.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

    @mock.patch.object(LeaguefilePlugin, '_render')
    @mock.patch.object(LeaguefilePlugin, '_check')
    def test_run__with_empty_filepart(self, mock_check, mock_render):
        mock_check.return_value = iter([CHECK_UP_FALSE])

        read = {'fp': FILEPART, 'up': []}
        plugin = self.create_plugin(read)
        ret = plugin._run_internal(date=NOW)
        self.assertEqual(ret, ActivityEnum.FILE)

        write = {'fp': None, 'up': [UP_FILEPART]}
        mock_check.assert_called_once_with()
        mock_render.assert_called_once_with(date=NOW)
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        calls = [
            mock.call('general', 'File is up.'),
            mock.call(
                'fairylab',
                'File upload completed.',
                attachments=plugin._attachments())
        ]
        self.mock_chat.assert_has_calls(calls)

    @mock.patch.object(LeaguefilePlugin, '_home')
    def test_render(self, mock_home):
        mock_home.return_value = HOME

        read = {'fp': None, 'up': []}
        plugin = self.create_plugin(read)
        ret = plugin._render_internal(date=NOW)
        self.assertEqual(ret, [(INDEX, '', 'leaguefile.html', HOME)])

        mock_home.assert_called_once_with(date=NOW)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

    @mock.patch.object(LeaguefilePlugin, '_render')
    @mock.patch.object(LeaguefilePlugin, '_check')
    def test_setup__with_valid_input(self, mock_check, mock_render):
        mock_check.return_value = iter([CHECK_FILEPART, CHECK_UP_TRUE])

        read = {'fp': None, 'up': []}
        plugin = self.create_plugin(read)
        plugin._setup_internal(date=NOW)

        write = {'fp': FILEPART, 'up': [UP_THEN]}
        mock_check.assert_called_once_with()
        mock_render.assert_called_once_with(date=NOW)
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_not_called()

    @mock.patch.object(LeaguefilePlugin, '_render')
    @mock.patch.object(LeaguefilePlugin, '_check')
    def test_setup__with_no_filepart_change(self, mock_check, mock_render):
        mock_check.return_value = iter([CHECK_FILEPART, CHECK_UP_TRUE])

        read = {'fp': FILEPART, 'up': [UP_THEN]}
        plugin = self.create_plugin(read)
        plugin._setup_internal(date=NOW)

        mock_check.assert_called_once_with()
        mock_render.assert_called_once_with(date=NOW)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

    @mock.patch.object(LeaguefilePlugin, '_render')
    @mock.patch.object(LeaguefilePlugin, '_check')
    def test_setup__with_no_up_change(self, mock_check, mock_render):
        mock_check.return_value = iter([CHECK_UP_TRUE])

        read = {'fp': None, 'up': [UP_THEN]}
        plugin = self.create_plugin(read)
        plugin._setup_internal(date=NOW)

        mock_check.assert_called_once_with()
        mock_render.assert_called_once_with(date=NOW)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

    @mock.patch.object(LeaguefilePlugin, '_render')
    @mock.patch.object(LeaguefilePlugin, '_check')
    def test_setup__with_empty_filepart(self, mock_check, mock_render):
        mock_check.return_value = iter([CHECK_UP_FALSE])

        read = {'fp': FILEPART, 'up': []}
        plugin = self.create_plugin(read)
        plugin._setup_internal(date=NOW)

        write = {'fp': None, 'up': [UP_NOW]}
        mock_check.assert_called_once_with()
        mock_render.assert_called_once_with(date=NOW)
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_not_called()

    @mock.patch.object(LeaguefilePlugin, '_render')
    @mock.patch.object(LeaguefilePlugin, '_check')
    def test_setup__with_new_up(self, mock_check, mock_render):
        mock_check.return_value = iter([CHECK_UP_FALSE])

        read = {'fp': FILEPART, 'up': [UP_THEN]}
        plugin = self.create_plugin(read)
        plugin._setup_internal(date=NOW)

        write = {'fp': None, 'up': [UP_NOW, UP_THEN]}
        mock_check.assert_called_once_with()
        mock_render.assert_called_once_with(date=NOW)
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_not_called()

    def test_date(self):
        s = 'Jan 29 15:55'
        actual = LeaguefilePlugin._date(s)
        expected = 'Jan 29'
        self.assertEqual(actual, expected)

    def test_size(self):
        s = '328706052'
        actual = LeaguefilePlugin._size(s)
        expected = '328,706,052'
        self.assertEqual(actual, expected)

    def test_time(self):
        s = 'Jan 29 14:00'
        e = 'Jan 29 15:55'
        actual = LeaguefilePlugin._time(s, e)
        expected = '1h 55m'
        self.assertEqual(actual, expected)

    @mock.patch('plugins.leaguefile.leaguefile_plugin.server', 'SERVER')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.check_output')
    def test_check__with_filepart(self, mock_check):
        mock_check.return_value = LS_WITH_FILEPART

        actual = LeaguefilePlugin._check()
        expected = iter([CHECK_FILEPART, CHECK_UP_TRUE])
        self.assertItemsEqual(actual, expected)

        mock_check.assert_called_once_with([
            'ssh', 'brunnerj@SERVER',
            'ls -l /var/www/html/StatsLab/league_file'
        ])
        self.mock_open.assert_not_called()
        self.mock_chat.assert_not_called()

    @mock.patch('plugins.leaguefile.leaguefile_plugin.server', 'SERVER')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.check_output')
    def test_check__without_filepart(self, mock_check):
        mock_check.return_value = LS_WITHOUT_FILEPART

        actual = LeaguefilePlugin._check()
        expected = iter([CHECK_UP_FALSE])
        self.assertItemsEqual(actual, expected)

        mock_check.assert_called_once_with([
            'ssh', 'brunnerj@SERVER',
            'ls -l /var/www/html/StatsLab/league_file'
        ])
        self.mock_open.assert_not_called()
        self.mock_chat.assert_not_called()

    def test_home__with_empty(self):
        read = {'fp': None, 'up': []}
        plugin = self.create_plugin(read)
        ret = plugin._home(date=NOW)
        up = table(cols=['', '', ''], head=['Date', 'Time', 'Size'], body=[])
        expected = {'breadcrumbs': BREADCRUMBS, 'fp': None, 'up': up}
        self.assertEqual(ret, expected)

    def test_home__with_filepart(self):
        read = {'fp': FILEPART, 'up': []}
        plugin = self.create_plugin(read)
        ret = plugin._home(date=NOW)
        fp = card(
            title='Jan 29',
            table=table(
                clazz='table-sm',
                cols=['', 'w-100'],
                body=[['Time: ', '0m'], ['Size: ', '100,000']]),
            ts='0s ago',
            success='ongoing')
        up = table(cols=['', '', ''], head=['Date', 'Time', 'Size'], body=[])
        expected = {'breadcrumbs': BREADCRUMBS, 'fp': fp, 'up': up}
        self.assertEqual(ret, expected)

    def test_home__with_up(self):
        read = {'fp': None, 'up': [UP_THEN]}
        plugin = self.create_plugin(read)
        ret = plugin._home(date=NOW)
        up = table(
            cols=['', '', ''],
            head=['Date', 'Time', 'Size'],
            body=[['Jan 27', '0m', '345,678,901']])
        expected = {'breadcrumbs': BREADCRUMBS, 'fp': None, 'up': up}
        self.assertEqual(ret, expected)


if __name__ in ['__main__', 'plugins.leaguefile.leaguefile_plugin_test']:
    _main = __name__ == '__main__'
    _pkg = 'plugins.leaguefile'
    _pth = 'plugins/leaguefile'
    main(LeaguefilePluginTest, LeaguefilePlugin, _pkg, _pth, {}, _main)
