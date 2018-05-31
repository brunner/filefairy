#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/core/dashboard/samples', '', _path)
sys.path.append(_root)
from util.component.component import span  # noqa
from util.component.component import table  # noqa

_breadcrumbs = [{
    'href': '/fairylab/',
    'name': 'Home'
}, {
    'href': '',
    'name': 'Dashboard'
}]

_fairylab = [
    'core/fairylab/fairylab.py#L252: ModuleReloadSuccess',
    span(['text-secondary'], '10h ago')
]
_git = [
    'plugin/git/git.py#L61: ConnectionError',
    span(['text-secondary'], '6h ago')
]
_snacks = [
    'plugin/snacks/snacks.py#L190: FileNotFoundError',
    span(['text-secondary'], '10m ago')
]
_logs = [
    table(
        clazz='border mt-3 table-fixed',
        hcols=['', ' class="text-right w-105p"'],
        bcols=['', ' class="text-right w-105p"'],
        head=['Monday, July 4th, 2022', ''],
        body=[_snacks, _git]),
    table(
        clazz='border mt-3 table-fixed',
        hcols=['', ' class="text-right w-105p"'],
        bcols=['', ' class="text-right w-105p"'],
        head=['Sunday, July 3rd, 2022', ''],
        body=[
            _fairylab, _fairylab, _fairylab, _fairylab, _fairylab, _fairylab,
            _fairylab
        ])
]

_error = [
    table(
        clazz='border mt-3 table-fixed',
        hcols=['', ' class="text-right w-105p"'],
        bcols=['', ' class="text-right w-105p"'],
        head=['plugin/snacks/snacks.py#190: FileNotFoundError', '(1)'],
        body=[[
            'No such file or directory: \'/home/pi/orangeandblueleague/filefairy3/resource/corpus\'.',
            span(['text-secondary'], '10m ago')
        ]]),
    table(
        clazz='border mt-3 table-fixed',
        hcols=['', ' class="text-right w-105p"'],
        bcols=['', ' class="text-right w-105p"'],
        head=['plugin/git/git.py#61: ConnectionError', '(1)'],
        body=[[
            'Request timed out: \'git commit -m "Automated data push."\'.',
            span(['text-secondary'], '6h ago')
        ]])
]
_info = [
    table(
        clazz='border mt-3 table-fixed',
        hcols=['', ' class="text-right w-105p"'],
        bcols=['', ' class="text-right w-105p"'],
        head=['core/fairylab/fairylab.py#252: ModuleReloadSuccess', '(7)'],
        body=[[
            'Reloaded plugin: \'download\'.',
            span(['text-secondary'], '10h ago')
        ], [
            'Reloaded plugin: \'exports\'.',
            span(['text-secondary'], '10h ago')
        ], ['Reloaded plugin: \'git\'.',
            span(['text-secondary'], '10h ago')], [
                'Reloaded plugin: \'leaguefile\'.',
                span(['text-secondary'], '10h ago')
            ], [
                'Reloaded plugin: \'recap\'.',
                span(['text-secondary'], '10h ago')
            ], [
                'Reloaded plugin: \'snacks\'.',
                span(['text-secondary'], '10h ago')
            ], [
                'Reloaded plugin: \'statsplus\'.',
                span(['text-secondary'], '10h ago')
            ]])
]

subtitle = ''

tmpl = 'dashboard.html'

context = {
    'title': 'dashboard',
    'breadcrumbs': _breadcrumbs,
    'logs': _logs,
    'error': _error,
    'info': _info,
}
