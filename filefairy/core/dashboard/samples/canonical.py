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
    'href': '/',
    'name': 'Fairylab'
}, {
    'href': '',
    'name': 'Dashboard'
}]

_link = 'https://github.com/brunner/orangeandblueleague/blob/master/filefairy/'

_ehref = _link + 'core/fairylab/fairylab.py#L127'
_etitle = 'fairylab.py#L127'
_einfo = 'Disabled snacks plugin.'
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
    card(href=_ehref, title=_etitle, info=_einfo, code=_etrace, ts='06:02:30 EDT (1985-10-26)')
]

_whref = _link + 'util/subprocess_/subprocess_.py#L19'
_wtitle = 'subprocess_.py#L19'
_winfo = 'Handled subprocess warning (x6).'
_wtrace = """Traceback (most recent call last):
  File "/home/jbrunner/orangeandblueleague/filefairy/util/subprocess_/subprocess_.py", line 16, in check_output
    check=True)
  File "/usr/lib/python3.5/subprocess.py", line 708, in run
    stdout=stdout, stderr=stderr)
subprocess.CalledProcessError: Command '['ssh', 'brunnerj@server', 'ls -l /var/www/html/StatsLab/league_file']' returned non-zero exit status 255
"""
_warnings = [
    card(href=_whref, title=_wtitle, info=_winfo, code=_wtrace, ts='06:02:30 EDT (1985-10-26)')
]

_dlink = _link + 'core/fairylab/fairylab.py#L127'
_disabled_snacks = [
    '<div class="d-inline-block pr-1">' + anchor(_dlink, 'fairylab.py#L127') +
    '</div><div class="d-inline-block">Disabled snacks plugin.</div>', '17:09'
]
_slink = _link + 'util/subprocess_/subprocess_.py#L19'
_subprocess = [
    '<div class="d-inline-block pr-1">' +
    anchor(_slink, 'subprocess_.py#L19') +
    '</div><div class="d-inline-block">Handled subprocess warning (x10).</div>',
    '14:47'
]
_tlink = _link + 'plugin/exports/exports.py#L92'
_tracker = [
    '<div class="d-inline-block pr-1">' + anchor(_tlink, 'exports.py#L92') +
    '</div><div class="d-inline-block">Tracker updated (x6).</div>',
    '14:21'
]
_rlink = _link + 'core/fairylab/fairylab.py#L252'
_reloaded_download = [
    '<div class="d-inline-block pr-1">' + anchor(_rlink, 'fairylab.py#L252') +
    '</div><div class="d-inline-block">Reloaded download plugin.</div>',
    '06:02'
]
_reloaded_exports = [
    '<div class="d-inline-block pr-1">' + anchor(_rlink, 'fairylab.py#L252') +
    '</div><div class="d-inline-block">Reloaded exports plugin.</div>', '06:02'
]

_cols = ['', ' class="text-right w-75p"']
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
