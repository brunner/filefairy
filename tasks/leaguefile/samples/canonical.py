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
    head=[cell(content='Date')],
    body=[
        [cell(content='19:15:00 PDT (2018-05-08)')],
        [cell(content='22:07:00 PDT (2018-05-06)')],
    ])

subtitle = ''

tmpl = 'leaguefile.html'

context = {
    'title': 'leaguefile',
    'breadcrumbs': _breadcrumbs,
    'completed': _completed
}
