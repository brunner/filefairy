#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/utils/team', '', _path)
sys.path.append(_root)
from utils.team.team_util import full_name  # noqa


class TeamUtilTest(unittest.TestCase):
    def test_full_name(self):
        self.assertEqual(full_name('31'), 'Arizona Diamondbacks')
        self.assertEqual(full_name('32'), 'Atlanta Braves')
        self.assertEqual(full_name('33'), 'Baltimore Orioles')
        self.assertEqual(full_name('34'), 'Boston Red Sox')
        self.assertEqual(full_name('35'), 'Chicago White Sox')
        self.assertEqual(full_name('36'), 'Chicago Cubs')
        self.assertEqual(full_name('37'), 'Cincinnati Reds')
        self.assertEqual(full_name('38'), 'Cleveland Indians')
        self.assertEqual(full_name('39'), 'Colorado Rockies')
        self.assertEqual(full_name('40'), 'Detroit Tigers')
        self.assertEqual(full_name('41'), 'Miami Marlins')
        self.assertEqual(full_name('42'), 'Houston Astros')
        self.assertEqual(full_name('43'), 'Kansas City Royals')
        self.assertEqual(full_name('44'), 'Los Angeles Angels')
        self.assertEqual(full_name('45'), 'Los Angeles Dodgers')
        self.assertEqual(full_name('46'), 'Milwaukee Brewers')
        self.assertEqual(full_name('47'), 'Minnesota Twins')
        self.assertEqual(full_name('48'), 'New York Yankees')
        self.assertEqual(full_name('49'), 'New York Mets')
        self.assertEqual(full_name('50'), 'Oakland Athletics')
        self.assertEqual(full_name('51'), 'Philadelphia Phillies')
        self.assertEqual(full_name('52'), 'Pittsburgh Pirates')
        self.assertEqual(full_name('53'), 'San Diego Padres')
        self.assertEqual(full_name('54'), 'Seattle Mariners')
        self.assertEqual(full_name('55'), 'San Francisco Giants')
        self.assertEqual(full_name('56'), 'St. Louis Cardinals')
        self.assertEqual(full_name('57'), 'Tampa Bay Rays')
        self.assertEqual(full_name('58'), 'Texas Rangers')
        self.assertEqual(full_name('59'), 'Toronto Blue Jays')
        self.assertEqual(full_name('60'), 'Washington Nationals')


if __name__ == '__main__':
    unittest.main()
