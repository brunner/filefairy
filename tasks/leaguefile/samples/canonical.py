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


_breadcrumbs = [{
    'href': '/',
    'name': 'Fairylab'
}, {
    'href': '',
    'name': 'Leaguefile'
}]


_cols = [col(), col(clazz='text-right')]
_completed = table(
    clazz='border mt-3',
    hcols=_cols,
    bcols=_cols,
    head=[cell(content='Date'), cell(content='Size')],
    body=[
        [
            cell(content='Mar 8'),
            cell(content='358,347,534')
        ],
        [
            cell(content='Mar 6'),
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
