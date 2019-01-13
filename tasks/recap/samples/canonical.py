#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/tasks/recap/samples', '', _path)
sys.path.append(_root)
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import table  # noqa
from util.team.team import logo_absolute  # noqa

_s31 = [
    cell(content=logo_absolute('31', 'Arizona', 'left')),
    cell(content='76'),
    cell(content='86'),
    cell(content='28.0'),
    cell()
]
_s32 = [
    cell(content=logo_absolute('32', 'Atlanta', 'left')),
    cell(content='77'),
    cell(content='85'),
    cell(content='18.0'),
    cell()
]
_s33 = [
    cell(content=logo_absolute('33', 'Baltimore', 'left')),
    cell(content='70'),
    cell(content='92'),
    cell(content='29.0'),
    cell()
]
_s34 = [
    cell(content=logo_absolute('34', 'Boston', 'left')),
    cell(content='99'),
    cell(content='63'),
    cell(content='-'),
    cell(content='X')
]
_s35 = [
    cell(content=logo_absolute('35', 'Chicago', 'left')),
    cell(content='82'),
    cell(content='80'),
    cell(content='6.0'),
    cell()
]
_s36 = [
    cell(content=logo_absolute('36', 'Chicago', 'left')),
    cell(content='71'),
    cell(content='91'),
    cell(content='40.0'),
    cell()
]
_s37 = [
    cell(content=logo_absolute('37', 'Cincinnati', 'left')),
    cell(content='111'),
    cell(content='51'),
    cell(content='-'),
    cell(content='X')
]
_s38 = [
    cell(content=logo_absolute('38', 'Cleveland', 'left')),
    cell(content='76'),
    cell(content='86'),
    cell(content='12.0'),
    cell()
]
_s39 = [
    cell(content=logo_absolute('39', 'Colorado', 'left')),
    cell(content='88'),
    cell(content='74'),
    cell(content='16.0'),
    cell()
]
_s40 = [
    cell(content=logo_absolute('40', 'Detroit', 'left')),
    cell(content='86'),
    cell(content='76'),
    cell(content='2.0'),
    cell()
]
_s41 = [
    cell(content=logo_absolute('41', 'Miami', 'left')),
    cell(content='84'),
    cell(content='78'),
    cell(content='11.0'),
    cell()
]
_s42 = [
    cell(content=logo_absolute('42', 'Houston', 'left')),
    cell(content='85'),
    cell(content='77'),
    cell(content='13.0'),
    cell()
]
_s43 = [
    cell(content=logo_absolute('43', 'Kansas City', 'left')),
    cell(content='76'),
    cell(content='86'),
    cell(content='12.0'),
    cell()
]
_s44 = [
    cell(content=logo_absolute('44', 'Los Angeles', 'left')),
    cell(content='70'),
    cell(content='92'),
    cell(content='28.0'),
    cell()
]
_s45 = [
    cell(content=logo_absolute('45', 'Los Angeles', 'left')),
    cell(content='97'),
    cell(content='65'),
    cell(content='7.0'),
    cell()
]
_s46 = [
    cell(content=logo_absolute('46', 'Milwaukee', 'left')),
    cell(content='77'),
    cell(content='85'),
    cell(content='34.0'),
    cell()
]
_s47 = [
    cell(content=logo_absolute('47', 'Minnesota', 'left')),
    cell(content='88'),
    cell(content='74'),
    cell(content='-'),
    cell(content='X')
]
_s48 = [
    cell(content=logo_absolute('48', 'New York', 'left')),
    cell(content='88'),
    cell(content='74'),
    cell(content='11.0'),
    cell()
]
_s49 = [
    cell(content=logo_absolute('49', 'New York', 'left')),
    cell(content='95'),
    cell(content='67'),
    cell(content='-'),
    cell(content='X')
]
_s50 = [
    cell(content=logo_absolute('50', 'Oakland', 'left')),
    cell(content='75'),
    cell(content='87'),
    cell(content='23.0'),
    cell()
]
_s51 = [
    cell(content=logo_absolute('51', 'Philadelphia', 'left')),
    cell(content='75'),
    cell(content='87'),
    cell(content='20.0'),
    cell()
]
_s52 = [
    cell(content=logo_absolute('52', 'Pittsburgh', 'left')),
    cell(content='53'),
    cell(content='109'),
    cell(content='58.0'),
    cell()
]
_s53 = [
    cell(content=logo_absolute('53', 'San Diego', 'left')),
    cell(content='104'),
    cell(content='58'),
    cell(content='-'),
    cell(content='X')
]
_s54 = [
    cell(content=logo_absolute('54', 'Seattle', 'left')),
    cell(content='98'),
    cell(content='64'),
    cell(content='-'),
    cell(content='X')
]
_s55 = [
    cell(content=logo_absolute('55', 'San Francisco', 'left')),
    cell(content='62'),
    cell(content='100'),
    cell(content='42.0'),
    cell()
]
_s56 = [
    cell(content=logo_absolute('56', 'St. Louis', 'left')),
    cell(content='89'),
    cell(content='73'),
    cell(content='22.0'),
    cell()
]
_s57 = [
    cell(content=logo_absolute('57', 'Tampa Bay', 'left')),
    cell(content='65'),
    cell(content='97'),
    cell(content='34.0'),
    cell()
]
_s58 = [
    cell(content=logo_absolute('58', 'Texas', 'left')),
    cell(content='67'),
    cell(content='95'),
    cell(content='31.0'),
    cell()
]
_s59 = [
    cell(content=logo_absolute('59', 'Toronto', 'left')),
    cell(content='73'),
    cell(content='89'),
    cell(content='26.0'),
    cell()
]
_s60 = [
    cell(content=logo_absolute('60', 'Washington', 'left')),
    cell(content='73'),
    cell(content='89'),
    cell(content='22.0'),
    cell()
]

_w35 = [
    cell(content=logo_absolute('35', 'Chicago', 'left')),
    cell(content='82'),
    cell(content='80'),
    cell(content='4.0'),
    cell()
]
_w39 = [
    cell(content=logo_absolute('39', 'Colorado', 'left')),
    cell(content='88'),
    cell(content='74'),
    cell(content='1.0'),
    cell()
]
_w40 = [
    cell(content=logo_absolute('40', 'Detroit', 'left')),
    cell(content='86'),
    cell(content='76'),
    cell(content='-'),
    cell(content='X')
]
_w41 = [
    cell(content=logo_absolute('41', 'Miami', 'left')),
    cell(content='84'),
    cell(content='78'),
    cell(content='5.0'),
    cell()
]
_w42 = [
    cell(content=logo_absolute('42', 'Houston', 'left')),
    cell(content='85'),
    cell(content='77'),
    cell(content='1.0'),
    cell()
]
_w45 = [
    cell(content=logo_absolute('45', 'Los Angeles', 'left')),
    cell(content='97'),
    cell(content='65'),
    cell(content='+8.0'),
    cell(content='X')
]
_w48 = [
    cell(content=logo_absolute('48', 'New York', 'left')),
    cell(content='88'),
    cell(content='74'),
    cell(content='+2.0'),
    cell(content='X')
]
_w56 = [
    cell(content=logo_absolute('56', 'St. Louis', 'left')),
    cell(content='89'),
    cell(content='73'),
    cell(content='-'),
    cell(content='X')
]

_breadcrumbs = [{
    'href': '/',
    'name': 'Fairylab'
}, {
    'href': '',
    'name': 'Recap'
}]

_injuries = [
    table(
        clazz='border mt-3',
        head=[[cell(content='Monday, July 4th, 2022')]],
        body=[
            [
                cell(
                    content=('Pittsburgh Pirates: <a href="../players/player_3'
                             '5155.html">John Barbato</a> diagnosed with a sor'
                             'e forearm, is day-to-day for 5 days.'))
            ],
        ]),
    table(
        clazz='border mt-3',
        head=[[cell(content='Sunday, July 3th, 2022')]],
        body=[
            [
                cell(
                    content=('Los Angeles Angels: SP <a href="../players/playe'
                             'r_37318.html">Ty Blach</a> was injured while pit'
                             'ching.  The Diagnosis: back stiffness. This is a'
                             ' day-to-day injury expected to last 5 days.'))
            ],
            [
                cell(
                    content=('Washington Nationals: RP <a href="../players/pla'
                             'yer_32624.html">Hunter Strickland</a> was injure'
                             'd while pitching.  The Diagnosis: back spasms. T'
                             'his is a day-to-day injury expected to last 5 da'
                             'ys.'))
            ],
            [
                cell(
                    content=('Tampa Bay Rays: RP <a href="../players/player_19'
                             '58.html">Javier Medina</a> was injured while pit'
                             'ching.  The diagnosis is not yet known.'))
            ],
            [
                cell(
                    content=('Pittsburgh Pirates: SP <a href="../players/playe'
                             'r_35155.html">John Barbato</a> was injured while'
                             ' pitching.  The diagnosis is not yet known.'))
            ],
            [
                cell(
                    content=('Pittsburgh Pirates: CF <a href="../players/playe'
                             'r_1604.html">Carl Cester</a> was injured on a de'
                             'fensive play.  The diagnosis is not yet known.'))
            ],
            [
                cell(
                    content=('Detroit Tigers: RP <a href="../players/player_22'
                             '457.html">Walker Buehler</a> was injured while p'
                             'itching.  The diagnosis is not yet known.'))
            ],
        ])
]
_news = [
    table(
        clazz='border mt-3',
        head=[[cell(content='Monday, July 4th, 2022')]],
        body=[
            [
                cell(
                    content=('1B <a href="../players/player_33892.html">Vioser'
                             'gy Rosa</a> of the Chicago White Sox honored: Wi'
                             'ns the MLB AL Player of the Week Award.'))
            ],
            [
                cell(
                    content=('1B <a href="../players/player_27194.html">Freddi'
                             'e Freeman</a> of the Atlanta Braves honored: Win'
                             's the MLB NL Player of the Week Award.'))
            ],
        ])
]
_transactions = [
    table(
        clazz='border mt-3',
        head=[[cell(content='Monday, July 4th, 2022')]],
        body=[
            [
                cell(
                    content=(
                        'San Diego Padres: Signed <a href="../players/pla'
                        'yer_56862.html">Antonio Marquis</a> to a minor l'
                        'eague contract with a signing bonus of $180,000.'))
            ],
            [
                cell(
                    content=('The Detroit Tigers traded 25-year-old minor leag'
                             'ue left fielder <a href="../players/player_28672'
                             '.html">Nick Plummer</a> to the Milwaukee Brewers'
                             ', getting 33-year-old closer <a href="../players'
                             '/player_36352.html">Phil Klein</a> in return.'))
            ],
            [
                cell(
                    content=('The Detroit Tigers traded 25-year-old minor leag'
                             'ue left fielder <a href="../players/player_25202'
                             '.html">Wesley Rodriguez</a> and 31-year-old left'
                             ' fielder <a href="../players/player_33588.html">'
                             'Michael A. Taylor</a> to the Chicago Cubs, getti'
                             'ng 30-year-old right fielder <a href="../players'
                             '/player_35161.html">Drew Vettleson</a> in return'
                             '.'))
            ],
            [
                cell(
                    content=('The Detroit Tigers traded 21-year-old minor leag'
                             'ue shortstop <a href="../players/player_32327.ht'
                             'ml">Jesus Martinez</a> to the Philadelphia Phill'
                             'ies, getting 28-year-old left fielder <a href=".'
                             './players/player_37237.html">Mitch Nay</a> in re'
                             'turn.'))
            ],
            [
                cell(
                    content=('The Minnesota Twins traded 25-year-old first bas'
                             'eman <a href="../players/player_39581.html">Lewi'
                             'n Diaz</a> to the Chicago Cubs, getting 30-year-'
                             'old starting pitcher <a href="../players/player_'
                             '37975.html">Matt Anderson</a>, 19-year-old minor'
                             ' league starting pitcher <a href="../players/pla'
                             'yer_22921.html">Juan Monreal</a> and 21-year-old'
                             ' minor league catcher <a href="../players/player'
                             '_55093.html">Jonathan Salazar</a> in return.'))
            ],
        ])
]
_scols = [
    col(clazz='position-relative text-truncate'),
    col(clazz='text-right w-55p'),
    col(clazz='text-right w-55p'),
    col(clazz='text-right w-75p'),
    col(clazz='text-right w-55p')
]
_standings = [
    table(
        clazz='table-fixed border mt-3',
        hcols=_scols,
        bcols=_scols,
        head=[[
            cell(content='AL East'),
            cell(content='W'),
            cell(content='L'),
            cell(content='GB'),
            cell(content='M#')
        ]],
        body=[_s34, _s48, _s59, _s33, _s57]),
    table(
        clazz='table-fixed border mt-3',
        hcols=_scols,
        bcols=_scols,
        head=[[
            cell(content='AL Central'),
            cell(content='W'),
            cell(content='L'),
            cell(content='GB'),
            cell(content='M#')
        ]],
        body=[_s47, _s40, _s35, _s38, _s43]),
    table(
        clazz='table-fixed border mt-3',
        hcols=_scols,
        bcols=_scols,
        head=[[
            cell(content='AL West'),
            cell(content='W'),
            cell(content='L'),
            cell(content='GB'),
            cell(content='M#')
        ]],
        body=[_s54, _s42, _s50, _s44, _s58]),
    table(
        clazz='table-fixed border mt-3',
        hcols=_scols,
        bcols=_scols,
        head=[[
            cell(content='AL Wild Card'),
            cell(content='W'),
            cell(content='L'),
            cell(content='GB'),
            cell(content='M#')
        ]],
        body=[_w48, _w40, _w42, _w35]),
    table(
        clazz='table-fixed border mt-3',
        hcols=_scols,
        bcols=_scols,
        head=[[
            cell(content='NL East'),
            cell(content='W'),
            cell(content='L'),
            cell(content='GB'),
            cell(content='M#')
        ]],
        body=[_s49, _s41, _s32, _s51, _s60]),
    table(
        clazz='table-fixed border mt-3',
        hcols=_scols,
        bcols=_scols,
        head=[[
            cell(content='NL Central'),
            cell(content='W'),
            cell(content='L'),
            cell(content='GB'),
            cell(content='M#')
        ]],
        body=[_s37, _s56, _s46, _s36, _s52]),
    table(
        clazz='table-fixed border mt-3',
        hcols=_scols,
        bcols=_scols,
        head=[[
            cell(content='NL West'),
            cell(content='W'),
            cell(content='L'),
            cell(content='GB'),
            cell(content='M#')
        ]],
        body=[_s53, _s45, _s39, _s31, _s55]),
    table(
        clazz='table-fixed border mt-3',
        hcols=_scols,
        bcols=_scols,
        head=[[
            cell(content='NL Wild Card'),
            cell(content='W'),
            cell(content='L'),
            cell(content='GB'),
            cell(content='M#')
        ]],
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
