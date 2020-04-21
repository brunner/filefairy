#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Common (non-reloadable) util methods for team information."""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/common/styles', '', _path))

from common.elements.elements import ruleset  # noqa

BASE_STYLES = {
    'badge': [
        ruleset(
            '.badge-icon',
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
            '.badge-icon[data-dismiss="modal"]:hover,\n' +
            '.badge-icon[data-toggle="modal"]:hover',
            [
                'background-color: #e9ecef',
                'border-color: #dee2e6',
            ],
        ),
        ruleset(
            '.badge-icon-button',
            [
                'display: block',
                'padding: 3px 0 2px',
            ],
        ),
        ruleset(
            '.badge-icon-image,\n.badge-icon-text',
            [
                'display: block',
            ],
        ),
        ruleset(
            '.badge-icon-image',
            [
                'margin: 1px auto 0',
            ],
        ),
        ruleset(
            '.badge-icon-grey',
            [
                '-webkit-filter: grayscale(1) opacity(0.5)',
                'filter: grayscale(1) opacity(0.5)',
            ],
        ),
        ruleset(
            '.badge-icon-text',
            [
                'color: #212529',
                'padding: 0',
                'padding-top: .25rem',
            ],
        ),
    ]
}


def base_styles():
    return BASE_STYLES
