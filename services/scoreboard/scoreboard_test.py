#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for scoreboard.py."""

import json
import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/services/scoreboard', '', _path))

from common.test.test import get_testdata  # noqa
from services.scoreboard.scoreboard import line_score_body  # noqa
from services.scoreboard.scoreboard import line_score_foot  # noqa
from services.scoreboard.scoreboard import line_score_head  # noqa
from services.scoreboard.scoreboard import pending_score_body  # noqa

TESTDATA = get_testdata()


class ScoreboardTest(unittest.TestCase):
    def test_line_score_body(self):
        for num in ['2449', '2469', '2476']:
            data = json.loads(TESTDATA['game_box_' + num + '.json'])
            actual = line_score_body(data)
            expected = json.loads(TESTDATA['line_score_body_' + num + '.json'])
            self.assertEqual(actual, expected)

    def test_line_score_foot(self):
        for num in ['2449', '2469', '2476']:
            data = json.loads(TESTDATA['game_box_' + num + '.json'])
            actual = line_score_foot(data)
            expected = json.loads(TESTDATA['line_score_foot_' + num + '.json'])
            self.assertEqual(actual, expected)

    def test_line_score_head(self):
        for num in ['2449', '2469', '2476']:
            data = json.loads(TESTDATA['game_box_' + num + '.json'])
            actual = line_score_head(data['date'])
            expected = json.loads(TESTDATA['line_score_head_' + num + '.json'])
            self.assertEqual(actual, expected)

    def test_pending_score_body(self):
        actual = pending_score_body(['T31 4, TLA 2', 'TNY 5, TLA 3'])
        expected = json.loads(TESTDATA['pending_score_body_la.json'])
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
