#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for teams.py."""

import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/common/teams', '', _path))

from common.teams.teams import color_name  # noqa
from common.teams.teams import decoding_to_encoding  # noqa
from common.teams.teams import decoding_to_encoding_sub  # noqa
from common.teams.teams import encoding_keys  # noqa
from common.teams.teams import encoding_to_abbreviation  # noqa
from common.teams.teams import encoding_to_colors  # noqa
from common.teams.teams import encoding_to_decoding  # noqa
from common.teams.teams import encoding_to_decoding_sub  # noqa
from common.teams.teams import encoding_to_encodings  # noqa
from common.teams.teams import encoding_to_hometown  # noqa
from common.teams.teams import encoding_to_hometown_sub  # noqa
from common.teams.teams import encoding_to_lower  # noqa
from common.teams.teams import encoding_to_nickname  # noqa
from common.teams.teams import encoding_to_repo  # noqa
from common.teams.teams import encoding_to_tag  # noqa
from common.teams.teams import encoding_to_teamid  # noqa
from common.teams.teams import icon_absolute  # noqa
from common.teams.teams import icon_badge  # noqa
from common.teams.teams import jersey_absolute  # noqa
from common.teams.teams import jersey_color  # noqa
from common.teams.teams import precoding_to_encoding  # noqa
from common.teams.teams import precoding_to_encoding_sub  # noqa

BLACK = 'black'
BLUE = 'blue'
CREAM = 'cream'
GREEN = 'green'
GREY = 'grey'
ORANGE = 'orange'
PURPLE = 'purple'
RED = 'red'
SKY = 'sky'
WHITE = 'white'
YELLOW = 'yellow'

MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = range(7)

DECODING_KEYS = [
    'Arizona Diamondbacks', 'Atlanta Braves', 'Baltimore Orioles',
    'Boston Red Sox', 'Chicago White Sox', 'Chicago Cubs', 'Cincinnati Reds',
    'Cleveland Indians', 'Colorado Rockies', 'Detroit Tigers', 'Miami Marlins',
    'Houston Astros', 'Kansas City Royals', 'Los Angeles Angels',
    'Los Angeles Dodgers', 'Milwaukee Brewers', 'Minnesota Twins',
    'New York Yankees', 'New York Mets', 'Oakland Athletics',
    'Philadelphia Phillies', 'Pittsburgh Pirates', 'San Diego Padres',
    'Seattle Mariners', 'San Francisco Giants', 'St. Louis Cardinals',
    'Tampa Bay Rays', 'Texas Rangers', 'Toronto Blue Jays',
    'Washington Nationals'
]

ENCODING_KEYS = [
    'T31', 'T32', 'T33', 'T34', 'T35', 'T36', 'T37', 'T38', 'T39', 'T40',
    'T41', 'T42', 'T43', 'T44', 'T45', 'T46', 'T47', 'T48', 'T49', 'T50',
    'T51', 'T52', 'T53', 'T54', 'T55', 'T56', 'T57', 'T58', 'T59', 'T60',
    'TCH', 'TLA', 'TNY'
]

PRECODING_KEYS = [
    'Arizona', 'Atlanta', 'Baltimore', 'Boston', 'Cincinnati', 'Cleveland',
    'Colorado', 'Detroit', 'Miami', 'Houston', 'Kansas City', 'Milwaukee',
    'Minnesota', 'Oakland', 'Philadelphia', 'Pittsburgh', 'San Diego',
    'Seattle', 'San Francisco', 'St. Louis', 'Tampa Bay', 'Texas', 'Toronto',
    'Washington', 'Chicago', 'Los Angeles', 'New York'
]


class TeamTest(unittest.TestCase):
    def test_color_name__alt(self):
        actual = color_name(CREAM)
        expected = 'alt-cream'
        self.assertEqual(actual, expected)

    def test_color_name__away(self):
        actual = color_name(GREY)
        expected = 'away'
        self.assertEqual(actual, expected)

    def test_color_name__home(self):
        actual = color_name(WHITE)
        expected = 'home'
        self.assertEqual(actual, expected)

    def test_decoding_to_encoding(self):
        encodings = [
            'T31', 'T32', 'T33', 'T34', 'T35', 'T36', 'T37', 'T38', 'T39',
            'T40', 'T41', 'T42', 'T43', 'T44', 'T45', 'T46', 'T47', 'T48',
            'T49', 'T50', 'T51', 'T52', 'T53', 'T54', 'T55', 'T56', 'T57',
            'T58', 'T59', 'T60'
        ]
        for decoding, encoding in zip(DECODING_KEYS, encodings):
            actual = decoding_to_encoding(decoding)
            self.assertEqual(actual, encoding)

    def test_decoding_to_encoding_sub(self):
        encodings = [
            'T31', 'T32', 'T33', 'T34', 'T35', 'T36', 'T37', 'T38', 'T39',
            'T40', 'T41', 'T42', 'T43', 'T44', 'T45', 'T46', 'T47', 'T48',
            'T49', 'T50', 'T51', 'T52', 'T53', 'T54', 'T55', 'T56', 'T57',
            'T58', 'T59', 'T60'
        ]
        actual = decoding_to_encoding_sub(', '.join(DECODING_KEYS))
        expected = ', '.join(encodings)
        self.assertEqual(actual, expected)

    def test_encoding_to_abbreviation(self):
        abbreviations = [
            'ARI', 'ATL', 'BAL', 'BOS', 'CWS', 'CHC', 'CIN', 'CLE', 'COL',
            'DET', 'MIA', 'HOU', 'KC', 'LAA', 'LAD', 'MIL', 'MIN', 'NYY',
            'NYM', 'OAK', 'PHI', 'PIT', 'SD', 'SEA', 'SF', 'STL', 'TB', 'TEX',
            'TOR', 'WAS', '', '', ''
        ]
        for encoding, abbreviation in zip(ENCODING_KEYS, abbreviations):
            actual = encoding_to_abbreviation(encoding)
            self.assertEqual(actual, abbreviation)

    def test_encoding_to_colors(self):
        colors = [
            [RED],
            [CREAM, BLUE],
            [BLACK, ORANGE],
            [RED, BLUE],
            [BLUE, BLACK],
            [BLUE],
            [RED],
            [BLUE],
            [PURPLE, BLACK],
            [BLUE, ORANGE],
            [],
            [ORANGE],
            [SKY, BLUE],
            [RED],
            [],
            [SKY],
            [CREAM, BLUE],
            [],
            [BLACK, BLUE],
            [YELLOW, GREEN],
            [SKY, CREAM],
            [YELLOW, BLACK],
            [CREAM, YELLOW],
            [GREEN, BLUE],
            [ORANGE],
            [CREAM],
            [SKY, BLUE],
            [SKY, BLUE],
            [BLUE],
            [BLUE, RED],
            [],
            [],
            [],
        ]
        for encoding, inner_colors in zip(ENCODING_KEYS, colors):
            actual = encoding_to_colors(encoding)
            self.assertEqual(actual, inner_colors)

    def test_encoding_to_decoding(self):
        decodings = [
            'Arizona Diamondbacks', 'Atlanta Braves', 'Baltimore Orioles',
            'Boston Red Sox', 'Chicago White Sox', 'Chicago Cubs',
            'Cincinnati Reds', 'Cleveland Indians', 'Colorado Rockies',
            'Detroit Tigers', 'Miami Marlins', 'Houston Astros',
            'Kansas City Royals', 'Los Angeles Angels', 'Los Angeles Dodgers',
            'Milwaukee Brewers', 'Minnesota Twins', 'New York Yankees',
            'New York Mets', 'Oakland Athletics', 'Philadelphia Phillies',
            'Pittsburgh Pirates', 'San Diego Padres', 'Seattle Mariners',
            'San Francisco Giants', 'St. Louis Cardinals', 'Tampa Bay Rays',
            'Texas Rangers', 'Toronto Blue Jays', 'Washington Nationals', '',
            '', ''
        ]
        for encoding, decoding in zip(ENCODING_KEYS, decodings):
            actual = encoding_to_decoding(encoding)
            self.assertEqual(actual, decoding)

    def test_encoding_to_decoding_sub(self):
        decodings = [
            'Arizona Diamondbacks', 'Atlanta Braves', 'Baltimore Orioles',
            'Boston Red Sox', 'Chicago White Sox', 'Chicago Cubs',
            'Cincinnati Reds', 'Cleveland Indians', 'Colorado Rockies',
            'Detroit Tigers', 'Miami Marlins', 'Houston Astros',
            'Kansas City Royals', 'Los Angeles Angels', 'Los Angeles Dodgers',
            'Milwaukee Brewers', 'Minnesota Twins', 'New York Yankees',
            'New York Mets', 'Oakland Athletics', 'Philadelphia Phillies',
            'Pittsburgh Pirates', 'San Diego Padres', 'Seattle Mariners',
            'San Francisco Giants', 'St. Louis Cardinals', 'Tampa Bay Rays',
            'Texas Rangers', 'Toronto Blue Jays', 'Washington Nationals',
            'TCH', 'TLA', 'TNY'
        ]
        actual = encoding_to_decoding_sub(', '.join(ENCODING_KEYS))
        expected = ', '.join(decodings)
        self.assertEqual(actual, expected)

    def test_encoding_to_encodings(self):
        encodings = [['T31'], ['T32'], ['T33'], ['T34'], ['T35'], ['T36'],
                     ['T37'], ['T38'], ['T39'], ['T40'], ['T41'], ['T42'],
                     ['T43'], ['T44'], ['T45'], ['T46'], ['T47'], ['T48'],
                     ['T49'], ['T50'], ['T51'], ['T52'], ['T53'], ['T54'],
                     ['T55'], ['T56'], ['T57'], ['T58'], ['T59'], ['T60'],
                     ['T35', 'T36'], ['T44', 'T45'], ['T48', 'T49']]
        for encoding, inner_encodings in zip(ENCODING_KEYS, encodings):
            actual = encoding_to_encodings(encoding)
            self.assertEqual(actual, inner_encodings)

    def test_encoding_to_hometown(self):
        hometowns = [
            'Arizona', 'Atlanta', 'Baltimore', 'Boston', 'Chicago', 'Chicago',
            'Cincinnati', 'Cleveland', 'Colorado', 'Detroit', 'Miami',
            'Houston', 'Kansas City', 'Los Angeles', 'Los Angeles',
            'Milwaukee', 'Minnesota', 'New York', 'New York', 'Oakland',
            'Philadelphia', 'Pittsburgh', 'San Diego', 'Seattle',
            'San Francisco', 'St. Louis', 'Tampa Bay', 'Texas', 'Toronto',
            'Washington', 'Chicago', 'Los Angeles', 'New York'
        ]
        for encoding, hometown in zip(ENCODING_KEYS, hometowns):
            actual = encoding_to_hometown(encoding)
            self.assertEqual(actual, hometown)

    def test_encoding_to_hometown_sub(self):
        hometowns = [
            'Arizona', 'Atlanta', 'Baltimore', 'Boston', 'Chicago', 'Chicago',
            'Cincinnati', 'Cleveland', 'Colorado', 'Detroit', 'Miami',
            'Houston', 'Kansas City', 'Los Angeles', 'Los Angeles',
            'Milwaukee', 'Minnesota', 'New York', 'New York', 'Oakland',
            'Philadelphia', 'Pittsburgh', 'San Diego', 'Seattle',
            'San Francisco', 'St. Louis', 'Tampa Bay', 'Texas', 'Toronto',
            'Washington', 'Chicago', 'Los Angeles', 'New York'
        ]
        actual = encoding_to_hometown_sub(', '.join(ENCODING_KEYS))
        expected = ', '.join(hometowns)
        self.assertEqual(actual, expected)

    def test_encoding_to_lower(self):
        lowers = [
            'diamondbacks', 'braves', 'orioles', 'redsox', 'whitesox', 'cubs',
            'reds', 'indians', 'rockies', 'tigers', 'marlins', 'astros',
            'royals', 'angels', 'dodgers', 'brewers', 'twins', 'yankees',
            'mets', 'athletics', 'phillies', 'pirates', 'padres', 'mariners',
            'giants', 'cardinals', 'rays', 'rangers', 'bluejays', 'nationals',
            '', '', ''
        ]
        for encoding, lower in zip(ENCODING_KEYS, lowers):
            actual = encoding_to_lower(encoding)
            self.assertEqual(actual, lower)

    def test_encoding_to_nickname(self):
        nicknames = [
            'Diamondbacks', 'Braves', 'Orioles', 'Red Sox', 'White Sox',
            'Cubs', 'Reds', 'Indians', 'Rockies', 'Tigers', 'Marlins',
            'Astros', 'Royals', 'Angels', 'Dodgers', 'Brewers', 'Twins',
            'Yankees', 'Mets', 'Athletics', 'Phillies', 'Pirates', 'Padres',
            'Mariners', 'Giants', 'Cardinals', 'Rays', 'Rangers', 'Blue Jays',
            'Nationals', '', '', ''
        ]
        for encoding, nickname in zip(ENCODING_KEYS, nicknames):
            actual = encoding_to_nickname(encoding)
            self.assertEqual(actual, nickname)

    def test_encoding_to_repo(self):
        repos = [
            '925f81153b44d0b35734ca0c43b9f89a',
            '70fe783889494c2c0de8cd9b2dbd05b2',
            '6df0d030fbb62f9cd169624afe5351e3',
            '4a6a4036834b558756dac7ac9c0309d0',
            '359d34636fabc914a83a8c746fc6eba9',
            'ed81fde94a24fdce340a19e52fda33bd',
            'af532f33900c377ea6a7d5c373a9785f',
            '40b0331a059d0ad8869df7e101863401',
            '79886209567ba70e64192b9810bde6a3',
            '89a0edfe4287648effd8021807ef9625',
            '793744dc81800fea7f219dd22b28afa1',
            '2d3444f09ba1f0c9a06b6e9bdd27eda7',
            'f87f4b6bf4821f16ef57eae0823e9fc7',
            '9780ce2762db67b17831a0c908aaf725',
            'd334f966fa470e01991d550266b94283',
            '5aa56738ca8fc3f8367d6f777614de38',
            '5b5568f5e186885d5e5175a25959f5d0',
            '5b8b9a01333351a92f6f91726dce239b',
            'aa9197d99dd2abcb7a50f13e5ae75ab0',
            '5641c5488e3de552ebd8f04c7d089fd9',
            '21cdbe29a981ae9e9eeeccbd93b7e76e',
            'b52b416175cd704f7dd007d890dd629e',
            'a2ae8f3ef490bad2f2f5510428d4bdc2',
            '146290fc1036d7628d016218e9a05a92',
            'd82f716325270e162d646bbaa7160c8b',
            '2f8467f7cef50d56217cd0bd4da65ca0',
            '72da90820a526e10bad1484efd2aaea3',
            '468cead9ea12e6bb3ba6f62236b8d1a7',
            '75833b35b51c8b6cd5c300e0d4117739',
            '7364eac50fccbb97ce1ea034da8e3c6a',
            '',
            '',
            '',
        ]
        for encoding, repo in zip(ENCODING_KEYS, repos):
            actual = encoding_to_repo(encoding)
            self.assertEqual(actual, repo)

    def test_encoding_to_tag(self):
        tags = [
            'e46d3919da84e127c46ddb9a98083fdfe45c550e',
            'af5e8226f04e295506a61636aaf6d405c6d24a54',
            'f9576bb0aa8427c19832bb972962b86c3a6cb1f2',
            'b370f4842d7d271d9935f30d231abe0368409944',
            '1afa211b3cec808c7d58863fd61d436bbdbe05da',
            'cf6811a0707e24be1ef2038f91cc295525274cf6',
            '8eb50b108f9f65dfcc71b30ddb3b9ab032a972c1',
            '39c4825ca85027191a3003528ce36ab6c85bf537',
            'ed1def95cd767f6c4e0601b6dd440d58f365e894',
            '2a80951e810dccdb569fc2f249e3fb8c00675000',
            'b2fe8e13546351a7272f1b90d066b398620adcac',
            'b19253b93017682124fe778e0a8624c12bcc6332',
            '1f8528c7ec317d89f3e7ba6de2b3c3dd7340f64c',
            '1018f1ba85a160d74d5a924749a6cd28cae44a40',
            '4572edb247c3b7281f01cf01e0ee97f34a14e145',
            '854c03ddbbd38842ee7e62f825b0dcd97cb9d391',
            '278276af922a94ee6396cace99f17c3a308da730',
            '0cfd7978330ee9e4c4c4fa37439b9abb903be46a',
            'b209622a6f5849a60035cd3f583914bb557fb514',
            'f62eb1e611dcb85832aa9cfc2ea1165a99325beb',
            '44bdf456e169c959be199c0030228077a7104c1e',
            'a3771c5794f7677c45b99bc467af7fa87ab26d6d',
            'b9c65c44cca5eab7453ae85ac728e27ae7416b67',
            '6a6f13694db39de9d335e25661138a4f14ccf4ab',
            'f5c7a0e63b18cfaef3aff919f1c74d60719f5747',
            'b854738755e6572c1aec7ca65a16b1030a4c3b53',
            '9596cda701c2d5af036d726e2547db65dfcda134',
            '80fb2958b8e027e2d8a8097bcb7cd4b3bd9bfe13',
            'ac65ce092e906593e512d3452a38c2e5668f8447',
            '47d7dae296e3b5d262e9dca3effad546969670f1',
            '',
            '',
            '',
        ]
        for encoding, tag in zip(ENCODING_KEYS, tags):
            actual = encoding_to_tag(encoding)
            self.assertEqual(actual, tag)

    def test_encoding_to_teamid(self):
        teamids = [
            '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41',
            '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52',
            '53', '54', '55', '56', '57', '58', '59', '60', '', '', ''
        ]
        for encoding, teamid in zip(ENCODING_KEYS, teamids):
            actual = encoding_to_teamid(encoding)
            self.assertEqual(actual, teamid)

    def test_encoding_keys(self):
        actual = encoding_keys()
        self.assertEqual(actual, ENCODING_KEYS)

    def test_icon_absolute(self):
        actual = icon_absolute('T35', 'Chicago', '20')
        src = ('https://fairylab.surge.sh/images/teams/whitesox/whitesox-icon.'
               'png')
        img = ('<img src="{}" width="20" height="20" border="0" class="positio'
               'n-absolute left-8p top-14p">').format(src)
        span = ('<span class="d-block text-truncate pl-24p">Chicago</span>')
        expected = img + span
        self.assertEqual(actual, expected)

    def test_icon_badge__active_false(self):
        actual = icon_badge('T35', '0-0', False, '20')
        badge = ('<span class="badge badge-icon badge-light">{}</span>')
        src = ('https://fairylab.surge.sh/images/teams/whitesox/whitesox-icon.'
               'png')
        img = ('<img src="{}" width="20" height="20" border="0" class="d-inlin'
               'e-block grayscale">').format(src)
        span = ('<span class="d-inline-block align-middle px-2 pt-1 text-secon'
                'dary">0-0</span>')
        expected = badge.format(img + span)
        self.assertEqual(actual, expected)

    def test_icon_badge__active_question(self):
        actual = icon_badge('T35', '0-0', True, '20')
        badge = ('<span class="badge badge-icon badge-light" data-toggle="moda'
                 'l" data-target="#35">{}</span>')
        src = ('https://fairylab.surge.sh/images/teams/whitesox/whitesox-icon.'
               'png')
        img = ('<img src="{}" width="20" height="20" border="0" class="d-inlin'
               'e-block">').format(src)
        span = '<span class="d-inline-block align-middle px-2 pt-1">?-?</span>'
        expected = badge.format(img + span)
        self.assertEqual(actual, expected)

    def test_icon_badge__active_true(self):
        actual = icon_badge('T35', '1-0', True, '20')
        badge = ('<span class="badge badge-icon badge-light" data-toggle="moda'
                 'l" data-target="#35">{}</span>')
        src = ('https://fairylab.surge.sh/images/teams/whitesox/whitesox-icon.'
               'png')
        img = ('<img src="{}" width="20" height="20" border="0" class="d-inlin'
               'e-block">').format(src)
        span = '<span class="d-inline-block align-middle px-2 pt-1">1-0</span>'
        expected = badge.format(img + span)
        self.assertEqual(actual, expected)

    def test_jersey_absolute(self):
        actual = jersey_absolute('T35', WHITE, 'front')
        expected = ('<div class="profile-image position-absolute whitesox-home'
                    '-front"></div>')
        self.assertEqual(actual, expected)

    @mock.patch('common.teams.teams.random.random')
    def test_jersey_color__clash_false(self, mock_random):
        mock_random.return_value = 0.5

        actual = jersey_color('T31', SUNDAY, 'home', BLUE)
        expected = RED
        self.assertEqual(actual, expected)

    @mock.patch('common.teams.teams.random.random')
    def test_jersey_color__clash_true(self, mock_random):
        mock_random.return_value = 0.5

        actual = jersey_color('T31', SUNDAY, 'home', ORANGE)
        expected = WHITE
        self.assertEqual(actual, expected)

    @mock.patch('common.teams.teams.random.random')
    def test_jersey_color__day_false(self, mock_random):
        mock_random.return_value = 0.5

        actual = jersey_color('T31', SATURDAY, 'home', None)
        expected = WHITE
        self.assertEqual(actual, expected)

    @mock.patch('common.teams.teams.random.random')
    def test_jersey_color__day_true(self, mock_random):
        mock_random.return_value = 0.5

        actual = jersey_color('T31', SUNDAY, 'home', None)
        expected = RED
        self.assertEqual(actual, expected)

    @mock.patch('common.teams.teams.random.random')
    def test_jersey_color__pct_false(self, mock_random):
        mock_random.return_value = 0.5

        actual = jersey_color('T37', SUNDAY, 'home', None)
        expected = WHITE
        self.assertEqual(actual, expected)

    @mock.patch('common.teams.teams.random.random')
    def test_jersey_color__pct_true(self, mock_random):
        mock_random.return_value = 0.3

        actual = jersey_color('T37', SUNDAY, 'home', None)
        expected = RED
        self.assertEqual(actual, expected)

    @mock.patch('common.teams.teams.random.random')
    def test_jersey_color__team_false(self, mock_random):
        mock_random.return_value = 0.3

        actual = jersey_color('T37', SUNDAY, 'away', None)
        expected = GREY
        self.assertEqual(actual, expected)

    @mock.patch('common.teams.teams.random.random')
    def test_jersey_color__team_true(self, mock_random):
        mock_random.return_value = 0.3

        actual = jersey_color('T37', SUNDAY, 'home', None)
        expected = RED
        self.assertEqual(actual, expected)

    def test_precoding_to_encoding(self):
        encodings = [
            'T31', 'T32', 'T33', 'T34', 'T37', 'T38', 'T39', 'T40', 'T41',
            'T42', 'T43', 'T46', 'T47', 'T50', 'T51', 'T52', 'T53', 'T54',
            'T55', 'T56', 'T57', 'T58', 'T59', 'T60', 'TCH', 'TLA', 'TNY'
        ]
        for precoding, encoding in zip(PRECODING_KEYS, encodings):
            actual = precoding_to_encoding(precoding)
            self.assertEqual(actual, encoding)

    def test_precoding_to_encoding_sub(self):
        encodings = [
            'T31', 'T32', 'T33', 'T34', 'T37', 'T38', 'T39', 'T40', 'T41',
            'T42', 'T43', 'T46', 'T47', 'T50', 'T51', 'T52', 'T53', 'T54',
            'T55', 'T56', 'T57', 'T58', 'T59', 'T60', 'TCH', 'TLA', 'TNY'
        ]
        actual = precoding_to_encoding_sub(', '.join(PRECODING_KEYS))
        expected = ', '.join(encodings)
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
