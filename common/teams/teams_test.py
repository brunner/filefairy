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

from common.elements.elements import ruleset  # noqa
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
from common.teams.teams import encoding_to_nickname  # noqa
from common.teams.teams import encoding_to_teamid  # noqa
from common.teams.teams import icon_absolute  # noqa
from common.teams.teams import icon_badge  # noqa
from common.teams.teams import jersey_absolute  # noqa
from common.teams.teams import jersey_color  # noqa
from common.teams.teams import jersey_style  # noqa
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
        expected = ('<div class="jersey-base position-absolute whitesox-home-f'
                    'ront"></div>')
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

    maxDiff = None

    def test_jersey_style(self):
        fairylab = 'https://fairylab.surge.sh/images/teams'
        gist = 'https://gistcdn.githack.com/brunner'
        grad = 'linear-gradient(transparent, transparent)'
        back35 = 'whitesox-alt-blue-back'
        front35 = 'whitesox-alt-blue-front'
        lower35 = 'whitesox'
        raw35 = ('359d34636fabc914a83a8c746fc6eba9/raw/1afa211b3cec808c7d58863'
                 'fd61d436bbdbe05da')
        back37 = 'reds-home-back'
        front37 = 'reds-home-front'
        lower37 = 'reds'
        raw37 = ('af532f33900c377ea6a7d5c373a9785f/raw/8eb50b108f9f65dfcc71b30'
                 'ddb3b9ab032a972c1')

        actual = jersey_style(('T35', BLUE), ('T37', WHITE))
        expected = [
            ruleset('.' + back35, [
                'background: url(\'{}/{}/{}.png\')'.format(
                    fairylab, lower35, back35),
                'background: url(\'{}/{}/{}.svg\'), {}'.format(
                    gist, raw35, back35, grad)
            ]),
            ruleset('.' + front35, [
                'background: url(\'{}/{}/{}.png\')'.format(
                    fairylab, lower35, front35),
                'background: url(\'{}/{}/{}.svg\'), {}'.format(
                    gist, raw35, front35, grad)
            ]),
            ruleset('.' + back37, [
                'background: url(\'{}/{}/{}.png\')'.format(
                    fairylab, lower37, back37),
                'background: url(\'{}/{}/{}.svg\'), {}'.format(
                    gist, raw37, back37, grad)
            ]),
            ruleset('.' + front37, [
                'background: url(\'{}/{}/{}.png\')'.format(
                    fairylab, lower37, front37),
                'background: url(\'{}/{}/{}.svg\'), {}'.format(
                    gist, raw37, front37, grad)
            ]),
            ruleset('.jersey-base', [
                'background-size: 78px 80px',
                'border: 1px solid #eeeff0',
                'height: 82px',
                'margin: -5px -1px -5px -5px',
                'width: 80px',
            ])
        ]
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
