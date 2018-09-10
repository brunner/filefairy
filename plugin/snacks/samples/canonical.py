#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugin/snacks/samples', '', _path)
sys.path.append(_root)
from util.component.component import card  # noqa
from util.component.component import table  # noqa

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

_cols = [' class="text-center w-75p"', '', ' class="text-right"']
_count = table(
    clazz='border mt-3',
    hcols=_cols,
    bcols=_cols,
    head=['Emoji', 'Name', 'Count'],
    body=[[_strawberry, 'strawberry', '21'], [_avocado, 'avocado', '13'],
          [_pie, 'pie', '12'], [_ramen, 'ramen', '9'],
          [_green_salad, 'green_salad', '8'], [_pineapple, 'pineapple', '8']])

_recent = table(
    clazz='border mt-3',
    hcols=_cols,
    bcols=_cols,
    head=['Emoji', 'Name', 'Last activity'],
    body=[[_pineapple, 'pineapple', '5m ago'], [_avocado, 'avocado', '5m ago'],
          [_ramen, 'ramen', '5m ago'], [_green_salad, 'green_salad', '3d ago'],
          [_strawberry, 'strawberry', '3d ago'], [_pie, 'pie', '3d ago']])

subtitle = ''

tmpl = 'snacks.html'

context = {
    'title': 'snacks',
    'breadcrumbs': _breadcrumbs,
    'statistics': _statistics,
    'count': _count,
    'recent': _recent
}
