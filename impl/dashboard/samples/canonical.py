#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sample data for dashboard.py golden test."""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/impl/dashboard/samples', '', _path))

from common.elements.elements import anchor  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import dialog  # noqa
from common.elements.elements import pre  # noqa
from common.elements.elements import row  # noqa
from common.elements.elements import table  # noqa

LINK = 'https://github.com/brunner/filefairy/blob/master/'

_error_title = 'filefairy.py#L127'
_error_link = LINK + 'impl/filefairy/' + _error_title
_error_msg = 'Disabled snacks.'

_exc = """Traceback (most recent call last):
  File "impl/filefairy/filefairy.py", line 127, in _foo
    a = func(*args, **kwargs)
  File "/home/pi/filefairy/tasks/snacks/snacks.py", line 234, in _bar
    b = self._baz()
  File "/home/pi/filefairy/tasks/snacks/snacks.py", line 190, in _baz
    return variable
NameError: name 'variable' is not defined
"""

_info_title = 'leaguefile.py#L317'
_info_link = LINK + 'tasks/leaguefile/' + _info_title
_info_msg = 'File is up.'

_logs = [
    table(
        clazz='border mb-3',
        hcols=[col(clazz='font-weight-bold text-dark', colspan='3')],
        bcols=[col(clazz='w-150p'), None,
               col(clazz='text-right w-75p')],
        fcols=[col(colspan='3')],
        head=[row(cells=[cell(content='Saturday, October 26th, 1985')])],
        body=[
            row(cells=[
                cell(content=anchor(_error_link, _error_title)),
                cell(content=_error_msg),
                cell(content='06:02')
            ])
        ],
        foot=[row(cells=[cell(content=pre(_exc))])]),
    table(
        clazz='border mb-3',
        hcols=[col(clazz='font-weight-bold text-dark', colspan='3')],
        bcols=[col(clazz='w-150p'), None,
               col(clazz='text-right w-75p')],
        fcols=[col(colspan='3')],
        head=[row(cells=[cell(content='Saturday, October 26th, 1985')])],
        body=[
            row(cells=[
                cell(content=anchor(_info_link, _info_title)),
                cell(content=_info_msg),
                cell(content='02:30')
            ]),
        ]),
]

subtitle = ''

tmpl = 'dashboard.html'

context = {
    'logs': _logs,
}
