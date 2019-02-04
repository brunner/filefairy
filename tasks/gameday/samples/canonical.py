#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sample data for gameday.py golden test."""

import json
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/tasks/gameday/samples', '', _path))

from common.elements.elements import topper  # noqa
from common.test.test import get_testdata  # noqa
from services.scoreboard.scoreboard import line_score_body  # noqa
from services.scoreboard.scoreboard import line_score_foot  # noqa
from services.scoreboard.scoreboard import pending_body  # noqa

TESTDATA = get_testdata()

_game_2449 = json.loads(TESTDATA['2449.json'])
_head_2449 = topper('Wednesday, August 28th, 2024')
_body_2449 = line_score_body(_game_2449)
_foot_2449 = line_score_foot(_game_2449)

_game_2469 = json.loads(TESTDATA['2469.json'])
_head_2469 = topper('Thursday, August 29th, 2024')
_body_2469 = line_score_body(_game_2469)
_foot_2469 = line_score_foot(_game_2469)

_game_2476 = json.loads(TESTDATA['2476.json'])
_head_2476 = topper('Friday, August 30th, 2024')
_body_2476 = line_score_body(_game_2476)
_foot_2476 = line_score_foot(_game_2476)

_body_pending = pending_body(['T31 4, TLA 2', 'TNY 5, TLA 3', 'TNY 1, T55 0'])

_days = [
    [_head_2449, _body_2449, _foot_2449, _body_pending],
    [_head_2469, _body_2469, _foot_2469],
    [_head_2476, _body_2476, _foot_2476],
]

subtitle = ''

tmpl = 'gameday.html'

context = {
    'days': _days,
}
