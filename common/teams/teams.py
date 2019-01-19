#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Common (non-reloadable) util methods for team information."""

import random
import re
from functools import partial


def _team(encoding, abbreviation, hometown, nickname, repo, tag, *alternates):
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
        'alternates': alternates,
        'colors': [alternate[0] for alternate in alternates],
        'decoding': (hometown + ' ' + nickname) if not special1 else '',
        'encoding': encoding,
        'encodings': encodings,
        'hometown': hometown,
        'lower': nickname.replace(' ', '').lower(),
        'nickname': nickname,
        'precoding': hometown if not special2 else '',
        'repo': repo,
        'tag': tag,
        'teamid': encoding.strip('T') if not special1 else '',
    }


BLACK = 'black'
BLUE = 'blue'
CREAM = 'cream'
GREEN = 'green'
GREY = 'grey'
ORANGE = 'orange'
PURPLE = 'purple'
RED = 'red'
SKY = 'sky'
WHITE = 'white'
YELLOW = 'yellow'

MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = range(7)
WEEKDAYS = [MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY]
ALL = WEEKDAYS + [SATURDAY, SUNDAY]

TEAMS = [
    _team('T31', 'ARI', 'Arizona', 'Diamondbacks',
          '925f81153b44d0b35734ca0c43b9f89a',
          'e46d3919da84e127c46ddb9a98083fdfe45c550e',
          (RED, [SUNDAY], 1.0, 'home|away')),
    _team('T32', 'ATL', 'Atlanta', 'Braves',
          '70fe783889494c2c0de8cd9b2dbd05b2',
          'af5e8226f04e295506a61636aaf6d405c6d24a54',
          (CREAM, [SUNDAY], 1.0, 'home'),
          (BLUE, ALL, .5, 'away')),
    _team('T33', 'BAL', 'Baltimore', 'Orioles',
          '6df0d030fbb62f9cd169624afe5351e3',
          'f9576bb0aa8427c19832bb972962b86c3a6cb1f2',
          (BLACK, [FRIDAY], 1.0, 'home|away'),
          (ORANGE, [SATURDAY], 1.0, 'home|away')),
    _team('T34', 'BOS', 'Boston', 'Red Sox',
          '4a6a4036834b558756dac7ac9c0309d0',
          'b370f4842d7d271d9935f30d231abe0368409944',
          (RED, [FRIDAY], 1.0, 'home'),
          (BLUE, [FRIDAY], 1.0, 'away')),
    _team('T35', 'CWS', 'Chicago', 'White Sox',
          '359d34636fabc914a83a8c746fc6eba9',
          '1afa211b3cec808c7d58863fd61d436bbdbe05da',
          (BLUE, [SUNDAY], 1.0, 'home'),
          (BLACK, ALL, .6, 'home|away')),
    _team('T36', 'CHC', 'Chicago', 'Cubs',
          'ed81fde94a24fdce340a19e52fda33bd',
          'cf6811a0707e24be1ef2038f91cc295525274cf6',
          (BLUE, [SUNDAY], 1.0, 'home|away')),
    _team('T37', 'CIN', 'Cincinnati', 'Reds',
          'af532f33900c377ea6a7d5c373a9785f',
          '8eb50b108f9f65dfcc71b30ddb3b9ab032a972c1',
          (RED, ALL, .35, 'home')),
    _team('T38', 'CLE', 'Cleveland', 'Indians',
          '40b0331a059d0ad8869df7e101863401',
          '39c4825ca85027191a3003528ce36ab6c85bf537',
          (BLUE, ALL, .6, 'home|away')),
    _team('T39', 'COL', 'Colorado', 'Rockies',
          '79886209567ba70e64192b9810bde6a3',
          'ed1def95cd767f6c4e0601b6dd440d58f365e894',
          (PURPLE, ALL, .35, 'home|away'),
          (BLACK, ALL, .15, 'home|away')),
    _team('T40', 'DET', 'Detroit', 'Tigers',
          '89a0edfe4287648effd8021807ef9625',
          '2a80951e810dccdb569fc2f249e3fb8c00675000',
          (BLUE, ALL, .6, 'home'),
          (ORANGE, ALL, .5, 'away')),
    _team('T41', 'MIA', 'Miami', 'Marlins',
          '793744dc81800fea7f219dd22b28afa1',
          'b2fe8e13546351a7272f1b90d066b398620adcac'),
    _team('T42', 'HOU', 'Houston', 'Astros',
          '2d3444f09ba1f0c9a06b6e9bdd27eda7',
          'b19253b93017682124fe778e0a8624c12bcc6332',
          (ORANGE, ALL, .2, 'home|away')),
    _team('T43', 'KC', 'Kansas City', 'Royals',
          'f87f4b6bf4821f16ef57eae0823e9fc7',
          '1f8528c7ec317d89f3e7ba6de2b3c3dd7340f64c',
          (SKY, [MONDAY, FRIDAY], 1.0, 'home'),
          (BLUE, [SUNDAY], 1.0, 'away')),
    _team('T44', 'LAA', 'Los Angeles', 'Angels',
          '9780ce2762db67b17831a0c908aaf725',
          '1018f1ba85a160d74d5a924749a6cd28cae44a40',
          (RED, ALL, .55, 'home|away')),
    _team('T45', 'LAD', 'Los Angeles', 'Dodgers',
          'd334f966fa470e01991d550266b94283',
          '4572edb247c3b7281f01cf01e0ee97f34a14e145'),
    _team('T46', 'MIL', 'Milwaukee', 'Brewers',
          '5aa56738ca8fc3f8367d6f777614de38',
          '854c03ddbbd38842ee7e62f825b0dcd97cb9d391',
          (SKY, [SATURDAY, SUNDAY], 1.0, 'home|away')),
    _team('T47', 'MIN', 'Minnesota', 'Twins',
          '5b5568f5e186885d5e5175a25959f5d0',
          '278276af922a94ee6396cace99f17c3a308da730',
          (CREAM, WEEKDAYS, 1.0, 'home'),
          (BLUE, ALL, .15, 'away')),
    _team('T48', 'NYY', 'New York', 'Yankees',
          '5b8b9a01333351a92f6f91726dce239b',
          '0cfd7978330ee9e4c4c4fa37439b9abb903be46a'),
    _team('T49', 'NYM', 'New York', 'Mets',
          'aa9197d99dd2abcb7a50f13e5ae75ab0',
          'b209622a6f5849a60035cd3f583914bb557fb514',
          (BLACK, ALL, .25, 'home'),
          (BLUE, ALL, .25, 'away')),
    _team('T50', 'OAK', 'Oakland', 'Athletics',
          '5641c5488e3de552ebd8f04c7d089fd9',
          'f62eb1e611dcb85832aa9cfc2ea1165a99325beb',
          (YELLOW, [FRIDAY], 1.0, 'home'),
          (GREEN, ALL, .15, 'away')),
    _team('T51', 'PHI', 'Philadelphia', 'Phillies',
          '21cdbe29a981ae9e9eeeccbd93b7e76e',
          '44bdf456e169c959be199c0030228077a7104c1e',
          (SKY, [THURSDAY], 1.0, 'home'),
          (CREAM, [SUNDAY], 1.0, 'home')),
    _team('T52', 'PIT', 'Pittsburgh', 'Pirates',
          'b52b416175cd704f7dd007d890dd629e',
          'a3771c5794f7677c45b99bc467af7fa87ab26d6d',
          (YELLOW, [SUNDAY], 1.0, 'home'),
          (BLACK, ALL, .4, 'home|away')),
    _team('T53', 'SD', 'San Diego', 'Padres',
          'a2ae8f3ef490bad2f2f5510428d4bdc2',
          'b9c65c44cca5eab7453ae85ac728e27ae7416b67',
          (CREAM, [SUNDAY], 1.0, 'home'),
          (YELLOW, ALL, .35, 'away')),
    _team('T54', 'SEA', 'Seattle', 'Mariners',
          '146290fc1036d7628d016218e9a05a92',
          '6a6f13694db39de9d335e25661138a4f14ccf4ab',
          (GREEN, [FRIDAY], 1.0, 'home'),
          (BLUE, ALL, .45, 'away')),
    _team('T55', 'SF', 'San Francisco', 'Giants',
          'd82f716325270e162d646bbaa7160c8b',
          'f5c7a0e63b18cfaef3aff919f1c74d60719f5747',
          (ORANGE, [FRIDAY], 1.0, 'home')),
    _team('T56', 'STL', 'St. Louis', 'Cardinals',
          '2f8467f7cef50d56217cd0bd4da65ca0',
          'b854738755e6572c1aec7ca65a16b1030a4c3b53',
          (CREAM, [SATURDAY], 1.0, 'home')),
    _team('T57', 'TB', 'Tampa Bay', 'Rays',
          '72da90820a526e10bad1484efd2aaea3',
          '9596cda701c2d5af036d726e2547db65dfcda134',
          (SKY, [SUNDAY], 1.0, 'home'),
          (BLUE, ALL, .5, 'away')),
    _team('T58', 'TEX', 'Texas', 'Rangers',
          '468cead9ea12e6bb3ba6f62236b8d1a7',
          '80fb2958b8e027e2d8a8097bcb7cd4b3bd9bfe13',
          (SKY, [SUNDAY], 1.0, 'home'),
          (BLUE, ALL, .5, 'home|away')),
    _team('T59', 'TOR', 'Toronto', 'Blue Jays',
          '75833b35b51c8b6cd5c300e0d4117739',
          'ac65ce092e906593e512d3452a38c2e5668f8447',
          (BLUE, ALL, .5, 'home|away')),
    _team('T60', 'WAS', 'Washington', 'Nationals',
          '7364eac50fccbb97ce1ea034da8e3c6a',
          '47d7dae296e3b5d262e9dca3effad546969670f1',
          (BLUE, [FRIDAY], 1.0, 'home|away'),
          (RED, [SUNDAY], 1.0, 'home|away')),
    _team('TCH', '', 'Chicago', '', '', ''),
    _team('TNY', '', 'New York', '', '', ''),
    _team('TLA', '', 'Los Angeles', '', '', ''),
]  # yapf: disable


def _map(k, vs):
    return {t[k]: {v: t[v] for v in vs if t[v]} for t in TEAMS if t[k]}


def _repl(f, m):
    a = m.group(0)
    b = f(a)
    return b if b else a


def _sub(ks, f, s):
    pattern = '|'.join(ks)
    return re.sub(pattern, partial(_repl, f), s)


CLASH_LIST = [
    (BLACK, BLUE, GREEN, PURPLE),
    (CREAM, WHITE),
    (GREY),
    (ORANGE, RED, YELLOW),
    (SKY),
]
CLASH_MAP = {k: (set(c) - set((k, ))) for c in CLASH_LIST for k in c}

DECODING_MAP = _map('decoding', ['encoding'])

ENCODING_MAP = _map('encoding', [
    'abbreviation',
    'alternates',
    'colors',
    'decoding',
    'encodings',
    'hometown',
    'lower',
    'nickname',
    'repo',
    'tag',
    'teamid',
])

PRECODING_MAP = _map('precoding', ['encoding'])

ICON_LINK = 'https://fairylab.surge.sh/images/teams/{0}/{0}-icon.png'
MODAL_LINK = ' data-toggle="modal" data-target="#{0}"'
BADGE_TAG = '<span class="badge badge-icon badge-light"{0}>{1}</span>'
DIV_TAG = '<div class="{}"></div>'
IMG_TAG = '<img src="{0}" width="{1}" height="{1}" border="0" class="{2}">'
SPAN_TAG = '<span class="{1}">{0}</span>'

FAIRYLAB = 'https://fairylab.surge.sh/images/teams'
GISTCDN = 'https://gistcdn.githack.com/brunner'
GRADIENT = 'linear-gradient(transparent, transparent)'
JERSEY_STYLE = """.jersey {
  background-size: 78px 80px;
  border: 1px solid #eeeff0;
  height: 82px;
  margin: -5px -1px -5px -5px;
  width: 80px;
}"""
SIDE_STYLE = """.{3}-{4}-{5} {{{{
  background: url('{0}/{0}/{3}-{4}-{5}.png');
  background: url('{1}/{6}/raw/{7}/{3}-{4}-{5}.svg'), {2};
}}}}""".format(FAIRYLAB, GISTCDN, GRADIENT, '{0}', '{1}', '{4}', '{2}', '{3}')


def _color_name(color):
    if color == GREY:
        return 'away'
    elif color == WHITE:
        return 'home'
    return 'alt-' + color


def _encoding_to_lower(encoding):
    return ENCODING_MAP.get(encoding, {}).get('lower', '')


def _encoding_to_repo(encoding):
    return ENCODING_MAP.get(encoding, {}).get('repo', '')


def _encoding_to_tag(encoding):
    return ENCODING_MAP.get(encoding, {}).get('tag', '')


def decoding_to_encoding(decoding):
    return DECODING_MAP.get(decoding, {}).get('encoding', '')


def decoding_to_encoding_sub(text):
    return _sub(DECODING_KEYS, decoding_to_encoding, text)


def encoding_keys():
    return ENCODING_KEYS


def encoding_to_abbreviation(encoding):
    return ENCODING_MAP.get(encoding, {}).get('abbreviation', '')


def encoding_to_alternates(encoding):
    return ENCODING_MAP.get(encoding, {}).get('alternates', '')


def encoding_to_colors(encoding):
    return ENCODING_MAP.get(encoding, {}).get('colors', [])


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
    lower = _encoding_to_lower(encoding)
    ic = 'position-absolute left-8p top-14p'
    sc = 'd-block text-truncate pl-24p'

    img = IMG_TAG.format(ICON_LINK.format(lower), size, ic)
    span = SPAN_TAG.format(text, sc)
    return img + span


def icon_badge(encoding, text, active, size):
    lower = _encoding_to_lower(encoding)
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

    img = IMG_TAG.format(ICON_LINK.format(lower), size, ic)
    span = SPAN_TAG.format(text, sc)
    return BADGE_TAG.format(ba, img + span)


def jersey_absolute(encoding, color, side):
    lower = _encoding_to_lower(encoding)

    if color == GREY:
        name = 'away'
    elif color == WHITE:
        name = 'home'
    else:
        name = 'alt-' + color

    dc = 'jersey position-absolute ' + '-'.join([lower, name, side])
    return DIV_TAG.format(dc)


def jersey_color(encoding, day, team, clash):
    alternates = encoding_to_alternates(encoding)
    for color, days, pct, teams in alternates:
        if color in CLASH_MAP.get(clash, {}):
            continue
        if day not in days:
            continue
        if pct < random.random():
            continue
        if not re.search(teams, team):
            continue

        return color

    if team == 'home':
        return WHITE
    return GREY


def jersey_style(*jerseys):
    styles = []
    for encoding, color in jerseys:
        lower = _encoding_to_lower(encoding)
        name = _color_name(color)
        repo = _encoding_to_repo(encoding)
        tag = _encoding_to_tag(encoding)

        for side in ['front', 'back']:
            styles.append(SIDE_STYLE.format(lower, name, repo, tag, side))

    styles.append(JERSEY_STYLE)
    return '\n'.join(styles)


def precoding_to_encoding(precoding):
    return PRECODING_MAP.get(precoding, {}).get('encoding', '')


def precoding_to_encoding_sub(text):
    return _sub(PRECODING_KEYS, precoding_to_encoding, text)


DECODING_KEYS = list(sorted(DECODING_MAP.keys()))
ENCODING_KEYS = list(sorted(ENCODING_MAP.keys()))
PRECODING_KEYS = list(sorted(PRECODING_MAP.keys()))
