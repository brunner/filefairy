#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
import random
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
_description_map = {
    'Flyball': ('flies out', 'fly ball'),
    'Groundball': ('grounds out', 'ground ball'),
    'Line Drive': ('lines out', 'line drive'),
    'Popup': ('pops out', 'pop up'),
}
_fielder_map = {
    '1': ('P', 'pitcher'),
    '2': ('C', 'catcher'),
    '3': ('1B', 'first baseman'),
    '4': ('2B', 'second baseman'),
    '5': ('3B', 'third baseman'),
    '6': ('SS', 'shortstop'),
    '7': ('LF', 'left fielder'),
    '8': ('CF', 'center fielder'),
    '9': ('RF', 'right fielder')
}
_homer_map = {
    '7': 'left field',
    '8': 'center field',
    '9': 'right field'
}


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
    check_outs = True
    outs, runs = 0, 0
    suffix = ''
    value_lower = value.lower()

    if any(s in value_lower
           for s in ['scores', 'home run', 'home, safe', 'is safe']):
        suffix = ', run(s)'
        if 'home run' in value_lower:
            if 'solo' in value_lower:
                runs = 1
            elif '2-run' in value_lower:
                runs = 2
            elif '3-run' in value_lower:
                runs = 3
            else:
                runs = 4
        else:
            runs = sum([
                value_lower.count(s)
                for s in ['scores', 'home, safe', 'is safe']
            ])
    elif any(s in value_lower for s in [
            'out', 'double play', 'lined into dp', 'first, dp',
            'fielders choice'
    ]):
        suffix = ', out(s)'
    elif sequence and 'In play' in sequence[-1]:
        check_outs = False
        suffix = ', no out'

    if check_outs:
        if any(s in value_lower
               for s in ['double play', 'lined into dp', 'first, dp']):
            outs = 2
        else:
            outs = sum([
                value_lower.count(s)
                for s in ['out', 'caught stealing', 'fielders choice']
            ])

    if sequence and 'In play' in sequence[-1]:
        sequence[-1] += suffix

    return {
        'type': 'event',
        'outs': outs,
        'runs': runs,
        'sequence': sequence,
        'value': value
    }


def _play_sub(subtype, value):
    return {'type': 'sub', 'subtype': subtype, 'value': value}


def _sequence(counts, value):
    return '{} {} {} {}'.format(*counts, value)


def _value(batting, values, during=False):
    if values:
        prefix = ('With {} batting, ' if during else '{} ').format(batting)
        values[0] = prefix + values[0]
    return ' '.join([v + ('.' if v[-1] != '!' else '') for v in values])


def parse_game_data(box_link, log_link):
    ret = {'ok': False, 'id': _find('log_(\d+)\.', log_link)}

    box_content = _open(box_link)
    title = re.findall(_game_box_title, box_content, re.DOTALL)
    if not title:
        return dict(ret, error='invalid_title')

    away_title, home_title, date = title[0]
    away_team = decoding_to_encoding(away_title)
    home_team = decoding_to_encoding(home_title)
    d = datetime.datetime.strptime(date, '%m/%d/%Y')
    date = datetime_datetime_pst(d.year, d.month, d.day)
    if not away_team or not home_team:
        return dict(ret, error='invalid_title')

    lines = re.findall(_game_box_line, box_content, re.DOTALL)
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

    fielders = {away_team: {}, home_team: {}}
    players = []
    regex = '"hsn dc">RBI</th>\s*</tr>(.+?)</table>'
    batting_linescores = re.findall(regex, box_content, re.DOTALL)

    for i, line in enumerate(batting_linescores):
        t = away_team if i == 0 else home_team
        regex = ('"dl"><a href="../players/player_(\d+).html">[^<]+</a>'
                 '([^<]+)</td>')
        for id_, pos in re.findall(regex, line):
            fielders[t][pos.strip().split(', ')[0]] = id_
            players.append(id_)

        regex = ('"dl">&#160;&#160;[^<]*<a href="../players/player_(\d+)'
                 '.html">')
        for id_ in re.findall(regex, line):
            players.append(id_)

    regex = '"hsn dc">ERA</th>\s*</tr>(.+?)</table>'
    pitching_linescores = re.findall(regex, box_content, re.DOTALL)

    regex = '<a href="../players/player_(\d+).html">'
    for line in pitching_linescores:
        t = away_team if i == 0 else home_team
        for i, id_ in enumerate(re.findall(regex, line)):
            if i == 0 and 'P' not in fielders[t]:
                fielders[t]['P'] = id_
            players.append(id_)

    players = list(sorted(set(players)))

    # try:
    plays = []
    if log_link:
        log_content = _open(log_link)

        away_title, home_title = _find('<title>(.+?) @ (.+?)</title>',
                                       log_content)
        away_team = decoding_to_encoding(away_title)
        home_team = decoding_to_encoding(home_title)

        date = _find('padding-top:4px;">(\d{2}\/\d{2}\/\d{4})</div>',
                     log_content)
        if not date:
            return ret

        d = datetime.datetime.strptime(date, '%m/%d/%Y')
        date = datetime_datetime_pst(d.year, d.month, d.day)

        log_content = re.sub('</?b>', '', log_content)
        log_content = re.sub('  ', ' ', log_content)
        log_content = re.sub(
            r'(<a href="../players/player_)(\d+)(.html">[^<]+</a>)',
            'P' + r'\2', log_content)
        log_content = decoding_to_encoding_sub(log_content)

        inning = []
        regex = 'class="data" width="968px">(.+?)</table>'
        for i, c in enumerate(re.findall(regex, log_content, re.DOTALL)):
            cell_label = _find('"boxtitle">(.+?)</th>', c, re.DOTALL)
            cell_label = '{}{} {}'.format(cell_label[0],
                                          cell_label[1:3].lower(),
                                          cell_label.split()[-1].lower())

            regex = 'style="padding:4px 0px 4px 4px;">(.+?) batting -'
            cell_batting = _find(regex, c, re.DOTALL)

            regex = 'Pitching for (\w+) : \w+ (.+?)</th>'
            fielding_team, cell_pitching = _find(regex, c, re.DOTALL)

            regex = 'span="2">[^-]+- ([^;]+); [^\d]+(\d+) - [^\d]+(\d+)</td>'
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
                    counts, sequence, values = [0, 0, 0], [], []
                    for part in r.split('<br>'):
                        if not part:
                            continue
                        value = _find('^\d-\d: (.+?)$', part, re.DOTALL)
                        if value:
                            counts[0] += 1
                            if values:
                                play.append(
                                    _play_event(
                                        sequence,
                                        _value(batting, values, during=True)))
                                sequence, values = [], []
                            _parse_value(value, counts, sequence, values,
                                         fielders[fielding_team])
                        else:
                            values.append(part + '*')
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
        'away_record': away_record,
        'away_runs': away_runs,
        'away_team': away_team,
        'home_record': home_record,
        'home_runs': home_runs,
        'home_team': home_team,
        'date': encode_datetime(date),
        'players': players,
        'plays': plays,
    })
    # except:
    #     pass

    return ret


def _description(category, index):
    desc = _description_map.get(category)
    return desc[index] if desc else ''


def _fielder(num, fielders):
    pos, title = _fielder_map.get(num, ('', ''))
    return title + ' P' + fielders.get(pos, '')


def _location(zone, index):
    if index == 0:
        if '1' in zone or 'P' in zone:
            return '1'
        if '2' in zone:
            return '2'
        if '3' in zone:
            return '3'
        if '5' in zone:
            return '5'
        if '4' in zone:
            return '4'
        return '6'
    else:
        if '8' in zone or 'M' in zone:
            return '8'
        if '3' in zone or '4' in zone or '9' in zone:
            return '9'
        return '7'


def _parse_value(value, counts, sequence, values, fielders):
    if _find('Base on Balls', value):
        counts[1] += 1
        sequence.append(_sequence(counts, 'Ball'))
        values.append('walks')
        return

    if _find('Strikes out swinging', value):
        counts[2] += 1
        sequence.append(_sequence(counts, 'Swinging Strike'))
        values.append('strikes out swinging')
        return

    if _find('Strikes out looking', value):
        counts[2] += 1
        sequence.append(_sequence(counts, 'Called Strike'))
        values.append('called out on strikes')
        return

    if _find('Bunted foul|Bunt missed!', value):
        counts[2] += 1
        sequence.append(_sequence(counts, 'Missed Bunt'))
        if _find('Strikeout', value):
            values.append('strikes out on a missed bunt')
        return

    if _find('Foul Ball', value):
        counts[2] = min(2, counts[2] + 1)
        sequence.append(_sequence(counts, 'Foul'))
        return

    if _find('Strike', value):
        counts[2] += 1
        sequence.append(_sequence(counts, value))
        return

    if _find('Ball', value):
        counts[1] += 1
        sequence.append(_sequence(counts, value))
        return

    num, category, zone = _find('Fly out, F(\d) \(([^,]+), (\w+)\)', value)
    if num:
        sequence.append(_sequence(counts, 'In play'))
        field = _fielder(num, fielders)
        desc = _description(category, 0)
        values.append('{} to {} (zone {})'.format(desc, field, zone))
        return

    nums, zone = _find('Ground out,? ([^\s]+) \(Groundball, (\w+)\)', value)
    if nums:
        sequence.append(_sequence(counts, 'In play'))
        nums = nums.replace('U', '').split('-')
        f = [_fielder(num, fielders) for num in nums]
        fields = ' to ' + f[0] if len(f) == 1 else ', ' + ' to '.join(f)
        values.append('grounds out{} (zone {})'.format(fields, zone))
        return

    hit = '(SINGLE|DOUBLE|TRIPLE)'
    hit, category, zone = _find(hit + ' \(([^,]+), (\w+)\)', value)
    if hit:
        sequence.append(_sequence(counts, 'In play'))
        hit = hit.lower() + 's'
        desc = _description(category, 1)
        index = 0 if _find('infield hit', value) else 1
        field = _fielder(_location(zone, index), fielders)
        values.append('{} on a {} to {} (zone {})'.format(
            hit, desc, field, zone))
        return

    # category, zone, dist = _find('HOME RUN \(([^,]+), (\w+)\), '
    #                              'Distance : (\d+) ft', value)
    # if category:
    #     sequence.append(_sequence(counts, 'In play'))
    #     desc = _description(category, 1)
    #     index = 0 if _find('infield hit', value) else 1
    #     homer = _homer_map.get(_location(zone, index), '')
    #     values.append('homers on a {} to {} (zone {}, {} ft)'.format(
    #         desc, homer, zone, dist))
    #     return

    sequence.append(_sequence(counts, 'In play'))
    values.append(value + '*')


def parse_player(link):
    ret = {'ok': False}

    content = _open(link)
    number, name = _find('Player Report for #(\d+)  ([^<]+)</title>', content)
    name = re.sub(' \'[^\']+\' ', ' ', name)
    subtitle = _find('class="repsubtitle">(.+?)</div>', content, re.DOTALL)
    team = _find('href=\"..\/teams\/team_\d{2}.html">([^<]+)</a>', subtitle)
    bats, throws = _find('Bats: (\w)[^T]+Throws: (\w)', content)

    ret.update({
        'ok': True,
        'bats': bats,
        'name': name,
        'number': number,
        'team': decoding_to_encoding(team),
        'throws': throws
    })

    return ret
