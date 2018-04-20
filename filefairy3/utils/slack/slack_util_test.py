#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mock
import os
import re
import sys
import unittest
import urllib
import urllib2

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/utils/slack', '', _path))
from utils.secrets.secrets_util import brunnerj, filefairy  # noqa
from utils.slack.slack_util import channels_kick, channels_history, channels_list, chat_post_message  # noqa
from utils.slack.slack_util import files_upload, reactions_add, rtm_connect, users_list  # noqa


class SlackUtilTest(unittest.TestCase):
    @mock.patch('utils.slack.slack_util.urlopen')
    @mock.patch('utils.slack.slack_util.create_request')
    def test_channels_kick(self, mock_request, mock_urlopen):
        mock_request.return_value = urllib2.Request(
            'https://slack.com/api/channels.kick',
            urllib.urlencode({
                'token': brunnerj,
                'channel': 'channel',
                'user': 'U1234',
            }))
        mock_urlopen.return_value = '{"ok":true}'
        actual = channels_kick('channel', 'U1234')
        expected = {'ok': True}
        self.assertEqual(actual, expected)
        mock_request.assert_called_once_with(
            'https://slack.com/api/channels.kick', {
                'token': brunnerj,
                'channel': 'channel',
                'user': 'U1234',
            })
        mock_urlopen.assert_called_once_with(mock_request.return_value)

    @mock.patch('utils.slack.slack_util.urlopen')
    @mock.patch('utils.slack.slack_util.create_request')
    def test_channels_history(self, mock_request, mock_urlopen):
        mock_request.return_value = urllib2.Request(
            'https://slack.com/api/channels.history',
            urllib.urlencode({
                'token': filefairy,
                'channel': 'channel',
                'count': 1000,
                'latest': 0,
            }))
        mock_urlopen.return_value = '{"ok":true,"latest":"12000000"}'
        actual = channels_history('channel', 0)
        expected = {'ok': True, 'latest': '12000000'}
        self.assertEqual(actual, expected)
        mock_request.assert_called_once_with(
            'https://slack.com/api/channels.history', {
                'token': filefairy,
                'channel': 'channel',
                'count': 1000,
                'latest': 0,
            })
        mock_urlopen.assert_called_once_with(mock_request.return_value)

    @mock.patch('utils.slack.slack_util.urlopen')
    @mock.patch('utils.slack.slack_util.create_request')
    def test_channels_list(self, mock_request, mock_urlopen):
        mock_request.return_value = urllib2.Request(
            'https://slack.com/api/channels.list',
            urllib.urlencode({
                'token': filefairy,
                'exclude_members': True,
                'exclude_archived': True,
            }))
        mock_urlopen.return_value = '{"ok":true,"channels":[{"id":"C12345"}]}'
        actual = channels_list()
        expected = {'ok': True, 'channels': [{'id': 'C12345'}]}
        self.assertEqual(actual, expected)
        mock_request.assert_called_once_with(
            'https://slack.com/api/channels.list', {
                'token': filefairy,
                'exclude_members': True,
                'exclude_archived': True,
            })
        mock_urlopen.assert_called_once_with(mock_request.return_value)

    @mock.patch('utils.slack.slack_util.urlopen')
    @mock.patch('utils.slack.slack_util.create_request')
    def test_chat_post_message(self, mock_request, mock_urlopen):
        attachments = [{'fallback': 'a', 'title': 'b', 'text': 'c'}]
        mock_request.return_value = urllib2.Request(
            'https://slack.com/api/chat.postMessage',
            urllib.urlencode({
                'token': filefairy,
                'channel': 'channel',
                'text': 'foo',
                'as_user': 'true',
                'attachments': attachments,
                'link_names': 'true',
            }))
        mock_urlopen.return_value = '{"ok":true,"message":{"text":"foo"}}'
        actual = chat_post_message('channel', 'foo', attachments=attachments)
        expected = {'ok': True, 'message': {'text': 'foo'}}
        self.assertEqual(actual, expected)
        mock_request.assert_called_once_with(
            'https://slack.com/api/chat.postMessage', {
                'token': filefairy,
                'channel': 'channel',
                'text': 'foo',
                'as_user': 'true',
                'attachments': attachments,
                'link_names': 'true',
            })
        mock_urlopen.assert_called_once_with(mock_request.return_value)

    @mock.patch('utils.slack.slack_util.urlopen')
    @mock.patch('utils.slack.slack_util.create_request')
    def test_files_upload(self, mock_request, mock_urlopen):
        mock_request.return_value = urllib2.Request(
            'https://slack.com/api/files.upload',
            urllib.urlencode({
                'token': filefairy,
                'content': 'content',
                'filename': 'filename.txt',
                'channels': 'channel',
            }))
        mock_urlopen.return_value = '{"ok":true,"file":{"preview":"content"}}'
        actual = files_upload('content', 'filename.txt', 'channel')
        expected = {'ok': True, 'file': {'preview': 'content'}}
        self.assertEqual(actual, expected)
        mock_request.assert_called_once_with(
            'https://slack.com/api/files.upload', {
                'token': filefairy,
                'content': 'content',
                'filename': 'filename.txt',
                'channels': 'channel',
            })
        mock_urlopen.assert_called_once_with(mock_request.return_value)

    @mock.patch('utils.slack.slack_util.urlopen')
    @mock.patch('utils.slack.slack_util.create_request')
    def test_reactions_add(self, mock_request, mock_urlopen):
        mock_request.return_value = urllib2.Request(
            'https://slack.com/api/reactions.add',
            urllib.urlencode({
                'token': filefairy,
                'name': 'name',
                'channel': 'C1234',
                'timestamp': 'timestamp',
            }))
        mock_urlopen.return_value = '{"ok":true}'
        actual = reactions_add('name', 'C1234', 'timestamp')
        expected = {'ok': True}
        self.assertEqual(actual, expected)
        mock_request.assert_called_once_with(
            'https://slack.com/api/reactions.add', {
                'token': filefairy,
                'name': 'name',
                'channel': 'C1234',
                'timestamp': 'timestamp',
            })
        mock_urlopen.assert_called_once_with(mock_request.return_value)

    @mock.patch('utils.slack.slack_util.urlopen')
    @mock.patch('utils.slack.slack_util.create_request')
    def test_rtm_connect(self, mock_request, mock_urlopen):
        mock_request.return_value = urllib2.Request(
            'https://slack.com/api/rtm.connect',
            urllib.urlencode({
                'token': filefairy
            }))
        mock_urlopen.return_value = '{"ok":true,"url":"wss://..."}'
        actual = rtm_connect()
        expected = {'ok': True, 'url': 'wss://...'}
        self.assertEqual(actual, expected)
        mock_request.assert_called_once_with(
            'https://slack.com/api/rtm.connect', {
                'token': filefairy
            })
        mock_urlopen.assert_called_once_with(mock_request.return_value)

    @mock.patch('utils.slack.slack_util.urlopen')
    @mock.patch('utils.slack.slack_util.create_request')
    def test_users_list(self, mock_request, mock_urlopen):
        mock_request.return_value = urllib2.Request(
            'https://slack.com/api/users.list',
            urllib.urlencode({
                'token': filefairy,
            }))
        mock_urlopen.return_value = '{"ok":true,"members":[{"id":"U12345"}]}'
        actual = users_list()
        expected = {'ok': True, 'members': [{'id': 'U12345'}]}
        self.assertEqual(actual, expected)
        mock_request.assert_called_once_with(
            'https://slack.com/api/users.list', {
                'token': filefairy,
            })
        mock_urlopen.assert_called_once_with(mock_request.return_value)


if __name__ == '__main__':
    unittest.main()
