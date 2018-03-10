#!/usr/bin/env python

from logger_util import log

import mock
import unittest


class LoggerUtilTest(unittest.TestCase):
    @mock.patch('logger_util.files_upload')
    @mock.patch('logger_util.chat_post_message')
    def test_log__with_string(self, mock_post, mock_upload):
        log('name', s='str')
        mock_post.assert_not_called()
        mock_upload.assert_not_called()

    @mock.patch('logger_util.files_upload')
    @mock.patch('logger_util.chat_post_message')
    def test_log__with_string_verbose(self, mock_post, mock_upload):
        log('name', s='str', v=True)
        mock_post.assert_called_once_with('testing', '(name) str')
        mock_upload.assert_called_once_with('', 'name.log.txt', 'testing')

    @mock.patch('logger_util.files_upload')
    @mock.patch('logger_util.chat_post_message')
    def test_log__with_return_string(self, mock_post, mock_upload):
        log('name', c='content', s='str')
        mock_post.assert_not_called()
        mock_upload.assert_not_called()

    @mock.patch('logger_util.files_upload')
    @mock.patch('logger_util.chat_post_message')
    def test_log__with_return_string_verbose(self, mock_post, mock_upload):
        log('name', c='content', s='str', v=True)
        mock_post.assert_called_once_with('testing', '(name) str')
        mock_upload.assert_called_once_with('content', 'name.log.txt', 'testing')


if __name__ == '__main__':
    unittest.main()
