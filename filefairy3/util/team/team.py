#!/usr/bin/env python3
# -*- coding: utf-8 -*-\

import re
from functools import partial


def _team(_, abbreviation, decoding, encoding, hometown, precoding, teamid):
    return {
        'abbreviation': abbreviation,
        'decoding': decoding.format(_),
        'encoding': encoding,
        'hometown': hometown.format(_),
        'precoding': precoding.format(_),
        'teamid': teamid,
    }


_teams = [
    _team('Arizona', 'ARI', '{} Diamondbacks', 'T31', '{}', '{}', '31'),
    _team('Atlanta', 'ATL', '{} Braves', 'T32', '{}', '{}', '32'),
    _team('Baltimore', 'BAL', '{} Orioles', 'T33', '{}', '{}', '33'),
    _team('Boston', 'BOS', '{} Red Sox', 'T34', '{}', '{}', '34'),
    _team('Chicago', 'CWS', '{} White Sox', 'T35', '{}', '', '35'),
    _team('Chicago', 'CHC', '{} Cubs', 'T36', '{}', '', '36'),
    _team('Cincinnati', 'CIN', '{} Reds', 'T37', '{}', '{}', '37'),
    _team('Cleveland', 'CLE', '{} Indians', 'T38', '{}', '{}', '38'),
    _team('Colorado', 'COL', '{} Rockies', 'T39', '{}', '{}', '39'),
    _team('Detroit', 'DET', '{} Tigers', 'T40', '{}', '{}', '40'),
    _team('Miami', 'MIA', '{} Marlins', 'T41', '{}', '{}', '41'),
    _team('Houston', 'HOU', '{} Astros', 'T42', '{}', '{}', '42'),
    _team('Kansas City', 'KC', '{} Royals', 'T43', '{}', '{}', '43'),
    _team('Los Angeles', 'LAA', '{} Angels', 'T44', '{}', '', '44'),
    _team('Los Angeles', 'LAD', '{} Dodgers', 'T45', '{}', '', '45'),
    _team('Milwaukee', 'MIL', '{} Brewers', 'T46', '{}', '{}', '46'),
    _team('Minnesota', 'MIN', '{} Twins', 'T47', '{}', '{}', '47'),
    _team('New York', 'NYY', '{} Yankees', 'T48', '{}', '', '48'),
    _team('New York', 'NYM', '{} Mets', 'T49', '{}', '', '49'),
    _team('Oakland', 'OAK', '{} Athletics', 'T50', '{}', '{}', '50'),
    _team('Philadelphia', 'PHI', '{} Phillies', 'T51', '{}', '{}', '51'),
    _team('Pittsburgh', 'PIT', '{} Pirates', 'T52', '{}', '{}', '52'),
    _team('San Diego', 'SD', '{} Padres', 'T53', '{}', '{}', '53'),
    _team('Seattle', 'SEA', '{} Mariners', 'T54', '{}', '{}', '54'),
    _team('San Francisco', 'SF', '{} Giants', 'T55', '{}', '{}', '55'),
    _team('St. Louis', 'STL', '{} Cardinals', 'T56', '{}', '{}', '56'),
    _team('Tampa Bay', 'TB', '{} Rays', 'T57', '{}', '{}', '57'),
    _team('Texas', 'TEX', '{} Rangers', 'T58', '{}', '{}', '58'),
    _team('Toronto', 'TOR', '{} Blue Jays', 'T59', '{}', '{}', '59'),
    _team('Washington', 'WAS', '{} Nationals', 'T60', '{}', '{}', '60'),
    _team('Chicago', '', '{}', 'TCH', '', '{}', ''),
    _team('Los Angeles', '', '{}', 'TLA', '', '{}', ''),
    _team('New York', '', '{}', 'TNY', '', '{}', ''),
]


def _map(k, vs):
    return {t[k]: {v: t[v] for v in vs if t[v]} for t in _teams if t[k]}


def _repl(f, m):
    a = m.group(0)
    b = f(a)
    return b if b else a


def _sub(ks, f, s):
    pattern = '|'.join(ks)
    return re.sub(pattern, partial(_repl, f), s)


_decodings = _map('decoding', ['encoding'])
_encodings = _map('encoding', ['decoding', 'precoding', 'teamid'])
_precodings = _map('precoding', ['encoding'])
_teamids = _map('teamid', ['abbreviation', 'decoding', 'encoding', 'hometown'])
_img = '<img src="https://orangeandblueleaguebaseball.com/StatsLab/' + \
       'reports/news/html/images/team_logos/{0}_40.png" width="20" ' + \
       'height="20" border="0" class="{1}">'
_span = '<span class="align-middle {0}">{1}</span>'
_absolute_img = _img.format('{0}', 'position-absolute {1}-8p top-14p')
_absolute_span = _span.format('d-block text-truncate p{0}-24p', '{1}')
_inline_img = _img.format('{0}', 'd-inline-block')
_inline_span = _span.format('d-inline-block px-2', '{0}')


def chlany():
    return ['TCH', 'TLA', 'TNY']


def decoding_to_encoding(decoding):
    return _decodings.get(decoding, {}).get('encoding', '')


def decoding_to_encoding_sub(text):
    return _sub(_decodings_keys, decoding_to_encoding, text)


def decodings():
    return _decodings_keys


def divisions():
    return [
        ('AL East', ('33', '34', '48', '57', '59')),
        ('AL Central', ('35', '38', '40', '43', '47')),
        ('AL West', ('42', '44', '50', '54', '58')),
        ('NL East', ('32', '41', '49', '51', '60')),
        ('NL Central', ('36', '37', '46', '52', '56')),
        ('NL West', ('31', '39', '45', '53', '55')),
    ]


def encoding_to_decoding(encoding):
    return _encodings.get(encoding, {}).get('decoding', '')


def encoding_to_decoding_sub(text):
    return _sub(_encodings_keys, encoding_to_decoding, text)


def encoding_to_precoding(encoding):
    return _encodings.get(encoding, {}).get('precoding', '')


def encoding_to_teamid(encoding):
    return _encodings.get(encoding, {}).get('teamid', '')


def encodings():
    return _encodings_keys


def precoding_to_encoding(precoding):
    return _precodings.get(precoding, {}).get('encoding', '')


def precoding_to_encoding_sub(text):
    return _sub(_precodings_keys, precoding_to_encoding, text)


def precodings():
    return _precodings_keys


def logo_absolute(teamid, text, side):
    decoding = teamid_to_decoding(teamid)
    fname = decoding.replace('.', '').replace(' ', '_').lower()
    img = _absolute_img.format(fname, side)
    span = _absolute_span.format(side[0], text)
    return img + span


def logo_inline(teamid, text):
    decoding = teamid_to_decoding(teamid)
    fname = decoding.replace('.', '').replace(' ', '_').lower()
    img = _inline_img.format(fname)
    span = _inline_span.format(text)
    return img + span


def teamid_to_abbreviation(teamid):
    return _teamids.get(teamid, {}).get('abbreviation', '')


def teamid_to_decoding(teamid):
    return _teamids.get(teamid, {}).get('decoding', '')


def teamid_to_encoding(teamid):
    return _teamids.get(teamid, {}).get('encoding', '')


def teamid_to_hometown(teamid):
    return _teamids.get(teamid, {}).get('hometown', '')


def teamids():
    return _teamids_keys


_decodings_keys = list(sorted(_decodings.keys(), key=decoding_to_encoding))
_encodings_keys = list(sorted(_encodings.keys()))
_precodings_keys = list(sorted(_precodings.keys(), key=precoding_to_encoding))
_teamids_keys = list(sorted(_teamids.keys()))
