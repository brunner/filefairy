#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/plugin/gameday', '', _path))
from util.component.component import anchor  # noqa
from util.component.component import table  # noqa
from util.team.team import logo_absolute  # noqa

_s31 = logo_absolute('31', anchor('/gameday/1/', 'Arizona Diamondbac'), 'left')
_s32 = logo_absolute('32', anchor('/gameday/1/', 'Atlanta Braves'), 'left')
_s33 = logo_absolute('33', anchor('/gameday/1/', 'Baltimore Orioles'), 'left')
_s34 = logo_absolute('34', anchor('/gameday/2/', 'Boston Red Sox'), 'left')
_s35 = logo_absolute('35', anchor('/gameday/1/', 'Chicago White Sox'), 'left')
_s36 = logo_absolute('36', anchor('/gameday/1/', 'Chicago Cubs'), 'left')
_s37 = logo_absolute('37', anchor('/gameday/2/', 'Cincinnati Reds'), 'left')
_s38 = logo_absolute('38', anchor('/gameday/2/', 'Cleveland Indians'), 'left')
_s39 = logo_absolute('39', anchor('/gameday/2/', 'Colorado Rockies'), 'left')
_s40 = logo_absolute('40', anchor('/gameday/3/', 'Detroit Tigers'), 'left')
_s41 = logo_absolute('41', anchor('/gameday/2/', 'Miami Marlins'), 'left')
_s42 = logo_absolute('42', anchor('/gameday/1/', 'Houston Astros'), 'left')
_s43 = logo_absolute('43', anchor('/gameday/4/', 'Kansas City Royals'), 'left')
_s44 = logo_absolute('44', anchor('/gameday/2/', 'Los Angeles Angels'), 'left')
_s45 = logo_absolute('45', anchor('/gameday/3/', 'Los Angeles Dodger'), 'left')
_s46 = logo_absolute('46', anchor('/gameday/3/', 'Milwaukee Brewers'), 'left')
_s47 = logo_absolute('47', anchor('/gameday/5/', 'Minnesota Twins'), 'left')
_s48 = logo_absolute('48', anchor('/gameday/3/', 'New York Yankees'), 'left')
_s49 = logo_absolute('49', anchor('/gameday/3/', 'New York Mets'), 'left')
_s50 = logo_absolute('50', anchor('/gameday/3/', 'Oakland Athletics'), 'left')
_s51 = logo_absolute('51', anchor('/gameday/4/', 'Philadelphia Phill'), 'left')
_s52 = logo_absolute('52', anchor('/gameday/4/', 'Pittsburgh Pirates'), 'left')
_s53 = logo_absolute('53', anchor('/gameday/4/', 'San Diego Padres'), 'left')
_s54 = logo_absolute('54', anchor('/gameday/4/', 'Seattle Mariners'), 'left')
_s55 = logo_absolute('55', anchor('/gameday/5/', 'San Francisco Gian'), 'left')
_s56 = logo_absolute('56', anchor('/gameday/5/', 'St. Louis Cardinal'), 'left')
_s57 = logo_absolute('57', anchor('/gameday/4/', 'Tampa Bay Rays'), 'left')
_s58 = logo_absolute('58', anchor('/gameday/5/', 'Texas Rangers'), 'left')
_s59 = logo_absolute('59', anchor('/gameday/5/', 'Toronto Blue Jays'), 'left')
_s60 = logo_absolute('60', anchor('/gameday/5/', 'Washington Nationa'), 'left')

_breadcrumbs = [{
    'href': '/',
    'name': 'Fairylab'
}, {
    'href': '',
    'name': 'Gameday'
}]

_schedule = [
    table(
        clazz='table-fixed border border-bottom-0 mt-3',
        head=['American League East']),
    table(
        clazz='table-fixed border',
        bcols=[' class="position-relative text-truncate"'],
        body=[
            [_s33],
            [_s34],
            [_s48],
            [_s57],
            [_s59],
        ]),
    table(
        clazz='table-fixed border border-bottom-0 mt-3',
        head=['American League Central']),
    table(
        clazz='table-fixed border',
        bcols=[' class="position-relative text-truncate"'],
        body=[
            [_s35],
            [_s38],
            [_s40],
            [_s43],
            [_s47],
        ]),
    table(
        clazz='table-fixed border border-bottom-0 mt-3',
        head=['American League West']),
    table(
        clazz='table-fixed border',
        bcols=[' class="position-relative text-truncate"'],
        body=[
            [_s42],
            [_s44],
            [_s50],
            [_s54],
            [_s58],
        ]),
    table(
        clazz='table-fixed border border-bottom-0 mt-3',
        head=['National League East']),
    table(
        clazz='table-fixed border',
        bcols=[' class="position-relative text-truncate"'],
        body=[
            [_s32],
            [_s41],
            [_s49],
            [_s51],
            [_s60],
        ]),
    table(
        clazz='table-fixed border border-bottom-0 mt-3',
        head=['National League Central']),
    table(
        clazz='table-fixed border',
        bcols=[' class="position-relative text-truncate"'],
        body=[
            [_s36],
            [_s37],
            [_s46],
            [_s52],
            [_s56],
        ]),
    table(
        clazz='table-fixed border border-bottom-0 mt-3',
        head=['National League West']),
    table(
        clazz='table-fixed border',
        bcols=[' class="position-relative text-truncate"'],
        body=[
            [_s31],
            [_s39],
            [_s45],
            [_s53],
            [_s55],
        ]),
]

subtitle = ''

tmpl = 'gameday.html'

context = {
    'title': 'gameday',
    'breadcrumbs': _breadcrumbs,
    'schedule': _schedule
}
