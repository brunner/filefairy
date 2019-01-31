#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/tasks/news/samples', '', _path))

from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import table  # noqa

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

subtitle = ''

tmpl = 'news.html'

context = {
    'injuries': _injuries,
    'news': _news,
    'transactions': _transactions
}
