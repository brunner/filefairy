#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/pluging/statsplus/samples', '', _path)
sys.path.append(_root)
from util.team.team_util import logo_absolute  # noqa

subtitle = ''

tmpl = 'statsplus.html'

_body = [[
    logo_absolute('54', 'Seattle', 'left'), '4', '1',
    logo_absolute('34', 'Boston', 'right')
], [
    logo_absolute('45', 'Los Angeles', 'left'), '4', '2',
    logo_absolute('53', 'San Diego', 'right')
]]

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
        'head': ['Postseason'],
        'body': []
    }, {
        'clazz':
        'table-fixed border',
        'hcols': [],
        'bcols': [
            ' class="position-relative w-40"', ' class="text-center w-10"',
            ' class="text-center w-10"',
            ' class="position-relative text-right w-40"'
        ],
        'head': [],
        'body':
        _body
    }],
    'scores': [{
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Wednesday, October 26th, 2022'],
        'body': [[
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25051.html">Los Angeles Dodgers 8, San Diego Padres 3</a>'
        ]]
    }, {
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Tuesday, October 25th, 2022'],
        'body': [[
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25043.html">Seattle Mariners 6, Boston Red Sox 3</a>'
        ]]
    }, {
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Monday, October 24th, 2022'],
        'body': [[
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25050.html">San Diego Padres 7, Los Angeles Dodgers 2</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25042.html">Seattle Mariners 1, Boston Red Sox 0</a>'
        ]]
    }, {
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Sunday, October 23rd, 2022'],
        'body': [[
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25034.html">Boston Red Sox 3, Seattle Mariners 2</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25049.html">Los Angeles Dodgers 3, San Diego Padres 2</a>'
        ]]
    }, {
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Saturday, October 22nd, 2022'],
        'body': [[
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25048.html">Los Angeles Dodgers 4, San Diego Padres 3</a>'
        ]]
    }, {
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Friday, October 21st, 2022'],
        'body': [[
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25029.html">Seattle Mariners 3, Boston Red Sox 2</a>'
        ]]
    }, {
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Thursday, October 20th, 2022'],
        'body': [[
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25047.html">Los Angeles Dodgers 13, San Diego Padres 7</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25024.html">Seattle Mariners 2, Boston Red Sox 0</a>'
        ]]
    }, {
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Wednesday, October 19th, 2022'],
        'body': [[
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25046.html">San Diego Padres 2, Los Angeles Dodgers 0</a>'
        ]]
    }],
    'injuries': [{
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Monday, October 24th, 2022'],
        'body': [[
            'C <a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/players/player_48236.html">Wilson Garcia</a> was injured being hit by a pitch (San Diego Padres @ Los Angeles Dodgers)'
        ]]
    }, {
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Thursday, October 20th, 2022'],
        'body': [[
            '3B <a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/players/player_22458.html">Alex Bregman</a> was injured while running the bases (Los Angeles Dodgers @ San Diego Padres)'
        ]]
    }, {
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Wednesday, October 19th, 2022'],
        'body': [[
            'SP <a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/players/player_37102.html">Jairo Labourt</a> was injured while pitching (Seattle Mariners @ Boston Red Sox)'
        ]]
    }],
    'highlights': [{
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Saturday, October 8th, 2022'],
        'body': [[
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/players/player_30744.html">Brad Debo</a> sets the NL playoff game record for doubles with 3 (San Diego Padres @ Los Angeles Dodgers)'
        ]]
    }],
    'forecast': []
}
