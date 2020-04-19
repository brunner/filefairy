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
from common.elements.elements import row  # noqa
from common.elements.elements import table  # noqa
from common.teams.teams import encoding_keys  # noqa
from common.teams.teams import encoding_to_decoding  # noqa
from common.teams.teams import icon_absolute  # noqa
from services.uniforms.uniforms import encoding_to_colors  # noqa
from services.uniforms.uniforms import jersey_absolute  # noqa
from services.uniforms.uniforms import jersey_style  # noqa

CONTENT = '<div class="position-relative h-58p">{}</div>'

_jerseys = []
_tables = []
for encoding in encoding_keys():
    if encoding in ['T30', 'TCH', 'TLA', 'TNY']:
        continue

    body = []
    for colors in encoding_to_colors(encoding):
        front = jersey_absolute(encoding, colors, None, 'front', [])

        backs = []
        for num in ['0', '11', '19', '21', '34', '56', '78']:
            back = jersey_absolute(encoding, colors, num, 'back', [])
            backs.append(cell(content=CONTENT.format(back)))

        cells = [cell(content=CONTENT.format(front))] + backs
        body.append(row(cells=cells))
        _jerseys.append((encoding, colors))

    decoding = encoding_to_decoding(encoding)
    head = [row(cells=[cell(content=icon_absolute(encoding, decoding))])]
    table_ = table(clazz='border mt-3',
                   hcols=[col(clazz='position-relative', colspan=8)],
                   head=head,
                   body=body)
    _tables.append(table_)

_styles = jersey_style(*_jerseys)

subtitle = ''

tmpl = 'empty.html'

context = {'styles': _styles, 'tables': _tables}
