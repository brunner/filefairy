#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/plugin/gameday', '', _path))
from util.component.component import anchor  # noqa
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

_raw = [
    table(
        clazz='border mt-3',
        bcols=[' class="w-50"', ' class="w-50"'],
        hcols=[' colspan="2"'],
        fcols=[' colspan="2"'],
        head=[
            'Arizona Diamondbacks batting - Pitching for Los Angeles ' +
            'Dodgers : LHP 101'
        ],
        body=[['Batting: SHB 102', '0-0: Ball'], ['', '103 to second']],
        foot=['0 run(s), 0 hit(s), 0 error(s), 0 left on base'])
]

_schedule = [
    table(
        clazz='table-fixed border border-bottom-0',
        hcols=[' class="text-center"'],
        head=['Arizona Diamondbacks']),
    table(
        clazz='table-fixed border border-bottom-0',
        bcols=[' class="text-center"'],
        body=[
            [
                replace('Previous game', 'Previous game not found') + ' - ' +
                replace('Next game', 'Next game not found')
            ],
        ]),
    table(
        clazz='table-fixed border show-toggler',
        bcols=[' class="text-center"'],
        body=[
            [show('schedule-t31', 'Toggle full schedule')],
        ]),
    table(
        clazz='table-fixed border collapse',
        id_='schedule-t31',
        bcols=[' class="text-center"'],
        body=[
            [span(['text-secondary'], '10/09/2022 @ Los Angeles Dodgers')],
            [anchor('/gameday/1000/', '10/10/2022 @ Los Angeles Dodgers')],
            [anchor('/gameday/2000/', '10/11/2022 @ Los Angeles Dodgers')],
        ]),
    table(
        clazz='table-fixed border border-bottom-0 mt-3',
        hcols=[' class="text-center"'],
        head=['Los Angeles Dodgers']),
    table(
        clazz='table-fixed border border-bottom-0',
        bcols=[' class="text-center"'],
        body=[
            [
                replace('Previous game', 'Previous game not found') + ' - ' +
                replace('Next game', 'Next game not found')
            ],
        ]),
    table(
        clazz='table-fixed border show-toggler',
        bcols=[' class="text-center"'],
        body=[
            [show('schedule-t45', 'Toggle full schedule')],
        ]),
    table(
        clazz='table-fixed border collapse',
        id_='schedule-t45',
        bcols=[' class="text-center"'],
        body=[
            [span(['text-secondary'], '10/09/2022 v Arizona Diamondbacks')],
            [anchor('/gameday/1000/', '10/10/2022 v Arizona Diamondbacks')],
            [anchor('/gameday/2000/', '10/11/2022 v Arizona Diamondbacks')],
        ]),
]

subtitle = 'Diamondbacks at Dodgers, 10/09/2022'

tmpl = 'game.html'

context = {
    'title': 'game',
    'breadcrumbs': _breadcrumbs,
    'raw': _raw,
    'schedule': _schedule
}
