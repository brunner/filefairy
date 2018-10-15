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
_player_title = '<title>Player Report for #\d+  ([^<]+)</title>'
_player_subtitle = '<div class="repsubtitle">(.+?)</div>'
_player_team = 'href=\"..\/teams\/team_\d{2}.html">([^<]+)</a>'


def _find(regex, text, flags=0):
    groups = re.compile(regex).groups
    match = re.findall(regex, text, flags)
    if groups > 1:
        return [m.strip() for m in match[0]] if match else [''] * groups
    return match[0].strip() if match else ''


def _open(link):
    if link.startswith('http'):
        return urlopen(link).decode('iso-8859-1')
    if os.path.isfile(link):
        with open(link, 'r', encoding='iso-8859-1') as f:
            return f.read()
    return ''


def _play_event(sequence, value):
    if sequence and 'In play' in sequence[-1]:
        value_lower = value.lower()
        if any(s in value_lower for s in ['scores', 'home run', 'home, safe']):
            suffix = ', run(s)'
        elif any(s in value_lower
                 for s in ['out', 'double play', 'fielders choice']):
            suffix = ', out(s)'
        else:
            suffix = ', no out'
        sequence[-1] += suffix
    return {'type': 'event', 'sequence': sequence, 'value': value}


def _play_sub(subtype, value):
    return {'type': 'sub', 'subtype': subtype, 'value': value}


def _value(batting, values, during=False):
    if values:
        values0 = ('With {} batting, ' if during else '{} ').format(batting)
        for i, v in enumerate(values[0]):
            if v.isupper() or v.isspace():
                values0 += v.lower()
            else:
                values0 += values[0][i:]
                break
        values[0] = values0
    return ' '.join([v + ('.' if v[-1] != '!' else '') for v in values])


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
    ret = {'ok': False, 'id': _find('log_(\d+)\.', link)}

    # try:
    content = _open(link)

    away_title, home_title = _find('<title>(.+?) @ (.+?)</title>', content)
    away_team = decoding_to_encoding(away_title)
    home_team = decoding_to_encoding(home_title)

    date = _find('padding-top:4px;">(\d{2}\/\d{2}\/\d{4})</div>', content)
    d = datetime.datetime.strptime(date, '%m/%d/%Y')
    date = datetime_datetime_pst(d.year, d.month, d.day)

    player = {}
    regex = '<a href="../players/player_(\d+).html">([^<]+)</a>'
    for (
            id_,
            name,
    ) in re.findall(regex, content):
        player['P' + id_] = name

    content = re.sub('</?b>', '', content)
    content = re.sub('  ', ' ', content)
    content = re.sub(r'(<a href="../players/player_)(\d+)(.html">[^<]+</a>)',
                     'P' + r'\2', content)
    content = decoding_to_encoding_sub(content)

    inning = []
    plays = []
    regex = 'class="data" width="968px">(.+?)</table>'
    for i, c in enumerate(re.findall(regex, content, re.DOTALL)):
        cell_label = _find('"boxtitle">(.+?)</th>', c, re.DOTALL)
        cell_label = '{}{} {}'.format(cell_label[0], cell_label[1:3].lower(),
                                      cell_label.split()[-1].lower())

        regex = 'style="padding:4px 0px 4px 4px;">(.+?) batting -'
        cell_batting = _find(regex, c, re.DOTALL)

        regex = 'Pitching for \w+ : (.+?)</th>'
        cell_pitching = _find(regex, c, re.DOTALL)

        regex = 'colspan="2">[^-]+- ([^;]+); [^\d]+(\d+) - [^\d]+(\d+)</td>'
        cell_footer = re.findall(regex, c)
        if cell_footer:
            m = list(cell_footer[0]) + [away_team, home_team]
            cell_footer = '{0}; {3} {1} - {4} {2}'.format(*m)
        else:
            cell_footer = ''

        play = []
        pitching, batting = '', ''
        left = 'valign="top" width="268px" class="dl"'
        right = 'class="dl" width="700px"'
        regex = '(<td (?:{}|{})>.+?</td>)'
        side = re.findall(regex.format(left, right), c, re.DOTALL)
        for s in side:
            regex = '<td {}>(.+?)</td>'
            l = _find(regex.format(left), s, re.DOTALL)
            r = _find(regex.format(right), s, re.DOTALL)
            if l:
                pitching = _find('Pitching: \w+ (\w+)', l)
                batting = _find('(?:Batting|Hitting): \w+ (\w+)', l)
                if pitching:
                    play.append(_play_sub('pitching', pitching))
                elif batting:
                    play.append(_play_sub('batting', batting))
                else:
                    play.append(_play_sub('other', l))
            elif r:
                sequence, values = [], []
                for part in r.split('<br>'):
                    if not part:
                        continue
                    value = _find('^\d-\d: (.+?)$', part, re.DOTALL)
                    if value:
                        if values:
                            play.append(
                                _play_event(
                                    sequence,
                                    _value(batting, values, during=True)))
                            sequence, values = [], []
                        if _find('Base on Balls', value):
                            sequence.append(
                                part.replace('Base on Balls', 'Ball'))
                            values.append(value)
                        elif _find('Strikes out swinging', value):
                            sequence.append(
                                part.replace('Strikes out swinging',
                                             'Swinging Strike'))
                            values.append(value)
                        elif _find('Strikes out looking', value):
                            sequence.append(
                                part.replace('Strikes out looking',
                                             'Called Strike'))
                            values.append('Called out on strikes')
                        elif _find('Ball|Strike|Bunted foul', value):
                            sequence.append(
                                part.replace(' Ball, location: 2F', ''))
                        else:
                            sequence.append(part.replace(value, 'In play'))
                            values.append(value)
                    else:
                        values.append(part)
                if sequence or values:
                    play.append(
                        _play_event(sequence,
                                    _value(batting, values, during=False)))

        inning.append({
            'label': cell_label,
            'batting': cell_batting,
            'pitching': cell_pitching,
            'footer': cell_footer,
            'play': play
        })

        if i % 2 != 0:
            plays.append(inning)
            inning = []

    if inning:
        plays.append(inning)

    ret.update({
        'ok': True,
        'away_team': away_team,
        'home_team': home_team,
        'date': encode_datetime(date),
        'player': player,
        'plays': plays,
    })
    # except:
    #     pass

    return ret


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
