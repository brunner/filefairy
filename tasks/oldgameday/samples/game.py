#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/tasks/oldgameday/samples', '', _path))
from common.elements.elements import anchor  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import span  # noqa
from common.elements.elements import table  # noqa

_log = [
    table(
        clazz='border mt-3',
        bcols=[col(clazz='w-50'), col(clazz='w-50')],
        hcols=[col(colspan='2')],
        fcols=[col(colspan='2')],
        head=[[
            cell(content='Arizona Diamondbacks batting - Pitching for Los '
                 'Angeles Dodgers : LHP 101')
        ]],
        body=[[cell(content='Batting: SHB 102'),
               cell(content='0-0: Ball')],
              [cell(), cell(content='103 to second')]],
        foot=[[cell(content='0 run(s), 0 hit(s), 0 error(s), 0 left on base')]
              ])
]

_schedule = [
    table(
        clazz='table-fixed border border-bottom-0 mt-3',
        head=[[cell(content='Arizona Diamondbacks')]]),
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
                    content=anchor('/oldgameday/1000/',
                                   '10/10/2022 @ Los Angeles Dodgers'))
            ],
            [
                cell(
                    content=anchor('/oldgameday/2000/',
                                   '10/11/2022 @ Los Angeles Dodgers'))
            ],
        ]),
    table(
        clazz='table-fixed border border-bottom-0 mt-3',
        head=[[cell(content='Los Angeles Dodgers')]]),
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
                    content=anchor('/oldgameday/1000/',
                                   '10/10/2022 v Arizona Diamondbacks'))
            ],
            [
                cell(
                    content=anchor('/oldgameday/2000/',
                                   '10/11/2022 v Arizona Diamondbacks'))
            ],
        ]),
]

subtitle = 'Diamondbacks at Dodgers, 10/09/2022'

tmpl = 'game.html'

context = {
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
