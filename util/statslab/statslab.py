#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/util/statslab', '', _path))
from util.datetime_.datetime_ import datetime_datetime_pst  # noqa
from util.datetime_.datetime_ import encode_datetime  # noqa
from util.team.team import decoding_to_encoding  # noqa
from util.team.team import decoding_to_encoding_sub  # noqa
from util.urllib_.urllib_ import urlopen  # noqa

_game_box_title = '<title>MLB Box Scores, (.+?) at (.+?), ' + \
                  '(\d{2}\/\d{2}\/\d{4})</title>'
_game_box_line = '<tr style=\"background-color:#FFFFFE;\">(.+?)</tr>'
_game_box_line_team = '<td class="dl">(?:<b>)?([^<]+)(?:</b>)?</td>'
_game_box_line_record = '([^(]+) \(([^)]+)\)'
_game_box_line_runs = '<td class="dc"><b>(\d+)</b></td>'
_game_log_game_title = '<title>(.+?) @ (.+?)</title>'
_game_log_date = '<div style="text-align:center; color:#000000; ' + \
                 'padding-top:4px;">(\d{2}\/\d{2}\/\d{4})</div>'
_game_log_player = '<a href="../players/player_(\d+).html">([^<]+)</a>'
_game_log_cell = '<table cellspacing="0" cellpadding="0" class="data" ' + \
                 'width="968px">(.+?)</table>'
_game_log_cell_id = '<th colspan="2" class="boxtitle">' + \
                       '(\w)[^\d]+(\d+?)\w+</th>'
_game_log_cell_intro = '<th colspan="2" align="left" ' + \
                       'style="padding:4px 0px 4px 4px;">(.+?)</th>'
_game_log_cell_outro = '<td class="datathbg" colspan="2">' + \
                       '[^-]+-  ([^;]+)[^<]+</td>'
_game_log_inner_left = '<td valign="top" width="268px" class="dl">(.+?)</td>'
_game_log_inner_right = '<td class="dl" width="700px">(.+?)</td>'
_game_log_outer = '(<td (?:valign="top" width="268px" class="dl"|' + \
                  'class="dl" width="700px")>.+?</td>)'
_player_title = '<title>Player Report for #\d+  ([^<]+)</title>'
_player_subtitle = '<div class="repsubtitle">(.+?)</div>'
_player_team = 'href=\"..\/teams\/team_\d{2}.html">([^<]+)</a>'


def _open(link):
    if link.startswith('http'):
        return urlopen(link).decode('iso-8859-1')
    if os.path.isfile(link):
        with open(link, 'r', encoding='iso-8859-1') as f:
            return f.read()
    return ''


def parse_box_score(link):
    ret = {'ok': False}

    content = _open(link)
    title = re.findall(_game_box_title, content, re.DOTALL)
    if not title:
        return dict(ret, error='invalid_title')

    away_title, home_title, date = title[0]
    away_team = decoding_to_encoding(away_title)
    home_team = decoding_to_encoding(home_title)
    d = datetime.datetime.strptime(date, '%m/%d/%Y')
    date = datetime_datetime_pst(d.year, d.month, d.day)
    if not away_team or not home_team:
        return dict(ret, error='invalid_title')

    lines = re.findall(_game_box_line, content, re.DOTALL)
    if len(lines) != 2:
        return dict(ret, error='invalid_line')

    teams = [re.findall(_game_box_line_team, line)[0] for line in lines]
    records = [re.findall(_game_box_line_record, line) for line in teams]
    if records[0] and records[1]:
        away_line = records[0][0][0]
        away_record = records[0][0][1]
        home_line = records[1][0][0]
        home_record = records[1][0][1]
    else:
        away_line = teams[0]
        away_record = ''
        home_line = teams[1]
        home_record = ''

    away_line = decoding_to_encoding(away_line)
    home_line = decoding_to_encoding(home_line)
    if away_line != away_team or home_line != home_team:
        return dict(ret, error='invalid_line')

    runs = [re.findall(_game_box_line_runs, line) for line in lines]
    if not runs[0] or not runs[1]:
        return dict(ret, error='invalid_line')

    away_runs = int(runs[0][0])
    home_runs = int(runs[1][0])

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


def parse_game_log(link):
    ret = {'ok': False}

    content = _open(link)

    game_title = re.findall(_game_log_game_title, content)
    if not game_title:
        return dict(ret, error='invalid_title')
    away_title, home_title = game_title[0]
    away_team = decoding_to_encoding(away_title)
    home_team = decoding_to_encoding(home_title)

    date = re.findall(_game_log_date, content)
    if not date:
        return dict(ret, error='invalid_date')
    d = datetime.datetime.strptime(date[0], '%m/%d/%Y')
    date = datetime_datetime_pst(d.year, d.month, d.day)

    player = {}
    for p in re.findall(_game_log_player, content):
        id_, name = p
        player['P' + id_] = name

    content = re.sub('</?b>', '', content)
    content = re.sub(r'(<a href="../players/player_)(\d+)(.html">[^<]+</a>)',
                     'P' + r'\2', content)
    content = decoding_to_encoding_sub(content)

    inning = []
    cell = re.findall(_game_log_cell, content, re.DOTALL)
    for c in cell:
        cell_id = re.findall(_game_log_cell_id, c)
        if not cell_id:
            return dict(ret, error='invalid_cell')
        cell_id = cell_id[0][0].lower() + cell_id[0][1]

        cell_intro = re.findall(_game_log_cell_intro, c, re.DOTALL)
        if not cell_intro:
            return dict(ret, error='invalid_cell')
        cell_intro = cell_intro[0].strip()

        cell_outro = re.findall(_game_log_cell_outro, c)
        if not cell_outro:
            return dict(ret, error='invalid_cell')
        cell_outro = cell_outro[0].strip()

        before = []
        pitch = []

        side = re.findall(_game_log_outer, c, re.DOTALL)
        for s in side:
            left = re.findall(_game_log_inner_left, s, re.DOTALL)
            right = re.findall(_game_log_inner_right, s, re.DOTALL)

            if left:
                before.append(left[0].strip())
            if right:
                for r in right[0].strip().split('<br>'):
                    if not r:
                        continue
                    if r[0].isdigit():
                        p = {'result': r}
                        if before:
                            p['before'] = before
                        pitch.append(p)
                        before = []
                    else:
                        p = pitch[-1]
                        if 'after' not in p:
                            p['after'] = []
                        p['after'].append(r)

        inning.append({
            'id': cell_id,
            'intro': cell_intro,
            'outro': cell_outro,
            'pitch': pitch
        })

    return {
        'away_team': away_team,
        'inning': inning,
        'date': encode_datetime(date),
        'home_team': home_team,
        'player': player,
        'ok': True
    }


def parse_player(link):
    ret = {'ok': False}

    content = _open(link)
    title = re.findall(_player_title, content)
    if not title:
        return dict(ret, error='invalid_title')

    name = title[0]

    subtitle = re.findall(_player_subtitle, content, re.DOTALL)
    if not subtitle:
        return dict(ret, error='invalid_team')

    team = re.findall(_player_team, subtitle[0])
    if not team:
        return dict(ret, error='invalid_team')

    team = decoding_to_encoding(team[0])

    return {'name': name, 'ok': True, 'team': team}
