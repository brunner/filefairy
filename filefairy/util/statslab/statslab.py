#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/util/box', '', _path))
from util.team.team import decoding_to_encoding  # noqa
from util.urllib_.urllib_ import urlopen  # noqa

_title = '<title>MLB Box Scores, (.+?) at (.+?), (\d{2}\/\d{2}\/\d{4})</title>'
_line = '<tr style=\"background-color:#FFFFFE;\">(.+?)</tr>'
_line_team = '<td class="dl">(?:<b>)?([^<]+)(?:</b>)?</td>'
_line_record = '([^(]+) \(([^)]+)\)'
_line_runs = '<td class="dc"><b>(\d+)</b></td>'


def _open(link):
    if link.startswith('http'):
        return urlopen(link).decode('iso-8859-1')
    if os.path.isfile(link):
        with open(link, 'r', encoding='iso-8859-1') as f:
            return f.read()
    return ''


def box_score(link):
    ret = {'ok': False}

    content = _open(link)
    title = re.findall(_title, content, re.DOTALL)
    if not title:
        return dict(ret, error='invalid_title')

    away_title, home_title, date = title[0]
    away_team = decoding_to_encoding(away_title)
    home_team = decoding_to_encoding(home_title)
    date = datetime.datetime.strptime(date, '%m/%d/%Y')
    if not away_team or not home_team:
        return dict(ret, error='invalid_title')

    lines = re.findall(_line, content, re.DOTALL)
    if len(lines) != 2:
        return dict(ret, error='invalid_line')

    line_teams = [re.findall(_line_team, line)[0] for line in lines]
    line_records = [re.findall(_line_record, line) for line in line_teams]
    if line_records[0] and line_records[1]:
        away_line = line_records[0][0][0]
        away_record = line_records[0][0][1]
        home_line = line_records[1][0][0]
        home_record = line_records[1][0][1]
    else:
        away_line = line_teams[0]
        away_record = ''
        home_line = line_teams[1]
        home_record = ''

    away_line = decoding_to_encoding(away_line)
    home_line = decoding_to_encoding(home_line)
    if away_line != away_team or home_line != home_team:
        return dict(ret, error='invalid_line')

    line_runs = [re.findall(_line_runs, line)[0] for line in lines]
    if not line_runs[0] or not line_runs[1]:
        return dict(ret, error='invalid_line')

    away_runs = int(line_runs[0])
    home_runs = int(line_runs[1])

    return {
        'away_record': away_record,
        'away_runs': away_runs,
        'away_team': away_team,
        'date': date,
        'home_record': home_record,
        'home_runs': home_runs,
        'home_team': home_team,
        'ok': True
    }
