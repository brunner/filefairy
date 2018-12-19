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

from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa
from data.shadow.shadow import Shadow  # noqa
from data.thread_.thread_ import Thread  # noqa
from tasks.download.download import Download  # noqa
from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.datetime_.datetime_ import encode_datetime  # noqa
from common.jinja2_.jinja2_ import env  # noqa
from common.json_.json_ import dumps  # noqa
from common.test.test import Test  # noqa

ENV = env()

DATE_01010000 = datetime_datetime_pst(2025, 1, 1)
DATE_08280000 = datetime_datetime_pst(2024, 8, 28)
DATE_08310000 = datetime_datetime_pst(2024, 8, 31)
DATE_10250007 = datetime_datetime_pst(1985, 10, 25, 0, 7)
DATE_10260000 = datetime_datetime_pst(1985, 10, 26)
DATE_10260602 = datetime_datetime_pst(1985, 10, 26, 6, 2, 30)
DATE_10260604 = datetime_datetime_pst(1985, 10, 26, 6, 4)
DATE_10260605 = datetime_datetime_pst(1985, 10, 26, 6, 5)

DOMAIN_NAME = 'statsplus.net'
FILE_NAME = 'orange%20and%20blue%20league.zip'
FILE_URL = 'https://{}/oblootp/files/{}'.format(DOMAIN_NAME, FILE_NAME)


def _data(end=None, start=None):
    return {
        'end': encode_datetime(end) if end else '',
        'start': encode_datetime(start) if start else '',
    }


class DownloadTest(Test):
    def setUp(self):
        patch_log = mock.patch('tasks.download.download._logger.log')
        self.addCleanup(patch_log.stop)
        self.mock_log = patch_log.start()

        patch_open = mock.patch(
            'api.serializable.serializable.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]

    def reset_mocks(self):
        self.mock_log.reset_mock()
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()

    def create_download(self, data):
        self.init_mocks(data)
        download = Download(date=DATE_10250007, e=ENV)

        self.mock_open.assert_called_once_with(Download._data(), 'r')
        self.assertNotCalled(self.mock_log, self.mock_handle.write)
        self.assertEqual(download.data, data)

        self.reset_mocks()
        self.init_mocks(data)

        return download

    @mock.patch.object(Download, 'start')
    def test_notify__upload(self, mock_start):
        response = Response(thread_=[Thread(target='_download_start')])
        mock_start.return_value = response

        download = self.create_download(_data())
        actual = download._notify_internal(notify=Notify.UPLOAD_FINISH)
        self.assertEqual(actual, response)

        mock_start.assert_called_once_with(notify=Notify.UPLOAD_FINISH)
        self.assertNotCalled(self.mock_log, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Download, 'start')
    def test_notify__other(self, mock_start):
        download = self.create_download(_data())
        actual = download._notify_internal(notify=Notify.OTHER)
        self.assertEqual(actual, Response())

        self.assertNotCalled(mock_start, self.mock_log, self.mock_open,
                             self.mock_handle.write)

    def test_reload(self):
        download = self.create_download(_data())
        actual = download._reload_internal(date=DATE_10260602)
        expected = {'leaguefile': ['download_file', 'extract_file']}
        self.assertEqual(actual, expected)

        self.assertNotCalled(self.mock_log, self.mock_open,
                             self.mock_handle.write)

    def test_setup(self):
        download = self.create_download(_data())
        response = download._setup_internal(date=DATE_10260604)
        self.assertEqual(response, Response())

        self.assertNotCalled(self.mock_log, self.mock_open,
                             self.mock_handle.write)

    def test_shadow(self):
        download = self.create_download(_data(end=DATE_10260602))
        actual = download._shadow_internal(date=DATE_10260604)
        date = encode_datetime(DATE_10260602)
        shadow = Shadow(destination='statsplus', key='download.end', info=date)
        self.assertEqual(actual, [shadow])

        self.assertNotCalled(self.mock_log, self.mock_open,
                             self.mock_handle.write)

    def test_start(self):
        download = self.create_download(_data(end=DATE_10260602))
        response = download.start(date=DATE_10260604)
        thread_ = Thread(
            target='_download_start', kwargs={'date': DATE_10260604})
        self.assertEqual(response, Response(thread_=[thread_]))

        self.assertNotCalled(self.mock_log, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Download, '_extract_file')
    @mock.patch.object(Download, '_call')
    def test_download_file__failed(self, mock_call, mock_extract):
        mock_call.return_value = {'ok': False, 'stdout': 'o', 'stderr': 'e'}

        now = DATE_10260604
        download = self.create_download(_data())
        response = download._download_file(date=now)
        thread_ = Thread(target='_download_start', kwargs={'date': now})
        self.assertEqual(response, Response(thread_=[thread_]))

        extra = {'stdout': 'o', 'stderr': 'e'}
        mock_call.assert_called_once_with('download_file', (FILE_URL, ))
        self.mock_log.assert_called_once_with(
            logging.WARNING, 'Download failed.', extra=extra)
        self.assertNotCalled(mock_extract, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Download, '_extract_file')
    @mock.patch.object(Download, '_call')
    def test_download_file__finished(self, mock_call, mock_extract):
        mock_call.return_value = {'ok': True}
        mock_extract.return_value = Response(notify=[Notify.BASE])

        now = DATE_10260604
        download = self.create_download(_data())
        response = download._download_file(date=now)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        mock_call.assert_called_once_with('download_file', (FILE_URL, ))
        mock_extract.assert_called_once_with(date=now)
        self.mock_log.assert_called_once_with(logging.INFO,
                                              'Download finished.')
        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    @mock.patch.object(Download, '_download_file')
    @mock.patch('tasks.download.download.check_output')
    def test_download_start__failed(self, mock_check, mock_download):
        mock_check.return_value = {'ok': False, 'stdout': 'o', 'stderr': 'e'}

        download = self.create_download(_data())
        response = download._download_start(date=DATE_10260604)
        thread_ = Thread(
            target='_download_start', kwargs={'date': DATE_10260604})
        self.assertEqual(response, Response(thread_=[thread_]))

        extra = {'stdout': 'o', 'stderr': 'e'}
        mock_check.assert_called_once_with(['ping', '-c 1', DOMAIN_NAME],
                                           timeout=10)
        self.mock_log.assert_called_once_with(
            logging.WARNING, 'Download failed.', extra=extra)
        self.assertNotCalled(mock_download, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Download, '_download_file')
    @mock.patch('tasks.download.download.check_output')
    def test_download_start__started(self, mock_check, mock_download):
        mock_check.return_value = {'ok': True}
        mock_download.return_value = Response(notify=[Notify.BASE])

        download = self.create_download(_data())
        response = download._download_start(date=DATE_10260604)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        mock_check.assert_called_once_with(['ping', '-c 1', DOMAIN_NAME],
                                           timeout=10)
        mock_download.assert_called_once_with(date=DATE_10260604)
        self.mock_log.assert_called_once_with(logging.INFO,
                                              'Download started.')
        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    @mock.patch.object(Download, '_shadow_internal')
    @mock.patch.object(Download, '_call')
    def test_extract_file__start(self, mock_call, mock_shadow):
        mock_call.return_value = DATE_08310000

        read = _data(end=DATE_08280000)
        download = self.create_download(read)
        response = download._extract_file(date=DATE_10260604)
        self.assertEqual(response,
                         Response(notify=[Notify.DOWNLOAD_FINISH]))

        write = _data(end=DATE_08310000, start=DATE_08280000)
        mock_call.assert_called_once_with('extract_file', (DATE_08280000, ))
        self.mock_open.assert_called_once_with(Download._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.assertNotCalled(mock_shadow, self.mock_log)

    @mock.patch.object(Download, '_shadow_internal')
    @mock.patch.object(Download, '_call')
    def test_extract_file__year(self, mock_call, mock_shadow):
        shadow = Shadow(destination='statsplus', key='download.end', info='')
        mock_call.return_value = DATE_01010000
        mock_shadow.return_value = [shadow]

        read = _data(end=DATE_08280000)
        download = self.create_download(read)
        response = download._extract_file(date=DATE_10260604)
        self.assertEqual(
            response,
            Response(
                notify=[Notify.DOWNLOAD_FINISH, Notify.DOWNLOAD_YEAR],
                shadow=[shadow]))

        write = _data(end=DATE_01010000, start=DATE_08280000)
        mock_call.assert_called_once_with('extract_file', (DATE_08280000, ))
        mock_shadow.assert_called_once_with(date=DATE_10260604)
        self.mock_open.assert_called_once_with(Download._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.assertNotCalled(self.mock_log)


if __name__ == '__main__':
    unittest.main()
