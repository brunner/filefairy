#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sample data for filefairy.py golden test."""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/core/fairylab/samples', '', _path))

from common.elements.elements import card  # noqa

_external = [
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
_internal = [
    card(
        title='bar',
        info='Description of bar.',
        ts='06:02:30 EDT (1985-10-26)',
    ),
    card(
        title='quux',
        info='Description of quux.',
        ts='06:02:30 EDT (1985-10-26)',
        danger='disabled'),
]

subtitle = ''

tmpl = 'home.html'

context = {
    'external': _external,
    'internal': _internal,
}
