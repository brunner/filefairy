#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Common (non-reloadable) util methods for team information."""

import os
import random
import re
import sys
from functools import partial

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/common/teams', '', _path))

from common.elements.elements import ruleset  # noqa


def _team(encoding, abbreviation, hometown, nickname, repo, tag, home, away,
          *alternates):
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
        'away': away,
        'colors': [home, away] + [alternate[:4] for alternate in alternates],
        'decoding': (hometown + ' ' + nickname) if not special1 else '',
        'encoding': encoding,
        'encodings': encodings,
        'home': home,
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
          (WHITE, '#cb0c29', '#000000', 'block'),
          (GREY, '#cb0c29', '#e79d94', 'block'),
          (RED, '#000000', '#e79d94', 'block', [SUNDAY], 1.0, 'home|away')),
    _team('T32', 'ATL', 'Atlanta', 'Braves',
          '70fe783889494c2c0de8cd9b2dbd05b2',
          'af5e8226f04e295506a61636aaf6d405c6d24a54',
          (WHITE, '#ab1234', '#0b2c5a', 'block'),
          (GREY, '#ab1234', '#0b2c5a', 'block'),
          (CREAM, '#ab1234', '#0b2c5a', 'block', [SUNDAY], 1.0, 'home'),
          (BLUE, '#0b2c5a', '#ffffff', 'block', ALL, .5, 'away')),
    _team('T33', 'BAL', 'Baltimore', 'Orioles',
          '6df0d030fbb62f9cd169624afe5351e3',
          'f9576bb0aa8427c19832bb972962b86c3a6cb1f2',
          (WHITE, '#f94900', '#000000', 'block'),
          (GREY, '#f94900', '#000000', 'block'),
          (BLACK, '#f94900', '#983206', 'block', [FRIDAY], 1.0, 'home|away'),
          (ORANGE, '#000000', '#ffffff', 'block', [SATURDAY], 1.0, 'home|away')),
    _team('T34', 'BOS', 'Boston', 'Red Sox',
          '4a6a4036834b558756dac7ac9c0309d0',
          'b370f4842d7d271d9935f30d231abe0368409944',
          (WHITE, '#d5122f', '#09285a', 'block'),
          (GREY, '#d5122f', '#09285a', 'block'),
          (RED, '#09285a', '#ffffff', 'block', [FRIDAY], 1.0, 'home'),
          (BLUE, '#d5122f', '#ffffff', 'block', [FRIDAY], 1.0, 'away')),
    _team('T35', 'CWS', 'Chicago', 'White Sox',
          '359d34636fabc914a83a8c746fc6eba9',
          '1afa211b3cec808c7d58863fd61d436bbdbe05da',
          (WHITE, '#000000', '#d0cfd1', 'block'),
          (GREY, '#000000', '#ffffff', 'block'),
          (BLUE, '#09285a', '#9d9f9f', 'block', [SUNDAY], 1.0, 'home'),
          (BLACK, '#ffffff', '#d0cfd1', 'block', ALL, .6, 'home|away')),
    _team('T36', 'CHC', 'Chicago', 'Cubs',
          'ed81fde94a24fdce340a19e52fda33bd',
          'cf6811a0707e24be1ef2038f91cc295525274cf6',
          (WHITE, '#122441', '#9da3aa', 'block'),
          (GREY, '#122441', '#63625f', 'block'),
          (BLUE, '#ffffff', '#000000', 'block', [SUNDAY], 1.0, 'home|away')),
    _team('T37', 'CIN', 'Cincinnati', 'Reds',
          'af532f33900c377ea6a7d5c373a9785f',
          '8eb50b108f9f65dfcc71b30ddb3b9ab032a972c1',
          (WHITE, '#ea164c', '#000000', 'block'),
          (GREY, '#ea164c', '#000000', 'block'),
          (RED, '#ffffff', '#000000', 'block', ALL, .35, 'home')),
    _team('T38', 'CLE', 'Cleveland', 'Indians',
          '40b0331a059d0ad8869df7e101863401',
          '39c4825ca85027191a3003528ce36ab6c85bf537',
          (WHITE, '#e9144b', '#09295c', 'block'),
          (GREY, '#09295c', '#e9144b', 'block'),
          (BLUE, '#e9144b', '#ffffff', 'block', ALL, .6, 'home|away')),
    _team('T39', 'COL', 'Colorado', 'Rockies',
          '79886209567ba70e64192b9810bde6a3',
          'ed1def95cd767f6c4e0601b6dd440d58f365e894',
          (WHITE, '#000000', '#a5a4a8', 'block'),
          (GREY, '#000000', '#ffffff', 'block'),
          (PURPLE, '#000000', '#ffffff', 'block', ALL, .35, 'home|away'),
          (BLACK, '#a5a4a8', '#3b3583', 'block', ALL, .15, 'home|away')),
    _team('T40', 'DET', 'Detroit', 'Tigers',
          '89a0edfe4287648effd8021807ef9625',
          '2a80951e810dccdb569fc2f249e3fb8c00675000',
          (WHITE, '#0b2245', '#e54927', 'block'),
          (GREY, '#0b2245', '#e54927', 'block'),
          (BLUE, '#ffffff', '#e54927', 'block', ALL, .6, 'home'),
          (ORANGE, '#0b2245', '#ffffff', 'block', ALL, .5, 'away')),
    _team('T41', 'MIA', 'Miami', 'Marlins',
          '793744dc81800fea7f219dd22b28afa1',
          'b2fe8e13546351a7272f1b90d066b398620adcac',
          (WHITE, '#000000', '#27aab8', 'block'),
          (GREY, '#000000', '#27aab8', 'block')),
    _team('T42', 'HOU', 'Houston', 'Astros',
          '2d3444f09ba1f0c9a06b6e9bdd27eda7',
          'b19253b93017682124fe778e0a8624c12bcc6332',
          (WHITE, '#141929', '#aa563e', 'block'),
          (GREY, '#141929', '#aa563e', 'block'),
          (ORANGE, '#141929', '#ffffff', 'block', ALL, .2, 'home|away')),
    _team('T43', 'KC', 'Kansas City', 'Royals',
          'f87f4b6bf4821f16ef57eae0823e9fc7',
          '1f8528c7ec317d89f3e7ba6de2b3c3dd7340f64c',
          (WHITE, '#0d326f', '#6a86a4', 'block'),
          (GREY, '#0d326f', '#6a86a4', 'block'),
          (SKY, '#ffffff', '#0d326f', 'block', [MONDAY, FRIDAY], 1.0, 'home'),
          (BLUE, '#ffffff', '#6a86a4', 'block', [SUNDAY], 1.0, 'away')),
    _team('T44', 'LAA', 'Los Angeles', 'Angels',
          '9780ce2762db67b17831a0c908aaf725',
          '1018f1ba85a160d74d5a924749a6cd28cae44a40',
          (WHITE, '#b11132', '#0c2445', 'block'),
          (GREY, '#b11132', '#0c2445', 'block'),
          (RED, '#b11132', '#0c2445', 'block', ALL, .55, 'home|away')),
    _team('T45', 'LAD', 'Los Angeles', 'Dodgers',
          'd334f966fa470e01991d550266b94283',
          '4572edb247c3b7281f01cf01e0ee97f34a14e145',
          (WHITE, '#233972', '#55678b', 'block'),
          (GREY, '#233972', '#55678b', 'block')),
    _team('T46', 'MIL', 'Milwaukee', 'Brewers',
          '5aa56738ca8fc3f8367d6f777614de38',
          '854c03ddbbd38842ee7e62f825b0dcd97cb9d391',
          (WHITE, '#1a4ba7', '#fbc72d', 'block'),
          (GREY, '#1a4ba7', '#fbc72d', 'block'),
          (SKY, '#1a4ba7', '#fbc72d', 'block', [SATURDAY, SUNDAY], 1.0, 'home|away')),
    _team('T47', 'MIN', 'Minnesota', 'Twins',
          '5b5568f5e186885d5e5175a25959f5d0',
          '278276af922a94ee6396cace99f17c3a308da730',
          (WHITE, '#d11242', '#052046', 'block'),
          (GREY, '#052046', '#d11242', 'block'),
          (CREAM, '#052046', '#d11242', 'block', WEEKDAYS, 1.0, 'home'),
          (BLUE, '#d11242', '#d0718f', 'block', ALL, .15, 'away')),
    _team('T48', 'NYY', 'New York', 'Yankees',
          '5b8b9a01333351a92f6f91726dce239b',
          '0cfd7978330ee9e4c4c4fa37439b9abb903be46a',
          (WHITE, '#051e42', '#7087a3', 'block'),
          (GREY, '#051e42', '#ffffff', 'block')),
    _team('T49', 'NYM', 'New York', 'Mets',
          'aa9197d99dd2abcb7a50f13e5ae75ab0',
          'b209622a6f5849a60035cd3f583914bb557fb514',
          (WHITE, '#144a8b', '#d57437', 'block'),
          (GREY, '#253b76', '#c45d3b', 'block'),
          (BLACK, '#144a8b', '#d57437', 'block', ALL, .25, 'home'),
          (BLUE, '#a4a1a1', '#c45d3b', 'block', ALL, .25, 'away')),
    _team('T50', 'OAK', 'Oakland', 'Athletics',
          '5641c5488e3de552ebd8f04c7d089fd9',
          'f62eb1e611dcb85832aa9cfc2ea1165a99325beb',
          (WHITE, '#064436', '#f0b019', 'block'),
          (GREY, '#064436', '#f0b019', 'block'),
          (YELLOW, '#064436', '#ffffff', 'block', [FRIDAY], 1.0, 'home'),
          (GREEN, '#ffffff', '#f0b019', 'block', ALL, .15, 'away')),
    _team('T51', 'PHI', 'Philadelphia', 'Phillies',
          '21cdbe29a981ae9e9eeeccbd93b7e76e',
          '44bdf456e169c959be199c0030228077a7104c1e',
          (WHITE, '#d11043', '#e37792', 'block'),
          (GREY, '#d11043', '#e37792', 'block'),
          (SKY, '#6d223a', '#ffffff', 'block', [THURSDAY], 1.0, 'home'),
          (CREAM, '#d11043', '#165397', 'block', [SUNDAY], 1.0, 'home')),
    _team('T52', 'PIT', 'Pittsburgh', 'Pirates',
          'b52b416175cd704f7dd007d890dd629e',
          'a3771c5794f7677c45b99bc467af7fa87ab26d6d',
          (WHITE, '#000000', '#fcc72d', 'block'),
          (GREY, '#000000', '#fcc72d', 'block'),
          (YELLOW, '#000000', '#ffffff', 'block', [SUNDAY], 1.0, 'home'),
          (BLACK, '#fcc72d', '#ffffff', 'block', ALL, .4, 'home|away')),
    _team('T53', 'SD', 'San Diego', 'Padres',
          'a2ae8f3ef490bad2f2f5510428d4bdc2',
          'b9c65c44cca5eab7453ae85ac728e27ae7416b67',
          (WHITE, '#512c1b', '#f0aa1c', 'block'),
          (GREY, '#512c1b', '#f0aa1c', 'block'),
          (CREAM, '#512c1b', '#f0aa1c', 'block', [SUNDAY], 1.0, 'home'),
          (YELLOW, '#512c1b', '#704f33', 'block', ALL, .35, 'away')),
    _team('T54', 'SEA', 'Seattle', 'Mariners',
          '146290fc1036d7628d016218e9a05a92',
          '6a6f13694db39de9d335e25661138a4f14ccf4ab',
          (WHITE, '#09285a', '#0b505a', 'block'),
          (GREY, '#09285a', '#0b505a', 'block'),
          (GREEN, '#c9d0d1', '#09285a', 'block', [FRIDAY], 1.0, 'home'),
          (BLUE, '#c9d0d1', '#0b505a', 'block', ALL, .45, 'away')),
    _team('T55', 'SF', 'San Francisco', 'Giants',
          'd82f716325270e162d646bbaa7160c8b',
          'f5c7a0e63b18cfaef3aff919f1c74d60719f5747',
          (WHITE, '#000000', '#c85633', 'block'),
          (GREY, '#000000', '#c85633', 'block'),
          (ORANGE, '#000000', '#ffffff', 'block', [FRIDAY], 1.0, 'home')),
    _team('T56', 'STL', 'St. Louis', 'Cardinals',
          '2f8467f7cef50d56217cd0bd4da65ca0',
          'b854738755e6572c1aec7ca65a16b1030a4c3b53',
          (WHITE, '#d11043', '#0c2340', 'block'),
          (GREY, '#d11043', '#0c2340', 'block'),
          (CREAM, '#d11043', '#0c2340', 'block', [SATURDAY], 1.0, 'home')),
    _team('T57', 'TB', 'Tampa Bay', 'Rays',
          '72da90820a526e10bad1484efd2aaea3',
          '9596cda701c2d5af036d726e2547db65dfcda134',
          (WHITE, '#08131e', '#0a2b5f', 'block'),
          (GREY, '#08131e', '#0a2b5f', 'block'),
          (SKY, '#09255c', '#fcc520', 'block', [SUNDAY], 1.0, 'home'),
          (BLUE, '#74b5e1', '#09255c', 'block', ALL, .5, 'away')),
    _team('T58', 'TEX', 'Texas', 'Rangers',
          '468cead9ea12e6bb3ba6f62236b8d1a7',
          '80fb2958b8e027e2d8a8097bcb7cd4b3bd9bfe13',
          (WHITE, '#124886', '#ce103b', 'block'),
          (GREY, '#124886', '#ce103b', 'block'),
          (SKY, '#e60021', '#ffffff', 'block', [SUNDAY], 1.0, 'home'),
          (BLUE, '#ffffff', '#ce103b', 'block', ALL, .5, 'home|away')),
    _team('T59', 'TOR', 'Toronto', 'Blue Jays',
          '75833b35b51c8b6cd5c300e0d4117739',
          'ac65ce092e906593e512d3452a38c2e5668f8447',
          (WHITE, '#1d469b', '#122856', 'block'),
          (GREY, '#1d469b', '#122856', 'block'),
          (BLUE, '#ffffff', '#122856', 'block', ALL, .5, 'home|away')),
    _team('T60', 'WAS', 'Washington', 'Nationals',
          '7364eac50fccbb97ce1ea034da8e3c6a',
          '47d7dae296e3b5d262e9dca3effad546969670f1',
          (WHITE, '#b10b30', '#0a2045', 'block'),
          (GREY, '#b10b30', '#0a2045', 'block'),
          (BLUE, '#b10b30', '#ffffff', 'block', [FRIDAY], 1.0, 'home|away'),
          (RED, '#ffffff', '#0a2045', 'block', [SUNDAY], 1.0, 'home|away')),
    _team('TCH', '', 'Chicago', '', '', '', None, None),
    _team('TNY', '', 'New York', '', '', '', None, None),
    _team('TLA', '', 'Los Angeles', '', '', '', None, None),
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
    'away',
    'colors',
    'decoding',
    'encodings',
    'home',
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

JERSEY_KWARGS = {
    'fairylab': 'https://fairylab.surge.sh/images/teams',
    'gist': 'https://gistcdn.githack.com/brunner',
    'grad': 'linear-gradient(transparent, transparent)',
}
JERSEY_RULES = [
    'background: url(\'{fairylab}/{{lower}}/{{asset}}.png\')',
    'background: url(\'{gist}/{{repo}}/raw/{{tag}}/{{asset}}.svg\'), {grad}',
]
JERSEY_RULES = [r.format(**JERSEY_KWARGS) for r in JERSEY_RULES]
JERSEY_STYLE = ruleset(
    selector='.jersey-base',
    rules=[
        'background-size: 78px 80px',
        'border: 1px solid #eeeff0',
        'height: 82px',
        'margin: -5px -1px -5px -5px',
        'width: 80px',
    ])
NUMBER_KWARGS = {
    'fairylab': 'https://fairylab.surge.sh/images/numbers',
}
NUMBER_RULES = [
    '-webkit-mask-image: url(\'{fairylab}/{{font}}/{{fill}}/{{num}}.png\')',
]
NUMBER_RULES = [r.format(**NUMBER_KWARGS) for r in NUMBER_RULES]
NUMBER_STYLE = ruleset(
    selector='.number-base',
    rules=[
        'height: 20px',
        'width: 12px',
        '-webkit-mask-size: 12px 20px',
        'top: 23px',
    ])


def _color_name(color):
    if color == GREY:
        return 'away'
    elif color == WHITE:
        return 'home'
    return 'alt-' + color


def _encoding_to_alternates(encoding):
    return ENCODING_MAP.get(encoding, {}).get('alternates', '')


def _encoding_to_away(encoding):
    return ENCODING_MAP.get(encoding, {}).get('away', '')


def _encoding_to_home(encoding):
    return ENCODING_MAP.get(encoding, {}).get('home', '')


def _encoding_to_lower(encoding):
    return ENCODING_MAP.get(encoding, {}).get('lower', '')


def _encoding_to_repo(encoding):
    return ENCODING_MAP.get(encoding, {}).get('repo', '')


def _encoding_to_tag(encoding):
    return ENCODING_MAP.get(encoding, {}).get('tag', '')


def _font_offset(font):
    return [('mid', 29), ('l-1', 24), ('l-2', 22), ('r-1', 34), ('r-2', 36)]


def _nums(num):
    i = int(num) % 100
    nums = []
    if i < 10:
        nums.append((i, 'mid'))
    else:
        left, right = i // 10, i % 10
        if left == 1 and right == 1:
            nums.append((1, 'l-1'))
            nums.append((1, 'r-1'))
        elif left == 1:
            nums.append((1, 'l-2'))
            nums.append((right, 'r-1'))
        elif right == 1:
            nums.append((left, 'l-1'))
            nums.append((1, 'r-2'))
        else:
            nums.append((left, 'l-2'))
            nums.append((right, 'r-2'))

    return nums


def decoding_to_encoding(decoding):
    return DECODING_MAP.get(decoding, {}).get('encoding', '')


def decoding_to_encoding_sub(text):
    return _sub(DECODING_KEYS, decoding_to_encoding, text)


def encoding_keys():
    return ENCODING_KEYS


def encoding_to_abbreviation(encoding):
    return ENCODING_MAP.get(encoding, {}).get('abbreviation', '')


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


def jersey_absolute(encoding, colors, num, side):
    jersey = []

    color, solid, border, font = colors
    if color == GREY:
        name = 'away'
    elif color == WHITE:
        name = 'home'
    else:
        name = 'alt-' + color

    lower = _encoding_to_lower(encoding)
    base = 'jersey-base position-absolute ' + '-'.join([lower, name, side])
    jersey.append(DIV_TAG.format(base))

    if num is not None:
        for n, offset in _nums(num):
            nc = 'number-base position-absolute '
            nc += 'number-{}-{} '.format(font, offset)
            nc += 'number-{}-{{0}}-{} '.format(font, n)
            nc += '{}-{}-{{0}}'.format(lower, name)
            jersey.append(DIV_TAG.format(nc.format('solid')))
            jersey.append(DIV_TAG.format(nc.format('border')))

    return '\n'.join(jersey)


def jersey_colors(encoding, day, team, clash):
    alternates = _encoding_to_alternates(encoding)
    for color, solid, border, font, days, pct, teams in alternates:
        if color in CLASH_MAP.get(clash, {}):
            continue
        if day not in days:
            continue
        if pct < random.random():
            continue
        if not re.search(teams, team):
            continue

        return (color, solid, border, font)

    if team == 'home':
        return _encoding_to_home(encoding)
    return _encoding_to_away(encoding)


def jersey_style(*jerseys):
    fonts = set()
    styles = []

    for encoding, colors in jerseys:
        color, solid, border, font = colors
        fonts.add(font)

        lower = _encoding_to_lower(encoding)
        name = _color_name(color)
        repo = _encoding_to_repo(encoding)
        tag = _encoding_to_tag(encoding)

        for side in ['back', 'front']:
            asset = '-'.join([lower, name, side])
            kwargs = {'asset': asset, 'lower': lower, 'repo': repo, 'tag': tag}
            rules = [r.format(**kwargs) for r in JERSEY_RULES]
            styles.append(ruleset(selector=('.' + asset), rules=rules))

        asset = '-'.join([lower, name, 'solid'])
        rules = ['background-color: ' + solid]
        styles.append(ruleset(selector='.' + asset, rules=rules))

        if border is not None:
            asset = '-'.join([lower, name, 'border'])
            rules = ['background-color: ' + border]
            styles.append(ruleset(selector='.' + asset, rules=rules))

    styles.append(JERSEY_STYLE)

    for font in fonts:
        for i in range(10):
            for fill in ['solid', 'border']:
                selector = '.' + '-'.join(['number', font, fill, str(i)])
                kwargs = {'fill': fill, 'font': font, 'num': i}
                rules = [r.format(**kwargs) for r in NUMBER_RULES]
                styles.append(ruleset(selector=selector, rules=rules))

        for s, offset in _font_offset(font):
            selector = '.' + '-'.join(['number', font, s])
            styles.append(
                ruleset(
                    selector=selector, rules=['left: {}px'.format(offset)]))

    styles.append(NUMBER_STYLE)
    return styles


def precoding_to_encoding(precoding):
    return PRECODING_MAP.get(precoding, {}).get('encoding', '')


def precoding_to_encoding_sub(text):
    return _sub(PRECODING_KEYS, precoding_to_encoding, text)


DECODING_KEYS = list(sorted(DECODING_MAP.keys()))
ENCODING_KEYS = list(sorted(ENCODING_MAP.keys()))
PRECODING_KEYS = list(sorted(PRECODING_MAP.keys()))
