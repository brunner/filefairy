#!/usr/bin/env python3
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
from util.team.team import teamids  # noqa

_cols = [
    'class="position-relative text-truncate"', ' class="text-right w-55p"',
    ' class="text-right w-55p"', ' class="text-right w-55p"',
    ' class="text-right w-55p"'
]
_divisions = divisions()
_teamids = teamids()


def _decode(s, to_int=True):
    return [int(n) if to_int else n for n in s.split('-')]


def _keys(k):
    return [k + ey for ey in ['gb', 'mn']]


def _process_group(teams, ordered, i, k):
    kgb, kmn = _keys(k)
    ts = list(filter(lambda v: teams[v[0]][kgb] >= 0, ordered))
    if len(ts) == len(ordered):
        for t, tr in ordered:
            vs = list(filter(lambda v: v[0] != t, ts))
            u0, u0r = sorted(vs, key=lambda v: _decode(v[1])[1])[-1]
            en = elimination_number(u0r, tr)
            if not teams[t][kmn] or en > teams[t][kmn]:
                teams[t][kmn] = en
    else:
        for t, tr in ts:
            for j, (u, ur) in enumerate(ordered):
                if u == t:
                    continue
                if 'd0' in teams[u] and ((u, ur) not in ts or j > i):
                    continue
                en = elimination_number(ur, tr)
                teams[t][kmn].append(en)
        for u, ur in ordered:
            if teams[u][kmn]:
                teams[u][kmn] = sorted(teams[u][kmn], reverse=True)[i]


def _process_league(teams, league, abbr):
    lg, wc = [], []
    ret = []
    for division, ts in league:
        ordered = sort([(t, teams[t]['r']) for t in ts])
        (t0, t0r), teams[t0]['dgb'], teams[t0]['d0'] = ordered[0], 0.0, True
        for u, ur in ordered[1:]:
            gb = games_behind(t0r, ur)
            teams[u]['dgb'] = gb
            if gb == 0.0 and 'd0' in teams[t0]:
                del teams[t0]['d0']
        for t, tr in ordered:
            lg.append((t, tr))
            if 'd0' not in teams[t]:
                wc.append((t, tr))
        ret.append((division, ordered, 'd'))
        _process_group(teams, ordered, 0, 'd')

    ordered = sort(lg)
    k, j = 0, 2
    for i, (t0, t0r) in enumerate(ordered):
        if 'd0' not in teams[t0]:
            k += 1
            if teams[t0]['dgb'] == 0.0:
                j = 3
        if k == j:
            break

    teams[t0]['wgb'] = 0.0
    for (v, vr) in ordered:
        teams[v]['wgb'] = games_behind(t0r, vr)
    ret.append((abbr + ' Wild Card', sort(wc), 'w'))
    _process_group(teams, ordered, i, 'w')
    return ret


def games_behind(t, u):
    tw, tl = _decode(t)
    uw, ul = _decode(u)
    return (uw - tw + tl - ul) / 2.0


def elimination_number(u, t):
    uw, ul = _decode(u)
    tw, tl = _decode(t)
    return max(163 - tw - ul, 0)


def sort(group):
    def _sort(team_tuple):
        t, tr = team_tuple
        tw, tl = _decode(tr)
        gb = abs(min([games_behind(tr, u[1]) for u in group]))
        pct = float(tw) / ((tw + tl) or 1)
        inv = 1.0 / tl if tl else 2
        n = 1.0 / int(t)
        return (gb, pct, tw, inv, n)

    return sorted(group, key=_sort, reverse=True)


def standings_table(records, num_wc):
    size = len(_divisions) // 2
    teams = {
        t: {
            'r': records.get(t, '0-0'),
            'dmn': [],
            'dtn': [],
            'wmn': [],
            'wtn': []
        }
        for t in _teamids
    }
    tables = []
    leagues = [
        _process_league(teams, _divisions[:size], 'AL'),
        _process_league(teams, _divisions[size:], 'NL')
    ]
    for league in leagues:
        for group, ts, k in league:
            body = []
            kgb, kmn = _keys(k)
            for i, team_tuple in enumerate(sort(ts)):
                if num_wc and k == 'w' and i >= num_wc:
                    break
                t, tr = team_tuple
                tname = logo_absolute(t, teamid_to_hometown(t), 'left')
                tw, tl = _decode(tr, to_int=False)
                gb, mn = teams[t][kgb], teams[t][kmn]
                tgb = str(-gb) if gb < 0 else '+' + str(gb) if gb > 0 else '-'
                tmn = '' if mn == [] or mn < 0 else str(mn) if mn > 0 else 'X'
                body.append([tname, tw, tl, tgb, tmn])
            tables.append(
                table(
                    hcols=_cols,
                    bcols=_cols,
                    head=[group, 'W', 'L', 'GB', 'M#'],
                    body=body))

    return tables
