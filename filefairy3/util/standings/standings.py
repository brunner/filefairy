#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/util/standings', '', _path))
from util.component.component import table  # noqa
from util.team.team import divisions  # noqa
from util.team.team import logo_absolute  # noqa
from util.team.team import teamid_to_hometown  # noqa

_cols = [
    'class="position-relative text-truncate"', ' class="text-right w-55p"',
    ' class="text-right w-55p"'
]
_divisions = divisions()


def _decode(s, to_int=True):
    return [int(n) if to_int else n for n in s.split('-')]


def games_behind(t, u):
    tw, tl = _decode(t)
    uw, ul = _decode(u)
    return (uw - tw + tl - ul) / 2.0


def elimination_number(t, u):
    tw, tl = _decode(t)
    uw, ul = _decode(u)
    return max(163 - uw - tl, 0)


def sort(group):
    def _sort(team_tuple):
        teamid, t = team_tuple
        tw, tl = _decode(t)
        gb = abs(min([games_behind(t, u[1]) for u in group]))
        pct = float(tw) / ((tw + tl) or 1)
        inv = 1.0 / tl if tl else 2
        n = 1.0 / int(teamid)
        return (gb, pct, tw, inv, n)

    return sorted(group, key=_sort, reverse=True)


def standings_table(records):
    tables = []
    for division, teamids in _divisions:
        body = []
        for team_tuple in sort(filter(lambda t: t[0] in teamids, records)):
            teamid, record = team_tuple
            t = logo_absolute(teamid, teamid_to_hometown(teamid), 'left')
            w, l = _decode(record, to_int=False)
            body.append([t, w, l])

        tables.append(
            table(
                hcols=_cols, bcols=_cols, head=[division, 'W', 'L'],
                body=body))

    return tables
