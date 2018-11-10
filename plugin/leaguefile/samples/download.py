#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugin/leaguefile/samples', '', _path)
sys.path.append(_root)
from util.component.component import card  # noqa
from util.component.component import cell  # noqa
from util.component.component import col  # noqa
from util.component.component import table  # noqa

_breadcrumbs = [{
    'href': '/',
    'name': 'Fairylab'
}, {
    'href': '',
    'name': 'Leaguefile'
}]

_cols = [col(clazz='w-55p'), col()]
_table = table(
    clazz='table-sm',
    hcols=_cols,
    bcols=_cols,
    body=[[cell(content='Time: '),
           cell(content='4h 56m')],
          [cell(content='Size: '),
           cell(content='359,969,530')]])
_upload = card(
    title='Mar 10',
    table=_table,
    ts='06:02:30 EDT (1985-10-26)',
    success='completed')

_table = table(
    clazz='table-sm',
    hcols=_cols,
    bcols=_cols,
    body=[[cell(content='Time: '), cell(content='3m')],
          [cell(content='Size: '),
           cell(content='59,969,530')]])
_download = card(
    title='Mar 10',
    table=_table,
    ts='06:02:30 EDT (1985-10-26)',
    success='ongoing')

_ccols = [
    col(),
    col(clazz='text-center'),
    col(clazz='text-center'),
    col(clazz='text-right')
]
_completed = table(
    clazz='border mt-3',
    hcols=_ccols,
    bcols=_ccols,
    head=[
        cell(content='Date'),
        cell(content='Upload'),
        cell(content='Download'),
        cell(content='Size')
    ],
    body=[[
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
    'upload': _upload,
    'download': _download,
    'completed': _completed
}
