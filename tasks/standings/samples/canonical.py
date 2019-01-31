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
from common.teams.teams import encoding_keys  # noqa
from common.teams.teams import icon_absolute  # noqa
from common.teams.teams import icon_badge  # noqa
from common.test.test import get_testdata  # noqa
from services.division.division import condensed_league  # noqa
from services.division.division import expanded_league  # noqa
from services.scoreboard.scoreboard import line_score_body  # noqa
from services.scoreboard.scoreboard import line_score_foot  # noqa
from services.scoreboard.scoreboard import line_score_head  # noqa
from services.scoreboard.scoreboard import pending_score_body  # noqa


def _table(keys, table_):
    return {k: table_.get(k, '0-0') for k in keys}


EXPANDED_COLS = [
    col(clazz='position-relative text-truncate'),
    col(clazz='text-right w-55p'),
    col(clazz='text-right w-55p'),
    col(clazz='text-right w-75p')
]

ENCODINGS = encoding_keys()

DIALOG_TEAMS = ['T31', 'T40', 'T44', 'T45', 'T47', 'T48', 'T55']

LEAGUE_ALE = ['T33', 'T34', 'T48', 'T57', 'T59']
LEAGUE_ALC = ['T35', 'T38', 'T40', 'T43', 'T47']
LEAGUE_ALW = ['T42', 'T44', 'T50', 'T54', 'T58']
LEAGUE_NLE = ['T32', 'T41', 'T49', 'T51', 'T60']
LEAGUE_NLC = ['T36', 'T37', 'T46', 'T52', 'T56']
LEAGUE_NLW = ['T31', 'T39', 'T45', 'T53', 'T55']

STATSPLUS_TABLE = {
    'T31': '1-0',
    'T40': '0-3',
    'T44': '0-1',
    'T45': '0-1',
    'T47': '3-0',
    'T48': '1-0',
    'T55': '0-1'
}
EXPANDED_AL = [
    ('East', _table(LEAGUE_ALE, STATSPLUS_TABLE)),
    ('Central', _table(LEAGUE_ALC, STATSPLUS_TABLE)),
    ('West', _table(LEAGUE_ALW, STATSPLUS_TABLE)),
]
EXPANDED_NL = [
    ('East', _table(LEAGUE_NLE, STATSPLUS_TABLE)),
    ('Central', _table(LEAGUE_NLC, STATSPLUS_TABLE)),
    ('West', _table(LEAGUE_NLW, STATSPLUS_TABLE)),
]

CONDENSED_TABLE = {
    e: (STATSPLUS_TABLE.get(e, '0-0'), e in DIALOG_TEAMS)
    for e in ENCODINGS
}
CONDENSED_AL = [
    ('East', _table(LEAGUE_ALE, CONDENSED_TABLE)),
    ('Central', _table(LEAGUE_ALC, CONDENSED_TABLE)),
    ('West', _table(LEAGUE_ALW, CONDENSED_TABLE)),
]
CONDENSED_NL = [
    ('East', _table(LEAGUE_NLE, CONDENSED_TABLE)),
    ('Central', _table(LEAGUE_NLC, CONDENSED_TABLE)),
    ('West', _table(LEAGUE_NLW, CONDENSED_TABLE)),
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
    condensed_league('American League', CONDENSED_AL),
    condensed_league('National League', CONDENSED_NL),
]

_expanded_al = expanded_league('American League', EXPANDED_AL)
_expanded_nl = expanded_league('National League', EXPANDED_NL)
_expanded = _expanded_al + _expanded_nl

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
