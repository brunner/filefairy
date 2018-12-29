#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Service (reloadable) methods for displaying divisional standings."""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/services/division', '', _path))

from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import table  # noqa
from common.record.record import decode_record  # noqa
from common.teams.teams import encoding_to_teamid  # noqa
from common.teams.teams import icon_inline  # noqa


def _diff(record1, record2):
    w1, l1 = decode_record(record1)
    w2, l2 = decode_record(record2)

    return (w2 - w1 + l1 - l2) / 2.0


def _sort(table_):
    def _sort(team1):
        record1 = table_[team1]
        tw, tl = decode_record(record1)

        diff = abs(min([_diff(record1, table_[team2]) for team2 in table_]))
        pcnt = float(tw) / ((tw + tl) or 1)
        invs = 1.0 / tl if tl else 2
        name = 1.0 / int(encoding_to_teamid(team1))
        return (diff, pcnt, tw, invs, name)

    return sorted(table_, key=_sort, reverse=True)


def condensed(title, tables):
    """Create a condensed-view table for a given league's standings.

    The condensed-view table shows a number of rows (one for each division),
    with each row column containing the team logo and record. The rows are
    sorted left to right, first place to last place.

    The expected format for a division table is a dictionary mapping from team
    encoding to team record.

    Args:
        title: The league name.
        tables: The list of division tables.

    Returns:
        A renderable table element in the condensed-view style.
    """
    body = []
    for table_ in tables:
        row = []
        for team in _sort(table_):
            row.append(cell(content=icon_inline(team, table_[team])))
        body.append(row)

    colspan = len(tables[0]) if tables else 0
    bclazz = 'td-sm position-relative text-center w-20'

    return table(
        clazz='table-fixed border mt-3',
        hcols=[col(clazz='text-center', colspan=colspan)],
        bcols=[col(clazz=bclazz)] * colspan,
        head=[cell(content=title)],
        body=body)
