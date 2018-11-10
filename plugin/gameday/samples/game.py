#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/plugin/gameday', '', _path))
from util.component.component import anchor  # noqa
from util.component.component import cell  # noqa
from util.component.component import col  # noqa
from util.component.component import replace  # noqa
from util.component.component import show  # noqa
from util.component.component import span  # noqa
from util.component.component import table  # noqa

_breadcrumbs = [{
    'href': '/',
    'name': 'Fairylab'
}, {
    'href': '/gameday/',
    'name': 'Gameday'
}, {
    'href': '',
    'name': 'Diamondbacks at Dodgers, 10/09/2022'
}]

_replace = cell(
    content=replace('Previous game', 'Previous game not found') + ' - ' +
    replace('Next game', 'Next game not found'))
_log = [
    table(
        clazz='border mt-3',
        bcols=[col(clazz='w-50'), col(clazz='w-50')],
        hcols=[col(colspan='2')],
        fcols=[col(colspan='2')],
        head=[
            cell(content='Arizona Diamondbacks batting - Pitching for Los '
                 'Angeles Dodgers : LHP 101')
        ],
        body=[[cell(content='Batting: SHB 102'),
               cell(content='0-0: Ball')],
              [cell(), cell(content='103 to second')]],
        foot=[cell(content='0 run(s), 0 hit(s), 0 error(s), 0 left on base')])
]

_schedule = [
    table(
        clazz='table-fixed border border-bottom-0 mt-3',
        head=[cell(content='Arizona Diamondbacks')]),
    table(clazz='table-fixed border border-bottom-0', body=[[_replace]]),
    table(
        clazz='table-fixed border show-toggler',
        body=[
            [cell(content=show('schedule-t31', 'Toggle full schedule'))],
        ]),
    table(
        clazz='table-fixed border collapse',
        id_='schedule-t31',
        body=[
            [
                cell(
                    content=span(['text-secondary'],
                                 '10/09/2022 @ Los Angeles Dodgers'))
            ],
            [
                cell(
                    content=anchor('/gameday/1000/',
                                   '10/10/2022 @ Los Angeles Dodgers'))
            ],
            [
                cell(
                    content=anchor('/gameday/2000/',
                                   '10/11/2022 @ Los Angeles Dodgers'))
            ],
        ]),
    table(
        clazz='table-fixed border border-bottom-0 mt-3',
        head=[cell(content='Los Angeles Dodgers')]),
    table(clazz='table-fixed border border-bottom-0', body=[[_replace]]),
    table(
        clazz='table-fixed border show-toggler',
        body=[
            [cell(content=show('schedule-t45', 'Toggle full schedule'))],
        ]),
    table(
        clazz='table-fixed border collapse',
        id_='schedule-t45',
        body=[
            [
                cell(
                    content=span(['text-secondary'],
                                 '10/09/2022 v Arizona Diamondbacks'))
            ],
            [
                cell(
                    content=anchor('/gameday/1000/',
                                   '10/10/2022 v Arizona Diamondbacks'))
            ],
            [
                cell(
                    content=anchor('/gameday/2000/',
                                   '10/11/2022 v Arizona Diamondbacks'))
            ],
        ]),
]

subtitle = 'Diamondbacks at Dodgers, 10/09/2022'

tmpl = 'game.html'

context = {
    'title': 'game',
    'breadcrumbs': _breadcrumbs,
    'tabs': {
        'tabs': [{
            'name': 'log',
            'title': 'Game Log',
            'tables': _log
        }, {
            'name': 'schedule',
            'title': 'Schedule',
            'tables': _schedule
        }]
    }
}
