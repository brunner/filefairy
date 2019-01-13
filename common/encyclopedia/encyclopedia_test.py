#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for encyclopedia.py."""

import os
import re
import sys
import unittest

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
        inputs = [('123', 'L'), ('456', 'R'), ('789', 'R')]
        for num, expected in inputs:
            actual = player_to_bats(num)
            self.assertEqual(actual, expected)

    def test_player_to_name(self):
        inputs = [('123', 'Jim Alfa'), ('456', 'Jim Beta'),
                  ('789', 'Jim Unknown')]
        for num, expected in inputs:
            actual = player_to_name(num)
            self.assertEqual(actual, expected)

    def test_player_to_name_sub(self):
        actual = player_to_name_sub('P123 (1-0, 0.00 ERA)')
        expected = 'Jim Alfa (1-0, 0.00 ERA)'
        self.assertEqual(actual, expected)

    def test_player_to_number(self):
        inputs = [('123', '1'), ('456', '42'), ('789', '0')]
        for num, expected in inputs:
            actual = player_to_number(num)
            self.assertEqual(actual, expected)

    def test_player_to_team(self):
        inputs = [('123', 'T31'), ('456', 'T32'), ('789', 'T??')]
        for num, expected in inputs:
            actual = player_to_team(num)
            self.assertEqual(actual, expected)

    def test_player_to_throws(self):
        inputs = [('123', 'R'), ('456', 'L'), ('789', 'R')]
        for num, expected in inputs:
            actual = player_to_throws(num)
            self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
