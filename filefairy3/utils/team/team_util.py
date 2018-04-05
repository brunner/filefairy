#!/usr/bin/env python
# -*- coding: utf-8 -*-

_collection = {
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
    return _collection.get(teamid, '')


def divisions():
    return [
        ('AL East', ('33', '34', '48', '57', '59')),
        ('AL Central', ('35', '38', '40', '43', '47')),
        ('AL West', ('42', '44', '50', '54', '58')),
        ('NL East', ('32', '41', '49', '51', '60')),
        ('NL Central', ('36', '37', '46', '52', '56')),
        ('NL West', ('31', '39', '45', '53', '55')),
    ]
