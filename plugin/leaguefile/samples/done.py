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
    'href': '/',
    'name': 'Fairylab'
}, {
    'href': '',
    'name': 'Leaguefile'
}]

_cols = [
    '', ' class="text-center"', ' class="text-center"', ' class="text-right"'
]
_completed = table(
    clazz='border mt-3',
    hcols=_cols,
    bcols=_cols,
    head=['Date', 'Upload', 'Download', 'Size'],
    body=[['Mar 10', '4h 56m', '7m',
           '359,969,530'], ['Mar 8', '10h 11m', '11m', '358,347,534'],
          ['Mar 6', '9h 34m', '6m', '356,922,996']])

subtitle = ''

tmpl = 'leaguefile.html'

context = {
    'title': 'leaguefile',
    'breadcrumbs': _breadcrumbs,
    'completed': _completed
}
