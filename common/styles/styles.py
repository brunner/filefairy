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

BASE_STYLES = {
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
    ]
}


def base_styles():
    return BASE_STYLES
