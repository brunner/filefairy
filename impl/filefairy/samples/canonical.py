#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/core/fairylab/samples', '', _path)
sys.path.append(_root)
from common.elements.elements import card  # noqa

_breadcrumbs = [{'href': '', 'name': 'Fairylab'}]

_registered = [
    card(
        href='/fairylab/bar/',
        title='bar',
        info='Description of bar.',
        ts='06:02:30 EDT (1985-10-26)',
    ),
    card(
        href='/fairylab/baz/',
        title='baz',
        info='Description of baz.',
        ts='06:02:30 EDT (1985-10-26)',
        danger='disabled'),
    card(
        href='/fairylab/foo/',
        title='foo',
        info='Description of foo.',
        ts='06:02:30 EDT (1985-10-26)',
    ),
    card(
        href='/fairylab/quux/',
        title='quux',
        info='Description of quux.',
        ts='06:02:30 EDT (1985-10-26)',
        danger='disabled'),
    card(
        href='/fairylab/quuz/',
        title='quuz',
        info='Description of quuz.',
        ts='06:02:30 EDT (1985-10-26)',
    ),
    card(
        href='/fairylab/qux/',
        title='qux',
        info='Description of qux.',
        ts='06:02:30 EDT (1985-10-26)',
    )
]

subtitle = ''

tmpl = 'home.html'

context = {
    'title': 'home',
    'breadcrumbs': _breadcrumbs,
    'registered': _registered,
}
