#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sample data for standings.py golden test."""

import json
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/tasks/standings/samples', '', _path))

from common.elements.elements import anchor  # noqa
from common.elements.elements import card  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import dialog  # noqa
from common.elements.elements import table  # noqa
from common.teams.teams import icon_absolute  # noqa
from common.teams.teams import icon_badge  # noqa
from common.test.test import get_testdata  # noqa
from services.scoreboard.scoreboard import line_score_body  # noqa
from services.scoreboard.scoreboard import line_score_foot  # noqa
from services.scoreboard.scoreboard import line_score_head  # noqa
from services.scoreboard.scoreboard import pending_score_body  # noqa

EXPANDED_COLS = [
    col(clazz='position-relative text-truncate'),
    col(clazz='text-right w-55p'),
    col(clazz='text-right w-55p'),
    col(clazz='text-right w-75p')
]

TESTDATA = get_testdata()


def _expanded_head(subleague):
    return [
        cell(content=subleague),
        cell(content='W'),
        cell(content='L'),
        cell(content='GB'),
    ]


_breadcrumbs = [{
    'href': '/',
    'name': 'Fairylab'
}, {
    'href': '',
    'name': 'Standings'
}]

_bcols = [
    col(clazz='td-sm position-relative text-center w-20 pl-2'),
    col(clazz='td-sm position-relative text-center w-20'),
    col(clazz='td-sm position-relative text-center w-20'),
    col(clazz='td-sm position-relative text-center w-20'),
    col(clazz='td-sm position-relative text-center w-20 pr-2')
]
_recent = [
    table(
        clazz='table-fixed border mt-3',
        hcols=[col(clazz='text-center', colspan=5)],
        bcols=_bcols,
        head=[[cell(content='American League')]],
        body=[
            [
                cell(content=icon_badge('T48', '1-0', True, '16')),
                cell(content=icon_badge('T33', '0-0', False, '16')),
                cell(content=icon_badge('T34', '0-0', False, '16')),
                cell(content=icon_badge('T57', '0-0', False, '16')),
                cell(content=icon_badge('T59', '0-0', False, '16')),
            ],
            [
                cell(content=icon_badge('T47', '3-0', True, '16')),
                cell(content=icon_badge('T35', '0-0', False, '16')),
                cell(content=icon_badge('T38', '0-0', False, '16')),
                cell(content=icon_badge('T43', '0-0', False, '16')),
                cell(content=icon_badge('T40', '0-3', True, '16')),
            ],
            [
                cell(content=icon_badge('T44', '0-1', True, '16')),
                cell(content=icon_badge('T42', '0-0', False, '16')),
                cell(content=icon_badge('T50', '0-0', False, '16')),
                cell(content=icon_badge('T54', '0-0', False, '16')),
                cell(content=icon_badge('T59', '0-0', False, '16')),
            ],
        ],
    ),
    table(
        clazz='table-fixed border mt-3',
        hcols=[col(clazz='text-center', colspan=5)],
        bcols=_bcols,
        head=[[cell(content='National League')]],
        body=[
            [
                cell(content=icon_badge('T32', '0-0', False, '16')),
                cell(content=icon_badge('T41', '0-0', False, '16')),
                cell(content=icon_badge('T49', '0-0', False, '16')),
                cell(content=icon_badge('T51', '0-0', False, '16')),
                cell(content=icon_badge('T60', '0-0', False, '16')),
            ],
            [
                cell(content=icon_badge('T36', '0-0', False, '16')),
                cell(content=icon_badge('T37', '0-0', False, '16')),
                cell(content=icon_badge('T46', '0-0', False, '16')),
                cell(content=icon_badge('T52', '0-0', False, '16')),
                cell(content=icon_badge('T56', '0-0', False, '16')),
            ],
            [
                cell(content=icon_badge('T31', '1-0', True, '16')),
                cell(content=icon_badge('T39', '0-0', False, '16')),
                cell(content=icon_badge('T53', '0-0', False, '16')),
                cell(content=icon_badge('T45', '0-1', True, '16')),
                cell(content=icon_badge('T55', '0-1', True, '16')),
            ],
        ],
    ),
]

_expanded = [
    table(
        hcols=EXPANDED_COLS,
        bcols=EXPANDED_COLS,
        head=[_expanded_head('AL East')],
        body=[
            [
                cell(content=icon_absolute('T48', 'New York', '20')),
                cell(content='1'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=icon_absolute('T33', 'Baltimore', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='0.5'),
            ],
            [
                cell(content=icon_absolute('T34', 'Boston', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='0.5'),
            ],
            [
                cell(content=icon_absolute('T57', 'Tampa Bay', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='0.5'),
            ],
            [
                cell(content=icon_absolute('T59', 'Toronto', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='0.5'),
            ],
        ],
    ),
    table(
        hcols=EXPANDED_COLS,
        bcols=EXPANDED_COLS,
        head=[_expanded_head('AL Central')],
        body=[
            [
                cell(content=icon_absolute('T47', 'Minnesota', '20')),
                cell(content='3'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=icon_absolute('T35', 'Chicago', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='1.5'),
            ],
            [
                cell(content=icon_absolute('T38', 'Cleveland', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='1.5'),
            ],
            [
                cell(content=icon_absolute('T43', 'Kansas City', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='1.5'),
            ],
            [
                cell(content=icon_absolute('T40', 'Detroit', '20')),
                cell(content='0'),
                cell(content='3'),
                cell(content='3.0'),
            ],
        ],
    ),
    table(
        hcols=EXPANDED_COLS,
        bcols=EXPANDED_COLS,
        head=[_expanded_head('AL West')],
        body=[
            [
                cell(content=icon_absolute('T42', 'Houston', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=icon_absolute('T50', 'Oakland', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=icon_absolute('T54', 'Seattle', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=icon_absolute('T58', 'Texas', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=icon_absolute('T44', 'Los Angeles', '20')),
                cell(content='0'),
                cell(content='1'),
                cell(content='0.5'),
            ],
        ],
    ),
    table(
        hcols=EXPANDED_COLS,
        bcols=EXPANDED_COLS,
        head=[_expanded_head('AL Wild Card')],
        body=[
            [
                cell(content=icon_absolute('T33', 'Baltimore', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=icon_absolute('T34', 'Boston', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=icon_absolute('T35', 'Chicago', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=icon_absolute('T38', 'Cleveland', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=icon_absolute('T42', 'Houston', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
        ],
    ),
    table(
        hcols=EXPANDED_COLS,
        bcols=EXPANDED_COLS,
        head=[_expanded_head('NL East')],
        body=[
            [
                cell(content=icon_absolute('T32', 'Atlanta', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=icon_absolute('T41', 'Miami', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=icon_absolute('T49', 'New York', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=icon_absolute('T51', 'Philadelphia', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=icon_absolute('T60', 'Washington', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
        ],
    ),
    table(
        hcols=EXPANDED_COLS,
        bcols=EXPANDED_COLS,
        head=[_expanded_head('NL Central')],
        body=[
            [
                cell(content=icon_absolute('T36', 'Chicago', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=icon_absolute('T37', 'Cincinnati', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=icon_absolute('T46', 'Milwaukee', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=icon_absolute('T52', 'Pittsburgh', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=icon_absolute('T56', 'St. Louis', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
        ],
    ),
    table(
        hcols=EXPANDED_COLS,
        bcols=EXPANDED_COLS,
        head=[_expanded_head('NL West')],
        body=[
            [
                cell(content=icon_absolute('T31', 'Arizona', '20')),
                cell(content='1'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=icon_absolute('T39', 'Colorado', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='0.5'),
            ],
            [
                cell(content=icon_absolute('T53', 'San Diego', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='0.5'),
            ],
            [
                cell(content=icon_absolute('T45', 'Los Angeles', '20')),
                cell(content='0'),
                cell(content='1'),
                cell(content='1.0'),
            ],
            [
                cell(content=icon_absolute('T55', 'San Francisco', '20')),
                cell(content='0'),
                cell(content='1'),
                cell(content='1.0'),
            ],
        ],
    ),
    table(
        hcols=EXPANDED_COLS,
        bcols=EXPANDED_COLS,
        head=[_expanded_head('NL Wild Card')],
        body=[
            [
                cell(content=icon_absolute('T32', 'Atlanta', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=icon_absolute('T36', 'Chicago', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=icon_absolute('T37', 'Cincinnati', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=icon_absolute('T39', 'Colorado', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=icon_absolute('T41', 'Miami', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
        ],
    ),
]

_game_2449 = json.loads(TESTDATA['2449.json'])
_head_2449 = line_score_head(_game_2449['date'])
_body_2449 = line_score_body(_game_2449)
_foot_2449 = line_score_foot(_game_2449)

_game_2469 = json.loads(TESTDATA['2469.json'])
_head_2469 = line_score_head(_game_2469['date'])
_body_2469 = line_score_body(_game_2469)
_foot_2469 = line_score_foot(_game_2469)

_game_2476 = json.loads(TESTDATA['2476.json'])
_head_2476 = line_score_head(_game_2476['date'])
_body_2476 = line_score_body(_game_2476)
_foot_2476 = line_score_foot(_game_2476)

_tables = [
    _head_2449, _body_2449, _foot_2449, _head_2469, _body_2469, _foot_2469,
    _head_2476, _body_2476, _foot_2476,
]  # yapf: disable

_body_31 = pending_score_body(['T31 4, TLA 2'])
_body_55 = pending_score_body(['TNY 1, T55 0'])
_body_la = pending_score_body(['T31 4, TLA 2', 'TNY 5, TLA 3'])
_body_ny = pending_score_body(['TNY 5, TLA 3', 'TNY 1, T55 0'])

_dialogs = [
    dialog('31', 'Arizona Diamondbacks', [_head_2449, _body_31]),
    dialog('40', 'Detroit Tigers', _tables),
    dialog('44', 'Los Angeles Angels', [_head_2449, _body_la]),
    dialog('45', 'Los Angeles Dodgers', [_head_2449, _body_la]),
    dialog('47', 'Minnesota Twins', _tables),
    dialog('48', 'New York Yankees', [_head_2449, _body_ny]),
    dialog('49', 'New York Mets', [_head_2449, _body_ny]),
    dialog('55', 'San Francisco Giants', [_head_2449, _body_55]),
]

subtitle = ''

tmpl = 'standings.html'

context = {
    'title': 'standings',
    'breadcrumbs': _breadcrumbs,
    'recent': _recent,
    'expanded': _expanded,
    'dialogs': _dialogs,
}
