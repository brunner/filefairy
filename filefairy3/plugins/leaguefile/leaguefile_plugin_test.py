#!/usr/bin/env python

import jinja2
import mock
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(_path)
_root = re.sub(r'/plugins/leaguefile', '', _path)
sys.path.append(_root)
from plugins.leaguefile.leaguefile_plugin import LeaguefilePlugin  # noqa
from utils.jinja2.jinja2_util import env  # noqa
from utils.test.test_util import main, TestUtil  # noqa

_data = LeaguefilePlugin._data()

_check_stored = """total 321012
-rwxrwxrwx 1 user user       421 Aug 19 13:48 index.html
-rwxrwxrwx 1 user user 336724001 Jan 27 12:00 orange_and_blue_league_baseball.tar.gz
"""

_check_started_1 = """total 321012
-rwxrwxrwx 1 user user       421 Aug 19 13:48 index.html
-rwxrwxrwx 1 user user 345678901 Jan 27 12:00 orange_and_blue_league_baseball.tar.gz
-rwxrwxrwx 1 user user 100000 Jan 29 15:00 orange_and_blue_league_baseball.tar.gz.filepart
"""

_check_started_95 = """total 321012
-rwxrwxrwx 1 user user       421 Aug 19 13:48 index.html
-rwxrwxrwx 1 user user 345678901 Jan 27 12:00 orange_and_blue_league_baseball.tar.gz
-rwxrwxrwx 1 user user 310000000 Jan 29 19:26 orange_and_blue_league_baseball.tar.gz.filepart
"""

_check_stopped = """total 321012
-rwxrwxrwx 1 user user       421 Aug 19 13:48 index.html
-rwxrwxrwx 1 user user 328706052 Jan 29 14:55 orange_and_blue_league_baseball.tar.gz
"""

_fp_stored = {
    'size': '300000000',
    'start': 'Jan 27 12:05',
    'end': 'Jan 27 16:00',
    'now': ''
}

_fp_started_1 = {
    'size': '100000',
    'start': 'Jan 29 15:00',
    'end': 'Jan 29 15:00',
    'now': ''
}

_fp_started_95 = {
    'size': '310000000',
    'start': 'Jan 29 15:00',
    'end': 'Jan 29 19:26',
    'now': ''
}

_fp_started_95_ret = {
    'date': 'Jan 29',
    'size': '310,000,000',
    'time': '4h 26m',
    'delta': '30s ago'
}

_up_started_1 = {
    'size': '345678901',
    'start': 'Jan 27 12:00',
    'end': 'Jan 27 12:00',
    'date': 'Jan 27 12:00'
}

_up_started_stopped = {
    'size': '328706052',
    'start': 'Jan 29 15:00',
    'end': 'Jan 29 19:26',
    'date': 'Jan 29 14:55'
}

_up_stopped = {
    'size': '328706052',
    'start': 'Jan 29 14:55',
    'end': 'Jan 29 14:55',
    'date': 'Jan 29 14:55'
}

_up_stored = {
    'size': '336724001',
    'start': 'Jan 27 12:00',
    'end': 'Jan 27 12:00',
    'date': 'Jan 27 12:00'
}

_up_stored_ret = {
    'date': 'Jan 27',
    'size': '336,724,001',
    'time': '0m',
}

_up_stored_diff = {
    'size': '336724001',
    'start': 'Jan 24 15:35',
    'end': 'Jan 24 20:00',
    'date': 'Jan 24 15:30'
}

_up_stored_started = {
    'size': '345678901',
    'start': 'Jan 27 12:05',
    'end': 'Jan 27 16:00',
    'date': 'Jan 27 12:00'
}

_up_stored_stopped = {
    'size': '345678901',
    'start': 'Jan 29 15:00',
    'end': 'Jan 29 20:00',
    'date': 'Jan 29 14:55'
}


class LeaguefilePluginTest(TestUtil):
    @mock.patch.object(LeaguefilePlugin, '_render')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.chat_post_message')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.check_output')
    def test_setup__with_empty_stored(self, mock_check, mock_post,
                                      mock_render):
        mock_check.return_value = _check_stored
        data = {'fp': None, 'up': []}
        original = self.write(_data, data)
        plugin = LeaguefilePlugin(e=env())
        plugin._setup()
        actual = self.write(_data, original)
        expected = {'fp': None, 'up': [_up_stored]}
        self.assertEqual(actual, expected)
        mock_post.assert_not_called()
        mock_render.assert_called_once_with()

    @mock.patch.object(LeaguefilePlugin, '_render')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.chat_post_message')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.check_output')
    def test_setup__with_empty_started(self, mock_check, mock_post,
                                       mock_render):
        mock_check.return_value = _check_started_1
        data = {'fp': None, 'up': []}
        original = self.write(_data, data)
        plugin = LeaguefilePlugin(e=env())
        plugin._setup()
        actual = self.write(_data, original)
        expected = {'fp': _fp_started_1, 'up': [_up_started_1]}
        self.assertEqual(actual, expected)
        mock_post.assert_not_called()
        mock_render.assert_called_once_with()

    @mock.patch.object(LeaguefilePlugin, '_render')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.chat_post_message')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.check_output')
    def test_setup__with_fp_started(self, mock_check, mock_post, mock_render):
        mock_check.return_value = _check_started_1
        data = {'fp': _fp_stored, 'up': []}
        original = self.write(_data, data)
        plugin = LeaguefilePlugin(e=env())
        plugin._setup()
        actual = self.write(_data, original)
        expected = {'fp': _fp_started_1, 'up': [_up_started_1]}
        self.assertEqual(actual, expected)
        mock_post.assert_not_called()
        mock_render.assert_called_once_with()

    @mock.patch.object(LeaguefilePlugin, '_render')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.chat_post_message')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.check_output')
    def test_setup__with_up_started_diff_date(self, mock_check, mock_post,
                                              mock_render):
        mock_check.return_value = _check_started_1
        data = {'fp': None, 'up': [_up_stored_diff]}
        original = self.write(_data, data)
        plugin = LeaguefilePlugin(e=env())
        plugin._setup()
        actual = self.write(_data, original)
        expected = {
            'fp': _fp_started_1,
            'up': [_up_started_1, _up_stored_diff]
        }
        self.assertEqual(actual, expected)
        mock_post.assert_not_called()
        mock_render.assert_called_once_with()

    @mock.patch.object(LeaguefilePlugin, '_render')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.chat_post_message')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.check_output')
    def test_setup__with_up_started_same_date(self, mock_check, mock_post,
                                              mock_render):
        mock_check.return_value = _check_started_1
        data = {'fp': None, 'up': [_up_stored_started]}
        original = self.write(_data, data)
        plugin = LeaguefilePlugin(e=env())
        plugin._setup()
        actual = self.write(_data, original)
        expected = {'fp': _fp_started_1, 'up': [_up_stored_started]}
        self.assertEqual(actual, expected)
        mock_post.assert_not_called()
        mock_render.assert_called_once_with()

    @mock.patch.object(LeaguefilePlugin, '_render')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.chat_post_message')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.check_output')
    def test_setup__with_both_started(self, mock_check, mock_post,
                                      mock_render):
        mock_check.return_value = _check_started_1
        data = {'fp': _fp_stored, 'up': [_up_stored_diff]}
        original = self.write(_data, data)
        plugin = LeaguefilePlugin(e=env())
        plugin._setup()
        actual = self.write(_data, original)
        expected = {
            'fp': _fp_started_1,
            'up': [_up_started_1, _up_stored_diff]
        }
        self.assertEqual(actual, expected)
        mock_post.assert_not_called()
        mock_render.assert_called_once_with()

    @mock.patch.object(LeaguefilePlugin, '_render')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.chat_post_message')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.check_output')
    def test_setup__with_empty_stopped(self, mock_check, mock_post,
                                       mock_render):
        mock_check.return_value = _check_stopped
        data = {'fp': None, 'up': []}
        original = self.write(_data, data)
        plugin = LeaguefilePlugin(e=env())
        plugin._setup()
        actual = self.write(_data, original)
        expected = {'fp': None, 'up': [_up_stopped]}
        self.assertEqual(actual, expected)
        mock_post.assert_not_called()
        mock_render.assert_called_once_with()

    @mock.patch.object(LeaguefilePlugin, '_render')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.chat_post_message')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.check_output')
    def test_setup__with_fp_stopped(self, mock_check, mock_post, mock_render):
        mock_check.return_value = _check_stopped
        data = {'fp': _fp_stored, 'up': []}
        original = self.write(_data, data)
        plugin = LeaguefilePlugin(e=env())
        plugin._setup()
        actual = self.write(_data, original)
        expected = {'fp': None, 'up': [_up_stopped]}
        self.assertEqual(actual, expected)
        mock_post.assert_not_called()
        mock_render.assert_called_once_with()

    @mock.patch.object(LeaguefilePlugin, '_render')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.chat_post_message')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.check_output')
    def test_setup__with_up_stopped_diff_date(self, mock_check, mock_post,
                                              mock_render):
        mock_check.return_value = _check_stopped
        data = {'fp': None, 'up': [_up_stored_diff]}
        original = self.write(_data, data)
        plugin = LeaguefilePlugin(e=env())
        plugin._setup()
        actual = self.write(_data, original)
        expected = {'fp': None, 'up': [_up_stopped, _up_stored_diff]}
        self.assertEqual(actual, expected)
        mock_post.assert_not_called()
        mock_render.assert_called_once_with()

    @mock.patch.object(LeaguefilePlugin, '_render')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.chat_post_message')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.check_output')
    def test_setup__with_up_stopped_same_date(self, mock_check, mock_post,
                                              mock_render):
        mock_check.return_value = _check_stopped
        data = {'fp': None, 'up': [_up_stored_stopped]}
        original = self.write(_data, data)
        plugin = LeaguefilePlugin(e=env())
        plugin._setup()
        actual = self.write(_data, original)
        expected = {'fp': None, 'up': [_up_stored_stopped]}
        self.assertEqual(actual, expected)
        mock_post.assert_not_called()
        mock_render.assert_called_once_with()

    @mock.patch.object(LeaguefilePlugin, '_render')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.chat_post_message')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.check_output')
    def test_setup__with_both_stopped(self, mock_check, mock_post,
                                      mock_render):
        mock_check.return_value = _check_stopped
        data = {'fp': _fp_stored, 'up': [_up_stored_diff]}
        original = self.write(_data, data)
        plugin = LeaguefilePlugin(e=env())
        plugin._setup()
        actual = self.write(_data, original)
        expected = {'fp': None, 'up': [_up_stopped, _up_stored_diff]}
        self.assertEqual(actual, expected)
        mock_post.assert_not_called()
        mock_render.assert_called_once_with()

    @mock.patch.object(LeaguefilePlugin, '_render')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.chat_post_message')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.check_output')
    def test_run__returns(self, mock_check, mock_post, mock_render):
        mock_check.side_effect = [
            _check_stored, _check_started_1, _check_started_1,
            _check_started_95
        ]
        data = {'fp': None, 'up': []}
        original = self.write(_data, data)
        plugin = LeaguefilePlugin(e=env())
        plugin._setup()
        ret = plugin._run()
        self.assertTrue(ret)
        actual = self.write(_data, original)
        expected = {'fp': _fp_started_1, 'up': [_up_stored]}
        self.assertEqual(actual, expected)
        self.write(_data, actual)
        ret = plugin._run()
        self.assertTrue(ret)
        actual = self.write(_data, original)
        expected = {'fp': _fp_started_1, 'up': [_up_stored]}
        self.assertEqual(actual, expected)
        self.write(_data, actual)
        ret = plugin._run()
        self.assertTrue(ret)
        actual = self.write(_data, original)
        expected = {'fp': _fp_started_95, 'up': [_up_stored]}
        self.assertEqual(actual, expected)
        mock_post.assert_not_called()
        mock_render.assert_has_calls([mock.call(), mock.call(), mock.call()])

    @mock.patch.object(LeaguefilePlugin, '_render')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.chat_post_message')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.check_output')
    def test_run__with_stored_started_fp1(self, mock_check, mock_post,
                                          mock_render):
        mock_check.side_effect = [_check_stored, _check_started_1]
        data = {'fp': None, 'up': []}
        original = self.write(_data, data)
        plugin = LeaguefilePlugin(e=env())
        plugin._setup()
        plugin._run()
        actual = self.write(_data, original)
        expected = {'fp': _fp_started_1, 'up': [_up_stored]}
        self.assertEqual(actual, expected)
        mock_post.assert_not_called()
        calls = [mock.call(), mock.call()]
        mock_render.assert_has_calls(calls)

    @mock.patch.object(LeaguefilePlugin, '_render')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.chat_post_message')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.check_output')
    def test_run__with_stored_started_fp95(self, mock_check, mock_post,
                                           mock_render):
        mock_check.side_effect = [
            _check_stored, _check_started_1, _check_started_95
        ]
        data = {'fp': None, 'up': []}
        original = self.write(_data, data)
        plugin = LeaguefilePlugin(e=env())
        plugin._setup()
        plugin._run()
        plugin._run()
        actual = self.write(_data, original)
        expected = {'fp': _fp_started_95, 'up': [_up_stored]}
        self.assertEqual(actual, expected)
        mock_post.assert_not_called()
        calls = [mock.call(), mock.call(), mock.call()]
        mock_render.assert_has_calls(calls)

    @mock.patch.object(LeaguefilePlugin, '_render')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.chat_post_message')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.check_output')
    def test_run__with_stored_stopped(self, mock_check, mock_post,
                                      mock_render):
        mock_check.side_effect = [
            _check_stored, _check_started_1, _check_started_95, _check_stopped
        ]
        data = {'fp': None, 'up': []}
        original = self.write(_data, data)
        plugin = LeaguefilePlugin(e=env())
        plugin._setup()
        plugin._run()
        plugin._run()
        plugin._run()
        actual = self.write(_data, original)
        expected = {'fp': None, 'up': [_up_started_stopped, _up_stored]}
        self.assertEqual(actual, expected)
        mock_post.assert_called_once_with('general', 'File is up.')
        calls = [mock.call(), mock.call(), mock.call(), mock.call()]
        mock_render.assert_has_calls(calls)

    @mock.patch('apis.renderable.renderable_api.check_output')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.check_output')
    @mock.patch.object(jinja2.environment.TemplateStream, 'dump')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.delta')
    def test_render(self, mock_delta, mock_dump, mock_lcheck, mock_rcheck):
        mock_delta.return_value = '30s ago'
        mock_lcheck.side_effect = [_check_stored, _check_started_95]
        data = {'fp': None, 'up': []}
        original = self.write(_data, data)
        plugin = LeaguefilePlugin(e=env())
        plugin.data = {'fp': _fp_started_95, 'up': [_up_stored]}
        actual = plugin._render_internal()
        expected = {
            'title':
            'leaguefile',
            'breadcrumbs': [{
                'href': '/fairylab/',
                'name': 'Home'
            }, {
                'href': '',
                'name': 'Leaguefile'
            }],
            'fp':
            _fp_started_95_ret,
            'up': [_up_stored_ret]
        }
        self.assertEqual(actual, expected)
        self.write(_data, original)


if __name__ == '__main__':
    main(LeaguefilePluginTest, LeaguefilePlugin, 'plugins.leaguefile', _path)
