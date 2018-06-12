#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugin/leaguefile/samples', '', _path)
sys.path.append(_root)
from util.component.component import card  # noqa
from util.component.component import table  # noqa

_breadcrumbs = [{
    'href': '/fairylab/',
    'name': 'Home'
}, {
    'href': '',
    'name': 'Leaguefile'
}]

_ucols = [' class="w-55p"', '']
_table = table(
    clazz='table-sm',
    hcols=_ucols,
    bcols=_ucols,
    body=[['Time: ', '56m'], ['Size: ', '59,969,530']])
_upload = card(title='Mar 10', table=_table, ts='30s ago', success='ongoing')

_ccols = [
    '', ' class="text-center"', ' class="text-center"', ' class="text-right"'
]
_completed = table(
    clazz='border mt-3',
    hcols=_ccols,
    bcols=_ccols,
    head=['Date', 'Upload', 'Download', 'Size'],
    body=[['Mar 8', '10h 11m', '11m', '358,347,534'],
          ['Mar 6', '9h 34m', '6m', '356,922,996']])

subtitle = ''

tmpl = 'leaguefile.html'

context = {
    'title': 'leaguefile',
    'breadcrumbs': _breadcrumbs,
    'upload': _upload,
    'completed': _completed
}
