#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for leaguefile.py."""

import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/services/leaguefile', '', _path))

from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.secrets.secrets import server  # noqa
from common.test.test import get_testdata  # noqa
from services.leaguefile.leaguefile import download_file  # noqa
from services.leaguefile.leaguefile import extract_file  # noqa
from services.leaguefile.leaguefile import find_download  # noqa
from services.leaguefile.leaguefile import find_upload  # noqa

CWD_DIR = re.sub(r'/services/leaguefile', '', _path)
DATE_08280000 = datetime_datetime_pst(2024, 8, 28)
DATE_08310000 = datetime_datetime_pst(2024, 8, 31)
DATE_10260000 = datetime_datetime_pst(1985, 10, 26)
DATE_10260604 = datetime_datetime_pst(1985, 10, 26, 6, 4)
DOWNLOAD_DIR = re.sub(r'/services/leaguefile', '/resource/download', _path)
DOWNLOAD_BOX_SCORES = os.path.join(DOWNLOAD_DIR, 'news/html/box_scores')
DOWNLOAD_LEAGUES = os.path.join(DOWNLOAD_DIR, 'news/txt/leagues')
EXTRACT_DIR = re.sub(r'/services/leaguefile', '/resource/extract', _path)
EXTRACT_BOX_SCORES = os.path.join(EXTRACT_DIR, 'box_scores')
EXTRACT_GAME_LOGS = os.path.join(EXTRACT_DIR, 'game_logs')
EXTRACT_LEAGUES = os.path.join(EXTRACT_DIR, 'leagues')
FILE_HOST = 'https://www.orangeandblueleaguebaseball.com/StatsLab/league_file/'
FILE_NAME = 'orange_and_blue_league_baseball.tar.gz'
ISO = 'iso-8859-1'
SERVER = server()
TESTDATA_DIR = os.path.join(_path, 'testdata')
TESTDATA = get_testdata(TESTDATA_DIR)


class Mock(object):
    def __init__(self, read=None, write=None):
        self.mo = mock.mock_open(read_data=read)
        self.mock_handle = self.mo()
        self.write = write


class ReadMock(Mock):
    def __init__(self, path, filename):
        self.call = mock.call(os.path.join(path, filename), 'r', encoding=ISO)
        super().__init__(read=TESTDATA[filename])


class WriteMock(Mock):
    def __init__(self, path, filename):
        self.call = mock.call(os.path.join(path, filename), 'w')
        super().__init__(write=TESTDATA[filename])


class Suite(object):
    def __init__(self, *mocks):
        self.mocks = mocks

    def calls(self):
        return [m.call for m in self.mocks]

    def values(self):
        return [m.mo.return_value for m in self.mocks]

    def verify(self):
        for m in self.mocks:
            if m.write is not None:
                m.mock_handle.write.assert_called_once_with(m.write)


class LeaguefileTest(unittest.TestCase):
    @mock.patch('services.leaguefile.leaguefile.chdir')
    @mock.patch('services.leaguefile.leaguefile.check_output')
    def test_download_file__ok(self, mock_check, mock_chdir):
        url = FILE_HOST + FILE_NAME
        expected = {'ok': True}
        mock_check.return_value = expected

        actual = download_file(url)
        self.assertEqual(actual, expected)

        mock_check.assert_has_calls([
            mock.call(['rm', '-rf', DOWNLOAD_DIR]),
            mock.call(['mkdir', DOWNLOAD_DIR]),
            mock.call(['wget', url], timeout=4800),
            mock.call(['tar', '-xzf', FILE_NAME]),
        ])
        mock_chdir.assert_called_once_with(DOWNLOAD_DIR)

    @mock.patch('services.leaguefile.leaguefile.chdir')
    @mock.patch('services.leaguefile.leaguefile.check_output')
    def test_download_file__timeout(self, mock_check, mock_chdir):
        url = FILE_HOST + FILE_NAME
        e = 'Command \'wget {}\' timed out after {} seconds'.format(url, 4800)
        expected = {'ok': False, 'stdout': e, 'stderr': e}
        mock_check.return_value = expected

        actual = download_file(url)
        self.assertEqual(actual, expected)

        mock_check.assert_has_calls([
            mock.call(['rm', '-rf', DOWNLOAD_DIR]),
            mock.call(['mkdir', DOWNLOAD_DIR]),
            mock.call(['wget', url], timeout=4800),
        ])
        mock_chdir.assert_called_once_with(DOWNLOAD_DIR)

    @mock.patch('services.leaguefile.leaguefile.open', create=True)
    @mock.patch('services.leaguefile.leaguefile.os.listdir')
    @mock.patch('services.leaguefile.leaguefile.os.path.isfile')
    @mock.patch('services.leaguefile.leaguefile.check_output')
    def test_extract_file(self, mock_check, mock_isfile, mock_listdir,
                          mock_open):
        mock_isfile.return_value = True
        mock_listdir.return_value = [
            'game_box_2449.html', 'game_box_2469.html', 'game_box_2476.html'
        ]
        suite = Suite(
            ReadMock(DOWNLOAD_BOX_SCORES, 'game_box_2449.html'),
            ReadMock(DOWNLOAD_LEAGUES, 'log_2449.txt'),
            WriteMock(EXTRACT_BOX_SCORES, 'game_box_2449.html'),
            WriteMock(EXTRACT_GAME_LOGS, 'log_2449.txt'),
            ReadMock(DOWNLOAD_BOX_SCORES, 'game_box_2469.html'),
            ReadMock(DOWNLOAD_LEAGUES, 'log_2469.txt'),
            WriteMock(EXTRACT_BOX_SCORES, 'game_box_2469.html'),
            WriteMock(EXTRACT_GAME_LOGS, 'log_2469.txt'),
            ReadMock(DOWNLOAD_BOX_SCORES, 'game_box_2476.html'),
            ReadMock(DOWNLOAD_LEAGUES, 'log_2476.txt'),
            WriteMock(EXTRACT_BOX_SCORES, 'game_box_2476.html'),
            WriteMock(EXTRACT_GAME_LOGS, 'log_2476.txt'),
            ReadMock(DOWNLOAD_LEAGUES, 'league_100_injuries.txt'),
            WriteMock(EXTRACT_LEAGUES, 'injuries.txt'),
            ReadMock(DOWNLOAD_LEAGUES, 'league_100_news.txt'),
            WriteMock(EXTRACT_LEAGUES, 'news.txt'),
            ReadMock(DOWNLOAD_LEAGUES, 'league_100_transactions.txt'),
            WriteMock(EXTRACT_LEAGUES, 'transactions.txt'),
        )
        mock_open.side_effect = suite.values()

        actual = extract_file(DATE_08280000)
        self.assertEqual(actual, DATE_08310000)

        mock_check.assert_has_calls([
            mock.call(['rm', '-rf', EXTRACT_BOX_SCORES]),
            mock.call(['mkdir', EXTRACT_BOX_SCORES]),
            mock.call(['rm', '-rf', EXTRACT_GAME_LOGS]),
            mock.call(['mkdir', EXTRACT_GAME_LOGS]),
            mock.call(['rm', '-rf', EXTRACT_LEAGUES]),
            mock.call(['mkdir', EXTRACT_LEAGUES]),
        ])
        mock_listdir.assert_called_once_with(DOWNLOAD_BOX_SCORES)
        mock_open.assert_has_calls(suite.calls())
        suite.verify()

    @mock.patch('services.leaguefile.leaguefile.check_output')
    def test_find_download__done(self, mock_check):
        stdout = ('total 60224\n'
                  'drwxrwxr-x 4 user user      4096 Oct 26 00:00 news\n'
                  '-rw-rw-r-- 1 user user 345678901 Oct 26 06:04 '
                  'orange_and_blue_league_baseball.tar.gz')
        mock_check.return_value = {'ok': True, 'stdout': stdout}

        actual = find_download(DATE_10260000)
        expected = ('345678901', DATE_10260604, False)
        self.assertEqual(actual, expected)

        mock_check.assert_called_once_with(
            ['ls', '-l', DOWNLOAD_DIR], timeout=10)

    @mock.patch('services.leaguefile.leaguefile.check_output')
    def test_find_download__ongoing(self, mock_check):
        stdout = ('total 60224\n'
                  '-rw-rw-r-- 1 user user 100000 Oct 26 06:04 '
                  'orange_and_blue_league_baseball.tar.gz')
        mock_check.return_value = {'ok': True, 'stdout': stdout}

        actual = find_download(DATE_10260000)
        expected = ('100000', DATE_10260604, True)
        self.assertEqual(actual, expected)

        mock_check.assert_called_once_with(
            ['ls', '-l', DOWNLOAD_DIR], timeout=10)

    @mock.patch('services.leaguefile.leaguefile.check_output')
    def test_find_upload__done(self, mock_check):
        stdout = ('total 60224\n'
                  'drwxrwxr-x 4 user user      4096 Oct 26 00:00 news\n'
                  '-rw-rw-r-- 1 user user 345678901 Oct 26 09:04 {}'
                  ).format(FILE_NAME)
        mock_check.return_value = {'ok': True, 'stdout': stdout}

        actual = find_upload(DATE_10260000)
        expected = ('345678901', DATE_10260604, False)
        self.assertEqual(actual, expected)

        ls = 'ls -l /var/www/html/StatsLab/league_file'
        mock_check.assert_called_once_with(
            ['ssh', 'brunnerj@' + SERVER, ls], timeout=10)

    @mock.patch('services.leaguefile.leaguefile.check_output')
    def test_find_upload__ongoing(self, mock_check):
        stdout = (
            'total 321012\n'
            '-rwxrwxrwx 1 user user       421 Aug 19 13:48 index.html\n'
            '-rwxrwxrwx 1 user user 345678901 Oct 24 12:00 {}\n'
            '-rwxrwxrwx 1 user user 100000 Oct 26 09:04 {}.filepart').format(
                FILE_NAME, FILE_NAME)
        mock_check.return_value = {'ok': True, 'stdout': stdout}

        actual = find_upload(DATE_10260000)
        expected = ('100000', DATE_10260604, True)
        self.assertEqual(actual, expected)

        ls = 'ls -l /var/www/html/StatsLab/league_file'
        mock_check.assert_called_once_with(
            ['ssh', 'brunnerj@' + SERVER, ls], timeout=10)


if __name__ == '__main__':
    unittest.main()
