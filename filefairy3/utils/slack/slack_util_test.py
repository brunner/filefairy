#!/usr/bin/env python

import mock
import os
import re
import sys
import unittest
import urllib
import urllib2

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/utils/slack', '', _path))
from secrets import filefairy  # noqa
from utils.slack.slack_util import chat_post_message, files_upload, rtm_connect  # noqa


class SlackUtilTest(unittest.TestCase):
    @mock.patch('utils.slack.slack_util.urlopen')
    @mock.patch('utils.slack.slack_util.create_request')
    def test_chat_post_message(self, mock_request, mock_urlopen):
        mock_request.return_value = urllib2.Request(
            'https://slack.com/api/chat.postMessage',
            urllib.urlencode({
                'token': filefairy,
                'channel': 'channel',
                'text': 'foo',
                'as_user': 'true',
                'link_names': 'true',
            }))
        mock_urlopen.return_value = '{"ok":true,"message":{"text":"foo"}}'
        actual = chat_post_message('channel', 'foo')
        expected = {'ok': True, 'message': {'text': 'foo'}}
        self.assertEquals(actual, expected)
        mock_request.assert_called_once_with(
            'https://slack.com/api/chat.postMessage', {
                'token': filefairy,
                'channel': 'channel',
                'text': 'foo',
                'as_user': 'true',
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
        self.assertEquals(actual, expected)
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
    def test_rtm_connect(self, mock_request, mock_urlopen):
        mock_request.return_value = urllib2.Request(
            'https://slack.com/api/rtm.connect',
            urllib.urlencode({
                'token': filefairy
            }))
        mock_urlopen.return_value = '{"ok":true,"url":"wss://..."}'
        actual = rtm_connect()
        expected = {'ok': True, 'url': 'wss://...'}
        self.assertEquals(actual, expected)
        mock_request.assert_called_once_with(
            'https://slack.com/api/rtm.connect', {
                'token': filefairy
            })
        mock_urlopen.assert_called_once_with(mock_request.return_value)


if __name__ == '__main__':
    unittest.main()
