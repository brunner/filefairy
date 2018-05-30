#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/core/fairylab/samples', '', _path)
sys.path.append(_root)
from util.component.component import card  # noqa

_breadcrumbs = [{'href': '', 'name': 'Home'}]

_browsable = [
    card(
        href='/fairylab/bar/',
        title='bar',
        info='Description of bar.',
        ts='10m ago',
    ),
    card(
        href='/fairylab/baz/',
        title='baz',
        info='Description of baz.',
        ts='1h ago',
        danger='failed'),
    card(
        href='/fairylab/foo/',
        title='foo',
        info='Description of foo.',
        ts='2m ago',
    )
]
_internal = [
    card(
        title='quux',
        info='Description of quux.',
        ts='15m ago',
        danger='failed'),
    card(
        title='quuz',
        info='Description of quuz.',
        ts='30s ago',
        success='just now',
    ),
    card(
        title='qux',
        info='Description of qux.',
        ts='2d ago',
    )
]

subtitle = ''

tmpl = 'home.html'

context = {
    'title': 'home',
    'breadcrumbs': _breadcrumbs,
    'browsable': _browsable,
    'internal': _internal,
}
