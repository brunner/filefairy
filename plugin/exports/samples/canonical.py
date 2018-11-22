#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugin/exports/samples', '', _path)
sys.path.append(_root)
from common.elements.elements import card  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import span  # noqa
from common.elements.elements import table  # noqa
from util.team.team import logo_absolute  # noqa

_t31 = [
    cell(content=logo_absolute('31', 'Arizona', 'left')),
    cell(content='5 - 5'),
    cell(content='W1')
]
_t32 = [
    cell(content=logo_absolute('32', 'Atlanta', 'left')),
    cell(content='10 - 0'),
    cell(content='W10')
]
_t33 = [
    cell(content=logo_absolute('33', 'Baltimore', 'left')),
    cell(content='6 - 4'),
    cell(content='W1')
]
_t34 = [
    cell(content=logo_absolute('34', 'Boston', 'left')),
    cell(content='10 - 0'),
    cell(content='W10')
]
_t35 = [
    cell(content=logo_absolute('35', 'Chicago', 'left')),
    cell(content='9 - 1'),
    cell(content='L1')
]
_t36 = [
    cell(content=logo_absolute('36', 'Chicago', 'left')),
    cell(content='8 - 2'),
    cell(content='L1')
]
_t37 = [
    cell(content=logo_absolute('37', 'Cincinnati', 'left')),
    cell(content='10 - 0'),
    cell(content='W10')
]
_t38 = [
    cell(content=logo_absolute('38', 'Cleveland', 'left')),
    cell(content='8 - 2'),
    cell(content='W2')
]
_t39 = [
    cell(content=logo_absolute('39', 'Colorado', 'left')),
    cell(content='10 - 0'),
    cell(content='W10')
]
_t40 = [
    cell(content=logo_absolute('40', 'Detroit', 'left')),
    cell(content='10 - 0'),
    cell(content='W10')
]
_t41 = [
    cell(content=logo_absolute('41', 'Miami', 'left')),
    cell(content='4 - 6'),
    cell(content='W1')
]
_t42 = [
    cell(content=logo_absolute('42', 'Houston', 'left')),
    cell(content='10 - 0'),
    cell(content='W10')
]
_t43 = [
    cell(content=logo_absolute('43', 'Kansas City', 'left')),
    cell(content='9 - 1'),
    cell(content='W5')
]
_t44 = [
    cell(content=logo_absolute('44', 'Los Angeles', 'left')),
    cell(content='7 - 3'),
    cell(content='L1')
]
_t45 = [
    cell(content=logo_absolute('45', 'Los Angeles', 'left')),
    cell(content='5 - 5'),
    cell(content='W2')
]
_t46 = [
    cell(content=logo_absolute('46', 'Milwaukee', 'left')),
    cell(content='10 - 0'),
    cell(content='W10')
]
_t47 = [
    cell(content=logo_absolute('47', 'Minnesota', 'left')),
    cell(content='10 - 0'),
    cell(content='W10')
]
_t48 = [
    cell(content=logo_absolute('48', 'New York', 'left')),
    cell(content='10 - 0'),
    cell(content='W10')
]
_t49 = [
    cell(content=logo_absolute('49', 'New York', 'left')),
    cell(content='8 - 2'),
    cell(content='L1')
]
_t50 = [
    cell(content=logo_absolute('50', 'Oakland', 'left')),
    cell(content='7 - 3'),
    cell(content='L3')
]
_t51 = [
    cell(content=logo_absolute('51', 'Philadelphia', 'left')),
    cell(content='3 - 7'),
    cell(content='L5')
]
_t52 = [
    cell(content=logo_absolute('52', 'Pittsburgh', 'left')),
    cell(content='6 - 4'),
    cell(content='L1')
]
_t53 = [
    cell(content=logo_absolute('53', 'San Diego', 'left')),
    cell(content='9 - 1'),
    cell(content='W8')
]
_t54 = [
    cell(content=logo_absolute('54', 'Seattle', 'left')),
    cell(content='10 - 0'),
    cell(content='W10')
]
_t55 = [
    cell(content=logo_absolute('55', 'San Francisco', 'left')),
    cell(content='2 - 8'),
    cell(content='L4')
]
_t56 = [
    cell(content=logo_absolute('56', 'St. Louis', 'left')),
    cell(content='10 - 0'),
    cell(content='W10')
]
_t57 = [
    cell(content=logo_absolute('57', 'Tampa Bay', 'left')),
    cell(content='10 - 0'),
    cell(content='W10')
]
_t58 = [
    cell(content=logo_absolute('58', 'Texas', 'left')),
    cell(content='9 - 1'),
    cell(content='W9')
]
_t59 = [
    cell(content=logo_absolute('59', 'Toronto', 'left')),
    cell(content='9 - 1'),
    cell(content='W4')
]
_t60 = [
    cell(content=logo_absolute('60', 'Washington', 'left')),
    cell(content='5 - 5'),
    cell(content='L1')
]

_breadcrumbs = [{
    'href': '/',
    'name': 'Fairylab'
}, {
    'href': '',
    'name': 'Exports'
}]

_tcols = [col()] + [col(clazz='text-center')] * 5
_table = table(
    clazz='table-sm',
    hcols=_tcols,
    bcols=_tcols,
    body=[[
        cell(content='AL East'),
        cell(content='BAL'),
        cell(content='BOS'),
        cell(content='NYY'),
        cell(content='TB'),
        cell(content='TOR')
    ], [
        cell(content='AL Central'),
        cell(content=span(['text-success', 'border', 'px-1'], 'CWS')),
        cell(content='CLE'),
        cell(content=span(['text-success', 'border', 'px-1'], 'DET')),
        cell(content='KC'),
        cell(content=span(['text-success', 'border', 'px-1'], 'MIN'))
    ], [
        cell(content='AL West'),
        cell(content='HOU'),
        cell(content=span(['text-success', 'border', 'px-1'], 'LAA')),
        cell(content='OAK'),
        cell(content=span(['text-success', 'border', 'px-1'], 'SEA')),
        cell(content=span(['text-success', 'border', 'px-1'], 'TEX'))
    ], [
        cell(content='NL East'),
        cell(content=span(['text-success', 'border', 'px-1'], 'ATL')),
        cell(content='MIA'),
        cell(content=span(['text-success', 'border', 'px-1'], 'NYM')),
        cell(content='PHI'),
        cell(content=span(['text-success', 'border', 'px-1'], 'WAS'))
    ], [
        cell(content='NL Cental'),
        cell(content=span(['text-success', 'border', 'px-1'], 'CHC')),
        cell(content=span(['text-success', 'border', 'px-1'], 'CIN')),
        cell(content=span(['text-success', 'border', 'px-1'], 'MIL')),
        cell(content='PIT'),
        cell(content=span(['text-success', 'border', 'px-1'], 'STL'))
    ], [
        cell(content='NL West'),
        cell(content='ARI'),
        cell(content='COL'),
        cell(content=span(['text-success', 'border', 'px-1'], 'LAD')),
        cell(content=span(['text-success', 'border', 'px-1'], 'SD')),
        cell(content='SF')
    ]])

_breakdown = [
    span(['text-success', 'border', 'px-1'], '16 new'), '14 old',
    span(['text-secondary'], '0 ai')
]
_info = 'Upcoming sim contains ' + ', '.join(_breakdown) + '.'
_live = card(
    title='53%', info=_info, table=_table, ts='06:02:30 EDT (1985-10-26)')

_scols = [
    col(clazz='position-relative'),
    col(clazz='text-center w-25'),
    col(clazz='text-center w-25')
]
_standings = [
    table(
        clazz='border mt-3',
        hcols=_scols,
        bcols=_scols,
        head=[
            cell(content='AL East'),
            cell(content='Last 10'),
            cell(content='Streak')
        ],
        body=[_t34, _t48, _t57, _t59, _t33]),
    table(
        clazz='border mt-3',
        hcols=_scols,
        bcols=_scols,
        head=[
            cell(content='AL Central'),
            cell(content='Last 10'),
            cell(content='Streak')
        ],
        body=[_t40, _t47, _t43, _t35, _t38]),
    table(
        clazz='border mt-3',
        hcols=_scols,
        bcols=_scols,
        head=[
            cell(content='AL West'),
            cell(content='Last 10'),
            cell(content='Streak')
        ],
        body=[_t42, _t54, _t58, _t44, _t50]),
    table(
        clazz='border mt-3',
        hcols=_scols,
        bcols=_scols,
        head=[
            cell(content='NL East'),
            cell(content='Last 10'),
            cell(content='Streak')
        ],
        body=[_t32, _t49, _t60, _t41, _t51]),
    table(
        clazz='border mt-3',
        hcols=_scols,
        bcols=_scols,
        head=[
            cell(content='NL Central'),
            cell(content='Last 10'),
            cell(content='Streak')
        ],
        body=[_t37, _t46, _t56, _t36, _t52]),
    table(
        clazz='border mt-3',
        hcols=_scols,
        bcols=_scols,
        head=[
            cell(content='NL West'),
            cell(content='Last 10'),
            cell(content='Streak')
        ],
        body=[_t39, _t53, _t45, _t31, _t55])
]

subtitle = ''

tmpl = 'exports.html'

context = {
    'title': 'exports',
    'breadcrumbs': _breadcrumbs,
    'live': _live,
    'standings': _standings
}
