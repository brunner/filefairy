#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for reference.py."""

import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/common/reference', '', _path))

from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.elements.elements import anchor  # noqa
from common.reference.reference import player_to_bats  # noqa
from common.reference.reference import player_to_link  # noqa
from common.reference.reference import player_to_link_sub  # noqa
from common.reference.reference import player_to_name  # noqa
from common.reference.reference import player_to_name_sub  # noqa
from common.reference.reference import player_to_number  # noqa
from common.reference.reference import player_to_shortname  # noqa
from common.reference.reference import player_to_shortname_sub  # noqa
from common.reference.reference import player_to_starter  # noqa
from common.reference.reference import player_to_starter_sub  # noqa
from common.reference.reference import player_to_team  # noqa
from common.reference.reference import player_to_throws  # noqa
from common.reference.reference import put_players  # noqa
from common.reference.reference import set_reference  # noqa
from common.jinja2_.jinja2_ import env  # noqa
from impl.reference.reference import Reference  # noqa

ENV = env()

DATE_10260602 = datetime_datetime_pst(1985, 10, 26, 6, 2, 30)

PLAYERS = {'P123': 'T31 1 L R Jim Alfa', 'P456': 'T32 42 R L Jim Beta'}

STATSPLUS_PLAYER = 'https://statsplus.net/oblootp/player/'


class ReferenceTest(unittest.TestCase):
    def setUp(self):
        reference = Reference(date=DATE_10260602)
        reference.data['players'] = PLAYERS

        set_reference(reference)

    def test_player_to_bats(self):
        inputs = [('P123', 'L'), ('P456', 'R'), ('P789', 'R')]
        for num, expected in inputs:
            actual = player_to_bats(num)
            self.assertEqual(actual, expected)

    def test_player_to_link(self):
        inputs = [
            ('P123', anchor(STATSPLUS_PLAYER + '123', 'Jim Alfa')),
            ('P456', anchor(STATSPLUS_PLAYER + '456', 'Jim Beta')),
            ('P789', anchor(STATSPLUS_PLAYER + '789', 'Jim Unknown')),
        ]
        for num, expected in inputs:
            actual = player_to_link(num)
            self.assertEqual(actual, expected)

    def test_player_to_link_sub(self):
        actual = player_to_link_sub('P123 (1-0)')
        expected = ' '.join(
            [anchor(STATSPLUS_PLAYER + '123', 'Jim Alfa'), '(1-0)'])
        self.assertEqual(actual, expected)

    def test_player_to_name(self):
        inputs = [('P123', 'Jim Alfa'), ('P456', 'Jim Beta'),
                  ('P789', 'Jim Unknown')]
        for num, expected in inputs:
            actual = player_to_name(num)
            self.assertEqual(actual, expected)

    def test_player_to_name_sub(self):
        actual = player_to_name_sub('P123 (1-0)')
        expected = 'Jim Alfa (1-0)'
        self.assertEqual(actual, expected)

    def test_player_to_number(self):
        inputs = [('P123', '1'), ('P456', '42'), ('P789', '0')]
        for num, expected in inputs:
            actual = player_to_number(num)
            self.assertEqual(actual, expected)

    def test_player_to_shortname(self):
        inputs = [('P123', 'J. Alfa'), ('P456', 'J. Beta'),
                  ('P789', 'J. Unknown')]
        for num, expected in inputs:
            actual = player_to_shortname(num)
            self.assertEqual(actual, expected)

    def test_player_to_shortname_sub(self):
        actual = player_to_shortname_sub('P123 (1-0)')
        expected = 'J. Alfa (1-0)'
        self.assertEqual(actual, expected)

    def test_player_to_starter(self):
        inputs = [('P123', 'Jim Alfa (R)'), ('P456', 'Jim Beta (L)'),
                  ('P789', 'Jim Unknown (R)')]
        for num, expected in inputs:
            actual = player_to_starter(num)
            self.assertEqual(actual, expected)

    def test_player_to_starter_sub(self):
        actual = player_to_starter_sub('ARI: P123')
        expected = 'ARI: Jim Alfa (R)'
        self.assertEqual(actual, expected)

    def test_player_to_team(self):
        inputs = [('P123', 'T31'), ('P456', 'T32'), ('P789', 'T30')]
        for num, expected in inputs:
            actual = player_to_team(num)
            self.assertEqual(actual, expected)

    def test_player_to_throws(self):
        inputs = [('P123', 'R'), ('P456', 'L'), ('P789', 'R')]
        for num, expected in inputs:
            actual = player_to_throws(num)
            self.assertEqual(actual, expected)

    @mock.patch.object(Reference, '_put')
    def test_put_players(self, mock_put):
        put_players(['P123', 'P456', 'P789'])
        mock_put.assert_called_once_with(['P123', 'P456', 'P789'])


if __name__ == '__main__':
    unittest.main()
