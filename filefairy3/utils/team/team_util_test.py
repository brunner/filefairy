#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/utils/team', '', _path)
sys.path.append(_root)
from utils.team.team_util import abbreviation, hometown, nickname, divisions, logo  # noqa


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
        _logo = '<img src="https://orangeandblueleaguebaseball.com/' + \
                'StatsLab/reports/news/html/images/team_logos/{}_40.png" ' + \
                'width="20" height="20" border="0" class="d-inline-block">'

        self.assertEqual(logo('31'), _logo.format('arizona_diamondbacks'))
        self.assertEqual(logo('32'), _logo.format('atlanta_braves'))
        self.assertEqual(logo('33'), _logo.format('baltimore_orioles'))
        self.assertEqual(logo('34'), _logo.format('boston_red_sox'))
        self.assertEqual(logo('35'), _logo.format('chicago_white_sox'))
        self.assertEqual(logo('36'), _logo.format('chicago_cubs'))
        self.assertEqual(logo('37'), _logo.format('cincinnati_reds'))
        self.assertEqual(logo('38'), _logo.format('cleveland_indians'))
        self.assertEqual(logo('39'), _logo.format('colorado_rockies'))
        self.assertEqual(logo('40'), _logo.format('detroit_tigers'))
        self.assertEqual(logo('41'), _logo.format('miami_marlins'))
        self.assertEqual(logo('42'), _logo.format('houston_astros'))
        self.assertEqual(logo('43'), _logo.format('kansas_city_royals'))
        self.assertEqual(logo('44'), _logo.format('los_angeles_angels'))
        self.assertEqual(logo('45'), _logo.format('los_angeles_dodgers'))
        self.assertEqual(logo('46'), _logo.format('milwaukee_brewers'))
        self.assertEqual(logo('47'), _logo.format('minnesota_twins'))
        self.assertEqual(logo('48'), _logo.format('new_york_yankees'))
        self.assertEqual(logo('49'), _logo.format('new_york_mets'))
        self.assertEqual(logo('50'), _logo.format('oakland_athletics'))
        self.assertEqual(
            logo('51'), _logo.format('philadelphia_phillies'))
        self.assertEqual(logo('52'), _logo.format('pittsburgh_pirates'))
        self.assertEqual(logo('53'), _logo.format('san_diego_padres'))
        self.assertEqual(logo('54'), _logo.format('seattle_mariners'))
        self.assertEqual(logo('55'), _logo.format('san_francisco_giants'))
        self.assertEqual(logo('56'), _logo.format('st_louis_cardinals'))
        self.assertEqual(logo('57'), _logo.format('tampa_bay_rays'))
        self.assertEqual(logo('58'), _logo.format('texas_rangers'))
        self.assertEqual(logo('59'), _logo.format('toronto_blue_jays'))
        self.assertEqual(logo('60'), _logo.format('washington_nationals'))


if __name__ == '__main__':
    unittest.main()
