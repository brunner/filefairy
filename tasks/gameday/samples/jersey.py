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
from common.teams.teams import color_name  # noqa
from common.teams.teams import encoding_keys  # noqa
from common.teams.teams import encoding_to_colors  # noqa
from common.teams.teams import encoding_to_decoding  # noqa
from common.teams.teams import encoding_to_lower  # noqa
from common.teams.teams import encoding_to_repo  # noqa
from common.teams.teams import encoding_to_tag  # noqa
from common.teams.teams import icon_absolute  # noqa
from common.teams.teams import jersey_absolute  # noqa
from common.teams.teams import jersey_color  # noqa

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

    lower = encoding_to_lower(encoding)
    repo = encoding_to_repo(encoding)
    tag = encoding_to_tag(encoding)

    body = []
    for color in ['white', 'grey'] + encoding_to_colors(encoding):
        name = color_name(color)
        _jerseys.append((lower, name, repo, tag))

        front = jersey_absolute(encoding, color, 'front')
        back = jersey_absolute(encoding, color, 'back')
        row = [
            cell(content=CONTENT.format(front)),
            cell(content=CONTENT.format(back))
        ]
        body.append(row)

    decoding = encoding_to_decoding(encoding)
    head = [[cell(content=icon_absolute(encoding, decoding, '20'))]]
    table_ = table(
        hcols=[col(clazz='position-relative', colspan=2)],
        head=head,
        body=body)
    _tables.append(table_)

subtitle = ''

tmpl = 'empty.html'

context = {
    'title': 'jersey',
    'breadcrumbs': _breadcrumbs,
    'jerseys': _jerseys,
    'tables': _tables
}
