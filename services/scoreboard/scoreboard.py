#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Service (reloadable) methods for displaying game data."""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/services/scoreboard', '', _path))

from common.datetime_.datetime_ import datetime_as_est  # noqa
from common.datetime_.datetime_ import datetime_replace  # noqa
from common.datetime_.datetime_ import decode_datetime  # noqa
from common.elements.elements import anchor  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import dialog  # noqa
from common.elements.elements import icon_span  # noqa
from common.elements.elements import row  # noqa
from common.elements.elements import span  # noqa
from common.elements.elements import table  # noqa
from common.elements.elements import topper  # noqa
from common.json_.json_ import loads  # noqa
from common.re_.re_ import search  # noqa
from common.record.record import decode_record  # noqa
from common.record.record import encode_record  # noqa
from common.reference.reference import player_to_shortname_sub  # noqa
from common.reference.reference import player_to_starter_sub  # noqa
from common.teams.teams import encoding_to_abbreviation  # noqa
from common.teams.teams import encoding_to_encodings  # noqa
from common.teams.teams import encoding_to_hometown  # noqa
from common.teams.teams import encoding_to_hometown_sub  # noqa
from common.teams.teams import icon_absolute  # noqa

GAMES_DIR = re.sub(r'/services/scoreboard', '/resources/games', _path)

STATSPLUS_LINK = 'https://statsplus.net/oblootp/reports/news/html'
STATSPLUS_BOX_SCORES = os.path.join(STATSPLUS_LINK, 'box_scores')


def _add_line_score(s, data, body, foot):
    for team in ['away', 'home']:
        e = data[team + '_team']
        if e not in s:
            s[e] = []
        s[e].append((data['date'], body, foot))


def _cell(text, attributes):
    text = span(classes=['align-middle', 'badge-icon-button'], text=text)
    attributes.update({'data-dismiss': 'modal'})
    return cell(content=span(classes=['badge', 'badge-icon', 'badge-light'],
                             text=text,
                             attributes=attributes))


def _date(date):
    return decode_datetime(date).strftime('%m%d')


def _location_row(data):
    date = datetime_as_est(decode_datetime(data['date']))
    start = date.strftime('%I:%M %p').lstrip('0')
    ballpark = ' at ' + data['ballpark']
    location = span(classes=['small', 'text-secondary'],
                    text=(start + ballpark))
    return row(cells=[cell(col=col(clazz='border-0 py-2'), content=location)])


def create_dialog(date, game):
    """Creates a dialog for showing a hidden game score.

    Args:
        date: The MMDD-formatted date of the game.
        game: The game id number.

    Returns:
        A dialog.
    """
    id_ = 'd{}g{}'.format(date, game)
    icon = icon_absolute('T30', 'Spoilers Hidden')

    t = 'Pending Games Only' if game == '0' else 'Selected Game Only'
    tables = [
        topper('Reveal Final Scores'),
        table(clazz='border mb-3',
              hcols=[col(clazz='font-weight-bold text-dark', colspan="2")],
              bcols=[
                  col(clazz='w-50 badge-icon-wrapper pl-2'),
                  col(clazz='w-50 badge-icon-wrapper pr-2')
              ],
              head=[row(cells=[cell(content='Options')])],
              body=[
                  row(cells=[
                      _cell('All Games for Today', {'data-show-date': date}),
                      _cell(t, {'data-show-game': game})
                  ])
              ])
    ]

    return dialog(id_=id_, icon=icon, tables=tables)


def line_score_hide_body(data):
    """Creates a hidden line score table body for a given game data object.

    The table body contains the teams for the game.

    Args:
        data: The parsed game data.

    Returns:
        A line score table body.
    """
    hcols = [
        col(clazz='font-weight-bold text-dark'),
        col(clazz='position-relative')
    ]
    bcols = [col(colspan="2", clazz='position-relative')]

    d, g = _date(data['date']), data['num']
    attr = {'data-toggle': 'modal', 'data-target': '#d{}g{}'.format(d, g)}
    span_ = icon_span(
        name='eye',
        classes=['hover', 'right', 'text-dark'],
        attributes=attr,
    )
    head = [row(cells=[cell(content='Warmup'), cell(content=span_)])]

    body = []
    for team, other in [('away', 'home'), ('home', 'away')]:
        encoding = data[team + '_team']
        text = encoding_to_hometown(encoding)
        title = icon_absolute(encoding, text)
        body.append(row(cells=[cell(content=title)]))

    attr = {'data-game': g, 'data-date': d}
    return table(
        clazz='border',
        attributes=attr,
        hcols=hcols,
        bcols=bcols,
        head=head,
        body=body,
    )


def line_score_hide_foot(data):
    """Creates a hidden line score table footer for a given game data object.

    The table footer contains game details, such as starting pitchers.

    Args:
        data: The parsed game data.

    Returns:
        A line score table footer.
    """
    lines = []

    head = anchor('/fairylab/gameday/' + data['num'] + '/', 'Watch Live')
    lines.append(head)

    # TODO: Remove events check after game log 404 error is fixed.
    if data['events']:
        pitching = []
        for team in ['away', 'home']:
            encoding = data[team + '_team']
            pitcher = data[team + '_pitcher']

            abbr = encoding_to_abbreviation(encoding)
            span_ = span(classes=['text-secondary'], text=(abbr + ': '))
            pitching.append(span_ + pitcher)

        sp = span(classes=['font-weight-bold text-secondary'], text='SP: ')
        sps = '&nbsp; '.join(pitching)
        lines.append(player_to_starter_sub(sp + sps))

    foot = [_location_row(data)]
    if lines:
        foot.append(row(cells=[cell(content='<br>'.join(lines))]))

    attributes = {'data-game': data['num'], 'data-date': _date(data['date'])}
    return table(
        clazz='border border-top-0 mb-3',
        attributes=attributes,
        foot=foot,
    )


def line_score_show_body(data, hidden=False):
    """Creates a shown line score table body for a given game data object.

    The table body contains the teams, records, and runs for the game.

    Args:
        data: The parsed game data.
        hidden: Whether to initially hide the table body.

    Returns:
        A line score table body.
    """
    num = len(data['home_line'].split())
    max_num = max(num, 9)
    final = 'Final' + ('' if num == 9 else ' ({})'.format(num))

    hcols = [col(clazz='font-weight-bold text-danger pr-3')]
    hcols += [col(clazz='td-lg-none w-24p px-1 text-center')] * 5
    hcols += [col(clazz='td-md-none w-24p px-1 text-center')] * 4
    hcols += [col(clazz='td-sm-none w-24p px-1 text-center')] * 8
    hcols += [col(clazz='td-sm-none w-28p pl-1 pr-2 text-center')]
    hcols += [col(clazz='font-weight-bold w-24p px-1 text-center')] * 2
    hcols += [col(clazz='font-weight-bold w-32p pl-1 text-center')]

    bc = 'text-center text-secondary'
    bcols = [col(clazz='position-relative pr-3')]
    bcols += [col(clazz=(bc + ' td-lg-none w-24p px-1'))] * 5
    bcols += [col(clazz=(bc + ' td-md-none w-24p px-1'))] * 4
    bcols += [col(clazz=(bc + ' td-sm-none w-24p px-1'))] * 8
    bcols += [col(clazz=(bc + ' td-sm-none w-28p pl-1 pr-2'))]
    bcols += [col(clazz='w-24p px-1 text-center')] * 2
    bcols += [col(clazz='w-32p pl-1 text-center')]

    head_cells = [cell(content=final)]
    head_cells += [cell() for _ in range(18 - max_num)]
    head_cells += [cell(content=str(i + 1)) for i in range(max_num)]
    head_cells += [cell(content=content) for content in ['R', 'H', 'E']]
    head = [row(cells=head_cells)]

    body = []
    for team, other in [('away', 'home'), ('home', 'away')]:
        encoding = data[team + '_team']
        record = data[team + '_record']
        win = int(data[team + '_runs']) > int(data[other + '_runs'])
        primary = col(clazz='font-weight-bold') if win else col()

        text = encoding_to_hometown(encoding)
        text += ' (' + record + ')' if record else ''
        title = icon_absolute(encoding, text)
        body_cells = [cell(col=primary, content=title)]

        rhe = [data[team + suff] for suff in ('_runs', '_hits', '_errors')]
        body_cells += [cell() for _ in range(18 - max_num)]
        body_cells += [cell(content=s) for s in data[team + '_line'].split()]
        body_cells += [cell() for _ in range(9 - num)]
        body_cells += [cell(col=primary, content=s) for s in rhe]

        body.append(row(cells=body_cells))

    clazz = 'border' + (' d-none' if hidden else '')
    attributes = {'data-game': data['num'], 'data-date': _date(data['date'])}
    return table(
        clazz=clazz,
        attributes=attributes,
        hcols=hcols,
        bcols=bcols,
        head=head,
        body=body,
    )


def line_score_show_foot(data, hidden=False):
    """Creates a shown line score table footer for a given game data object.

    The table footer contains game details, such as winning and losing pitcher.

    Args:
        data: The parsed game data.
        hidden: Whether to initially hide the table footer.

    Returns:
        A line score table footer.
    """
    lines = []

    head = anchor('/fairylab/gameday/' + data['num'] + '/', 'Watch Live')
    if data['recap']:
        span_ = span(classes=['text-underline'], text=data['recap'])
        head += ' &nbsp;|&nbsp; ' + span_
    lines.append(head)

    pitching = []
    for pitcher in ['winning', 'losing', 'saving']:
        encoding = data[pitcher + '_pitcher']
        if not encoding:
            continue

        pref = pitcher[0].upper() + ': '
        span_ = span(classes=['font-weight-bold text-secondary'], text=pref)
        s = '{} ({})'.format(*(encoding.split()))
        pitching.append(span_ + s)

    lines.append(player_to_shortname_sub('&nbsp; '.join(pitching)))

    batting = []
    for team in ['away', 'home']:
        if data[team + '_homeruns']:
            abbr = encoding_to_abbreviation(data[team + '_team'])
            homeruns = []
            for h in data[team + '_homeruns'].split(' '):
                p, n, total = h.split(',')
                if int(n) > 1:
                    p += ' ' + n
                homeruns.append('{} ({})'.format(p, total))
            span_ = span(classes=['text-secondary'], text=(abbr + ': '))
            s = ', '.join(homeruns)
            batting.append(span_ + s)

    hr = span(classes=['font-weight-bold text-secondary'], text='HR: ')
    hrs = '&nbsp; '.join(batting) if batting else 'None'
    lines.append(player_to_shortname_sub(hr + hrs))

    clazz = 'border border-top-0 mb-3' + (' d-none' if hidden else '')
    attributes = {'data-game': data['num'], 'data-date': _date(data['date'])}
    return table(
        clazz=clazz,
        attributes=attributes,
        foot=[
            _location_row(data),
            row(cells=[cell(content='<br>'.join(lines))]),
        ],
    )


def line_scores(nums, hidden=False):
    """Returns a dictionary of all line scores.

    If including hidden line scores, also return the necessary dialogs.

    Args:
        nums: The list of game numbers to include.
        hidden: Whether to include hidden line scores.

    Returns:
        A dictionary of line scores.
    """
    d = []
    s = {}
    for num in nums:
        data = loads(os.path.join(GAMES_DIR, num + '.json'))
        if hidden:
            d.append(create_dialog(_date(data['date']), data['num']))

            body = line_score_hide_body(data)
            foot = line_score_hide_foot(data)
            _add_line_score(s, data, body, foot)

        body = line_score_show_body(data, hidden=hidden)
        foot = line_score_show_foot(data, hidden=hidden)
        _add_line_score(s, data, body, foot)

    return {'dialogs': d, 'scores': s}


def pending_hide_body(date, scores):
    """Creates a hidden pending table body for a given list of pending scores.

    The table body contains the teams for the games.

    Args:
        date: The encoded date for the scores.
        scores: The list of pending scores.

    Returns:
        A line score table body.
    """
    hcols = [
        col(clazz='font-weight-bold text-dark'),
        col(clazz='position-relative')
    ]
    bcols = [col(clazz='position-relative', colspan="2")]

    d, g = _date(date), '0'
    attr = {'data-toggle': 'modal', 'data-target': '#d{}g{}'.format(d, g)}
    span_ = icon_span(
        name='eye',
        classes=['hover', 'right', 'text-dark'],
        attributes=attr,
    )
    head = [row(cells=[cell(content='Pending'), cell(content=span_)])]

    body = []
    for score in scores:
        t1, t2 = search(r'(\w+) \d+, (\w+) \d+', score)
        hometowns = [encoding_to_hometown(t) for t in (t1, t2)]
        text = icon_absolute('T30', ' · '.join(sorted(hometowns)))
        body.append(row(cells=[cell(content=text)]))

    attr = {'data-game': g, 'data-date': d}
    return table(
        clazz='border mb-3',
        attributes=attr,
        hcols=hcols,
        bcols=bcols,
        head=head,
        body=body,
    )


def pending_show_body(date, scores, hidden=False):
    """Creates a shown pending table body for a given list of pending scores.

    The table body contains the teams and runs for the games.

    Args:
        date: The encoded date for the scores.
        scores: The list of pending scores.
        hidden: Whether to initially hide the table body.

    Returns:
        A line score table body.
    """
    hcols = [col(clazz='font-weight-bold text-dark')]
    bcols = [col(clazz='position-relative')]

    head = [row(cells=[cell(content='Pending')])]

    body = []
    for score in scores:
        text = icon_absolute('T30', encoding_to_hometown_sub(score))
        body.append(row(cells=[cell(content=text)]))

    clazz = 'border mb-3' + (' d-none' if hidden else '')
    attributes = {'data-game': '0', 'data-date': _date(date)}
    return table(
        clazz=clazz,
        attributes=attributes,
        hcols=hcols,
        bcols=bcols,
        head=head,
        body=body,
    )


def pending_carousel(statsplus_scores, hidden=False):
    """Returns a dictionary of all pending scores, grouped for a carousel.

    If including hidden line scores, also return the necessary dialogs.

    Args:
        statsplus_scores: A mapping from date to a list of pending scores.
        hidden: Whether to include pending line scores.

    Returns:
        A dictionary of pending scores.
    """
    d = []
    s = {}
    for date in statsplus_scores:
        start = datetime_replace(date, hour=23, minute=59)
        scores = list(sorted(statsplus_scores[date].values()))

        value = []
        if hidden:
            d.append(create_dialog(_date(date), '0'))
            value.append((start, pending_hide_body(date, scores)))
        value.append((start, pending_show_body(date, scores, hidden=hidden)))

        s[date] = value

    return {'dialogs': d, 'scores': s}


def pending_dialog(statsplus_scores):
    """Returns a dictionary of all pending scores, grouped for a dialog.

    Args:
        statsplus_scores: A mapping from date to a list of pending scores.

    Returns:
        A dictionary of pending scores.
    """
    d = {}
    for date in statsplus_scores:
        scores = {}
        for s in sorted(statsplus_scores[date].values()):
            for t in search(r'(\w+) \d+, (\w+) \d+', s):
                if t not in scores:
                    scores[t] = []
                scores[t].append(s)

        for t in sorted(scores):
            body = pending_show_body(date, scores[t])
            for e in encoding_to_encodings(t):
                if e not in d:
                    d[e] = []
                d[e].append((date, body, None))

    return d
