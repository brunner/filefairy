#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Service (reloadable) methods for displaying game data."""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/services/scoreboard', '', _path))

from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import span  # noqa
from common.elements.elements import table  # noqa
from common.teams.teams import encoding_to_hometown  # noqa
from common.teams.teams import icon_absolute  # noqa


def line_score(data):
    away_team = data['away_team']
    home_team = data['home_team']

    away_hometown = encoding_to_hometown(away_team)
    away_record = ' (' + data['away_record'] + ')'
    away_title = icon_absolute(away_team, away_hometown + away_record, '16')

    home_hometown = encoding_to_hometown(home_team)
    home_record = ' (' + data['home_record'] + ')'
    home_title = icon_absolute(home_team, home_hometown + home_record, '16')

    away_line = data['away_line'].split()
    home_line = data['home_line'].split()

    num = len(home_line)
    final = 'Final' + ('' if num == 9 else ' ({})'.format(num))

    hcols = [col(clazz='font-weight-bold text-danger')]
    hcols += [col(clazz='td-sm-none w-24p px-1 text-center')] * (num - 1)
    hcols += [col(clazz='td-sm-none w-28p pl-1 pr-2 text-center')]
    hcols += [col(clazz='font-weight-bold w-24p px-1 text-center')] * 3

    head = [cell(content=final)]
    head += [cell(content=str(i + 1)) for i in range(num)]
    head += [cell(content=content) for content in ['R', 'H', 'E']]

    away_runs = data['away_runs']
    home_runs = data['home_runs']

    if int(away_runs) > int(home_runs):
        away_col = col(clazz='font-weight-bold')
        home_col = col()
    else:
        away_col = col()
        home_col = col(clazz='font-weight-bold')

    bc = 'td-sm-none text-center text-secondary'
    bcols = [col(clazz='position-relative pr-4p')]
    bcols += [col(clazz=(bc + ' w-24p px-1'))] * (num - 1)
    bcols += [col(clazz=(bc + ' w-28p pl-1 pr-2'))]
    bcols += [col(clazz='w-24p px-1 text-center')] * 3

    away_rhe = [data['away_runs'], data['away_hits'], data['away_errors']]
    away_row = [cell(col=away_col, content=away_title)]
    away_row += [cell(content=inning) for inning in away_line]
    away_row += [cell(col=away_col, content=content) for content in away_rhe]

    home_rhe = [data['home_runs'], data['home_hits'], data['home_errors']]
    home_row = [cell(col=home_col, content=home_title)]
    home_row += [cell(content=inning) for inning in home_line]
    home_row += [cell(col=home_col, content=content) for content in home_rhe]

    body = [away_row, home_row]

    summary = [span(['text-secondary'], 'W: ') + data['winning_pitcher']]
    summary += [span(['text-secondary'], 'L: ') + data['losing_pitcher']]
    if data['saving_pitcher']:
        summary += [span(['text-secondary'], 'S: ') + data['saving_pitcher']]

    fcols = [col(colspan=(num + 4))]
    foot = [cell(content=(', '.join(summary)))]

    return table(
        clazz='table border mt-3 small',
        hcols=hcols,
        bcols=bcols,
        fcols=fcols,
        head=head,
        body=body,
        foot=foot,
    )
