#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mock
import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/util/logger', '', _path))
from util.logger.logger_util import log  # noqa


class LoggerUtilTest(unittest.TestCase):
    @mock.patch('util.logger.logger_util.files_upload')
    @mock.patch('util.logger.logger_util.chat_post_message')
    def test_log__with_string(self, mock_post, mock_upload):
        log('name', s='str')
        mock_post.assert_not_called()
        mock_upload.assert_not_called()

    @mock.patch('util.logger.logger_util.files_upload')
    @mock.patch('util.logger.logger_util.chat_post_message')
    def test_log__with_string_verbose(self, mock_post, mock_upload):
        log('name', s='str', v=True)
        mock_post.assert_called_once_with('testing', '(name) str')
        mock_upload.assert_not_called()

    @mock.patch('util.logger.logger_util.files_upload')
    @mock.patch('util.logger.logger_util.chat_post_message')
    def test_log__with_return_string(self, mock_post, mock_upload):
        log('name', c='content', s='str')
        mock_post.assert_not_called()
        mock_upload.assert_not_called()

    @mock.patch('util.logger.logger_util.files_upload')
    @mock.patch('util.logger.logger_util.chat_post_message')
    def test_log__with_return_string_verbose(self, mock_post, mock_upload):
        log('name', c='content', s='str', v=True)
        mock_post.assert_called_once_with('testing', '(name) str')
        mock_upload.assert_called_once_with('content', 'name.log.txt', 'testing')


if __name__ == '__main__':
    unittest.main()
