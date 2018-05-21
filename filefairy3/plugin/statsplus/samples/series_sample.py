#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugin/statsplus/samples', '', _path)
sys.path.append(_root)
from util.team.team import logo_absolute  # noqa

subtitle = ''

tmpl = 'statsplus.html'

_body = [[
    logo_absolute('54', 'Seattle', 'left'), '4', '2',
    logo_absolute('45', 'Los Angeles', 'right')
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
        'head': ['Friday, November 4th, 2022'],
        'body': [[
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25072.html">Seattle Mariners 13, Los Angeles Dodgers 3</a>'
        ]]
    }, {
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Wednesday, November 2nd, 2022'],
        'body': [[
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25071.html">Seattle Mariners 5, Los Angeles Dodgers 3</a>'
        ]]
    }, {
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Tuesday, November 1st, 2022'],
        'body': [[
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25052.html">Seattle Mariners 3, Los Angeles Dodgers 2</a>'
        ]]
    }, {
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Monday, October 31st, 2022'],
        'body': [[
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25045.html">Los Angeles Dodgers 5, Seattle Mariners 4</a>'
        ]]
    }, {
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Saturday, October 29th, 2022'],
        'body': [[
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25044.html">Seattle Mariners 5, Los Angeles Dodgers 2</a>'
        ]]
    }, {
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Friday, October 28th, 2022'],
        'body': [[
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25041.html">Los Angeles Dodgers 5, Seattle Mariners 3</a>'
        ]]
    }],
    'injuries': [{
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Monday, October 31st, 2022'],
        'body': [[
            'RP <a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/players/player_19570.html">Josh Outman</a> was injured while pitching (Los Angeles Dodgers @ Seattle Mariners)'
        ]]
    }, {
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Friday, October 28th, 2022'],
        'body': [[
            'SP <a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/players/player_33236.html">Mario Ram?rez</a> was injured while pitching (Seattle Mariners @ Los Angeles Dodgers)'
        ]]
    }],
    'highlights': [],
    'forecast': []
}
