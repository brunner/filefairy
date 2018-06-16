#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugin/git/samples', '', _path)
sys.path.append(_root)
from util.component.component import anchor  # noqa
from util.component.component import span  # noqa
from util.component.component import table  # noqa

_breadcrumbs = [{
    'href': '/fairylab/',
    'name': 'Home'
}, {
    'href': '',
    'name': 'Git'
}]

_commit = 'https://github.com/brunner/orangeandblueleague/commit/'
_ebf = anchor(_commit + 'ebf3b76317d286fdccc314fa2865e351f56e04ad', 'ebf3b76')
_4ce = anchor(_commit + '4ce85e1b709a23532c37a27b6066e0ac131527d4', '4ce85e1')
_fd1 = anchor(_commit + 'fd1bc5566e1ee5439874244898240bf48c22a7e0', 'fd1bc55')
_d03 = anchor(_commit + 'd03805db8a1b2d03ab77b47f0f20a5669a0a6c4c', 'd03805d')

_l = ['d-inline-block', 'w-65p']
_r = ['d-inline-block', 'text-right', 'w-65p']

_pull = table(
    clazz='border mt-3',
    head=['Range', 'Date', 'Time'],
    body=[[span(_l, _ebf) + ' ... ' + span(_r, _4ce), 'Jun 14', '22:11']])

_push = table(
    clazz='border mt-3',
    head=['Range', 'Date', 'Time'],
    body=[[span(_l, _d03) + ' ... ' + span(_r, _fd1), 'Jun 14', '00:01']])

subtitle = ''

tmpl = 'git.html'

context = {
    'title': 'git',
    'breadcrumbs': _breadcrumbs,
    'pull': _pull,
    'push': _push,
}
