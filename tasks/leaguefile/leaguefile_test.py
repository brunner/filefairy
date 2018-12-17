#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for leaguefile.py."""

import logging
import os
import re
import sys
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(_path)
_root = re.sub(r'/tasks/leaguefile', '', _path)
sys.path.append(_root)
from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa
from data.shadow.shadow import Shadow  # noqa
from data.thread_.thread_ import Thread  # noqa
from tasks.leaguefile.leaguefile import Leaguefile  # noqa
from common.elements.elements import card  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import table  # noqa
from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.datetime_.datetime_ import encode_datetime  # noqa
from common.jinja2_.jinja2_ import env  # noqa
from common.json_.json_ import dumps  # noqa
from common.secrets.secrets import server  # noqa
from common.test.test import Test  # noqa
from common.test.test import main  # noqa

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


def _data(completed=None, end=None, start=None):
    if completed is None:
        completed = []

    return {
        'completed': completed,
        'end': encode_datetime(end) if end else '',
        'start': encode_datetime(start) if start else '',
    }


def _completed(date=None, size=None):
    return {
        'date': encode_datetime(date) if date else '',
        'size': size if size else '',
    }


class LeaguefileTest(Test):
    def setUp(self):
        patch_chat = mock.patch.object(Leaguefile, '_chat')
        self.addCleanup(patch_chat.stop)
        self.mock_chat = patch_chat.start()

        patch_log = mock.patch('tasks.leaguefile.leaguefile._logger.log')
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
        self.mock_chat.reset_mock()
        self.mock_log.reset_mock()
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()

    def create_leaguefile(self, data):
        self.init_mocks(data)
        leaguefile = Leaguefile(date=DATE_10250007, e=ENV)

        self.mock_open.assert_called_once_with(Leaguefile._data(), 'r')
        self.assertNotCalled(self.mock_chat, self.mock_log,
                             self.mock_handle.write)
        self.assertEqual(leaguefile.data, data)

        self.reset_mocks()
        self.init_mocks(data)

        return leaguefile

    def test_notify(self):
        leaguefile = self.create_leaguefile(_data())
        response = leaguefile._notify_internal(
            date=DATE_10260602, notify=Notify.OTHER)
        self.assertEqual(response, Response())

        self.assertNotCalled(self.mock_chat, self.mock_log, self.mock_open,
                             self.mock_handle.write)

    def test_on_message(self):
        leaguefile = self.create_leaguefile(_data())
        response = leaguefile._on_message_internal(date=DATE_10260602)
        self.assertEqual(response, Response())

        self.assertNotCalled(self.mock_chat, self.mock_log, self.mock_open,
                             self.mock_handle.write)

    def test_reload(self):
        leaguefile = self.create_leaguefile(_data())
        actual = leaguefile._reload_internal(date=DATE_10260602)
        expected = {'leaguefile': ['download_file', 'extract_file']}
        self.assertEqual(actual, expected)

        self.assertNotCalled(self.mock_chat, self.mock_log, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_get_completed')
    def test_run__completed(self, mock_completed, mock_render):
        new = _completed(date=DATE_10260604, size='384,530,143')
        mock_completed.return_value = new

        old = _completed(date=DATE_10260602, size='345,678,901')
        read = _data(completed=[old])
        leaguefile = self.create_leaguefile(read)
        actual = leaguefile._run_internal(date=DATE_10260604)
        thread_ = Thread(
            target='_download_start', kwargs={'date': DATE_10260604})
        expected = Response(
            notify=[Notify.BASE, Notify.LEAGUEFILE_UPLOAD], thread_=[thread_])
        self.assertEqual(actual, expected)

        write = _data(completed=[new, old])
        mock_completed.assert_called_once_with()
        mock_render.assert_called_once_with(date=DATE_10260604)
        self.mock_chat.assert_called_once_with('fairylab', 'File is up.')
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.assertNotCalled(self.mock_log)

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_get_completed')
    def test_run__unchanged(self, mock_completed, mock_render):
        old = _completed(date=DATE_10260604, size='384,530,143')
        mock_completed.return_value = old

        read = _data(completed=[old])
        leaguefile = self.create_leaguefile(read)
        actual = leaguefile._run_internal(date=DATE_10260604)
        expected = Response()
        self.assertEqual(actual, expected)

        mock_completed.assert_called_once_with()
        self.assertNotCalled(mock_render, self.mock_chat, self.mock_log,
                             self.mock_open, self.mock_handle.write)

    @mock.patch.object(Leaguefile, '_index_html')
    def test_render(self, mock_index):
        index_html = {'breadcrumbs': []}
        mock_index.return_value = index_html

        leaguefile = self.create_leaguefile(_data())
        actual = leaguefile._render_internal(date=DATE_10260602)
        expected = [('leaguefile/index.html', '', 'leaguefile.html',
                     index_html)]
        self.assertEqual(actual, expected)

        mock_index.assert_called_once_with(date=DATE_10260602)
        self.assertNotCalled(self.mock_chat, self.mock_log, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_reload')
    def test_setup(self, mock_reload, mock_render):
        leaguefile = self.create_leaguefile(_data())
        response = leaguefile._setup_internal(date=DATE_10260604)
        self.assertEqual(response, Response())

        mock_reload.assert_called_once_with(date=DATE_10260604)
        mock_render.assert_called_once_with(date=DATE_10260604)
        self.assertNotCalled(self.mock_chat, self.mock_log, self.mock_open,
                             self.mock_handle.write)

    def test_shadow(self):
        leaguefile = self.create_leaguefile(_data(end=DATE_10260602))
        actual = leaguefile._shadow_internal(date=DATE_10260604)
        date = encode_datetime(DATE_10260602)
        shadow = Shadow(
            destination='statsplus', key='leaguefile.end', info=date)
        self.assertEqual(actual, [shadow])

        self.assertNotCalled(self.mock_chat, self.mock_log, self.mock_open,
                             self.mock_handle.write)

    def test_download(self):
        leaguefile = self.create_leaguefile(_data(end=DATE_10260602))
        response = leaguefile.download(date=DATE_10260604)
        thread_ = Thread(
            target='_download_start', kwargs={'date': DATE_10260604})
        self.assertEqual(response, Response(thread_=[thread_]))

        self.assertNotCalled(self.mock_chat, self.mock_log, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Leaguefile, '_extract_file')
    @mock.patch.object(Leaguefile, '_call')
    def test_download_file__failed(self, mock_call, mock_extract):
        mock_call.return_value = {'ok': False, 'stdout': 'o', 'stderr': 'e'}

        now = DATE_10260604
        leaguefile = self.create_leaguefile(_data())
        response = leaguefile._download_file(date=now)
        thread_ = Thread(target='_download_start', kwargs={'date': now})
        self.assertEqual(response, Response(thread_=[thread_]))

        extra = {'stdout': 'o', 'stderr': 'e'}
        mock_call.assert_called_once_with('download_file', (FILE_URL, ))
        self.mock_log.assert_called_once_with(
            logging.WARNING, 'Download failed.', extra=extra)
        self.assertNotCalled(mock_extract, self.mock_chat, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Leaguefile, '_extract_file')
    @mock.patch.object(Leaguefile, '_call')
    def test_download_file__finished(self, mock_call, mock_extract):
        mock_call.return_value = {'ok': True}
        mock_extract.return_value = Response(notify=[Notify.BASE])

        now = DATE_10260604
        leaguefile = self.create_leaguefile(_data())
        response = leaguefile._download_file(date=now)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        mock_call.assert_called_once_with('download_file', (FILE_URL, ))
        mock_extract.assert_called_once_with(date=now)
        self.mock_log.assert_called_once_with(logging.INFO,
                                              'Download finished.')
        self.assertNotCalled(self.mock_chat, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Leaguefile, '_download_file')
    @mock.patch('tasks.leaguefile.leaguefile.check_output')
    def test_download_start__failed(self, mock_check, mock_download):
        mock_check.return_value = {'ok': False, 'stdout': 'o', 'stderr': 'e'}

        leaguefile = self.create_leaguefile(_data())
        response = leaguefile._download_start(date=DATE_10260604)
        thread_ = Thread(
            target='_download_start', kwargs={'date': DATE_10260604})
        self.assertEqual(response, Response(thread_=[thread_]))

        extra = {'stdout': 'o', 'stderr': 'e'}
        mock_check.assert_called_once_with(['ping', '-c 1', DOMAIN_NAME],
                                           timeout=10)
        self.mock_log.assert_called_once_with(
            logging.WARNING, 'Download failed.', extra=extra)
        self.assertNotCalled(mock_download, self.mock_chat, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Leaguefile, '_download_file')
    @mock.patch('tasks.leaguefile.leaguefile.check_output')
    def test_download_start__started(self, mock_check, mock_download):
        mock_check.return_value = {'ok': True}
        mock_download.return_value = Response(notify=[Notify.BASE])

        leaguefile = self.create_leaguefile(_data())
        response = leaguefile._download_start(date=DATE_10260604)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        mock_check.assert_called_once_with(['ping', '-c 1', DOMAIN_NAME],
                                           timeout=10)
        mock_download.assert_called_once_with(date=DATE_10260604)
        self.mock_log.assert_called_once_with(logging.INFO,
                                              'Download started.')
        self.assertNotCalled(self.mock_chat, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Leaguefile, '_shadow_internal')
    @mock.patch.object(Leaguefile, '_call')
    def test_extract_file__start(self, mock_call, mock_shadow):
        mock_call.return_value = DATE_08310000

        read = _data(end=DATE_08280000)
        leaguefile = self.create_leaguefile(read)
        response = leaguefile._extract_file(date=DATE_10260604)
        self.assertEqual(response,
                         Response(notify=[Notify.LEAGUEFILE_DOWNLOAD]))

        write = _data(end=DATE_08310000, start=DATE_08280000)
        mock_call.assert_called_once_with('extract_file', (DATE_08280000, ))
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.assertNotCalled(mock_shadow, self.mock_chat, self.mock_log)

    @mock.patch.object(Leaguefile, '_shadow_internal')
    @mock.patch.object(Leaguefile, '_call')
    def test_extract_file__year(self, mock_call, mock_shadow):
        shadow = Shadow(destination='statsplus', key='leaguefile.end', info='')
        mock_call.return_value = DATE_01010000
        mock_shadow.return_value = [shadow]

        read = _data(end=DATE_08280000)
        leaguefile = self.create_leaguefile(read)
        response = leaguefile._extract_file(date=DATE_10260604)
        self.assertEqual(
            response,
            Response(
                notify=[Notify.LEAGUEFILE_DOWNLOAD, Notify.LEAGUEFILE_YEAR],
                shadow=[shadow]))

        write = _data(end=DATE_01010000, start=DATE_08280000)
        mock_call.assert_called_once_with('extract_file', (DATE_08280000, ))
        mock_shadow.assert_called_once_with(date=DATE_10260604)
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.assertNotCalled(self.mock_chat, self.mock_log)

    @mock.patch('tasks.leaguefile.leaguefile.get')
    def test_get_completed(self, mock_get):
        text = 'League File: Oct. 26, 1985, 8:04 a.m. CST\n(Size: 345,678,901)'
        mock_get.return_value = text

        leaguefile = self.create_leaguefile(_data())
        actual = leaguefile._get_completed()
        expected = _completed(date=DATE_10260604, size='345,678,901')
        self.assertEqual(actual, expected)

        self.assertNotCalled(self.mock_chat, self.mock_log, self.mock_open,
                             self.mock_handle.write)

    def test_index_html(self):
        completed = _completed(date=DATE_10260604, size='345,678,901')
        read = _data(completed=[completed])
        leaguefile = self.create_leaguefile(read)

        breadcrumbs = [{
            'href': '/',
            'name': 'Fairylab'
        }, {
            'href': '',
            'name': 'Leaguefile'
        }]
        actual = leaguefile._index_html(date=DATE_10260604)
        cols = [col(), col(clazz='text-right')]
        head = [cell(content='Date'), cell(content='Size')]
        row = [cell(content='Oct 26'), cell(content='345,678,901')]
        expected = {
            'breadcrumbs': breadcrumbs,
            'completed': table(hcols=cols, bcols=cols, head=head, body=[row])
        }
        self.assertEqual(actual, expected)
        self.assertNotCalled(self.mock_chat, self.mock_log, self.mock_open,
                             self.mock_handle.write)


if __name__ in ['__main__', 'tasks.leaguefile.leaguefile_test']:
    main(
        LeaguefileTest,
        Leaguefile,
        'tasks.leaguefile',
        'tasks/leaguefile', {},
        __name__ == '__main__',
        date=DATE_10260602,
        e=ENV)
