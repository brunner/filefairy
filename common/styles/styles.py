#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Common (non-reloadable) util methods for team information."""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/common/styles', '', _path))

from common.elements.elements import media  # noqa
from common.elements.elements import ruleset  # noqa
from common.re_.re_ import findall  # noqa
from common.re_.re_ import search  # noqa

BASE_STYLES = {
    'badge-pitch': [
        ruleset(
            '.badge-pitch',
            [
                'border-radius: 16px',
                'height: 16px',
                'line-height: 16px',
                'margin-left: 15px',
                'margin-right: 26px',
                'padding: 0 .4em',
                'text-align: center',
                'width: 24px',
                'vertical-align: top',
            ],
        ),
        ruleset(
            '.badge-pitch-danger',
            [
                'color: #721c24',
                'background-color: #f8d7da',
                'border: 1px solid #721c24',
            ],
        ),
        ruleset(
            '.badge-pitch-primary',
            [
                'color: #004085',
                'background-color: #cce5ff',
                'border: 1px solid #004085',
            ],
        ),
        ruleset(
            '.badge-pitch-success',
            [
                'color: #155724',
                'background-color: #d4edda',
                'border: 1px solid #155724',
            ],
        ),
    ],
    'badge-team': [
        ruleset(
            '.badge-team',
            [
                'border: 1px solid #dee2e6',
                'cursor: pointer',
                'font-weight: 400!important',
                'font-size: 100%',
                'padding: .25rem .5rem',
                'white-space: normal',
                'width: 100%',
            ],
        ),
        ruleset(
            '.badge-team[data-dismiss="modal"]:hover,\n' +
            '.badge-team[data-toggle="modal"]:hover',
            [
                'background-color: #e9ecef',
                'border-color: #dee2e6',
            ],
        ),
        ruleset(
            '.badge-team-button',
            [
                'display: block',
                'padding: 3px 0 2px',
            ],
        ),
        ruleset(
            '.badge-team-image,\n.badge-team-text',
            [
                'display: block',
            ],
        ),
        ruleset(
            '.badge-team-image',
            [
                'margin: 1px auto 0',
            ],
        ),
        ruleset(
            '.badge-team-grey',
            [
                '-webkit-filter: grayscale(1) opacity(0.5)',
                'filter: grayscale(1) opacity(0.5)',
            ],
        ),
        ruleset(
            '.badge-team-text',
            [
                'color: #212529',
                'padding: 0',
                'padding-top: .25rem',
            ],
        ),
        media(
            '576px',
            [
                ruleset(
                    '.badge-team-image,\n.badge-team-text',
                    [
                        'display: inline-block',
                    ],
                ),
                ruleset(
                    '.badge-team-text',
                    [
                        'padding: 2px 0 2px .5rem',
                    ],
                ),
            ],
        ),
        media(
            '768px',
            [
                ruleset(
                    '.badge-team-image,\n.badge-team-text',
                    [
                        'display: block',
                    ],
                ),
                ruleset(
                    '.badge-team-text',
                    [
                        'padding: 0',
                        'padding-top: .25rem',
                    ],
                ),
            ],
        ),
        media(
            '992px',
            [
                ruleset(
                    '.badge-team-image,\n.badge-team-text',
                    [
                        'display: inline-block',
                    ],
                ),
                ruleset(
                    '.badge-team-text',
                    [
                        'padding: 2px 0 2px .5rem',
                    ],
                ),
            ],
        ),
    ],
    'ballpark': [
        ruleset(
            '.ballpark',
            [
                'height: 256px',
                'overflow: hidden',
                'position: relative',
            ],
        ),
        ruleset(
            '.ballpark-inner',
            [
                'height: 256px',
                'left: 0',
                'margin: 0 auto',
                'position: absolute',
                'right: 0',
                'width: 256px',
                'z-index: 100',
            ],
        ),
    ],
    'jersey': [
        ruleset(
            '.jersey-base',
            [
                'background-size: 62px 66px',
                'border: 1px solid #eeeff0',
                'height: 68px',
                'margin: -5px -1px -5px -5px',
                'width: 64px',
            ],
        ),
        ruleset(
            '.jersey-ballpark',
            [
                'background-position: -122px -36px',
                'background-size: 500px 512px',
                'height: 256px',
                'margin: 0',
                'opacity: 0.3',
                'width: 256px',
            ],
        ),
        ruleset(
            '.jersey-left',
            [
                'right: 50%',
            ],
        ),
        ruleset(
            '.jersey-right',
            [
                'left: 50%',
            ],
        ),
        media(
            '768px',
            [
                ruleset(
                    '.jersey-ballpark',
                    [
                        'background-size: 750px 768px',
                        'height: 256px',
                        'width: 388px',
                    ],
                ),
                ruleset(
                    '.jersey-left',
                    [
                        'background-position: -165px -118px',
                    ],
                ),
                ruleset(
                    '.jersey-right',
                    [
                        'background-position: -199px -118px',
                    ],
                ),
            ],
        ),
        media(
            '992px',
            [
                ruleset(
                    '.jersey-ballpark',
                    [
                        'background-size: 1000px 1024px',
                        'height: 256px',
                        'width: 512px',
                    ],
                ),
                ruleset(
                    '.jersey-left',
                    [
                        'background-position: -220px -244px',
                    ],
                ),
                ruleset(
                    '.jersey-right',
                    [
                        'background-position: -268px -244px',
                    ],
                ),
            ],
        ),
        media(
            '1200px',
            [
                ruleset(
                    '.jersey-ballpark',
                    [
                        'background-size: 1000px 1024px',
                        'height: 256px',
                        'width: 556px',
                    ],
                ),
                ruleset(
                    '.jersey-left',
                    [
                        'background-position: -220px -244px',
                    ],
                ),
                ruleset(
                    '.jersey-right',
                    [
                        'background-position: -224px -244px',
                    ],
                ),
            ],
        ),
        ruleset(
            '.jersey-profile-text',
            [
                'min-height: 72px',
                'padding-left: 65px',
            ],
        ),
    ],
    'score-tag': [
        ruleset(
            '.tag',
            [
                'background-color: #ffffff',
                'line-height: 16px',
                'padding: 0 .75em',
                'vertical-align: top',
            ],
        ),
        ruleset(
            '.tag-light',
            [
                'border-color: #1b1e21!important',
                'color: #1b1e21',
            ],
        ),
    ]
}


def _find_base_style(pattern, context):
    ret = False

    is_dict = isinstance(context, dict)
    is_list = isinstance(context, list)
    if is_dict or is_list:
        items = context.items() if is_dict else enumerate(context)
        for key, value in items:
            if isinstance(value, str) and search(pattern, value):
                context[key] = _rewrite_context(pattern, value)
                ret = True
            if _find_base_style(pattern, value):
                ret = True

    return ret


GENERATED_PATTERN = r'css-style-([a-z]+)-([0-9]+)([a-z]*)[\s"]'


def _find_generated_style(found, generated, context):
    is_dict = isinstance(context, dict)
    is_list = isinstance(context, list)
    if is_dict or is_list:
        items = context.items() if is_dict else enumerate(context)
        for key, value in items:
            if isinstance(value, str):
                for attr, val, unit in findall(GENERATED_PATTERN, value):
                    selector = '.' + attr + '-' + val + unit
                    if selector not in found:
                        r = ruleset(selector, [
                            '{}: {}{}'.format(_get_attr(attr), val, unit)])
                        found.add(selector)
                        generated.append(r)
                context[key] = re.sub(r'css-style-', '', value)
            _find_generated_style(found, generated, value)


def _get_attr(attr):
    if attr == 'h':
        return 'height'
    if attr == 'w':
        return 'width'

    return 'unknown'


def _rewrite_context(pattern, value):
    value = re.sub(r'"' + pattern + r'\s?', r'"', value)
    value = re.sub(r'^' + pattern + r'\s?', r'', value)
    value = re.sub(r'\s?' + pattern + r'"', r'"', value)
    value = re.sub(r'\s?' + pattern + r'$', r'', value)
    return re.sub(pattern + r' ', r'', value)


def get_styles(context):
    extra_styles = context.pop('styles', [])

    styles = []
    for name in BASE_STYLES:
        pattern = r'css-style-' + name
        if _find_base_style(pattern, context):
            styles += BASE_STYLES[name]

    found = set()
    generated = []
    _find_generated_style(found, generated, context)

    styles += sorted(generated, key=lambda r: r['selector'])
    styles += extra_styles
    return styles
