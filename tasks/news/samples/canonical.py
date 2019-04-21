#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/tasks/news/samples', '', _path))

from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import row  # noqa
from common.elements.elements import table  # noqa
from common.teams.teams import icon_absolute  # noqa

_injuries = [
    table(
        clazz='border mb-3',
        hcols=[col(clazz='font-weight-bold text-dark')],
        bcols=[col(clazz='position-relative')],
        head=[row(cells=[cell(content='Monday, July 4th, 2022')])],
        body=[
            row(cells=[
                cell(
                    content=icon_absolute('T52', (
                        'SP <a href="https://statsplus.net/oblootp/player/3515'
                        '5">John Barbato</a> diagnosed with a sore forearm, is'
                        ' day-to-day for 5 days.')))
            ]),
        ]),
    table(
        clazz='border mb-3',
        hcols=[col(clazz='font-weight-bold text-dark')],
        bcols=[col(clazz='position-relative')],
        head=[row(cells=[cell(content='Sunday, July 3th, 2022')])],
        body=[
            row(cells=[
                cell(
                    content=icon_absolute('T44', (
                        'SP <a href="https://statsplus.net/oblootp/player/3731'
                        '8">Ty Blach</a> was injured while pitching. Diagnosis'
                        ': back stiffness. This is a day-to-day injury expecte'
                        'd to last 5 days.')))
            ]),
            row(cells=[
                cell(
                    content=icon_absolute('T60', (
                        'RP <a href="https://statsplus.net/oblootp/player/3262'
                        '4">Hunter Strickland</a> was injured while pitching. '
                        'Diagnosis: back spasms. This is a day-to-day injury e'
                        'xpected to last 5 days.')))
            ]),
            row(cells=[
                cell(
                    content=icon_absolute('T57', (
                        'RP <a href="https://statsplus.net/oblootp/player/1958'
                        '">Javier Medina</a> was injured while pitching. The d'
                        'iagnosis is not yet known.')))
            ]),
            row(cells=[
                cell(
                    content=icon_absolute('T52', (
                        'SP <a href="https://statsplus.net/oblootp/player/3515'
                        '5">John Barbato</a> was injured while pitching. The d'
                        'iagnosis is not yet known.')))
            ]),
            row(cells=[
                cell(
                    content=icon_absolute('T52', (
                        'CF <a href="https://statsplus.net/oblootp/player/1604'
                        '">Carl Cester</a> was injured on a defensive play. Th'
                        'e diagnosis is not yet known.')))
            ]),
            row(cells=[
                cell(
                    content=icon_absolute('T40', (
                        'RP <a href="https://statsplus.net/oblootp/player/2245'
                        '7">Walker Buehler</a> was injured while pitching. The'
                        ' diagnosis is not yet known.')))
            ]),
        ])
]
_news = [
    table(
        clazz='border mb-3',
        hcols=[col(clazz='font-weight-bold text-dark')],
        bcols=[col(clazz='position-relative')],
        head=[row(cells=[cell(content='Monday, July 4th, 2022')])],
        body=[
            row(cells=[
                cell(
                    content=icon_absolute('T35', (
                        '1B <a href="https://statsplus.net/oblootp/player/3389'
                        '2">Viosergy Rosa</a> wins the MLB AL Player of the We'
                        'ek Award.')))
            ]),
            row(cells=[
                cell(
                    content=icon_absolute('T32', (
                        '1B <a href="https://statsplus.net/oblootp/player/2719'
                        '4">Freddie Freeman</a> wins the MLB NL Player of the '
                        'Week Award.')))
            ]),
        ])
]
_transactions = [
    table(
        clazz='border mb-3',
        hcols=[col(clazz='font-weight-bold text-dark')],
        bcols=[col(clazz='position-relative')],
        head=[row(cells=[cell(content='Monday, July 4th, 2022')])],
        body=[
            row(cells=[
                cell(
                    content=icon_absolute('T53', (
                        'Signed <a href="https://statsplus.net/oblootp/player/'
                        '56862">Antonio Marquis</a> to a minor league contract'
                        ' with a signing bonus of $180,000.')))
            ]),
            row(cells=[
                cell(
                    content=icon_absolute('T30', (
                        'The Detroit Tigers traded 25-year-old minor league le'
                        'ft fielder <a href="https://statsplus.net/oblootp/pla'
                        'yer/28672">Nick Plummer</a> to the Milwaukee Brewers,'
                        ' getting 33-year-old closer <a href="https://statsplu'
                        's.net/oblootp/player/36352">Phil Klein</a> in return.'
                    )))
            ]),
            row(cells=[
                cell(
                    content=icon_absolute('T30', (
                        'The Detroit Tigers traded 25-year-old minor league le'
                        'ft fielder <a href="https://statsplus.net/oblootp/pla'
                        'yer/25202">Wesley Rodriguez</a> and 31-year-old left '
                        'fielder <a href="https://statsplus.net/oblootp/player'
                        '/33588">Michael A. Taylor</a> to the Chicago Cubs, ge'
                        'tting 30-year-old right fielder <a href="https://stat'
                        'splus.net/oblootp/player/35161">Drew Vettleson</a> in'
                        ' return.')))
            ]),
            row(cells=[
                cell(
                    content=icon_absolute('T30', (
                        'The Detroit Tigers traded 21-year-old minor league sh'
                        'ortstop <a href="https://statsplus.net/oblootp/player'
                        '/32327">Jesus Martinez</a> to the Philadelphia Philli'
                        'es, getting 28-year-old left fielder <a href="https:/'
                        '/statsplus.net/oblootp/player/37237">Mitch Nay</a> in'
                        ' return.')))
            ]),
            row(cells=[
                cell(
                    content=icon_absolute('T30', (
                        'The Minnesota Twins traded 25-year-old first baseman '
                        '<a href="https://statsplus.net/oblootp/player/39581">'
                        'Lewin Diaz</a> to the Chicago Cubs, getting 30-year-o'
                        'ld starting pitcher <a href="https://statsplus.net/ob'
                        'lootp/player/37975">Matt Anderson</a>, 19-year-old mi'
                        'nor league starting pitcher <a href="https://statsplu'
                        's.net/oblootp/player/22921">Juan Monreal</a> and 21-y'
                        'ear-old minor league catcher <a href="https://statspl'
                        'us.net/oblootp/player/55093">Jonathan Salazar</a> in '
                        'return.')))
            ]),
        ])
]

subtitle = ''

tmpl = 'news.html'

context = {'injuries': _injuries, 'news': _news, 'transactions': _transactions}
