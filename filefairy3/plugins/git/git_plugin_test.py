#!/usr/bin/env python

from git_plugin import GitPlugin

import mock
import unittest


class GitPluginTest(unittest.TestCase):
    @mock.patch('git_plugin.log')
    @mock.patch('git_plugin.check_output')
    def test_add(self, mock_check, mock_log):
        mock_check.return_value = ''
        mock_log.return_value = ''
        data = {'a': '', 'v': True}
        plugin = GitPlugin()
        plugin.add(**data)
        mock_check.assert_called_once_with(['git', 'add', '.'])
        mock_log.assert_called_once_with(plugin._name(), **{
            'a': '',
            'r': '',
            's': 'Call completed.',
            'v': True
        })

    @mock.patch('git_plugin.log')
    @mock.patch('git_plugin.check_output')
    def test_commit(self, mock_check, mock_log):
        mock_check.return_value = '[master 0abcd0a] Auto...\n1 files\n'
        mock_log.return_value = '[master 0abcd0a] Auto...\n1 files'
        data = {'a': '', 'v': True}
        plugin = GitPlugin()
        plugin.commit(**data)
        mock_check.assert_called_once_with(
            ['git', 'commit', '-m', 'Automated data push.'])
        mock_log.assert_called_once_with(
            plugin._name(), **{
                'a': '',
                'r': '[master 0abcd0a] Auto...\n1 files',
                's': 'Call completed.',
                'v': True
            })

    @mock.patch('git_plugin.log')
    @mock.patch('git_plugin.check_output')
    def test_pull(self, mock_check, mock_log):
        mock_check.return_value = 'remote: Counting...\nUnpacking...\n'
        mock_log.return_value = 'remote: Counting...\nUnpacking...'
        data = {'a': '', 'v': True}
        plugin = GitPlugin()
        plugin.pull(**data)
        mock_check.assert_called_once_with(['git', 'pull'])
        mock_log.assert_called_once_with(
            plugin._name(), **{
                'a': '',
                'r': 'remote: Counting...\nUnpacking...',
                's': 'Call completed.',
                'v': True
            })

    @mock.patch('git_plugin.log')
    @mock.patch('git_plugin.check_output')
    def test_push(self, mock_check, mock_log):
        mock_check.return_value = 'Counting...\nCompressing...\n'
        mock_log.return_value = 'Counting...\nCompressing...'
        data = {'a': '', 'v': True}
        plugin = GitPlugin()
        plugin.push(**data)
        mock_check.assert_called_once_with(['git', 'push', 'origin', 'master'])
        mock_log.assert_called_once_with(
            plugin._name(), **{
                'a': '',
                'r': 'Counting...\nCompressing...',
                's': 'Call completed.',
                'v': True
            })

    @mock.patch('git_plugin.log')
    @mock.patch('git_plugin.check_output')
    def test_reset(self, mock_check, mock_log):
        mock_check.return_value = ''
        mock_log.return_value = ''
        data = {'a': '', 'v': True}
        plugin = GitPlugin()
        plugin.reset(**data)
        mock_check.assert_called_once_with(['git', 'reset', '--hard'])
        mock_log.assert_called_once_with(
            plugin._name(), **{
                'a': '',
                'r': '',
                's': 'Call completed.',
                'v': True
            })

    @mock.patch('git_plugin.log')
    @mock.patch('git_plugin.check_output')
    def test_status(self, mock_check, mock_log):
        mock_check.return_value = 'On branch master\nYour branch...\n'
        mock_log.return_value = 'On branch master\nYour branch...'
        data = {'a': '', 'v': True}
        plugin = GitPlugin()
        plugin.status(**data)
        mock_check.assert_called_once_with(['git', 'status'])
        mock_log.assert_called_once_with(
            plugin._name(), **{
                'a': '',
                'r': 'On branch master\nYour branch...',
                's': 'Call completed.',
                'v': True
            })


if __name__ == '__main__':
    unittest.main()
