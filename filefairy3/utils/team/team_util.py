#!/usr/bin/env python
# -*- coding: utf-8 -*-

_abbreviations = {
    '31': 'ARI',
    '32': 'ATL',
    '33': 'BAL',
    '34': 'BOS',
    '35': 'CWS',
    '36': 'CHC',
    '37': 'CIN',
    '38': 'CLE',
    '39': 'COL',
    '40': 'DET',
    '41': 'MIA',
    '42': 'HOU',
    '43': 'KC',
    '44': 'LAA',
    '45': 'LAD',
    '46': 'MIL',
    '47': 'MIN',
    '48': 'NYY',
    '49': 'NYM',
    '50': 'OAK',
    '51': 'PHI',
    '52': 'PIT',
    '53': 'SD',
    '54': 'SEA',
    '55': 'SF',
    '56': 'STL',
    '57': 'TB',
    '58': 'TEX',
    '59': 'TOR',
    '60': 'WAS',
}


def abbreviation(teamid):
    return _abbreviations.get(teamid, '')


_full_names = {
    '31': 'arizona_diamondbacks',
    '32': 'atlanta_braves',
    '33': 'baltimore_orioles',
    '34': 'boston_red_sox',
    '35': 'chicago_white_sox',
    '36': 'chicago_cubs',
    '37': 'cincinnati_reds',
    '38': 'cleveland_indians',
    '39': 'colorado_rockies',
    '40': 'detroit_tigers',
    '41': 'miami_marlins',
    '42': 'houston_astros',
    '43': 'kansas_city_royals',
    '44': 'los_angeles_angels',
    '45': 'los_angeles_dodgers',
    '46': 'milwaukee_brewers',
    '47': 'minnesota_twins',
    '48': 'new_york_yankees',
    '49': 'new_york_mets',
    '50': 'oakland_athletics',
    '51': 'philadelphia_phillies',
    '52': 'pittsburgh_pirates',
    '53': 'san_diego_padres',
    '54': 'seattle_mariners',
    '55': 'san_francisco_giants',
    '56': 'st_louis_cardinals',
    '57': 'tampa_bay_rays',
    '58': 'texas_rangers',
    '59': 'toronto_blue_jays',
    '60': 'washington_nationals',
}

_img_24 = '<img src="https://orangeandblueleaguebaseball.com/StatsLab/' + \
       'reports/news/html/images/team_logos/{}_40.png" ' + \
       'width="24" height="24" border="0" class="d-inline-block">'


def logo_24(teamid):
    return _img_24.format(_full_names.get(teamid, ''))


def divisions():
    return [
        ('AL East', ('33', '34', '48', '57', '59')),
        ('AL Central', ('35', '38', '40', '43', '47')),
        ('AL West', ('42', '44', '50', '54', '58')),
        ('NL East', ('32', '41', '49', '51', '60')),
        ('NL Central', ('36', '37', '46', '52', '56')),
        ('NL West', ('31', '39', '45', '53', '55')),
    ]
