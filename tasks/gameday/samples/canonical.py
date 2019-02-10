#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sample data for gameday.py golden test."""

import json
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/tasks/gameday/samples', '', _path))

from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.datetime_.datetime_ import encode_datetime  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import dialog  # noqa
from common.elements.elements import span  # noqa
from common.elements.elements import table  # noqa
from common.elements.elements import topper  # noqa
from common.teams.teams import icon_absolute  # noqa
from common.test.test import get_testdata  # noqa
from services.scoreboard.scoreboard import line_score_hide_body  # noqa
from services.scoreboard.scoreboard import line_score_hide_foot  # noqa
from services.scoreboard.scoreboard import line_score_show_body  # noqa
from services.scoreboard.scoreboard import line_score_show_foot  # noqa
from services.scoreboard.scoreboard import pending_hide_body  # noqa
from services.scoreboard.scoreboard import pending_show_body  # noqa

DATE_08280000 = datetime_datetime_pst(2024, 8, 28)

TESTDATA = get_testdata()

_game_2449 = json.loads(TESTDATA['2449.json'])
_head_2449 = topper('Wednesday, August 28th, 2024')
_hide_body_2449 = line_score_hide_body(_game_2449)
_hide_foot_2449 = line_score_hide_foot(_game_2449)
_show_body_2449 = line_score_show_body(_game_2449, hidden=True)
_show_foot_2449 = line_score_show_foot(_game_2449, hidden=True)

_game_2469 = json.loads(TESTDATA['2469.json'])
_head_2469 = topper('Thursday, August 29th, 2024')
_hide_body_2469 = line_score_hide_body(_game_2469)
_hide_foot_2469 = line_score_hide_foot(_game_2469)
_show_body_2469 = line_score_show_body(_game_2469, hidden=True)
_show_foot_2469 = line_score_show_foot(_game_2469, hidden=True)

_game_2476 = json.loads(TESTDATA['2476.json'])
_head_2476 = topper('Friday, August 30th, 2024')
_hide_body_2476 = line_score_hide_body(_game_2476)
_hide_foot_2476 = line_score_hide_foot(_game_2476)
_show_body_2476 = line_score_show_body(_game_2476, hidden=True)
_show_foot_2476 = line_score_show_foot(_game_2476, hidden=True)

_pending_hide_body = pending_hide_body(
    encode_datetime(DATE_08280000),
    ['T31 4, TLA 2', 'TNY 5, TLA 3', 'TNY 1, T55 0'])
_pending_show_body = pending_show_body(
    encode_datetime(DATE_08280000),
    ['T31 4, TLA 2', 'TNY 5, TLA 3', 'TNY 1, T55 0'],
    hidden=True)

_days = [
    [
        _head_2449, _hide_body_2449, _hide_foot_2449, _show_body_2449,
        _show_foot_2449, _pending_hide_body, _pending_show_body
    ],
    [
        _head_2469, _hide_body_2469, _hide_foot_2469, _show_body_2469,
        _show_foot_2469
    ],
    [
        _head_2476, _hide_body_2476, _hide_foot_2476, _show_body_2476,
        _show_foot_2476
    ],
]

_icon_0828 = icon_absolute('T30', 'Pending Games')
_icon_2449 = icon_absolute('T30', 'Tigers at Twins, 7:10 PM')

_bc = ['badge', 'badge-icon', 'badge-light']
_tc = ['align-middle', 'badge-icon-button']


def _tables(d, g):
    date = {'data-dismiss': 'modal', 'data-show-date': d}
    game = {'data-dismiss': 'modal', 'data-show-game': g}

    t = 'Pending Games Only' if g == '0' else 'Current Game Only'
    return [
        table(
            clazz='border mb-3',
            hcols=[col(clazz='font-weight-bold text-dark', colspan="2")],
            bcols=[
                col(clazz='w-50 badge-icon-wrapper pl-2'),
                col(clazz='w-50 badge-icon-wrapper pr-2')
            ],
            head=[[cell(content='Spoiler Options')]],
            body=[[
                cell(
                    content=span(
                        classes=_bc,
                        text=span(classes=_tc, text='All Games for Today'),
                        attributes=date)),
                cell(
                    content=span(
                        classes=_bc,
                        text=span(classes=_tc, text=t),
                        attributes=game)),
            ]])
    ]


_tables_2449 = _tables('0828', '2449')
_tables_0828 = _tables('0828', '0')
_tables_2469 = _tables('0829', '2469')
_tables_2476 = _tables('0830', '2476')

_dialogs = [
    dialog(id_='d0828g2449', icon=_icon_2449, tables=_tables_2449),
    dialog(id_='d0828g0', icon=_icon_0828, tables=_tables_0828),
    dialog(id_='d0829g2469', icon=_icon_2449, tables=_tables_2469),
    dialog(id_='d0830g2476', icon=_icon_2449, tables=_tables_2476),
]

subtitle = ''

tmpl = 'gameday.html'

context = {
    'days': _days,
    'dialogs': _dialogs,
}
