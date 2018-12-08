#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/tasks/snacks/samples', '', _path)
sys.path.append(_root)
from common.elements.elements import card  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import table  # noqa

_breadcrumbs = [{
    'href': '/',
    'name': 'Fairylab'
}, {
    'href': '',
    'name': 'Snacks'
}]

_servings = card(title='143', info='Total snacks served.', ts='5m ago')
_stars = card(title='3', info='Total stars awarded.', ts='23d ago')
_trophies = card(title='1', info='Total trophies lifted.', ts='51d ago')
_statistics = [_servings, _stars, _trophies]

_avocado = '\U0001F951'
_green_salad = '\U0001F957'
_pie = '\U0001F967'
_pineapple = '\U0001F34D'
_ramen = '\U0001F35C'
_strawberry = '\U0001F353'

_cols = [col(clazz='text-center w-75p'), col(), col(clazz='text-right')]
_count = table(
    clazz='border mt-3',
    hcols=_cols,
    bcols=_cols,
    head=[
        cell(content='Emoji'),
        cell(content='Name'),
        cell(content='Count'),
    ],
    body=[
        [
            cell(content=_strawberry),
            cell(content='strawberry'),
            cell(content='21'),
        ],
        [
            cell(content=_avocado),
            cell(content='avocado'),
            cell(content='13'),
        ],
        [
            cell(content=_pie),
            cell(content='pie'),
            cell(content='12'),
        ],
        [
            cell(content=_ramen),
            cell(content='ramen'),
            cell(content='9'),
        ],
        [
            cell(content=_green_salad),
            cell(content='green_salad'),
            cell(content='8'),
        ],
        [
            cell(content=_pineapple),
            cell(content='pineapple'),
            cell(content='8'),
        ],
    ])

_recent = table(
    clazz='border mt-3',
    hcols=_cols,
    bcols=_cols,
    head=[
        cell(content='Emoji'),
        cell(content='Name'),
        cell(content='Last activity'),
    ],
    body=[
        [
            cell(content=_pineapple),
            cell(content='pineapple'),
            cell(content='5m ago'),
        ],
        [
            cell(content=_avocado),
            cell(content='avocado'),
            cell(content='5m ago'),
        ],
        [
            cell(content=_ramen),
            cell(content='ramen'),
            cell(content='5m ago'),
        ],
        [
            cell(content=_green_salad),
            cell(content='green_salad'),
            cell(content='3d ago'),
        ],
        [
            cell(content=_strawberry),
            cell(content='strawberry'),
            cell(content='3d ago'),
        ],
        [
            cell(content=_pie),
            cell(content='pie'),
            cell(content='3d ago'),
        ],
    ])

subtitle = ''

tmpl = 'snacks.html'

context = {
    'title': 'snacks',
    'breadcrumbs': _breadcrumbs,
    'statistics': _statistics,
    'count': _count,
    'recent': _recent
}
