#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/util/slack', '', _path))
from util.secrets.secrets import brunnerj  # noqa
from util.secrets.secrets import filefairy  # noqa
from util.slack.slack import channels_kick  # noqa
from util.slack.slack import channels_history  # noqa
from util.slack.slack import channels_list  # noqa
from util.slack.slack import chat_post_message  # noqa
from util.slack.slack import files_upload  # noqa
from util.slack.slack import reactions_add  # noqa
from util.slack.slack import rtm_connect  # noqa
from util.slack.slack import users_list  # noqa

_brunnerj = brunnerj()
_filefairy = filefairy()


class SlackTest(unittest.TestCase):
    @mock.patch('util.slack.slack.urlopen')
    def test_channels_kick(self, mock_urlopen):
        mock_urlopen.return_value = bytes('{"ok":true}', 'utf-8')

        actual = channels_kick('channel', 'U1234')
        expected = {'ok': True}
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(
            'https://slack.com/api/channels.kick', {
                'token': _brunnerj,
                'channel': 'channel',
                'user': 'U1234',
            })

    @mock.patch('util.slack.slack.urlopen')
    def test_channels_history(self, mock_urlopen):
        mock_urlopen.return_value = bytes('{"ok":true,"latest":"12000000"}',
                                          'utf-8')

        actual = channels_history('channel', 0)
        expected = {'ok': True, 'latest': '12000000'}
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(
            'https://slack.com/api/channels.history', {
                'token': _filefairy,
                'channel': 'channel',
                'count': 1000,
                'latest': 0,
            })

    @mock.patch('util.slack.slack.urlopen')
    def test_channels_list(self, mock_urlopen):
        mock_urlopen.return_value = bytes(
            '{"ok":true,"channels":[{"id":"C12345"}]}', 'utf-8')

        actual = channels_list()
        expected = {'ok': True, 'channels': [{'id': 'C12345'}]}
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(
            'https://slack.com/api/channels.list', {
                'token': _filefairy,
                'exclude_members': True,
                'exclude_archived': True,
            })

    @mock.patch('util.slack.slack.urlopen')
    def test_chat_post_message(self, mock_urlopen):
        mock_urlopen.return_value = bytes(
            '{"ok":true,"message":{"text":"foo"}}', 'utf-8')

        attachments = [{'fallback': 'a', 'title': 'b', 'text': 'c'}]
        actual = chat_post_message('channel', 'foo', attachments=attachments)
        expected = {'ok': True, 'message': {'text': 'foo'}}
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(
            'https://slack.com/api/chat.postMessage', {
                'token': _filefairy,
                'channel': 'channel',
                'text': 'foo',
                'as_user': 'true',
                'attachments': attachments,
                'link_names': 'true',
            })

    @mock.patch('util.slack.slack.urlopen')
    def test_files_upload(self, mock_urlopen):
        mock_urlopen.return_value = bytes(
            '{"ok":true,"file":{"preview":"content"}}', 'utf-8')

        actual = files_upload('content', 'filename.txt', 'channel')
        expected = {'ok': True, 'file': {'preview': 'content'}}
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(
            'https://slack.com/api/files.upload', {
                'token': _filefairy,
                'content': 'content',
                'filename': 'filename.txt',
                'channels': 'channel',
            })

    @mock.patch('util.slack.slack.urlopen')
    def test_reactions_add(self, mock_urlopen):
        mock_urlopen.return_value = bytes('{"ok":true}', 'utf-8')

        actual = reactions_add('name', 'C1234', 'timestamp')
        expected = {'ok': True}
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(
            'https://slack.com/api/reactions.add', {
                'token': _filefairy,
                'name': 'name',
                'channel': 'C1234',
                'timestamp': 'timestamp',
            })

    @mock.patch('util.slack.slack.urlopen')
    def test_rtm_connect(self, mock_urlopen):
        mock_urlopen.return_value = bytes('{"ok":true,"url":"wss://..."}',
                                          'utf-8')

        actual = rtm_connect()
        expected = {'ok': True, 'url': 'wss://...'}
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(
            'https://slack.com/api/rtm.connect', {
                'token': _filefairy
            })

    @mock.patch('util.slack.slack.urlopen')
    def test_users_list(self, mock_urlopen):
        mock_urlopen.return_value = bytes(
            '{"ok":true,"members":[{"id":"U12345"}]}', 'utf-8')

        actual = users_list()
        expected = {'ok': True, 'members': [{'id': 'U12345'}]}
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(
            'https://slack.com/api/users.list', {
                'token': _filefairy,
            })


if __name__ == '__main__':
    unittest.main()
