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
        head=['t1'],
        body=[['T31 batting - Pitching for T45 : LHP P101'],
              ['Batting: SHB P102'], ['0-0: Ball'], ['P103 to second'],
              ['0 run(s), 0 hit(s), 0 error(s), 0 left on base']])
]

subtitle = 'Diamondbacks at Dodgers, 10/09/2022'

tmpl = 'game.html'

context = {'title': 'game', 'breadcrumbs': _breadcrumbs, 'inning': _inning}
