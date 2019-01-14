#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Service (reloadable) methods for displaying game data."""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/services/scoreboard', '', _path))

from common.datetime_.datetime_ import decode_datetime  # noqa
from common.datetime_.datetime_ import suffix  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import span  # noqa
from common.elements.elements import table  # noqa
from common.encyclopedia.encyclopedia import player_to_name_sub  # noqa
from common.teams.teams import encoding_to_abbreviation  # noqa
from common.teams.teams import encoding_to_hometown  # noqa
from common.teams.teams import encoding_to_hometown_sub  # noqa
from common.teams.teams import icon_absolute  # noqa


def line_score_body(data):
    """Creates a line score table body for a given game data object.

    The table body contains the teams, records, and runs for the game.

    Args:
        data: The parsed game data.

    Returns:
        A line score table body.
    """
    away_team = data['away_team']
    home_team = data['home_team']

    away_hometown = encoding_to_hometown(away_team)
    if data['away_record']:
        away_hometown += ' (' + data['away_record'] + ')'
    away_title = icon_absolute(away_team, away_hometown, '16')

    home_hometown = encoding_to_hometown(home_team)
    if data['home_record']:
        home_hometown += ' (' + data['home_record'] + ')'
    home_title = icon_absolute(home_team, home_hometown, '16')

    away_line = data['away_line'].split()
    home_line = data['home_line'].split()
    num = len(home_line)
    final = 'Final' + ('' if num == 9 else ' ({})'.format(num))

    hcols = [col(clazz='font-weight-bold text-danger')]
    hcols += [col(clazz='td-sm-none w-24p pr-1 pl-2 text-center')]
    hcols += [col(clazz='td-sm-none w-24p px-1 text-center')] * 7
    hcols += [col(clazz='td-sm-none w-28p pl-1 pr-2 text-center')]
    hcols += [col(clazz='font-weight-bold w-24p px-1 text-center')] * 3

    head_row = [cell(content=final)]
    head_row += [cell(content=str(i + 1)) for i in range(num - 9, num)]
    head_row += [cell(content=content) for content in ['R', 'H', 'E']]

    away_runs = data['away_runs']
    home_runs = data['home_runs']

    if int(away_runs) > int(home_runs):
        away_col = col(clazz='font-weight-bold')
        home_col = col()
    else:
        away_col = col()
        home_col = col(clazz='font-weight-bold')

    bc = 'td-sm-none text-center text-secondary'
    bcols = [col(clazz='position-relative')]
    bcols += [col(clazz=(bc + ' w-24p pr-1 pl-2'))]
    bcols += [col(clazz=(bc + ' w-24p px-1'))] * 7
    bcols += [col(clazz=(bc + ' w-28p pl-1 pr-2'))]
    bcols += [col(clazz='w-24p px-1 text-center')] * 3

    away_rhe = [data['away_runs'], data['away_hits'], data['away_errors']]
    home_rhe = [data['home_runs'], data['home_hits'], data['home_errors']]

    away_row = [cell(col=away_col, content=away_title)]
    home_row = [cell(col=home_col, content=home_title)]

    away_row += [cell(content=inning) for inning in away_line[num - 9:]]
    home_row += [cell(content=inning) for inning in home_line[num - 9:]]

    if num < 9:
        away_row += [cell() for _ in range(9 - num)]
        home_row += [cell() for _ in range(9 - num)]

    away_row += [cell(col=away_col, content=content) for content in away_rhe]
    home_row += [cell(col=home_col, content=content) for content in home_rhe]

    head = [head_row]
    body = [away_row, home_row]

    return table(
        clazz='border small',
        hcols=hcols,
        bcols=bcols,
        head=head,
        body=body,
    )


def line_score_foot(data):
    """Creates a line score table footer for a given game data object.

    The table footer contains game details, such as winning and losing pitcher.

    Args:
        data: The parsed game data.

    Returns:
        A line score table footer.
    """
    fcols = [col(clazz='border-0')]
    lines = []

    lines.append(span(['text-underline'], data['recap']))

    pitching = []
    if data['winning_pitcher']:
        s = '{} ({}, {} ERA)'.format(*(data['winning_pitcher'].split()))
        pitching.append(span(['font-weight-bold text-secondary'], 'W: ') + s)

    if data['losing_pitcher']:
        s = '{} ({}, {} ERA)'.format(*(data['losing_pitcher'].split()))
        pitching.append(span(['font-weight-bold text-secondary'], 'L: ') + s)

    if data['saving_pitcher']:
        s = '{} ({})'.format(*(data['saving_pitcher'].split()))
        pitching.append(span(['font-weight-bold text-secondary'], 'S: ') + s)

    lines.append(player_to_name_sub(', '.join(pitching)))

    batting = []
    for team in ['away', 'home']:
        if data[team + '_homeruns']:
            away_abbr = encoding_to_abbreviation(data[team + '_team'])
            away_homeruns = []
            for h in data[team + '_homeruns'].split(', '):
                p, n, total = h.split()
                if int(n) > 1:
                    p += ' ' + n
                away_homeruns.append('{} ({})'.format(p, total))
            s = ', '.join(away_homeruns)
            batting.append(span(['text-secondary'], away_abbr + ': ') + s)

    hr = span(['font-weight-bold text-secondary'], 'HR: ')
    hrs = ', '.join(batting) if batting else 'None'
    lines.append(player_to_name_sub(hr + hrs))

    return table(
        clazz='border border-top-0 small',
        fcols=fcols,
        foot=[[cell(content='<br>'.join(lines))]],
    )


def line_score_head(date):
    """Creates a line score table header for a given date.

    The table header contains the formatted date.

    Args:
        date: The encoded game date.

    Returns:
        A line score table header.
    """
    date = decode_datetime(date)
    title = date.strftime('%A, %B %-d{S}, %Y').replace('{S}', suffix(date.day))

    bcols = [col(clazz='font-weight-bold border-0')]
    body = [[cell(content=title)]]

    return table(
        clazz='small mt-2',
        bcols=bcols,
        body=body,
    )


def unofficial_score_body(scores):
    """Creates a line score table body for a list of unofficial scores.

    The table body contains the teams and runs for the games.

    Args:
        data: The list of unofficial scores.

    Returns:
        A line score table body.
    """
    hcols = [col(clazz='font-weight-bold text-secondary')]
    head = [[cell(content='Unofficial')]]

    body = []
    for score in scores:
        body.append([cell(content=encoding_to_hometown_sub(score))])

    return table(
        clazz='border small',
        hcols=hcols,
        head=head,
        body=body,
    )
