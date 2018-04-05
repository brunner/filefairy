#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/utils/team', '', _path)
sys.path.append(_root)
from utils.team.team_util import abbreviation, divisions  # noqa


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


if __name__ == '__main__':
    unittest.main()
