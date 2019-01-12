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
from common.test.test import RMock  # noqa
from common.test.test import Suite  # noqa
from common.test.test import WMock  # noqa
from common.test.test import get_testdata  # noqa
from services.statslab.statslab import parse_score  # noqa

DATE_08280000 = datetime_datetime_pst(2024, 8, 28)
DATE_08290000 = datetime_datetime_pst(2024, 8, 29)
DATE_08300000 = datetime_datetime_pst(2024, 8, 30)

EXTRACT_DIR = re.sub(r'/services/statslab', '/resource/extract', _path)
EXTRACT_BOX_SCORES = os.path.join(EXTRACT_DIR, 'box_scores')

GAMES_DIR = re.sub(r'/services/statslab', '/resource/games', _path)

STATSPLUS_LINK = 'https://statsplus.net/oblootp/reports/news/html'
STATSPLUS_BOX_SCORES = os.path.join(STATSPLUS_LINK, 'box_scores')

TESTDATA = get_testdata()


def _extract_box_score(num):
    return os.path.join(EXTRACT_BOX_SCORES, 'game_box_{}.html'.format(num))


def _statsplus_box_score(num):
    return os.path.join(STATSPLUS_BOX_SCORES, 'game_box_{}.html'.format(num))


class StatslabTest(unittest.TestCase):
    @mock.patch('services.statslab.statslab.open', create=True)
    @mock.patch('services.statslab.statslab.get')
    @mock.patch('services.statslab.statslab.os.path.isfile')
    def test_parse_score__file(self, mock_isfile, mock_get, mock_open):
        mock_isfile.return_value = True
        suite = Suite(
            RMock(EXTRACT_BOX_SCORES, 'game_box_2449.html', TESTDATA),
            WMock(GAMES_DIR, '2449.json', TESTDATA),
            RMock(EXTRACT_BOX_SCORES, 'game_box_2469.html', TESTDATA),
            WMock(GAMES_DIR, '2469.json', TESTDATA),
            RMock(EXTRACT_BOX_SCORES, 'game_box_2476.html', TESTDATA),
            WMock(GAMES_DIR, '2476.json', TESTDATA),
        )
        mock_open.side_effect = suite.values()

        for num in ['2449', '2469', '2476']:
            in_ = _extract_box_score(num)
            out = os.path.join(GAMES_DIR, num + '.json')
            actual = parse_score(in_, out, None)
            self.assertTrue(actual)

        mock_get.assert_not_called()
        mock_open.assert_has_calls(suite.calls())
        suite.verify()

    @mock.patch('services.statslab.statslab.open', create=True)
    @mock.patch('services.statslab.statslab.get')
    @mock.patch('services.statslab.statslab.os.path.isfile')
    def test_parse_score__link(self, mock_isfile, mock_get, mock_open):
        mock_isfile.return_value = False
        mock_get.side_effect = [
            TESTDATA['game_box_2449.html'],
            TESTDATA['game_box_2469.html'],
            TESTDATA['game_box_2476.html'],
        ]
        suite = Suite(
            WMock(GAMES_DIR, '2449.json', TESTDATA),
            WMock(GAMES_DIR, '2469.json', TESTDATA),
            WMock(GAMES_DIR, '2476.json', TESTDATA),
        )
        mock_open.side_effect = suite.values()

        inputs = [
            ('2449', DATE_08280000),
            ('2469', DATE_08290000),
            ('2476', DATE_08300000),
        ]

        for num, date in inputs:
            in_ = _statsplus_box_score(num)
            out = os.path.join(GAMES_DIR, num + '.json')
            actual = parse_score(in_, out, encode_datetime(date))
            self.assertTrue(actual)

        mock_get.assert_has_calls([
            mock.call(_statsplus_box_score('2449')),
            mock.call(_statsplus_box_score('2469')),
            mock.call(_statsplus_box_score('2476')),
        ])
        mock_open.assert_has_calls(suite.calls())
        suite.verify()


if __name__ == '__main__':
    unittest.main()
