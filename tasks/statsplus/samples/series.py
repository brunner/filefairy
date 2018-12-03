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

subtitle = ''

tmpl = 'statsplus.html'

_body = [[
    cell(content=logo_absolute('54', 'Seattle', 'left')),
    cell(content='4'),
    cell(content='2'),
    cell(content=logo_absolute('45', 'Los Angeles', 'right'))
]]

context = {
    'title':
    'statsplus',
    'breadcrumbs': [{
        'href': '/',
        'name': 'Fairylab'
    }, {
        'href': '',
        'name': 'Statsplus'
    }],
    'live': [
        table(
            clazz='table-fixed border border-bottom-0 mt-3',
            hcols=[col(clazz='text-center')],
            head=[cell(content='Postseason')],
        ),
        table(
            clazz='table-fixed border',
            bcols=[
                col(clazz='position-relative w-40'),
                col(clazz='text-center w-10'),
                col(clazz='text-center w-10'),
                col(clazz='position-relative text-right w-40')
            ],
            body=_body)
    ],
    'scores': [
        table(
            clazz='border mt-3',
            head=[cell(content='Friday, November 4th, 2022')],
            body=[[
                cell(
                    content=
                    '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25072.html">Seattle Mariners 13, Los Angeles Dodgers 3</a>'
                )
            ]]),
        table(
            clazz='border mt-3',
            head=[cell(content='Wednesday, November 2nd, 2022')],
            body=[[
                cell(
                    content=
                    '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25071.html">Seattle Mariners 5, Los Angeles Dodgers 3</a>'
                )
            ]]),
        table(
            clazz='border mt-3',
            head=[cell(content='Tuesday, November 1st, 2022')],
            body=[[
                cell(
                    content=
                    '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25052.html">Seattle Mariners 3, Los Angeles Dodgers 2</a>'
                )
            ]]),
        table(
            clazz='border mt-3',
            head=[cell(content='Monday, October 31st, 2022')],
            body=[[
                cell(
                    content=
                    '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25045.html">Los Angeles Dodgers 5, Seattle Mariners 4</a>'
                )
            ]]),
        table(
            clazz='border mt-3',
            head=[cell(content='Saturday, October 29th, 2022')],
            body=[[
                cell(
                    content=
                    '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25044.html">Seattle Mariners 5, Los Angeles Dodgers 2</a>'
                )
            ]]),
        table(
            clazz='border mt-3',
            head=[cell(content='Friday, October 28th, 2022')],
            body=[[
                cell(
                    content=
                    '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25041.html">Los Angeles Dodgers 5, Seattle Mariners 3</a>'
                )
            ]])
    ],
    'injuries': [
        table(
            clazz='border mt-3',
            head=[cell(content='Monday, October 31st, 2022')],
            body=[[
                cell(
                    content=
                    'RP <a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/players/player_19570.html">Josh Outman</a> was injured while pitching (Los Angeles Dodgers @ Seattle Mariners)'
                )
            ]]),
        table(
            clazz='border mt-3',
            head=[cell(content='Friday, October 28th, 2022')],
            body=[[
                cell(
                    content=
                    'SP <a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/players/player_33236.html">Mario Ram?rez</a> was injured while pitching (Seattle Mariners @ Los Angeles Dodgers)'
                )
            ]])
    ],
    'highlights': [],
    'forecast': []
}
