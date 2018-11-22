#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugin/leaguefile/samples', '', _path)
sys.path.append(_root)
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import table  # noqa

_breadcrumbs = [{
    'href': '/',
    'name': 'Fairylab'
}, {
    'href': '',
    'name': 'Leaguefile'
}]

_cols = [
    col(),
    col(clazz='text-center'),
    col(clazz='text-center'),
    col(clazz='text-right')
]
_completed = table(
    clazz='border mt-3',
    hcols=_cols,
    bcols=_cols,
    head=[
        cell(content='Date'),
        cell(content='Upload'),
        cell(content='Download'),
        cell(content='Size')
    ],
    body=[[
        cell(content='Mar 10'),
        cell(content='4h 56m'),
        cell(content='7m'),
        cell(content='359,969,530')
    ], [
        cell(content='Mar 8'),
        cell(content='10h 11m'),
        cell(content='11m'),
        cell(content='358,347,534')
    ], [
        cell(content='Mar 6'),
        cell(content='9h 34m'),
        cell(content='6m'),
        cell(content='356,922,996')
    ]])

subtitle = ''

tmpl = 'leaguefile.html'

context = {
    'title': 'leaguefile',
    'breadcrumbs': _breadcrumbs,
    'completed': _completed
}
