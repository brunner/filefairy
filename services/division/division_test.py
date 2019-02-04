#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for division.py."""

import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/services/division', '', _path))

from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import table  # noqa
from common.teams.teams import icon_absolute  # noqa
from common.teams.teams import icon_badge  # noqa
from services.division.division import condensed_league  # noqa
from services.division.division import expanded_impl  # noqa
from services.division.division import expanded_league  # noqa

EAST = {'T33': '1-1', 'T34': '2-0', 'T48': '0-2'}
CENTRAL = {'T35': '1-1', 'T38': '2-0', 'T40': '0-2'}
LEADERS = ['T34', 'T38']
WILD_CARD = {'T33': '1-1', 'T35': '1-1', 'T40': '0-2', 'T48': '0-2'}


def _condensed_row(*args):
    i = iter(args)
    row = []
    for encoding in i:
        row.append(cell(content=icon_badge(encoding, next(i), True)))
    return row


def _expanded_head(subleague):
    return [
        cell(content=subleague),
        cell(content='W'),
        cell(content='L'),
        cell(content='%'),
        cell(content='GB'),
    ]


def _expanded_row(*args):
    contents = [icon_absolute(args[0], args[1])] + list(args[2:])
    return [cell(content=content) for content in contents]


class DivisionTest(unittest.TestCase):
    def test_condensed_league(self):
        e = {'T33': ('1-1', True), 'T34': ('2-0', True), 'T48': ('0-2', True)}
        c = {'T35': ('1-1', True), 'T38': ('2-0', True), 'T40': ('0-2', True)}
        tables = [('East', e), ('Central', c)]

        bc = 'position-relative text-center w-20 badge-icon-wrapper'
        hc = 'font-weight-bold text-dark text-center'
        actual = condensed_league('American League', tables)
        expected = table(
            clazz='table-fixed border mb-3',
            hcols=[col(clazz=hc, colspan=3)],
            bcols=[
                col(clazz=(bc + ' pl-2')),
                col(clazz=bc),
                col(clazz=(bc + ' pr-2')),
            ],
            head=[[cell(content='American League')]],
            body=[
                _condensed_row('T34', '2-0', 'T33', '1-1', 'T48', '0-2'),
                _condensed_row('T38', '2-0', 'T35', '1-1', 'T40', '0-2'),
            ])
        self.assertEqual(actual, expected)

    def test_expanded_impl__empty(self):
        east = {'T33': '0-0', 'T34': '0-0', 'T48': '0-0'}
        central = {'T35': '0-0', 'T38': '0-0', 'T40': '0-0'}
        west = {'T42': '0-0', 'T44': '0-0', 'T50': '0-0'}
        tables = [('East', east), ('Central', central), ('West', west)]

        actual = expanded_impl('American League', tables)
        expected = [
            ('AL East', {
                'T33': ('0-0', '-'),
                'T34': ('0-0', '-'),
                'T48': ('0-0', '-'),
            }),
            ('AL Central', {
                'T35': ('0-0', '-'),
                'T38': ('0-0', '-'),
                'T40': ('0-0', '-'),
            }),
            ('AL West', {
                'T42': ('0-0', '-'),
                'T44': ('0-0', '-'),
                'T50': ('0-0', '-'),
            }),
            ('AL Wild Card', {
                'T33': ('0-0', '-'),
                'T34': ('0-0', '-'),
                'T35': ('0-0', '-'),
                'T38': ('0-0', '-'),
                'T40': ('0-0', '-'),
                'T42': ('0-0', '-'),
                'T44': ('0-0', '-'),
                'T48': ('0-0', '-'),
                'T50': ('0-0', '-'),
            }),
        ]
        self.assertEqual(actual, expected)

    def test_expanded_impl__final(self):
        east = {'T34': '99-63', 'T48': '88-74', 'T33': '70-92'}
        central = {'T40': '86-76', 'T35': '82-80', 'T38': '76-86'}
        west = {'T42': '85-77', 'T50': '75-87', 'T44': '70-92'}
        tables = [('East', east), ('Central', central), ('West', west)]

        actual = expanded_impl('American League', tables)
        expected = [
            ('AL East', {
                'T34': ('99-63', '-'),
                'T48': ('88-74', '11.0'),
                'T33': ('70-92', '29.0'),
            }),
            ('AL Central', {
                'T40': ('86-76', '-'),
                'T35': ('82-80', '4.0'),
                'T38': ('76-86', '10.0'),
            }),
            ('AL West', {
                'T42': ('85-77', '-'),
                'T50': ('75-87', '10.0'),
                'T44': ('70-92', '15.0'),
            }),
            ('AL Wild Card', {
                'T48': ('88-74', '+6.0'),
                'T35': ('82-80', '-'),
                'T38': ('76-86', '6.0'),
                'T50': ('75-87', '7.0'),
                'T33': ('70-92', '12.0'),
                'T44': ('70-92', '12.0'),
            }),
        ]
        self.assertEqual(actual, expected)

    def test_expanded_impl__irregular(self):
        east = {'T33': '26-15', 'T34': '23-13', 'T48': '17-20'}
        central = {'T38': '23-15', 'T35': '24-16', 'T40': '22-17'}
        west = {'T42': '25-13', 'T44': '21-18', 'T50': '19-19'}
        tables = [('East', east), ('Central', central), ('West', west)]

        actual = expanded_impl('American League', tables)
        expected = [
            ('AL East', {
                'T33': ('26-15', '-'),
                'T34': ('23-13', '0.5'),
                'T48': ('17-20', '7.0'),
            }),
            ('AL Central', {
                'T38': ('23-15', '-'),
                'T35': ('24-16', '-'),
                'T40': ('22-17', '1.5'),
            }),
            ('AL West', {
                'T42': ('25-13', '-'),
                'T44': ('21-18', '4.5'),
                'T50': ('19-19', '6.0'),
            }),
            ('AL Wild Card', {
                'T34': ('23-13', '+1.0'),
                'T38': ('23-15', '-'),
                'T35': ('24-16', '-'),
                'T40': ('22-17', '1.5'),
                'T44': ('21-18', '2.5'),
                'T50': ('19-19', '4.0'),
                'T48': ('17-20', '5.5'),
            }),
        ]
        self.assertEqual(actual, expected)

    def test_expanded_impl__midseason(self):
        east = {'T33': '64-47', 'T34': '57-54', 'T48': '57-54'}
        central = {'T38': '66-45', 'T35': '59-53', 'T40': '57-54'}
        west = {'T42': '65-45', 'T44': '54-57', 'T50': '53-58'}
        tables = [('East', east), ('Central', central), ('West', west)]

        actual = expanded_impl('American League', tables)
        expected = [
            ('AL East', {
                'T33': ('64-47', '-'),
                'T34': ('57-54', '7.0'),
                'T48': ('57-54', '7.0'),
            }),
            ('AL Central', {
                'T38': ('66-45', '-'),
                'T35': ('59-53', '7.5'),
                'T40': ('57-54', '9.0'),
            }),
            ('AL West', {
                'T42': ('65-45', '-'),
                'T44': ('54-57', '11.5'),
                'T50': ('53-58', '12.5'),
            }),
            ('AL Wild Card', {
                'T35': ('59-53', '+1.5'),
                'T34': ('57-54', '-'),
                'T40': ('57-54', '-'),
                'T48': ('57-54', '-'),
                'T44': ('54-57', '3.0'),
                'T50': ('53-58', '4.0'),
            }),
        ]
        self.assertEqual(actual, expected)

    def test_expanded_impl__weak(self):
        east = {'T33': '80-55', 'T34': '70-64', 'T48': '65-70'}
        central = {'T38': '84-52', 'T35': '75-60', 'T40': '75-61'}
        west = {'T42': '70-65', 'T44': '71-66', 'T50': '67-70'}
        tables = [('East', east), ('Central', central), ('West', west)]

        actual = expanded_impl('American League', tables)
        expected = [
            ('AL East', {
                'T33': ('80-55', '-'),
                'T34': ('70-64', '9.5'),
                'T48': ('65-70', '15.0'),
            }),
            ('AL Central', {
                'T38': ('84-52', '-'),
                'T35': ('75-60', '8.5'),
                'T40': ('75-61', '9.0'),
            }),
            ('AL West', {
                'T42': ('70-65', '-'),
                'T44': ('71-66', '-'),
                'T50': ('67-70', '4.0'),
            }),
            ('AL Wild Card', {
                'T35': ('75-60', '+0.5'),
                'T40': ('75-61', '-'),
                'T34': ('70-64', '4.0'),
                'T42': ('70-65', '4.5'),
                'T44': ('71-66', '4.5'),
                'T50': ('67-70', '8.5'),
                'T48': ('65-70', '9.5'),
            }),
        ]
        self.assertEqual(actual, expected)

    @mock.patch('services.division.division.expanded_impl')
    def test_expanded_league(self, mock_expanded):
        mock_expanded.return_value = [
            ('AL East', {
                'T33': ('1-1', '1.0'),
                'T34': ('2-0', '-'),
                'T48': ('0-2', '2.0')
            }),
            ('AL Central', {
                'T35': ('1-1', '1.0'),
                'T38': ('2-0', '-'),
                'T40': ('0-2', '2.0')
            }),
            ('AL Wild Card', {
                'T33': ('1-1', '-'),
                'T35': ('1-1', '-'),
                'T40': ('0-2', '1.0'),
                'T48': ('0-2', '1.0')
            }),
        ]

        east = {'T33': '1-1', 'T34': '2-0', 'T48': '0-2'}
        central = {'T35': '1-1', 'T38': '2-0', 'T40': '0-2'}
        tables = [('East', east), ('Central', central)]

        hc = 'font-weight-bold text-dark '
        clazzes = [
            'position-relative text-truncate',
            'text-right w-40p',
            'text-right w-40p',
            'text-right w-50p',
            'text-right w-50p',
        ]
        hcols = [col(clazz=(hc + c)) for c in clazzes]
        bcols = [col(clazz=c) for c in clazzes]

        actual = expanded_league('American League', tables)
        expected = [
            table(
                clazz='table-fixed border mb-3',
                hcols=hcols,
                bcols=bcols,
                head=[_expanded_head('AL East')],
                body=[
                    _expanded_row('T34', 'Boston', '2', '0', '1.000', '-'),
                    _expanded_row('T33', 'Baltimore', '1', '1', '.500', '1.0'),
                    _expanded_row('T48', 'New York', '0', '2', '.000', '2.0'),
                ],
            ),
            table(
                clazz='table-fixed border mb-3',
                hcols=hcols,
                bcols=bcols,
                head=[_expanded_head('AL Central')],
                body=[
                    _expanded_row('T38', 'Cleveland', '2', '0', '1.000', '-'),
                    _expanded_row('T35', 'Chicago', '1', '1', '.500', '1.0'),
                    _expanded_row('T40', 'Detroit', '0', '2', '.000', '2.0'),
                ],
            ),
            table(
                clazz='table-fixed border mb-3',
                hcols=hcols,
                bcols=bcols,
                head=[_expanded_head('AL Wild Card')],
                body=[
                    _expanded_row('T33', 'Baltimore', '1', '1', '.500', '-'),
                    _expanded_row('T35', 'Chicago', '1', '1', '.500', '-'),
                    _expanded_row('T40', 'Detroit', '0', '2', '.000', '1.0'),
                    _expanded_row('T48', 'New York', '0', '2', '.000', '1.0'),
                ],
            )
        ]
        self.assertEqual(actual, expected)

        mock_expanded.assert_called_once_with('American League', tables)


if __name__ == '__main__':
    unittest.main()
