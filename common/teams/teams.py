#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Common (non-reloadable) util methods for team information."""

import re
from functools import partial


def _team(encoding, hometown, nickname):
    special1 = encoding in ['TCH', 'TLA', 'TNY']
    special2 = encoding in ['T35', 'T36', 'T44', 'T45', 'T48', 'T49']

    return {
        'decoding': (hometown + ' ' + nickname) if not special1 else '',
        'encoding': encoding,
        'hometown': hometown if not special1 else '',
        'nickname': nickname,
        'precoding': hometown if not special2 else '',
        'teamid': encoding.strip('T') if not special1 else '',
    }


TEAMS = [
    _team('T31', 'Arizona', 'Diamondbacks'),
    _team('T32', 'Atlanta', 'Braves'),
    _team('T33', 'Baltimore', 'Orioles'),
    _team('T34', 'Boston', 'Red Sox'),
    _team('T35', 'Chicago', 'White Sox'),
    _team('T36', 'Chicago', 'Cubs'),
    _team('T37', 'Cincinnati', 'Reds'),
    _team('T38', 'Cleveland', 'Indians'),
    _team('T39', 'Colorado', 'Rockies'),
    _team('T40', 'Detroit', 'Tigers'),
    _team('T41', 'Miami', 'Marlins'),
    _team('T42', 'Houston', 'Astros'),
    _team('T43', 'Kansas City', 'Royals'),
    _team('T44', 'Los Angeles', 'Angels'),
    _team('T45', 'Los Angeles', 'Dodgers'),
    _team('T46', 'Milwaukee', 'Brewers'),
    _team('T47', 'Minnesota', 'Twins'),
    _team('T48', 'New York', 'Yankees'),
    _team('T49', 'New York', 'Mets'),
    _team('T50', 'Oakland', 'Athletics'),
    _team('T51', 'Philadelphia', 'Phillies'),
    _team('T52', 'Pittsburgh', 'Pirates'),
    _team('T53', 'San Diego', 'Padres'),
    _team('T54', 'Seattle', 'Mariners'),
    _team('T55', 'San Francisco', 'Giants'),
    _team('T56', 'St. Louis', 'Cardinals'),
    _team('T57', 'Tampa Bay', 'Rays'),
    _team('T58', 'Texas', 'Rangers'),
    _team('T59', 'Toronto', 'Blue Jays'),
    _team('T60', 'Washington', 'Nationals'),
    _team('TCH', 'Chicago', ''),
    _team('TNY', 'New York', ''),
    _team('TLA', 'Los Angeles', ''),
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
    'decoding',
    'hometown',
    'nickname',
    'teamid',
])

PRECODING_MAP = _map('precoding', ['encoding'])

ICON_LINK = 'https://fairylab.surge.sh/images/teams/{0}/{0}-icon.png'
IMG_TAG = '<img src="{0}" width="20" height="20" border="0" class="{1}">'
SPAN_TAG = '<span class="align-middle {1}">{0}</span>'


def decoding_to_encoding(decoding):
    return DECODING_MAP.get(decoding, {}).get('encoding', '')


def decoding_to_encoding_sub(text):
    return _sub(DECODING_KEYS, decoding_to_encoding, text)


def encoding_keys():
    return ENCODING_KEYS


def encoding_to_decoding(encoding):
    return ENCODING_MAP.get(encoding, {}).get('decoding', '')


def encoding_to_decoding_sub(text):
    return _sub(ENCODING_KEYS, encoding_to_decoding, text)


def encoding_to_hometown(encoding):
    return ENCODING_MAP.get(encoding, {}).get('hometown', '')


def encoding_to_nickname(encoding):
    return ENCODING_MAP.get(encoding, {}).get('nickname', '')


def encoding_to_teamid(encoding):
    return ENCODING_MAP.get(encoding, {}).get('teamid', '')


def icon_absolute(encoding, text, side):
    name = encoding_to_nickname(encoding).replace(' ', '').lower()
    src = ICON_LINK.format(name)

    ic = 'position-absolute {}-8p top-14p'.format(side)
    sc = 'd-block text-truncate p{}-24p'.format(side[0])

    img = IMG_TAG.format(src, ic)
    span = SPAN_TAG.format(text, sc)
    return img + span


def icon_inline(encoding, text):
    name = encoding_to_nickname(encoding).replace(' ', '').lower()
    src = ICON_LINK.format(name)

    img = IMG_TAG.format(src, 'd-inline-block')
    span = SPAN_TAG.format(text, 'd-inline-block px-2')
    return img + span


def precoding_to_encoding(precoding):
    return PRECODING_MAP.get(precoding, {}).get('encoding', '')


def precoding_to_encoding_sub(text):
    return _sub(PRECODING_KEYS, precoding_to_encoding, text)


DECODING_KEYS = list(sorted(DECODING_MAP.keys()))
ENCODING_KEYS = list(sorted(ENCODING_MAP.keys()))
PRECODING_KEYS = list(sorted(PRECODING_MAP.keys()))
