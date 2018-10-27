#!/usr/bin/env python3
# -*- coding: utf-8 -*-\

import random
import re
from functools import partial


def _team(_1, _2, abbr, colors, chlany, cross, de, en, hn, pre, teamid):
    return {
        'abbreviation': abbr,
        'chlany': chlany,
        'colors': colors,
        'crosstown': cross,
        'decoding': de.format(_1, _2),
        'encoding': en,
        'hometown': hn.format(_1),
        'nickname': hn.format(_2),
        'precoding': pre.format(_1),
        'teamid': teamid,
    }


_v2_teams = [
    'T33', 'T34', 'T35', 'T36', 'T37', 'T38', 'T39', 'T40', 'T41', 'T43',
    'T46', 'T47', 'T48', 'T49', 'T51', 'T52', 'T56', 'T57', 'T58', 'T59'
]
_all = [0, 1, 2, 3, 4, 5, 6]

# yapf: disable
_h31, _n31 = 'Arizona', 'Diamondbacks'
_c31 = (('#000000', '#ffffff', '#a71930', ''),
        ('#000000', '#acacac', '#e3d4ad', ''),
        ('#000000', '#a71930', '#e3d4ad', '', ('red', 'home|away', [6], 1.0)))

_h32, _n32 = 'Atlanta', 'Braves'
_c32 = (('#ce1141', '#ffffff', '#13274f', ''),
        ('#ce1141', '#acacac', '#13274f', ''),
        ('#000000', '#f0f0dc', '#13274f', '', ('cream', 'home', [6], 1.0)),
        ('#ffffff', '#13274f', '#13274f', '', ('blue', 'away', _all, .5)))

_h33, _n33 = 'Baltimore', 'Orioles'
_c33 = [('black', 'home|away', [4], 1.0),
        ('orange', 'home|away', [5], 1.0)]

_h34, _n34 = 'Boston', 'Red Sox'
_c34 = [('red', 'home', [4], 1.0),
        ('blue', 'away', [4], 1.0)]

_h37, _n37 = 'Cincinnati', 'Reds'
_c37 = [('red', 'home', _all, .35)]

_h38, _n38 = 'Cleveland', 'Indians'
_c38 = [('blue', 'home|away', _all, .6)]

_h39, _n39 = 'Colorado', 'Rockies'
_c39 = [('purple', 'home|away', _all, .35),
        ('black', 'home|away', _all, .15)]

_h40, _n40 = 'Detroit', 'Tigers'
_c40 = [('blue', 'home', _all, .6),
        ('orange', 'away', _all, .5)]

_h41, _n41, _c41 = 'Miami', 'Marlins', []

_h42, _n42 = 'Houston', 'Astros'
_c42 = (('#002d62', '#ffffff', '#eb6e1f', ''),
        ('#002d62', '#acacac', '#eb6e1f', ''),
        ('#002d62', '#eb6e1f', '#ffffff', '', ('orange', 'home|away', _all, .2)))

_h43, _n43 = 'Kansas City', 'Royals'
_c43 = [('sky', 'home', [6], 1.0)]

_h46, _n46 = 'Milwaukee', 'Brewers'
_c46 = [('sky', 'home|away', [5, 6], 1.0)]

_h47, _n47 = 'Minnesota', 'Twins'
_c47 = [('cream', 'home', [0, 1, 2, 3, 4], 1.0),
        ('blue', 'away', _all, .25)]

_h50, _n50 = 'Oakland', 'Athletics'
_c50 = (('#003831', '#ffffff', '#efb21e', ''),
        ('#003831', '#acacac', '#efb21e', ''),
        ('#ffffff', '#035a2e', '#efb21e', '', ('green', 'home', [4], 1.0)),
        ('#003831', '#fcb600', '#ffffff', '', ('yellow', 'home', _all, .1)),
        ('#ffffff', '#003831', '#efb21e', '', ('green', 'home|away', _all, .45)))

_h51, _n51 = 'Philadelphia', 'Phillies'
_c51 = [('sky', 'home', [3], 1.0),
        ('cream', 'home', [6], 1.0)]

_h52, _n52 = 'Pittsburgh', 'Pirates'
_c52 = [('yellow', 'home', [6], 1.0),
        ('black', 'home|away', _all, .4)]

_h53, _n53 = 'San Diego', 'Padres'
_c53 = (('#002d62', '#ffffff', '#ffffff', ''),
        ('#002d62', '#acacac', '#acacac', ''),
        ('#ffc72c', '#473729', '#473729', '', ('brown', 'home', [4], 1.0)),
        ('#ffffff', '#002d62', '#002d62', '', ('blue', 'away', _all, .5)))

_h54, _n54 = 'Seattle', 'Mariners'
_c54 = (('#0c2c56', '#ffffff', '#005c5c', ''),
        ('#0c2c56', '#acacac', '#005c5c', ''),
        ('#c4ced4', '#005c5c', '#0c2c56', '', ('green', 'home', [4], 1.0)),
        ('#0c2c56', '#f0f0dc', '#005c5c', '', ('cream', 'home', [6], 1.0)),
        ('#c4ced4', '#0c2c56', '#005c5c', '', ('blue', 'away', _all, .45)))

_h55, _n55 = 'San Francisco', 'Giants'
_c55 = (('#27251f', '#ffffff', '#fd5a1e', ''),
        ('#27251f', '#acacac', '#fd5a1e', ''),
        ('#27251f', '#fd5a1e', '#ffffff', '', ('orange', 'home', [4], 1.0)))

_h56, _n56 = 'St. Louis', 'Cardinals'
_c56 = [('cream', 'home', [5], 1.0)]

_h57, _n57 = 'Tampa Bay', 'Rays'
_c57 = [('sky', 'home', [6], 1.0),
        ('blue', 'away', _all, .5)]

_h58, _n58 = 'Texas', 'Rangers'
_c58 = [('sky', 'home', [6], 1.0),
        ('blue', 'home|away', _all, .5)]

_h59, _n59 = 'Toronto', 'Blue Jays'
_c59 = [('blue', 'home|away', _all, .5)]

_h60, _n60 = 'Washington', 'Nationals'
_c60 = (('#ab0003', '#ffffff', '#14225a', ''),
        ('#ab0003', '#acacac', '#14225a', ''),
        ('#ab0003', '#14225a', '#ffffff', '', ('blue', 'home|away', [1, 4], .5)),
        ('#ffffff', '#ab0003', '#14225a', '', ('red', 'home|away', [5, 6], .5)))

_hch, _n35, _n36 = 'Chicago', 'White Sox', 'Cubs'
_c35 = [('blue', 'home', [6], 1.0),
        ('black', 'home|away', _all, .6)]
_c36 = [('blue', 'home|away', [6], 1.0)]

_hla, _n44, _n45 = 'Los Angeles', 'Angels', 'Dodgers'
_c44 = (('#ba0021', '#ffffff', '#003263', ''),
        ('#ba0021', '#acacac', '#003263', ''),
        ('#c4ced4', '#ba0021', '#003263', '', ('red', 'home|away', _all, .55)))
_c45 = (('#005a9c', '#ffffff', '#ef3e42', ''),
        ('#005a9c', '#acacac', '#ef3e42', ''))

_hny, _n48, _n49 = 'New York', 'Yankees', 'Mets'
_c48 = []
_c49 = [('black', 'home', _all, .25),
        ('blue', 'away', _all, .25)]
# yapf: enable

_teams = [
    _team(_h31, _n31, 'ARI', _c31, '', '', '{} {}', 'T31', '{}', '{}', '31'),
    _team(_h32, _n32, 'ATL', _c32, '', '', '{} {}', 'T32', '{}', '{}', '32'),
    _team(_h33, _n33, 'BAL', _c33, '', '', '{} {}', 'T33', '{}', '{}', '33'),
    _team(_h34, _n34, 'BOS', _c34, '', '', '{} {}', 'T34', '{}', '{}', '34'),
    _team(_hch, _n35, 'CWS', _c35, 'TCH', 'T36', '{} {}', 'T35', '{}', '',
          '35'),
    _team(_hch, _n36, 'CHC', _c36, 'TCH', 'T35', '{} {}', 'T36', '{}', '',
          '36'),
    _team(_h37, _n37, 'CIN', _c37, '', '', '{} {}', 'T37', '{}', '{}', '37'),
    _team(_h38, _n38, 'CLE', _c38, '', '', '{} {}', 'T38', '{}', '{}', '38'),
    _team(_h39, _n39, 'COL', _c39, '', '', '{} {}', 'T39', '{}', '{}', '39'),
    _team(_h40, _n40, 'DET', _c40, '', '', '{} {}', 'T40', '{}', '{}', '40'),
    _team(_h41, _n41, 'MIA', _c41, '', '', '{} {}', 'T41', '{}', '{}', '41'),
    _team(_h42, _n42, 'HOU', _c42, '', '', '{} {}', 'T42', '{}', '{}', '42'),
    _team(_h43, _n43, 'KC', _c43, '', '', '{} {}', 'T43', '{}', '{}', '43'),
    _team(_hla, _n44, 'LAA', _c44, 'TLA', 'T45', '{} {}', 'T44', '{}', '',
          '44'),
    _team(_hla, _n45, 'LAD', _c45, 'TLA', 'T44', '{} {}', 'T45', '{}', '',
          '45'),
    _team(_h46, _n46, 'MIL', _c46, '', '', '{} {}', 'T46', '{}', '{}', '46'),
    _team(_h47, _n47, 'MIN', _c47, '', '', '{} {}', 'T47', '{}', '{}', '47'),
    _team(_hny, _n48, 'NYY', _c48, 'TNY', 'T49', '{} {}', 'T48', '{}', '',
          '48'),
    _team(_hny, _n49, 'NYM', _c49, 'TNY', 'T48', '{} {}', 'T49', '{}', '',
          '49'),
    _team(_h50, _n50, 'OAK', _c50, '', '', '{} {}', 'T50', '{}', '{}', '50'),
    _team(_h51, _n51, 'PHI', _c51, '', '', '{} {}', 'T51', '{}', '{}', '51'),
    _team(_h52, _n52, 'PIT', _c52, '', '', '{} {}', 'T52', '{}', '{}', '52'),
    _team(_h53, _n53, 'SD', _c53, '', '', '{} {}', 'T53', '{}', '{}', '53'),
    _team(_h54, _n54, 'SEA', _c54, '', '', '{} {}', 'T54', '{}', '{}', '54'),
    _team(_h55, _n55, 'SF', _c55, '', '', '{} {}', 'T55', '{}', '{}', '55'),
    _team(_h56, _n56, 'STL', _c56, '', '', '{} {}', 'T56', '{}', '{}', '56'),
    _team(_h57, _n57, 'TB', _c57, '', '', '{} {}', 'T57', '{}', '{}', '57'),
    _team(_h58, _n58, 'TEX', _c58, '', '', '{} {}', 'T58', '{}', '{}', '58'),
    _team(_h59, _n59, 'TOR', _c59, '', '', '{} {}', 'T59', '{}', '{}', '59'),
    _team(_h60, _n60, 'WAS', _c60, '', '', '{} {}', 'T60', '{}', '{}', '60'),
    _team(_hch, '', '', '', '', '', '{}', 'TCH', '', '{}', ''),
    _team(_hla, '', '', '', '', '', '{}', 'TLA', '', '{}', ''),
    _team(_hny, '', '', '', '', '', '{}', 'TNY', '', '{}', ''),
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


_decodings = _map('decoding', ['encoding', 'nickname'])
_encodings = _map('encoding', [
    'abbreviation', 'chlany', 'colors', 'crosstown', 'decoding', 'nickname',
    'precoding', 'teamid'
])
_precodings = _map('precoding', ['encoding'])
_teamids = _map(
    'teamid', ['abbreviation', 'decoding', 'encoding', 'hometown', 'nickname'])
_img = '<img src="https://orangeandblueleaguebaseball.com/StatsLab/' + \
       'reports/news/html/images/team_logos/{0}_40.png" width="20" ' + \
       'height="20" border="0" class="{1}">'
_span = '<span class="align-middle {0}">{1}</span>'
_absolute_img = _img.format('{0}', 'position-absolute {1}-8p top-14p')
_absolute_span = _span.format('d-block text-truncate p{0}-24p', '{1}')
_inline_img = _img.format('{0}', 'd-inline-block')
_inline_span = _span.format('d-inline-block px-2', '{0}')


def choose_colors(encoding, colors, day, where, clash):
    if encoding in _v2_teams:
        for primary, regex, days, pct in colors:
            m = re.search(regex, where)
            if m and day in days and primary != clash:
                if pct >= random.random():
                    return (primary, 'alt-{}'.format(primary))
        if re.search('home', where):
            return ('white', 'home')
        return ('grey', 'away')

    for alt in colors[2:]:
        primary, regex, days, pct = alt[-1]
        m = re.search(regex, where)
        if m and day in days and pct >= random.random() and primary != clash:
            return (primary, alt[:4])
    if re.search('home', where):
        return ('white', colors[0])
    return ('grey', colors[1])


def chlany():
    return ['TCH', 'TLA', 'TNY']


def decoding_to_encoding(decoding):
    return _decodings.get(decoding, {}).get('encoding', '')


def decoding_to_nickname(decoding):
    return _decodings.get(decoding, {}).get('nickname', '')


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


def encoding_to_abbreviation(encoding):
    return _encodings.get(encoding, {}).get('abbreviation', '')


def encoding_to_chlany(encoding):
    return _encodings.get(encoding, {}).get('chlany', '')


def encoding_to_colors(encoding):
    return _encodings.get(encoding, {}).get('colors', '')


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


def teamid_to_nickname(teamid):
    return _teamids.get(teamid, {}).get('nickname', '')


def teamids():
    return _teamids_keys


_decodings_keys = list(sorted(_decodings.keys(), key=decoding_to_encoding))
_encodings_keys = list(sorted(_encodings.keys()))
_precodings_keys = list(sorted(_precodings.keys(), key=precoding_to_encoding))
_teamids_keys = list(sorted(_teamids.keys()))
