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
from common.re_.re_ import findall  # noqa
from common.re_.re_ import match  # noqa
from common.re_.re_ import search  # noqa
from common.reference.reference import put_players  # noqa
from common.requests_.requests_ import get  # noqa
from common.service.service import call_service  # noqa
from common.teams.teams import decoding_to_encoding_sub  # noqa
from common.teams.teams import encoding_to_hometown  # noqa
from types_.event.event import Event  # noqa


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
    text = re.sub(r' &#xA0;&#xA0;', '', text)

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
        team = 'T30'
    bats, throws = search(r'Bats: (\w)[^T]+Throws: (\w)', text)
    data = [team, number, bats, throws, name]

    if not all(data):
        return None

    return ' '.join(data)


def parse_game(box_in, log_in, out, date):
    """Parse a StatsLab box score and game log into a task-readable format.

    If the game is parsed successfully, the resulting data is written to a
    specified file and also returned to the caller. Alternatively, if the game
    is missing or does not match the given date, no JSON data is written and
    None is returned.

    Args:
        box_in: The StatsLab box score link or file path.
        log_in: The StatsLab game log link or file path.
        out: The file path to write the parsed data to.
        date: The encoded date that the game is expected to match.

    Returns:
        The game data if the parse was successful, otherwise None.
    """
    num = search(r'game_box_(\d+)\.html', box_in)
    if not num:
        return None

    box_text = _open(box_in)
    away, home, s = search(r'(\w+) at (\w+), (\d{2}\/\d{2}\/\d{4})', box_text)
    if not s:
        return None

    d = datetime.datetime.strptime(s, '%m/%d/%Y')
    d = datetime_datetime_pst(d.year, d.month, d.day)
    if date is not None and date != encode_datetime(d):
        return None

    t = search(r'(?s)Start Time:(.+?)<br>', box_text)
    if not t:
        return None
    s = datetime.datetime.strptime(t.strip(' EST').upper(), '%I:%M %p')

    d = datetime_as_est(d)
    date = datetime_datetime_est(d.year, d.month, d.day, s.hour, s.minute)
    date = encode_datetime(datetime_as_pst(date))

    data = {
        'away_team': away,
        'date': date,
        'home_team': home,
        'num': num,
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

    regex = r'(?s)<!--RECAP_SUBJECT_START-->(.+?)<!--RECAP_SUBJECT_END-->'
    data['recap'] = search(regex, box_text)

    blines = findall(r'(?s)>RBI</th>\s*</tr>(.+?)</table>', box_text)
    plines = findall(r'(?s)>ERA</th>\s*</tr>(.+?)</table>', box_text)
    if len(blines) != 2 or len(plines) != 2:
        return None

    regex = r'([\s>-])(P\d+) ([^<]+)</td>'
    regex += (r'\s*<td class="dc">(\d+)</td>' * 6)
    for team, bline in zip(['away', 'home'], blines):
        batting = []
        bench = []
        prev = ''
        for line in findall(regex, bline):
            delim, player, pos, ab, r, h, rbi, bb, k = line
            pos = pos.replace(' ', '')
            stats = ','.join([ab, r, h, rbi, bb, k])
            if delim == '>':
                batting.append(' '.join([player, pos, stats]))
            else:
                bench.append(' '.join([player, pos, stats, prev]))
            prev = player
        data[team + '_batting'] = batting
        data[team + '_bench'] = bench

    regex = r'(P\d+)[^<]+</td>' + (r'\s*<td class="dc">([\d.]+)</td>' * 6)
    for team, pline in zip(['away', 'home'], plines):
        pitching = []
        for line in findall(regex, pline):
            player, ip, h, r, er, bb, k = line
            stats = ','.join([ip, h, r, er, bb, k])
            pitching.append(player + ' ' + stats)
        data[team + '_pitching'] = pitching

    encodings = set()
    encodings.update(findall(r'>(P\d+) ', box_text))
    put_players(list(sorted(encodings)))

    bdetails = findall(r'(?s)BATTING<br>(.+?)</table>', box_text)
    if len(bdetails) != 2:
        return None
    for team, btext in zip(['away', 'home'], bdetails):
        homeruns = []
        container = search(r'(?s)Home Runs:(.+?)<br>', btext)
        if container:
            container = re.sub(r'\s+', ' ', container)
            for s in container.split(') '):
                p, n, total = search(r'^(\w+)(?:\s(\d+))?\s\((\d+),', s)
                if not n:
                    n = '1'
                homeruns.append(','.join([p, n, total]))
        data[team + '_homeruns'] = ' '.join(homeruns) if homeruns else None

    for pitcher in ['winning', 'losing']:
        i = pitcher[0].upper()
        p, line = search(r'(?s)<td class="dl">(\w+) ' + i + r' (.+?)</tr>',
                         box_text)

        record = search(r'^\((\d+-\d+)\)', line)
        data[pitcher + '_pitcher'] = ' '.join([p, record])

    p, saves = search(r'(?s)<td class="dl">(\w+) SV \((\d+)\)', box_text)
    data['saving_pitcher'] = ' '.join([p, saves]) if saves else ''
    data['ballpark'] = search(r'(?s)Ballpark:(.+?)<br>', box_text)

    html = log_in.endswith('html')
    log_text = _open(log_in)

    away_pitcher = search(r'Pitching for ' + away + r' : \w+ (\w+)', log_text)
    home_pitcher = search(r'Pitching for ' + home + r' : \w+ (\w+)', log_text)

    data['away_pitcher'] = away_pitcher
    data['home_pitcher'] = home_pitcher

    events = []
    events_map = call_service('events', 'get_map', ())
    for inning in _parse_innings(log_text, html):
        batting, pitching, pitcher, content = inning
        lines = _parse_lines(content, html)
        for i, line in enumerate(lines):
            for event, regex in events_map.items():
                groups = match(regex, line)
                if groups is not None:
                    events.append(event.encode(*groups))
                    break
            else:
                events.append(Event.SPECIAL.encode('<br>'.join(lines[i:])))
                _logger.log(logging.DEBUG, '\n'.join([log_in, line]))
                break

        regex = r'left on base; [^\d]+(\d+) - [^\d]+(\d+)'
        away_inning, home_inning = search(regex, content)
        if away_inning:
            events.append(Event.CHANGE_INNING.encode(away_inning, home_inning))

    data['events'] = events

    day = d.weekday()
    home_fargs = (home, day, 'home', None)
    home_colors = call_service('uniforms', 'jersey_colors', home_fargs)
    away_fargs = (away, day, 'away', home_colors[0])
    away_colors = call_service('uniforms', 'jersey_colors', away_fargs)

    data['away_colors'] = ' '.join(away_colors)
    data['home_colors'] = ' '.join(home_colors)

    data['injuries'] = {}
    for player, injury in findall(r'(P\d+) was injured ([^.]+)', box_text):
        data['injuries'][player] = injury

    with open(out, 'w') as f:
        f.write(dumps(data) + '\n')

    return data

# from common.datetime_.datetime_ import datetime_now
# from common.jinja2_.jinja2_ import env
# from common.reference.reference import set_reference
# from common.service.service import reload_service_for_test
# from impl.reference.reference import Reference

# date = datetime_now()
# e = env()

# reference = Reference(date=date, e=e)
# set_reference(reference)

# reload_service_for_test('events')
# reload_service_for_test('roster')
# reload_service_for_test('state')
# reload_service_for_test('tables')
# reload_service_for_test('livesim')
# reload_service_for_test('scoreboard')
# reload_service_for_test('uniforms')

# CONTAINING_DIR = re.sub(r'/services/statslab', '/resource/extract', _path)
# BOX_SCORES_DIR = os.path.join(CONTAINING_DIR, 'box_scores')
# GAME_LOGS_DIR = os.path.join(CONTAINING_DIR, 'game_logs')
# GAMES_DIR = re.sub(r'/services/statslab', '/resource/games', _path)

# box_in = os.path.join(BOX_SCORES_DIR, 'game_box_24969.html')
# log_in = os.path.join(GAME_LOGS_DIR, 'log_24969.txt')
# out = os.path.join(GAMES_DIR, '24969.json')
# date = encode_datetime(datetime_datetime_pst(2025, 9, 28))
# parse_game(box_in, log_in, out, None)
