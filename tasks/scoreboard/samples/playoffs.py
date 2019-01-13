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

_body = [
    [
        cell(content=logo_absolute('54', 'Seattle', 'left')),
        cell(content='4'),
        cell(content='1'),
        cell(content=logo_absolute('34', 'Boston', 'right'))
    ],
    [
        cell(content=logo_absolute('45', 'Los Angeles', 'left')),
        cell(content='4'),
        cell(content='2'),
        cell(content=logo_absolute('53', 'San Diego', 'right'))
    ],
]

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
            head=[cell(content='Postseason')]),
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
            head=[cell(content='Wednesday, October 26th, 2022')],
            body=[
                [
                    cell(
                        content=('<a href="https://orangeandblueleaguebaseball'
                                 '.com/StatsLab/reports/news/html/box_scores/g'
                                 'ame_box_25051.html">Los Angeles Dodgers 8, S'
                                 'an Diego Padres 3</a>'))
                ],
            ]),
        table(
            clazz='border mt-3',
            head=[cell(content='Tuesday, October 25th, 2022')],
            body=[
                [
                    cell(
                        content=('<a href="https://orangeandblueleaguebaseball'
                                 '.com/StatsLab/reports/news/html/box_scores/g'
                                 'ame_box_25043.html">Seattle Mariners 6, Bost'
                                 'on Red Sox 3</a>'))
                ],
            ]),
        table(
            clazz='border mt-3',
            head=[cell(content='Monday, October 24th, 2022')],
            body=[
                [
                    cell(
                        content=('<a href="https://orangeandblueleaguebaseball'
                                 '.com/StatsLab/reports/news/html/box_scores/g'
                                 'ame_box_25050.html">San Diego Padres 7, Los '
                                 'Angeles Dodgers 2</a>'))
                ],
                [
                    cell(
                        content=('<a href="https://orangeandblueleaguebaseball'
                                 '.com/StatsLab/reports/news/html/box_scores/g'
                                 'ame_box_25042.html">Seattle Mariners 1, Bost'
                                 'on Red Sox 0</a>'))
                ],
            ]),
        table(
            clazz='border mt-3',
            head=[cell(content='Sunday, October 23rd, 2022')],
            body=[
                [
                    cell(
                        content=('<a href="https://orangeandblueleaguebaseball'
                                 '.com/StatsLab/reports/news/html/box_scores/g'
                                 'ame_box_25034.html">Boston Red Sox 3, Seattl'
                                 'e Mariners 2</a>'))
                ],
                [
                    cell(
                        content=('<a href="https://orangeandblueleaguebaseball'
                                 '.com/StatsLab/reports/news/html/box_scores/g'
                                 'ame_box_25049.html">Los Angeles Dodgers 3, S'
                                 'an Diego Padres 2</a>'))
                ],
            ]),
        table(
            clazz='border mt-3',
            head=[cell(content='Saturday, October 22nd, 2022')],
            body=[
                [
                    cell(
                        content=('<a href="https://orangeandblueleaguebaseball'
                                 '.com/StatsLab/reports/news/html/box_scores/g'
                                 'ame_box_25048.html">Los Angeles Dodgers 4, S'
                                 'an Diego Padres 3</a>'))
                ],
            ]),
        table(
            clazz='border mt-3',
            head=[cell(content='Friday, October 21st, 2022')],
            body=[
                [
                    cell(
                        content=('<a href="https://orangeandblueleaguebaseball'
                                 '.com/StatsLab/reports/news/html/box_scores/g'
                                 'ame_box_25029.html">Seattle Mariners 3, Bost'
                                 'on Red Sox 2</a>'))
                ],
            ]),
        table(
            clazz='border mt-3',
            head=[cell(content='Thursday, October 20th, 2022')],
            body=[
                [
                    cell(
                        content=('<a href="https://orangeandblueleaguebaseball'
                                 '.com/StatsLab/reports/news/html/box_scores/g'
                                 'ame_box_25047.html">Los Angeles Dodgers 13, '
                                 'San Diego Padres 7</a>'))
                ],
                [
                    cell(
                        content=('<a href="https://orangeandblueleaguebaseball'
                                 '.com/StatsLab/reports/news/html/box_scores/g'
                                 'ame_box_25024.html">Seattle Mariners 2, Bost'
                                 'on Red Sox 0</a>'))
                ],
            ]),
        table(
            clazz='border mt-3',
            head=[cell(content='Wednesday, October 19th, 2022')],
            body=[
                [
                    cell(
                        content=('<a href="https://orangeandblueleaguebaseball'
                                 '.com/StatsLab/reports/news/html/box_scores/g'
                                 'ame_box_25046.html">San Diego Padres 2, Los '
                                 'Angeles Dodgers 0</a>'))
                ],
            ])
    ],
    'injuries': [
        table(
            clazz='border mt-3',
            head=[cell(content='Monday, October 24th, 2022')],
            body=[
                [
                    cell(
                        content=('C <a href="https://orangeandblueleaguebaseba'
                                 'll.com/StatsLab/reports/news/html/players/pl'
                                 'ayer_48236.html">Wilson Garcia</a> was injur'
                                 'ed being hit by a pitch (San Diego Padres @ '
                                 'Los Angeles Dodgers)'))
                ],
            ]),
        table(
            clazz='border mt-3',
            head=[cell(content='Thursday, October 20th, 2022')],
            body=[
                [
                    cell(
                        content=('3B <a href="https://orangeandblueleaguebaseb'
                                 'all.com/StatsLab/reports/news/html/players/p'
                                 'layer_22458.html">Alex Bregman</a> was injur'
                                 'ed while running the bases (Los Angeles Dodg'
                                 'ers @ San Diego Padres)'))
                ],
            ]),
        table(
            clazz='border mt-3',
            head=[cell(content='Wednesday, October 19th, 2022')],
            body=[
                [
                    cell(
                        content=('SP <a href="https://orangeandblueleaguebaseb'
                                 'all.com/StatsLab/reports/news/html/players/p'
                                 'layer_37102.html">Jairo Labourt</a> was inju'
                                 'red while pitching (Seattle Mariners @ Bosto'
                                 'n Red Sox)'))
                ],
            ])
    ],
    'highlights': [
        table(
            clazz='border mt-3',
            head=[cell(content='Saturday, October 8th, 2022')],
            body=[
                [
                    cell(
                        content=('<a href="https://orangeandblueleaguebaseball'
                                 '.com/StatsLab/reports/news/html/players/play'
                                 'er_30744.html">Brad Debo</a> sets the NL pla'
                                 'yoff game record for doubles with 3 (San Die'
                                 'go Padres @ Los Angeles Dodgers)'))
                ],
            ])
    ],
    'forecast': []
}