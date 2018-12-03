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

COLS = [col(clazz=c) for c in ('', 'text-center', 'text-center', 'text-right')]
DATE_01010000 = datetime_datetime_pst(2025, 1, 1)
DATE_08280000 = datetime_datetime_pst(2024, 8, 28)
DATE_08310000 = datetime_datetime_pst(2024, 8, 31)
DATE_10250007 = datetime_datetime_pst(1985, 10, 25, 0, 7)
DATE_10260000 = datetime_datetime_pst(1985, 10, 26)
DATE_10260602 = datetime_datetime_pst(1985, 10, 26, 6, 2, 30)
DATE_10260604 = datetime_datetime_pst(1985, 10, 26, 6, 4)
DATE_10260605 = datetime_datetime_pst(1985, 10, 26, 6, 5)
ENV = env()
FILE_HOST = 'www.orangeandblueleaguebaseball.com'
FILE_NAME = 'orange_and_blue_league_baseball.tar.gz'
FILE_URL = 'https://{}/StatsLab/league_file/{}'.format(FILE_HOST, FILE_NAME)
HEAD = [cell(content=c) for c in ('Date', 'Upload', 'Download', 'Size')]


def _data(completed=None,
          date=None,
          download=None,
          end=None,
          stalled=False,
          start=None,
          upload=None):
    if completed is None:
        completed = []

    return {
        'completed': completed,
        'date': encode_datetime(date) if date else '',
        'download': download,
        'end': encode_datetime(end) if end else '',
        'stalled': stalled,
        'start': encode_datetime(start) if start else '',
        'upload': upload
    }


def _completed(download=None, size=None, start=None, upload=None):
    return {
        'download': download if download else '',
        'size': size if size else '',
        'start': encode_datetime(start) if start else '',
        'upload': upload if upload else ''
    }


def _state(end=None, now=None, size=None, start=None):
    d = {}
    if end:
        d['end'] = encode_datetime(end)
    if now:
        d['now'] = encode_datetime(now)
    if size:
        d['size'] = size
    if start:
        d['start'] = encode_datetime(start)
    return d


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
        expected = {
            'leaguefile':
            ['download_file', 'extract_file', 'find_download', 'find_upload']
        }
        self.assertEqual(actual, expected)

        self.assertNotCalled(self.mock_chat, self.mock_log, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Leaguefile, '_get_upload')
    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_get_download')
    def test_run__download(self, mock_download, mock_render, mock_upload):
        mock_download.return_value = Response(notify=[Notify.BASE])

        read = _data(
            download=_state(now=DATE_10260602),
            upload=_state(now=DATE_10260602))
        leaguefile = self.create_leaguefile(read)
        response = leaguefile._run_internal(date=DATE_10260604)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        mock_download.assert_called_once_with(date=DATE_10260604)
        mock_render.assert_called_once_with(date=DATE_10260604)
        self.assertNotCalled(mock_upload, self.mock_chat, self.mock_log,
                             self.mock_open, self.mock_handle.write)

    @mock.patch.object(Leaguefile, '_get_upload')
    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_get_download')
    def test_run__inside_delta(self, mock_download, mock_render, mock_upload):
        mock_upload.return_value = Response()

        read = _data(date=DATE_10260602, upload=_state(now=DATE_10260602))
        leaguefile = self.create_leaguefile(read)
        response = leaguefile._run_internal(date=DATE_10260604)
        self.assertEqual(response, Response())

        mock_upload.assert_called_once_with(date=DATE_10260604)
        self.assertNotCalled(mock_download, mock_render, self.mock_chat,
                             self.mock_log, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Leaguefile, '_get_upload')
    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_get_download')
    def test_run__outside_delta(self, mock_download, mock_render, mock_upload):
        mock_upload.return_value = Response()

        read = _data(date=DATE_10260602, upload=_state(now=DATE_10260602))
        leaguefile = self.create_leaguefile(read)
        response = leaguefile._run_internal(date=DATE_10260605)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        write = _data(date=DATE_10260605, upload=_state(now=DATE_10260602))
        mock_render.assert_called_once_with(date=DATE_10260605)
        mock_upload.assert_called_once_with(date=DATE_10260605)
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.assertNotCalled(mock_download, self.mock_chat, self.mock_log)

    @mock.patch.object(Leaguefile, '_get_upload')
    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_get_download')
    def test_run__upload(self, mock_download, mock_render, mock_upload):
        mock_upload.return_value = Response(notify=[Notify.BASE])

        leaguefile = self.create_leaguefile(_data())
        response = leaguefile._run_internal(date=DATE_10260604)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        mock_render.assert_called_once_with(date=DATE_10260604)
        mock_upload.assert_called_once_with(date=DATE_10260604)
        self.assertNotCalled(mock_download, self.mock_chat, self.mock_log,
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
    @mock.patch.object(Leaguefile, '_call')
    def test_setup__download(self, mock_call, mock_reload, mock_render):
        read = _data(download=_state(now=DATE_10260602))
        leaguefile = self.create_leaguefile(read)
        response = leaguefile._setup_internal(date=DATE_10260604)
        thread_ = Thread(
            target='_download_start', kwargs={'date': DATE_10260604})
        self.assertEqual(response, Response(thread_=[thread_]))

        mock_reload.assert_called_once_with(date=DATE_10260604)
        self.assertNotCalled(mock_call, mock_render, self.mock_chat,
                             self.mock_log, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_reload')
    @mock.patch.object(Leaguefile, '_call')
    def test_setup__ongoing(self, mock_call, mock_reload, mock_render):
        mock_call.return_value = ('100000', DATE_10260602, True)

        read = _data(date=DATE_10260604)
        leaguefile = self.create_leaguefile(read)
        response = leaguefile._setup_internal(date=DATE_10260604)
        self.assertEqual(response, Response())

        upload = _state(
            end=DATE_10260602,
            now=DATE_10260604,
            size='100000',
            start=DATE_10260602)
        write = _data(date=DATE_10260604, upload=upload)
        mock_call.assert_called_once_with('find_upload', (DATE_10260604, ))
        mock_reload.assert_called_once_with(date=DATE_10260604)
        mock_render.assert_called_once_with(date=DATE_10260604)
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.assertNotCalled(self.mock_chat, self.mock_log)

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_reload')
    @mock.patch.object(Leaguefile, '_call')
    def test_setup__uploaded(self, mock_call, mock_reload, mock_render):
        mock_call.return_value = ('345678901', DATE_10260602, False)

        read = _data(date=DATE_10260604)
        leaguefile = self.create_leaguefile(read)
        response = leaguefile._setup_internal(date=DATE_10260604)
        self.assertEqual(response, Response())

        mock_call.assert_called_once_with('find_upload', (DATE_10260604, ))
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

        read = _data(date=DATE_10260604)
        leaguefile = self.create_leaguefile(read)
        response = leaguefile._download_file(date=DATE_10260604)
        thread_ = Thread(
            target='_download_start', kwargs={'date': DATE_10260604})
        self.assertEqual(response, Response(thread_=[thread_]))

        download = _state(end=DATE_10260604, start=DATE_10260604)
        extra = {'stdout': 'o', 'stderr': 'e'}
        write = _data(date=DATE_10260604, download=download)
        mock_call.assert_called_once_with('download_file', (FILE_URL, ))
        self.mock_log.assert_called_once_with(
            logging.WARNING, 'Download failed.', extra=extra)
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.assertNotCalled(mock_extract, self.mock_chat)

    @mock.patch.object(Leaguefile, '_extract_file')
    @mock.patch.object(Leaguefile, '_call')
    def test_download_file__finished(self, mock_call, mock_extract):
        mock_call.return_value = {'ok': True}
        mock_extract.return_value = Response(notify=[Notify.BASE])

        read = _data(date=DATE_10260604)
        leaguefile = self.create_leaguefile(read)
        response = leaguefile._download_file(date=DATE_10260604)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        download = _state(end=DATE_10260604, start=DATE_10260604)
        write = _data(date=DATE_10260604, download=download)
        mock_call.assert_called_once_with('download_file', (FILE_URL, ))
        mock_extract.assert_called_once_with(date=DATE_10260604)
        self.mock_log.assert_called_once_with(logging.INFO,
                                              'Download finished.')
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.assertNotCalled(self.mock_chat)

    @mock.patch.object(Leaguefile, '_download_file')
    @mock.patch('tasks.leaguefile.leaguefile.check_output')
    def test_download_start__failed(self, mock_check, mock_download):
        mock_check.return_value = {'ok': False, 'stdout': 'o', 'stderr': 'e'}

        read = _data(upload=_state(now=DATE_10260602))
        leaguefile = self.create_leaguefile(read)
        response = leaguefile._download_start(date=DATE_10260604)
        thread_ = Thread(
            target='_download_start', kwargs={'date': DATE_10260604})
        self.assertEqual(response, Response(thread_=[thread_]))

        extra = {'stdout': 'o', 'stderr': 'e'}
        mock_check.assert_called_once_with(
            ['ping', '-c 1', FILE_HOST], timeout=8)
        self.mock_log.assert_called_once_with(
            logging.WARNING, 'Download failed.', extra=extra)
        self.assertNotCalled(mock_download, self.mock_chat, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Leaguefile, '_download_file')
    @mock.patch('tasks.leaguefile.leaguefile.check_output')
    def test_download_start__started(self, mock_check, mock_download):
        mock_check.return_value = {'ok': True}
        mock_download.return_value = Response(notify=[Notify.BASE])

        read = _data(upload=_state(now=DATE_10260602))
        leaguefile = self.create_leaguefile(read)
        response = leaguefile._download_start(date=DATE_10260604)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        mock_check.assert_called_once_with(
            ['ping', '-c 1', FILE_HOST], timeout=8)
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
        self.assertEqual(
            response, Response(notify=[Notify.LEAGUEFILE_DOWNLOAD]))

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

    @mock.patch.object(Leaguefile, '_set_completed')
    @mock.patch.object(Leaguefile, '_call')
    def test_get_download__downloaded(self, mock_call, mock_set):
        mock_call.return_value = ('345678901', DATE_10260604, False)

        leaguefile = self.create_leaguefile(_data())
        response = leaguefile._get_download(date=DATE_10260605)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        mock_call.assert_called_once_with('find_download', (DATE_10260605, ))
        mock_set.assert_called_once_with()
        self.assertNotCalled(self.mock_chat, self.mock_log, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Leaguefile, '_set_completed')
    @mock.patch.object(Leaguefile, '_call')
    def test_get_download__ongoing(self, mock_call, mock_set):
        mock_call.return_value = ('100000', DATE_10260604, True)

        read = _data(download=_state(start=DATE_10260602))
        leaguefile = self.create_leaguefile(read)
        response = leaguefile._get_download(date=DATE_10260605)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        download = _state(
            end=DATE_10260604,
            now=DATE_10260605,
            size='100000',
            start=DATE_10260602)
        write = _data(download=download)
        mock_call.assert_called_once_with('find_download', (DATE_10260605, ))
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.assertNotCalled(mock_set, self.mock_chat, self.mock_log)

    @mock.patch.object(Leaguefile, '_handle_uploaded')
    @mock.patch.object(Leaguefile, '_handle_ongoing')
    @mock.patch.object(Leaguefile, '_call')
    def test_get_upload__inactive(self, mock_call, mock_ongoing,
                                  mock_uploaded):
        mock_call.return_value = ('345678901', DATE_10260604, False)
        mock_uploaded.return_value = Response(notify=[Notify.BASE])

        leaguefile = self.create_leaguefile(_data())
        response = leaguefile._get_upload(date=DATE_10260605)
        self.assertEqual(response, Response())

        mock_call.assert_called_once_with('find_upload', (DATE_10260605, ))
        self.assertNotCalled(mock_ongoing, mock_uploaded, self.mock_chat,
                             self.mock_log, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Leaguefile, '_handle_uploaded')
    @mock.patch.object(Leaguefile, '_handle_ongoing')
    @mock.patch.object(Leaguefile, '_call')
    def test_get_upload__ongoing(self, mock_call, mock_ongoing, mock_uploaded):
        mock_call.return_value = ('100000', DATE_10260604, True)
        mock_ongoing.return_value = Response(notify=[Notify.BASE])

        read = _data(upload=_state(start=DATE_10260602))
        leaguefile = self.create_leaguefile(read)
        response = leaguefile._get_upload(date=DATE_10260605)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        mock_call.assert_called_once_with('find_upload', (DATE_10260605, ))
        mock_ongoing.assert_called_once_with(
            '100000', DATE_10260604, date=DATE_10260605)
        self.assertNotCalled(mock_uploaded, self.mock_chat, self.mock_log,
                             self.mock_open, self.mock_handle.write)

    @mock.patch.object(Leaguefile, '_handle_uploaded')
    @mock.patch.object(Leaguefile, '_handle_ongoing')
    @mock.patch.object(Leaguefile, '_call')
    def test_get_upload__uploaded(self, mock_call, mock_ongoing,
                                  mock_uploaded):
        mock_call.return_value = ('345678901', DATE_10260604, False)
        mock_uploaded.return_value = Response(notify=[Notify.BASE])

        read = _data(upload=_state(start=DATE_10260602))
        leaguefile = self.create_leaguefile(read)
        response = leaguefile._get_upload(date=DATE_10260605)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        mock_call.assert_called_once_with('find_upload', (DATE_10260605, ))
        mock_uploaded.assert_called_once_with(
            '345678901', DATE_10260604, date=DATE_10260605)
        self.assertNotCalled(mock_ongoing, self.mock_chat, self.mock_log,
                             self.mock_open, self.mock_handle.write)

    def test_handle_ongoing__ongoing(self):
        upload = _state(
            end=DATE_10260602,
            now=DATE_10260602,
            size='100000',
            start=DATE_10260602)
        read = _data(upload=upload)
        leaguefile = self.create_leaguefile(read)
        response = leaguefile._handle_ongoing(
            '200000', DATE_10260604, date=DATE_10260605)
        self.assertEqual(response, Response())

        upload = _state(
            end=DATE_10260604,
            now=DATE_10260605,
            size='200000',
            start=DATE_10260602)
        write = _data(upload=upload)
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.assertNotCalled(self.mock_chat, self.mock_log)

    def test_handle_ongoing__resumed(self):
        upload = _state(
            end=DATE_10260602,
            now=DATE_10260602,
            size='100000',
            start=DATE_10260602)
        read = _data(stalled=True, upload=upload)
        leaguefile = self.create_leaguefile(read)
        response = leaguefile._handle_ongoing(
            '200000', DATE_10260604, date=DATE_10260605)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        upload = _state(
            end=DATE_10260604,
            now=DATE_10260605,
            size='200000',
            start=DATE_10260602)
        write = _data(upload=upload)
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.assertNotCalled(self.mock_chat, self.mock_log)

    def test_handle_ongoing__stalled(self):
        upload = _state(
            end=DATE_10260602,
            now=DATE_10260604,
            size='100000',
            start=DATE_10260602)
        read = _data(upload=upload)
        leaguefile = self.create_leaguefile(read)
        response = leaguefile._handle_ongoing(
            '100000', DATE_10260602, date=DATE_10260605)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        write = _data(stalled=True, upload=upload)
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.assertNotCalled(self.mock_chat, self.mock_log)

    def test_handle_ongoing__started(self):
        leaguefile = self.create_leaguefile(_data())
        response = leaguefile._handle_ongoing(
            '100000', DATE_10260604, date=DATE_10260605)
        self.assertEqual(response, Response(notify=[Notify.LEAGUEFILE_START]))

        upload = _state(
            end=DATE_10260604,
            now=DATE_10260605,
            size='100000',
            start=DATE_10260604)
        write = _data(upload=upload)
        self.mock_chat.assert_called_once_with('fairylab', 'Upload started.')
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.assertNotCalled(self.mock_log)

    def test_handle_uploaded(self):
        upload = _state(
            end=DATE_10260602,
            now=DATE_10260602,
            size='320000000',
            start=DATE_10260602)
        read = _data(upload=upload)
        leaguefile = self.create_leaguefile(read)
        response = leaguefile._handle_uploaded(
            '345678901', DATE_10260604, date=DATE_10260605)
        thread_ = Thread(
            target='_download_start', kwargs={'date': DATE_10260605})
        self.assertEqual(
            response,
            Response(notify=[Notify.LEAGUEFILE_FINISH], thread_=[thread_]))

        upload = _state(
            end=DATE_10260604,
            now=DATE_10260605,
            size='345678901',
            start=DATE_10260602)
        write = _data(upload=upload)
        self.mock_chat.assert_called_once_with('fairylab', 'File is up.')
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.assertNotCalled(self.mock_log)

    def test_set_completed(self):
        download = _state(
            end=DATE_10260605,
            now=DATE_10260605,
            size='345678901',
            start=DATE_10260604)
        upload = _state(
            end=DATE_10260604,
            now=DATE_10260604,
            size='345678901',
            start=DATE_10260602)
        read = _data(download=download, upload=upload)
        leaguefile = self.create_leaguefile(read)
        leaguefile._set_completed()

        completed = _completed(
            download='1m', size='345678901', start=DATE_10260602, upload='1m')
        write = _data(completed=[completed])
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.assertNotCalled(self.mock_chat, self.mock_log)

    @mock.patch.object(Leaguefile, '_card')
    def test_index_html__completed(self, mock_card):
        completed = _completed(
            download='1m', size='345678901', start=DATE_10260602, upload='1m')
        read = _data(completed=[completed])
        leaguefile = self.create_leaguefile(read)

        breadcrumbs = [{
            'href': '/',
            'name': 'Fairylab'
        }, {
            'href': '',
            'name': 'Leaguefile'
        }]
        actual = leaguefile._index_html(date=DATE_10260602)
        row = [
            cell(content='Oct 26'),
            cell(content='1m'),
            cell(content='1m'),
            cell(content='345,678,901')
        ]
        expected = {
            'breadcrumbs': breadcrumbs,
            'completed': table(hcols=COLS, bcols=COLS, head=HEAD, body=[row])
        }
        self.assertEqual(actual, expected)
        self.assertNotCalled(mock_card, self.mock_chat, self.mock_log,
                             self.mock_open, self.mock_handle.write)

    @mock.patch.object(Leaguefile, '_card')
    def test_index_html__download(self, mock_card):
        mock_card.side_effect = [
            card(success='completed'),
            card(success='ongoing')
        ]

        download = _state(
            end=DATE_10260605,
            now=DATE_10260605,
            size='100000',
            start=DATE_10260604)
        upload = _state(
            end=DATE_10260604,
            now=DATE_10260604,
            size='345678901',
            start=DATE_10260602)
        read = _data(download=download, upload=upload)
        leaguefile = self.create_leaguefile(read)

        breadcrumbs = [{
            'href': '/',
            'name': 'Fairylab'
        }, {
            'href': '',
            'name': 'Leaguefile'
        }]
        actual = leaguefile._index_html(date=DATE_10260602)
        expected = {
            'breadcrumbs': breadcrumbs,
            'download': card(success='ongoing'),
            'upload': card(success='completed'),
            'completed': table(hcols=COLS, bcols=COLS, head=HEAD, body=[])
        }
        mock_card.assert_has_calls([
            mock.call(upload, '06:04:00 PDT (1985-10-26)', 'completed', ''),
            mock.call(download, '06:05:00 PDT (1985-10-26)', 'ongoing', '')
        ])
        self.assertEqual(actual, expected)
        self.assertNotCalled(self.mock_chat, self.mock_log, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Leaguefile, '_card')
    def test_index_html__stalled(self, mock_card):
        mock_card.return_value = card(danger='stalled')

        upload = _state(
            end=DATE_10260604,
            now=DATE_10260604,
            size='100000',
            start=DATE_10260602)
        read = _data(stalled=True, upload=upload)
        leaguefile = self.create_leaguefile(read)

        breadcrumbs = [{
            'href': '/',
            'name': 'Fairylab'
        }, {
            'href': '',
            'name': 'Leaguefile'
        }]
        actual = leaguefile._index_html(date=DATE_10260602)
        expected = {
            'breadcrumbs': breadcrumbs,
            'upload': card(danger='stalled'),
            'completed': table(hcols=COLS, bcols=COLS, head=HEAD, body=[])
        }
        mock_card.assert_called_once_with(upload, '06:04:00 PDT (1985-10-26)',
                                          '', 'stalled')
        self.assertEqual(actual, expected)
        self.assertNotCalled(self.mock_chat, self.mock_log, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Leaguefile, '_card')
    def test_index_html__upload(self, mock_card):
        mock_card.return_value = card(success='ongoing')

        upload = _state(
            end=DATE_10260604,
            now=DATE_10260604,
            size='345678901',
            start=DATE_10260602)
        read = _data(upload=upload)
        leaguefile = self.create_leaguefile(read)

        breadcrumbs = [{
            'href': '/',
            'name': 'Fairylab'
        }, {
            'href': '',
            'name': 'Leaguefile'
        }]
        actual = leaguefile._index_html(date=DATE_10260602)
        expected = {
            'breadcrumbs': breadcrumbs,
            'upload': card(success='ongoing'),
            'completed': table(hcols=COLS, bcols=COLS, head=HEAD, body=[])
        }
        mock_card.assert_called_once_with(upload, '06:04:00 PDT (1985-10-26)',
                                          'ongoing', '')
        self.assertEqual(actual, expected)
        self.assertNotCalled(self.mock_chat, self.mock_log, self.mock_open,
                             self.mock_handle.write)

    def test_card__success(self):
        state = _state(
            end=DATE_10260604,
            now=DATE_10260604,
            size='345678901',
            start=DATE_10260602)
        leaguefile = self.create_leaguefile(_data())
        actual = leaguefile._card(state, '06:04:00 PDT (1985-10-26)',
                                  'ongoing', '')
        expected = card(
            title='Oct 26',
            table=table(
                clazz='table-sm',
                bcols=[col(clazz='w-55p'), col()],
                body=[[cell(content='Time: '),
                       cell(content='1m')],
                      [cell(content='Size: '),
                       cell(content='345,678,901')]]),
            ts='06:04:00 PDT (1985-10-26)',
            success='ongoing',
            danger='')
        self.assertEqual(actual, expected)
        self.assertNotCalled(self.mock_chat, self.mock_log, self.mock_open,
                             self.mock_handle.write)

    def test_card__danger(self):
        state = _state(
            end=DATE_10260604,
            now=DATE_10260604,
            size='345678901',
            start=DATE_10260602)
        leaguefile = self.create_leaguefile(_data())
        actual = leaguefile._card(state, '06:04:00 PDT (1985-10-26)', '',
                                  'stalled')
        expected = card(
            title='Oct 26',
            table=table(
                clazz='table-sm',
                bcols=[col(clazz='w-55p'), col()],
                body=[[cell(content='Time: '),
                       cell(content='1m')],
                      [cell(content='Size: '),
                       cell(content='345,678,901')]]),
            ts='06:04:00 PDT (1985-10-26)',
            success='',
            danger='stalled')
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
