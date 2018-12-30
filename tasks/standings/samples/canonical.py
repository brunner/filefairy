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

EXPANDED_COLS = [
    col(clazz='position-relative text-truncate'),
    col(clazz='text-right w-55p'),
    col(clazz='text-right w-55p'),
    col(clazz='text-right w-75p')
]


def _expanded_head(subleague):
    return [
        cell(content=subleague),
        cell(content='W'),
        cell(content='L'),
        cell(content='GB'),
    ]


_breadcrumbs = [{
    'href': '/',
    'name': 'Fairylab'
}, {
    'href': '',
    'name': 'Standings'
}]

_inline = ('<img src="https://fairylab.surge.sh/images/teams/{0}/{0}-icon.png"'
           ' width="20" height="20" border="0" class="d-inline-block"><span cl'
           'ass="align-middle d-inline-block px-2">{1}</span>')
_recent = [
    table(
        clazz='table-fixed border mt-3',
        hcols=[col(clazz='text-center', colspan=5)],
        bcols=[col(clazz='td-sm position-relative text-center w-20')] * 5,
        head=[cell(content='American League')],
        body=[
            [
                cell(content=_inline.format('orioles', '0-0')),
                cell(content=_inline.format('redsox', '0-0')),
                cell(content=_inline.format('yankees', '0-0')),
                cell(content=_inline.format('rays', '0-0')),
                cell(content=_inline.format('bluejays', '0-0')),
            ],
            [
                cell(content=_inline.format('whitesox', '0-0')),
                cell(content=_inline.format('indians', '0-0')),
                cell(content=_inline.format('tigers', '0-0')),
                cell(content=_inline.format('royals', '0-0')),
                cell(content=_inline.format('twins', '0-0')),
            ],
            [
                cell(content=_inline.format('astros', '0-0')),
                cell(content=_inline.format('angels', '0-0')),
                cell(content=_inline.format('athletics', '0-0')),
                cell(content=_inline.format('mariners', '0-0')),
                cell(content=_inline.format('rangers', '0-0')),
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
                cell(content=_inline.format('braves', '0-0')),
                cell(content=_inline.format('marlins', '0-0')),
                cell(content=_inline.format('mets', '0-0')),
                cell(content=_inline.format('phillies', '0-0')),
                cell(content=_inline.format('nationals', '0-0')),
            ],
            [
                cell(content=_inline.format('cubs', '0-0')),
                cell(content=_inline.format('reds', '0-0')),
                cell(content=_inline.format('brewers', '0-0')),
                cell(content=_inline.format('pirates', '0-0')),
                cell(content=_inline.format('cardinals', '0-0')),
            ],
            [
                cell(content=_inline.format('diamondbacks', '0-0')),
                cell(content=_inline.format('rockies', '0-0')),
                cell(content=_inline.format('dodgers', '0-0')),
                cell(content=_inline.format('padres', '0-0')),
                cell(content=_inline.format('giants', '0-0')),
            ],
        ],
    ),
]

_absolute = ('<img src="https://fairylab.surge.sh/images/teams/{0}/{0}-icon.pn'
             'g" width="20" height="20" border="0" class="position-absolute le'
             'ft-8p top-14p"><span class="d-block text-truncate pl-24p">{1}</s'
             'pan>')
_expanded = [
    table(
        hcols=EXPANDED_COLS,
        bcols=EXPANDED_COLS,
        head=_expanded_head('AL East'),
        body=[
            [
                cell(content=_absolute.format('orioles', 'Baltimore')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=_absolute.format('redsox', 'Boston')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=_absolute.format('yankees', 'New York')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=_absolute.format('rays', 'Tampa Bay')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=_absolute.format('bluejays', 'Toronto')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
        ],
    ),
    table(
        hcols=EXPANDED_COLS,
        bcols=EXPANDED_COLS,
        head=_expanded_head('NL East'),
        body=[
            [
                cell(content=_absolute.format('braves', 'Atlanta')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=_absolute.format('marlins', 'Miami')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=_absolute.format('mets', 'New York')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=_absolute.format('phillies', 'Philadelphia')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=_absolute.format('nationals', 'Washington')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
        ],
    ),
    table(
        hcols=EXPANDED_COLS,
        bcols=EXPANDED_COLS,
        head=_expanded_head('AL Central'),
        body=[
            [
                cell(content=_absolute.format('whitesox', 'Chicago')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=_absolute.format('indians', 'Cleveland')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=_absolute.format('tigers', 'Detroit')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=_absolute.format('royals', 'Kansas City')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=_absolute.format('twins', 'Minnesota')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
        ],
    ),
    table(
        hcols=EXPANDED_COLS,
        bcols=EXPANDED_COLS,
        head=_expanded_head('NL Central'),
        body=[
            [
                cell(content=_absolute.format('cubs', 'Chicago')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=_absolute.format('reds', 'Cincinnati')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=_absolute.format('brewers', 'Milwaukee')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=_absolute.format('pirates', 'Pittsburgh')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=_absolute.format('cardinals', 'St. Louis')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
        ],
    ),
    table(
        hcols=EXPANDED_COLS,
        bcols=EXPANDED_COLS,
        head=_expanded_head('AL West'),
        body=[
            [
                cell(content=_absolute.format('astros', 'Houston')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=_absolute.format('angels', 'Los Angeles')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=_absolute.format('athletics', 'Oakland')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=_absolute.format('mariners', 'Seattle')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=_absolute.format('rangers', 'Texas')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
        ],
    ),
    table(
        hcols=EXPANDED_COLS,
        bcols=EXPANDED_COLS,
        head=_expanded_head('NL West'),
        body=[
            [
                cell(content=_absolute.format('diamondbacks', 'Arizona')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=_absolute.format('rockies', 'Colorado')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=_absolute.format('dodgers', 'Los Angeles')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=_absolute.format('padres', 'San Diego')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=_absolute.format('giants', 'San Francisco')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
        ],
    ),
    table(
        hcols=EXPANDED_COLS,
        bcols=EXPANDED_COLS,
        head=_expanded_head('AL Wild Card'),
        body=[
            [
                cell(content=_absolute.format('orioles', 'Baltimore')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=_absolute.format('redsox', 'Boston')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=_absolute.format('whitesox', 'Chicago')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=_absolute.format('indians', 'Cleveland')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=_absolute.format('tigers', 'Detroit')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
        ],
    ),
    table(
        hcols=EXPANDED_COLS,
        bcols=EXPANDED_COLS,
        head=_expanded_head('NL Wild Card'),
        body=[
            [
                cell(content=_absolute.format('diamondbacks', 'Arizona')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=_absolute.format('braves', 'Atlanta')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=_absolute.format('cubs', 'Chicago')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=_absolute.format('reds', 'Cincinnati')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
            ],
            [
                cell(content=_absolute.format('rockies', 'Colorado')),
                cell(content='0'),
                cell(content='0'),
                cell(content='-'),
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
    'expanded': _expanded,
}
