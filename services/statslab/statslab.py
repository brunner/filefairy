#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Service (reloadable) methods for parsing StatsLab pages."""

import datetime
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/services/statslab', '', _path))

from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.datetime_.datetime_ import encode_datetime  # noqa
from common.json_.json_ import dumps  # noqa
from common.re_.re_ import find  # noqa
from common.requests_.requests_ import get  # noqa
from util.team.team import decoding_to_encoding_sub  # noqa


def _open(in_):
    if in_.startswith('http'):
        return get(in_)
    if os.path.isfile(in_):
        with open(in_, 'r', encoding='iso-8859-1') as f:
            return f.read()
    return ''


def parse_score(in_, out, date):
    """Parse a StatsLab box score into a task-readable format.

    If the box score is parsed successfully, the resulting data is written to a
    specified file and True is the returned value. Alternatively, if the box
    score is missing or does not match the given date, no JSON data is written
    and None is returned.

    Args:
        in_: The StatsLab box score link or file path.
        out: The file path to write the parsed data to.
        date: The encoded date that the box score is expected to match.

    Returns:
        True if the parse was successful, otherwise None.
    """
    text = decoding_to_encoding_sub(_open(in_))
    text = re.sub(r'<a href="../\w+/player_(\d+)\.[^<]+</a>', r'P\1', text)
    text = re.sub(r'</?b>', '', text)

    away, home, match = find(r'(\w+) at (\w+), (\d{2}\/\d{2}\/\d{4})', text)
    if not match:
        return None

    d = datetime.datetime.strptime(match, '%m/%d/%Y')
    parsed = encode_datetime(datetime_datetime_pst(d.year, d.month, d.day))
    if date is None:
        date = parsed
    elif date != parsed:
        return None

    data = {'away_team': away, 'date': date, 'home_team': home}

    for team in ['away', 'home']:
        i = data[team + '_team']
        line = find(r'(?s)<td class="dl">' + i + r'(.+?)</tr>', text)
        data[team + '_record'] = find(r'^\((\d+-\d+)\)', line)

        cols = [n for n in re.findall(r'>(\d+|X)<', line)]
        data[team + '_line'] = ' '.join(cols)

    for pitcher in ['winning', 'losing']:
        i = pitcher[0].upper()
        p, line = find(r'(?s)<td class="dl">(\w+) ' + i + r' (.+?)</tr>', text)

        record = find(r'^(\(\d+-\d+\))', line)
        era = find(r'>([^<]+)</td>$', line)
        data[pitcher + '_pitcher'] = ' '.join([p, record, era])

    p, saves = find(r'(?s)<td class="dl">(\w+) SV (\(\d+\))', text)
    data['saving_pitcher'] = ' '.join([p, saves]) if saves else ''

    data['ballpark'] = find(r'(?s)Ballpark:(.+?)<br>', text)

    with open(out, 'w') as f:
        f.write(dumps(data) + '\n')

    return True
