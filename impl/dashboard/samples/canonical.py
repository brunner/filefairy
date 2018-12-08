#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sample data for dashboard.py golden test."""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/impl/dashboard/samples', '', _path))

from common.elements.elements import anchor  # noqa
from common.elements.elements import card  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import table  # noqa

LINK = 'https://github.com/brunner/filefairy/blob/master/'

_breadcrumbs = [{
    'href': '/',
    'name': 'Fairylab'
}, {
    'href': '',
    'name': 'Dashboard'
}]

_error_title = 'filefairy.py#L127'
_error_link = LINK + 'impl/filefairy/' + _error_title
_error_msg = 'Disabled snacks.'

_info_title = 'leaguefile.py#L317'
_info_link = LINK + 'tasks/leaguefile/' + _info_title
_info_msg = 'File is up.'

_logs = [
    table(
        clazz='border mt-3',
        hcols=[col(colspan='3')],
        bcols=[None, None, col(clazz='text-right w-75p')],
        head=[cell(content='Saturday, October 26th, 1985')],
        body=[
            [
                cell(content=anchor(_error_link, _error_title)),
                cell(content=_error_msg),
                cell(content='06:02')
            ],
            [
                cell(content=anchor(_info_link, _info_title)),
                cell(content=_info_msg),
                cell(content='02:30')
            ],
        ]),
]

_exc = """Traceback (most recent call last):
  File "impl/filefairy/filefairy.py", line 127, in _foo
    a = func(*args, **kwargs)
  File "/home/pi/filefairy/tasks/snacks/snacks.py", line 234, in _bar
    b = self._baz()
  File "/home/pi/filefairy/tasks/snacks/snacks.py", line 190, in _baz
    return variable
NameError: name 'variable' is not defined
"""

_exceptions = [
    card(
        href=_error_link,
        title=_error_title,
        info=_error_msg,
        code=_exc,
        ts='06:02:30 PDT (1985-10-26)')
]

subtitle = ''

tmpl = 'dashboard.html'

context = {
    'title': 'dashboard',
    'breadcrumbs': _breadcrumbs,
    'exceptions': _exceptions,
    'logs': _logs,
}
