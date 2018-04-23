#!/usr/bin/env python
# -*- coding: utf-8 -*-\

_nicknames = {
    'Arizona': 'Diamondbacks',
    'Atlanta': 'Braves',
    'Baltimore': 'Orioles',
    'Boston': 'Red Sox',
    'Chicago': '',
    'Cincinnati': 'Reds',
    'Cleveland': 'Indians',
    'Colorado': 'Rockies',
    'Detroit': 'Tigers',
    'Miami': 'Marlins',
    'Houston': 'Astros',
    'Kansas City': 'Royals',
    'Los Angeles': '',
    'Milwaukee': 'Brewers',
    'Minnesota': 'Twins',
    'New York': '',
    'Oakland': 'Athletics',
    'Philadelphia': 'Phillies',
    'Pittsburgh': 'Pirates',
    'San Diego': 'Padres',
    'Seattle': 'Mariners',
    'San Francisco': 'Giants',
    'St. Louis': 'Cardinals',
    'Tampa Bay': 'Rays',
    'Texas': 'Rangers',
    'Toronto': 'Blue Jays',
    'Washington': 'Nationals',
}


def _team(abbreviation, hometown, nickname=''):
    return {
        'abbreviation': abbreviation,
        'hometown': hometown,
        'nickname': nickname if nickname else _nicknames[hometown],
    }


_teams = {
    '31': _team('ARI', 'Arizona'),
    '32': _team('ATL', 'Atlanta'),
    '33': _team('BAL', 'Baltimore'),
    '34': _team('BOS', 'Boston'),
    '35': _team('CWS', 'Chicago', nickname='White Sox'),
    '36': _team('CHC', 'Chicago', nickname='Cubs'),
    '37': _team('CIN', 'Cincinnati'),
    '38': _team('CLE', 'Cleveland'),
    '39': _team('COL', 'Colorado'),
    '40': _team('DET', 'Detroit'),
    '41': _team('MIA', 'Miami'),
    '42': _team('HOU', 'Houston'),
    '43': _team('KC', 'Kansas City'),
    '44': _team('LAA', 'Los Angeles', nickname='Angels'),
    '45': _team('LAD', 'Los Angeles', nickname='Dodgers'),
    '46': _team('MIL', 'Milwaukee'),
    '47': _team('MIN', 'Minnesota'),
    '48': _team('NYY', 'New York', nickname='Yankees'),
    '49': _team('NYM', 'New York', nickname='Mets'),
    '50': _team('OAK', 'Oakland'),
    '51': _team('PHI', 'Philadelphia'),
    '52': _team('PIT', 'Pittsburgh'),
    '53': _team('SD', 'San Diego'),
    '54': _team('SEA', 'Seattle'),
    '55': _team('SF', 'San Francisco'),
    '56': _team('STL', 'St. Louis'),
    '57': _team('TB', 'Tampa Bay'),
    '58': _team('TEX', 'Texas'),
    '59': _team('TOR', 'Toronto'),
    '60': _team('WAS', 'Washington'),
}


def abbreviation(teamid):
    return _teams.get(teamid, {}).get('abbreviation', '')


def hometown(teamid):
    return _teams.get(teamid, {}).get('hometown', '')


def nickname(key, hometown=False):
    if hometown:
        return _nicknames.get(key, '')

    return _teams.get(key, {}).get('nickname', '')


def divisions():
    return [
        ('AL East', ('33', '34', '48', '57', '59')),
        ('AL Central', ('35', '38', '40', '43', '47')),
        ('AL West', ('42', '44', '50', '54', '58')),
        ('NL East', ('32', '41', '49', '51', '60')),
        ('NL Central', ('36', '37', '46', '52', '56')),
        ('NL West', ('31', '39', '45', '53', '55')),
    ]


def hometowns():
    return _nicknames.keys()

_aimg = '<img src="https://orangeandblueleaguebaseball.com/StatsLab/' + \
        'reports/news/html/images/team_logos/{0}_40.png" width="20" ' + \
        'height="20" border="0" class="position-absolute {1}-8p top-14p">'
_aspan = '<span class="d-block text-truncate align-middle p{0}-24p">{1}</span>'


def alogo(teamid, text, side):
    path = hometown(teamid) + ' ' + nickname(teamid)
    fname = path.replace('.', '').replace(' ', '_').lower()
    return _aimg.format(fname, side) + _aspan.format(side[0], text)

_iimg = '<img src="https://orangeandblueleaguebaseball.com/StatsLab/' + \
        'reports/news/html/images/team_logos/{}_40.png" ' + \
        'width="20" height="20" border="0" class="d-inline-block">'
_ispan = '<span class="d-inline-block align-middle px-2">{}</span>'


def ilogo(teamid, text):
    path = hometown(teamid) + ' ' + nickname(teamid)
    fname = path.replace('.', '').replace(' ', '_').lower()
    return _iimg.format(fname) + _ispan.format(text)
