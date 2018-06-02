#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/core/dashboard/samples', '', _path)
sys.path.append(_root)
from util.component.component import anchor  # noqa
from util.component.component import span  # noqa
from util.component.component import card  # noqa
from util.component.component import table  # noqa

_breadcrumbs = [{
    'href': '/fairylab/',
    'name': 'Home'
}, {
    'href': '',
    'name': 'Dashboard'
}]

_link = 'https://github.com/brunner/orangeandblueleague/blob/master/filefairy/'

_cols = ['', ' class="text-right w-75p"']
_ehref = _link + 'core/fairylab/fairylab.py#L127'
_etitle = 'fairylab.py#L127'
_etable = table(
    clazz='table-sm mb-2',
    bcols=_cols,
    body=[['Disabled snacks plugin.', '(1)']])
_etrace = """Traceback (most recent call last):
  File "core/fairylab/fairylab.py", line 117, in _try
    response = item(*args, **dict(kwargs, date=date))
  File "/home/pi/orangeandblueleague/filefairy3/plugin/snacks/snacks.py", line 234, in _load_internal
    fnames = self._fnames()
  File "/home/pi/orangeandblueleague/filefairy3/plugin/snacks/snacks.py", line 190, in _fnames
    return [os.path.join(d, c) for c in os.listdir(d)]
FileNotFoundError: [Errno 2] No such file or directory: '/home/pi/orangeandblueleague/filefairy3/resource/corpus'
"""
_exceptions = [
    card(
        href=_ehref, title=_etitle, table=_etable, code=_etrace, ts='43m ago')
]

_whref = _link + 'util/subprocess_/subprocess_.py#L19'
_wtitle = 'subprocess_.py#L19'
_wtable = table(
    clazz='table-sm mb-2',
    bcols=_cols,
    body=[['Handled subprocess warning.', '(10)']])
_wtrace = """Traceback (most recent call last):
  File "/home/jbrunner/orangeandblueleague/filefairy/util/subprocess_/subprocess_.py", line 16, in check_output
    check=True)
  File "/usr/lib/python3.5/subprocess.py", line 708, in run
    output=stdout, stderr=stderr)
subprocess.CalledProcessError: Command '['ssh', 'brunnerj@server', 'ls -l /var/www/html/StatsLab/league_file']' returned non-zero exit status 255
"""
_warnings = [
    card(href=_whref, title=_wtitle, table=_wtable, code=_wtrace, ts='3h ago')
]

_dlink = _link + 'core/fairylab/fairylab.py#L127'
_disabled_snacks = [
    anchor(_dlink, 'fairylab.py#L127') + '<br>Disabled snacks plugin.',
    '17:09<br>(1)'
]
_slink = _link + 'util/subprocess_/subprocess_.py#L19'
_subprocess = [
    anchor(_slink, 'subprocess_.py#L19') + '<br>Handled subprocess warning.',
    '14:47<br>(10)'
]
_tlink = _link + 'plugin/exports/exports.py#L92'
_tracker = [
    anchor(_tlink, 'exports.py#L92') + '<br>Tracker updated.', '14:21<br>(6)'
]
_rlink = _link + 'core/fairylab/fairylab.py#L252'
_reloaded_download = [
    anchor(_rlink, 'fairylab.py#L252') + '<br>Reloaded download plugin.',
    '06:02<br>(1)'
]
_reloaded_exports = [
    anchor(_rlink, 'fairylab.py#L252') + '<br>Reloaded exports plugin.',
    '06:02<br>(1)'
]

_logs = [
    table(
        clazz='border mt-3 table-fixed',
        hcols=_cols,
        bcols=_cols,
        head=['Monday, July 4th, 2022', ''],
        body=[_disabled_snacks, _subprocess, _tracker]),
    table(
        clazz='border mt-3 table-fixed',
        hcols=_cols,
        bcols=_cols,
        head=['Sunday, July 3rd, 2022', ''],
        body=[_reloaded_exports, _reloaded_download]),
]

subtitle = ''

tmpl = 'dashboard.html'

context = {
    'title': 'dashboard',
    'breadcrumbs': _breadcrumbs,
    'exceptions': _exceptions,
    'warnings': _warnings,
    'logs': _logs,
}
