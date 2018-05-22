#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/plugin/git', '', _path))
from plugin.git.git import Git  # noqa
from value.notify.notify import Notify  # noqa
from value.response.response import Response  # noqa

NOW = datetime.datetime(1985, 10, 27, 0, 0, 0)
THEN = datetime.datetime(1985, 10, 26, 0, 2, 30)


class GitTest(unittest.TestCase):
    def setUp(self):
        patch_log = mock.patch('plugin.git.git.log')
        self.addCleanup(patch_log.stop)
        self.mock_log = patch_log.start()
        patch_check = mock.patch('plugin.git.git.check_output')
        self.addCleanup(patch_check.stop)
        self.mock_check = patch_check.start()

    def reset_mocks(self):
        self.mock_log.reset_mock()
        self.mock_check.reset_mock()

    def create_plugin(self, day=0):
        plugin = Git()

        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

        self.reset_mocks()

        return plugin

    @mock.patch.object(Git, 'automate')
    def test_notify__with_day(self, mock_automate):
        plugin = self.create_plugin()
        value = plugin._notify_internal(notify=Notify.FAIRYLAB_DAY)
        self.assertFalse(value)

        mock_automate.assert_called_once_with(notify=Notify.FAIRYLAB_DAY)
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    @mock.patch.object(Git, 'automate')
    def test_notify__with_other(self, mock_automate):
        plugin = self.create_plugin()
        value = plugin._notify_internal(notify=Notify.OTHER)
        self.assertFalse(value)

        mock_automate.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    def test_on_message(self):
        plugin = self.create_plugin()
        response = plugin._on_message_internal()
        self.assertEqual(response, Response())

        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    def test_run(self):
        plugin = self.create_plugin()
        response = plugin._run_internal(date=THEN)
        self.assertEqual(response, Response())

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

    def test_call__with_ok_false(self):
        self.mock_check.return_value = {'ok': False, 'error': 'timeout'}

        plugin = self.create_plugin()
        plugin._call(['cmd'], {'a1': '', 'v': True})

        self.mock_check.assert_called_once_with(['cmd'])
        self.mock_log.assert_called_once_with(
            plugin._name(), **{
                'a1': '',
                'c': {'ok': False, 'error': 'timeout'},
                's': 'Call failed: \'cmd\'.',
                'v': True
            })

    def test_call__with_ok_true(self):
        self.mock_check.return_value = {'ok': True, 'output': ''}

        plugin = self.create_plugin()
        plugin._call(['cmd'], {'a1': '', 'v': True})

        self.mock_check.assert_called_once_with(['cmd'])
        self.mock_log.assert_called_once_with(
            plugin._name(), **{
                'a1': '',
                'c': '',
                's': 'Call completed: \'cmd\'.',
                'v': True
            })

    def test_add(self):
        self.mock_check.return_value = {'ok': True, 'output': ''}

        plugin = self.create_plugin()
        plugin.add(**{'a1': '', 'v': True})

        self.mock_check.assert_called_once_with(['git', 'add', '.'])
        self.mock_log.assert_called_once_with(
            plugin._name(), **{
                'a1': '',
                'c': '',
                's': 'Call completed: \'git add .\'.',
                'v': True
            })

    @mock.patch.object(Git, 'push')
    @mock.patch.object(Git, 'commit')
    @mock.patch.object(Git, 'add')
    def test_automate(self, mock_add, mock_commit, mock_push):
        plugin = self.create_plugin()
        plugin.automate(date=NOW)

        mock_add.assert_called_once_with(date=NOW)
        mock_commit.assert_called_once_with(date=NOW)
        mock_push.assert_called_once_with(date=NOW)
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    def test_commit(self):
        self.mock_check.return_value = {
            'ok': True,
            'output': '[master 0abcd0a] Auto...\n1 files\n'
        }

        plugin = self.create_plugin()
        plugin.commit(**{'a1': '', 'v': True})

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
        self.mock_check.return_value = {
            'ok': True,
            'output': 'remote: Counting...\nUnpacking...\n'
        }

        plugin = self.create_plugin()
        plugin.pull(**{'a1': '', 'v': True})

        self.mock_check.assert_called_once_with(['git', 'pull'])
        self.mock_log.assert_called_once_with(
            plugin._name(), **{
                'a1': '',
                'c': 'remote: Counting...\nUnpacking...',
                's': 'Call completed: \'git pull\'.',
                'v': True
            })

    def test_push(self):
        self.mock_check.return_value = {
            'ok': True,
            'output': 'Counting...\nCompressing...\n'
        }

        plugin = self.create_plugin()
        plugin.push(**{'a1': '', 'v': True})

        self.mock_check.assert_called_once_with(['git', 'push'])
        self.mock_log.assert_called_once_with(
            plugin._name(), **{
                'a1': '',
                'c': 'Counting...\nCompressing...',
                's': 'Call completed: \'git push\'.',
                'v': True
            })

    def test_reset(self):
        self.mock_check.return_value = {'ok': True, 'output': ''}

        plugin = self.create_plugin()
        plugin.reset(**{'a1': '', 'v': True})

        self.mock_check.assert_called_once_with(['git', 'reset', '--hard'])
        self.mock_log.assert_called_once_with(
            plugin._name(), **{
                'a1': '',
                'c': '',
                's': 'Call completed: \'git reset --hard\'.',
                'v': True
            })

    def test_status(self):
        self.mock_check.return_value = {
            'ok': True,
            'output': 'On branch master\nYour branch...\n'
        }

        plugin = self.create_plugin()
        plugin.status(**{'a1': '', 'v': True})

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
