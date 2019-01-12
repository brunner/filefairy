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
from services.scoreboard.scoreboard import line_score  # noqa

TESTDATA = get_testdata()


class ScoreboardTest(unittest.TestCase):
    def test_line_score(self):
        for num in ['2449', '2469', '2476']:
            actual = line_score(json.loads(TESTDATA[num + '.json']))
            expected = json.loads(TESTDATA['table_' + num + '.json'])
            self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
