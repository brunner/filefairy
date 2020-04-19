#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for download.py."""

import logging
import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.extend((_path, re.sub(r'/tasks/download', '', _path)))

from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.datetime_.datetime_ import encode_datetime  # noqa
from common.json_.json_ import dumps  # noqa
from common.test.test import Test  # noqa
from tasks.download.download import Download  # noqa
from types_.notify.notify import Notify  # noqa
from types_.response.response import Response  # noqa
from types_.thread_.thread_ import Thread  # noqa

DATE_01010000 = datetime_datetime_pst(2025, 1, 1)
DATE_08280000 = datetime_datetime_pst(2024, 8, 28)
DATE_08310000 = datetime_datetime_pst(2024, 8, 31)
DATE_10250007 = datetime_datetime_pst(1985, 10, 25, 0, 7)
DATE_10260000 = datetime_datetime_pst(1985, 10, 26)
DATE_10260602 = datetime_datetime_pst(1985, 10, 26, 6, 2, 30)
DATE_10260604 = datetime_datetime_pst(1985, 10, 26, 6, 4)
DATE_10260605 = datetime_datetime_pst(1985, 10, 26, 6, 5)

DOMAIN_NAME = 'statsplus.net'
FILE_NAME = 'orange%20and%20blue%20league%20baseball.zip'
FILE_URL = 'https://{}/oblootp/files/{}'.format(DOMAIN_NAME, FILE_NAME)


def _data(end=None, start=None):
    return {
        'end': encode_datetime(end) if end else '',
        'start': encode_datetime(start) if start else '',
    }


class DownloadTest(Test):
    def setUp(self):
        log_patch = mock.patch('tasks.download.download._logger.log')
        self.addCleanup(log_patch.stop)
        self.log_ = log_patch.start()

        open_patch = mock.patch('common.io_.io_.open', create=True)
        self.addCleanup(open_patch.stop)
        self.open_ = open_patch.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.open_handle_ = mo()
        self.open_.side_effect = [mo.return_value]

    def reset_mocks(self):
        self.log_.reset_mock()
        self.open_handle_.write.reset_mock()

    def create_download(self, data):
        self.init_mocks(data)
        download = Download(date=DATE_10250007)

        self.assertEqual(download.data, data)

        self.reset_mocks()
        self.init_mocks(data)

        return download

    @mock.patch.object(Download, 'start')
    def test_notify__upload_finish(self, mock_start):
        response = Response(thread_=[Thread(target='download_start')])
        mock_start.return_value = response

        download = self.create_download(_data())
        actual = download._notify_internal(notify=Notify.UPLOAD_FINISH)
        self.assertEqual(actual, response)

        mock_start.assert_called_once_with(notify=Notify.UPLOAD_FINISH)
        self.assertNotCalled(self.log_, self.open_handle_.write)

    @mock.patch.object(Download, 'start')
    def test_notify__other(self, mock_start):
        download = self.create_download(_data())
        actual = download._notify_internal(notify=Notify.OTHER)
        self.assertEqual(actual, Response())

        self.assertNotCalled(mock_start, self.log_, self.open_handle_.write)

    def test_start(self):
        download = self.create_download(_data(end=DATE_10260602))
        response = download.start(date=DATE_10260604)
        thread_ = Thread(target='download_start',
                         kwargs={'date': DATE_10260604})
        self.assertEqual(response, Response(thread_=[thread_]))

        self.assertNotCalled(self.log_, self.open_handle_.write)

    @mock.patch.object(Download, 'extract_file')
    @mock.patch('tasks.download.download.call_service')
    def test_download_file__failed(self, call_service_, extract_file_):
        call_service_.return_value = {
            'ok': False,
            'stdout': 'o',
            'stderr': 'e'
        }

        now = DATE_10260604
        download = self.create_download(_data())
        response = download.download_file(date=now)
        thread_ = Thread(target='download_start', kwargs={'date': now})
        self.assertEqual(response, Response(thread_=[thread_]))

        extra = {'stdout': 'o', 'stderr': 'e'}
        call_service_.assert_called_once_with('leaguefile', 'download_file',
                                              (FILE_URL, ))
        self.log_.assert_called_once_with(logging.WARNING,
                                          'Download failed.',
                                          extra=extra)
        self.assertNotCalled(extract_file_, self.open_handle_.write)

    @mock.patch.object(Download, 'extract_file')
    @mock.patch('tasks.download.download.call_service')
    def test_download_file__finished(self, call_service_, extract_file_):
        call_service_.return_value = {'ok': True}
        extract_file_.return_value = Response(notify=[Notify.BASE])

        now = DATE_10260604
        download = self.create_download(_data())
        response = download.download_file(date=now)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        call_service_.assert_called_once_with('leaguefile', 'download_file',
                                              (FILE_URL, ))
        extract_file_.assert_called_once_with(date=now)
        self.log_.assert_called_once_with(logging.INFO, 'Download finished.')
        self.assertNotCalled(self.open_handle_.write)

    @mock.patch.object(Download, 'download_file')
    @mock.patch('tasks.download.download.check_output')
    def test_download_start__failed(self, check_output_, download_file_):
        check_output_.return_value = {
            'ok': False,
            'stdout': 'o',
            'stderr': 'e'
        }

        download = self.create_download(_data())
        response = download.download_start(date=DATE_10260604)
        thread_ = Thread(target='download_start',
                         kwargs={'date': DATE_10260604})
        self.assertEqual(response, Response(thread_=[thread_]))

        extra = {'stdout': 'o', 'stderr': 'e'}
        check_output_.assert_called_once_with(['ping', '-c 1', DOMAIN_NAME],
                                              timeout=10)
        self.log_.assert_called_once_with(logging.WARNING,
                                          'Download failed.',
                                          extra=extra)
        self.assertNotCalled(download_file_, self.open_handle_.write)

    @mock.patch.object(Download, 'download_file')
    @mock.patch('tasks.download.download.check_output')
    def test_download_start__started(self, check_output_, download_file_):
        check_output_.return_value = {'ok': True}
        download_file_.return_value = Response(notify=[Notify.BASE])

        download = self.create_download(_data())
        response = download.download_start(date=DATE_10260604)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        check_output_.assert_called_once_with(['ping', '-c 1', DOMAIN_NAME],
                                              timeout=10)
        download_file_.assert_called_once_with(date=DATE_10260604)
        self.log_.assert_called_once_with(logging.INFO, 'Download started.')
        self.assertNotCalled(self.open_handle_.write)

    @mock.patch('tasks.download.download.call_service')
    def test_extract_file__start(self, call_service_):
        call_service_.return_value = DATE_08310000

        read = _data(end=DATE_08280000)
        download = self.create_download(read)
        response = download.extract_file(date=DATE_10260604)
        self.assertEqual(response, Response(notify=[Notify.DOWNLOAD_FINISH]))

        write = _data(end=DATE_08310000, start=DATE_08280000)
        call_service_.assert_called_once_with('leaguefile', 'extract_file',
                                              (DATE_08280000, ))
        self.open_handle_.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch('tasks.download.download.call_service')
    def test_extract_file__year(self, call_service_):
        call_service_.return_value = DATE_01010000

        read = _data(end=DATE_08280000)
        download = self.create_download(read)
        response = download.extract_file(date=DATE_10260604)
        self.assertEqual(
            response,
            Response(notify=[Notify.DOWNLOAD_FINISH, Notify.DOWNLOAD_YEAR]))

        write = _data(end=DATE_01010000, start=DATE_08280000)
        call_service_.assert_called_once_with('leaguefile', 'extract_file',
                                              (DATE_08280000, ))
        self.open_handle_.write.assert_called_once_with(dumps(write) + '\n')
        self.assertNotCalled(self.log_)


if __name__ == '__main__':
    unittest.main()
