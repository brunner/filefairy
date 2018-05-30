#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugin/recap/samples', '', _path)
sys.path.append(_root)
from util.component.component import table  # noqa
from util.team.team import logo_absolute  # noqa

_s31 = [logo_absolute('31', 'Arizona', 'left'), '76', '86', '28.0', '']
_s32 = [logo_absolute('32', 'Atlanta', 'left'), '77', '85', '18.0', '']
_s33 = [logo_absolute('33', 'Baltimore', 'left'), '70', '92', '29.0', '']
_s34 = [logo_absolute('34', 'Boston', 'left'), '99', '63', '-', 'X']
_s35 = [logo_absolute('35', 'Chicago', 'left'), '82', '80', '6.0', '']
_s36 = [logo_absolute('36', 'Chicago', 'left'), '71', '91', '40.0', '']
_s37 = [logo_absolute('37', 'Cincinnati', 'left'), '111', '51', '-', 'X']
_s38 = [logo_absolute('38', 'Cleveland', 'left'), '76', '86', '12.0', '']
_s39 = [logo_absolute('39', 'Colorado', 'left'), '88', '74', '16.0', '']
_s40 = [logo_absolute('40', 'Detroit', 'left'), '86', '76', '2.0', '']
_s41 = [logo_absolute('41', 'Miami', 'left'), '84', '78', '11.0', '']
_s42 = [logo_absolute('42', 'Houston', 'left'), '85', '77', '13.0', '']
_s43 = [logo_absolute('43', 'Kansas City', 'left'), '76', '86', '12.0', '']
_s44 = [logo_absolute('44', 'Los Angeles', 'left'), '70', '92', '28.0', '']
_s45 = [logo_absolute('45', 'Los Angeles', 'left'), '97', '65', '7.0', '']
_s46 = [logo_absolute('46', 'Milwaukee', 'left'), '77', '85', '34.0', '']
_s47 = [logo_absolute('47', 'Minnesota', 'left'), '88', '74', '-', 'X']
_s48 = [logo_absolute('48', 'New York', 'left'), '88', '74', '11.0', '']
_s49 = [logo_absolute('49', 'New York', 'left'), '95', '67', '-', 'X']
_s50 = [logo_absolute('50', 'Oakland', 'left'), '75', '87', '23.0', '']
_s51 = [logo_absolute('51', 'Philadelphia', 'left'), '75', '87', '20.0', '']
_s52 = [logo_absolute('52', 'Pittsburgh', 'left'), '53', '109', '58.0', '']
_s53 = [logo_absolute('53', 'San Diego', 'left'), '104', '58.0', '-', 'X']
_s54 = [logo_absolute('54', 'Seattle', 'left'), '98', '64', '-', 'X']
_s55 = [logo_absolute('55', 'San Francisco', 'left'), '62', '100', '42.0', '']
_s56 = [logo_absolute('56', 'St. Louis', 'left'), '89', '73', '22.0', '']
_s57 = [logo_absolute('57', 'Tampa Bay', 'left'), '65', '97', '34.0', '']
_s58 = [logo_absolute('58', 'Texas', 'left'), '67', '95', '31.0', '']
_s59 = [logo_absolute('59', 'Toronto', 'left'), '73', '89', '26.0', '']
_s60 = [logo_absolute('60', 'Washington', 'left'), '73', '89', '22.0', '']

_w35 = [logo_absolute('35', 'Chicago', 'left'), '82', '80', '4.0', '']
_w39 = [logo_absolute('39', 'Colorado', 'left'), '88', '74', '1.0', '']
_w40 = [logo_absolute('40', 'Detroit', 'left'), '86', '76', '-', 'X']
_w41 = [logo_absolute('41', 'Miami', 'left'), '84', '78', '5.0', '']
_w42 = [logo_absolute('42', 'Houston', 'left'), '85', '77', '1.0', '']
_w45 = [logo_absolute('45', 'Los Angeles', 'left'), '97', '65', '+8.0', 'X']
_w48 = [logo_absolute('48', 'New York', 'left'), '88', '74', '+2.0', 'X']
_w56 = [logo_absolute('56', 'St. Louis', 'left'), '89', '73', '-', 'X']

_breadcrumbs = [{
    'href': '/fairylab/',
    'name': 'Home'
}, {
    'href': '',
    'name': 'Recap'
}]

_injuries = [
    table(
        clazz='border mt-3',
        head=['Monday, July 4th, 2022'],
        body=[[
            'Pittsburgh Pirates: <a href="../players/player_35155.html">John Barbato</a> diagnosed with a sore forearm, is day-to-day for 5 days.'
        ]]),
    table(
        clazz='border mt-3',
        head=['Sunday, July 3th, 2022'],
        body=[[
            'Los Angeles Angels: SP <a href="../players/player_37318.html">Ty Blach</a> was injured while pitching.  The Diagnosis: back stiffness. This is a day-to-day injury expected to last 5 days.'
        ], [
            'Washington Nationals: RP <a href="../players/player_32624.html">Hunter Strickland</a> was injured while pitching.  The Diagnosis: back spasms. This is a day-to-day injury expected to last 5 days.'
        ], [
            'Tampa Bay Rays: RP <a href="../players/player_1958.html">Javier Medina</a> was injured while pitching.  The diagnosis is not yet known.'
        ], [
            'Pittsburgh Pirates: SP <a href="../players/player_35155.html">John Barbato</a> was injured while pitching.  The diagnosis is not yet known.'
        ], [
            'Pittsburgh Pirates: CF <a href="../players/player_1604.html">Carl Chester</a> was injured on a defensive play.  The diagnosis is not yet known.'
        ], [
            'Detroit Tigers: RP <a href="../players/player_22457.html">Walker Buehler</a> was injured while pitching.  The diagnosis is not yet known.'
        ]])
]
_news = [
    table(
        clazz='border mt-3',
        head=['Monday, July 4th, 2022'],
        body=[[
            '1B <a href="../players/player_33892.html">Viosergy Rosa</a> of the Chicago White Sox honored: Wins the MLB AL Player of the Week Award.'
        ], [
            '1B <a href="../players/player_27194.html">Freddie Freeman</a> of the Atlanta Braves honored: Wins the MLB NL Player of the Week Award.'
        ]])
]
_transactions = [
    table(
        clazz='border mt-3',
        head=['Monday, July 4th, 2022'],
        body=[[
            'San Diego Padres: Signed <a href="../players/player_56862.html">Antonio Marquis</a> to a minor league contract with a signing bonus of $180,000.'
        ], [
            'The Detroit Tigers traded 25-year-old minor league left fielder <a href="../players/player_28672.html">Nick Plummer</a> to the Milwaukee Brewers, getting 33-year-old closer <a href="../players/player_36352.html">Phil Klein</a> in return.'
        ], [
            'The Detroit Tigers traded 25-year-old minor league left fielder <a href="../players/player_25202.html">Wesley Rodriguez</a> and 31-year-old left fielder <a href="../players/player_33588.html">Michael A. Taylor</a> to the Chicago Cubs, getting 30-year-old right fielder <a href="../players/player_35161.html">Drew Vettleson</a> in return.'
        ], [
            'The Detroit Tigers traded 21-year-old minor league shortstop <a href="../players/player_32327.html">Jesus Martinez</a> to the Philadelphia Phillies, getting 28-year-old left fielder <a href="../players/player_37237.html">Mitch Nay</a> in return.'
        ], [
            'The Minnesota Twins traded 25-year-old first baseman <a href="../players/player_39581.html">Lewin Diaz</a> to the Chicago Cubs, getting 30-year-old starting pitcher <a href="../players/player_37975.html">Matt Anderson</a>, 19-year-old minor league starting pitcher <a href="../players/player_22921.html">Juan Monreal</a> and 21-year-old minor league catcher <a href="../players/player_55093.html">Jonathan Salazar</a> in return.'
        ]])
]
_scols = [
    ' class="position-relative text-truncate"', ' class="text-right w-55p"',
    ' class="text-right w-55p"', ' class="text-right w-55p"',
    ' class="text-right w-55p"'
]
_standings = [
    table(
        clazz='table-fixed border mt-3',
        hcols=_scols,
        bcols=_scols,
        head=['AL East', 'W', 'L', 'GB', 'M#'],
        body=[_s34, _s48, _s59, _s33, _s57]),
    table(
        clazz='table-fixed border mt-3',
        hcols=_scols,
        bcols=_scols,
        head=['AL Central', 'W', 'L', 'GB', 'M#'],
        body=[_s47, _s40, _s35, _s38, _s43]),
    table(
        clazz='table-fixed border mt-3',
        hcols=_scols,
        bcols=_scols,
        head=['AL West', 'W', 'L', 'GB', 'M#'],
        body=[_s54, _s42, _s50, _s44, _s58]),
    table(
        clazz='table-fixed border mt-3',
        hcols=_scols,
        bcols=_scols,
        head=['AL Wild Card', 'W', 'L', 'GB', 'M#'],
        body=[_w48, _w40, _w42, _w35]),
    table(
        clazz='table-fixed border mt-3',
        hcols=_scols,
        bcols=_scols,
        head=['NL East', 'W', 'L', 'GB', 'M#'],
        body=[_s49, _s41, _s32, _s51, _s60]),
    table(
        clazz='table-fixed border mt-3',
        hcols=_scols,
        bcols=_scols,
        head=['NL Central', 'W', 'L', 'GB', 'M#'],
        body=[_s37, _s56, _s46, _s36, _s52]),
    table(
        clazz='table-fixed border mt-3',
        hcols=_scols,
        bcols=_scols,
        head=['NL West', 'W', 'L', 'GB', 'M#'],
        body=[_s53, _s45, _s39, _s31, _s55]),
    table(
        clazz='table-fixed border mt-3',
        hcols=_scols,
        bcols=_scols,
        head=['NL Wild Card', 'W', 'L', 'GB', 'M#'],
        body=[_w45, _w56, _w39, _w41])
]

subtitle = ''

tmpl = 'recap.html'

context = {
    'title': 'recap',
    'breadcrumbs': _breadcrumbs,
    'injuries': _injuries,
    'news': _news,
    'transactions': _transactions,
    'standings': _standings
}
