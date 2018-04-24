#!/usr/bin/env python
# -*- coding: utf-8 -*-\


def _team(teamid, abbreviation, hometown, nickname):
    return {
        'teamid': teamid,
        'abbreviation': abbreviation,
        'hometown': hometown,
        'nickname': nickname,
        'fullname': hometown + ' ' + nickname,
    }


_teams = [
    _team('31', 'ARI', 'Arizona', 'Diamondbacks'),
    _team('32', 'ATL', 'Atlanta', 'Braves'),
    _team('33', 'BAL', 'Baltimore', 'Orioles'),
    _team('34', 'BOS', 'Boston', 'Red Sox'),
    _team('35', 'CWS', 'Chicago', 'White Sox'),
    _team('36', 'CHC', 'Chicago', 'Cubs'),
    _team('37', 'CIN', 'Cincinnati', 'Reds'),
    _team('38', 'CLE', 'Cleveland', 'Indians'),
    _team('39', 'COL', 'Colorado', 'Rockies'),
    _team('40', 'DET', 'Detroit', 'Tigers'),
    _team('41', 'MIA', 'Miami', 'Marlins'),
    _team('42', 'HOU', 'Houston', 'Astros'),
    _team('43', 'KC', 'Kansas City', 'Royals'),
    _team('44', 'LAA', 'Los Angeles', 'Angels'),
    _team('45', 'LAD', 'Los Angeles', 'Dodgers'),
    _team('46', 'MIL', 'Milwaukee', 'Brewers'),
    _team('47', 'MIN', 'Minnesota', 'Twins'),
    _team('48', 'NYY', 'New York', 'Yankees'),
    _team('49', 'NYM', 'New York', 'Mets'),
    _team('50', 'OAK', 'Oakland', 'Athletics'),
    _team('51', 'PHI', 'Philadelphia', 'Phillies'),
    _team('52', 'PIT', 'Pittsburgh', 'Pirates'),
    _team('53', 'SD', 'San Diego', 'Padres'),
    _team('54', 'SEA', 'Seattle', 'Mariners'),
    _team('55', 'SF', 'San Francisco', 'Giants'),
    _team('56', 'STL', 'St. Louis', 'Cardinals'),
    _team('57', 'TB', 'Tampa Bay', 'Rays'),
    _team('58', 'TEX', 'Texas', 'Rangers'),
    _team('59', 'TOR', 'Toronto', 'Blue Jays'),
    _team('60', 'WAS', 'Washington', 'Nationals'),
]

_chlany = ['Chicago', 'Los Angeles', 'New York']


def _map(key, values):
    return {
        t[key]: {v: t[v]
                 for v in values}
        for t in _teams if t[key] not in _chlany
    }

_by_teamid_values = ['abbreviation', 'hometown', 'nickname', 'fullname']
_by_teamid_map = _map('teamid', _by_teamid_values)
_by_hometown_map = _map('hometown', ['teamid', 'nickname'])
_by_fullname_map = _map('fullname', ['teamid'])


def abbreviation_by_teamid(teamid):
    return _by_teamid_map.get(teamid, {}).get('abbreviation', '')


def hometown_by_teamid(teamid):
    return _by_teamid_map.get(teamid, {}).get('hometown', '')


def nickname_by_teamid(teamid):
    return _by_teamid_map.get(teamid, {}).get('nickname', '')


def fullname_by_teamid(teamid):
    return _by_teamid_map.get(teamid, {}).get('fullname', '')


def teamid_by_hometown(hometown):
    return _by_hometown_map.get(hometown, {}).get('teamid', '')


def nickname_by_hometown(hometown):
    return _by_hometown_map.get(hometown, {}).get('nickname', '')


def teamid_by_fullname(fullname):
    return _by_fullname_map.get(fullname, {}).get('teamid', '')


def divisions():
    return [
        ('AL East', ('33', '34', '48', '57', '59')),
        ('AL Central', ('35', '38', '40', '43', '47')),
        ('AL West', ('42', '44', '50', '54', '58')),
        ('NL East', ('32', '41', '49', '51', '60')),
        ('NL Central', ('36', '37', '46', '52', '56')),
        ('NL West', ('31', '39', '45', '53', '55')),
    ]


def fullnames():
    return list(set(t['fullname'] for t in _teams))


def hometowns():
    return list(set(t['hometown'] for t in _teams))


def teamids():
    return list(set(t['teamid'] for t in _teams))


def _path(teamid):
    return hometown_by_teamid(teamid) + ' ' + nickname_by_teamid(teamid)


_aimg = '<img src="https://orangeandblueleaguebaseball.com/StatsLab/' + \
        'reports/news/html/images/team_logos/{0}_40.png" width="20" ' + \
        'height="20" border="0" class="position-absolute {1}-8p top-14p">'
_aspan = '<span class="d-block text-truncate align-middle p{0}-24p">{1}</span>'


def alogo(teamid, text, side):
    path = _path(teamid)
    fname = path.replace('.', '').replace(' ', '_').lower()
    return _aimg.format(fname, side) + _aspan.format(side[0], text)

_iimg = '<img src="https://orangeandblueleaguebaseball.com/StatsLab/' + \
        'reports/news/html/images/team_logos/{}_40.png" ' + \
        'width="20" height="20" border="0" class="d-inline-block">'
_ispan = '<span class="d-inline-block align-middle px-2">{}</span>'


def ilogo(teamid, text):
    path = _path(teamid)
    fname = path.replace('.', '').replace(' ', '_').lower()
    return _iimg.format(fname) + _ispan.format(text)
