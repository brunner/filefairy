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


class GitPluginTest(unittest.TestCase):
    def test_setup(self):
        date = datetime.datetime(1985, 10, 26, 0, 2, 30)
        plugin = GitPlugin()
        plugin._setup(date=date)
        self.assertEqual(plugin.day, 26)

    @mock.patch.object(GitPlugin, 'push')
    @mock.patch.object(GitPlugin, 'commit')
    @mock.patch.object(GitPlugin, 'add')
    def test_run__with_different_day(self, mock_add, mock_commit, mock_push):
        then = datetime.datetime(1985, 10, 26, 0, 2, 30)
        now = datetime.datetime(1985, 10, 27, 0, 0, 0)
        plugin = GitPlugin()
        plugin._setup(date=then)
        plugin._run_internal(date=now)
        self.assertEqual(plugin.day, 27)
        mock_add.assert_called_once_with(date=now)
        mock_commit.assert_called_once_with(date=now)
        mock_push.assert_called_once_with(date=now)

    @mock.patch.object(GitPlugin, 'push')
    @mock.patch.object(GitPlugin, 'commit')
    @mock.patch.object(GitPlugin, 'add')
    def test_run__with_same_day(self, mock_add, mock_commit, mock_push):
        then = datetime.datetime(1985, 10, 26, 0, 2, 30)
        now = datetime.datetime(1985, 10, 26, 12, 0, 0)
        plugin = GitPlugin()
        plugin._setup(date=then)
        plugin._run_internal(date=now)
        self.assertEqual(plugin.day, 26)
        mock_add.assert_not_called()
        mock_commit.assert_not_called()
        mock_push.assert_not_called()

    @mock.patch('plugins.git.git_plugin.log')
    @mock.patch('plugins.git.git_plugin.check_output')
    def test_add(self, mock_check, mock_log):
        mock_check.return_value = ''
        mock_log.return_value = ''
        data = {'a1': '', 'v': True}
        plugin = GitPlugin()
        ret = plugin.add(**data)
        self.assertTrue(ret)
        mock_check.assert_called_once_with(['git', 'add', '.'])
        mock_log.assert_called_once_with(plugin._name(), **{
            'a1': '',
            'c': '',
            's': 'Call completed.',
            'v': True
        })

    @mock.patch('plugins.git.git_plugin.log')
    @mock.patch('plugins.git.git_plugin.check_output')
    def test_commit(self, mock_check, mock_log):
        mock_check.return_value = '[master 0abcd0a] Auto...\n1 files\n'
        mock_log.return_value = '[master 0abcd0a] Auto...\n1 files'
        data = {'a1': '', 'v': True}
        plugin = GitPlugin()
        ret = plugin.commit(**data)
        self.assertTrue(ret)
        mock_check.assert_called_once_with(
            ['git', 'commit', '-m', 'Automated data push.'])
        mock_log.assert_called_once_with(
            plugin._name(), **{
                'a1': '',
                'c': '[master 0abcd0a] Auto...\n1 files',
                's': 'Call completed.',
                'v': True
            })

    @mock.patch('plugins.git.git_plugin.log')
    @mock.patch('plugins.git.git_plugin.check_output')
    def test_pull(self, mock_check, mock_log):
        mock_check.return_value = 'remote: Counting...\nUnpacking...\n'
        mock_log.return_value = 'remote: Counting...\nUnpacking...'
        data = {'a1': '', 'v': True}
        plugin = GitPlugin()
        ret = plugin.pull(**data)
        self.assertTrue(ret)
        mock_check.assert_called_once_with(['git', 'pull'])
        mock_log.assert_called_once_with(
            plugin._name(), **{
                'a1': '',
                'c': 'remote: Counting...\nUnpacking...',
                's': 'Call completed.',
                'v': True
            })

    @mock.patch('plugins.git.git_plugin.log')
    @mock.patch('plugins.git.git_plugin.check_output')
    def test_push(self, mock_check, mock_log):
        mock_check.return_value = 'Counting...\nCompressing...\n'
        mock_log.return_value = 'Counting...\nCompressing...'
        data = {'a1': '', 'v': True}
        plugin = GitPlugin()
        ret = plugin.push(**data)
        self.assertTrue(ret)
        mock_check.assert_called_once_with(['git', 'push'])
        mock_log.assert_called_once_with(
            plugin._name(), **{
                'a1': '',
                'c': 'Counting...\nCompressing...',
                's': 'Call completed.',
                'v': True
            })

    @mock.patch('plugins.git.git_plugin.log')
    @mock.patch('plugins.git.git_plugin.check_output')
    def test_reset(self, mock_check, mock_log):
        mock_check.return_value = ''
        mock_log.return_value = ''
        data = {'a1': '', 'v': True}
        plugin = GitPlugin()
        ret = plugin.reset(**data)
        self.assertTrue(ret)
        mock_check.assert_called_once_with(['git', 'reset', '--hard'])
        mock_log.assert_called_once_with(
            plugin._name(), **{
                'a1': '',
                'c': '',
                's': 'Call completed.',
                'v': True
            })

    @mock.patch('plugins.git.git_plugin.log')
    @mock.patch('plugins.git.git_plugin.check_output')
    def test_status(self, mock_check, mock_log):
        mock_check.return_value = 'On branch master\nYour branch...\n'
        mock_log.return_value = 'On branch master\nYour branch...'
        data = {'a1': '', 'v': True}
        plugin = GitPlugin()
        ret = plugin.status(**data)
        self.assertTrue(ret)
        mock_check.assert_called_once_with(['git', 'status'])
        mock_log.assert_called_once_with(
            plugin._name(), **{
                'a1': '',
                'c': 'On branch master\nYour branch...',
                's': 'Call completed.',
                'v': True
            })


if __name__ == '__main__':
    unittest.main()
