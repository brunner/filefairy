#!/usr/bin/env python3
# -*- coding: utf-8 -*-\

import re
from functools import partial


def _team(_1, _2, abbr, chlany, cross, de, en, hn, pre, teamid):
    return {
        'abbreviation': abbr,
        'chlany': chlany,
        'crosstown': cross,
        'decoding': de.format(_1, _2),
        'encoding': en,
        'hometown': hn.format(_1),
        'nickname': hn.format(_2),
        'precoding': pre.format(_1),
        'teamid': teamid,
    }


_h31, _n31 = 'Arizona', 'Diamondbacks'
_h32, _n32 = 'Atlanta', 'Braves'
_h33, _n33 = 'Baltimore', 'Orioles'
_h34, _n34 = 'Boston', 'Red Sox'
_h37, _n37 = 'Cincinnati', 'Reds'
_h38, _n38 = 'Cleveland', 'Indians'
_h39, _n39 = 'Colorado', 'Rockies'
_h40, _n40 = 'Detroit', 'Tigers'
_h41, _n41 = 'Miami', 'Marlins'
_h42, _n42 = 'Houston', 'Astros'
_h43, _n43 = 'Kansas City', 'Royals'
_h46, _n46 = 'Milwaukee', 'Brewers'
_h47, _n47 = 'Minnesota', 'Twins'
_h50, _n50 = 'Oakland', 'Athletics'
_h51, _n51 = 'Philadelphia', 'Phillies'
_h52, _n52 = 'Pittsburgh', 'Pirates'
_h53, _n53 = 'San Diego', 'Padres'
_h54, _n54 = 'Seattle', 'Mariners'
_h55, _n55 = 'San Francisco', 'Giants'
_h56, _n56 = 'St. Louis', 'Cardinals'
_h57, _n57 = 'Tampa Bay', 'Rays'
_h58, _n58 = 'Texas', 'Rangers'
_h59, _n59 = 'Toronto', 'Blue Jays'
_h60, _n60 = 'Washington', 'Nationals'
_hch, _n35, _n36 = 'Chicago', 'White Sox', 'Cubs'
_hla, _n44, _n45 = 'Los Angeles', 'Angels', 'Dodgers'
_hny, _n48, _n49 = 'New York', 'Yankees', 'Mets'

_teams = [
    _team(_h31, _n31, 'ARI', '', '', '{} {}', 'T31', '{}', '{}', '31'),
    _team(_h32, _n32, 'ATL', '', '', '{} {}', 'T32', '{}', '{}', '32'),
    _team(_h33, _n33, 'BAL', '', '', '{} {}', 'T33', '{}', '{}', '33'),
    _team(_h34, _n34, 'BOS', '', '', '{} {}', 'T34', '{}', '{}', '34'),
    _team(_hch, _n35, 'CWS', 'TCH', 'T36', '{} {}', 'T35', '{}', '', '35'),
    _team(_hch, _n36, 'CHC', 'TCH', 'T35', '{} {}', 'T36', '{}', '', '36'),
    _team(_h37, _n37, 'CIN', '', '', '{} {}', 'T37', '{}', '{}', '37'),
    _team(_h38, _n38, 'CLE', '', '', '{} {}', 'T38', '{}', '{}', '38'),
    _team(_h39, _n39, 'COL', '', '', '{} {}', 'T39', '{}', '{}', '39'),
    _team(_h40, _n40, 'DET', '', '', '{} {}', 'T40', '{}', '{}', '40'),
    _team(_h41, _n41, 'MIA', '', '', '{} {}', 'T41', '{}', '{}', '41'),
    _team(_h42, _n42, 'HOU', '', '', '{} {}', 'T42', '{}', '{}', '42'),
    _team(_h43, _n43, 'KC', '', '', '{} {}', 'T43', '{}', '{}', '43'),
    _team(_hla, _n44, 'LAA', 'TLA', 'T45', '{} {}', 'T44', '{}', '', '44'),
    _team(_hla, _n45, 'LAD', 'TLA', 'T44', '{} {}', 'T45', '{}', '', '45'),
    _team(_h46, _n46, 'MIL', '', '', '{} {}', 'T46', '{}', '{}', '46'),
    _team(_h47, _n47, 'MIN', '', '', '{} {}', 'T47', '{}', '{}', '47'),
    _team(_hny, _n48, 'NYY', 'TNY', 'T49', '{} {}', 'T48', '{}', '', '48'),
    _team(_hny, _n49, 'NYM', 'TNY', 'T48', '{} {}', 'T49', '{}', '', '49'),
    _team(_h50, _n50, 'OAK', '', '', '{} {}', 'T50', '{}', '{}', '50'),
    _team(_h51, _n51, 'PHI', '', '', '{} {}', 'T51', '{}', '{}', '51'),
    _team(_h52, _n52, 'PIT', '', '', '{} {}', 'T52', '{}', '{}', '52'),
    _team(_h53, _n53, 'SD', '', '', '{} {}', 'T53', '{}', '{}', '53'),
    _team(_h54, _n54, 'SEA', '', '', '{} {}', 'T54', '{}', '{}', '54'),
    _team(_h55, _n55, 'SF', '', '', '{} {}', 'T55', '{}', '{}', '55'),
    _team(_h56, _n56, 'STL', '', '', '{} {}', 'T56', '{}', '{}', '56'),
    _team(_h57, _n57, 'TB', '', '', '{} {}', 'T57', '{}', '{}', '57'),
    _team(_h58, _n58, 'TEX', '', '', '{} {}', 'T58', '{}', '{}', '58'),
    _team(_h59, _n59, 'TOR', '', '', '{} {}', 'T59', '{}', '{}', '59'),
    _team(_h60, _n60, 'WAS', '', '', '{} {}', 'T60', '{}', '{}', '60'),
    _team(_hch, '', '', '', '', '{}', 'TCH', '', '{}', ''),
    _team(_hla, '', '', '', '', '{}', 'TLA', '', '{}', ''),
    _team(_hny, '', '', '', '', '{}', 'TNY', '', '{}', ''),
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
_encodings = _map(
    'encoding',
    ['chlany', 'crosstown', 'decoding', 'nickname', 'precoding', 'teamid'])
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


def encoding_to_nickname(encoding):
    return _encodings.get(encoding, {}).get('nickname', '')


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
