#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/tasks/gameday/samples', '', _path))
from common.elements.elements import anchor  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import table  # noqa
from common.teams.teams import icon_absolute  # noqa

_s31 = icon_absolute('T31', anchor('/gameday/1/', 'Arizona Diamondbac'), '20')
_s32 = icon_absolute('T32', anchor('/gameday/1/', 'Atlanta Braves'), '20')
_s33 = icon_absolute('T33', anchor('/gameday/1/', 'Baltimore Orioles'), '20')
_s34 = icon_absolute('T34', anchor('/gameday/2/', 'Boston Red Sox'), '20')
_s35 = icon_absolute('T35', anchor('/gameday/1/', 'Chicago White Sox'), '20')
_s36 = icon_absolute('T36', anchor('/gameday/1/', 'Chicago Cubs'), '20')
_s37 = icon_absolute('T37', anchor('/gameday/2/', 'Cincinnati Reds'), '20')
_s38 = icon_absolute('T38', anchor('/gameday/2/', 'Cleveland Indians'), '20')
_s39 = icon_absolute('T39', anchor('/gameday/2/', 'Colorado Rockies'), '20')
_s40 = icon_absolute('T40', anchor('/gameday/3/', 'Detroit Tigers'), '20')
_s41 = icon_absolute('T41', anchor('/gameday/2/', 'Miami Marlins'), '20')
_s42 = icon_absolute('T42', anchor('/gameday/1/', 'Houston Astros'), '20')
_s43 = icon_absolute('T43', anchor('/gameday/4/', 'Kansas City Royals'), '20')
_s44 = icon_absolute('T44', anchor('/gameday/2/', 'Los Angeles Angels'), '20')
_s45 = icon_absolute('T45', anchor('/gameday/3/', 'Los Angeles Dodger'), '20')
_s46 = icon_absolute('T46', anchor('/gameday/3/', 'Milwaukee Brewers'), '20')
_s47 = icon_absolute('T47', anchor('/gameday/5/', 'Minnesota Twins'), '20')
_s48 = icon_absolute('T48', anchor('/gameday/3/', 'New York Yankees'), '20')
_s49 = icon_absolute('T49', anchor('/gameday/3/', 'New York Mets'), '20')
_s50 = icon_absolute('T50', anchor('/gameday/3/', 'Oakland Athletics'), '20')
_s51 = icon_absolute('T51', anchor('/gameday/4/', 'Philadelphia Phill'), '20')
_s52 = icon_absolute('T52', anchor('/gameday/4/', 'Pittsburgh Pirates'), '20')
_s53 = icon_absolute('T53', anchor('/gameday/4/', 'San Diego Padres'), '20')
_s54 = icon_absolute('T54', anchor('/gameday/4/', 'Seattle Mariners'), '20')
_s55 = icon_absolute('T55', anchor('/gameday/5/', 'San Francisco Gian'), '20')
_s56 = icon_absolute('T56', anchor('/gameday/5/', 'St. Louis Cardinal'), '20')
_s57 = icon_absolute('T57', anchor('/gameday/4/', 'Tampa Bay Rays'), '20')
_s58 = icon_absolute('T58', anchor('/gameday/5/', 'Texas Rangers'), '20')
_s59 = icon_absolute('T59', anchor('/gameday/5/', 'Toronto Blue Jays'), '20')
_s60 = icon_absolute('T60', anchor('/gameday/5/', 'Washington Nationa'), '20')

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
        head=[[cell(content='American League East')]]),
    table(
        clazz='table-fixed border',
        bcols=[col(clazz='position-relative text-truncate')],
        body=[
            [cell(content=_s33)],
            [cell(content=_s34)],
            [cell(content=_s48)],
            [cell(content=_s57)],
            [cell(content=_s59)],
        ]),
    table(
        clazz='table-fixed border border-bottom-0 mt-3',
        head=[[cell(content='American League Central')]]),
    table(
        clazz='table-fixed border',
        bcols=[col(clazz='position-relative text-truncate')],
        body=[
            [cell(content=_s35)],
            [cell(content=_s38)],
            [cell(content=_s40)],
            [cell(content=_s43)],
            [cell(content=_s47)],
        ]),
    table(
        clazz='table-fixed border border-bottom-0 mt-3',
        head=[[cell(content='American League West')]]),
    table(
        clazz='table-fixed border',
        bcols=[col(clazz='position-relative text-truncate')],
        body=[
            [cell(content=_s42)],
            [cell(content=_s44)],
            [cell(content=_s50)],
            [cell(content=_s54)],
            [cell(content=_s58)],
        ]),
    table(
        clazz='table-fixed border border-bottom-0 mt-3',
        head=[[cell(content='National League East')]]),
    table(
        clazz='table-fixed border',
        bcols=[col(clazz='position-relative text-truncate')],
        body=[
            [cell(content=_s32)],
            [cell(content=_s41)],
            [cell(content=_s49)],
            [cell(content=_s51)],
            [cell(content=_s60)],
        ]),
    table(
        clazz='table-fixed border border-bottom-0 mt-3',
        head=[[cell(content='National League Central')]]),
    table(
        clazz='table-fixed border',
        bcols=[col(clazz='position-relative text-truncate')],
        body=[
            [cell(content=_s36)],
            [cell(content=_s37)],
            [cell(content=_s46)],
            [cell(content=_s52)],
            [cell(content=_s56)],
        ]),
    table(
        clazz='table-fixed border border-bottom-0 mt-3',
        head=[[cell(content='National League West')]]),
    table(
        clazz='table-fixed border',
        bcols=[col(clazz='position-relative text-truncate')],
        body=[
            [cell(content=_s31)],
            [cell(content=_s39)],
            [cell(content=_s45)],
            [cell(content=_s53)],
            [cell(content=_s55)],
        ]),
]

subtitle = ''

tmpl = 'gameday.html'

context = {
    'title': 'gameday',
    'breadcrumbs': _breadcrumbs,
    'schedule': _schedule
}
