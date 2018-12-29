#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for standings.py."""

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/common/teams', '', _path)
sys.path.append(_root)
from common.teams.teams import decoding_to_encoding  # noqa
from common.teams.teams import decoding_to_encoding_sub  # noqa
from common.teams.teams import encoding_keys  # noqa
from common.teams.teams import encoding_to_decoding  # noqa
from common.teams.teams import encoding_to_decoding_sub  # noqa
from common.teams.teams import encoding_to_nickname  # noqa
from common.teams.teams import encoding_to_teamid  # noqa
from common.teams.teams import icon_inline  # noqa
from common.teams.teams import precoding_to_encoding  # noqa
from common.teams.teams import precoding_to_encoding_sub  # noqa

DECODING = [
    'Arizona Diamondbacks', 'Atlanta Braves', 'Baltimore Orioles',
    'Boston Red Sox', 'Chicago White Sox', 'Chicago Cubs', 'Cincinnati Reds',
    'Cleveland Indians', 'Colorado Rockies', 'Detroit Tigers', 'Miami Marlins',
    'Houston Astros', 'Kansas City Royals', 'Los Angeles Angels',
    'Los Angeles Dodgers', 'Milwaukee Brewers', 'Minnesota Twins',
    'New York Yankees', 'New York Mets', 'Oakland Athletics',
    'Philadelphia Phillies', 'Pittsburgh Pirates', 'San Diego Padres',
    'Seattle Mariners', 'San Francisco Giants', 'St. Louis Cardinals',
    'Tampa Bay Rays', 'Texas Rangers', 'Toronto Blue Jays',
    'Washington Nationals',
]  # yapf: disable

DE_ENCODING = [
    'T31', 'T32', 'T33', 'T34', 'T35', 'T36', 'T37', 'T38', 'T39', 'T40',
    'T41', 'T42', 'T43', 'T44', 'T45', 'T46', 'T47', 'T48', 'T49', 'T50',
    'T51', 'T52', 'T53', 'T54', 'T55', 'T56', 'T57', 'T58', 'T59', 'T60',
]  # yapf: disable

ENCODING_KEYS = DE_ENCODING + ['TCH', 'TLA', 'TNY']

NICKNAME = [
    'Diamondbacks', 'Braves', 'Orioles', 'Red Sox', 'White Sox', 'Cubs',
    'Reds', 'Indians', 'Rockies', 'Tigers', 'Marlins', 'Astros', 'Royals',
    'Angels', 'Dodgers', 'Brewers', 'Twins', 'Yankees', 'Mets', 'Athletics',
    'Phillies', 'Pirates', 'Padres', 'Mariners', 'Giants', 'Cardinals', 'Rays',
    'Rangers', 'Blue Jays', 'Nationals', '', '', '',
]  # yapf: disable

PRE_ENCODING = [
    'T31', 'T32', 'T33', 'T34', 'T37', 'T38', 'T39', 'T40', 'T41', 'T42',
    'T43', 'T46', 'T47', 'T50', 'T51', 'T52', 'T53', 'T54', 'T55', 'T56',
    'T57', 'T58', 'T59', 'T60', 'TCH', 'TLA', 'TNY',
]  # yapf: disable

PRECODING = [
    'Arizona', 'Atlanta', 'Baltimore', 'Boston', 'Cincinnati', 'Cleveland',
    'Colorado', 'Detroit', 'Miami', 'Houston', 'Kansas City', 'Milwaukee',
    'Minnesota', 'Oakland', 'Philadelphia', 'Pittsburgh', 'San Diego',
    'Seattle', 'San Francisco', 'St. Louis', 'Tampa Bay', 'Texas', 'Toronto',
    'Washington', 'Chicago', 'Los Angeles', 'New York',
]  # yapf: disable

TEAMID = [
    '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42',
    '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54',
    '55', '56', '57', '58', '59', '60', '', '', '',
]  # yapf: disable


class TeamTest(unittest.TestCase):
    def test_decoding_to_encoding(self):
        for decoding, encoding in zip(DECODING, DE_ENCODING):
            actual = decoding_to_encoding(decoding)
            self.assertEqual(actual, encoding)

    def test_decoding_to_encoding_sub(self):
        actual = decoding_to_encoding_sub(', '.join(DECODING))
        expected = ', '.join(DE_ENCODING)
        self.assertEqual(actual, expected)

    def test_encoding_to_decoding(self):
        for encoding, decoding in zip(DE_ENCODING, DECODING):
            actual = encoding_to_decoding(encoding)
            self.assertEqual(actual, decoding)

    def test_encoding_to_decoding_sub(self):
        actual = encoding_to_decoding_sub(', '.join(DE_ENCODING))
        expected = ', '.join(DECODING)
        self.assertEqual(actual, expected)

    def test_encoding_to_nickname(self):
        for encoding, nickname in zip(DE_ENCODING, NICKNAME):
            actual = encoding_to_nickname(encoding)
            self.assertEqual(actual, nickname)

    def test_encoding_to_teamid(self):
        for encoding, teamid in zip(DE_ENCODING, TEAMID):
            actual = encoding_to_teamid(encoding)
            self.assertEqual(actual, teamid)

    def test_encoding_keys(self):
        actual = encoding_keys()
        self.assertEqual(actual, ENCODING_KEYS)

    def test_icon_inline__one(self):
        actual = icon_inline('T36', '0-0')
        src = 'https://fairylab.surge.sh/images/teams/cubs/cubs-icon.png'
        img = ('<img src="{}" width="20" height="20" border="0" class="d-inli'
               'ne-block">').format(src)
        span = '<span class="align-middle d-inline-block px-2">0-0</span>'
        expected = img + span
        self.assertEqual(actual, expected)

    def test_icon_inline__two(self):
        actual = icon_inline('T35', '0-0')
        src = ('https://fairylab.surge.sh/images/teams/whitesox/whitesox-icon.'
               'png')
        img = ('<img src="{}" width="20" height="20" border="0" class="d-inli'
               'ne-block">').format(src)
        span = '<span class="align-middle d-inline-block px-2">0-0</span>'
        expected = img + span
        self.assertEqual(actual, expected)

    def test_precoding_to_encoding(self):
        for precoding, encoding in zip(PRECODING, PRE_ENCODING):
            actual = precoding_to_encoding(precoding)
            self.assertEqual(actual, encoding)

    def test_precoding_to_encoding_sub(self):
        actual = precoding_to_encoding_sub(', '.join(PRECODING))
        expected = ', '.join(PRE_ENCODING)
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
