#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugins/statsplus/samples', '', _path)
sys.path.append(_root)
from utils.team.team_util import alogo, ilogo  # noqa

subtitle = ''

tmpl = 'statsplus.html'

_l31 = ilogo('31', '4-3')
_l32 = ilogo('32', '5-1')
_l33 = ilogo('33', '0-6')
_l34 = ilogo('34', '4-3')
_l35 = ilogo('35', '3-3')
_l36 = ilogo('36', '3-4')
_l37 = ilogo('37', '3-3')
_l38 = ilogo('38', '1-4')
_l39 = ilogo('39', '2-3')
_l40 = ilogo('40', '4-3')
_l41 = ilogo('41', '2-5')
_l42 = ilogo('42', '5-2')
_l43 = ilogo('43', '4-3')
_l44 = ilogo('44', '3-3')
_l45 = ilogo('45', '4-2')
_l46 = ilogo('46', '2-4')
_l47 = ilogo('47', '4-3')
_l48 = ilogo('48', '4-2')
_l49 = ilogo('49', '5-1')
_l50 = ilogo('50', '4-3')
_l51 = ilogo('51', '5-2')
_l52 = ilogo('52', '1-5')
_l53 = ilogo('53', '4-2')
_l54 = ilogo('54', '2-5')
_l55 = ilogo('55', '2-5')
_l56 = ilogo('56', '6-0')
_l57 = ilogo('57', '4-3')
_l58 = ilogo('58', '3-3')
_l59 = ilogo('59', '2-4')
_l60 = ilogo('60', '1-6')

_s31 = [alogo('31', 'Arizona', 'left'), '76', '86', '28', '']
_s32 = [alogo('32', 'Atlanta', 'left'), '77', '85', '18', '']
_s33 = [alogo('33', 'Baltimore', 'left'), '70', '92', '29', '']
_s34 = [alogo('34', 'Boston', 'left'), '99', '63', '-', 'X']
_s35 = [alogo('35', 'Chicago', 'left'), '82', '80', '6', '']
_s36 = [alogo('36', 'Chicago', 'left'), '71', '91', '40', '']
_s37 = [alogo('37', 'Cincinnati', 'left'), '111', '51', '-', 'X']
_s38 = [alogo('38', 'Cleveland', 'left'), '76', '86', '12', '']
_s39 = [alogo('39', 'Colorado', 'left'), '88', '74', '16', '']
_s40 = [alogo('40', 'Detroit', 'left'), '86', '76', '2', '']
_s41 = [alogo('41', 'Miami', 'left'), '84', '78', '11', '']
_s42 = [alogo('42', 'Houston', 'left'), '85', '77', '13', '']
_s43 = [alogo('43', 'Kansas City', 'left'), '76', '86', '12', '']
_s44 = [alogo('44', 'Los Angeles', 'left'), '70', '92', '28', '']
_s45 = [alogo('45', 'Los Angeles', 'left'), '97', '65', '7', '']
_s46 = [alogo('46', 'Milwaukee', 'left'), '77', '85', '34', '']
_s47 = [alogo('47', 'Minnesota', 'left'), '88', '74', '-', 'X']
_s48 = [alogo('48', 'New York', 'left'), '88', '74', '11', '']
_s49 = [alogo('49', 'New York', 'left'), '95', '67', '-', 'X']
_s50 = [alogo('50', 'Oakland', 'left'), '75', '87', '23', '']
_s51 = [alogo('51', 'Philadelphia', 'left'), '75', '87', '20', '']
_s52 = [alogo('52', 'Pittsburgh', 'left'), '53', '109', '58', '']
_s53 = [alogo('53', 'San Diego', 'left'), '104', '58', '-', 'X']
_s54 = [alogo('54', 'Seattle', 'left'), '98', '64', '-', 'X']
_s55 = [alogo('55', 'San Francisco', 'left'), '62', '100', '42', '']
_s56 = [alogo('56', 'St. Louis', 'left'), '89', '73', '22', '']
_s57 = [alogo('57', 'Tampa Bay', 'left'), '65', '97', '34', '']
_s58 = [alogo('58', 'Texas', 'left'), '67', '95', '31', '']
_s59 = [alogo('59', 'Toronto', 'left'), '73', '89', '26', '']
_s60 = [alogo('60', 'Washington', 'left'), '73', '89', '22', '']

_w35 = [alogo('35', 'Chicago', 'left'), '82', '80', '4', '']
_w39 = [alogo('39', 'Colorado', 'left'), '88', '74', '1', '']
_w40 = [alogo('40', 'Detroit', 'left'), '86', '76', '-', 'X']
_w41 = [alogo('41', 'Miami', 'left'), '84', '78', '5', '']
_w42 = [alogo('42', 'Houston', 'left'), '85', '77', '1', '']
_w45 = [alogo('45', 'Los Angeles', 'left'), '97', '65', '-', 'X']
_w48 = [alogo('48', 'New York', 'left'), '88', '74', '+2', 'X']
_w56 = [alogo('56', 'St. Louis', 'left'), '89', '73', '-', 'X']

LIVE_BCOL = ' class="td-sm position-relative text-center w-20"'
FORE_COLS = [
    ' class="position-relative text-truncate"', ' class="text-right w-55p"',
    ' class="text-right w-55p"', ' class="text-right w-55p"',
    ' class="text-right w-55p"'
]

context = {
    'title':
    'statsplus',
    'breadcrumbs': [{
        'href': '/fairylab/',
        'name': 'Home'
    }, {
        'href': '',
        'name': 'Statsplus'
    }],
    'live': [{
        'clazz': 'table-fixed border border-bottom-0 mt-3',
        'hcols': [' class="text-center"'],
        'bcols': [],
        'head': ['American League'],
        'body': []
    }, {
        'clazz':
        'table-fixed border',
        'hcols': [],
        'bcols': [LIVE_BCOL] * 5,
        'head': [],
        'body': [[_l48, _l34, _l57, _l59,
                  _l33], [_l40, _l43, _l47, _l35, _l38],
                 [_l42, _l50, _l44, _l58, _l54]]
    }, {
        'clazz': 'table-fixed border border-bottom-0 mt-3',
        'hcols': [' class="text-center"'],
        'bcols': [],
        'head': ['National League'],
        'body': []
    }, {
        'clazz':
        'table-fixed border',
        'hcols': [],
        'bcols': [LIVE_BCOL] * 5,
        'head': [],
        'body': [[_l32, _l49, _l51, _l41,
                  _l60], [_l56, _l37, _l36, _l46, _l52],
                 [_l45, _l53, _l31, _l39, _l55]]
    }],
    'scores': [{
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Sunday, October 9th, 2022'],
        'body': [[
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2998.html">Arizona Diamondbacks 4, Los Angeles Dodgers 2</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_3003.html">Atlanta Braves 2, Los Angeles Angels 1</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2996.html">Cincinnati Reds 7, Milwaukee Brewers 2</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_3002.html">Detroit Tigers 11, Chicago White Sox 4</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2993.html">Houston Astros 7, Seattle Mariners 2</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2991.html">Kansas City Royals 8, Cleveland Indians 2</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_14721.html">Miami Marlins 6, Chicago Cubs 2</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_3001.html">New York Mets 1, San Francisco Giants 0</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_3000.html">New York Yankees 5, Baltimore Orioles 3</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2992.html">Philadelphia Phillies 3, Washington Nationals 1</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2999.html">San Diego Padres 8, Colorado Rockies 2</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2990.html">St. Louis Cardinals 5, Pittsburgh Pirates 4</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2997.html">Tampa Bay Rays 12, Boston Red Sox 9</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2994.html">Texas Rangers 5, Oakland Athletics 3</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2995.html">Toronto Blue Jays 8, Minnesota Twins 2</a>'
        ]]
    }, {
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Saturday, October 8th, 2022'],
        'body': [[
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2979.html">Atlanta Braves 10, Los Angeles Angels 5</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2984.html">Boston Red Sox 10, Tampa Bay Rays 5</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2975.html">Chicago Cubs 10, Miami Marlins 2</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2977.html">Chicago White Sox 5, Detroit Tigers 2</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2983.html">Cincinnati Reds 8, Milwaukee Brewers 0</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2989.html">Cleveland Indians 3, Kansas City Royals 2</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2976.html">Houston Astors 6, Seattle Mariners 3</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2978.html">Los Angeles Dodgers 5, Arizona Diamondbacks 1</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2981.html">Minnesota Twins 10, Toronto Blue Jays 7</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2987.html">New York Yankees 5, Baltimore Orioles 4</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2982.html">Philadelphia Phillies 3, Washington Nationals 2</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2986.html">San Diego Padres 6, Colorado Rockies 5</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2985.html">San Francisco Giants 5, New York Mets 4</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2988.html">St. Louis Cardinals 4, Pittsburgh Pirates 1</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2980.html">Texas Rangers 9, Oakland Athletics 1</a>'
        ]]
    }],
    'injuries': [{
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Sunday, October 9th, 2022'],
        'body': [[
            'RF <a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/players/player_36649.html">Elier Hernandez</a> was injured while running the bases (Cleveland Indians @ Kansas City Royals)'
        ], [
            'RF <a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/players/player_34118.html">Gregory Polanco</a> was injured on a defensive play (Milwaukee Brewers @ Cincinnati Reds)'
        ], [
            'SS <a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/players/player_30016.html">Austin Bodrato</a> was injured while running the bases (Milwaukee Brewers @ Cincinnati Reds)'
        ]]
    }, {
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Saturday, October 8th, 2022'],
        'body': [[
            '3B <a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/players/player_33777.html">Kaleb Cowart</a> was injured in a collision at a base (Cleveland Indians @ Kansas City Royals)'
        ], [
            'LF <a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/players/player_29996.html">Keon Broxton</a> was injured while throwing the ball (Houston Astros @ Seattle Mariners)'
        ], [
            'LF <a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/players/player_26747.html">Desmond Lindsay</a> was injured on a defensive play (New York Yankees @ Baltimore Orioles)'
        ]]
    }],
    'highlights': [{
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Saturday, October 8th, 2022'],
        'body': [[
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/players/player_38868.html">Connor Harrell</a> ties the BOS regular season game record for runs with 4 (Boston Red Sox @ Tampa Bay Rays)'
        ]]
    }],
    'forecast': [{
        'clazz': 'table-fixed border mt-3',
        'hcols': FORE_COLS,
        'bcols': FORE_COLS,
        'head': ['AL East', 'W', 'L', 'GB', 'M#'],
        'body': [_s34, _s48, _s59, _s33, _s57]
    }, {
        'clazz': 'table-fixed border mt-3',
        'hcols': FORE_COLS,
        'bcols': FORE_COLS,
        'head': ['AL Central', 'W', 'L', 'GB', 'M#'],
        'body': [_s47, _s40, _s35, _s38, _s43]
    }, {
        'clazz': 'table-fixed border mt-3',
        'hcols': FORE_COLS,
        'bcols': FORE_COLS,
        'head': ['AL West', 'W', 'L', 'GB', 'M#'],
        'body': [_s54, _s42, _s50, _s44, _s58]
    }, {
        'clazz': 'table-fixed border mt-3',
        'hcols': FORE_COLS,
        'bcols': FORE_COLS,
        'head': ['AL Wild Card', 'W', 'L', 'GB', 'M#'],
        'body': [_w48, _w40, _w42, _w35]
    }, {
        'clazz': 'table-fixed border mt-3',
        'hcols': FORE_COLS,
        'bcols': FORE_COLS,
        'head': ['NL East', 'W', 'L', 'GB', 'M#'],
        'body': [_s49, _s41, _s32, _s51, _s60]
    }, {
        'clazz': 'table-fixed border mt-3',
        'hcols': FORE_COLS,
        'bcols': FORE_COLS,
        'head': ['NL Central', 'W', 'L', 'GB', 'M#'],
        'body': [_s37, _s56, _s46, _s36, _s52]
    }, {
        'clazz': 'table-fixed border mt-3',
        'hcols': FORE_COLS,
        'bcols': FORE_COLS,
        'head': ['NL West', 'W', 'L', 'GB', 'M#'],
        'body': [_s53, _s45, _s39, _s31, _s55]
    }, {
        'clazz': 'table-fixed border mt-3',
        'hcols': FORE_COLS,
        'bcols': FORE_COLS,
        'head': ['NL Wild Card', 'W', 'L', 'GB', 'M#'],
        'body': [_w45, _w56, _w39, _w41]
    }]
}