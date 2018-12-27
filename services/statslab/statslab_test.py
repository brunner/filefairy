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

TESTDATA = get_testdata(os.path.join(_path, 'testdata'))


class StatslabTest(unittest.TestCase):
    @mock.patch('services.statslab.statslab.open', create=True)
    @mock.patch('services.statslab.statslab.os.path.isfile')
    def test_parse_score(self, mock_isfile, mock_open):
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

        inputs = [
            (DATE_08280000, '2449'),
            (DATE_08290000, '2469'),
            (DATE_08300000, '2476'),
        ]

        for date, num in inputs:
            actual = parse_score(encode_datetime(date), num, False)
            self.assertTrue(actual)

        mock_open.assert_has_calls(suite.calls())
        suite.verify()


if __name__ == '__main__':
    unittest.main()
