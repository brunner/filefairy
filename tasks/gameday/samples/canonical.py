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
_tc = ['align-middle', 'badge-icon-text']

_s = span(classes=_tc, text='Show')

_attr_2449 = {'data-dismiss': 'modal', 'data-show': '2449'}
_table_2449 = table(
    clazz='mb-3',
    bcols=[col(clazz='border-0 p-0 w-150p')],
    body=[[cell(content=span(classes=_bc, text=_s, attributes=_attr_2449))]])

_attr_0828 = {'data-dismiss': 'modal', 'data-show': '0828'}
_table_0828 = table(
    clazz='mb-3',
    bcols=[col(clazz='border-0 p-0 w-150p')],
    body=[[cell(content=span(classes=_bc, text=_s, attributes=_attr_0828))]])

_attr_2469 = {'data-dismiss': 'modal', 'data-show': '2469'}
_table_2469 = table(
    clazz='mb-3',
    bcols=[col(clazz='border-0 p-0 w-150p')],
    body=[[cell(content=span(classes=_bc, text=_s, attributes=_attr_2469))]])

_attr_2476 = {'data-dismiss': 'modal', 'data-show': '2476'}
_table_2476 = table(
    clazz='mb-3',
    bcols=[col(clazz='border-0 p-0 w-150p')],
    body=[[cell(content=span(classes=_bc, text=_s, attributes=_attr_2476))]])

_dialogs = [
    dialog(id_='game2449', icon=_icon_2449, tables=[_table_2449]),
    dialog(id_='date0828', icon=_icon_0828, tables=[_table_0828]),
    dialog(id_='game2469', icon=_icon_2449, tables=[_table_2469]),
    dialog(id_='game2476', icon=_icon_2449, tables=[_table_2476]),
]

subtitle = ''

tmpl = 'gameday.html'

context = {
    'days': _days,
    'dialogs': _dialogs,
}
