#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/tasks/statsplus/samples', '', _path)
sys.path.append(_root)
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import table  # noqa
from util.team.team import logo_absolute  # noqa
from util.team.team import logo_inline  # noqa

_l31 = cell(content=logo_inline('31', '4-3'))
_l32 = cell(content=logo_inline('32', '5-1'))
_l33 = cell(content=logo_inline('33', '0-6'))
_l34 = cell(content=logo_inline('34', '4-3'))
_l35 = cell(content=logo_inline('35', '3-3'))
_l36 = cell(content=logo_inline('36', '3-4'))
_l37 = cell(content=logo_inline('37', '3-3'))
_l38 = cell(content=logo_inline('38', '1-4'))
_l39 = cell(content=logo_inline('39', '2-3'))
_l40 = cell(content=logo_inline('40', '4-3'))
_l41 = cell(content=logo_inline('41', '2-5'))
_l42 = cell(content=logo_inline('42', '5-2'))
_l43 = cell(content=logo_inline('43', '4-3'))
_l44 = cell(content=logo_inline('44', '3-3'))
_l45 = cell(content=logo_inline('45', '4-2'))
_l46 = cell(content=logo_inline('46', '2-4'))
_l47 = cell(content=logo_inline('47', '4-3'))
_l48 = cell(content=logo_inline('48', '4-2'))
_l49 = cell(content=logo_inline('49', '5-1'))
_l50 = cell(content=logo_inline('50', '4-3'))
_l51 = cell(content=logo_inline('51', '5-2'))
_l52 = cell(content=logo_inline('52', '1-5'))
_l53 = cell(content=logo_inline('53', '4-2'))
_l54 = cell(content=logo_inline('54', '2-5'))
_l55 = cell(content=logo_inline('55', '2-5'))
_l56 = cell(content=logo_inline('56', '6-0'))
_l57 = cell(content=logo_inline('57', '4-3'))
_l58 = cell(content=logo_inline('58', '3-3'))
_l59 = cell(content=logo_inline('59', '2-4'))
_l60 = cell(content=logo_inline('60', '1-6'))

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
    'name': 'Statsplus'
}]

_al = [[_l48, _l34, _l57, _l59, _l33], [_l40, _l43, _l47, _l35, _l38],
       [_l42, _l50, _l44, _l58, _l54]]
_nl = [[_l32, _l49, _l51, _l41, _l60], [_l56, _l37, _l36, _l46, _l52],
       [_l45, _l53, _l31, _l39, _l55]]
_lcols = [col(clazz='td-sm position-relative text-center w-20')] * 5
_live = [
    table(
        clazz='table-fixed border border-bottom-0 mt-3',
        hcols=[col(clazz='text-center')],
        head=[cell(content='American League')]),
    table(
        clazz='table-fixed border',
        bcols=_lcols,
        body=_al,
    ),
    table(
        clazz='table-fixed border border-bottom-0 mt-3',
        hcols=[col(clazz='text-center')],
        head=[cell(content='National League')]),
    table(clazz='table-fixed border', bcols=_lcols, body=_nl)
]

_scores = [
    table(
        clazz='border mt-3',
        head=[cell(content='Sunday, October 9th, 2022')],
        body=[
            [
                cell(
                    content=('<a href="https://orangeandblueleaguebaseball.com'
                             '/StatsLab/reports/news/html/box_scores/game_box_'
                             '2998.html">Arizona Diamondbacks 4, Los Angeles D'
                             'odgers 2</a>'))
            ],
            [
                cell(
                    content=('<a href="https://orangeandblueleaguebaseball.com'
                             '/StatsLab/reports/news/html/box_scores/game_box_'
                             '3003.html">Atlanta Braves 2, Los Angeles Angels '
                             '1</a>'))
            ],
            [
                cell(
                    content=('<a href="https://orangeandblueleaguebaseball.com'
                             '/StatsLab/reports/news/html/box_scores/game_box_'
                             '2996.html">Cincinnati Reds 7, Milwaukee Brewers '
                             '2</a>'))
            ],
            [
                cell(
                    content=('<a href="https://orangeandblueleaguebaseball.com'
                             '/StatsLab/reports/news/html/box_scores/game_box_'
                             '3002.html">Detroit Tigers 11, Chicago White Sox '
                             '4</a>'))
            ],
            [
                cell(
                    content=('<a href="https://orangeandblueleaguebaseball.com'
                             '/StatsLab/reports/news/html/box_scores/game_box_'
                             '2993.html">Houston Astros 7, Seattle Mariners 2<'
                             '/a>'))
            ],
            [
                cell(
                    content=('<a href="https://orangeandblueleaguebaseball.com'
                             '/StatsLab/reports/news/html/box_scores/game_box_'
                             '2991.html">Kansas City Royals 8, Cleveland India'
                             'ns 2</a>'))
            ],
            [
                cell(
                    content=(
                        '<a href="https://orangeandblueleaguebaseball.com'
                        '/StatsLab/reports/news/html/box_scores/game_box_'
                        '14721.html">Miami Marlins 6, Chicago Cubs 2</a>'))
            ],
            [
                cell(
                    content=('<a href="https://orangeandblueleaguebaseball.com'
                             '/StatsLab/reports/news/html/box_scores/game_box_'
                             '3001.html">New York Mets 1, San Francisco Giants'
                             ' 0</a>'))
            ],
            [
                cell(
                    content=('<a href="https://orangeandblueleaguebaseball.com'
                             '/StatsLab/reports/news/html/box_scores/game_box_'
                             '3000.html">New York Yankees 5, Baltimore Orioles'
                             ' 3</a>'))
            ],
            [
                cell(
                    content=('<a href="https://orangeandblueleaguebaseball.com'
                             '/StatsLab/reports/news/html/box_scores/game_box_'
                             '2992.html">Philadelphia Phillies 3, Washington N'
                             'ationals 1</a>'))
            ],
            [
                cell(
                    content=('<a href="https://orangeandblueleaguebaseball.com'
                             '/StatsLab/reports/news/html/box_scores/game_box_'
                             '2999.html">San Diego Padres 8, Colorado Rockies '
                             '2</a>'))
            ],
            [
                cell(
                    content=('<a href="https://orangeandblueleaguebaseball.com'
                             '/StatsLab/reports/news/html/box_scores/game_box_'
                             '2990.html">St. Louis Cardinals 5, Pittsburgh Pir'
                             'ates 4</a>'))
            ],
            [
                cell(
                    content=('<a href="https://orangeandblueleaguebaseball.com'
                             '/StatsLab/reports/news/html/box_scores/game_box_'
                             '2997.html">Tampa Bay Rays 12, Boston Red Sox 9</'
                             'a>'))
            ],
            [
                cell(
                    content=('<a href="https://orangeandblueleaguebaseball.com'
                             '/StatsLab/reports/news/html/box_scores/game_box_'
                             '2994.html">Texas Rangers 5, Oakland Athletics 3<'
                             '/a>'))
            ],
            [
                cell(
                    content=('<a href="https://orangeandblueleaguebaseball.com'
                             '/StatsLab/reports/news/html/box_scores/game_box_'
                             '2995.html">Toronto Blue Jays 8, Minnesota Twins '
                             '2</a>'))
            ],
        ]),
    table(
        clazz='border mt-3',
        head=[cell(content='Saturday, October 8th, 2022')],
        body=[
            [
                cell(
                    content=('<a href="https://orangeandblueleaguebaseball.com'
                             '/StatsLab/reports/news/html/box_scores/game_box_'
                             '2979.html">Atlanta Braves 10, Los Angeles Angels'
                             ' 5</a>'))
            ],
            [
                cell(
                    content=('<a href="https://orangeandblueleaguebaseball.com'
                             '/StatsLab/reports/news/html/box_scores/game_box_'
                             '2984.html">Boston Red Sox 10, Tampa Bay Rays 5</'
                             'a>'))
            ],
            [
                cell(
                    content=('<a href="https://orangeandblueleaguebaseball.com'
                             '/StatsLab/reports/news/html/box_scores/game_box_'
                             '297.html">Chicago Cubs 10, Miami Marlins 2</a>'))
            ],
            [
                cell(
                    content=('<a href="https://orangeandblueleaguebaseball.com'
                             '/StatsLab/reports/news/html/box_scores/game_box_'
                             '2977.html">Chicago White Sox 5, Detroit Tigers 2'
                             '</a>'))
            ],
            [
                cell(
                    content=('<a href="https://orangeandblueleaguebaseball.com'
                             '/StatsLab/reports/news/html/box_scores/game_box_'
                             '2983.html">Cincinnati Reds 8, Milwaukee Brewers '
                             '0</a>'))
            ],
            [
                cell(
                    content=('<a href="https://orangeandblueleaguebaseball.com'
                             '/StatsLab/reports/news/html/box_scores/game_box_'
                             '2989.html">Cleveland Indians 3, Kansas City Roya'
                             'ls 2</a>'))
            ],
            [
                cell(
                    content=('<a href="https://orangeandblueleaguebaseball.com'
                             '/StatsLab/reports/news/html/box_scores/game_box_'
                             '2976.html">Houston Astors 6, Seattle Mariners 3<'
                             '/a>'))
            ],
            [
                cell(
                    content=('<a href="https://orangeandblueleaguebaseball.com'
                             '/StatsLab/reports/news/html/box_scores/game_box_'
                             '2978.html">Los Angeles Dodgers 5, Arizona Diamon'
                             'dbacks 1</a>'))
            ],
            [
                cell(
                    content=('<a href="https://orangeandblueleaguebaseball.com'
                             '/StatsLab/reports/news/html/box_scores/game_box_'
                             '2981.html">Minnesota Twins 10, Toronto Blue Jays'
                             ' 7</a>'))
            ],
            [
                cell(
                    content=('<a href="https://orangeandblueleaguebaseball.com'
                             '/StatsLab/reports/news/html/box_scores/game_box_'
                             '2987.html">New York Yankees 5, Baltimore Orioles'
                             ' 4</a>'))
            ],
            [
                cell(
                    content=('<a href="https://orangeandblueleaguebaseball.com'
                             '/StatsLab/reports/news/html/box_scores/game_box_'
                             '2982.html">Philadelphia Phillies 3, Washington N'
                             'ationals 2</a>'))
            ],
            [
                cell(
                    content=('<a href="https://orangeandblueleaguebaseball.com'
                             '/StatsLab/reports/news/html/box_scores/game_box_'
                             '2986.html">San Diego Padres 6, Colorado Rockies '
                             '5</a>'))
            ],
            [
                cell(
                    content=('<a href="https://orangeandblueleaguebaseball.com'
                             '/StatsLab/reports/news/html/box_scores/game_box_'
                             '2985.html">San Francisco Giants 5, New York Mets'
                             ' 4</a>'))
            ],
            [
                cell(
                    content=('<a href="https://orangeandblueleaguebaseball.com'
                             '/StatsLab/reports/news/html/box_scores/game_box_'
                             '2988.html">St. Louis Cardinals 4, Pittsburgh Pir'
                             'ates 1</a>'))
            ],
            [
                cell(
                    content=('<a href="https://orangeandblueleaguebaseball.com'
                             '/StatsLab/reports/news/html/box_scores/game_box_'
                             '2980.html">Texas Rangers 9, Oakland Athletics 1<'
                             '/a>'))
            ],
        ])
]

_injuries = [
    table(
        clazz='border mt-3',
        head=[cell(content='Sunday, October 9th, 2022')],
        body=[
            [
                cell(
                    content=('RF <a href="https://orangeandblueleaguebaseball.'
                             'com/StatsLab/reports/news/html/players/player_36'
                             '649.html">Elier Hernandez</a> was injured while '
                             'running the bases (Cleveland Indians @ Kansas Ci'
                             'ty Royals)'))
            ],
            [
                cell(
                    content=('RF <a href="https://orangeandblueleaguebaseball.'
                             'com/StatsLab/reports/news/html/players/player_34'
                             '118.html">Gregory Polanco</a> was injured on a d'
                             'efensive play (Milwaukee Brewers @ Cincinnati Re'
                             'ds)'))
            ],
            [
                cell(
                    content=('SS <a href="https://orangeandblueleaguebaseball.'
                             'com/StatsLab/reports/news/html/players/player_30'
                             '016.html">Austin Bodrato</a> was injured while r'
                             'unning the bases (Milwaukee Brewers @ Cincinnati'
                             ' Reds)'))
            ],
        ]),
    table(
        clazz='border mt-3',
        head=[cell(content='Saturday, October 8th, 2022')],
        body=[
            [
                cell(
                    content=('3B <a href="https://orangeandblueleaguebaseball.'
                             'com/StatsLab/reports/news/html/players/player_33'
                             '777.html">Kaleb Cowart</a> was injured in a coll'
                             'ision at a base (Cleveland Indians @ Kansas City'
                             ' Royals)'))
            ],
            [
                cell(
                    content=('LF <a href="https://orangeandblueleaguebaseball.'
                             'com/StatsLab/reports/news/html/players/player_29'
                             '996.html">Keon Broxton</a> was injured while thr'
                             'owing the ball (Houston Astros @ Seattle Mariner'
                             's)'))
            ],
            [
                cell(
                    content=('LF <a href="https://orangeandblueleaguebaseball.'
                             'com/StatsLab/reports/news/html/players/player_26'
                             '747.html">Desmond Lindsay</a> was injured on a d'
                             'efensive play (New York Yankees @ Baltimore Orio'
                             'les)'))
            ],
        ])
]

_highlights = [
    table(
        clazz='border mt-3',
        head=[cell(content='Saturday, October 8th, 2022')],
        body=[
            [
                cell(
                    content=('<a href="https://orangeandblueleaguebaseball.com'
                             '/StatsLab/reports/news/html/players/player_38868'
                             '.html">Connor Harrell</a> ties the BOS regular s'
                             'eason game record for runs with 4 (Boston Red So'
                             'x @ Tampa Bay Rays)'))
            ],
        ])
]

_fcols = [
    col(clazz='position-relative text-truncate'),
    col(clazz='text-right w-55p'),
    col(clazz='text-right w-55p'),
    col(clazz='text-right w-75p'),
    col(clazz='text-right w-55p')
]
_forecast = [
    table(
        clazz='table-fixed border mt-3',
        hcols=_fcols,
        bcols=_fcols,
        head=[
            cell(content='AL East'),
            cell(content='W'),
            cell(content='L'),
            cell(content='GB'),
            cell(content='M#')
        ],
        body=[_s34, _s48, _s59, _s33, _s57]),
    table(
        clazz='table-fixed border mt-3',
        hcols=_fcols,
        bcols=_fcols,
        head=[
            cell(content='AL Central'),
            cell(content='W'),
            cell(content='L'),
            cell(content='GB'),
            cell(content='M#')
        ],
        body=[_s47, _s40, _s35, _s38, _s43]),
    table(
        clazz='table-fixed border mt-3',
        hcols=_fcols,
        bcols=_fcols,
        head=[
            cell(content='AL West'),
            cell(content='W'),
            cell(content='L'),
            cell(content='GB'),
            cell(content='M#')
        ],
        body=[_s54, _s42, _s50, _s44, _s58]),
    table(
        clazz='table-fixed border mt-3',
        hcols=_fcols,
        bcols=_fcols,
        head=[
            cell(content='AL Wild Card'),
            cell(content='W'),
            cell(content='L'),
            cell(content='GB'),
            cell(content='M#')
        ],
        body=[_w48, _w40, _w42, _w35]),
    table(
        clazz='table-fixed border mt-3',
        hcols=_fcols,
        bcols=_fcols,
        head=[
            cell(content='NL East'),
            cell(content='W'),
            cell(content='L'),
            cell(content='GB'),
            cell(content='M#')
        ],
        body=[_s49, _s41, _s32, _s51, _s60]),
    table(
        clazz='table-fixed border mt-3',
        hcols=_fcols,
        bcols=_fcols,
        head=[
            cell(content='NL Central'),
            cell(content='W'),
            cell(content='L'),
            cell(content='GB'),
            cell(content='M#')
        ],
        body=[_s37, _s56, _s46, _s36, _s52]),
    table(
        clazz='table-fixed border mt-3',
        hcols=_fcols,
        bcols=_fcols,
        head=[
            cell(content='NL West'),
            cell(content='W'),
            cell(content='L'),
            cell(content='GB'),
            cell(content='M#')
        ],
        body=[_s53, _s45, _s39, _s31, _s55]),
    table(
        clazz='table-fixed border mt-3',
        hcols=_fcols,
        bcols=_fcols,
        head=[
            cell(content='NL Wild Card'),
            cell(content='W'),
            cell(content='L'),
            cell(content='GB'),
            cell(content='M#')
        ],
        body=[_w45, _w56, _w39, _w41])
]

subtitle = ''

tmpl = 'statsplus.html'

context = {
    'title': 'statsplus',
    'breadcrumbs': _breadcrumbs,
    'live': _live,
    'scores': _scores,
    'injuries': _injuries,
    'highlights': _highlights,
    'forecast': _forecast
}
