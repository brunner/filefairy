#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/util/team', '', _path)
sys.path.append(_root)
from util.team.team import _absolute_img  # noqa
from util.team.team import _absolute_span  # noqa
from util.team.team import _inline_img  # noqa
from util.team.team import _inline_span  # noqa
from util.team.team import chlany  # noqa
from util.team.team import decoding_to_encoding  # noqa
from util.team.team import decoding_to_encoding_sub  # noqa
from util.team.team import decodings  # noqa
from util.team.team import divisions  # noqa
from util.team.team import encoding_to_decoding  # noqa
from util.team.team import encoding_to_decoding_sub  # noqa
from util.team.team import encoding_to_precoding  # noqa
from util.team.team import encoding_to_teamid  # noqa
from util.team.team import encodings  # noqa
from util.team.team import precoding_to_encoding  # noqa
from util.team.team import precoding_to_encoding_sub  # noqa
from util.team.team import precodings  # noqa
from util.team.team import logo_absolute  # noqa
from util.team.team import logo_inline  # noqa
from util.team.team import teamid_to_abbreviation  # noqa
from util.team.team import teamid_to_decoding  # noqa
from util.team.team import teamid_to_encoding  # noqa
from util.team.team import teamid_to_hometown  # noqa

DECODINGS = [
    'Arizona Diamondbacks', 'Atlanta Braves', 'Baltimore Orioles',
    'Boston Red Sox', 'Chicago White Sox', 'Chicago Cubs', 'Cincinnati Reds',
    'Cleveland Indians', 'Colorado Rockies', 'Detroit Tigers', 'Miami Marlins',
    'Houston Astros', 'Kansas City Royals', 'Los Angeles Angels',
    'Los Angeles Dodgers', 'Milwaukee Brewers', 'Minnesota Twins',
    'New York Yankees', 'New York Mets', 'Oakland Athletics',
    'Philadelphia Phillies', 'Pittsburgh Pirates', 'San Diego Padres',
    'Seattle Mariners', 'San Francisco Giants', 'St. Louis Cardinals',
    'Tampa Bay Rays', 'Texas Rangers', 'Toronto Blue Jays',
    'Washington Nationals', 'Chicago', 'Los Angeles', 'New York'
]
DE_ENCODINGS = [
    'T31', 'T32', 'T33', 'T34', 'T35', 'T36', 'T37', 'T38', 'T39', 'T40',
    'T41', 'T42', 'T43', 'T44', 'T45', 'T46', 'T47', 'T48', 'T49', 'T50',
    'T51', 'T52', 'T53', 'T54', 'T55', 'T56', 'T57', 'T58', 'T59', 'T60',
    'TCH', 'TLA', 'TNY'
]
PRE_ENCODINGS = [
    'T31', 'T32', 'T33', 'T34', 'T37', 'T38', 'T39', 'T40', 'T41', 'T42',
    'T43', 'T46', 'T47', 'T50', 'T51', 'T52', 'T53', 'T54', 'T55', 'T56',
    'T57', 'T58', 'T59', 'T60', 'TCH', 'TLA', 'TNY'
]
PRECODINGS = [
    'Arizona', 'Atlanta', 'Baltimore', 'Boston', 'Cincinnati', 'Cleveland',
    'Colorado', 'Detroit', 'Miami', 'Houston', 'Kansas City', 'Milwaukee',
    'Minnesota', 'Oakland', 'Philadelphia', 'Pittsburgh', 'San Diego',
    'Seattle', 'San Francisco', 'St. Louis', 'Tampa Bay', 'Texas', 'Toronto',
    'Washington', 'Chicago', 'Los Angeles', 'New York'
]


class TeamTest(unittest.TestCase):
    def test_chlany(self):
        actual = chlany()
        expected = ['TCH', 'TLA', 'TNY']
        self.assertEqual(actual, expected)

    def test_decoding_to_encoding(self):
        self.assertEqual(decoding_to_encoding('Arizona Diamondbacks'), 'T31')
        self.assertEqual(decoding_to_encoding('Atlanta Braves'), 'T32')
        self.assertEqual(decoding_to_encoding('Baltimore Orioles'), 'T33')
        self.assertEqual(decoding_to_encoding('Boston Red Sox'), 'T34')
        self.assertEqual(decoding_to_encoding('Chicago White Sox'), 'T35')
        self.assertEqual(decoding_to_encoding('Chicago Cubs'), 'T36')
        self.assertEqual(decoding_to_encoding('Cincinnati Reds'), 'T37')
        self.assertEqual(decoding_to_encoding('Cleveland Indians'), 'T38')
        self.assertEqual(decoding_to_encoding('Colorado Rockies'), 'T39')
        self.assertEqual(decoding_to_encoding('Detroit Tigers'), 'T40')
        self.assertEqual(decoding_to_encoding('Miami Marlins'), 'T41')
        self.assertEqual(decoding_to_encoding('Houston Astros'), 'T42')
        self.assertEqual(decoding_to_encoding('Kansas City Royals'), 'T43')
        self.assertEqual(decoding_to_encoding('Los Angeles Angels'), 'T44')
        self.assertEqual(decoding_to_encoding('Los Angeles Dodgers'), 'T45')
        self.assertEqual(decoding_to_encoding('Milwaukee Brewers'), 'T46')
        self.assertEqual(decoding_to_encoding('Minnesota Twins'), 'T47')
        self.assertEqual(decoding_to_encoding('New York Yankees'), 'T48')
        self.assertEqual(decoding_to_encoding('New York Mets'), 'T49')
        self.assertEqual(decoding_to_encoding('Oakland Athletics'), 'T50')
        self.assertEqual(decoding_to_encoding('Philadelphia Phillies'), 'T51')
        self.assertEqual(decoding_to_encoding('Pittsburgh Pirates'), 'T52')
        self.assertEqual(decoding_to_encoding('San Diego Padres'), 'T53')
        self.assertEqual(decoding_to_encoding('Seattle Mariners'), 'T54')
        self.assertEqual(decoding_to_encoding('San Francisco Giants'), 'T55')
        self.assertEqual(decoding_to_encoding('St. Louis Cardinals'), 'T56')
        self.assertEqual(decoding_to_encoding('Tampa Bay Rays'), 'T57')
        self.assertEqual(decoding_to_encoding('Texas Rangers'), 'T58')
        self.assertEqual(decoding_to_encoding('Toronto Blue Jays'), 'T59')
        self.assertEqual(decoding_to_encoding('Washington Nationals'), 'T60')
        self.assertEqual(decoding_to_encoding('Chicago'), 'TCH')
        self.assertEqual(decoding_to_encoding('Los Angeles'), 'TLA')
        self.assertEqual(decoding_to_encoding('New York'), 'TNY')

    def test_decoding_to_encoding_sub(self):
        decodings = ', '.join(DECODINGS)
        encodings = ', '.join(DE_ENCODINGS)
        self.assertEqual(decoding_to_encoding_sub(decodings), encodings)

    def test_decodings(self):
        self.assertEqual(decodings(), DECODINGS)

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

    def test_encoding_to_decoding(self):
        self.assertEqual(encoding_to_decoding('T31'), 'Arizona Diamondbacks')
        self.assertEqual(encoding_to_decoding('T32'), 'Atlanta Braves')
        self.assertEqual(encoding_to_decoding('T33'), 'Baltimore Orioles')
        self.assertEqual(encoding_to_decoding('T34'), 'Boston Red Sox')
        self.assertEqual(encoding_to_decoding('T35'), 'Chicago White Sox')
        self.assertEqual(encoding_to_decoding('T36'), 'Chicago Cubs')
        self.assertEqual(encoding_to_decoding('T37'), 'Cincinnati Reds')
        self.assertEqual(encoding_to_decoding('T38'), 'Cleveland Indians')
        self.assertEqual(encoding_to_decoding('T39'), 'Colorado Rockies')
        self.assertEqual(encoding_to_decoding('T40'), 'Detroit Tigers')
        self.assertEqual(encoding_to_decoding('T41'), 'Miami Marlins')
        self.assertEqual(encoding_to_decoding('T42'), 'Houston Astros')
        self.assertEqual(encoding_to_decoding('T43'), 'Kansas City Royals')
        self.assertEqual(encoding_to_decoding('T44'), 'Los Angeles Angels')
        self.assertEqual(encoding_to_decoding('T45'), 'Los Angeles Dodgers')
        self.assertEqual(encoding_to_decoding('T46'), 'Milwaukee Brewers')
        self.assertEqual(encoding_to_decoding('T47'), 'Minnesota Twins')
        self.assertEqual(encoding_to_decoding('T48'), 'New York Yankees')
        self.assertEqual(encoding_to_decoding('T49'), 'New York Mets')
        self.assertEqual(encoding_to_decoding('T50'), 'Oakland Athletics')
        self.assertEqual(encoding_to_decoding('T51'), 'Philadelphia Phillies')
        self.assertEqual(encoding_to_decoding('T52'), 'Pittsburgh Pirates')
        self.assertEqual(encoding_to_decoding('T53'), 'San Diego Padres')
        self.assertEqual(encoding_to_decoding('T54'), 'Seattle Mariners')
        self.assertEqual(encoding_to_decoding('T55'), 'San Francisco Giants')
        self.assertEqual(encoding_to_decoding('T56'), 'St. Louis Cardinals')
        self.assertEqual(encoding_to_decoding('T57'), 'Tampa Bay Rays')
        self.assertEqual(encoding_to_decoding('T58'), 'Texas Rangers')
        self.assertEqual(encoding_to_decoding('T59'), 'Toronto Blue Jays')
        self.assertEqual(encoding_to_decoding('T60'), 'Washington Nationals')
        self.assertEqual(encoding_to_decoding('TCH'), 'Chicago')
        self.assertEqual(encoding_to_decoding('TLA'), 'Los Angeles')
        self.assertEqual(encoding_to_decoding('TNY'), 'New York')

    def test_encoding_to_decoding_sub(self):
        encodings = ', '.join(DE_ENCODINGS)
        decodings = ', '.join(DECODINGS)
        self.assertEqual(encoding_to_decoding_sub(encodings), decodings)

    def test_encoding_to_precoding(self):
        self.assertEqual(encoding_to_precoding('T31'), 'Arizona')
        self.assertEqual(encoding_to_precoding('T32'), 'Atlanta')
        self.assertEqual(encoding_to_precoding('T33'), 'Baltimore')
        self.assertEqual(encoding_to_precoding('T34'), 'Boston')
        self.assertEqual(encoding_to_precoding('T37'), 'Cincinnati')
        self.assertEqual(encoding_to_precoding('T38'), 'Cleveland')
        self.assertEqual(encoding_to_precoding('T39'), 'Colorado')
        self.assertEqual(encoding_to_precoding('T40'), 'Detroit')
        self.assertEqual(encoding_to_precoding('T41'), 'Miami')
        self.assertEqual(encoding_to_precoding('T42'), 'Houston')
        self.assertEqual(encoding_to_precoding('T43'), 'Kansas City')
        self.assertEqual(encoding_to_precoding('T46'), 'Milwaukee')
        self.assertEqual(encoding_to_precoding('T47'), 'Minnesota')
        self.assertEqual(encoding_to_precoding('T50'), 'Oakland')
        self.assertEqual(encoding_to_precoding('T51'), 'Philadelphia')
        self.assertEqual(encoding_to_precoding('T52'), 'Pittsburgh')
        self.assertEqual(encoding_to_precoding('T53'), 'San Diego')
        self.assertEqual(encoding_to_precoding('T54'), 'Seattle')
        self.assertEqual(encoding_to_precoding('T55'), 'San Francisco')
        self.assertEqual(encoding_to_precoding('T56'), 'St. Louis')
        self.assertEqual(encoding_to_precoding('T57'), 'Tampa Bay')
        self.assertEqual(encoding_to_precoding('T58'), 'Texas')
        self.assertEqual(encoding_to_precoding('T59'), 'Toronto')
        self.assertEqual(encoding_to_precoding('T60'), 'Washington')
        self.assertEqual(encoding_to_precoding('TCH'), 'Chicago')
        self.assertEqual(encoding_to_precoding('TLA'), 'Los Angeles')
        self.assertEqual(encoding_to_precoding('TNY'), 'New York')

    def test_encoding_to_teamid(self):
        self.assertEqual(encoding_to_teamid('T31'), '31')
        self.assertEqual(encoding_to_teamid('T32'), '32')
        self.assertEqual(encoding_to_teamid('T33'), '33')
        self.assertEqual(encoding_to_teamid('T34'), '34')
        self.assertEqual(encoding_to_teamid('T35'), '35')
        self.assertEqual(encoding_to_teamid('T36'), '36')
        self.assertEqual(encoding_to_teamid('T37'), '37')
        self.assertEqual(encoding_to_teamid('T38'), '38')
        self.assertEqual(encoding_to_teamid('T39'), '39')
        self.assertEqual(encoding_to_teamid('T40'), '40')
        self.assertEqual(encoding_to_teamid('T41'), '41')
        self.assertEqual(encoding_to_teamid('T42'), '42')
        self.assertEqual(encoding_to_teamid('T43'), '43')
        self.assertEqual(encoding_to_teamid('T44'), '44')
        self.assertEqual(encoding_to_teamid('T45'), '45')
        self.assertEqual(encoding_to_teamid('T46'), '46')
        self.assertEqual(encoding_to_teamid('T47'), '47')
        self.assertEqual(encoding_to_teamid('T48'), '48')
        self.assertEqual(encoding_to_teamid('T49'), '49')
        self.assertEqual(encoding_to_teamid('T50'), '50')
        self.assertEqual(encoding_to_teamid('T51'), '51')
        self.assertEqual(encoding_to_teamid('T52'), '52')
        self.assertEqual(encoding_to_teamid('T53'), '53')
        self.assertEqual(encoding_to_teamid('T54'), '54')
        self.assertEqual(encoding_to_teamid('T55'), '55')
        self.assertEqual(encoding_to_teamid('T56'), '56')
        self.assertEqual(encoding_to_teamid('T57'), '57')
        self.assertEqual(encoding_to_teamid('T58'), '58')
        self.assertEqual(encoding_to_teamid('T59'), '59')
        self.assertEqual(encoding_to_teamid('T60'), '60')

    def test_encodings(self):
        self.assertEqual(encodings(), DE_ENCODINGS)

    def test_precoding_to_encoding(self):
        self.assertEqual(precoding_to_encoding('Arizona'), 'T31')
        self.assertEqual(precoding_to_encoding('Atlanta'), 'T32')
        self.assertEqual(precoding_to_encoding('Baltimore'), 'T33')
        self.assertEqual(precoding_to_encoding('Boston'), 'T34')
        self.assertEqual(precoding_to_encoding('Cincinnati'), 'T37')
        self.assertEqual(precoding_to_encoding('Cleveland'), 'T38')
        self.assertEqual(precoding_to_encoding('Colorado'), 'T39')
        self.assertEqual(precoding_to_encoding('Detroit'), 'T40')
        self.assertEqual(precoding_to_encoding('Miami'), 'T41')
        self.assertEqual(precoding_to_encoding('Houston'), 'T42')
        self.assertEqual(precoding_to_encoding('Kansas City'), 'T43')
        self.assertEqual(precoding_to_encoding('Milwaukee'), 'T46')
        self.assertEqual(precoding_to_encoding('Minnesota'), 'T47')
        self.assertEqual(precoding_to_encoding('Oakland'), 'T50')
        self.assertEqual(precoding_to_encoding('Philadelphia'), 'T51')
        self.assertEqual(precoding_to_encoding('Pittsburgh'), 'T52')
        self.assertEqual(precoding_to_encoding('San Diego'), 'T53')
        self.assertEqual(precoding_to_encoding('Seattle'), 'T54')
        self.assertEqual(precoding_to_encoding('San Francisco'), 'T55')
        self.assertEqual(precoding_to_encoding('St. Louis'), 'T56')
        self.assertEqual(precoding_to_encoding('Tampa Bay'), 'T57')
        self.assertEqual(precoding_to_encoding('Texas'), 'T58')
        self.assertEqual(precoding_to_encoding('Toronto'), 'T59')
        self.assertEqual(precoding_to_encoding('Washington'), 'T60')
        self.assertEqual(precoding_to_encoding('Chicago'), 'TCH')
        self.assertEqual(precoding_to_encoding('Los Angeles'), 'TLA')
        self.assertEqual(precoding_to_encoding('New York'), 'TNY')

    def test_precodings(self):
        self.assertEqual(precodings(), PRECODINGS)

    def test_precoding_to_encoding_sub(self):
        precodings = ', '.join(PRECODINGS)
        encodings = ', '.join(PRE_ENCODINGS)
        self.assertEqual(precoding_to_encoding_sub(precodings), encodings)

    def test_logo_absolute(self):
        actual = logo_absolute('31', 'Arizona', 'left')
        img = _absolute_img.format('arizona_diamondbacks', 'left')
        span = _absolute_span.format('l', 'Arizona')
        expected = img + span
        self.assertEqual(actual, expected)

    def test_logo_inline(self):
        actual = logo_inline('31', 'Arizona')
        img = _inline_img.format('arizona_diamondbacks')
        span = _inline_span.format('Arizona')
        expected = img + span
        self.assertEqual(actual, expected)

    def test_teamid_to_abbreviation(self):
        self.assertEqual(teamid_to_abbreviation('31'), 'ARI')
        self.assertEqual(teamid_to_abbreviation('32'), 'ATL')
        self.assertEqual(teamid_to_abbreviation('33'), 'BAL')
        self.assertEqual(teamid_to_abbreviation('34'), 'BOS')
        self.assertEqual(teamid_to_abbreviation('35'), 'CWS')
        self.assertEqual(teamid_to_abbreviation('36'), 'CHC')
        self.assertEqual(teamid_to_abbreviation('37'), 'CIN')
        self.assertEqual(teamid_to_abbreviation('38'), 'CLE')
        self.assertEqual(teamid_to_abbreviation('39'), 'COL')
        self.assertEqual(teamid_to_abbreviation('40'), 'DET')
        self.assertEqual(teamid_to_abbreviation('41'), 'MIA')
        self.assertEqual(teamid_to_abbreviation('42'), 'HOU')
        self.assertEqual(teamid_to_abbreviation('43'), 'KC')
        self.assertEqual(teamid_to_abbreviation('44'), 'LAA')
        self.assertEqual(teamid_to_abbreviation('45'), 'LAD')
        self.assertEqual(teamid_to_abbreviation('46'), 'MIL')
        self.assertEqual(teamid_to_abbreviation('47'), 'MIN')
        self.assertEqual(teamid_to_abbreviation('48'), 'NYY')
        self.assertEqual(teamid_to_abbreviation('49'), 'NYM')
        self.assertEqual(teamid_to_abbreviation('50'), 'OAK')
        self.assertEqual(teamid_to_abbreviation('51'), 'PHI')
        self.assertEqual(teamid_to_abbreviation('52'), 'PIT')
        self.assertEqual(teamid_to_abbreviation('53'), 'SD')
        self.assertEqual(teamid_to_abbreviation('54'), 'SEA')
        self.assertEqual(teamid_to_abbreviation('55'), 'SF')
        self.assertEqual(teamid_to_abbreviation('56'), 'STL')
        self.assertEqual(teamid_to_abbreviation('57'), 'TB')
        self.assertEqual(teamid_to_abbreviation('58'), 'TEX')
        self.assertEqual(teamid_to_abbreviation('59'), 'TOR')
        self.assertEqual(teamid_to_abbreviation('60'), 'WAS')

    def test_teamid_to_decoding(self):
        self.assertEqual(teamid_to_decoding('31'), 'Arizona Diamondbacks')
        self.assertEqual(teamid_to_decoding('32'), 'Atlanta Braves')
        self.assertEqual(teamid_to_decoding('33'), 'Baltimore Orioles')
        self.assertEqual(teamid_to_decoding('34'), 'Boston Red Sox')
        self.assertEqual(teamid_to_decoding('35'), 'Chicago White Sox')
        self.assertEqual(teamid_to_decoding('36'), 'Chicago Cubs')
        self.assertEqual(teamid_to_decoding('37'), 'Cincinnati Reds')
        self.assertEqual(teamid_to_decoding('38'), 'Cleveland Indians')
        self.assertEqual(teamid_to_decoding('39'), 'Colorado Rockies')
        self.assertEqual(teamid_to_decoding('40'), 'Detroit Tigers')
        self.assertEqual(teamid_to_decoding('41'), 'Miami Marlins')
        self.assertEqual(teamid_to_decoding('42'), 'Houston Astros')
        self.assertEqual(teamid_to_decoding('43'), 'Kansas City Royals')
        self.assertEqual(teamid_to_decoding('44'), 'Los Angeles Angels')
        self.assertEqual(teamid_to_decoding('45'), 'Los Angeles Dodgers')
        self.assertEqual(teamid_to_decoding('46'), 'Milwaukee Brewers')
        self.assertEqual(teamid_to_decoding('47'), 'Minnesota Twins')
        self.assertEqual(teamid_to_decoding('48'), 'New York Yankees')
        self.assertEqual(teamid_to_decoding('49'), 'New York Mets')
        self.assertEqual(teamid_to_decoding('50'), 'Oakland Athletics')
        self.assertEqual(teamid_to_decoding('51'), 'Philadelphia Phillies')
        self.assertEqual(teamid_to_decoding('52'), 'Pittsburgh Pirates')
        self.assertEqual(teamid_to_decoding('53'), 'San Diego Padres')
        self.assertEqual(teamid_to_decoding('54'), 'Seattle Mariners')
        self.assertEqual(teamid_to_decoding('55'), 'San Francisco Giants')
        self.assertEqual(teamid_to_decoding('56'), 'St. Louis Cardinals')
        self.assertEqual(teamid_to_decoding('57'), 'Tampa Bay Rays')
        self.assertEqual(teamid_to_decoding('58'), 'Texas Rangers')
        self.assertEqual(teamid_to_decoding('59'), 'Toronto Blue Jays')
        self.assertEqual(teamid_to_decoding('60'), 'Washington Nationals')

    def test_teamid_to_encoding(self):
        self.assertEqual(teamid_to_encoding('31'), 'T31')
        self.assertEqual(teamid_to_encoding('32'), 'T32')
        self.assertEqual(teamid_to_encoding('33'), 'T33')
        self.assertEqual(teamid_to_encoding('34'), 'T34')
        self.assertEqual(teamid_to_encoding('35'), 'T35')
        self.assertEqual(teamid_to_encoding('36'), 'T36')
        self.assertEqual(teamid_to_encoding('37'), 'T37')
        self.assertEqual(teamid_to_encoding('38'), 'T38')
        self.assertEqual(teamid_to_encoding('39'), 'T39')
        self.assertEqual(teamid_to_encoding('40'), 'T40')
        self.assertEqual(teamid_to_encoding('41'), 'T41')
        self.assertEqual(teamid_to_encoding('42'), 'T42')
        self.assertEqual(teamid_to_encoding('43'), 'T43')
        self.assertEqual(teamid_to_encoding('44'), 'T44')
        self.assertEqual(teamid_to_encoding('45'), 'T45')
        self.assertEqual(teamid_to_encoding('46'), 'T46')
        self.assertEqual(teamid_to_encoding('47'), 'T47')
        self.assertEqual(teamid_to_encoding('48'), 'T48')
        self.assertEqual(teamid_to_encoding('49'), 'T49')
        self.assertEqual(teamid_to_encoding('50'), 'T50')
        self.assertEqual(teamid_to_encoding('51'), 'T51')
        self.assertEqual(teamid_to_encoding('52'), 'T52')
        self.assertEqual(teamid_to_encoding('53'), 'T53')
        self.assertEqual(teamid_to_encoding('54'), 'T54')
        self.assertEqual(teamid_to_encoding('55'), 'T55')
        self.assertEqual(teamid_to_encoding('56'), 'T56')
        self.assertEqual(teamid_to_encoding('57'), 'T57')
        self.assertEqual(teamid_to_encoding('58'), 'T58')
        self.assertEqual(teamid_to_encoding('59'), 'T59')
        self.assertEqual(teamid_to_encoding('60'), 'T60')

    def test_teamid_to_hometown(self):
        self.assertEqual(teamid_to_hometown('31'), 'Arizona')
        self.assertEqual(teamid_to_hometown('32'), 'Atlanta')
        self.assertEqual(teamid_to_hometown('33'), 'Baltimore')
        self.assertEqual(teamid_to_hometown('34'), 'Boston')
        self.assertEqual(teamid_to_hometown('35'), 'Chicago')
        self.assertEqual(teamid_to_hometown('36'), 'Chicago')
        self.assertEqual(teamid_to_hometown('37'), 'Cincinnati')
        self.assertEqual(teamid_to_hometown('38'), 'Cleveland')
        self.assertEqual(teamid_to_hometown('39'), 'Colorado')
        self.assertEqual(teamid_to_hometown('40'), 'Detroit')
        self.assertEqual(teamid_to_hometown('41'), 'Miami')
        self.assertEqual(teamid_to_hometown('42'), 'Houston')
        self.assertEqual(teamid_to_hometown('43'), 'Kansas City')
        self.assertEqual(teamid_to_hometown('44'), 'Los Angeles')
        self.assertEqual(teamid_to_hometown('45'), 'Los Angeles')
        self.assertEqual(teamid_to_hometown('46'), 'Milwaukee')
        self.assertEqual(teamid_to_hometown('47'), 'Minnesota')
        self.assertEqual(teamid_to_hometown('48'), 'New York')
        self.assertEqual(teamid_to_hometown('49'), 'New York')
        self.assertEqual(teamid_to_hometown('50'), 'Oakland')
        self.assertEqual(teamid_to_hometown('51'), 'Philadelphia')
        self.assertEqual(teamid_to_hometown('52'), 'Pittsburgh')
        self.assertEqual(teamid_to_hometown('53'), 'San Diego')
        self.assertEqual(teamid_to_hometown('54'), 'Seattle')
        self.assertEqual(teamid_to_hometown('55'), 'San Francisco')
        self.assertEqual(teamid_to_hometown('56'), 'St. Louis')
        self.assertEqual(teamid_to_hometown('57'), 'Tampa Bay')
        self.assertEqual(teamid_to_hometown('58'), 'Texas')
        self.assertEqual(teamid_to_hometown('59'), 'Toronto')
        self.assertEqual(teamid_to_hometown('60'), 'Washington')


if __name__ == '__main__':
    unittest.main()
