#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/util/logger', '', _path))
from util.logger.logger import log  # noqa


class LoggerTest(unittest.TestCase):
    @mock.patch('util.logger.logger.files_upload')
    @mock.patch('util.logger.logger.chat_post_message')
    def test_log__with_string(self, mock_post, mock_upload):
        log('name', s='str')
        mock_post.assert_called_once_with('testing', '(name) str')
        mock_upload.assert_not_called()

    @mock.patch('util.logger.logger.files_upload')
    @mock.patch('util.logger.logger.chat_post_message')
    def test_log__with_string_verbose(self, mock_post, mock_upload):
        log('name', s='str', v=True)
        mock_post.assert_called_once_with('testing', '(name) str')
        mock_upload.assert_not_called()

    @mock.patch('util.logger.logger.files_upload')
    @mock.patch('util.logger.logger.chat_post_message')
    def test_log__with_return_string(self, mock_post, mock_upload):
        log('name', c='content', s='str')
        mock_post.assert_called_once_with('testing', '(name) str')
        mock_upload.assert_called_once_with('content', 'name.log.txt', 'testing')

    @mock.patch('util.logger.logger.files_upload')
    @mock.patch('util.logger.logger.chat_post_message')
    def test_log__with_return_string_verbose(self, mock_post, mock_upload):
        log('name', c='content', s='str', v=True)
        mock_post.assert_called_once_with('testing', '(name) str')
        mock_upload.assert_called_once_with('content', 'name.log.txt', 'testing')


if __name__ == '__main__':
    unittest.main()
