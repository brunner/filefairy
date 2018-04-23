#!/usr/bin/env python
# -*- coding: utf-8 -*-


def _decode(s):
    return [int(n) for n in s.split('-')]


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
