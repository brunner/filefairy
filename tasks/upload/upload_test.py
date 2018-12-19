#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for upload.py."""

import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.extend((_path, re.sub(r'/tasks/upload', '', _path)))

from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa
from tasks.upload.upload import Upload  # noqa
from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.datetime_.datetime_ import encode_datetime  # noqa
from common.jinja2_.jinja2_ import env  # noqa
from common.json_.json_ import dumps  # noqa
from common.test.test import Test  # noqa

ENV = env()

DATE_10260602 = datetime_datetime_pst(1985, 10, 26, 6, 2, 30)
DATE_10260604 = datetime_datetime_pst(1985, 10, 26, 6, 4)

DOMAIN_NAME = 'statsplus.net'
FILE_NAME = 'orange%20and%20blue%20league.zip'
FILE_URL = 'https://{}/oblootp/files/{}'.format(DOMAIN_NAME, FILE_NAME)


def _data(date=None):
    return {'date': encode_datetime(date) if date else ''}


class UploadTest(Test):
    def setUp(self):
        patch_chat = mock.patch.object(Upload, '_chat')
        self.addCleanup(patch_chat.stop)
        self.mock_chat = patch_chat.start()

        patch_open = mock.patch(
            'api.serializable.serializable.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]

    def reset_mocks(self):
        self.mock_chat.reset_mock()
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()

    def create_upload(self, data):
        self.init_mocks(data)
        upload = Upload(date=DATE_10260602, e=ENV)

        self.mock_open.assert_called_once_with(Upload._data(), 'r')
        self.assertNotCalled(self.mock_chat, self.mock_handle.write)
        self.assertEqual(upload.data, data)

        self.reset_mocks()
        self.init_mocks(data)

        return upload

    @mock.patch.object(Upload, '_get_date')
    def test_run__new(self, mock_get_date):
        mock_get_date.return_value = encode_datetime(DATE_10260604)

        read = _data(date=DATE_10260602)
        upload = self.create_upload(read)
        actual = upload._run_internal(date=DATE_10260604)
        expected = Response(notify=[Notify.UPLOAD_FINISH])
        self.assertEqual(actual, expected)

        write = _data(date=DATE_10260604)
        mock_get_date.assert_called_once_with()
        self.mock_chat.assert_called_once_with('fairylab', 'File is up.')
        self.mock_open.assert_called_once_with(Upload._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch.object(Upload, '_get_date')
    def test_run__old(self, mock_get_date):
        mock_get_date.return_value = encode_datetime(DATE_10260602)

        read = _data(date=DATE_10260602)
        upload = self.create_upload(read)
        actual = upload._run_internal(date=DATE_10260604)
        expected = Response()
        self.assertEqual(actual, expected)

        mock_get_date.assert_called_once_with()
        self.assertNotCalled(self.mock_chat, self.mock_open,
                             self.mock_handle.write)

    @mock.patch('tasks.upload.upload.get')
    def test_get_date(self, mock_get):
        text = 'League File: Oct. 26, 1985, 8:04 a.m. CST'
        mock_get.return_value = text

        upload = self.create_upload(_data())
        actual = upload._get_date()
        expected = encode_datetime(DATE_10260604)
        self.assertEqual(actual, expected)

        self.assertNotCalled(self.mock_chat, self.mock_open,
                             self.mock_handle.write)


if __name__ == '__main__':
    unittest.main()
