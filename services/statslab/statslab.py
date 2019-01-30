#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Service (reloadable) methods for parsing StatsLab pages."""

import logging
import datetime
import os
import re
import sys

_logger = logging.getLogger('filefairy')
_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/services/statslab', '', _path))

from common.datetime_.datetime_ import datetime_as_est  # noqa
from common.datetime_.datetime_ import datetime_as_pst  # noqa
from common.datetime_.datetime_ import datetime_datetime_est  # noqa
from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.datetime_.datetime_ import encode_datetime  # noqa
from common.json_.json_ import dumps  # noqa
from common.re_.re_ import search  # noqa
from common.re_.re_ import findall  # noqa
from common.re_.re_ import match  # noqa
from common.reference.reference import put_players  # noqa
from common.requests_.requests_ import get  # noqa
from common.service.service import call_service  # noqa
from common.teams.teams import decoding_to_encoding_sub  # noqa
from common.teams.teams import encoding_to_hometown  # noqa
from data.event.event import Event  # noqa


def _open(in_):
    text = ''
    if in_.startswith('http'):
        text = get(in_)
    elif os.path.isfile(in_):
        with open(in_, 'r', encoding='iso-8859-1') as f:
            text = f.read()

    text = decoding_to_encoding_sub(text)
    text = re.sub(r'<a href="../\w+/player_(\d+)\.[^<]+</a>', r'P\1', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'</?b>', '', text)
    text = re.sub(r' &nbsp;&nbsp;', '', text)

    return text


def _parse_innings(text, html):
    regex = r'(?s)(\w+) batting - Pitching for (\w+) : \w+ (\w+)(.+?)'
    if html:
        regex += r'</table>'
    else:
        regex += r'\[%T\]'
        text += '[%T]'

    return findall(regex, text)


def _parse_lines(content, html):
    lines = []
    if html:
        regex = (r'(?s)<td valign="top" width="268px" class="dl">(.+?)</td> <t'
                 r'd class="dl" width="700px">(.+?)</td>')
        for left, right in findall(regex, content):
            lines.append(left)
            for r in right.split('<br>'):
                lines.append(r)
    else:
        lines += findall(r'(?s)[BN]\](.+?)\[%', content + '[%T]')

    return list(filter(bool, lines))


def parse_player(link):
    """Parse a StatsLab player page into a reference-readable format.

    Args:
        link: The StatsLab player page link.

    Returns:
        A data string if the parse was successful, otherwise None.
    """
    text = _open(link)
    number, name = search(r'Player Report for #(\d+) ([^<]+)</title>', text)
    if not number:
        return None
    name = re.sub(r' \'[^\']+\' ', r' ', name)
    subtext = search(r'(?s)class="repsubtitle">(.+?)</div>', text)
    if not subtext:
        return None

    team = search(r'href=\"..\/teams\/team_\d{2}.html">(\w+)</a>', subtext)
    if not team:
        team = 'T??'
    bats, throws = search(r'Bats: (\w)[^T]+Throws: (\w)', text)
    data = [team, number, bats, throws, name]

    if not all(data):
        return None

    return ' '.join(data)


def parse_game(box_in, log_in, out, date):
    """Parse a StatsLab box score and game log into a task-readable format.

    If the game is parsed successfully, the resulting data is written to a
    specified file and True is the returned value. Alternatively, if the game
    is missing or does not match the given date, no JSON data is written and
    None is returned.

    Args:
        box_in: The StatsLab box score link or file path.
        log_in: The StatsLab game log link or file path.
        out: The file path to write the parsed data to.
        date: The encoded date that the game is expected to match.

    Returns:
        True if the parse was successful, otherwise None.
    """
    box_text = _open(box_in)
    away, home, s = search(r'(\w+) at (\w+), (\d{2}\/\d{2}\/\d{4})', box_text)
    if not s:
        return None

    d = datetime.datetime.strptime(s, '%m/%d/%Y')
    d = datetime_datetime_pst(d.year, d.month, d.day)
    if date is not None and date != encode_datetime(d):
        return None

    t = search(r'(?s)Start Time:(.+?)<br>', box_text).strip(' EST')
    s = datetime.datetime.strptime(t.upper(), '%I:%M %p')

    d = datetime_as_est(d)
    date = datetime_datetime_est(d.year, d.month, d.day, s.hour, s.minute)
    date = encode_datetime(datetime_as_pst(date))

    day = d.weekday()
    home_fargs = (home, day, 'home', None)
    home_colors = call_service('uniforms', 'jersey_colors', home_fargs)
    away_fargs = (away, day, 'away', home_colors[0])
    away_colors = call_service('uniforms', 'jersey_colors', away_fargs)

    away_colors = ' '.join(away_colors)
    home_colors = ' '.join(home_colors)

    data = {
        'away_colors': away_colors,
        'away_team': away,
        'date': date,
        'home_colors': home_colors,
        'home_team': home,
    }

    for team in ['away', 'home']:
        i = data[team + '_team']
        line = search(r'(?s)<td class="dl">' + i + r'(.+?)</tr>', box_text)
        data[team + '_record'] = search(r'^\((\d+-\d+)\)', line)

        cols = findall(r'>(\d+|X)<', line)
        if not cols:
            cols = ['0', '0', '0']
        for suffix in ['_errors', '_hits', '_runs']:
            data[team + suffix] = cols.pop(-1)
        data[team + '_line'] = ' '.join(cols)

    data['recap'] = search(
        r'(?s)<!--RECAP_SUBJECT_START-->(.+?)<!--RECAP_SUBJECT_END-->',
        box_text)

    blines = findall(r'(?s)>RBI</th>\s*</tr>(.+?)</table>', box_text)
    plines = findall(r'(?s)>ERA</th>\s*</tr>(.+?)</table>', box_text)
    if len(blines) != 2 or len(plines) != 2:
        return None

    encodings = set()
    for line in (plines + blines):
        encodings.update(findall(r'>(P\d+) ', box_text))
    put_players(list(sorted(encodings)))

    batting = findall(r'(?s)BATTING<br>(.+?)</table>', box_text)
    if len(batting) != 2:
        return None

    for team, btext in zip(['away', 'home'], batting):
        homeruns = []
        container = search(r'(?s)Home Runs:(.+?)<br>', btext)
        if container:
            container = re.sub(r'\s+', ' ', container)
            for s in container.split(') '):
                p, n, total = search(r'^(\w+)(?:\s(\d+))?\s\((\d+),', s)
                if not n:
                    n = '1'
                homeruns.append(' '.join([p, n, total]))
        data[team + '_homeruns'] = ', '.join(homeruns)

    for pitcher in ['winning', 'losing']:
        i = pitcher[0].upper()
        p, line = search(r'(?s)<td class="dl">(\w+) ' + i + r' (.+?)</tr>',
                         box_text)

        record = search(r'^\((\d+-\d+)\)', line)
        era = search(r'>([^<]+)</td>$', line)
        data[pitcher + '_pitcher'] = ' '.join([p, record, era])

    p, saves = search(r'(?s)<td class="dl">(\w+) SV \((\d+)\)', box_text)
    data['saving_pitcher'] = ' '.join([p, saves]) if saves else ''
    data['ballpark'] = search(r'(?s)Ballpark:(.+?)<br>', box_text)

    html = log_in.endswith('html')
    log_text = _open(log_in)

    away_pitcher = search(r'Pitching for ' + away + r' : \w+ (\w+)', log_text)
    home_pitcher = search(r'Pitching for ' + home + r' : \w+ (\w+)', log_text)
    if away_pitcher is None or home_pitcher is None:
        return None

    events = []
    events_map = call_service('events', 'get_map', ())
    for inning in _parse_innings(log_text, html):
        events.append(Event.CHANGE_INNING.encode())

        batting, pitching, pitcher, content = inning
        for line in _parse_lines(content, html):
            for event, regex in events_map.items():
                groups = match(regex, line)
                if groups is not None:
                    events.append(event.encode(*groups))
                    break
            else:
                s = log_in.rsplit('/', 1)[1] + ' ' + line
                _logger.log(logging.INFO, s)
                return None

    data['away_pitcher'] = away_pitcher
    data['home_pitcher'] = home_pitcher
    data['events'] = events

    with open(out, 'w') as f:
        f.write(dumps(data) + '\n')

    return True
