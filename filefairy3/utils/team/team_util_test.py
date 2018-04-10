#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/utils/team', '', _path)
sys.path.append(_root)
from utils.team.team_util import _img_24, abbreviation, divisions, logo_24  # noqa


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

    def test_logo_24(self):
        self.assertEqual(logo_24('31'), _img_24.format('arizona_diamondbacks'))
        self.assertEqual(logo_24('32'), _img_24.format('atlanta_braves'))
        self.assertEqual(logo_24('33'), _img_24.format('baltimore_orioles'))
        self.assertEqual(logo_24('34'), _img_24.format('boston_red_sox'))
        self.assertEqual(logo_24('35'), _img_24.format('chicago_white_sox'))
        self.assertEqual(logo_24('36'), _img_24.format('chicago_cubs'))
        self.assertEqual(logo_24('37'), _img_24.format('cincinnati_reds'))
        self.assertEqual(logo_24('38'), _img_24.format('cleveland_indians'))
        self.assertEqual(logo_24('39'), _img_24.format('colorado_rockies'))
        self.assertEqual(logo_24('40'), _img_24.format('detroit_tigers'))
        self.assertEqual(logo_24('41'), _img_24.format('miami_marlins'))
        self.assertEqual(logo_24('42'), _img_24.format('houston_astros'))
        self.assertEqual(logo_24('43'), _img_24.format('kansas_city_royals'))
        self.assertEqual(logo_24('44'), _img_24.format('los_angeles_angels'))
        self.assertEqual(logo_24('45'), _img_24.format('los_angeles_dodgers'))
        self.assertEqual(logo_24('46'), _img_24.format('milwaukee_brewers'))
        self.assertEqual(logo_24('47'), _img_24.format('minnesota_twins'))
        self.assertEqual(logo_24('48'), _img_24.format('new_york_yankees'))
        self.assertEqual(logo_24('49'), _img_24.format('new_york_mets'))
        self.assertEqual(logo_24('50'), _img_24.format('oakland_athletics'))
        self.assertEqual(
            logo_24('51'), _img_24.format('philadelphia_phillies'))
        self.assertEqual(logo_24('52'), _img_24.format('pittsburgh_pirates'))
        self.assertEqual(logo_24('53'), _img_24.format('san_diego_padres'))
        self.assertEqual(logo_24('54'), _img_24.format('seattle_mariners'))
        self.assertEqual(logo_24('55'), _img_24.format('san_francisco_giants'))
        self.assertEqual(logo_24('56'), _img_24.format('st_louis_cardinals'))
        self.assertEqual(logo_24('57'), _img_24.format('tampa_bay_rays'))
        self.assertEqual(logo_24('58'), _img_24.format('texas_rangers'))
        self.assertEqual(logo_24('59'), _img_24.format('toronto_blue_jays'))
        self.assertEqual(logo_24('60'), _img_24.format('washington_nationals'))


if __name__ == '__main__':
    unittest.main()
