#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugin/leaguefile/samples', '', _path)
sys.path.append(_root)
from util.component.component import table  # noqa

_breadcrumbs = [{
    'href': '/fairylab/',
    'name': 'Home'
}, {
    'href': '',
    'name': 'Leaguefile'
}]

_up = table(
    clazz='border mt-3',
    head=['Date', 'Time', 'Size'],
    body=[['Mar 10', '4h 56m',
           '359,969,530'], ['Mar 8', '10h 11m', '358,347,534'],
          ['Mar 6', '9h 34m', '356,922,996']])

subtitle = ''

tmpl = 'leaguefile.html'

context = {'title': 'leaguefile', 'breadcrumbs': _breadcrumbs, 'up': _up}
