#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Common (non-reloadable) util methods for team information."""

import re
from functools import partial


def _team(encoding, abbreviation, hometown, nickname):
    special1 = encoding in ['TCH', 'TLA', 'TNY']
    special2 = encoding in ['T35', 'T36', 'T44', 'T45', 'T48', 'T49']

    if encoding == 'TCH':
        encodings = ['T35', 'T36']
    elif encoding == 'TLA':
        encodings = ['T44', 'T45']
    elif encoding == 'TNY':
        encodings = ['T48', 'T49']
    else:
        encodings = [encoding]

    return {
        'abbreviation': abbreviation if not special1 else '',
        'decoding': (hometown + ' ' + nickname) if not special1 else '',
        'encoding': encoding,
        'encodings': encodings,
        'hometown': hometown,
        'nickname': nickname,
        'precoding': hometown if not special2 else '',
        'teamid': encoding.strip('T') if not special1 else '',
    }


TEAMS = [
    _team('T31', 'ARI', 'Arizona', 'Diamondbacks'),
    _team('T32', 'ATL', 'Atlanta', 'Braves'),
    _team('T33', 'BAL', 'Baltimore', 'Orioles'),
    _team('T34', 'BOS', 'Boston', 'Red Sox'),
    _team('T35', 'CWS', 'Chicago', 'White Sox'),
    _team('T36', 'CHC', 'Chicago', 'Cubs'),
    _team('T37', 'CIN', 'Cincinnati', 'Reds'),
    _team('T38', 'CLE', 'Cleveland', 'Indians'),
    _team('T39', 'COL', 'Colorado', 'Rockies'),
    _team('T40', 'DET', 'Detroit', 'Tigers'),
    _team('T41', 'MIA', 'Miami', 'Marlins'),
    _team('T42', 'HOU', 'Houston', 'Astros'),
    _team('T43', 'KC', 'Kansas City', 'Royals'),
    _team('T44', 'LAA', 'Los Angeles', 'Angels'),
    _team('T45', 'LAD', 'Los Angeles', 'Dodgers'),
    _team('T46', 'MIL', 'Milwaukee', 'Brewers'),
    _team('T47', 'MIN', 'Minnesota', 'Twins'),
    _team('T48', 'NYY', 'New York', 'Yankees'),
    _team('T49', 'NYM', 'New York', 'Mets'),
    _team('T50', 'OAK', 'Oakland', 'Athletics'),
    _team('T51', 'PHI', 'Philadelphia', 'Phillies'),
    _team('T52', 'PIT', 'Pittsburgh', 'Pirates'),
    _team('T53', 'SD', 'San Diego', 'Padres'),
    _team('T54', 'SEA', 'Seattle', 'Mariners'),
    _team('T55', 'SF', 'San Francisco', 'Giants'),
    _team('T56', 'STL', 'St. Louis', 'Cardinals'),
    _team('T57', 'TB', 'Tampa Bay', 'Rays'),
    _team('T58', 'TEX', 'Texas', 'Rangers'),
    _team('T59', 'TOR', 'Toronto', 'Blue Jays'),
    _team('T60', 'WAS', 'Washington', 'Nationals'),
    _team('TCH', '', 'Chicago', ''),
    _team('TNY', '', 'New York', ''),
    _team('TLA', '', 'Los Angeles', ''),
]


def _map(k, vs):
    return {t[k]: {v: t[v] for v in vs if t[v]} for t in TEAMS if t[k]}


def _repl(f, m):
    a = m.group(0)
    b = f(a)
    return b if b else a


def _sub(ks, f, s):
    pattern = '|'.join(ks)
    return re.sub(pattern, partial(_repl, f), s)


DECODING_MAP = _map('decoding', ['encoding'])

ENCODING_MAP = _map('encoding', [
    'abbreviation',
    'decoding',
    'encodings',
    'hometown',
    'nickname',
    'teamid',
])

PRECODING_MAP = _map('precoding', ['encoding'])

ICON_LINK = 'https://fairylab.surge.sh/images/teams/{0}/{0}-icon.png'
MODAL_LINK = ' data-toggle="modal" data-target="#{0}"'
BADGE_TAG = '<span class="badge badge-icon badge-light"{0}>{1}</span>'
IMG_TAG = '<img src="{0}" width="{1}" height="{1}" border="0" class="{2}">'
SPAN_TAG = '<span class="{1}">{0}</span>'


def decoding_to_encoding(decoding):
    return DECODING_MAP.get(decoding, {}).get('encoding', '')


def decoding_to_encoding_sub(text):
    return _sub(DECODING_KEYS, decoding_to_encoding, text)


def encoding_keys():
    return ENCODING_KEYS


def encoding_to_abbreviation(encoding):
    return ENCODING_MAP.get(encoding, {}).get('abbreviation', '')


def encoding_to_decoding(encoding):
    return ENCODING_MAP.get(encoding, {}).get('decoding', '')


def encoding_to_decoding_sub(text):
    return _sub(ENCODING_KEYS, encoding_to_decoding, text)


def encoding_to_encodings(encoding):
    return ENCODING_MAP.get(encoding, {}).get('encodings', '')


def encoding_to_hometown(encoding):
    return ENCODING_MAP.get(encoding, {}).get('hometown', '')


def encoding_to_hometown_sub(text):
    return _sub(ENCODING_KEYS, encoding_to_hometown, text)


def encoding_to_nickname(encoding):
    return ENCODING_MAP.get(encoding, {}).get('nickname', '')


def encoding_to_teamid(encoding):
    return ENCODING_MAP.get(encoding, {}).get('teamid', '')


def icon_absolute(encoding, text, size):
    name = encoding_to_nickname(encoding).replace(' ', '').lower()
    ic = 'position-absolute left-8p top-14p'
    sc = 'd-block text-truncate pl-24p'

    img = IMG_TAG.format(ICON_LINK.format(name), size, ic)
    span = SPAN_TAG.format(text, sc)
    return img + span


def icon_badge(encoding, text, active, size):
    name = encoding_to_nickname(encoding).replace(' ', '').lower()
    teamid = encoding_to_teamid(encoding)
    ic = 'd-inline-block'
    sc = 'd-inline-block align-middle px-2 pt-1'

    if active:
        ba = MODAL_LINK.format(teamid)
        if text == '0-0':
            text = '?-?'
    else:
        ba = ''
        ic += ' grayscale'
        sc += ' text-secondary'

    img = IMG_TAG.format(ICON_LINK.format(name), size, ic)
    span = SPAN_TAG.format(text, sc)
    return BADGE_TAG.format(ba, img + span)


def precoding_to_encoding(precoding):
    return PRECODING_MAP.get(precoding, {}).get('encoding', '')


def precoding_to_encoding_sub(text):
    return _sub(PRECODING_KEYS, precoding_to_encoding, text)


DECODING_KEYS = list(sorted(DECODING_MAP.keys()))
ENCODING_KEYS = list(sorted(ENCODING_MAP.keys()))
PRECODING_KEYS = list(sorted(PRECODING_MAP.keys()))
