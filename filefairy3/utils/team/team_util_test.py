#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/utils/team', '', _path)
sys.path.append(_root)
from utils.team.team_util import _aimg, _aspan, _iimg, _ispan, abbreviation, hometown, nickname, divisions, alogo, ilogo  # noqa


class TeamUtilTest(unittest.TestCase):
    def test_abbreviation(self):
        self.assertEqual(abbreviation('31'), 'ARI')
        self.assertEqual(abbreviation('32'), 'ATL')
        self.assertEqual(abbreviation('33'), 'BAL')
        self.assertEqual(abbreviation('34'), 'BOS')
        self.assertEqual(abbreviation('35'), 'CWS')
        self.assertEqual(abbreviation('36'), 'CHC')
        self.assertEqual(abbreviation('37'), 'CIN')
        self.assertEqual(abbreviation('38'), 'CLE')
        self.assertEqual(abbreviation('39'), 'COL')
        self.assertEqual(abbreviation('40'), 'DET')
        self.assertEqual(abbreviation('41'), 'MIA')
        self.assertEqual(abbreviation('42'), 'HOU')
        self.assertEqual(abbreviation('43'), 'KC')
        self.assertEqual(abbreviation('44'), 'LAA')
        self.assertEqual(abbreviation('45'), 'LAD')
        self.assertEqual(abbreviation('46'), 'MIL')
        self.assertEqual(abbreviation('47'), 'MIN')
        self.assertEqual(abbreviation('48'), 'NYY')
        self.assertEqual(abbreviation('49'), 'NYM')
        self.assertEqual(abbreviation('50'), 'OAK')
        self.assertEqual(abbreviation('51'), 'PHI')
        self.assertEqual(abbreviation('52'), 'PIT')
        self.assertEqual(abbreviation('53'), 'SD')
        self.assertEqual(abbreviation('54'), 'SEA')
        self.assertEqual(abbreviation('55'), 'SF')
        self.assertEqual(abbreviation('56'), 'STL')
        self.assertEqual(abbreviation('57'), 'TB')
        self.assertEqual(abbreviation('58'), 'TEX')
        self.assertEqual(abbreviation('59'), 'TOR')
        self.assertEqual(abbreviation('60'), 'WAS')

    def test_hometown(self):
        self.assertEqual(hometown('31'), 'Arizona')
        self.assertEqual(hometown('32'), 'Atlanta')
        self.assertEqual(hometown('33'), 'Baltimore')
        self.assertEqual(hometown('34'), 'Boston')
        self.assertEqual(hometown('35'), 'Chicago')
        self.assertEqual(hometown('36'), 'Chicago')
        self.assertEqual(hometown('37'), 'Cincinnati')
        self.assertEqual(hometown('38'), 'Cleveland')
        self.assertEqual(hometown('39'), 'Colorado')
        self.assertEqual(hometown('40'), 'Detroit')
        self.assertEqual(hometown('41'), 'Miami')
        self.assertEqual(hometown('42'), 'Houston')
        self.assertEqual(hometown('43'), 'Kansas City')
        self.assertEqual(hometown('44'), 'Los Angeles')
        self.assertEqual(hometown('45'), 'Los Angeles')
        self.assertEqual(hometown('46'), 'Milwaukee')
        self.assertEqual(hometown('47'), 'Minnesota')
        self.assertEqual(hometown('48'), 'New York')
        self.assertEqual(hometown('49'), 'New York')
        self.assertEqual(hometown('50'), 'Oakland')
        self.assertEqual(hometown('51'), 'Philadelphia')
        self.assertEqual(hometown('52'), 'Pittsburgh')
        self.assertEqual(hometown('53'), 'San Diego')
        self.assertEqual(hometown('54'), 'Seattle')
        self.assertEqual(hometown('55'), 'San Francisco')
        self.assertEqual(hometown('56'), 'St. Louis')
        self.assertEqual(hometown('57'), 'Tampa Bay')
        self.assertEqual(hometown('58'), 'Texas')
        self.assertEqual(hometown('59'), 'Toronto')
        self.assertEqual(hometown('60'), 'Washington')

    def test_nickname(self):
        self.assertEqual(nickname('31'), 'Diamondbacks')
        self.assertEqual(nickname('32'), 'Braves')
        self.assertEqual(nickname('33'), 'Orioles')
        self.assertEqual(nickname('34'), 'Red Sox')
        self.assertEqual(nickname('35'), 'White Sox')
        self.assertEqual(nickname('36'), 'Cubs')
        self.assertEqual(nickname('37'), 'Reds')
        self.assertEqual(nickname('38'), 'Indians')
        self.assertEqual(nickname('39'), 'Rockies')
        self.assertEqual(nickname('40'), 'Tigers')
        self.assertEqual(nickname('41'), 'Marlins')
        self.assertEqual(nickname('42'), 'Astros')
        self.assertEqual(nickname('43'), 'Royals')
        self.assertEqual(nickname('44'), 'Angels')
        self.assertEqual(nickname('45'), 'Dodgers')
        self.assertEqual(nickname('46'), 'Brewers')
        self.assertEqual(nickname('47'), 'Twins')
        self.assertEqual(nickname('48'), 'Yankees')
        self.assertEqual(nickname('49'), 'Mets')
        self.assertEqual(nickname('50'), 'Athletics')
        self.assertEqual(nickname('51'), 'Phillies')
        self.assertEqual(nickname('52'), 'Pirates')
        self.assertEqual(nickname('53'), 'Padres')
        self.assertEqual(nickname('54'), 'Mariners')
        self.assertEqual(nickname('55'), 'Giants')
        self.assertEqual(nickname('56'), 'Cardinals')
        self.assertEqual(nickname('57'), 'Rays')
        self.assertEqual(nickname('58'), 'Rangers')
        self.assertEqual(nickname('59'), 'Blue Jays')
        self.assertEqual(nickname('60'), 'Nationals')

    def test_divisions(self):
        actual = divisions()
        expected = [
            ('AL East', ('33', '34', '48', '57', '59')),
            ('AL Central', ('35', '38', '40', '43', '47')),
            ('AL West', ('42', '44', '50', '54', '58')),
            ('NL East', ('32', '41', '49', '51', '60')),
            ('NL Central', ('36', '37', '46', '52', '56')),
            ('NL West', ('31', '39', '45', '53', '55')),
        ]
        self.assertEqual(actual, expected)

    def test_logo(self):
        actual = alogo('31', 'Arizona', 'left')
        img = _aimg.format('arizona_diamondbacks', 'left')
        span = _aspan.format('l', 'Arizona')
        expected = img + span
        self.assertEqual(actual, expected)

        actual = ilogo('31', 'Arizona')
        img = _iimg.format('arizona_diamondbacks')
        span = _ispan.format('Arizona')
        expected = img + span
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
