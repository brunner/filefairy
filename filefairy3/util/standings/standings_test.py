#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/util/standings', '', _path))
from util.component.component import table  # noqa
from util.standings.standings import elimination_number  # noqa
from util.standings.standings import games_behind  # noqa
from util.standings.standings import sort  # noqa
from util.standings.standings import standings_table  # noqa
from util.team.team import logo_absolute  # noqa

COLS = [
    'class="position-relative text-truncate"', ' class="text-right w-55p"',
    ' class="text-right w-55p"'
]
RECORDS = [('31', '76-86'), ('32', '77-85'), ('33', '70-92'), ('34', '99-63'),
           ('35', '82-80'), ('36', '71-91'), ('37', '111-51'), ('38', '76-86'),
           ('39', '88-74'), ('40', '86-76'), ('41', '84-78'), ('42', '85-77'),
           ('43', '76-86'), ('44', '70-92'), ('45', '97-65'), ('46', '77-85'),
           ('47', '88-74'), ('48', '88-74'), ('49', '95-67'), ('50', '75-87'),
           ('51', '75-87'), ('52', '53-109'), ('53', '104-58'),
           ('54', '98-64'), ('55', '62-100'), ('56', '89-73'), ('57', '65-97'),
           ('58', '67-95'), ('59', '73-89'), ('60', '73-89')]


class StandingsTest(unittest.TestCase):
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

    def test_standings_table(self):
        actual = standings_table(RECORDS)
        expected = [
            table(
                hcols=COLS,
                bcols=COLS,
                head=['AL East', 'W', 'L'],
                body=[[logo_absolute('34', 'Boston', 'left'), '99', '63'], [
                    logo_absolute('48', 'New York', 'left'), '88', '74'
                ], [logo_absolute('59', 'Toronto', 'left'), '73', '89'],
                      [logo_absolute('33', 'Baltimore', 'left'), '70', '92'],
                      [logo_absolute('57', 'Tampa Bay', 'left'), '65', '97']]),
            table(
                hcols=COLS,
                bcols=COLS,
                head=['AL Central', 'W', 'L'],
                body=[[logo_absolute('47', 'Minnesota', 'left'), '88', '74'], [
                    logo_absolute('40', 'Detroit', 'left'), '86', '76'
                ], [logo_absolute('35', 'Chicago', 'left'), '82', '80'], [
                    logo_absolute('38', 'Cleveland', 'left'), '76', '86'
                ], [logo_absolute('43', 'Kansas City', 'left'), '76', '86']]),
            table(
                hcols=COLS,
                bcols=COLS,
                head=['AL West', 'W', 'L'],
                body=[[logo_absolute('54', 'Seattle', 'left'), '98', '64'], [
                    logo_absolute('42', 'Houston', 'left'), '85', '77'
                ], [logo_absolute('50', 'Oakland', 'left'), '75', '87'],
                      [logo_absolute('44', 'Los Angeles', 'left'), '70', '92'],
                      [logo_absolute('58', 'Texas', 'left'), '67', '95']]),
            table(
                hcols=COLS,
                bcols=COLS,
                head=['NL East', 'W', 'L'],
                body=[[logo_absolute('49', 'New York', 'left'), '95', '67'], [
                    logo_absolute('41', 'Miami', 'left'), '84', '78'
                ], [logo_absolute('32', 'Atlanta', 'left'), '77', '85'], [
                    logo_absolute('51', 'Philadelphia', 'left'), '75', '87'
                ], [logo_absolute('60', 'Washington', 'left'), '73', '89']]),
            table(
                hcols=COLS,
                bcols=COLS,
                head=['NL Central', 'W', 'L'],
                body=[[logo_absolute('37', 'Cincinnati', 'left'), '111', '51'],
                      [logo_absolute('56', 'St. Louis', 'left'), '89', '73'], [
                          logo_absolute('46', 'Milwaukee', 'left'), '77', '85'
                      ], [logo_absolute('36', 'Chicago', 'left'), '71', '91'],
                      [logo_absolute('52', 'Pittsburgh', 'left'), '53',
                       '109']]),
            table(
                hcols=COLS,
                bcols=COLS,
                head=['NL West', 'W', 'L'],
                body=[[logo_absolute('53', 'San Diego', 'left'), '104', '58'],
                      [logo_absolute('45', 'Los Angeles', 'left'), '97', '65'],
                      [logo_absolute('39', 'Colorado', 'left'), '88', '74'],
                      [logo_absolute('31', 'Arizona', 'left'), '76', '86'], [
                          logo_absolute('55', 'San Francisco', 'left'), '62',
                          '100'
                      ]])
        ]
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
