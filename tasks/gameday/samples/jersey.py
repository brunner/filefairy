#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/tasks/gameday/samples', '', _path))
from common.elements.elements import anchor  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import table  # noqa
from common.teams.teams import encoding_keys  # noqa
from common.teams.teams import encoding_to_colors  # noqa
from common.teams.teams import encoding_to_decoding  # noqa
from common.teams.teams import icon_absolute  # noqa
from common.teams.teams import jersey_absolute  # noqa
from common.teams.teams import jersey_color  # noqa
from common.teams.teams import jersey_style  # noqa

CONTENT = '<div class="position-relative h-72p">{}</div>'

_breadcrumbs = [{
    'href': '/',
    'name': 'Fairylab'
}, {
    'href': '',
    'name': 'Jersey'
}]

_jerseys = []
_tables = []
for encoding in encoding_keys():
    if encoding in ['TCH', 'TLA', 'TNY']:
        continue

    body = []
    for color in ['white', 'grey'] + encoding_to_colors(encoding):
        front = jersey_absolute(encoding, color, 'front')
        back = jersey_absolute(encoding, color, 'back')
        row = [
            cell(content=CONTENT.format(front)),
            cell(content=CONTENT.format(back))
        ]
        body.append(row)
        _jerseys.append((encoding, color))

    decoding = encoding_to_decoding(encoding)
    head = [[cell(content=icon_absolute(encoding, decoding, '20'))]]
    table_ = table(
        hcols=[col(clazz='position-relative', colspan=2)],
        head=head,
        body=body)
    _tables.append(table_)

_styles = jersey_style(*_jerseys)

subtitle = ''

tmpl = 'empty.html'

context = {
    'title': 'jersey',
    'breadcrumbs': _breadcrumbs,
    'styles': _styles,
    'tables': _tables
}
