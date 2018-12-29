#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sample data for standings.py golden test."""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/tasks/standings/samples', '', _path))

from common.elements.elements import anchor  # noqa
from common.elements.elements import card  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import table  # noqa

_breadcrumbs = [{
    'href': '/',
    'name': 'Fairylab'
}, {
    'href': '',
    'name': 'Standings'
}]

_content = ('<img src="https://fairylab.surge.sh/images/teams/{0}/{0}-icon.png'
            '" width="20" height="20" border="0" class="d-inline-block"><span '
            'class="align-middle d-inline-block px-2">{1}</span>')
_recent = [
    table(
        clazz='table-fixed border mt-3',
        hcols=[col(clazz='text-center', colspan=5)],
        bcols=[col(clazz='td-sm position-relative text-center w-20')] * 5,
        head=[cell(content='American League')],
        body=[
            [
                cell(content=_content.format('orioles', '0-0')),
                cell(content=_content.format('redsox', '0-0')),
                cell(content=_content.format('yankees', '0-0')),
                cell(content=_content.format('rays', '0-0')),
                cell(content=_content.format('bluejays', '0-0')),
            ],
            [
                cell(content=_content.format('whitesox', '0-0')),
                cell(content=_content.format('indians', '0-0')),
                cell(content=_content.format('tigers', '0-0')),
                cell(content=_content.format('royals', '0-0')),
                cell(content=_content.format('twins', '0-0')),
            ],
            [
                cell(content=_content.format('astros', '0-0')),
                cell(content=_content.format('angels', '0-0')),
                cell(content=_content.format('athletics', '0-0')),
                cell(content=_content.format('mariners', '0-0')),
                cell(content=_content.format('rangers', '0-0')),
            ],
        ],
    ),
    table(
        clazz='table-fixed border mt-3',
        hcols=[col(clazz='text-center', colspan=5)],
        bcols=[col(clazz='td-sm position-relative text-center w-20')] * 5,
        head=[cell(content='National League')],
        body=[
            [
                cell(content=_content.format('braves', '0-0')),
                cell(content=_content.format('marlins', '0-0')),
                cell(content=_content.format('mets', '0-0')),
                cell(content=_content.format('phillies', '0-0')),
                cell(content=_content.format('nationals', '0-0')),
            ],
            [
                cell(content=_content.format('cubs', '0-0')),
                cell(content=_content.format('reds', '0-0')),
                cell(content=_content.format('brewers', '0-0')),
                cell(content=_content.format('pirates', '0-0')),
                cell(content=_content.format('cardinals', '0-0')),
            ],
            [
                cell(content=_content.format('diamondbacks', '0-0')),
                cell(content=_content.format('rockies', '0-0')),
                cell(content=_content.format('dodgers', '0-0')),
                cell(content=_content.format('padres', '0-0')),
                cell(content=_content.format('giants', '0-0')),
            ],
        ],
    ),
]

subtitle = ''

tmpl = 'standings.html'

context = {
    'title': 'standings',
    'breadcrumbs': _breadcrumbs,
    'recent': _recent,
    'table': [],
}
