#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugin/exports/samples', '', _path)
sys.path.append(_root)
from plugin.exports.exports import Exports  # noqa
from util.component.component import card  # noqa
from util.component.component import table  # noqa
from util.team.team import logo_absolute  # noqa

_t31 = [logo_absolute('31', 'Arizona', 'left'), '5 - 5', 'W1']
_t32 = [logo_absolute('32', 'Atlanta', 'left'), '10 - 0', 'W10']
_t33 = [logo_absolute('33', 'Baltimore', 'left'), '6 - 4', 'W1']
_t34 = [logo_absolute('34', 'Boston', 'left'), '10 - 0', 'W10']
_t35 = [logo_absolute('35', 'Chicago', 'left'), '9 - 1', 'L1']
_t36 = [logo_absolute('36', 'Chicago', 'left'), '8 - 2', 'L1']
_t37 = [logo_absolute('37', 'Cincinnati', 'left'), '10 - 0', 'W10']
_t38 = [logo_absolute('38', 'Cleveland', 'left'), '8 - 2', 'W2']
_t39 = [logo_absolute('39', 'Colorado', 'left'), '10 - 0', 'W10']
_t40 = [logo_absolute('40', 'Detroit', 'left'), '10 - 0', 'W10']
_t41 = [logo_absolute('41', 'Miami', 'left'), '4 - 6', 'W1']
_t42 = [logo_absolute('42', 'Houston', 'left'), '10 - 0', 'W10']
_t43 = [logo_absolute('43', 'Kansas City', 'left'), '9 - 1', 'W5']
_t44 = [logo_absolute('44', 'Los Angeles', 'left'), '7 - 3', 'L1']
_t45 = [logo_absolute('45', 'Los Angeles', 'left'), '5 - 5', 'W2']
_t46 = [logo_absolute('46', 'Milwaukee', 'left'), '10 - 0', 'W10']
_t47 = [logo_absolute('47', 'Minnesota', 'left'), '10 - 0', 'W10']
_t48 = [logo_absolute('48', 'New York', 'left'), '10 - 0', 'W10']
_t49 = [logo_absolute('49', 'New York', 'left'), '8 - 2', 'L1']
_t50 = [logo_absolute('50', 'Oakland', 'left'), '7 - 3', 'L3']
_t51 = [logo_absolute('51', 'Philadelphia', 'left'), '3 - 7', 'L5']
_t52 = [logo_absolute('52', 'Pittsburgh', 'left'), '6 - 4', 'L1']
_t53 = [logo_absolute('53', 'San Diego', 'left'), '9 - 1', 'W8']
_t54 = [logo_absolute('54', 'Seattle', 'left'), '10 - 0', 'W10']
_t55 = [logo_absolute('55', 'San Francisco', 'left'), '2 - 8', 'L4']
_t56 = [logo_absolute('56', 'St. Louis', 'left'), '10 - 0', 'W10']
_t57 = [logo_absolute('57', 'Tampa Bay', 'left'), '10 - 0', 'W10']
_t58 = [logo_absolute('58', 'Texas', 'left'), '9 - 1', 'W9']
_t59 = [logo_absolute('59', 'Toronto', 'left'), '9 - 1', 'W4']
_t60 = [logo_absolute('60', 'Washington', 'left'), '5 - 5', 'L1']

_breadcrumbs = [{
    'href': '/fairylab/',
    'name': 'Home'
}, {
    'href': '',
    'name': 'Exports'
}]

_tcols = [''] + [' class="text-center"'] * 5
_table = table(
    clazz='table-sm',
    hcols=_tcols,
    bcols=_tcols,
    body=[['AL East', 'BAL', 'BOS', 'NYY', 'TB', 'TOR'], [
        'AL Central',
        Exports._success('CWS'), 'CLE',
        Exports._success('DET'), 'KC',
        Exports._success('MIN')
    ], [
        'AL West', 'HOU',
        Exports._success('LAA'), 'OAK',
        Exports._success('SEA'),
        Exports._success('TEX')
    ], [
        'NL East',
        Exports._success('ATL'), 'MIA',
        Exports._success('NYM'), 'PHI',
        Exports._success('WAS')
    ], [
        'NL Central',
        Exports._success('CHC'),
        Exports._success('CIN'),
        Exports._success('MIL'), 'PIT',
        Exports._success('STL')
    ], [
        'NL West', 'ARI', 'COL',
        Exports._success('LAD'),
        Exports._success('SD'), 'SF'
    ]])

_breakdown = [Exports._success('16 new'), '14 old', Exports._secondary('0 ai')]
_info = 'Upcoming sim contains ' + ', '.join(_breakdown) + '.'
_live = card(title='53%', info=_info, table=_table, ts='30s ago')

_scols = [
    'class="position-relative"', ' class="text-center w-25"',
    ' class="text-center w-25"'
]
_standings = [
    table(
        clazz='border mt-3',
        hcols=_scols,
        bcols=_scols,
        head=['AL East', 'Last 10', 'Streak'],
        body=[_t34, _t48, _t57, _t59, _t33]),
    table(
        clazz='border mt-3',
        hcols=_scols,
        bcols=_scols,
        head=['AL Central', 'Last 10', 'Streak'],
        body=[_t40, _t47, _t43, _t35, _t38]),
    table(
        clazz='border mt-3',
        hcols=_scols,
        bcols=_scols,
        head=['AL West', 'Last 10', 'Streak'],
        body=[_t42, _t54, _t58, _t44, _t50]),
    table(
        clazz='border mt-3',
        hcols=_scols,
        bcols=_scols,
        head=['NL East', 'Last 10', 'Streak'],
        body=[_t32, _t49, _t60, _t41, _t51]),
    table(
        clazz='border mt-3',
        hcols=_scols,
        bcols=_scols,
        head=['NL Central', 'Last 10', 'Streak'],
        body=[_t37, _t46, _t56, _t36, _t52]),
    table(
        clazz='border mt-3',
        hcols=_scols,
        bcols=_scols,
        head=['NL West', 'Last 10', 'Streak'],
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
