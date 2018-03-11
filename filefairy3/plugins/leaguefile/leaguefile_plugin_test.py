#!/usr/bin/env python

import datetime
import jinja2
import importlib
import mock
import os
import re
import unittest
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(_path)
_root = re.sub(r'/plugins/leaguefile', '', _path)
sys.path.append(_root)
from plugins.leaguefile.leaguefile_plugin import LeaguefilePlugin  # noqa
from utils.testing.testing_util import write  # noqa

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
    'end': 'Jan 27 16:00'
}

_fp_started_1 = {
    'size': '100000',
    'start': 'Jan 29 15:00',
    'end': 'Jan 29 15:00'
}

_fp_started_1_ret = {
    'size': '100,000',
    'start': '15:00 Jan 29',
    'end': '15:00 Jan 29'
}

_fp_started_95 = {
    'size': '310000000',
    'start': 'Jan 29 15:00',
    'end': 'Jan 29 19:26'
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
    'size': '336,724,001',
    'start': '12:00 Jan 27',
    'end': '12:00 Jan 27'
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


class LeaguefilePluginTest(unittest.TestCase):
    @mock.patch.object(LeaguefilePlugin, '_render')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.chat_post_message')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.check_output')
    def test_setup__with_empty_stored(self, mock_check, mock_post,
                                      mock_render):
        mock_check.return_value = _check_stored
        data = {'fp': None, 'up': []}
        original = write(_data, data)
        plugin = LeaguefilePlugin()
        plugin._setup()
        actual = write(_data, original)
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
        original = write(_data, data)
        plugin = LeaguefilePlugin()
        plugin._setup()
        actual = write(_data, original)
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
        original = write(_data, data)
        plugin = LeaguefilePlugin()
        plugin._setup()
        actual = write(_data, original)
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
        original = write(_data, data)
        plugin = LeaguefilePlugin()
        plugin._setup()
        actual = write(_data, original)
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
        original = write(_data, data)
        plugin = LeaguefilePlugin()
        plugin._setup()
        actual = write(_data, original)
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
        original = write(_data, data)
        plugin = LeaguefilePlugin()
        plugin._setup()
        actual = write(_data, original)
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
        original = write(_data, data)
        plugin = LeaguefilePlugin()
        plugin._setup()
        actual = write(_data, original)
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
        original = write(_data, data)
        plugin = LeaguefilePlugin()
        plugin._setup()
        actual = write(_data, original)
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
        original = write(_data, data)
        plugin = LeaguefilePlugin()
        plugin._setup()
        actual = write(_data, original)
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
        original = write(_data, data)
        plugin = LeaguefilePlugin()
        plugin._setup()
        actual = write(_data, original)
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
        original = write(_data, data)
        plugin = LeaguefilePlugin()
        plugin._setup()
        actual = write(_data, original)
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
        original = write(_data, data)
        plugin = LeaguefilePlugin()
        plugin._setup()
        ret = plugin._run()
        self.assertTrue(ret)
        actual = write(_data, original)
        expected = {'fp': _fp_started_1, 'up': [_up_stored]}
        self.assertEqual(actual, expected)
        write(_data, actual)
        ret = plugin._run()
        self.assertTrue(ret)
        actual = write(_data, original)
        expected = {'fp': _fp_started_1, 'up': [_up_stored]}
        self.assertEqual(actual, expected)
        write(_data, actual)
        ret = plugin._run()
        self.assertTrue(ret)
        actual = write(_data, original)
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
        original = write(_data, data)
        plugin = LeaguefilePlugin()
        plugin._setup()
        plugin._run()
        actual = write(_data, original)
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
        original = write(_data, data)
        plugin = LeaguefilePlugin()
        plugin._setup()
        plugin._run()
        plugin._run()
        actual = write(_data, original)
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
        original = write(_data, data)
        plugin = LeaguefilePlugin()
        plugin._setup()
        plugin._run()
        plugin._run()
        plugin._run()
        actual = write(_data, original)
        expected = {'fp': None, 'up': [_up_started_stopped, _up_stored]}
        self.assertEqual(actual, expected)
        mock_post.assert_called_once_with('general', 'File is up.')
        calls = [mock.call(), mock.call(), mock.call(), mock.call()]
        mock_render.assert_has_calls(calls)

    @mock.patch('apis.renderable.renderable_api.check_output')
    @mock.patch('plugins.leaguefile.leaguefile_plugin.check_output')
    @mock.patch.object(jinja2.environment.TemplateStream, 'dump')
    def test_render(self, mock_dump, mock_lcheck, mock_rcheck):
        mock_lcheck.side_effect = [_check_stored, _check_started_1]
        data = {'fp': None, 'up': []}
        original = write(_data, data)
        plugin = LeaguefilePlugin()
        plugin.data = {'fp': _fp_started_1, 'up': [_up_stored]}
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
            _fp_started_1_ret,
            'up': [_up_stored_ret]
        }
        self.assertEqual(actual, expected)
        write(_data, original)


class LeaguefilePluginGoldenTest(unittest.TestCase):
    @mock.patch('apis.renderable.renderable_api.datetime')
    @mock.patch.object(LeaguefilePlugin, '_html')
    @mock.patch('apis.renderable.renderable_api.check_output')
    def test_golden__canonical(self, mock_check, mock_html, mock_datetime):
        now = datetime.datetime(1985, 10, 26, 0, 3, 0)
        mock_datetime.datetime.now.return_value = now
        golden = os.path.join(_path, 'goldens/canonical_golden.html')
        mock_html.return_value = golden
        sample = 'plugins.leaguefile.samples.canonical_sample'
        module = importlib.import_module(sample)
        data = getattr(module, 'data')
        ldr = jinja2.FileSystemLoader(os.path.join(_root, 'templates'))
        env = jinja2.Environment(
            loader=ldr, trim_blocks=True, lstrip_blocks=True)
        plugin = LeaguefilePlugin(e=env)
        plugin.data = data
        plugin._render()


if __name__ == '__main__':
    unittest.main()
