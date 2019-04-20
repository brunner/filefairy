#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Service (reloadable) methods for rendering team uniforms."""

import os
import random
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/services/uniform', '', _path))

from common.elements.elements import ruleset  # noqa
from common.teams.teams import encoding_keys  # noqa
from common.teams.teams import encoding_to_lower  # noqa

AWAY = 'away'
BOTH = 'away|home'
HOME = 'home'

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

CLASH_LIST = [
    (BLACK, BLUE, GREEN, PURPLE),
    (CREAM, WHITE),
    (GREY),
    (ORANGE, RED, YELLOW),
    (SKY),
]
CLASH_MAP = {k: (set(c) - set((k, ))) for c in CLASH_LIST for k in c}


def _color_name(color):
    if color == GREY:
        return 'away'
    elif color == WHITE:
        return 'home'
    return 'alt-' + color


def _uniform(home, away, *alternates):
    return {
        'alternates': alternates,
        'away': away,
        'colors': [home, away] + [colors for colors, _ in alternates],
        'home': home,
    }


MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = range(7)
WEEKDAYS = [MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY]
WEEKENDS = [SATURDAY, SUNDAY]
ALL = WEEKDAYS + WEEKENDS

REPOS = [
    None,  # T30
    '925f81153b44d0b35734ca0c43b9f89a',  # T31
    '70fe783889494c2c0de8cd9b2dbd05b2',  # T32
    '6df0d030fbb62f9cd169624afe5351e3',  # T33
    '4a6a4036834b558756dac7ac9c0309d0',  # T34
    '359d34636fabc914a83a8c746fc6eba9',  # T35
    'ed81fde94a24fdce340a19e52fda33bd',  # T36
    'af532f33900c377ea6a7d5c373a9785f',  # T37
    '40b0331a059d0ad8869df7e101863401',  # T38
    '79886209567ba70e64192b9810bde6a3',  # T39
    '89a0edfe4287648effd8021807ef9625',  # T41
    '793744dc81800fea7f219dd22b28afa1',  # T42
    '2d3444f09ba1f0c9a06b6e9bdd27eda7',  # T43
    'f87f4b6bf4821f16ef57eae0823e9fc7',  # T44
    '9780ce2762db67b17831a0c908aaf725',  # T45
    'd334f966fa470e01991d550266b94283',  # T46
    '5aa56738ca8fc3f8367d6f777614de38',  # T47
    '5b5568f5e186885d5e5175a25959f5d0',  # T48
    '5b8b9a01333351a92f6f91726dce239b',  # T49
    'aa9197d99dd2abcb7a50f13e5ae75ab0',  # T50
    '5641c5488e3de552ebd8f04c7d089fd9',  # T50
    '21cdbe29a981ae9e9eeeccbd93b7e76e',  # T51
    'b52b416175cd704f7dd007d890dd629e',  # T52
    'a2ae8f3ef490bad2f2f5510428d4bdc2',  # T53
    '146290fc1036d7628d016218e9a05a92',  # T54
    'd82f716325270e162d646bbaa7160c8b',  # T55
    '2f8467f7cef50d56217cd0bd4da65ca0',  # T56
    '72da90820a526e10bad1484efd2aaea3',  # T57
    '468cead9ea12e6bb3ba6f62236b8d1a7',  # T58
    '75833b35b51c8b6cd5c300e0d4117739',  # T59
    '7364eac50fccbb97ce1ea034da8e3c6a',  # T60
    None,  # TCH
    None,  # TLA
    None,  # TNY
]

TAGS = [
    None,  # T30
    'e46d3919da84e127c46ddb9a98083fdfe45c550e',  # T31
    'af5e8226f04e295506a61636aaf6d405c6d24a54',  # T32
    'f9576bb0aa8427c19832bb972962b86c3a6cb1f2',  # T33
    'b370f4842d7d271d9935f30d231abe0368409944',  # T34
    '1afa211b3cec808c7d58863fd61d436bbdbe05da',  # T35
    'cf6811a0707e24be1ef2038f91cc295525274cf6',  # T36
    '8eb50b108f9f65dfcc71b30ddb3b9ab032a972c1',  # T37
    '39c4825ca85027191a3003528ce36ab6c85bf537',  # T38
    'ed1def95cd767f6c4e0601b6dd440d58f365e894',  # T39
    '2a80951e810dccdb569fc2f249e3fb8c00675000',  # T41
    'b2fe8e13546351a7272f1b90d066b398620adcac',  # T42
    'b19253b93017682124fe778e0a8624c12bcc6332',  # T43
    '1f8528c7ec317d89f3e7ba6de2b3c3dd7340f64c',  # T44
    '1018f1ba85a160d74d5a924749a6cd28cae44a40',  # T45
    '4572edb247c3b7281f01cf01e0ee97f34a14e145',  # T46
    '854c03ddbbd38842ee7e62f825b0dcd97cb9d391',  # T47
    '278276af922a94ee6396cace99f17c3a308da730',  # T48
    '0cfd7978330ee9e4c4c4fa37439b9abb903be46a',  # T49
    'b209622a6f5849a60035cd3f583914bb557fb514',  # T50
    'f62eb1e611dcb85832aa9cfc2ea1165a99325beb',  # T50
    '44bdf456e169c959be199c0030228077a7104c1e',  # T51
    'a3771c5794f7677c45b99bc467af7fa87ab26d6d',  # T52
    'b9c65c44cca5eab7453ae85ac728e27ae7416b67',  # T53
    '6a6f13694db39de9d335e25661138a4f14ccf4ab',  # T54
    'f5c7a0e63b18cfaef3aff919f1c74d60719f5747',  # T55
    'b854738755e6572c1aec7ca65a16b1030a4c3b53',  # T56
    '9596cda701c2d5af036d726e2547db65dfcda134',  # T57
    '80fb2958b8e027e2d8a8097bcb7cd4b3bd9bfe13',  # T58
    'ac65ce092e906593e512d3452a38c2e5668f8447',  # T59
    '47d7dae296e3b5d262e9dca3effad546969670f1',  # T60
    None,  # TCH
    None,  # TLA
    None,  # TNY
]

UNIFORMS = [
    None,  # T30
    _uniform(  # T31
        (WHITE, '#cb0c29', '#000000', 'diamondbacks'),
        (GREY, '#000000', '#cb0c29', 'diamondbacks'),
        ((RED, '#000000', '#e79d94', 'diamondbacks'), ([SUNDAY], 1.0, BOTH)),
    ),
    _uniform(  # T32
        (WHITE, '#ab1234', '#0b2c5a', 'block'),
        (GREY, '#ab1234', '#0b2c5a', 'block'),
        ((CREAM, '#ab1234', '#0b2c5a', 'block'), ([SUNDAY], 1.0, HOME)),
        ((BLUE, '#0b2c5a', '#f5f5f5', 'block'), (ALL, .5, AWAY)),
    ),
    _uniform(  # T33
        (WHITE, '#f94900', '#000000', 'basic'),
        (GREY, '#f94900', '#000000', 'basic'),
        ((BLACK, '#f94900', 'none', 'basic'), ([FRIDAY], 1.0, BOTH)),
        ((ORANGE, '#000000', '#7f7f7f', 'basic'), ([SATURDAY], 1.0, BOTH)),
    ),
    _uniform(  # T34
        (WHITE, '#d5122f', '#09285a', 'redsox'),
        (GREY, '#d5122f', '#09285a', 'redsox'),
        ((RED, '#09285a', '#88a7d9', 'redsox'), ([FRIDAY], 1.0, HOME)),
        ((BLUE, '#d5122f', '#82a7d9', 'redsox'), ([FRIDAY], 1.0, AWAY)),
    ),
    _uniform(  # T35
        (WHITE, '#000000', 'none', 'basic'),
        (GREY, '#000000', '#f5f5f5', 'basic'),
        ((BLUE, '#09285a', 'none', 'block'), ([SUNDAY], 1.0, HOME)),
        ((BLACK, '#ffffff', 'none', 'basic'), (ALL, .6, BOTH)),
    ),
    _uniform(  # T36
        (WHITE, '#122441', 'none', 'serif'),
        (GREY, '#122441', 'none', 'serif'),
        ((BLUE, '#ffffff', 'none', 'serif'), ([SUNDAY], 1.0, BOTH)),
    ),
    _uniform(  # T37
        (WHITE, '#ea164c', '#000000', 'reds'),
        (GREY, '#ea164c', '#000000', 'reds'),
        ((RED, '#ffffff', '#000000', 'reds'), (ALL, .35, HOME)),
    ),
    _uniform(  # T38
        (WHITE, '#e9144b', '#09295c', 'basic'),
        (GREY, '#09295c', '#e9144b', 'basic'),
        ((BLUE, '#e9144b', '#82b0e2', 'basic'), (ALL, .6, BOTH)),
    ),
    _uniform(  # T39
        (WHITE, '#000000', 'none', 'basic'),
        (GREY, '#22176b', 'none', 'basic'),
        ((PURPLE, '#000000', '#f5f5f5', 'basic'), (ALL, .35, BOTH)),
        ((BLACK, '#a5a4a8', '#3b3583', 'basic'), (ALL, .15, BOTH)),
    ),
    _uniform(  # T40
        (WHITE, '#0b2245', '#e54927', 'block'),
        (GREY, '#0b2245', '#e54927', 'block'),
        ((BLUE, '#ffffff', '#e54927', 'block'), (ALL, .6, HOME)),
        ((ORANGE, '#0b2245', '#98aece', 'block'), (ALL, .5, AWAY)),
    ),
    _uniform(  # T41
        (WHITE, '#000000', '#27aab8', 'basic'),
        (GREY, '#000000', '#27aab8', 'basic'),
    ),
    _uniform(  # T42
        (WHITE, '#141929', '#aa563e', 'block'),
        (GREY, '#141929', '#aa563e', 'block'),
        ((ORANGE, '#141929', '#f5f5f5', 'block'), (ALL, .2, BOTH)),
    ),
    _uniform(  # T43
        (WHITE, '#0d326f', 'none', 'basic'),
        (GREY, '#0d326f', 'none', 'basic'),
        ((SKY, '#ffffff', '#0d326f', 'basic'), ([MONDAY, FRIDAY], 1.0, HOME)),
        ((BLUE, '#ffffff', 'none', 'basic'), ([SUNDAY], 1.0, AWAY)),
    ),
    _uniform(  # T44
        (WHITE, '#b11132', '#0c2445', 'pointed'),
        (GREY, '#b11132', '#0c2445', 'pointed'),
        ((RED, '#b11132', '#0c2445', 'pointed'), (ALL, .55, BOTH)),
    ),
    _uniform(  # T45
        (WHITE, '#233972', 'none', 'basic'),
        (GREY, '#233972', 'none', 'basic'),
    ),
    _uniform(  # T46
        (WHITE, '#1a4ba7', '#fbc72d', 'block'),
        (GREY, '#1a4ba7', '#fbc72d', 'block'),
        ((SKY, '#1a4ba7', '#fbc72d', 'block'), (WEEKENDS, 1.0, BOTH)),
    ),
    _uniform(  # T47
        (WHITE, '#d11242', '#052046', 'basic'),
        (GREY, '#052046', '#d11242', 'basic'),
        ((CREAM, '#052046', '#d11242', 'basic'), (WEEKDAYS, 1.0, HOME)),
        ((BLUE, '#d11242', '#ff94c4', 'basic'), (ALL, .15, AWAY)),
    ),
    _uniform(  # T48
        (WHITE, '#051e42', 'none', 'block'),
        (GREY, '#051e42', '#f5f5f5', 'block'),
    ),
    _uniform(  # T49
        (WHITE, '#144a8b', '#d57437', 'basic'),
        (GREY, '#253b76', '#c45d3b', 'basic'),
        ((BLACK, '#144a8b', '#d57437', 'basic'), (ALL, .25, HOME)),
        ((BLUE, '#a4a1a1', '#c45d3b', 'basic'), (ALL, .25, AWAY)),
    ),
    _uniform(  # T50
        (WHITE, '#064436', '#f0b019', 'basic'),
        (GREY, '#064436', '#f0b019', 'basic'),
        ((YELLOW, '#064436', 'none', 'basic'), ([FRIDAY], 1.0, HOME)),
        ((GREEN, '#ffffff', '#f0b019', 'basic'), (ALL, .15, AWAY)),
    ),
    _uniform(  # T51
        (WHITE, '#d11043', 'none', 'rounded'),
        (GREY, '#d11043', '#f5f5f5', 'rounded'),
        ((SKY, '#6d223a', '#d991a8', 'rounded'), ([THURSDAY], 1.0, HOME)),
        ((CREAM, '#d11043', '#165397', 'rounded'), ([SUNDAY], 1.0, HOME)),
    ),
    _uniform(  # T52
        (WHITE, '#000000', '#fcc72d', 'pirates'),
        (GREY, '#000000', '#fcc72d', 'pirates'),
        ((YELLOW, '#000000', '#f5f5f5', 'basic'), ([SUNDAY], 1.0, HOME)),
        ((BLACK, '#fcc72d', '#ffffd0', 'pirates'), (ALL, .4, BOTH)),
    ),
    _uniform(  # T53
        (WHITE, '#512c1b', '#f0aa1c', 'serif'),
        (GREY, '#512c1b', '#f0aa1c', 'serif'),
        ((CREAM, '#512c1b', '#f0aa1c', 'serif'), ([SUNDAY], 1.0, HOME)),
        ((YELLOW, '#512c1b', 'none', 'serif'), (ALL, .35, AWAY)),
    ),
    _uniform(  # T54
        (WHITE, '#09285a', '#0b505a', 'basic'),
        (GREY, '#09285a', '#0b505a', 'basic'),
        ((GREEN, '#c9d0d1', '#09285a', 'basic'), ([FRIDAY], 1.0, HOME)),
        ((BLUE, '#c9d0d1', '#0b505a', 'mariners'), (ALL, .45, AWAY)),
    ),
    _uniform(  # T55
        (WHITE, '#000000', '#c85633', 'basic'),
        (GREY, '#000000', '#c85633', 'basic'),
        ((ORANGE, '#000000', '#f5f5f5', 'basic'), ([FRIDAY], 1.0, HOME)),
    ),
    _uniform(  # T56
        (WHITE, '#d11043', '#0c2340', 'basic'),
        (GREY, '#d11043', '#0c2340', 'basic'),
        ((CREAM, '#d11043', '#0c2340', 'basic'), ([SATURDAY], 1.0, HOME)),
    ),
    _uniform(  # T57
        (WHITE, '#08131e', '#284d6e', 'basic'),
        (GREY, '#08131e', '#284d6e', 'basic'),
        ((SKY, '#fcc520', '#08131e', 'rounded'), ([SUNDAY], 1.0, HOME)),
        ((BLUE, '#74b5e1', 'none', 'rounded'), (ALL, .5, AWAY)),
    ),
    _uniform(  # T58
        (WHITE, '#124886', '#ce103b', 'pointed'),
        (GREY, '#124886', '#ce103b', 'pointed'),
        ((SKY, '#e60021', '#99dcff', 'block'), ([SUNDAY], 1.0, HOME)),
        ((BLUE, '#ffffff', '#ce103b', 'pointed'), (ALL, .5, BOTH)),
    ),
    _uniform(  # T59
        (WHITE, '#1d469b', 'none', 'bluejays'),
        (GREY, '#1d469b', 'none', 'bluejays'),
        ((BLUE, '#ffffff', 'none', 'bluejays'), (ALL, .5, BOTH)),
    ),
    _uniform(  # T60
        (WHITE, '#b10b30', '#0a2045', 'block'),
        (GREY, '#b10b30', '#0a2045', 'block'),
        ((BLUE, '#b10b30', '#7f9fc2', 'block'), ([FRIDAY], 1.0, BOTH)),
        ((RED, '#ffffff', '#0a2045', 'block'), ([SUNDAY], 1.0, BOTH)),
    ),
    None,  # TCH
    None,  # TLA
    None,  # TNY
]

KEYS = encoding_keys()
REPO_MAP = dict(zip(KEYS, REPOS))
TAG_MAP = dict(zip(KEYS, TAGS))
UNIFORM_MAP = dict(zip(KEYS, UNIFORMS))


def _encoding_to_alternates(encoding):
    return UNIFORM_MAP.get(encoding, {}).get('alternates', [])


def _encoding_to_away(encoding):
    return UNIFORM_MAP.get(encoding, {}).get('away', None)


def _encoding_to_home(encoding):
    return UNIFORM_MAP.get(encoding, {}).get('home', None)


def _encoding_to_repo(encoding):
    return REPO_MAP.get(encoding, None)


def _encoding_to_tag(encoding):
    return TAG_MAP.get(encoding, None)


DIV_TAG = '<div class="{}"></div>'

JERSEY_KWARGS = {
    'fairylab': 'https://fairylab.surge.sh/images/teams',
    'gist': 'https://gistcdn.githack.com/brunner',
    'grad': 'linear-gradient(transparent, transparent)',
}
JERSEY_RULES = [
    'background-image: url(\'{fairylab}/{{lower}}/{{asset}}.png\')',
    'background-image: url(\'{gist}/{{repo}}/raw/{{tag}}/{{asset}}.svg\'), {grad}',
]
JERSEY_RULES = [r.format(**JERSEY_KWARGS) for r in JERSEY_RULES]

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
        'height: 18px',
        'width: 14px',
        '-webkit-mask-size: 14px 18px',
        'top: 18px',
    ])


def _font_offset(font):
    if font == 'bluejays':
        return [('mid', 20), ('l1', 15), ('l2', 14), ('r1', 26), ('r2', 27)]
    if font == 'diamondbacks':
        return [('mid', 20), ('l1', 17), ('l2', 15), ('r1', 24), ('r2', 26)]
    if font == 'redsox':
        return [('mid', 20), ('l1', 16), ('l2', 14), ('r1', 25), ('r2', 27)]
    if font == 'rounded':
        return [('mid', 20), ('l1', 16), ('l2', 15), ('r1', 25), ('r2', 26)]

    return [('mid', 20), ('l1', 16), ('l2', 14), ('r1', 25), ('r2', 27)]


def _nums(num):
    i = int(num) % 100
    nums = []
    if i < 10:
        nums.append((i, 'mid'))
    else:
        left, right = i // 10, i % 10
        if left == 1 and right == 1:
            nums.append((1, 'l1'))
            nums.append((1, 'r1'))
        elif left == 1:
            nums.append((1, 'l2'))
            nums.append((right, 'r1'))
        elif right == 1:
            nums.append((left, 'l1'))
            nums.append((1, 'r2'))
        else:
            nums.append((left, 'l2'))
            nums.append((right, 'r2'))

    return nums


def encoding_to_colors(encoding):
    return UNIFORM_MAP.get(encoding, {}).get('colors', None)


def jersey_absolute(encoding, colors, num, side, classes):
    jersey = []

    color, solid, border, font = colors
    if color == GREY:
        name = 'away'
    elif color == WHITE:
        name = 'home'
    else:
        name = 'alt-' + color

    lower = encoding_to_lower(encoding)
    base = 'jersey-base position-absolute ' + '-'.join([lower, name, side])
    if classes:
        base += ' ' + ' '.join(classes)
    jersey.append(DIV_TAG.format(base))

    if side == 'back' and num is not None:
        for n, offset in _nums(num):
            nc = 'number-base position-absolute '
            nc += 'number-{}-{} '.format(font, offset)
            nc += 'number-{}-{{0}}-{} '.format(font, n)
            nc += '{}-{}-{{0}}'.format(lower, name)

            jersey.append(DIV_TAG.format(nc.format('solid')))
            if border is not 'none':
                jersey.append(DIV_TAG.format(nc.format('border')))

    return '\n'.join(jersey)


def jersey_colors(encoding, day, team, clash):
    alternates = _encoding_to_alternates(encoding)
    for colors, constraints in alternates:
        if colors[0] in CLASH_MAP.get(clash, {}):
            continue

        days, pct, teams = constraints
        if day not in days:
            continue
        if pct < random.random():
            continue
        if not re.search(teams, team):
            continue

        return colors

    if team == 'home':
        return _encoding_to_home(encoding)
    return _encoding_to_away(encoding)


def jersey_style(*jerseys):
    fonts = set()
    styles = []

    for encoding, colors in jerseys:
        color, solid, border, font = colors
        fonts.add(font)

        lower = encoding_to_lower(encoding)
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

        if border is not 'none':
            asset = '-'.join([lower, name, 'border'])
            rules = ['background-color: ' + border]
            styles.append(ruleset(selector='.' + asset, rules=rules))

    for font in sorted(fonts):
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
