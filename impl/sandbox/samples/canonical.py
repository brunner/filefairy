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
from common.elements.elements import menu  # noqa
from common.elements.elements import row  # noqa
from common.elements.elements import table  # noqa
from common.teams.teams import encoding_keys  # noqa
from common.teams.teams import encoding_to_decoding  # noqa
from common.teams.teams import icon_absolute  # noqa
from services.uniforms.uniforms import encoding_to_colors  # noqa
from services.uniforms.uniforms import jersey_absolute  # noqa
from services.uniforms.uniforms import jersey_style  # noqa

BCOLS = [col(clazz='w-75p')] + ([col(clazz='w-70p')] * 3) + [col()]
CONTENT = '<div class="position-relative h-58p">{}</div>'


def numbers():
    while True:
        for num in ['0', '1', '11', '19', '21', '34', '56', '78']:
            yield num


_jerseys = []
_tables = []

_keys = encoding_keys()
_keys_length = len(_keys)
for i, encoding in enumerate(_keys):
    if encoding in ['T30', 'TCH', 'TLA', 'TNY']:
        continue

    body = []
    numbers_generator = numbers()
    for colors in encoding_to_colors(encoding):
        front = jersey_absolute(encoding, colors, None, 'front', [])

        backs = []
        for _ in range(4):
            num = next(numbers_generator)
            back = jersey_absolute(encoding, colors, num, 'back', [])
            backs.append(cell(content=CONTENT.format(back)))

        cells = [cell(content=CONTENT.format(front))] + backs
        body.append(row(cells=cells))
        _jerseys.append((encoding, colors))

    decoding = encoding_to_decoding(encoding)
    head = [row(cells=[cell(content=icon_absolute(encoding, decoding))])]
    table_ = table(clazz='border mb-3',
                   hcols=[col(clazz='position-relative', colspan=5)],
                   head=head,
                   bcols=BCOLS,
                   body=body)
    _tables.append(table_)

_styles = jersey_style(*_jerseys)

subtitle = ''

tmpl = 'sandbox.html'

context = {'styles': _styles, 'tables': _tables}
