#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Service (reloadable) methods for displaying live sim data."""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/services/livesim', '', _path))

from common.datetime_.datetime_ import suffix  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import table  # noqa
from common.elements.elements import topper  # noqa
from common.json_.json_ import loads  # noqa
from common.reference.reference import player_to_bats  # noqa
from common.reference.reference import player_to_name  # noqa
from common.reference.reference import player_to_number  # noqa
from common.reference.reference import player_to_throws  # noqa
from common.service.service import call_service  # noqa
from common.teams.teams import encoding_to_nickname  # noqa
from data.event.event import Event  # noqa

SMALLCAPS = {k: v for k, v in zip('BCDFHLPRS', 'ʙᴄᴅꜰʜʟᴘʀs')}


def _inning(half):
    s = 'Top' if half % 2 == 0 else 'Bottom'
    n = (half // 2) + 1
    return '{} {}{}'.format(s, n, suffix(n))


def _profile(team, num, colors, s):
    args = (team, colors, num, 'back')
    img = call_service('uniforms', 'jersey_absolute', args)
    spn = '<span class="profile-text align-middle d-block">{}</span>'.format(s)
    return '<div class="position-relative h-58p">{}</div>'.format(img + spn)


def _player(bats, team, player, fielding, colors):
    title = 'ᴀᴛ ʙᴀᴛ' if bats else 'ᴘɪᴛᴄʜɪɴɢ'
    hand = player_to_bats(player) if bats else player_to_throws(player)
    name = player_to_name(player)
    num = player_to_number(player)
    pos = ''.join(SMALLCAPS.get(c, c) for c in fielding)
    stats = ''

    s = '{}: {} #{} ({})<br>{}<br>{}'.format(
        title,
        pos,
        num,
        SMALLCAPS.get(hand, 'ʀ'),
        name,
        stats,
    )
    return cell(content=_profile(team, num, colors, s))


def get_html(game_in):
    """Gets template data for a given game data object.

    Args:
        game_in: The game data file path.

    Returns:
        The template data.
    """
    data = loads(game_in)
    if not data['events']:
        return None

    colors = {
        data['away_team']: data['away_colors'].split(),
        data['home_team']: data['home_colors'].split(),
    }

    jerseys = [(encoding, colors[encoding]) for encoding in colors]
    styles = call_service('uniforms', 'jersey_style', (*jerseys, ))

    batting, throwing = data['home_team'], data['away_team']
    half = 0
    inning = True

    tables = []
    body = []

    for encoding in data['events']:
        event, args = Event.decode(encoding)
        if event == Event.CHANGE_INNING:
            inning = True
        elif inning:
            if body:
                tables.append(table(clazz='border mb-3', body=body))
                body = []
            tables.append(topper(_inning(half)))
            batting, throwing = throwing, batting
            half, inning = half + 1, False

        if event == Event.CHANGE_BATTER:
            cell = _player(True, batting, args[0], '', colors[batting])
            body.append([cell])

    if body:
        tables.append(table(clazz='border mb-3', body=body))

    return {'styles': styles, 'tables': tables}
