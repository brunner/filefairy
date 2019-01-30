#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for statslab.py."""

import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/services/statslab', '', _path))

from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.datetime_.datetime_ import encode_datetime  # noqa
from common.service.service import mock_service_for_test  # noqa
from common.service.service import reload_service_for_test  # noqa
from common.test.test import RMock  # noqa
from common.test.test import Suite  # noqa
from common.test.test import WMock  # noqa
from common.test.test import get_testdata  # noqa
from services.statslab.statslab import parse_player  # noqa
from services.statslab.statslab import parse_game  # noqa

DATE_03100000 = datetime_datetime_pst(2025, 3, 10)
DATE_03110000 = datetime_datetime_pst(2025, 3, 11)
DATE_03130000 = datetime_datetime_pst(2025, 3, 13)
DATE_03160000 = datetime_datetime_pst(2025, 3, 16)

EXTRACT_DIR = re.sub(r'/services/statslab', '/resource/extract', _path)
EXTRACT_BOX_SCORES = os.path.join(EXTRACT_DIR, 'box_scores')
EXTRACT_LEAGUES = os.path.join(EXTRACT_DIR, 'leagues')

GAMES_DIR = re.sub(r'/services/statslab', '/resource/games', _path)

PLAYERS = [
    [
        'P1150', 'P12', 'P21314', 'P22458', 'P23026', 'P23553', 'P24176',
        'P24184', 'P25154', 'P25189', 'P25233', 'P26617', 'P26980', 'P29705',
        'P29741', 'P36248', 'P37050', 'P38655', 'P38811', 'P40726', 'P41755',
        'P50258', 'P52260', 'P53426', 'P53750', 'P55021', 'P55249', 'P57'
    ],
    [
        'P1473', 'P22819', 'P23688', 'P24548', 'P26087', 'P26672', 'P26879',
        'P27194', 'P28185', 'P28401', 'P28785', 'P33236', 'P33562', 'P34705',
        'P37037', 'P39432', 'P41310', 'P49103', 'P49738', 'P50298', 'P50308',
        'P51521', 'P53209', 'P53282', 'P53328'
    ],
    [
        'P1392', 'P1614', 'P20230', 'P20296', 'P23264', 'P23816', 'P23857',
        'P25981', 'P27803', 'P28636', 'P30055', 'P30088', 'P30138', 'P33764',
        'P34175', 'P36272', 'P38844', 'P42045', 'P46441', 'P48230', 'P48257',
        'P50249', 'P50304', 'P51461', 'P53046', 'P54518', 'P91'
    ],
    [
        'P22145', 'P22503', 'P22635', 'P23241', 'P23269', 'P25202', 'P25310',
        'P25651', 'P29670', 'P29755', 'P30238', 'P30804', 'P30965', 'P38657',
        'P40187', 'P50004', 'P50900', 'P53050', 'P53129', 'P53197', 'P54893',
        'P55542', 'P55778', 'P57150'
    ],
    [
        'P1604', 'P22470', 'P23261', 'P23619', 'P25140', 'P30583', 'P33100',
        'P35105', 'P35481', 'P39616', 'P39880', 'P40738', 'P44320', 'P50013',
        'P50114', 'P50254', 'P50265', 'P50269', 'P53182', 'P53626', 'P53645',
        'P53825', 'P53987', 'P55096', 'P55237', 'P55336'
    ],
]

STATSPLUS_LINK = 'https://statsplus.net/oblootp/reports/news/html'
STATSPLUS_BOX_SCORES = os.path.join(STATSPLUS_LINK, 'box_scores')
STATSPLUS_GAME_LOGS = os.path.join(STATSPLUS_LINK, 'game_logs')
STATSPLUS_PLAYERS = os.path.join(STATSPLUS_LINK, 'players')

TESTDATA = get_testdata()

COLORS_32 = ('grey', '#ab1234', '#0b2c5a', 'block')
COLORS_39 = ('purple', '#000000', '#ffffff', 'basic')
COLORS_41 = ('white', '#000000', '#27aab8', 'basic')
COLORS_42 = ('grey', '#141929', '#aa563e', 'block')
COLORS_45 = ('white', '#233972', 'none', 'basic')
COLORS_49 = ('blue', '#a4a1a1', '#c45d3b', 'basic')
COLORS_51 = ('white', '#d11043', 'none', 'rounded')
COLORS_52 = ('white', '#000000', '#fcc72d', 'pirates')
COLORS_53 = ('yellow', '#512c1b', 'none', 'serif')
COLORS_58 = ('white', '#124886', '#ce103b', 'pointed')


def _extract_box_score(num):
    return os.path.join(EXTRACT_BOX_SCORES, 'game_box_{}.html'.format(num))


def _extract_log(num):
    return os.path.join(EXTRACT_LEAGUES, 'log_{}.txt'.format(num))


def _games_out(num):
    return os.path.join(GAMES_DIR, '{}.json'.format(num))


def _statsplus_box_score(num):
    return os.path.join(STATSPLUS_BOX_SCORES, 'game_box_{}.html'.format(num))


def _statsplus_log(num):
    return os.path.join(STATSPLUS_GAME_LOGS, 'log_{}.html'.format(num))


def _statsplus_player_page(num):
    return os.path.join(STATSPLUS_PLAYERS, 'player_{}.html'.format(num))


class StatslabTest(unittest.TestCase):
    @mock.patch('services.statslab.statslab.open', create=True)
    @mock.patch('services.statslab.statslab.get')
    @mock.patch('services.statslab.statslab.os.path.isfile')
    def test_parse_player(self, mock_isfile, mock_get, mock_open):
        mock_isfile.return_value = False
        mock_get.side_effect = [
            TESTDATA['player_24322.html'],
            TESTDATA['player_35903.html'],
            TESTDATA['player_54297.html'],
        ]

        inputs = [
            ('24322', 'T47 16 R R Jarid Joseph'),
            ('35903', 'T47 35 R R Jose Fernandez'),
            ('54297', 'T?? 56 R R Lineu Murraas'),
        ]

        for num, expected in inputs:
            link = _statsplus_player_page(num)
            actual = parse_player(link)
            self.assertEqual(actual, expected)

        mock_get.assert_has_calls([
            mock.call(_statsplus_player_page('24322')),
            mock.call(_statsplus_player_page('35903')),
            mock.call(_statsplus_player_page('54297')),
        ])
        mock_open.assert_not_called()

    @mock.patch('services.statslab.statslab.put_players')
    @mock.patch('services.statslab.statslab.open', create=True)
    @mock.patch('services.statslab.statslab.get')
    @mock.patch('services.statslab.statslab.os.path.isfile')
    def test_parse_game__file(self, mock_isfile, mock_get, mock_open,
                              mock_put):
        mock_isfile.return_value = True
        suite = Suite(
            RMock(EXTRACT_BOX_SCORES, 'game_box_23520.html', TESTDATA),
            RMock(EXTRACT_LEAGUES, 'log_23520.txt', TESTDATA),
            WMock(GAMES_DIR, '23520.json', TESTDATA),
            RMock(EXTRACT_BOX_SCORES, 'game_box_23766.html', TESTDATA),
            RMock(EXTRACT_LEAGUES, 'log_23766.txt', TESTDATA),
            WMock(GAMES_DIR, '23766.json', TESTDATA),
            RMock(EXTRACT_BOX_SCORES, 'game_box_23769.html', TESTDATA),
            RMock(EXTRACT_LEAGUES, 'log_23769.txt', TESTDATA),
            WMock(GAMES_DIR, '23769.json', TESTDATA),
            RMock(EXTRACT_BOX_SCORES, 'game_box_23775.html', TESTDATA),
            RMock(EXTRACT_LEAGUES, 'log_23775.txt', TESTDATA),
            WMock(GAMES_DIR, '23775.json', TESTDATA),
            RMock(EXTRACT_BOX_SCORES, 'game_box_23803.html', TESTDATA),
            RMock(EXTRACT_LEAGUES, 'log_23803.txt', TESTDATA),
            WMock(GAMES_DIR, '23803.json', TESTDATA),
        )
        mock_open.side_effect = suite.values()

        mock_jersey_colors = mock.Mock()
        mock_jersey_colors.side_effect = [
            COLORS_58, COLORS_42, COLORS_45, COLORS_32, COLORS_51, COLORS_39,
            COLORS_41, COLORS_49, COLORS_52, COLORS_53
        ]

        mock_service_for_test('uniforms', 'jersey_colors', mock_jersey_colors)
        reload_service_for_test('events')

        for num in ['23520', '23766', '23769', '23775', '23803']:
            box_in = _extract_box_score(num)
            log_in = _extract_log(num)
            out = _games_out(num)
            actual = parse_game(box_in, log_in, out, None)
            self.assertTrue(actual)

        mock_get.assert_not_called()
        mock_open.assert_has_calls(suite.calls())
        mock_put.assert_has_calls([mock.call(p) for p in PLAYERS])
        suite.verify()

    @mock.patch('services.statslab.statslab.put_players')
    @mock.patch('services.statslab.statslab.open', create=True)
    @mock.patch('services.statslab.statslab.get')
    @mock.patch('services.statslab.statslab.os.path.isfile')
    def test_parse_game__link(self, mock_isfile, mock_get, mock_open,
                              mock_put):
        mock_isfile.return_value = False
        mock_get.side_effect = [
            TESTDATA['game_box_23520.html'],
            TESTDATA['log_23520.html'],
            TESTDATA['game_box_23766.html'],
            TESTDATA['log_23766.html'],
            TESTDATA['game_box_23769.html'],
            TESTDATA['log_23769.html'],
            TESTDATA['game_box_23775.html'],
            TESTDATA['log_23775.html'],
            TESTDATA['game_box_23803.html'],
            TESTDATA['log_23803.html'],
        ]
        suite = Suite(
            WMock(GAMES_DIR, '23520.json', TESTDATA),
            WMock(GAMES_DIR, '23766.json', TESTDATA),
            WMock(GAMES_DIR, '23769.json', TESTDATA),
            WMock(GAMES_DIR, '23775.json', TESTDATA),
            WMock(GAMES_DIR, '23803.json', TESTDATA),
        )
        mock_open.side_effect = suite.values()

        mock_jersey_colors = mock.Mock()
        mock_jersey_colors.side_effect = [
            COLORS_58, COLORS_42, COLORS_45, COLORS_32, COLORS_51, COLORS_39,
            COLORS_41, COLORS_49, COLORS_52, COLORS_53
        ]

        mock_service_for_test('uniforms', 'jersey_colors', mock_jersey_colors)
        reload_service_for_test('events')

        inputs = [
            ('23520', DATE_03130000),
            ('23766', DATE_03100000),
            ('23769', DATE_03100000),
            ('23775', DATE_03110000),
            ('23803', DATE_03160000),
        ]

        for num, d in inputs:
            box_in = _statsplus_box_score(num)
            log_in = _statsplus_log(num)
            out = _games_out(num)
            date = encode_datetime(d)
            actual = parse_game(box_in, log_in, out, date)
            self.assertTrue(actual)

        mock_get.assert_has_calls([
            mock.call(_statsplus_box_score('23520')),
            mock.call(_statsplus_log('23520')),
            mock.call(_statsplus_box_score('23766')),
            mock.call(_statsplus_log('23766')),
            mock.call(_statsplus_box_score('23769')),
            mock.call(_statsplus_log('23769')),
            mock.call(_statsplus_box_score('23775')),
            mock.call(_statsplus_log('23775')),
            mock.call(_statsplus_box_score('23803')),
            mock.call(_statsplus_log('23803')),
        ])
        mock_open.assert_has_calls(suite.calls())
        mock_put.assert_has_calls([mock.call(p) for p in PLAYERS])
        suite.verify()


if __name__ == '__main__':
    unittest.main()
