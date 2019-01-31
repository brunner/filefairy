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
from common.test.test import RMock  # noqa
from common.test.test import Suite  # noqa
from common.test.test import WMock  # noqa
from common.test.test import get_testdata  # noqa
from services.leaguefile.leaguefile import download_file  # noqa
from services.leaguefile.leaguefile import extract_file  # noqa

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

FILE_HOST = 'https://statsplus.net/oblootp/files/'
ISO = 'iso-8859-1'

PLAYERS = [
    'P10', 'P1401', 'P1407', 'P1473', 'P18826', 'P20199', 'P20225', 'P206',
    'P23261', 'P23692', 'P23933', 'P24210', 'P25154', 'P25200', 'P26347',
    'P26604', 'P26879', 'P27015', 'P27200', 'P27218', 'P27521', 'P27957',
    'P29637', 'P29705', 'P29724', 'P29736', 'P29739', 'P30248', 'P30490',
    'P30918', 'P31993', 'P32323', 'P33166', 'P33611', 'P33777', 'P33949',
    'P33952', 'P34118', 'P34338', 'P35840', 'P35889', 'P36064', 'P36477',
    'P37214', 'P37330', 'P38782', 'P38843', 'P38870', 'P38917', 'P38928',
    'P39655', 'P39926', 'P42310', 'P44974', 'P49108', 'P49545', 'P50287',
    'P52197', 'P52484', 'P53121', 'P53305', 'P53414', 'P53701', 'P53711',
    'P53987', 'P54515', 'P54894', 'P55084', 'P55093', 'P55104', 'P55237',
    'P55254', 'P55336', 'P59192', 'P61570'
]

TESTDATA = get_testdata()


class LeaguefileTest(unittest.TestCase):
    @mock.patch('services.leaguefile.leaguefile.chdir')
    @mock.patch('services.leaguefile.leaguefile.check_output')
    def test_download_file__ok(self, mock_check, mock_chdir):
        url = FILE_HOST + 'orange%20and%20blue%20league.zip'
        expected = {'ok': True}
        mock_check.return_value = expected

        actual = download_file(url)
        self.assertEqual(actual, expected)

        filename = 'orange_and_blue_league.zip'
        mock_check.assert_has_calls([
            mock.call(['rm', '-rf', DOWNLOAD_DIR]),
            mock.call(['mkdir', DOWNLOAD_DIR]),
            mock.call(['wget', url, '-O', filename], timeout=4800),
            mock.call(['unzip', filename]),
        ])
        mock_chdir.assert_called_once_with(DOWNLOAD_DIR)

    @mock.patch('services.leaguefile.leaguefile.chdir')
    @mock.patch('services.leaguefile.leaguefile.check_output')
    def test_download_file__timeout(self, mock_check, mock_chdir):
        url = FILE_HOST + 'orange%20and%20blue%20league.zip'
        e = 'Command \'wget {}\' timed out after {} seconds'.format(url, 4800)
        expected = {'ok': False, 'stdout': e, 'stderr': e}
        mock_check.return_value = expected

        url = FILE_HOST + 'orange%20and%20blue%20league%20baseball.zip'
        actual = download_file(url)
        self.assertEqual(actual, expected)

        filename = 'orange_and_blue_league_baseball.zip'
        mock_check.assert_has_calls([
            mock.call(['rm', '-rf', DOWNLOAD_DIR]),
            mock.call(['mkdir', DOWNLOAD_DIR]),
            mock.call(['wget', url, '-O', filename], timeout=4800),
        ])
        mock_chdir.assert_called_once_with(DOWNLOAD_DIR)

    @mock.patch('services.leaguefile.leaguefile.put_players')
    @mock.patch('services.leaguefile.leaguefile.open', create=True)
    @mock.patch('services.leaguefile.leaguefile.os.listdir')
    @mock.patch('services.leaguefile.leaguefile.os.path.isfile')
    @mock.patch('services.leaguefile.leaguefile.check_output')
    def test_extract_file(self, mock_check, mock_isfile, mock_listdir,
                          mock_open, mock_put):
        mock_isfile.return_value = True
        mock_listdir.return_value = [
            'game_box_2449.html', 'game_box_2469.html', 'game_box_2476.html'
        ]
        suite = Suite(
            RMock(DOWNLOAD_BOX_SCORES, 'game_box_2449.html', TESTDATA),
            RMock(DOWNLOAD_LEAGUES, 'log_2449.txt', TESTDATA),
            WMock(EXTRACT_BOX_SCORES, 'game_box_2449.html', TESTDATA),
            WMock(EXTRACT_GAME_LOGS, 'log_2449.txt', TESTDATA),
            RMock(DOWNLOAD_BOX_SCORES, 'game_box_2469.html', TESTDATA),
            RMock(DOWNLOAD_LEAGUES, 'log_2469.txt', TESTDATA),
            WMock(EXTRACT_BOX_SCORES, 'game_box_2469.html', TESTDATA),
            WMock(EXTRACT_GAME_LOGS, 'log_2469.txt', TESTDATA),
            RMock(DOWNLOAD_BOX_SCORES, 'game_box_2476.html', TESTDATA),
            RMock(DOWNLOAD_LEAGUES, 'log_2476.txt', TESTDATA),
            WMock(EXTRACT_BOX_SCORES, 'game_box_2476.html', TESTDATA),
            WMock(EXTRACT_GAME_LOGS, 'log_2476.txt', TESTDATA),
            RMock(DOWNLOAD_LEAGUES, 'league_100_injuries.txt', TESTDATA),
            WMock(EXTRACT_LEAGUES, 'injuries.json', TESTDATA),
            RMock(DOWNLOAD_LEAGUES, 'league_100_news.txt', TESTDATA),
            WMock(EXTRACT_LEAGUES, 'news.json', TESTDATA),
            RMock(DOWNLOAD_LEAGUES, 'league_100_transactions.txt', TESTDATA),
            WMock(EXTRACT_LEAGUES, 'transactions.json', TESTDATA),
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
        mock_put.assert_called_once_with(PLAYERS)
        suite.verify()


if __name__ == '__main__':
    unittest.main()
