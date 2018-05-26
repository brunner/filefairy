#!/usr/bin/env python3
# -*- coding: utf-8 -*-\

import re
from functools import partial


def _team(_, abbr, chlany, cross, decoding, encoding, home, precoding, teamid):
    return {
        'abbreviation': abbr,
        'chlany': chlany,
        'crosstown': cross,
        'decoding': decoding.format(_),
        'encoding': encoding,
        'hometown': home.format(_),
        'precoding': precoding.format(_),
        'teamid': teamid,
    }


_31 = 'Arizona'
_32 = 'Atlanta'
_33 = 'Baltimore'
_34 = 'Boston'
_37 = 'Cincinnati'
_38 = 'Cleveland'
_39 = 'Colorado'
_40 = 'Detroit'
_41 = 'Miami'
_42 = 'Houston'
_43 = 'Kansas City'
_46 = 'Milwaukee'
_47 = 'Minnesota'
_50 = 'Oakland'
_51 = 'Philadelphia'
_52 = 'Pittsburgh'
_53 = 'San Diego'
_54 = 'Seattle'
_55 = 'San Francisco'
_56 = 'St. Louis'
_57 = 'Tampa Bay'
_58 = 'Texas'
_59 = 'Toronto'
_60 = 'Washington'
_ch = 'Chicago'
_la = 'Los Angeles'
_ny = 'New York'

_teams = [
    _team(_31, 'ARI', '', '', '{} Diamondbacks', 'T31', '{}', '{}', '31'),
    _team(_32, 'ATL', '', '', '{} Braves', 'T32', '{}', '{}', '32'),
    _team(_33, 'BAL', '', '', '{} Orioles', 'T33', '{}', '{}', '33'),
    _team(_34, 'BOS', '', '', '{} Red Sox', 'T34', '{}', '{}', '34'),
    _team(_ch, 'CWS', 'TCH', 'T36', '{} White Sox', 'T35', '{}', '', '35'),
    _team(_ch, 'CHC', 'TCH', 'T35', '{} Cubs', 'T36', '{}', '', '36'),
    _team(_37, 'CIN', '', '', '{} Reds', 'T37', '{}', '{}', '37'),
    _team(_38, 'CLE', '', '', '{} Indians', 'T38', '{}', '{}', '38'),
    _team(_39, 'COL', '', '', '{} Rockies', 'T39', '{}', '{}', '39'),
    _team(_40, 'DET', '', '', '{} Tigers', 'T40', '{}', '{}', '40'),
    _team(_41, 'MIA', '', '', '{} Marlins', 'T41', '{}', '{}', '41'),
    _team(_42, 'HOU', '', '', '{} Astros', 'T42', '{}', '{}', '42'),
    _team(_43, 'KC', '', '', '{} Royals', 'T43', '{}', '{}', '43'),
    _team(_la, 'LAA', 'TLA', 'T45', '{} Angels', 'T44', '{}', '', '44'),
    _team(_la, 'LAD', 'TLA', 'T44', '{} Dodgers', 'T45', '{}', '', '45'),
    _team(_46, 'MIL', '', '', '{} Brewers', 'T46', '{}', '{}', '46'),
    _team(_47, 'MIN', '', '', '{} Twins', 'T47', '{}', '{}', '47'),
    _team(_ny, 'NYY', 'TNY', 'T49', '{} Yankees', 'T48', '{}', '', '48'),
    _team(_ny, 'NYM', 'TNY', 'T48', '{} Mets', 'T49', '{}', '', '49'),
    _team(_50, 'OAK', '', '', '{} Athletics', 'T50', '{}', '{}', '50'),
    _team(_51, 'PHI', '', '', '{} Phillies', 'T51', '{}', '{}', '51'),
    _team(_52, 'PIT', '', '', '{} Pirates', 'T52', '{}', '{}', '52'),
    _team(_53, 'SD', '', '', '{} Padres', 'T53', '{}', '{}', '53'),
    _team(_54, 'SEA', '', '', '{} Mariners', 'T54', '{}', '{}', '54'),
    _team(_55, 'SF', '', '', '{} Giants', 'T55', '{}', '{}', '55'),
    _team(_56, 'STL', '', '', '{} Cardinals', 'T56', '{}', '{}', '56'),
    _team(_57, 'TB', '', '', '{} Rays', 'T57', '{}', '{}', '57'),
    _team(_58, 'TEX', '', '', '{} Rangers', 'T58', '{}', '{}', '58'),
    _team(_59, 'TOR', '', '', '{} Blue Jays', 'T59', '{}', '{}', '59'),
    _team(_60, 'WAS', '', '', '{} Nationals', 'T60', '{}', '{}', '60'),
    _team(_ch, '', '', '', '{}', 'TCH', '', '{}', ''),
    _team(_la, '', '', '', '{}', 'TLA', '', '{}', ''),
    _team(_ny, '', '', '', '{}', 'TNY', '', '{}', ''),
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
_encodings = _map('encoding',
                  ['chlany', 'crosstown', 'decoding', 'precoding', 'teamid'])
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


def encoding_to_chlany(encoding):
    return _encodings.get(encoding, {}).get('chlany', '')


def encoding_to_crosstown(encoding):
    return _encodings.get(encoding, {}).get('crosstown', '')


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
