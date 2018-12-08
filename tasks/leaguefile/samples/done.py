#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sample data for leaguefile.py golden test."""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/tasks/leaguefile/samples', '', _path))

from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import table  # noqa

COLS = [col(clazz=c) for c in ('', 'text-center', 'text-center', 'text-right')]
HEAD = [cell(content=c) for c in ('Date', 'Upload', 'Download', 'Size')]

_breadcrumbs = [{
    'href': '/',
    'name': 'Fairylab'
}, {
    'href': '',
    'name': 'Leaguefile'
}]

_completed = table(
    clazz='border mt-3',
    hcols=COLS,
    bcols=COLS,
    head=HEAD,
    body=[
        [
            cell(content='Mar 10'),
            cell(content='4h 56m'),
            cell(content='7m'),
            cell(content='359,969,530')
        ],
        [
            cell(content='Mar 8'),
            cell(content='10h 11m'),
            cell(content='11m'),
            cell(content='358,347,534')
        ],
        [
            cell(content='Mar 6'),
            cell(content='9h 34m'),
            cell(content='6m'),
            cell(content='356,922,996')
        ],
    ])

subtitle = ''

tmpl = 'leaguefile.html'

context = {
    'title': 'leaguefile',
    'breadcrumbs': _breadcrumbs,
    'completed': _completed
}
