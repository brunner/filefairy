#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/utils/team', '', _path)
sys.path.append(_root)
from utils.team.team_util import _aimg  # noqa
from utils.team.team_util import _aspan  # noqa
from utils.team.team_util import _iimg  # noqa
from utils.team.team_util import _ispan  # noqa
from utils.team.team_util import abbreviation_by_teamid  # noqa
from utils.team.team_util import alogo  # noqa
from utils.team.team_util import divisions  # noqa
from utils.team.team_util import hometown_by_teamid  # noqa
from utils.team.team_util import hometowns  # noqa
from utils.team.team_util import ilogo  # noqa
from utils.team.team_util import nickname_by_hometown  # noqa
from utils.team.team_util import nickname_by_teamid  # noqa
from utils.team.team_util import teamid_by_hometown  # noqa


class TeamUtilTest(unittest.TestCase):
    def test_abbreviation_by_teamid_by_teamid(self):
        self.assertEqual(abbreviation_by_teamid('31'), 'ARI')
        self.assertEqual(abbreviation_by_teamid('32'), 'ATL')
        self.assertEqual(abbreviation_by_teamid('33'), 'BAL')
        self.assertEqual(abbreviation_by_teamid('34'), 'BOS')
        self.assertEqual(abbreviation_by_teamid('35'), 'CWS')
        self.assertEqual(abbreviation_by_teamid('36'), 'CHC')
        self.assertEqual(abbreviation_by_teamid('37'), 'CIN')
        self.assertEqual(abbreviation_by_teamid('38'), 'CLE')
        self.assertEqual(abbreviation_by_teamid('39'), 'COL')
        self.assertEqual(abbreviation_by_teamid('40'), 'DET')
        self.assertEqual(abbreviation_by_teamid('41'), 'MIA')
        self.assertEqual(abbreviation_by_teamid('42'), 'HOU')
        self.assertEqual(abbreviation_by_teamid('43'), 'KC')
        self.assertEqual(abbreviation_by_teamid('44'), 'LAA')
        self.assertEqual(abbreviation_by_teamid('45'), 'LAD')
        self.assertEqual(abbreviation_by_teamid('46'), 'MIL')
        self.assertEqual(abbreviation_by_teamid('47'), 'MIN')
        self.assertEqual(abbreviation_by_teamid('48'), 'NYY')
        self.assertEqual(abbreviation_by_teamid('49'), 'NYM')
        self.assertEqual(abbreviation_by_teamid('50'), 'OAK')
        self.assertEqual(abbreviation_by_teamid('51'), 'PHI')
        self.assertEqual(abbreviation_by_teamid('52'), 'PIT')
        self.assertEqual(abbreviation_by_teamid('53'), 'SD')
        self.assertEqual(abbreviation_by_teamid('54'), 'SEA')
        self.assertEqual(abbreviation_by_teamid('55'), 'SF')
        self.assertEqual(abbreviation_by_teamid('56'), 'STL')
        self.assertEqual(abbreviation_by_teamid('57'), 'TB')
        self.assertEqual(abbreviation_by_teamid('58'), 'TEX')
        self.assertEqual(abbreviation_by_teamid('59'), 'TOR')
        self.assertEqual(abbreviation_by_teamid('60'), 'WAS')

    def test_hometown_by_teamid(self):
        self.assertEqual(hometown_by_teamid('31'), 'Arizona')
        self.assertEqual(hometown_by_teamid('32'), 'Atlanta')
        self.assertEqual(hometown_by_teamid('33'), 'Baltimore')
        self.assertEqual(hometown_by_teamid('34'), 'Boston')
        self.assertEqual(hometown_by_teamid('35'), 'Chicago')
        self.assertEqual(hometown_by_teamid('36'), 'Chicago')
        self.assertEqual(hometown_by_teamid('37'), 'Cincinnati')
        self.assertEqual(hometown_by_teamid('38'), 'Cleveland')
        self.assertEqual(hometown_by_teamid('39'), 'Colorado')
        self.assertEqual(hometown_by_teamid('40'), 'Detroit')
        self.assertEqual(hometown_by_teamid('41'), 'Miami')
        self.assertEqual(hometown_by_teamid('42'), 'Houston')
        self.assertEqual(hometown_by_teamid('43'), 'Kansas City')
        self.assertEqual(hometown_by_teamid('44'), 'Los Angeles')
        self.assertEqual(hometown_by_teamid('45'), 'Los Angeles')
        self.assertEqual(hometown_by_teamid('46'), 'Milwaukee')
        self.assertEqual(hometown_by_teamid('47'), 'Minnesota')
        self.assertEqual(hometown_by_teamid('48'), 'New York')
        self.assertEqual(hometown_by_teamid('49'), 'New York')
        self.assertEqual(hometown_by_teamid('50'), 'Oakland')
        self.assertEqual(hometown_by_teamid('51'), 'Philadelphia')
        self.assertEqual(hometown_by_teamid('52'), 'Pittsburgh')
        self.assertEqual(hometown_by_teamid('53'), 'San Diego')
        self.assertEqual(hometown_by_teamid('54'), 'Seattle')
        self.assertEqual(hometown_by_teamid('55'), 'San Francisco')
        self.assertEqual(hometown_by_teamid('56'), 'St. Louis')
        self.assertEqual(hometown_by_teamid('57'), 'Tampa Bay')
        self.assertEqual(hometown_by_teamid('58'), 'Texas')
        self.assertEqual(hometown_by_teamid('59'), 'Toronto')
        self.assertEqual(hometown_by_teamid('60'), 'Washington')

    def test_nickname_by_teamid(self):
        self.assertEqual(nickname_by_teamid('31'), 'Diamondbacks')
        self.assertEqual(nickname_by_teamid('32'), 'Braves')
        self.assertEqual(nickname_by_teamid('33'), 'Orioles')
        self.assertEqual(nickname_by_teamid('34'), 'Red Sox')
        self.assertEqual(nickname_by_teamid('35'), 'White Sox')
        self.assertEqual(nickname_by_teamid('36'), 'Cubs')
        self.assertEqual(nickname_by_teamid('37'), 'Reds')
        self.assertEqual(nickname_by_teamid('38'), 'Indians')
        self.assertEqual(nickname_by_teamid('39'), 'Rockies')
        self.assertEqual(nickname_by_teamid('40'), 'Tigers')
        self.assertEqual(nickname_by_teamid('41'), 'Marlins')
        self.assertEqual(nickname_by_teamid('42'), 'Astros')
        self.assertEqual(nickname_by_teamid('43'), 'Royals')
        self.assertEqual(nickname_by_teamid('44'), 'Angels')
        self.assertEqual(nickname_by_teamid('45'), 'Dodgers')
        self.assertEqual(nickname_by_teamid('46'), 'Brewers')
        self.assertEqual(nickname_by_teamid('47'), 'Twins')
        self.assertEqual(nickname_by_teamid('48'), 'Yankees')
        self.assertEqual(nickname_by_teamid('49'), 'Mets')
        self.assertEqual(nickname_by_teamid('50'), 'Athletics')
        self.assertEqual(nickname_by_teamid('51'), 'Phillies')
        self.assertEqual(nickname_by_teamid('52'), 'Pirates')
        self.assertEqual(nickname_by_teamid('53'), 'Padres')
        self.assertEqual(nickname_by_teamid('54'), 'Mariners')
        self.assertEqual(nickname_by_teamid('55'), 'Giants')
        self.assertEqual(nickname_by_teamid('56'), 'Cardinals')
        self.assertEqual(nickname_by_teamid('57'), 'Rays')
        self.assertEqual(nickname_by_teamid('58'), 'Rangers')
        self.assertEqual(nickname_by_teamid('59'), 'Blue Jays')
        self.assertEqual(nickname_by_teamid('60'), 'Nationals')

    def test_teamid_by_hometown(self):
        self.assertEqual(teamid_by_hometown('Arizona'), '31')
        self.assertEqual(teamid_by_hometown('Atlanta'), '32')
        self.assertEqual(teamid_by_hometown('Baltimore'), '33')
        self.assertEqual(teamid_by_hometown('Boston'), '34')
        self.assertEqual(teamid_by_hometown('Chicago'), '')
        self.assertEqual(teamid_by_hometown('Cincinnati'), '37')
        self.assertEqual(teamid_by_hometown('Cleveland'), '38')
        self.assertEqual(teamid_by_hometown('Colorado'), '39')
        self.assertEqual(teamid_by_hometown('Detroit'), '40')
        self.assertEqual(teamid_by_hometown('Miami'), '41')
        self.assertEqual(teamid_by_hometown('Houston'), '42')
        self.assertEqual(teamid_by_hometown('Kansas City'), '43')
        self.assertEqual(teamid_by_hometown('Los Angeles'), '')
        self.assertEqual(teamid_by_hometown('Milwaukee'), '46')
        self.assertEqual(teamid_by_hometown('Minnesota'), '47')
        self.assertEqual(teamid_by_hometown('New York'), '')
        self.assertEqual(teamid_by_hometown('Oakland'), '50')
        self.assertEqual(teamid_by_hometown('Philadelphia'), '51')
        self.assertEqual(teamid_by_hometown('Pittsburgh'), '52')
        self.assertEqual(teamid_by_hometown('San Diego'), '53')
        self.assertEqual(teamid_by_hometown('Seattle'), '54')
        self.assertEqual(teamid_by_hometown('San Francisco'), '55')
        self.assertEqual(teamid_by_hometown('St. Louis'), '56')
        self.assertEqual(teamid_by_hometown('Tampa Bay'), '57')
        self.assertEqual(teamid_by_hometown('Texas'), '58')
        self.assertEqual(teamid_by_hometown('Toronto'), '59')
        self.assertEqual(teamid_by_hometown('Washington'), '60')

    def test_nickname_by_hometown(self):
        self.assertEqual(nickname_by_hometown('Arizona'), 'Diamondbacks')
        self.assertEqual(nickname_by_hometown('Atlanta'), 'Braves')
        self.assertEqual(nickname_by_hometown('Baltimore'), 'Orioles')
        self.assertEqual(nickname_by_hometown('Boston'), 'Red Sox')
        self.assertEqual(nickname_by_hometown('Chicago'), '')
        self.assertEqual(nickname_by_hometown('Cincinnati'), 'Reds')
        self.assertEqual(nickname_by_hometown('Cleveland'), 'Indians')
        self.assertEqual(nickname_by_hometown('Colorado'), 'Rockies')
        self.assertEqual(nickname_by_hometown('Detroit'), 'Tigers')
        self.assertEqual(nickname_by_hometown('Miami'), 'Marlins')
        self.assertEqual(nickname_by_hometown('Houston'), 'Astros')
        self.assertEqual(nickname_by_hometown('Kansas City'), 'Royals')
        self.assertEqual(nickname_by_hometown('Los Angeles'), '')
        self.assertEqual(nickname_by_hometown('Milwaukee'), 'Brewers')
        self.assertEqual(nickname_by_hometown('Minnesota'), 'Twins')
        self.assertEqual(nickname_by_hometown('New York'), '')
        self.assertEqual(nickname_by_hometown('Oakland'), 'Athletics')
        self.assertEqual(nickname_by_hometown('Philadelphia'), 'Phillies')
        self.assertEqual(nickname_by_hometown('Pittsburgh'), 'Pirates')
        self.assertEqual(nickname_by_hometown('San Diego'), 'Padres')
        self.assertEqual(nickname_by_hometown('Seattle'), 'Mariners')
        self.assertEqual(nickname_by_hometown('San Francisco'), 'Giants')
        self.assertEqual(nickname_by_hometown('St. Louis'), 'Cardinals')
        self.assertEqual(nickname_by_hometown('Tampa Bay'), 'Rays')
        self.assertEqual(nickname_by_hometown('Texas'), 'Rangers')
        self.assertEqual(nickname_by_hometown('Toronto'), 'Blue Jays')
        self.assertEqual(nickname_by_hometown('Washington'), 'Nationals')

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

    def test_hometowns(self):
        actual = sorted(hometowns())
        expected = [
            'Arizona', 'Atlanta', 'Baltimore', 'Boston', 'Chicago',
            'Cincinnati', 'Cleveland', 'Colorado', 'Detroit', 'Houston',
            'Kansas City', 'Los Angeles', 'Miami', 'Milwaukee', 'Minnesota',
            'New York', 'Oakland', 'Philadelphia', 'Pittsburgh', 'San Diego',
            'San Francisco', 'Seattle', 'St. Louis', 'Tampa Bay', 'Texas',
            'Toronto', 'Washington'
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
