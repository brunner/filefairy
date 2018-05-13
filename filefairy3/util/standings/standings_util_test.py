#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/util/standings', '', _path))
from util.standings.standings_util import elimination_number  # noqa
from util.standings.standings_util import games_behind  # noqa
from util.standings.standings_util import sort  # noqa


class StandingsUtilTest(unittest.TestCase):
    def test_games_behind(self):
        self.assertEqual(games_behind('0-0', '0-0'), 0.0)
        self.assertEqual(games_behind('1-0', '1-0'), 0.0)
        self.assertEqual(games_behind('1-0', '0-0'), -0.5)
        self.assertEqual(games_behind('0-0', '1-0'), 0.5)
        self.assertEqual(games_behind('2-0', '0-0'), -1.0)
        self.assertEqual(games_behind('0-0', '2-0'), 1.0)
        self.assertEqual(games_behind('1-0', '0-1'), -1.0)
        self.assertEqual(games_behind('0-1', '1-0'), 1.0)
        self.assertEqual(games_behind('6-1', '3-3'), -2.5)
        self.assertEqual(games_behind('3-3', '6-1'), 2.5)

    def test_elimination_number(self):
        self.assertEqual(elimination_number('0-0', '0-0'), 163)
        self.assertEqual(elimination_number('1-0', '1-0'), 162)
        self.assertEqual(elimination_number('1-0', '0-0'), 163)
        self.assertEqual(elimination_number('0-0', '1-0'), 162)
        self.assertEqual(elimination_number('2-0', '0-0'), 163)
        self.assertEqual(elimination_number('0-0', '2-0'), 161)
        self.assertEqual(elimination_number('1-0', '0-1'), 163)
        self.assertEqual(elimination_number('0-1', '1-0'), 161)
        self.assertEqual(elimination_number('6-1', '3-3'), 159)
        self.assertEqual(elimination_number('3-3', '6-1'), 154)

    def test_sort__with_different(self):
        group = [('31', '0-2'), ('33', '2-0'), ('32', '1-1')]
        actual = sort(group)
        expected = [('33', '2-0'), ('32', '1-1'), ('31', '0-2')]
        self.assertEqual(actual, expected)

    def test_sort__with_same(self):
        group = [('31', '0-0'), ('33', '0-0'), ('32', '0-0')]
        actual = sort(group)
        expected = [('31', '0-0'), ('32', '0-0'), ('33', '0-0')]
        self.assertEqual(actual, expected)

    def test_sort__with_uneven(self):
        group = [('31', '3-2'), ('33', '4-0'), ('32', '2-1')]
        actual = sort(group)
        expected = [('33', '4-0'), ('32', '2-1'), ('31', '3-2')]
        self.assertEqual(actual, expected)

    def test_sort__with_zeroes(self):
        group = [('31', '3-0'), ('33', '0-3'), ('32', '4-0'), ('34', '0-4')]
        actual = sort(group)
        expected = [('32', '4-0'), ('31', '3-0'), ('33', '0-3'), ('34', '0-4')]
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
