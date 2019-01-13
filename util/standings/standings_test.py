#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/util/standings', '', _path))
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import table  # noqa
from util.standings.standings import elimination_number  # noqa
from util.standings.standings import games_behind  # noqa
from util.standings.standings import sort  # noqa
from util.standings.standings import standings_table  # noqa
from util.team.team import logo_absolute  # noqa


def _fake_logo(*args, **kwargs):
    teamid, text, side = args
    return teamid


def _row(teamid, w, l, gb, mn):
    return [
        cell(content=_fake_logo(teamid, '', '')),
        cell(content=w),
        cell(content=l),
        cell(content=gb),
        cell(content=mn)
    ]


def _table(title, body):
    cols = [
        col(clazz='position-relative text-truncate'),
        col(clazz='text-right w-55p'),
        col(clazz='text-right w-55p'),
        col(clazz='text-right w-75p'),
        col(clazz='text-right w-55p')
    ]
    return table(
        hcols=cols,
        bcols=cols,
        head=[[
            cell(content=title),
            cell(content='W'),
            cell(content='L'),
            cell(content='GB'),
            cell(content='M#')
        ]],
        body=body)


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

    maxDiff = None

    @mock.patch('util.standings.standings.logo_absolute')
    def test_standings_table__with_empty(self, mock_logo):
        mock_logo.side_effect = _fake_logo

        actual = standings_table({})
        expected = [
            _table('AL East', [
                _row('33', '0', '0', '-', '163'),
                _row('34', '0', '0', '-', '163'),
                _row('48', '0', '0', '-', '163'),
                _row('57', '0', '0', '-', '163'),
                _row('59', '0', '0', '-', '163')
            ]),
            _table('AL Central', [
                _row('35', '0', '0', '-', '163'),
                _row('38', '0', '0', '-', '163'),
                _row('40', '0', '0', '-', '163'),
                _row('43', '0', '0', '-', '163'),
                _row('47', '0', '0', '-', '163')
            ]),
            _table('AL West', [
                _row('42', '0', '0', '-', '163'),
                _row('44', '0', '0', '-', '163'),
                _row('50', '0', '0', '-', '163'),
                _row('54', '0', '0', '-', '163'),
                _row('58', '0', '0', '-', '163')
            ]),
            _table('AL Wild Card', [
                _row('33', '0', '0', '-', '163'),
                _row('34', '0', '0', '-', '163'),
                _row('35', '0', '0', '-', '163'),
                _row('38', '0', '0', '-', '163'),
                _row('40', '0', '0', '-', '163'),
                _row('42', '0', '0', '-', '163'),
                _row('43', '0', '0', '-', '163'),
                _row('44', '0', '0', '-', '163')
            ]),
            _table('NL East', [
                _row('32', '0', '0', '-', '163'),
                _row('41', '0', '0', '-', '163'),
                _row('49', '0', '0', '-', '163'),
                _row('51', '0', '0', '-', '163'),
                _row('60', '0', '0', '-', '163')
            ]),
            _table('NL Central', [
                _row('36', '0', '0', '-', '163'),
                _row('37', '0', '0', '-', '163'),
                _row('46', '0', '0', '-', '163'),
                _row('52', '0', '0', '-', '163'),
                _row('56', '0', '0', '-', '163')
            ]),
            _table('NL West', [
                _row('31', '0', '0', '-', '163'),
                _row('39', '0', '0', '-', '163'),
                _row('45', '0', '0', '-', '163'),
                _row('53', '0', '0', '-', '163'),
                _row('55', '0', '0', '-', '163')
            ]),
            _table('NL Wild Card', [
                _row('31', '0', '0', '-', '163'),
                _row('32', '0', '0', '-', '163'),
                _row('36', '0', '0', '-', '163'),
                _row('37', '0', '0', '-', '163'),
                _row('39', '0', '0', '-', '163'),
                _row('41', '0', '0', '-', '163'),
                _row('45', '0', '0', '-', '163'),
                _row('46', '0', '0', '-', '163')
            ])
        ]
        self.assertEqual(actual, expected)

    @mock.patch('util.standings.standings.logo_absolute')
    def test_standings_table__with_final(self, mock_logo):
        mock_logo.side_effect = _fake_logo

        records = {
            '31': '76-86',
            '32': '77-85',
            '33': '70-92',
            '34': '99-63',
            '35': '82-80',
            '36': '71-91',
            '37': '111-51',
            '38': '76-86',
            '39': '88-74',
            '40': '86-76',
            '41': '84-78',
            '42': '85-77',
            '43': '76-86',
            '44': '70-92',
            '45': '97-65',
            '46': '77-85',
            '47': '88-74',
            '48': '88-74',
            '49': '95-67',
            '50': '75-87',
            '51': '75-87',
            '52': '53-109',
            '53': '104-58',
            '54': '98-64',
            '55': '62-100',
            '56': '89-73',
            '57': '65-97',
            '58': '67-95',
            '59': '73-89',
            '60': '73-89'
        }
        actual = standings_table(records)
        expected = [
            _table('AL East', [
                _row('34', '99', '63', '-', 'X'),
                _row('48', '88', '74', '11.0', ''),
                _row('59', '73', '89', '26.0', ''),
                _row('33', '70', '92', '29.0', ''),
                _row('57', '65', '97', '34.0', '')
            ]),
            _table('AL Central', [
                _row('47', '88', '74', '-', 'X'),
                _row('40', '86', '76', '2.0', ''),
                _row('35', '82', '80', '6.0', ''),
                _row('38', '76', '86', '12.0', ''),
                _row('43', '76', '86', '12.0', '')
            ]),
            _table('AL West', [
                _row('54', '98', '64', '-', 'X'),
                _row('42', '85', '77', '13.0', ''),
                _row('50', '75', '87', '23.0', ''),
                _row('44', '70', '92', '28.0', ''),
                _row('58', '67', '95', '31.0', '')
            ]),
            _table('AL Wild Card', [
                _row('48', '88', '74', '+2.0', 'X'),
                _row('40', '86', '76', '-', 'X'),
                _row('42', '85', '77', '1.0', ''),
                _row('35', '82', '80', '4.0', '')
            ]),
            _table('NL East', [
                _row('49', '95', '67', '-', 'X'),
                _row('41', '84', '78', '11.0', ''),
                _row('32', '77', '85', '18.0', ''),
                _row('51', '75', '87', '20.0', ''),
                _row('60', '73', '89', '22.0', '')
            ]),
            _table('NL Central', [
                _row('37', '111', '51', '-', 'X'),
                _row('56', '89', '73', '22.0', ''),
                _row('46', '77', '85', '34.0', ''),
                _row('36', '71', '91', '40.0', ''),
                _row('52', '53', '109', '58.0', '')
            ]),
            _table('NL West', [
                _row('53', '104', '58', '-', 'X'),
                _row('45', '97', '65', '7.0', ''),
                _row('39', '88', '74', '16.0', ''),
                _row('31', '76', '86', '28.0', ''),
                _row('55', '62', '100', '42.0', '')
            ]),
            _table('NL Wild Card', [
                _row('45', '97', '65', '+8.0', 'X'),
                _row('56', '89', '73', '-', 'X'),
                _row('39', '88', '74', '1.0', ''),
                _row('41', '84', '78', '5.0', '')
            ])
        ]
        self.assertEqual(actual, expected)

    @mock.patch('util.standings.standings.logo_absolute')
    def test_standings_table__with_irregular(self, mock_logo):
        mock_logo.side_effect = _fake_logo

        records = {
            '31': '24-18',
            '32': '25-12',
            '33': '26-15',
            '34': '23-13',
            '35': '24-16',
            '36': '23-18',
            '37': '22-17',
            '38': '23-15',
            '39': '23-15',
            '40': '22-17',
            '41': '21-17',
            '42': '25-13',
            '43': '13-26',
            '44': '21-18',
            '45': '22-16',
            '46': '20-20',
            '47': '10-32',
            '48': '17-20',
            '49': '18-19',
            '50': '19-19',
            '51': '17-22',
            '52': '16-19',
            '53': '20-23',
            '54': '17-20',
            '55': '16-26',
            '56': '13-25',
            '57': '16-21',
            '58': '14-24',
            '59': '13-26',
            '60': '14-26'
        }
        actual = standings_table(records)
        expected = [
            _table('AL East', [
                _row('33', '26', '15', '-', '124'),
                _row('34', '23', '13', '0.5', ''),
                _row('48', '17', '20', '7.0', ''),
                _row('57', '16', '21', '8.0', ''),
                _row('59', '13', '26', '12.0', '')
            ]),
            _table('AL Central', [
                _row('38', '23', '15', '-', '124'),
                _row('35', '24', '16', '-', '124'),
                _row('40', '22', '17', '1.5', ''),
                _row('43', '13', '26', '10.5', ''),
                _row('47', '10', '32', '15.0', '')
            ]),
            _table('AL West', [
                _row('42', '25', '13', '-', '120'),
                _row('44', '21', '18', '4.5', ''),
                _row('50', '19', '19', '6.0', ''),
                _row('54', '17', '20', '7.5', ''),
                _row('58', '14', '24', '11.0', '')
            ]),
            _table('AL Wild Card', [
                _row('34', '23', '13', '+1.0', '123'),
                _row('38', '23', '15', '-', '123'),
                _row('35', '24', '16', '-', '122'),
                _row('40', '22', '17', '1.5', ''),
                _row('44', '21', '18', '2.5', ''),
                _row('50', '19', '19', '4.0', ''),
                _row('48', '17', '20', '5.5', ''),
                _row('54', '17', '20', '5.5', ''),
            ]),
            _table('NL East', [
                _row('32', '25', '12', '-', '121'),
                _row('41', '21', '17', '4.5', ''),
                _row('49', '18', '19', '7.0', ''),
                _row('51', '17', '22', '9.0', ''),
                _row('60', '14', '26', '12.5', '')
            ]),
            _table('NL Central', [
                _row('37', '22', '17', '-', '123'),
                _row('36', '23', '18', '-', '123'),
                _row('46', '20', '20', '2.5', ''),
                _row('52', '16', '19', '4.0', ''),
                _row('56', '13', '25', '8.5', '')
            ]),
            _table('NL West', [
                _row('39', '23', '15', '-', '124'),
                _row('45', '22', '16', '1.0', ''),
                _row('31', '24', '18', '1.0', ''),
                _row('53', '20', '23', '5.5', ''),
                _row('55', '16', '26', '9.0', '')
            ]),
            _table('NL Wild Card', [
                _row('45', '22', '16', '-', '124'),
                _row('31', '24', '18', '-', '122'),
                _row('37', '22', '17', '0.5', ''),
                _row('36', '23', '18', '0.5', ''),
                _row('41', '21', '17', '1.0', ''),
                _row('46', '20', '20', '3.0', ''),
                _row('49', '18', '19', '3.5', ''),
                _row('53', '20', '23', '4.5', ''),
            ])
        ]
        self.assertEqual(actual, expected)

    @mock.patch('util.standings.standings.logo_absolute')
    def test_standings_table__with_midseason(self, mock_logo):
        mock_logo.side_effect = _fake_logo

        records = {
            '31': '50-62',
            '32': '56-55',
            '33': '57-54',
            '34': '55-55',
            '35': '57-54',
            '36': '57-53',
            '37': '77-34',
            '38': '59-53',
            '39': '69-41',
            '40': '53-58',
            '41': '36-75',
            '42': '54-57',
            '43': '54-59',
            '44': '53-58',
            '45': '63-46',
            '46': '52-59',
            '47': '66-45',
            '48': '50-60',
            '49': '64-47',
            '50': '46-54',
            '51': '57-54',
            '52': '34-78',
            '53': '67-46',
            '54': '65-45',
            '55': '48-63',
            '56': '59-52',
            '57': '57-54',
            '58': '37-74',
            '59': '64-47',
            '60': '49-63'
        }
        actual = standings_table(records)
        expected = [
            _table('AL East', [
                _row('59', '64', '47', '-', '45'),
                _row('33', '57', '54', '7.0', ''),
                _row('57', '57', '54', '7.0', ''),
                _row('34', '55', '55', '8.5', ''),
                _row('48', '50', '60', '13.5', '')
            ]),
            _table('AL Central', [
                _row('47', '66', '45', '-', '44'),
                _row('38', '59', '53', '7.5', ''),
                _row('35', '57', '54', '9.0', ''),
                _row('43', '54', '59', '13.0', ''),
                _row('40', '53', '58', '13.0', '')
            ]),
            _table('AL West', [
                _row('54', '65', '45', '-', '44'),
                _row('42', '54', '57', '11.5', ''),
                _row('44', '53', '58', '12.5', ''),
                _row('50', '46', '54', '14.0', ''),
                _row('58', '37', '74', '28.5', '')
            ]),
            _table('AL Wild Card', [
                _row('38', '59', '53', '+1.5', '50'),
                _row('33', '57', '54', '-', '52'),
                _row('35', '57', '54', '-', '52'),
                _row('57', '57', '54', '-', '52'),
                _row('34', '55', '55', '1.5', ''),
                _row('42', '54', '57', '3.0', ''),
                _row('43', '54', '59', '4.0', ''),
                _row('40', '53', '58', '4.0', '')
            ]),
            _table('NL East', [
                _row('49', '64', '47', '-', '45'),
                _row('51', '57', '54', '7.0', ''),
                _row('32', '56', '55', '8.0', ''),
                _row('60', '49', '63', '15.5', ''),
                _row('41', '36', '75', '28.0', '')
            ]),
            _table('NL Central', [
                _row('37', '77', '34', '-', '34'),
                _row('56', '59', '52', '18.0', ''),
                _row('36', '57', '53', '19.5', ''),
                _row('46', '52', '59', '25.0', ''),
                _row('52', '34', '78', '43.5', '')
            ]),
            _table('NL West', [
                _row('39', '69', '41', '-', '48'),
                _row('53', '67', '46', '3.5', ''),
                _row('45', '63', '46', '5.5', ''),
                _row('31', '50', '62', '20.0', ''),
                _row('55', '48', '63', '21.5', '')
            ]),
            _table('NL Wild Card', [
                _row('53', '67', '46', '+2.0', '44'),
                _row('45', '63', '46', '-', '48'),
                _row('56', '59', '52', '5.0', ''),
                _row('36', '57', '53', '6.5', ''),
                _row('51', '57', '54', '7.0', ''),
                _row('32', '56', '55', '8.0', ''),
                _row('46', '52', '59', '12.0', ''),
                _row('31', '50', '62', '14.5', '')
            ])
        ]
        self.assertEqual(actual, expected)

    @mock.patch('util.standings.standings.logo_absolute')
    def test_standings_table__with_weak(self, mock_logo):
        mock_logo.side_effect = _fake_logo

        records = {
            '31': '77-60',
            '32': '58-79',
            '33': '53-82',
            '34': '70-64',
            '35': '65-70',
            '36': '82-53',
            '37': '60-76',
            '38': '84-52',
            '39': '61-75',
            '40': '75-60',
            '41': '80-57',
            '42': '70-65',
            '43': '48-89',
            '44': '71-66',
            '45': '89-47',
            '46': '79-57',
            '47': '75-61',
            '48': '65-70',
            '49': '59-78',
            '50': '65-72',
            '51': '64-72',
            '52': '74-62',
            '53': '63-75',
            '54': '67-70',
            '55': '55-82',
            '56': '60-77',
            '57': '65-71',
            '58': '61-75',
            '59': '80-55',
            '60': '67-70',
        }
        actual = standings_table(records)
        expected = [
            _table('AL East', [
                _row('59', '80', '55', '-', '19'),
                _row('34', '70', '64', '9.5', ''),
                _row('48', '65', '70', '15.0', ''),
                _row('57', '65', '71', '15.5', ''),
                _row('33', '53', '82', '27.0', '')
            ]),
            _table('AL Central', [
                _row('38', '84', '52', '-', '19'),
                _row('40', '75', '60', '8.5', ''),
                _row('47', '75', '61', '9.0', ''),
                _row('35', '65', '70', '18.5', ''),
                _row('43', '48', '89', '36.5', '')
            ]),
            _table('AL West', [
                _row('42', '70', '65', '-', '27'),
                _row('44', '71', '66', '-', '27'),
                _row('54', '67', '70', '4.0', ''),
                _row('50', '65', '72', '6.0', ''),
                _row('58', '61', '75', '9.5', '')
            ]),
            _table('AL Wild Card', [
                _row('40', '75', '60', '+0.5', '24'),
                _row('47', '75', '61', '-', '24'),
                _row('34', '70', '64', '4.0', ''),
                _row('42', '70', '65', '4.5', ''),
                _row('44', '71', '66', '4.5', ''),
                _row('54', '67', '70', '8.5', ''),
                _row('35', '65', '70', '9.5', ''),
                _row('48', '65', '70', '9.5', '')
            ]),
            _table('NL East', [
                _row('41', '80', '57', '-', '13'),
                _row('60', '67', '70', '13.0', ''),
                _row('51', '64', '72', '15.5', ''),
                _row('49', '59', '78', '21.0', ''),
                _row('32', '58', '79', '22.0', '')
            ]),
            _table('NL Central', [
                _row('36', '82', '53', '-', '24'),
                _row('46', '79', '57', '3.5', ''),
                _row('52', '74', '62', '8.5', ''),
                _row('37', '60', '76', '22.5', ''),
                _row('56', '60', '77', '23.0', '')
            ]),
            _table('NL West', [
                _row('45', '89', '47', '-', '14'),
                _row('31', '77', '60', '12.5', ''),
                _row('53', '63', '75', '27.0', ''),
                _row('39', '61', '75', '28.0', ''),
                _row('55', '55', '82', '34.5', '')
            ]),
            _table('NL Wild Card', [
                _row('46', '79', '57', '+2.5', '22'),
                _row('31', '77', '60', '-', '24'),
                _row('52', '74', '62', '2.5', ''),
                _row('60', '67', '70', '10.0', ''),
                _row('51', '64', '72', '12.5', ''),
                _row('53', '63', '75', '14.5', ''),
                _row('39', '61', '75', '15.5', ''),
                _row('37', '60', '76', '16.5', '')
            ])
        ]
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
