#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for slack.py."""

import logging
import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/common/slack', '', _path))

from common.secrets.secrets import filefairy  # noqa
from common.slack.slack import _call  # noqa
from common.slack.slack import channels_history  # noqa
from common.slack.slack import channels_list  # noqa
from common.slack.slack import chat_post_message  # noqa
from common.slack.slack import files_upload  # noqa
from common.slack.slack import pins_add  # noqa
from common.slack.slack import reactions_add  # noqa
from common.slack.slack import reactions_get  # noqa
from common.slack.slack import reactions_remove  # noqa
from common.slack.slack import rtm_connect  # noqa
from common.slack.slack import users_list  # noqa

FILEFAIRY = filefairy()


class SlackTest(unittest.TestCase):
    def setUp(self):
        patch_log = mock.patch('common.slack.slack._logger.log')
        self.addCleanup(patch_log.stop)
        self.mock_log = patch_log.start()

    @mock.patch('common.slack.slack.urlopen')
    def test_call__ok(self, mock_urlopen):
        mock_urlopen.return_value = bytes('{"ok":true}', 'utf-8')

        params = {'token': FILEFAIRY}
        actual = _call('method', params)
        expected = {'ok': True}
        self.assertEqual(actual, expected)

        url = 'https://slack.com/api/method'
        mock_urlopen.assert_called_once_with(url, params)
        self.mock_log.assert_not_called()

    @mock.patch('common.slack.slack.urlopen')
    def test_call__exception(self, mock_urlopen):
        mock_urlopen.side_effect = Exception()

        params = {'token': FILEFAIRY}
        actual = _call('method', params)
        expected = {'ok': False}
        self.assertEqual(actual, expected)

        url = 'https://slack.com/api/method'
        mock_urlopen.assert_called_once_with(url, params)
        self.mock_log.assert_called_once_with(
            logging.WARNING, 'Handled warning.', exc_info=True)

    @mock.patch('common.slack.slack._call')
    def test_channels_history(self, mock_call):
        mock_call.return_value = {'ok': True}

        actual = channels_history('channel', '456', '123')
        expected = {'ok': True}
        self.assertEqual(actual, expected)

        mock_call.assert_called_once_with('channels.history', {
            'token': FILEFAIRY,
            'channel': 'channel',
            'count': 1000,
            'latest': '456',
            'oldest': '123',
        })
        self.mock_log.assert_not_called()

    @mock.patch('common.slack.slack._call')
    def test_channels_list(self, mock_call):
        mock_call.return_value = {'ok': True}

        actual = channels_list()
        expected = {'ok': True}
        self.assertEqual(actual, expected)

        mock_call.assert_called_once_with(
            'channels.list', {
                'token': FILEFAIRY,
                'exclude_members': True,
                'exclude_archived': True,
            })
        self.mock_log.assert_not_called()

    @mock.patch('common.slack.slack._call')
    def test_chat_post_message(self, mock_call):
        mock_call.return_value = {'ok': True}

        attachments = [{'fallback': 'a', 'title': 'b', 'text': 'c'}]
        actual = chat_post_message('channel', 'foo', attachments=attachments)
        expected = {'ok': True}
        self.assertEqual(actual, expected)

        mock_call.assert_called_once_with(
            'chat.postMessage', {
                'token': FILEFAIRY,
                'channel': 'channel',
                'text': 'foo',
                'as_user': 'true',
                'attachments': attachments,
                'link_names': 'true',
            })
        self.mock_log.assert_not_called()

    @mock.patch('common.slack.slack._call')
    def test_files_upload(self, mock_call):
        mock_call.return_value = {'ok': True}

        actual = files_upload('content', 'filename.txt', 'channel')
        expected = {'ok': True}
        self.assertEqual(actual, expected)

        mock_call.assert_called_once_with(
            'files.upload', {
                'token': FILEFAIRY,
                'content': 'content',
                'filename': 'filename.txt',
                'channels': 'channel',
            })
        self.mock_log.assert_not_called()

    @mock.patch('common.slack.slack._call')
    def test_pins_add(self, mock_call):
        mock_call.return_value = {'ok': True}

        actual = pins_add('C1234', 'timestamp')
        expected = {'ok': True}
        self.assertEqual(actual, expected)

        mock_call.assert_called_once_with('pins.add', {
            'token': FILEFAIRY,
            'channel': 'C1234',
            'timestamp': 'timestamp',
        })
        self.mock_log.assert_not_called()

    @mock.patch('common.slack.slack._call')
    def test_reactions_add(self, mock_call):
        mock_call.return_value = {'ok': True}

        actual = reactions_add('name', 'C1234', 'timestamp')
        expected = {'ok': True}
        self.assertEqual(actual, expected)

        mock_call.assert_called_once_with(
            'reactions.add', {
                'token': FILEFAIRY,
                'name': 'name',
                'channel': 'C1234',
                'timestamp': 'timestamp',
            })
        self.mock_log.assert_not_called()

    @mock.patch('common.slack.slack._call')
    def test_reactions_get(self, mock_call):
        mock_call.return_value = {'ok': True}

        actual = reactions_get('C1234', 'timestamp')
        expected = {'ok': True}
        self.assertEqual(actual, expected)

        mock_call.assert_called_once_with('reactions.get', {
            'token': FILEFAIRY,
            'channel': 'C1234',
            'timestamp': 'timestamp',
        })

    @mock.patch('common.slack.slack._call')
    def test_reactions_remove(self, mock_call):
        mock_call.return_value = {'ok': True}

        actual = reactions_remove('name', 'C1234', 'timestamp')
        expected = {'ok': True}
        self.assertEqual(actual, expected)

        mock_call.assert_called_once_with(
            'reactions.remove', {
                'token': FILEFAIRY,
                'name': 'name',
                'channel': 'C1234',
                'timestamp': 'timestamp',
            })
        self.mock_log.assert_not_called()

    @mock.patch('common.slack.slack._call')
    def test_rtm_connect(self, mock_call):
        mock_call.return_value = {'ok': True}

        actual = rtm_connect()
        expected = {'ok': True}
        self.assertEqual(actual, expected)

        mock_call.assert_called_once_with('rtm.connect', {'token': FILEFAIRY})
        self.mock_log.assert_not_called()

    @mock.patch('common.slack.slack._call')
    def test_users_list(self, mock_call):
        mock_call.return_value = {'ok': True}

        actual = users_list()
        expected = {'ok': True}
        self.assertEqual(actual, expected)

        mock_call.assert_called_once_with('users.list', {
            'token': FILEFAIRY,
        })
        self.mock_log.assert_not_called()


if __name__ == '__main__':
    unittest.main()
