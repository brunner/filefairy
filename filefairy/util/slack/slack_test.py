#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/util/slack', '', _path))
from util.secrets.secrets import filefairy  # noqa
from util.slack.slack import _call  # noqa
from util.slack.slack import channels_history  # noqa
from util.slack.slack import channels_list  # noqa
from util.slack.slack import chat_post_message  # noqa
from util.slack.slack import files_upload  # noqa
from util.slack.slack import pins_add  # noqa
from util.slack.slack import reactions_add  # noqa
from util.slack.slack import reactions_get  # noqa
from util.slack.slack import reactions_remove  # noqa
from util.slack.slack import rtm_connect  # noqa
from util.slack.slack import users_list  # noqa

_filefairy = filefairy()
_ok = {'ok': True}


class SlackTest(unittest.TestCase):
    @mock.patch('util.slack.slack.urlopen')
    @mock.patch('util.slack.slack.logger_.log')
    def test_call__with_valid_input(self, mock_log, mock_urlopen):
        mock_urlopen.return_value = bytes('{"ok":true,"a":1}', 'utf-8')
        params = {'token': _filefairy}
        actual = _call('method', params)
        expected = {'ok': True, 'a': 1}
        self.assertEqual(actual, expected)
        url = 'https://slack.com/api/method'
        mock_log.assert_not_called()
        mock_urlopen.assert_called_once_with(url, params)

    @mock.patch('util.slack.slack.urlopen')
    @mock.patch('util.slack.slack.logger_.log')
    def test_call__with_thrown_exception(self, mock_log, mock_urlopen):
        mock_urlopen.side_effect = Exception('response')
        params = {'token': _filefairy}
        actual = _call('method', params)
        expected = {'ok': False}
        self.assertEqual(actual, expected)
        url = 'https://slack.com/api/method'
        mock_log.assert_called_once_with(
            logging.WARNING, 'Handled warning.', exc_info=True)
        mock_urlopen.assert_called_once_with(url, params)

    @mock.patch('util.slack.slack._call')
    def test_channels_history(self, mock_call):
        mock_call.return_value = _ok
        actual = channels_history('channel', 0)
        expected = _ok
        self.assertEqual(actual, expected)
        mock_call.assert_called_once_with(
            'channels.history', {
                'token': _filefairy,
                'channel': 'channel',
                'count': 1000,
                'latest': 0,
            })

    @mock.patch('util.slack.slack._call')
    def test_channels_list(self, mock_call):
        mock_call.return_value = _ok
        actual = channels_list()
        expected = _ok
        self.assertEqual(actual, expected)
        mock_call.assert_called_once_with(
            'channels.list', {
                'token': _filefairy,
                'exclude_members': True,
                'exclude_archived': True,
            })

    @mock.patch('util.slack.slack._call')
    def test_chat_post_message(self, mock_call):
        mock_call.return_value = _ok
        attachments = [{'fallback': 'a', 'title': 'b', 'text': 'c'}]
        actual = chat_post_message('channel', 'foo', attachments=attachments)
        expected = _ok
        self.assertEqual(actual, expected)
        mock_call.assert_called_once_with(
            'chat.postMessage', {
                'token': _filefairy,
                'channel': 'channel',
                'text': 'foo',
                'as_user': 'true',
                'attachments': attachments,
                'link_names': 'true',
            })

    @mock.patch('util.slack.slack._call')
    def test_files_upload(self, mock_call):
        mock_call.return_value = _ok
        actual = files_upload('content', 'filename.txt', 'channel')
        expected = _ok
        self.assertEqual(actual, expected)
        mock_call.assert_called_once_with(
            'files.upload', {
                'token': _filefairy,
                'content': 'content',
                'filename': 'filename.txt',
                'channels': 'channel',
            })

    @mock.patch('util.slack.slack._call')
    def test_pins_add(self, mock_call):
        mock_call.return_value = _ok
        actual = pins_add('C1234', 'timestamp')
        expected = _ok
        self.assertEqual(actual, expected)
        mock_call.assert_called_once_with('pins.add', {
            'token': _filefairy,
            'channel': 'C1234',
            'timestamp': 'timestamp',
        })

    @mock.patch('util.slack.slack._call')
    def test_reactions_add(self, mock_call):
        mock_call.return_value = _ok
        actual = reactions_add('name', 'C1234', 'timestamp')
        expected = _ok
        self.assertEqual(actual, expected)
        mock_call.assert_called_once_with(
            'reactions.add', {
                'token': _filefairy,
                'name': 'name',
                'channel': 'C1234',
                'timestamp': 'timestamp',
            })

    @mock.patch('util.slack.slack._call')
    def test_reactions_get(self, mock_call):
        mock_call.return_value = _ok
        actual = reactions_get('C1234', 'timestamp')
        expected = _ok
        self.assertEqual(actual, expected)
        mock_call.assert_called_once_with(
            'reactions.get', {
                'token': _filefairy,
                'channel': 'C1234',
                'timestamp': 'timestamp',
            })

    @mock.patch('util.slack.slack._call')
    def test_reactions_remove(self, mock_call):
        mock_call.return_value = _ok
        actual = reactions_remove('name', 'C1234', 'timestamp')
        expected = _ok
        self.assertEqual(actual, expected)
        mock_call.assert_called_once_with(
            'reactions.remove', {
                'token': _filefairy,
                'name': 'name',
                'channel': 'C1234',
                'timestamp': 'timestamp',
            })

    @mock.patch('util.slack.slack._call')
    def test_rtm_connect(self, mock_call):
        mock_call.return_value = _ok
        actual = rtm_connect()
        expected = _ok
        self.assertEqual(actual, expected)
        mock_call.assert_called_once_with('rtm.connect', {'token': _filefairy})

    @mock.patch('util.slack.slack._call')
    def test_users_list(self, mock_call):
        mock_call.return_value = _ok
        actual = users_list()
        expected = _ok
        self.assertEqual(actual, expected)
        mock_call.assert_called_once_with('users.list', {
            'token': _filefairy,
        })


if __name__ == '__main__':
    unittest.main()
