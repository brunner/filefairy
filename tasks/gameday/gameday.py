#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import json
import os
import re
import sys
from functools import partial

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/tasks/gameday', '', _path))

from api.registrable.registrable import Registrable  # noqa
from common.elements.elements import anchor  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import span  # noqa
from common.elements.elements import table  # noqa
from common.datetime_.datetime_ import decode_datetime  # noqa
from common.subprocess_.subprocess_ import check_output  # noqa
from common.json_.json_ import dumps  # noqa
from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa
from util.jersey.jersey import get_rawid  # noqa
from util.statslab.statslab import parse_game_data  # noqa
from util.statslab.statslab import parse_player  # noqa
from util.team.team import choose_colors  # noqa
from util.team.team import divisions  # noqa
from util.team.team import encoding_to_abbreviation  # noqa
from util.team.team import encoding_to_colors  # noqa
from util.team.team import encoding_to_decoding  # noqa
from util.team.team import encoding_to_nickname  # noqa
from util.team.team import encoding_to_teamid  # noqa
from util.team.team import logo_absolute  # noqa
from util.team.team import teamid_to_encoding  # noqa

FAIRYLAB_DIR = re.sub(r'/filefairy/tasks/gameday', '/fairylab/static', _path)
FILEFAIRY_DIR = re.sub(r'/tasks/gameday', '', _path)

_divisions = divisions()
_game_path = '/resource/games/game_{}.json'
_html = 'https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/'
_html_player = 'players/player_{}.html'
_player_default = {
    'name': 'Jim Unknown',
    'number': '0',
    'bats': '-',
    'throws': '-'
}
_smallcaps = {k: v for k, v in zip('BCDFHLPRS', 'ʙᴄᴅꜰʜʟᴘʀs')}
_statslab_link = ('https://orangeandblueleaguebaseball.com/StatsLab/'
                  'reports/news/html/')


def bold(text):
    return span(['text-bold'], text)


def secondary(text):
    return span(['text-secondary'], text)


class Gameday(Registrable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.colors = {}

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _href():
        return '/gameday/'

    @staticmethod
    def _info():
        return 'Replays finished games in real time.'

    @staticmethod
    def _title():
        return 'gameday'

    def _notify_internal(self, **kwargs):
        if kwargs['notify'] == Notify.STATSPLUS_SIM:
            self._clear()
            self.write()
        if kwargs['notify'] == Notify.LEAGUEFILE_DOWNLOAD:
            if not self.data['started']:
                self._backfill()
            self.data['started'] = False
            self.write()
        return Response()

    def _on_message_internal(self, **kwargs):
        return Response()

    def _render_internal(self, **kwargs):
        data = self.data
        original = copy.deepcopy(data)

        d = FAIRYLAB_DIR + '/gameday/'
        check_output(['rm', '-rf', d])
        check_output(['mkdir', d])

        games = copy.deepcopy(self.data['games'])
        schedule_data = self._schedule_data(games)

        ret = []

        gameday = self._gameday(schedule_data)
        html = 'gameday/index.html'
        ret.append((html, '', 'gameday.html', gameday))

        for id_ in games:
            with open(FILEFAIRY_DIR + _game_path.format(id_), 'r') as f:
                game_data = json.loads(f.read())
                if game_data['ok']:
                    away_team = encoding_to_nickname(game_data['away_team'])
                    home_team = encoding_to_nickname(game_data['home_team'])
                    date = decode_datetime(
                        game_data['date']).strftime('%m/%d/%Y')
                    subtitle = '{} at {}, {}'.format(away_team, home_team,
                                                     date)
                    game = self._game(id_, subtitle, game_data, schedule_data)
                    html = 'gameday/{}/index.html'.format(id_)
                    ret.append((html, subtitle, 'game.html', game))

        if data != original:
            self.write()

        return ret

    def _run_internal(self, **kwargs):
        response = Response()
        if self._check_games():
            self._render(**kwargs)
            response.append(notify=Notify.BASE)
        return response

    def _setup_internal(self, **kwargs):
        self._render(**kwargs)
        return Response()

    def _shadow_internal(self, **kwargs):
        return []

    def _game_repl(self, game_data, m):
        a = m.group(0)
        data = self.data
        if a.startswith('P'):
            return data['players'][a]['name'] if a in data['players'] else a
        if a.startswith('T'):
            return encoding_to_decoding(a)
        return a

    def _game_sub(self, game_data):
        data = self.data
        pattern = '|'.join([id_ + '(?!\d)' for id_ in data['players']] +
                           [game_data['away_team'], game_data['home_team']])
        return partial(re.sub, pattern, partial(self._game_repl, game_data))

    @staticmethod
    def _schedule_data(games):
        sdata = {}
        for id_ in games:
            with open(FILEFAIRY_DIR + _game_path.format(id_), 'r') as f:
                game_data = json.loads(f.read())
                if game_data['ok']:
                    date = decode_datetime(game_data['date'])

                    away_team = game_data['away_team']
                    if away_team not in sdata:
                        sdata[away_team] = []

                    home_team = game_data['home_team']
                    if home_team not in sdata:
                        sdata[home_team] = []

                    sdata[away_team].append((date, home_team, '@', id_))
                    sdata[home_team].append((date, away_team, 'v', id_))

        for encoding in sdata:
            sdata[encoding] = sorted(sdata[encoding])

        return sdata

    @staticmethod
    def _schedule_head(decoding):
        return table(
            clazz='table-fixed border border-bottom-0 mt-3',
            head=[cell(content=decoding + ' Schedule')])

    @staticmethod
    def _schedule_body(encoding, id_, schedule_data):
        body = []
        for sdate, steam, ssymbol, sid in schedule_data[encoding]:
            sdate = sdate.strftime('%m/%d/%Y')
            steam = encoding_to_decoding(steam)
            stext = '{} {} {}'.format(sdate, ssymbol, steam)
            if id_ == sid:
                body.append([cell(content=secondary(stext))])
            else:
                url = '/gameday/{}/'.format(sid)
                body.append([cell(content=anchor(url, stext))])

        return table(clazz='table-fixed border', body=body)

    def _backfill(self):
        self._clear()

        extract = FILEFAIRY_DIR + '/resource/extract'
        games = []
        for game in os.listdir(extract + '/box_scores/'):
            id_ = re.findall('game_box_(\d+).html', game)[0]
            games.append(id_)

        d = FILEFAIRY_DIR + '/resource/games/'
        check_output(['rm', '-rf', d])
        check_output(['mkdir', d])

        for id_ in games:
            box_link = extract + '/box_scores/game_box_{}.html'.format(id_)
            log_link = extract + '/game_logs/log_{}.txt'.format(id_)
            game_data_ = parse_game_data(box_link, log_link)
            fname = FILEFAIRY_DIR + '/resource/games/game_{}.json'.format(id_)
            with open(fname, 'w') as f:
                f.write(dumps(game_data_) + '\n')

        self.write()

    def _clear(self):
        self.data['games'] = []
        self.colors = {}

    def _add_players(self, players):
        for id_ in players:
            if 'P' + id_ in self.data['players']:
                continue
            link = _html + _html_player.format(id_)
            player = parse_player(link)
            self.data['players']['P' + id_] = player

    def _check_games(self):
        games = []
        for game in os.listdir(FILEFAIRY_DIR + '/resource/games/'):
            id_ = re.findall('game_(\d+).json', game)[0]
            games.append(id_)

        games = sorted(games)
        if games != self.data['games']:
            self.data['games'] = games

            if not self.data['started']:
                self.data['started'] = True
                self._chat('fairylab', 'Live sim created.')

            self.write()
            return True

        return False

    def _gameday(self, schedule_data):
        ret = {
            'breadcrumbs': [{
                'href': '/',
                'name': 'Fairylab'
            }, {
                'href': '',
                'name': 'Gameday'
            }],
            'schedule': []
        }

        for division, ts in _divisions:
            division = division.replace('AL', 'American League')
            division = division.replace('NL', 'National League')
            ret['schedule'].append(
                table(
                    clazz='table-fixed border border-bottom-0 mt-3',
                    head=[cell(content=division)]))
            body = []
            for teamid in ts:
                encoding = teamid_to_encoding(teamid)
                decoding = encoding_to_decoding(encoding)
                if encoding in schedule_data:
                    sid = schedule_data[encoding][0][3]
                    stext = anchor('/gameday/{}/'.format(sid), decoding)
                else:
                    stext = secondary(decoding)
                tcontent = logo_absolute(teamid, stext, 'left')
                body.append([cell(content=tcontent)])
            ret['schedule'].append(
                table(
                    clazz='table-fixed border',
                    bcols=[col(clazz='position-relative text-truncate')],
                    body=body))

        return ret

    @staticmethod
    def _pitch(pitch, sequence):
        p = '<div class="badge badge-pill pitch alert-{}">{}</div>'
        if 'In play' in sequence:
            return p.format('primary', pitch) + sequence
        if 'Ball' in sequence:
            return p.format('success', pitch) + sequence
        return p.format('danger', pitch) + sequence

    @staticmethod
    def _profile(encoding, num, colors, s):
        n = encoding_to_nickname(encoding).lower().replace(' ', '')
        div = '<div class="profile-image position-absolute ' + \
              '{}-{}-front"></div>'.format(n, colors)
        span = '<span class="profile-text align-middle ' + \
               'd-block">{}</span>'.format(s)
        return div + span

    def _player(self, key, encoding, player, colors):
        id_ = player['id']
        if id_ not in self.data['players']:
            player_data = _player_default
        else:
            player_data = self.data['players'][id_]
        title = 'ᴀᴛ ʙᴀᴛ' if key == 'bats' else 'ᴘɪᴛᴄʜɪɴɢ'
        pos = ''.join(_smallcaps.get(c, c) for c in player['pos'])
        num = player_data['number']
        s = '{}: {} #{} ({})<br>{}<br>{}'.format(
            title, pos, num, _smallcaps.get(player_data[key], 'ʀ'),
            player_data['name'], player['stats'])
        return cell(
            col=col(clazz='bg-light', colspan='2'),
            content=self._profile(encoding, num, colors, s))

    @staticmethod
    def _count(sequence):
        balls, strikes = [0, 0, 0, 0], [0, 0, 0]
        if sequence:
            _1, ball, strike, _2 = sequence[-1].split(' ', 3)
            for b in range(int(ball)):
                balls[b] = 1
            for s in range(int(strike)):
                strikes[s] = 1
        bdot, sdot = '', ''
        for b in balls:
            active = ' active' if b else ''
            bdot += '<div class="dot ball border{}"></div>'.format(active)
        for s in strikes:
            active = ' active' if s else ''
            sdot += '<div class="dot strike border{}"></div>'.format(active)
        return '<div class="count mr-8p">{}<br>{}</div>'.format(bdot, sdot)

    @staticmethod
    def _score(away_team, home_team, runs):
        s = '{} {} · {} {}'.format(
            encoding_to_abbreviation(away_team), runs[away_team],
            encoding_to_abbreviation(home_team), runs[home_team])
        return '<span class="badge border tag tag-light">{}</span>'.format(s)

    @staticmethod
    def _substitution(title, value, colspan):
        s = '<b>{}</b><br>{}'.format(title, value)
        return cell(col=col(clazz='bg-light', colspan=colspan), content=s)

    @staticmethod
    def _tag(value):
        tag = '<span class="badge border tag tag-{} mr-8p">{}</span>'
        if 'walk' in value:
            return tag.format('success', 'WALK')
        if 'hit by pitch' in value:
            return tag.format('success', 'HIT BY PITCH')
        if any([x in value for x in ['strikes out', 'called out on strikes']]):
            return tag.format('danger', 'STRIKEOUT')
        if 'singles' in value:
            return tag.format('primary', 'SINGLE')
        if 'doubles' in value:
            return tag.format('primary', 'DOUBLE')
        if 'triples' in value:
            return tag.format('primary', 'TRIPLE')
        if 'homers' in value:
            return tag.format('primary', 'HOME RUN')
        if 'sacrifice fly' in value:
            return tag.format('primary', 'SAC FLY')
        if 'sacrifice bunt' in value:
            return tag.format('primary', 'SAC BUNT')
        if 'reaches on an error' in value:
            return tag.format('primary', 'FIELD ERROR')
        if 'grounds into a double play' in value:
            return tag.format('secondary', 'GROUNDED INTO DP')
        if 'lines into a double play' in value:
            return tag.format('secondary', 'LINED INTO DP')
        if 'grounds into a fielders choice' in value:
            return tag.format('secondary', 'FORCE OUT')
        if 'flies out' in value:
            return tag.format('secondary', 'FLYOUT')
        if 'grounds out' in value:
            return tag.format('secondary', 'GROUNDOUT')
        if 'lines out' in value:
            return tag.format('secondary', 'LINEOUT')
        if 'pops out' in value:
            return tag.format('secondary', 'POP OUT')
        return tag.format('secondary', 'UNKNOWN*')

    def _play(self, value, encoding, id_, colors, sequence, score, colspan):
        if id_ not in self.data['players']:
            player_data = _player_default
        else:
            player_data = self.data['players'][id_]
        num = player_data['number']
        count = self._count(sequence)
        tag = self._tag(value)
        row = '<div class="d-flex">{}{}{}</div>'.format(count, tag, score)
        s = '{}<br>{}'.format(value, row)
        return cell(
            col=col(clazz='bg-light', colspan=colspan),
            content=self._profile(encoding, num, colors, s))

    def _game(self, game_id_, subtitle, game_data, schedule_data):
        ret = {
            'breadcrumbs': [{
                'href': '/',
                'name': 'Fairylab'
            }, {
                'href': '/gameday/',
                'name': 'Gameday'
            }, {
                'href': '',
                'name': subtitle
            }],
            'jerseys': [],
            'tabs': {
                'style': 'tabs',
                'tabs': []
            }
        }

        self._add_players(game_data['players'])

        game_sub = self._game_sub(game_data)
        away_team = game_data['away_team']
        away_decoding = encoding_to_decoding(away_team)
        home_team = game_data['home_team']
        home_decoding = encoding_to_decoding(home_team)

        if game_id_ in self.colors:
            colors = self.colors[game_id_]
        else:
            away_colors = encoding_to_colors(away_team)
            home_colors = encoding_to_colors(home_team)
            w = decode_datetime(game_data['date']).weekday()

            clash, hc = choose_colors(home_team, home_colors, w, 'home', '')
            _, ac = choose_colors(away_team, away_colors, w, 'away', clash)
            colors = {away_team: ac, home_team: hc}
            self.colors[game_id_] = colors

        for t in colors:
            c = colors[t]
            if isinstance(c, str):
                nickname = encoding_to_nickname(t).lower().replace(' ', '')
                ret['jerseys'].append((nickname, c, get_rawid(nickname)))

        runs = {away_team: 0, home_team: 0}

        log_tables = []
        plays = {
            'name': 'plays',
            'title': 'Plays',
            'tabs': {
                'style': 'pills',
                'tabs': []
            }
        }
        for i, inning in enumerate(game_data['plays']):
            plays_tables = []
            for half in inning:
                batting = half['batting']
                pitching = away_team if away_team != batting else home_team
                teamid = encoding_to_teamid(half['batting'])
                hcontent = logo_absolute(teamid, half['label'], 'left')
                log_table = table(
                    hcols=[col(clazz='position-relative', colspan='2')],
                    head=[cell(content=hcontent)],
                    bcols=[
                        col(clazz='position-relative'),
                        col(clazz='text-center text-secondary w-55p')
                    ],
                    body=[])
                plays_table = table(
                    hcols=[col(clazz='position-relative')],
                    head=[cell(content=hcontent)],
                    body=[])
                outs = 0
                for play in half['play']:
                    if play['type'] == 'sub':
                        for title, value in play['values']:
                            value = game_sub(value)
                            log_table['body'].append(
                                [self._substitution(title, value, '2')])
                            plays_table['body'].append(
                                [self._substitution(title, value, '')])
                    elif play['type'] == 'matchup':
                        log_table['body'].append([
                            self._player('throws', pitching, play['pitcher'],
                                         colors[pitching])
                        ])
                        log_table['body'].append([
                            self._player('bats', batting, play['batter'],
                                         colors[batting])
                        ])
                    elif play['type'] == 'event':
                        for s in play['sequence']:
                            pitch, balls, strikes, value = s.split(' ', 3)
                            pcontent = self._pitch(pitch, value)
                            if 'In play' in s:
                                log_table['body'].append([
                                    cell(
                                        col=col(colspan='2'), content=pcontent)
                                ])
                            else:
                                count = '{}-{}'.format(balls, strikes)
                                log_table['body'].append([
                                    cell(content=pcontent),
                                    cell(content=count)
                                ])
                        score = ''
                        value = game_sub(play['value'])
                        if play['outs']:
                            outs += play['outs']
                            value += ' ' + bold('{} out'.format(outs))
                        content = value
                        if play['runs']:
                            runs[batting] += play['runs']
                            score = self._score(away_team, home_team, runs)
                            content += '<br>' + score
                        log_table['body'].append(
                            [cell(col=col(colspan='2'), content=content)])
                        if play['batter']:
                            plays_table['body'].append([
                                self._play(value, batting, play['batter'],
                                           colors[batting], play['sequence'],
                                           score, '')
                            ])
                        else:
                            plays_table['body'].append([cell(content=content)])
                if half['footer']:
                    log_table['fcols'] = [col(colspan='2')]
                    fcontent = game_sub(half['footer'])
                    log_table['foot'] = [cell(content=fcontent)]
                    plays_table['foot'] = [cell(content=fcontent)]
                log_tables.append(log_table)
                plays_tables.append(plays_table)
            plays['tabs']['tabs'].append({
                'name': 'plays-' + str(i + 1),
                'title': str(i + 1),
                'tables': plays_tables
            })
        ret['tabs']['tabs'].append({
            'name': 'log',
            'title': 'Game Log',
            'tables': log_tables
        })

        game_box_link = 'box_scores/game_box_{}.html'.format(game_id_)
        log_link = 'game_logs/log_{}.html'.format(game_id_)
        sdate = decode_datetime(game_data['date']).strftime('%m/%d/%Y')

        links_tables = []
        links_tables.append(
            table(
                clazz='table-fixed border border-bottom-0 mt-3',
                head=[cell(content='Gameday Sources')]))
        links_tables.append(
            table(
                clazz='table-fixed border',
                body=[[
                    cell(
                        content=anchor(_statslab_link + game_box_link, sdate +
                                       ' StatsLab Game Box'))
                ], [
                    cell(
                        content=anchor(_statslab_link + log_link, sdate +
                                       ' StatsLab Log'))
                ]]))
        links_tables.append(self._schedule_head(away_decoding))
        links_tables.append(
            self._schedule_body(away_team, game_id_, schedule_data))
        links_tables.append(self._schedule_head(home_decoding))
        links_tables.append(
            self._schedule_body(home_team, game_id_, schedule_data))
        ret['tabs']['tabs'].append({
            'name': 'links',
            'title': 'Links',
            'tables': links_tables
        })

        ret['tabs']['tabs'].append(plays)
        return ret


# from tasks.statsplus.statsplus import Statsplus
# from common.datetime_.datetime_ import datetime_now
# from common.jinja2_.jinja2_ import env

# date = datetime_now()
# e = env()
# statsplus = Statsplus(date=date, e=e)

# for encoded_date in statsplus.data['scores']:
#     for score in statsplus.data['scores'][encoded_date]:
#         id_ = re.findall('(\d+)\.html', score)[0]
#         statsplus._extract(encoded_date, id_)
# statsplus._extract('2024-08-16T00:00:00-07:00', '2285')

# gameday = Gameday(date=date, e=e)
# gameday._backfill()
# gameday.data['started'] = True
# gameday._check_games()
# gameday.data['started'] = False
# gameday._setup_internal(date=date)
