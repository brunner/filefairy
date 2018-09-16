#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/plugin/gameday', '', _path))
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

_inning = [
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

subtitle = 'Diamondbacks at Dodgers, 10/09/2022'

tmpl = 'game.html'

context = {'title': 'game', 'breadcrumbs': _breadcrumbs, 'inning': _inning}
