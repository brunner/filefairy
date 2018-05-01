#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import mock
import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/plugins/git', '', _path))
from plugins.git.git_plugin import GitPlugin  # noqa
from values.notify.notify_value import NotifyValue  # noqa
from values.response.response_value import ResponseValue  # noqa

NOW = datetime.datetime(1985, 10, 27, 0, 0, 0)
THEN = datetime.datetime(1985, 10, 26, 0, 2, 30)


class GitPluginTest(unittest.TestCase):
    def setUp(self):
        patch_log = mock.patch('plugins.git.git_plugin.log')
        self.addCleanup(patch_log.stop)
        self.mock_log = patch_log.start()
        patch_check = mock.patch('plugins.git.git_plugin.check_output')
        self.addCleanup(patch_check.stop)
        self.mock_check = patch_check.start()

    def reset_mocks(self):
        self.mock_log.reset_mock()
        self.mock_check.reset_mock()

    def create_plugin(self, day=0):
        plugin = GitPlugin()

        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

        self.reset_mocks()

        return plugin

    @mock.patch('plugins.git.git_plugin.threading.Thread')
    @mock.patch.object(GitPlugin, 'automate')
    def test_notify__with_day(self, mock_automate, mock_thread):
        plugin = self.create_plugin()
        value = plugin._notify_internal(notify=NotifyValue.FAIRYLAB_DAY)
        self.assertFalse(value)

        mock_thread.assert_called_once_with(target=mock_automate)
        mock_thread.return_value.start.assert_called_once_with()
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    @mock.patch('plugins.git.git_plugin.threading.Thread')
    @mock.patch.object(GitPlugin, 'automate')
    def test_notify__with_other(self, mock_automate, mock_thread):
        plugin = self.create_plugin()
        value = plugin._notify_internal(notify=NotifyValue.OTHER)
        self.assertFalse(value)

        mock_thread.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    def test_on_message(self):
        plugin = self.create_plugin()
        response = plugin._on_message_internal()
        self.assertEqual(response, ResponseValue())

        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    def test_run(self):
        plugin = self.create_plugin()
        response = plugin._run_internal(date=THEN)
        self.assertEqual(response, ResponseValue())

        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    def test_setup(self):
        plugin = self.create_plugin()
        plugin._setup_internal(date=THEN)

        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    def test_shadow(self):
        plugin = self.create_plugin()
        value = plugin._shadow_internal()
        self.assertEqual(value, {})

        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    def test_add(self):
        plugin = self.create_plugin()

        self.mock_check.return_value = ''
        self.mock_log.return_value = ''

        response = plugin.add(**{'a1': '', 'v': True})
        self.assertEqual(response, ResponseValue(notify=[NotifyValue.BASE]))

        self.mock_check.assert_called_once_with(['git', 'add', '.'])
        self.mock_log.assert_called_once_with(
            plugin._name(), **{
                'a1': '',
                'c': '',
                's': 'Call completed: \'git add .\'.',
                'v': True
            })

    @mock.patch.object(GitPlugin, 'push')
    @mock.patch.object(GitPlugin, 'commit')
    @mock.patch.object(GitPlugin, 'add')
    def test_automate(self, mock_add, mock_commit, mock_push):
        plugin = self.create_plugin()
        value = plugin.automate(date=NOW)
        self.assertEqual(value, ResponseValue(notify=[NotifyValue.BASE]))

        mock_add.assert_called_once_with(date=NOW)
        mock_commit.assert_called_once_with(date=NOW)
        mock_push.assert_called_once_with(date=NOW)
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    def test_commit(self):
        plugin = self.create_plugin()

        self.mock_check.return_value = '[master 0abcd0a] Auto...\n1 files\n'
        self.mock_log.return_value = '[master 0abcd0a] Auto...\n1 files'

        response = plugin.commit(**{'a1': '', 'v': True})
        self.assertEqual(response, ResponseValue(notify=[NotifyValue.BASE]))

        self.mock_check.assert_called_once_with(
            ['git', 'commit', '-m', 'Automated data push.'])
        self.mock_log.assert_called_once_with(
            plugin._name(), **{
                'a1': '',
                'c': '[master 0abcd0a] Auto...\n1 files',
                's':
                'Call completed: \'git commit -m "Automated data push."\'.',
                'v': True
            })

    def test_pull(self):
        plugin = self.create_plugin()

        self.mock_check.return_value = 'remote: Counting...\nUnpacking...\n'
        self.mock_log.return_value = 'remote: Counting...\nUnpacking...'

        response = plugin.pull(**{'a1': '', 'v': True})
        self.assertEqual(response, ResponseValue(notify=[NotifyValue.BASE]))

        self.mock_check.assert_called_once_with(['git', 'pull'])
        self.mock_log.assert_called_once_with(
            plugin._name(), **{
                'a1': '',
                'c': 'remote: Counting...\nUnpacking...',
                's': 'Call completed: \'git pull\'.',
                'v': True
            })

    def test_push(self):
        plugin = self.create_plugin()

        self.mock_check.return_value = 'Counting...\nCompressing...\n'
        self.mock_log.return_value = 'Counting...\nCompressing...'

        response = plugin.push(**{'a1': '', 'v': True})
        self.assertEqual(response, ResponseValue(notify=[NotifyValue.BASE]))

        self.mock_check.assert_called_once_with(['git', 'push'])
        self.mock_log.assert_called_once_with(
            plugin._name(), **{
                'a1': '',
                'c': 'Counting...\nCompressing...',
                's': 'Call completed: \'git push\'.',
                'v': True
            })

    def test_reset(self):
        plugin = self.create_plugin()

        self.mock_check.return_value = ''
        self.mock_log.return_value = ''

        response = plugin.reset(**{'a1': '', 'v': True})
        self.assertEqual(response, ResponseValue(notify=[NotifyValue.BASE]))

        self.mock_check.assert_called_once_with(['git', 'reset', '--hard'])
        self.mock_log.assert_called_once_with(
            plugin._name(), **{
                'a1': '',
                'c': '',
                's': 'Call completed: \'git reset --hard\'.',
                'v': True
            })

    def test_status(self):
        plugin = self.create_plugin()

        self.mock_check.return_value = 'On branch master\nYour branch...\n'
        self.mock_log.return_value = 'On branch master\nYour branch...'

        response = plugin.status(**{'a1': '', 'v': True})
        self.assertEqual(response, ResponseValue(notify=[NotifyValue.BASE]))

        self.mock_check.assert_called_once_with(['git', 'status'])
        self.mock_log.assert_called_once_with(
            plugin._name(), **{
                'a1': '',
                'c': 'On branch master\nYour branch...',
                's': 'Call completed: \'git status\'.',
                'v': True
            })


if __name__ == '__main__':
    unittest.main()
