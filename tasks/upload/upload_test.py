#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for upload.py."""

import logging
import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.extend((_path, re.sub(r'/tasks/upload', '', _path)))

from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.datetime_.datetime_ import encode_datetime  # noqa
from common.json_.json_ import dumps  # noqa
from common.test.test import Test  # noqa
from tasks.upload.upload import Upload  # noqa
from types_.notify.notify import Notify  # noqa
from types_.response.response import Response  # noqa

DATE_10260602 = datetime_datetime_pst(1985, 10, 26, 6, 2, 30)
DATE_10260604 = datetime_datetime_pst(1985, 10, 26, 6, 4)

DOMAIN_NAME = 'statsplus.net'
FILE_NAME = 'orange%20and%20blue%20league.zip'
FILE_URL = 'https://{}/oblootp/files/{}'.format(DOMAIN_NAME, FILE_NAME)


class UploadTest(Test):
    def setUp(self):
        chat_post_message_patch = mock.patch('tasks.upload.upload.chat_post_message')
        self.addCleanup(chat_post_message_patch.stop)
        self.chat_post_message_ = chat_post_message_patch.start()

        log_patch = mock.patch('tasks.upload.upload._logger.log')
        self.addCleanup(log_patch.stop)
        self.log_ = log_patch.start()

        open_patch = mock.patch('api.serializable.serializable.open',
                                create=True)
        self.addCleanup(open_patch.stop)
        self.open_ = open_patch.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.open_handle_ = mo()
        self.open_.side_effect = [mo.return_value]

    def reset_mocks(self):
        self.chat_post_message_.reset_mock()
        self.log_.reset_mock()
        self.open_handle_.write.reset_mock()

    def create_upload(self, data):
        self.init_mocks(data)
        upload = Upload(date=DATE_10260602)

        self.assertNotCalled(self.chat_post_message_, self.log_,
                             self.open_handle_.write)
        self.assertEqual(upload.data, data)

        self.reset_mocks()
        self.init_mocks(data)

        return upload

    # @mock.patch.object(Upload, 'get_file_date')
    # def test_run__new(self, get_file_date_):
    #     get_file_date_.return_value = encode_datetime(DATE_10260604)

    #     read = {'date': encode_datetime(DATE_10260602)}
    #     upload = self.create_upload(read)
    #     actual = upload._run_internal(date=DATE_10260604)
    #     expected = Response(notify=[Notify.UPLOAD_FINISH])
    #     self.assertEqual(actual, expected)

    #     write = {'date': encode_datetime(DATE_10260604)}
    #     get_file_date_.assert_called_once_with()
    #     self.chat_post_message_.assert_called_once_with(
    #         'fairylab', 'File is up.')
    #     self.log_.assert_called_once_with(logging.INFO, 'File is up.')
    #     self.open_handle_.write.assert_called_once_with(dumps(write) + '\n')

    # @mock.patch.object(Upload, 'get_file_date')
    # def test_run__old(self, get_file_date_):
    #     get_file_date_.return_value = encode_datetime(DATE_10260602)

    #     read = {'date': encode_datetime(DATE_10260602)}
    #     upload = self.create_upload(read)
    #     actual = upload._run_internal(date=DATE_10260604)
    #     expected = Response()
    #     self.assertEqual(actual, expected)

    #     get_file_date_.assert_called_once_with()
    #     self.assertNotCalled(self.chat_post_message_, self.log_,
    #                          self.open_handle_.write)

    @mock.patch('tasks.upload.upload.get')
    def test_get_file_date(self, mock_get):
        text = 'League File: Oct. 26, 1985, 8:04 a.m. CST'
        mock_get.return_value = text

        data = {'date': ''}
        upload = self.create_upload(data)
        actual = upload.get_file_date()
        expected = encode_datetime(DATE_10260604)
        self.assertEqual(actual, expected)

        self.assertNotCalled(self.chat_post_message_, self.log_,
                             self.open_handle_.write)


if __name__ == '__main__':
    unittest.main()
