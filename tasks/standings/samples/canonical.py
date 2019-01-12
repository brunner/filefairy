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
from common.json_.json_ import filts  # noqa
from common.test.test import get_testdata  # noqa
from services.scoreboard.scoreboard import line_score  # noqa
from tasks.standings.standings import GAME_KEYS  # noqa

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
        head=[cell(content='American League')],
        body=[
            [
                cell(content=icon_badge('T33', '0-0', '16')),
                cell(content=icon_badge('T34', '0-0', '16')),
                cell(content=icon_badge('T48', '0-0', '16')),
                cell(content=icon_badge('T57', '0-0', '16')),
                cell(content=icon_badge('T59', '0-0', '16')),
            ],
            [
                cell(content=icon_badge('T47', '3-0', '16')),
                cell(content=icon_badge('T35', '0-0', '16')),
                cell(content=icon_badge('T38', '0-0', '16')),
                cell(content=icon_badge('T43', '0-0', '16')),
                cell(content=icon_badge('T40', '0-3', '16')),
            ],
            [
                cell(content=icon_badge('T42', '0-0', '16')),
                cell(content=icon_badge('T44', '0-0', '16')),
                cell(content=icon_badge('T50', '0-0', '16')),
                cell(content=icon_badge('T54', '0-0', '16')),
                cell(content=icon_badge('T59', '0-0', '16')),
            ],
        ],
    ),
    table(
        clazz='table-fixed border mt-3',
        hcols=[col(clazz='text-center', colspan=5)],
        bcols=_bcols,
        head=[cell(content='National League')],
        body=[
            [
                cell(content=icon_badge('T32', '0-0', '16')),
                cell(content=icon_badge('T41', '0-0', '16')),
                cell(content=icon_badge('T49', '0-0', '16')),
                cell(content=icon_badge('T51', '0-0', '16')),
                cell(content=icon_badge('T60', '0-0', '16')),
            ],
            [
                cell(content=icon_badge('T36', '0-0', '16')),
                cell(content=icon_badge('T37', '0-0', '16')),
                cell(content=icon_badge('T46', '0-0', '16')),
                cell(content=icon_badge('T52', '0-0', '16')),
                cell(content=icon_badge('T56', '0-0', '16')),
            ],
            [
                cell(content=icon_badge('T31', '0-0', '16')),
                cell(content=icon_badge('T39', '0-0', '16')),
                cell(content=icon_badge('T45', '0-0', '16')),
                cell(content=icon_badge('T53', '0-0', '16')),
                cell(content=icon_badge('T55', '0-0', '16')),
            ],
        ],
    ),
]

_expanded = [
    table(
        hcols=EXPANDED_COLS,
        bcols=EXPANDED_COLS,
        head=_expanded_head('AL East'),
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
                cell(content=icon_absolute('T48', 'New York', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=icon_absolute('T57', 'Tampa Bay', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=icon_absolute('T59', 'Toronto', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
        ],
    ),
    table(
        hcols=EXPANDED_COLS,
        bcols=EXPANDED_COLS,
        head=_expanded_head('AL Central'),
        body=[
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
                cell(content=icon_absolute('T40', 'Detroit', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=icon_absolute('T43', 'Kansas City', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=icon_absolute('T47', 'Minnesota', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
        ],
    ),
    table(
        hcols=EXPANDED_COLS,
        bcols=EXPANDED_COLS,
        head=_expanded_head('AL West'),
        body=[
            [
                cell(content=icon_absolute('T42', 'Houston', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=icon_absolute('T44', 'Los Angeles', '20')),
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
        ],
    ),
    table(
        hcols=EXPANDED_COLS,
        bcols=EXPANDED_COLS,
        head=_expanded_head('AL Wild Card'),
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
                cell(content=icon_absolute('T40', 'Detroit', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
        ],
    ),
    table(
        hcols=EXPANDED_COLS,
        bcols=EXPANDED_COLS,
        head=_expanded_head('NL East'),
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
        head=_expanded_head('NL Central'),
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
        head=_expanded_head('NL West'),
        body=[
            [
                cell(content=icon_absolute('T31', 'Arizona', '20')),
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
                cell(content=icon_absolute('T45', 'Los Angeles', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=icon_absolute('T53', 'San Diego', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=icon_absolute('T55', 'San Francisco', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
        ],
    ),
    table(
        hcols=EXPANDED_COLS,
        bcols=EXPANDED_COLS,
        head=_expanded_head('NL Wild Card'),
        body=[
            [
                cell(content=icon_absolute('T31', 'Arizona', '20')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
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
        ],
    ),
]

_game_2449 = filts(json.loads(TESTDATA['2449.json']), GAME_KEYS)
_line_2449 = line_score(_game_2449)

_game_2469 = filts(json.loads(TESTDATA['2469.json']), GAME_KEYS)
_line_2469 = line_score(_game_2469)

_game_2476 = filts(json.loads(TESTDATA['2476.json']), GAME_KEYS)
_line_2476 = line_score(_game_2476)

_dialogs = [
    dialog('40', 'Detroit Tigers', [_line_2449, _line_2469, _line_2476]),
    dialog('47', 'Minnesota Twins', [_line_2449, _line_2469, _line_2476]),
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
