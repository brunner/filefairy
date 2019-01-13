#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for encyclopedia.py."""

import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/common/encyclopedia', '', _path))

from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.encyclopedia.encyclopedia import set_reference  # noqa
from common.encyclopedia.encyclopedia import player_to_bats  # noqa
from common.encyclopedia.encyclopedia import player_to_name  # noqa
from common.encyclopedia.encyclopedia import player_to_name_sub  # noqa
from common.encyclopedia.encyclopedia import player_to_number  # noqa
from common.encyclopedia.encyclopedia import player_to_team  # noqa
from common.encyclopedia.encyclopedia import player_to_throws  # noqa
from common.encyclopedia.encyclopedia import put_players  # noqa
from common.jinja2_.jinja2_ import env  # noqa
from impl.reference.reference import Reference  # noqa

ENV = env()

DATE_10260602 = datetime_datetime_pst(1985, 10, 26, 6, 2, 30)

PLAYERS = {'P123': 'T31 1 L R Jim Alfa', 'P456': 'T32 42 R L Jim Beta'}


class EncyclopediaTest(unittest.TestCase):
    def setUp(self):
        reference = Reference(date=DATE_10260602, e=ENV)
        reference.data['players'] = PLAYERS

        set_reference(reference)

    def test_player_to_bats(self):
        inputs = [('P123', 'L'), ('P456', 'R'), ('P789', 'R')]
        for num, expected in inputs:
            actual = player_to_bats(num)
            self.assertEqual(actual, expected)

    def test_player_to_name(self):
        inputs = [('P123', 'Jim Alfa'), ('P456', 'Jim Beta'),
                  ('P789', 'Jim Unknown')]
        for num, expected in inputs:
            actual = player_to_name(num)
            self.assertEqual(actual, expected)

    def test_player_to_name_sub(self):
        actual = player_to_name_sub('P123 (1-0, 0.00 ERA)')
        expected = 'Jim Alfa (1-0, 0.00 ERA)'
        self.assertEqual(actual, expected)

    def test_player_to_number(self):
        inputs = [('P123', '1'), ('P456', '42'), ('P789', '0')]
        for num, expected in inputs:
            actual = player_to_number(num)
            self.assertEqual(actual, expected)

    def test_player_to_team(self):
        inputs = [('P123', 'T31'), ('P456', 'T32'), ('P789', 'T??')]
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
