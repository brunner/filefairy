#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import logging
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

logger_ = logging.getLogger('fairylab')

_game_box_title = '<title>MLB Box Scores, (.+?) at (.+?), ' + \
                  '(\d{2}\/\d{2}\/\d{4})</title>'
_game_box_line = '<tr style=\"background-color:#FFFFFE;\">(.+?)</tr>'
_game_box_line_team = '<td class="dl">(?:<b>)?([^<]+)(?:</b>)?</td>'
_game_box_line_record = '([^(]+) \(([^)]+)\)'
_game_box_line_runs = '<td class="dc"><b>(\d+)</b></td>'
_bases_map = {
    'SINGLE': 0,
    'first': 0,
    'DOUBLE': 1,
    'second': 1,
    'TRIPLE': 2,
    'third': 2,
    'scores': 3,
    'home': 3
}
_batting_map = {
    0: '1st',
    1: '2nd',
    2: '3rd',
    3: '4th',
    4: '5th',
    5: '6th',
    6: '7th',
    7: '8th',
    8: '9th'
}
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
_homer_map = {'7': 'left field', '8': 'center field', '9': 'right field'}
_sub_map = {
    'PH': ('Pinch-hitter', ''),
    'PR': ('Pinch-runner', ''),
    'P': ('pitcher', 'pitcher'),
    'C': ('catcher', 'catcher'),
    '1B': ('first baseman', 'first base'),
    '2B': ('second baseman', 'second base'),
    '3B': ('third baseman', 'third base'),
    'SS': ('shortstop', 'shortstop'),
    'LF': ('left fielder', 'left field'),
    'CF': ('center fielder', 'center field'),
    'RF': ('right fielder', 'right field')
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

    runs_list = ['scores', 'homers', 'steals home']
    out1_list = ['out', 'caught stealing', 'picks off']
    out2_list = ['double play']
    outs_list = out1_list + out2_list

    if any(r in value for r in runs_list):
        suffix = ', run(s)'
        runs = sum([value.count(r) for r in runs_list])
    elif any(o in value for o in outs_list):
        suffix = ', out(s)'
    elif sequence and 'In play' in sequence[-1]:
        check_outs = False
        suffix = ', no out'

    if check_outs:
        if 'strikes' in value and 'to first' in value:
            outs = 0
        elif any(o in value for o in out2_list):
            outs = 2
        else:
            outs = sum([value.count(o) for o in out1_list])

    if sequence and 'In play' in sequence[-1]:
        sequence[-1] += suffix

    return {
        'type': 'event',
        'outs': outs,
        'runs': runs,
        'sequence': sequence,
        'value': value
    }


def _play_matchup(pnum, bnum, pteam, bteam, players):
    _, pplayer = _player('P', pnum, players[pteam])
    ppos = 'SP' if len(players[pteam]['P']) == 1 else 'RP'
    pitch = _stats('P', pplayer)

    _, bplayer = _player('B', bnum, players[bteam])
    bat = _stats('B', bplayer)

    return {
        'type': 'matchup',
        'pitcher': {
            'id': pnum,
            'pos': ppos,
            'stats': pitch
        },
        'batter': {
            'id': bnum,
            'pos': bplayer['pos'][0],
            'stats': bat
        }
    }


def _play_sub(subtype, id_, players, bases, subs):
    values = []
    if subtype == 'P':
        xpid = players['P'][0]['id']
        players['P'].insert(0, _new_pitcher(id_))
        if id_ in subs:
            player = _player('B', subs[id_], players)
            if player is None:
                i, _ = _player('B', id_, players)
                players['B'][i]['pos'] = [subtype]
                value = ('{} remains in the game as the pitcher, replacing '
                         '{}.').format(id_, xpid)
            else:
                i, xplayer = player
                xbid = xplayer['id']
                players['B'][i] = _new_batter(id_, [subtype])
                replacing = ', replacing ' + xbid if xbid != xpid else ''
                value = '{} replaces {}, batting {}{}.'.format(
                    id_, xpid, _batting_map[i], replacing)
        else:
            value = '{} replaces {}.'.format(id_, xpid)
        values.append(('Pitching Substitution', value))
    elif subtype in ['PH', 'PR']:
        i, xplayer = _player('B', subs[id_], players)
        xbid = xplayer['id']
        players['B'][i] = _new_batter(id_, [subtype])
        sub = _sub_map[subtype][0]
        value = '{} {} replaces {}.'.format(sub, id_, xbid)
        for base in range(3):
            for r, p in bases[base]:
                if r == xbid:
                    bases[base] = [(id_, p)]
        values.append(('Offensive Substitution', value))
    else:
        player = _player('B', subs[id_], players)
        if player is None:
            i, _ = _player('B', id_, players)
            players['B'][i]['pos'] = [subtype]
            sub = _sub_map[subtype][0]
            value = '{} remains in the game as the {}.'.format(id_, sub)
            values.append(('Defensive Switch', value))
        else:
            i, xplayer = player
            players['B'][i] = _new_batter(id_, [subtype])
            xsub = _sub_map[xplayer['pos'][0]][0]
            if 'Pinch' in xsub:
                xsub = xplayer['id']
            else:
                xsub = xsub + ' ' + xplayer['id']
            sub = _sub_map[subtype][1]
            value = '{} replaces {}, batting {}, playing {}.'.format(
                id_, xsub, _batting_map[i], sub)
            values.append(('Defensive Substitution', value))

        pos = subtype
        while pos:
            for j, bplayer in enumerate(players['B']):
                if i == j:
                    continue
                if pos == bplayer['pos'][0]:
                    xsub = _sub_map[bplayer['pos'][0]][1]
                    bplayer['pos'] = bplayer['pos'][1:]
                    i, pos = j, bplayer['pos'][0]
                    value = 'Defensive switch from {} to {} for {}.'.format(
                        xsub, _sub_map[pos][1], bplayer['id'])
                    values.append(('Defensive Switch', value))
                    break
            else:
                pos = None

    return {'type': 'sub', 'values': values}


def _sequence(counts, value):
    return '{} {} {} {}'.format(*counts, value)


def _value(values, bases, pnum, bnum, pteam, bteam, players, during=False):
    _, pplayer = _player('P', pnum, players[pteam])
    pstats = pplayer['stats']

    _, bplayer = _player('B', bnum, players[bteam])
    bstats = bplayer['stats']

    if values:
        _tweak_runners(values)
        prefix = ('With {} batting, ' if during else '{} ').format(bnum)
        values[0] = prefix + values[0]
    value = ' '.join([v + ('.' if v[-1] != '!' else '') for v in values])

    out1_list = ['out', 'caught stealing', 'picks off']
    if 'strikes' in value and 'to first' in value:
        outs = 0
    elif 'double play' in value:
        outs = 2
    else:
        outs = sum([value.count(o) for o in out1_list])
    pstats['O'] += outs
    if pstats['O'] > 2:
        pstats['IP'] += 1
    pstats['O'] = pstats['O'] % 3

    if any([p in value for p in ['walk', 'sacrifice bunt', 'sacrifice fly']]):
        if 'walk' in value:
            pstats['BB'] += 1
            bstats['BB'] += 1
    else:
        bstats['AB'] += 1

    if any(s in value for s in ['strikes out', 'called out on strikes']):
        pstats['K'] += 1
        bstats['K'] += 1

    if any([h in value for h in ['singles', 'doubles', 'triples', 'homers']]):
        pstats['H'] += 1
        bstats['H'] += 1
        if 'doubles' in value:
            bstats['2B'] += 1
        if 'triples' in value:
            bstats['3B'] += 1
        if 'homers' in value:
            bstats['HR'] += 1

    for r, p in bases[3]:
        _, xplayer = _player('P', p, players[pteam])
        xplayer['stats']['R'] += 1
        if not any([o in value for o in ['double play', 'steals home']]):
            bstats['RBI'] += 1
    bases[3] = []

    return value


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

    players = {away_team: {'B': [], 'P': []}, home_team: {'B': [], 'P': []}}
    player_ids = []
    subs = {}

    last = ''
    regex = '"hsn dc">RBI</th>\s*</tr>(.+?)</table>'
    batting_linescores = re.findall(regex, box_content, re.DOTALL)
    for i, line in enumerate(batting_linescores):
        t = away_team if i == 0 else home_team
        regex = '(>)?<a href="../players/player_(\d+).html">[^<]+</a>([^<]+)<'
        for starter, id_, pos in re.findall(regex, line):
            player_ids.append(id_)
            if starter:
                pos = pos.strip().split(', ')
                players[t]['B'].append(_new_batter('P' + id_, pos))
            else:
                subs['P' + id_] = last
            last = 'P' + id_

    regex = '"hsn dc">ERA</th>\s*</tr>(.+?)</table>'
    pitching_linescores = re.findall(regex, box_content, re.DOTALL)
    regex = '<a href="../players/player_(\d+).html">'
    for i, line in enumerate(pitching_linescores):
        t = away_team if i == 0 else home_team
        for j, id_ in enumerate(re.findall(regex, line)):
            player_ids.append(id_)
            if j == 0:
                players[t]['P'].append(_new_pitcher('P' + id_))

    player_ids = list(sorted(set(player_ids)))

    try:
        plays = []
        if log_link:
            log_content = _open(log_link)
            html = log_link.startswith('http')

            if html:
                away_title, home_title = _find('<title>(.+?) @ (.+?)</title>',
                                               log_content)
                away_team = decoding_to_encoding(away_title)
                home_team = decoding_to_encoding(home_title)
                date_title = _find(
                    'padding-top:4px;">(\d{2}\/\d{2}\/\d{4})</div>',
                    log_content)
                if not date_title:
                    return ret

            regex = r'(<a href="../players/player_)(\d+)(.html">[^<]+</a>)'
            log_content = re.sub(regex, 'P' + r'\2', log_content)

            regex = r'(\[%T\]\tRain delay of [^\n]+\n)'
            log_content = re.sub(regex, '', log_content)

            log_content = re.sub('  ', ' ', log_content)
            log_content = re.sub('</?b>', '', log_content)
            log_content = decoding_to_encoding_sub(log_content)

            inning = []
            if html:
                regex = 'class="data" width="968px">(.+?)</table>'
                cells = re.findall(regex, log_content, re.DOTALL)
            else:
                cells = log_content.split('[%T]')[1:]

            for i, c in enumerate(cells):
                if 'Game Over' in c:
                    break

                bases = [[], [], [], []]
                sequence, values = [], []
                play = []
                curr_batting = ''

                regex = '"boxtitle">(.+?)</th>' if html else '^\t([^-]+)'
                cell_label = _find(regex, c, re.DOTALL)
                cell_inning = cell_label.strip().split()[-1]
                cell_label = '{}{} {}'.format(cell_label[0],
                                              cell_label[1:3].lower(),
                                              cell_inning.lower())

                c = c.replace('1st', 'first').replace('2nd', 'second').replace(
                    '3rd', 'third').replace('Home', 'home')

                if html:
                    regex = 'style="padding:4px 0px 4px 4px;">(.+?) batting -'
                else:
                    regex = '- (\w+) batting -'
                cell_batting = _find(regex, c, re.DOTALL)

                regex = 'Pitching for (\w+) : \w+ (\w+)'
                pitching_team, curr_pitching = _find(regex, c, re.DOTALL)
                if pitching_team not in [away_team, home_team]:
                    return ret
                if pitching_team == home_team:
                    batting_team = away_team
                else:
                    batting_team = home_team
                curr_fielders = players[pitching_team]

                if curr_pitching != curr_fielders['P'][0]['id']:
                    play.append(
                        _play_sub('P', curr_pitching, curr_fielders, bases,
                                  subs))

                if html:
                    regex = ('span="2">[^-]+- ([^;]+); [^\d]+(\d+) - '
                             '[^\d]+(\d+)</td>')
                else:
                    regex = 'over - ([^;]+); [^\d]+(\d+) - [^\d]+(\d+)'
                cell_footer = re.findall(regex, c)
                if cell_footer:
                    m = list(cell_footer[0]) + [away_team, home_team]
                    cell_footer = '{0}; {3} {1} - {4} {2}'.format(*m)
                else:
                    cell_footer = ''

                if html:
                    left = 'valign="top" width="268px" class="dl"'
                    right = 'class="dl" width="700px"'
                    regex = '(<td (?:{}|{})>.+?</td>)'
                    side = re.findall(regex.format(left, right), c, re.DOTALL)
                else:
                    regex = '(?:\[%B\]|\[%N\])\t[^\n]+'
                    side = re.findall(regex, c, re.DOTALL)
                for s in side:
                    if html:
                        regex = '<td {}>(.+?)</td>'
                        l = _find(regex.format(left), s, re.DOTALL)
                        r = _find(regex.format(right), s, re.DOTALL)
                    else:
                        l = s.split('\t', 1)[1] if _find('\[%B\]', s) else ''
                        r = s.split('\t', 1)[1] if _find('\[%N\]', s) else ''
                    if l:
                        if sequence or values:
                            d = False
                            if values and any(
                                    o in values[0]
                                    for o in ['caught stealing', 'picks off']):
                                d = True
                            play.append(
                                _play_event(
                                    sequence,
                                    _value(
                                        values,
                                        bases,
                                        curr_pitching,
                                        curr_batting,
                                        pitching_team,
                                        batting_team,
                                        players,
                                        during=d)))
                        sequence, values = [], []
                        counts = [0, 0, 0]
                        pitching = _find('Pitching: \w+ (\w+)', l)
                        batting = _find('Batting: \w+ (\w+)', l)
                        hitting = _find('Pinch Hitting: \w+ (\w+)', l)
                        running = _find('Pinch Runner at \w+ (\w+)', l)
                        defensive = _find('Now (?:at|in) (\w+): (\w+)', l)
                        if pitching and pitching != curr_pitching:
                            curr_pitching = pitching
                            play.append(
                                _play_sub('P', curr_pitching, curr_fielders,
                                          bases, subs))
                        elif batting or hitting:
                            if batting:
                                curr_batting = batting
                                if not _player('B', curr_batting,
                                               players[batting_team]):
                                    play.append(
                                        _play_sub('PH', curr_batting,
                                                  players[batting_team], bases,
                                                  subs))
                            if hitting:
                                curr_batting = hitting
                                play.append(
                                    _play_sub('PH', curr_batting,
                                              players[batting_team], bases,
                                              subs))
                            play.append(
                                _play_matchup(curr_pitching, curr_batting,
                                              pitching_team, batting_team,
                                              players))
                        elif running:
                            play.append(
                                _play_sub('PR', running, players[batting_team],
                                          bases, subs))
                        elif defensive[0]:
                            subtype, value = defensive
                            play.append(
                                _play_sub(subtype, value,
                                          players[pitching_team], bases, subs))
                    elif r:
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
                                            _value(
                                                values,
                                                bases,
                                                curr_pitching,
                                                curr_batting,
                                                pitching_team,
                                                batting_team,
                                                players,
                                                during=True)))
                                    sequence, values = [], []
                                _parse_value(value, bases, counts, sequence,
                                             values, curr_batting,
                                             curr_fielders)
                            else:
                                _parse_part(part, bases, values, curr_fielders)

                if sequence or values:
                    d = False
                    if values and any(
                            o in values[0]
                            for o in ['caught stealing', 'picks off']):
                        d = True
                    play.append(
                        _play_event(
                            sequence,
                            _value(
                                values,
                                bases,
                                curr_pitching,
                                curr_batting,
                                pitching_team,
                                batting_team,
                                players,
                                during=d)))

                inning.append({
                    'label': cell_label,
                    'batting': cell_batting,
                    'pitching': curr_pitching,
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
            'players': player_ids,
            'plays': plays,
        })
    except:
        logger_.log(
            logging.WARNING,
            'Unable to parse {}.'.format(log_link),
            exc_info=True)

    return ret


def _bases_pop(bases, base, runner):
    if base > -1 and len(bases[base]):
        pair = bases[base][0]
        bases[base] = []
        return pair

    for base in range(3):
        for r, p in bases[base]:
            if r == runner:
                bases[base].remove((r, p))
                return (r, p)


def _bases_push(bases, base, pair):
    if not pair:
        return

    b = _bases_map[base]
    bases[b].append(pair)

    for b in range(3):
        if len(bases[b]) == 2:
            prev, curr = bases[b]
            bases[b + 1].append(prev)
            bases[b] = [curr]


def _description(category, index):
    desc = _description_map.get(category)
    return desc[index] if desc else ''


def _stat(name, count):
    return '{} {}'.format(count, name) if count > 1 else name


def _new_batter(num, pos):
    stats = {k: 0 for k in ['H', 'AB', '2B', '3B', 'HR', 'RBI', 'BB', 'K']}
    return {
        'id': num,
        'pos': pos,
        'stats': stats,
    }


def _new_pitcher(num):
    stats = {k: 0 for k in ['IP', 'O', 'H', 'R', 'BB', 'K']}
    return {
        'id': num,
        'stats': stats,
    }


def _pitcher(fielders):
    return fielders['P'][0]['id']


def _fielder(num, fielders):
    if num == '1':
        return 'pitcher ' + _pitcher(fielders)

    pos, title = _fielder_map[num]
    for fielder in fielders['B']:
        if pos == fielder['pos'][0]:
            return title + ' ' + fielder['id']

    return title + '*'


def _fielders(nums, fielders):
    nums = nums.replace('U', '').split('-')
    f = [_fielder(num, fielders) for num in nums]
    return ' to ' + f[0] if len(f) == 1 else ', ' + ' to '.join(f)


def _player(key, id_, players):
    for i, player in enumerate(players[key]):
        if id_ == player['id']:
            return i, player


def _stats(key, player):
    stats = player['stats']
    if key == 'B':
        default = '{}-{}'.format(stats['H'], stats['AB'])
        extra = []
        for name in ['2B', '3B', 'HR', 'RBI', 'BB', 'K']:
            if stats[name]:
                extra.append(_stat(name, stats[name]))
        if extra:
            default = default + ', ' + ', '.join(extra)
        return default
    else:
        default = '{}.{} IP'.format(stats['IP'], stats['O'])
        extra = []
        for name in ['H', 'R', 'BB', 'K']:
            extra.append('{} {}'.format(stats[name], name))
        default = default + ', ' + ', '.join(extra)
        return default


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


def _parse_value(value, bases, counts, sequence, values, batting, fielders):
    if _find('Base on Balls', value):
        _bases_push(bases, 'first', (batting, _pitcher(fielders)))
        counts[1] += 1
        sequence.append(_sequence(counts, 'Ball'))
        values.append('walks')
        return

    if _find('Intentional Walk', value):
        _bases_push(bases, 'first', (batting, _pitcher(fielders)))
        values.append('walked intentionally by ' + _pitcher(fielders))
        return

    if _find('Strikes out swinging', value):
        counts[2] += 1
        sequence.append(_sequence(counts, 'Swinging Strike'))
        values.append('strikes out swinging')
        if 'reaches first' in value:
            if 'passed ball' in value:
                field = _fielder('2', fielders)
                values.append('Passed ball by ' + field)
            else:
                values.append('Wild pitch by ' + _pitcher(fielders))
            values.append(batting + ' to first')
            _bases_push(bases, 'first', (batting, _pitcher(fielders)))
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

    sequence.append(_sequence(counts, 'In play'))

    num, category, zone = _find('Fly out, F(\d) \(([^,]+), (\w+)\)', value)
    if num:
        field = _fielder(num, fielders)
        desc = _description(category, 0)
        values.append('{} to {} (zone {})'.format(desc, field, zone))
        return

    nums, zone = _find('Grounds? out,? ([^\s]+) \(Groundball, (\w+)\)', value)
    if nums:
        fields = _fielders(nums, fielders)
        values.append('grounds out{} (zone {})'.format(fields, zone))
        return

    num, zone = _find('Reached on error, E(\d) \([^,]+, (\w+)\)', value)
    if num:
        _bases_push(bases, 'first', (batting, _pitcher(fielders)))
        field = _fielder(num, fielders)
        values.append('reaches on an error by {} (zone {})'.format(
            field, zone))
        return

    num = _find('Reached via error on a dropped throw, E(\d)', value)
    if num:
        _bases_push(bases, 'first', (batting, _pitcher(fielders)))
        field = _fielder(num, fielders)
        zone = '34' if num == '1' else '56'
        values.append('reaches on an error by {} (zone {})'.format(
            field, zone))
        return

    if _find('Hit by Pitch', value):
        _bases_push(bases, 'first', (batting, _pitcher(fielders)))
        values.append('is hit by the pitch')
        return

    if _find('Reaches on Catchers interference', value):
        _bases_push(bases, 'first', (batting, _pitcher(fielders)))
        field = _fielder('2', fielders)
        values.append('reaches on an error by {} (interference)'.format(field))
        return

    nums = _find('Bunt for hit - play at first, batter safe!', value)
    if nums:
        _bases_push(bases, 'first', (batting, _pitcher(fielders)))
        field = _fielder('1', fielders)
        values.append('singles on a bunt ground ball to {} '
                      '(zone 1S)'.format(field))
        return

    nums = _find('Bunt for hit - play at first, batter OUT! ([^\s]+)', value)
    if nums:
        fields = _fielders(nums, fielders)
        field = nums[1] if nums[0] == 'U' else nums[2]
        zone = field + ('S' if field != '2' else '')
        values.append('bunt grounds out{} (zone {})'.format(fields, zone))
        return

    num = _find('Bunt - Flyout! F(\d)', value)
    if num:
        field = _fielder(num, fielders)
        zone = field + ('S' if field != '2' else '')
        values.append('bunt pops out to {} (zone {})'.format(field, zone))
        return

    if _find('Sac Bunt - play at first, batter safe!', value):
        _bases_push(bases, 'first', (batting, _pitcher(fielders)))
        field = _fielder('1', fielders)
        values.append('reaches a bunt ground ball to {} '
                      '(attempted sacrifice) (zone 1S)'.format(field))
        return

    nums = _find('Sac Bunt - play at first, batter OUT! ([^\s]+)', value)
    if nums:
        fields = _fielders(nums, fielders)
        field = nums[1] if nums[0] == 'U' else nums[2]
        zone = field + ('S' if field != '2' else '')
        values.append('out on a sacrifice bunt{} (zone {})'.format(
            fields, zone))
        return

    base = _find('Sac Bunt - play at (\w+), runner OUT -> throw to first, DP!',
                 value)
    if base:
        pair = _bases_pop(bases, _bases_map[base] - 1, '')
        runner = pair[0] if pair else ''
        nums = '1-5-3' if base == 'third' else '1-6-3'
        fields = _fielders(nums, fielders)
        values.append('bunt grounds into a double play{} '
                      '(attempted sacrifice) (zone 1S)'.format(fields))
        values.append('{} out at {}'.format(runner, base))
        return

    base, nums = _find('Sac Bunt - play at (\w+), runner OUT! ([^\s]+)', value)
    if base:
        pair = _bases_pop(bases, _bases_map[base] - 1, '')
        runner = pair[0] if pair else ''
        _bases_push(bases, 'first', (batting, _pitcher(fielders)))
        fields = _fielders(nums, fielders)
        field = nums[1] if nums[0] == 'U' else nums[2]
        zone = field + ('S' if field != '2' else '')
        values.append('bunt grounds into a fielders choice{} '
                      '(attempted sacrifice) (zone {})'.format(fields, zone))
        values.append('{} out at {}'.format(runner, base))
        return

    base = _find('Sac Bunt - play at (\w+), runner safe!', value)
    if base:
        pair = _bases_pop(bases, _bases_map[base] - 1, '')
        runner = pair[0] if pair else ''
        _bases_push(bases, base, pair)
        _bases_push(bases, 'first', (batting, _pitcher(fielders)))
        nums = '1-5' if base == 'third' else '1-6'
        fields = _fielders(nums, fielders)
        values.append('bunt grounds into a failed fielders choice{} '
                      '(attempted sacrifice) (zone 1S)'.format(fields))
        values.append('{} to {}'.format(runner, base))
        return

    nums = _find('Squeeze Bunt - play home, runner OUT, batter safe! ([^\s]+)',
                 value)
    if nums:
        pair = _bases_pop(bases, 2, '')
        runner = pair[0] if pair else ''
        _bases_push(bases, 'first', (batting, _pitcher(fielders)))
        fields = _fielders(nums, fielders)
        field = nums[1] if nums[0] == 'U' else nums[2]
        zone = field + ('S' if field != '2' else '')
        values.append('bunt grounds into a fielders choice{} '
                      '(attempted sacrifice) (zone {})'.format(fields, zone))
        values.append('{} out at home'.format(runner))

    base, nums, zone = _find(
        'Fielders Choice at (\w+), ([^\s]+) \(Groundball, (\w+)\)', value)
    if base:
        pair = _bases_pop(bases, _bases_map[base] - 1, '')
        runner = pair[0] if pair else ''
        _bases_push(bases, 'first', (batting, _pitcher(fielders)))
        fields = _fielders(nums, fielders)
        values.append('grounds into a fielders choice{} (zone {})'.format(
            fields, zone))
        values.append('{} out at {}'.format(runner, base))
        return

    nums, zone = _find(
        'Grounds into fielders choice (\d-2) \(Groundball, (\w+)\)', value)
    if nums:
        pair = _bases_pop(bases, 2, '')
        runner = pair[0] if pair else ''
        _bases_push(bases, 'first', (batting, _pitcher(fielders)))
        fields = _fielders(nums, fielders)
        values.append('grounds into a fielders choice{} (zone {})'.format(
            fields, zone))
        values.append('{} out at home'.format(runner))
        return

    nums, zone = _find('double play, ([^\s]+) \(Groundball, (\w+)\)', value)
    if nums:
        base = nums[1] if nums[0] == 'U' else nums[2]
        base = 'home' if base == '2' else 'third' if base == '5' else 'second'
        pair = _bases_pop(bases, _bases_map[base] - 1, '')
        runner = pair[0] if pair else ''
        fields = _fielders(nums, fielders)
        values.append('grounds into a double play{} (zone {})'.format(
            fields, zone))
        values.append('{} out at {}'.format(runner, base.lower()))
        return

    base = '(SINGLE|DOUBLE|TRIPLE)'
    base, category, zone = _find(base + ' \(([^,]+), (\w+)\)', value)
    if base:
        if base != 'SINGLE':
            _bases_push(bases, 'home', _bases_pop(bases, 2, ''))
        if base == 'TRIPLE':
            _bases_push(bases, 'home', _bases_pop(bases, 1, ''))
            _bases_push(bases, 'home', _bases_pop(bases, 0, ''))
        elif base == 'DOUBLE':
            b = 'home' if bases[0] else 'third'
            _bases_push(bases, b, _bases_pop(bases, 1, ''))
            _bases_push(bases, 'third', _bases_pop(bases, 0, ''))
        _bases_push(bases, base, (batting, _pitcher(fielders)))
        base = base.lower() + 's'
        desc = _description(category, 1)
        index = 0 if _find('infield hit', value) else 1
        inf = '' if index else ' (infield hit)'
        field = _fielder(_location(zone, index), fielders)
        values.append('{} on a {} to {}{} (zone {})'.format(
            base, desc, field, inf, zone))
        base = _find('OUT at (\w+) base trying to stretch hit', value)
        if base:
            _bases_pop(bases, _bases_map[base] - 1, '')
            values.append(batting +
                          ' out at {} trying to stretch hit'.format(base))
        return

    num, base = _find(
        '(?:Single|Double), Error in OF, E(\d), batter to (\w+) base', value)
    if num:
        if base != 'second':
            _bases_push(bases, 'home', _bases_pop(bases, 2, ''))
        if base == 'third':
            b = 'home' if bases[0] else 'third'
            _bases_push(bases, b, _bases_pop(bases, 1, ''))
            _bases_push(bases, 'third', _bases_pop(bases, 0, ''))
        _bases_push(bases, base, (batting, _pitcher(fielders)))
        hit = 'singles' if base == 'second' else 'doubles'
        field = _fielder(num, fielders)
        zone = num + 'S'
        values.append('{} on a line drive to {} (zone {})'.format(
            hit, field, zone))
        values.append('{} to {} on an error by {}'.format(
            batting, base, field))
        return

    category, zone = _find('HOME RUN \(([^,]+), (\w+)\)', value)
    if category:
        desc = _description(category, 1)
        ins = ' (inside the park)' if _find('Inside the Park', value) else ''
        index = 0 if _find('infield hit', value) else 1
        loc = _location(zone, index)
        field = _fielder(loc, fielders) if ins else _homer_map.get(loc, '')
        dist = _find('Distance : (\d+) ft', value)
        dist = ', {} ft'.format(dist) if dist else ''
        values.append('homers on a {} to {}{} (zone {}{})'.format(
            desc, field, ins, zone, dist))
        for b in [2, 1, 0]:
            if len(bases[b]):
                values.append(bases[b][0][0] + ' scores')
                _bases_push(bases, 'home', _bases_pop(bases, b, ''))
        _bases_push(bases, 'home', (batting, _pitcher(fielders)))
        return

    values.append(value + '*')


def _parse_part(value, bases, values, fielders):
    base = '(scores|to third|to second|steals third|steals second)'
    runner, base = _find('(P\d+) ' + base, value)
    if runner:
        base = base.replace('to ', '').replace('steals ', '')
        _bases_push(bases, base, _bases_pop(bases, -1, runner))
        values.append(value)
        return

    if _find('Steal of home', value):
        pair = _bases_pop(bases, 2, '')
        runner = pair[0] if pair else ''
        if 'is safe' in value:
            _bases_push(bases, 'home', pair)
            values.append(runner + ' steals home')
            return
        else:
            values.append(runner + ' caught stealing home')
            return

    if _find('home, SAFE, throw made at trailing runner, SAFE', value):
        pair = _bases_pop(bases, 2, '')
        runner = pair[0] if pair else ''
        _bases_push(bases, 'home', pair)
        values.append(runner + ' scores')
        pair = _bases_pop(bases, 1, '')
        runner = pair[0] if pair else ''
        _bases_push(bases, 'third', pair)
        values.append(runner + ' to third (throw made)')
        return

    if _find('home, SAFE, throw made at trailing runner, OUT', value):
        pair = _bases_pop(bases, 2, '')
        runner = pair[0] if pair else ''
        _bases_push(bases, 'home', pair)
        values.append(runner + ' scores')
        pair = _bases_pop(bases, 1, '')
        runner = pair[0] if pair else ''
        values.append(runner + ' out at third on the throw')
        return

    throw = ['throw made', 'with throw']
    advance = '(?:tries for home, SAFE|tags up, SCORES)'
    if _find(advance, value):
        pair = _bases_pop(bases, 2, '')
        runner = pair[0] if pair else ''
        _bases_push(bases, 'home', pair)
        throw = ' (throw made)' if any([t in value for t in throw]) else ''
        values.append(runner + ' scores{}'.format(throw))
        return

    advance = '(?:tries for home, (?:throw and )?OUT|tags up, OUT at HOME)'
    if _find(advance, value):
        pair = _bases_pop(bases, 2, '')
        runner = pair[0] if pair else ''
        values.append(runner + ' out at home on the throw')
        return

    advance = '(?:tries for third, SAFE|tags up, SAFE at third)'
    if _find(advance, value):
        pair = _bases_pop(bases, 1, '')
        runner = pair[0] if pair else ''
        _bases_push(bases, 'third', pair)
        throw = ' (throw made)' if any([t in value for t in throw]) else ''
        values.append(runner + ' to third{}'.format(throw))
        return

    if _find('(?:tries for third, OUT|tags up, OUT at third)', value):
        pair = _bases_pop(bases, 1, '')
        runner = pair[0] if pair else ''
        values.append(runner + ' out at third on the throw')
        return

    advance = '(?:tries for second, SAFE|tags up, SAFE at second)'
    if _find(advance, value):
        pair = _bases_pop(bases, 0, '')
        runner = pair[0] if pair else ''
        _bases_push(bases, 'second', pair)
        throw = ' (throw made)' if any([t in value for t in throw]) else ''
        values.append(runner + ' to second{}'.format(throw))
        return

    if _find('(?:tries for second, OUT|tags up, OUT at second)', value):
        pair = _bases_pop(bases, 0, '')
        runner = pair[0] if pair else ''
        values.append(runner + ' out at second on the throw')
        return

    if _find('Wild Pitch!', value):
        values.append('wild pitch by ' + _pitcher(fielders))
        return

    if _find('Balk!', value):
        values.append('balk by ' + _pitcher(fielders))
        return

    if _find('Passed Ball!', value):
        field = _fielder('2', fielders)
        values.append('passed ball by ' + field)
        return

    num = _find('Error on foul ball, E(\d)', value)
    if num:
        field = _fielder(num, fielders)
        values.append('error by {} (foul catch attempt)'.format(field))
        return

    if _find('Throwing error on steal attempt, E2', value):
        field = _fielder('2', fielders)
        values.append('throwing error by {} (steal attempt)'.format(field))
        return

    num = _find('Throwing error, E(\d)', value)
    if num:
        field = _fielder(num, fielders)
        values.append('Throwing error by {}'.format(field))
        return

    base = _find('caught stealing (\w+) base', value)
    if base:
        _bases_pop(bases, _bases_map[base] - 1, '')
        values.append(value)
        return

    base = _find('Pickoff Throw to (\w+) - Out!', value)
    if base:
        pair = _bases_pop(bases, _bases_map[base.lower()], '')
        runner = pair[0] if pair else ''
        values.append('{} picks off {}'.format(_pitcher(fielders), runner))
        return

    base = _find('Pickoff Throw to (\w+) - Error! E1', value)
    if base:
        values.append('throwing error by {} (pickoff attempt)'.format(
            _pitcher(fielders)))
        return

    base = _find('Pickoff Throw by Catcher to (\w+) - Out!', value)
    if base:
        pair = _bases_pop(bases, _bases_map[base.lower()], '')
        field = _fielder('2', fielders)
        runner = pair[0] if pair else ''
        values.append('{} picks off {}'.format(field, runner))
        return

    base = _find('Pickoff Throw by Catcher to (\w+) - Error! E2', value)
    if base:
        field = _fielder('2', fielders)
        values.append('throwing error by {} (pickoff attempt)'.format(field))
        return

    nums, zone = _find('Lined into DP, ([^\s]+) \(Line Drive, (\w+)\)', value)
    if nums:
        fields = _fielders(nums, fielders)
        base = 0 if nums[-1] == '3' else 2 if nums[-1] == '5' else 1
        pair = _bases_pop(bases, base, '')
        base = 'first' if base == 0 else 'second' if base == 1 else 'third'
        runner = pair[0] if pair else ''
        values[-1] = ('lines into a double play{} (zone {}). '
                      '{} out at {}'.format(fields, zone, runner, base))
        return

    if _find('Batter strikes out.', value):
        return

    values.append(value + '*')


def _tweak_runners(values):
    sac = 'out on a sacrifice fly'
    adv_list = ['scores', 'to third', 'to second']
    run_list = adv_list + ['out at']
    regex = '(\w+) (?:{})'.format('|'.join(run_list))
    lines, runners = [], []
    throw = None
    for v in list(values[1:]):
        if sac and any([a in v for a in adv_list]):
            values[0] = re.sub('flies out|lines out|pops out', sac, values[0])
            sac = ''
        if any([r in v for r in run_list]):
            lines.append(v)
            runners.append(_find(regex, v))
            values.remove(v)
        if v.startswith('Throwing error '):
            throw = v
            values.remove(v)

    for r, l in list(zip(runners, lines)):
        if runners.count(r) > 1:
            lines.remove(l)
            runners.remove(r)

    for r in run_list:
        for l in lines:
            if r in l:
                values.append(l)

    if throw:
        values.append(throw)


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
