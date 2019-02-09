#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/tasks/oldgameday/samples', '', _path))
from common.elements.elements import anchor  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import table  # noqa
from common.teams.teams import icon_absolute  # noqa

_s31 = icon_absolute('T31', anchor('/oldgameday/1/', 'Arizona Diamondbac'))
_s32 = icon_absolute('T32', anchor('/oldgameday/1/', 'Atlanta Braves'))
_s33 = icon_absolute('T33', anchor('/oldgameday/1/', 'Baltimore Orioles'))
_s34 = icon_absolute('T34', anchor('/oldgameday/2/', 'Boston Red Sox'))
_s35 = icon_absolute('T35', anchor('/oldgameday/1/', 'Chicago White Sox'))
_s36 = icon_absolute('T36', anchor('/oldgameday/1/', 'Chicago Cubs'))
_s37 = icon_absolute('T37', anchor('/oldgameday/2/', 'Cincinnati Reds'))
_s38 = icon_absolute('T38', anchor('/oldgameday/2/', 'Cleveland Indians'))
_s39 = icon_absolute('T39', anchor('/oldgameday/2/', 'Colorado Rockies'))
_s40 = icon_absolute('T40', anchor('/oldgameday/3/', 'Detroit Tigers'))
_s41 = icon_absolute('T41', anchor('/oldgameday/2/', 'Miami Marlins'))
_s42 = icon_absolute('T42', anchor('/oldgameday/1/', 'Houston Astros'))
_s43 = icon_absolute('T43', anchor('/oldgameday/4/', 'Kansas City Royals'))
_s44 = icon_absolute('T44', anchor('/oldgameday/2/', 'Los Angeles Angels'))
_s45 = icon_absolute('T45', anchor('/oldgameday/3/', 'Los Angeles Dodger'))
_s46 = icon_absolute('T46', anchor('/oldgameday/3/', 'Milwaukee Brewers'))
_s47 = icon_absolute('T47', anchor('/oldgameday/5/', 'Minnesota Twins'))
_s48 = icon_absolute('T48', anchor('/oldgameday/3/', 'New York Yankees'))
_s49 = icon_absolute('T49', anchor('/oldgameday/3/', 'New York Mets'))
_s50 = icon_absolute('T50', anchor('/oldgameday/3/', 'Oakland Athletics'))
_s51 = icon_absolute('T51', anchor('/oldgameday/4/', 'Philadelphia Phill'))
_s52 = icon_absolute('T52', anchor('/oldgameday/4/', 'Pittsburgh Pirates'))
_s53 = icon_absolute('T53', anchor('/oldgameday/4/', 'San Diego Padres'))
_s54 = icon_absolute('T54', anchor('/oldgameday/4/', 'Seattle Mariners'))
_s55 = icon_absolute('T55', anchor('/oldgameday/5/', 'San Francisco Gian'))
_s56 = icon_absolute('T56', anchor('/oldgameday/5/', 'St. Louis Cardinal'))
_s57 = icon_absolute('T57', anchor('/oldgameday/4/', 'Tampa Bay Rays'))
_s58 = icon_absolute('T58', anchor('/oldgameday/5/', 'Texas Rangers'))
_s59 = icon_absolute('T59', anchor('/oldgameday/5/', 'Toronto Blue Jays'))
_s60 = icon_absolute('T60', anchor('/oldgameday/5/', 'Washington Nationa'))

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

tmpl = 'oldgameday.html'

context = {'schedule': _schedule}