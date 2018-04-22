#!/usr/bin/env python
# -*- coding: utf-8 -*-\


def _team(abbreviation, hometown, nickname):
    return {
        'abbreviation': abbreviation,
        'hometown': hometown,
        'nickname': nickname,
    }


_teams = {
    '31': _team('ARI', 'Arizona', 'Diamondbacks'),
    '32': _team('ATL', 'Atlanta', 'Braves'),
    '33': _team('BAL', 'Baltimore', 'Orioles'),
    '34': _team('BOS', 'Boston', 'Red Sox'),
    '35': _team('CWS', 'Chicago', 'White Sox'),
    '36': _team('CHC', 'Chicago', 'Cubs'),
    '37': _team('CIN', 'Cincinnati', 'Reds'),
    '38': _team('CLE', 'Cleveland', 'Indians'),
    '39': _team('COL', 'Colorado', 'Rockies'),
    '40': _team('DET', 'Detroit', 'Tigers'),
    '41': _team('MIA', 'Miami', 'Marlins'),
    '42': _team('HOU', 'Houston', 'Astros'),
    '43': _team('KC', 'Kansas City', 'Royals'),
    '44': _team('LAA', 'Los Angeles', 'Angels'),
    '45': _team('LAD', 'Los Angeles', 'Dodgers'),
    '46': _team('MIL', 'Milwaukee', 'Brewers'),
    '47': _team('MIN', 'Minnesota', 'Twins'),
    '48': _team('NYY', 'New York', 'Yankees'),
    '49': _team('NYM', 'New York', 'Mets'),
    '50': _team('OAK', 'Oakland', 'Athletics'),
    '51': _team('PHI', 'Philadelphia', 'Phillies'),
    '52': _team('PIT', 'Pittsburgh', 'Pirates'),
    '53': _team('SD', 'San Diego', 'Padres'),
    '54': _team('SEA', 'Seattle', 'Mariners'),
    '55': _team('SF', 'San Francisco', 'Giants'),
    '56': _team('STL', 'St. Louis', 'Cardinals'),
    '57': _team('TB', 'Tampa Bay', 'Rays'),
    '58': _team('TEX', 'Texas', 'Rangers'),
    '59': _team('TOR', 'Toronto', 'Blue Jays'),
    '60': _team('WAS', 'Washington', 'Nationals'),
}


def abbreviation(teamid):
    return _teams.get(teamid, {}).get('abbreviation', '')


def hometown(teamid):
    return _teams.get(teamid, {}).get('hometown', '')


def nickname(teamid):
    return _teams.get(teamid, {}).get('nickname', '')


def divisions():
    return [
        ('AL East', ('33', '34', '48', '57', '59')),
        ('AL Central', ('35', '38', '40', '43', '47')),
        ('AL West', ('42', '44', '50', '54', '58')),
        ('NL East', ('32', '41', '49', '51', '60')),
        ('NL Central', ('36', '37', '46', '52', '56')),
        ('NL West', ('31', '39', '45', '53', '55')),
    ]

_img = '<img src="https://orangeandblueleaguebaseball.com/StatsLab/' + \
        'reports/news/html/images/team_logos/{0}_40.png" width="20" ' + \
        'height="20" border="0" class="position-absolute {1}-8p top-14p">'
_span = '<span class="d-block text-truncate align-middle p{0}-24p">{1}</span>'


def logo(teamid, text, side):
    path = hometown(teamid) + ' ' + nickname(teamid)
    fname = path.replace('.', '').replace(' ', '_').lower()
    return _img.format(fname, side) + _span.format(side[0], text)
