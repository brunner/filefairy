#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import json
import os
import re
import sys
from functools import partial

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugin/gameday', '', _path)
sys.path.append(_root)
from api.registrable.registrable import Registrable  # noqa
from core.notify.notify import Notify  # noqa
from core.response.response import Response  # noqa
from util.component.component import anchor  # noqa
from util.component.component import bold  # noqa
from util.component.component import secondary  # noqa
from util.component.component import table  # noqa
from util.datetime_.datetime_ import decode_datetime  # noqa
from util.file_.file_ import recreate  # noqa
from util.jersey.jersey import get_rawid  # noqa
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

_divisions = divisions()
_fairylab_root = re.sub(r'/filefairy', '/fairylab/static', _root)
_game_path = '/resource/games/game_{}.json'
_html = 'https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/'
_player = 'players/player_{}.html'
_player_default = {
    'name': 'Jim Unknown',
    'number': '0',
    'bats': '-',
    'throws': '-'
}
_smallcaps = {'L': 'ʟ', 'R': 'ʀ', 'S': 'ꜱ'}


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
            self.data['started'] = False
            self.data['games'] = []
            self.colors = {}
            self.write()
        return Response()

    def _on_message_internal(self, **kwargs):
        return Response()

    def _render_internal(self, **kwargs):
        data = self.data
        original = copy.deepcopy(data)

        recreate(_fairylab_root + '/gameday/')

        games = copy.deepcopy(self.data['games'])
        schedule_data = self._schedule_data(games)

        ret = []

        gameday = self._gameday(schedule_data)
        html = 'gameday/index.html'
        ret.append((html, '', 'gameday.html', gameday))

        for id_ in games:
            with open(_root + _game_path.format(id_), 'r') as f:
                game_data = json.loads(f.read())
                away_team = encoding_to_nickname(game_data['away_team'])
                home_team = encoding_to_nickname(game_data['home_team'])
                date = decode_datetime(game_data['date']).strftime('%m/%d/%Y')
                subtitle = '{} at {}, {}'.format(away_team, home_team, date)
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
            response.append_notify(Notify.BASE)
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
        schedule_data = {}
        for id_ in games:
            with open(_root + _game_path.format(id_), 'r') as f:
                game_data = json.loads(f.read())
                date = decode_datetime(game_data['date'])

                away_team = game_data['away_team']
                if away_team not in schedule_data:
                    schedule_data[away_team] = []

                home_team = game_data['home_team']
                if home_team not in schedule_data:
                    schedule_data[home_team] = []

                schedule_data[away_team].append((date, home_team, '@', id_))
                schedule_data[home_team].append((date, away_team, 'v', id_))

        for encoding in schedule_data:
            schedule_data[encoding] = sorted(schedule_data[encoding])

        return schedule_data

    @staticmethod
    def _schedule_head(decoding):
        return table(
            clazz='table-fixed border border-bottom-0 mt-3', head=[decoding])

    @staticmethod
    def _schedule_body(encoding, id_, schedule_data):
        body = []
        for sdate, steam, ssymbol, sid in schedule_data[encoding]:
            sdate = sdate.strftime('%m/%d/%Y')
            steam = encoding_to_decoding(steam)
            stext = '{} {} {}'.format(sdate, ssymbol, steam)
            if id_ == sid:
                body.append([secondary(stext)])
            else:
                url = '/gameday/{}/'.format(sid)
                body.append([anchor(url, stext)])

        return table(clazz='table-fixed border', body=body)

    def _add_players(self, players):
        for id_ in players:
            if 'P' + id_ in self.data['players']:
                continue
            link = _html + _player.format(id_)
            player = parse_player(link)
            self.data['players']['P' + id_] = player

    def _check_games(self):
        games = []
        for game in os.listdir(_root + '/resource/games/'):
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
                    head=[division]))
            body = []
            for teamid in ts:
                encoding = teamid_to_encoding(teamid)
                decoding = encoding_to_decoding(encoding)
                if encoding in schedule_data:
                    sid = schedule_data[encoding][0][3]
                    stext = anchor('/gameday/{}/'.format(sid), decoding)
                else:
                    stext = secondary(decoding)
                body.append([logo_absolute(teamid, stext, 'left')])
            ret['schedule'].append(
                table(
                    clazz='table-fixed border',
                    bcols=[' class="position-relative text-truncate"'],
                    body=body))

        return ret

    @staticmethod
    def _badge(pitch, sequence):
        p = '<div class="badge badge-pill alert-pitch alert-{0}">{1}</div>'
        if 'In play' in sequence:
            return p.format('primary', pitch) + sequence
        if 'Ball' in sequence:
            return p.format('success', pitch) + sequence
        return p.format('danger', pitch) + sequence

    @staticmethod
    def _profile(encoding, num, colors, s):
        n = encoding_to_nickname(encoding).lower().replace(' ', '')
        div = '<div class="profile position-absolute ' + \
              '{}-{}-front"></div>'.format(n, colors)
        span = '<span class="align-middle d-block ' + \
               'pl-84p">{}</span>'.format(s)
        return div + span

    def _atbat(self, encoding, id_, colors):
        if id_ not in self.data['players']:
            player = _player_default
        else:
            player = self.data['players'][id_]
        num = player['number']
        s = 'ᴀᴛ ʙᴀᴛ: #{} ({})<br>{}<br>&nbsp;'.format(
            num, _smallcaps.get(player['bats'], 'ʀ'), player['name'])
        return self._profile(encoding, num, colors, s)

    def _pitching(self, encoding, id_, colors):
        if id_ not in self.data['players']:
            player = _player_default
        else:
            player = self.data['players'][id_]
        num = player['number']
        s = 'ᴘɪᴛᴄʜɪɴɢ: #{} {}ʜᴘ<br>{}<br>&nbsp;'.format(
            num, _smallcaps.get(player['throws'], 'ʀ'), player['name'])
        return self._profile(encoding, num, colors, s)

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
                log_table = table(
                    hcols=[' colspan="2" class="position-relative"'],
                    head=[logo_absolute(teamid, half['label'], 'left')],
                    bcols=[
                        ' class="position-relative"',
                        ' class="text-center text-secondary w-55p"'
                    ],
                    body=[])
                plays_table = table(
                    hcols=[' class="position-relative"'],
                    head=[logo_absolute(teamid, half['label'], 'left')],
                    body=[])
                outs = 0
                for play in half['play']:
                    if play['type'] == 'sub':
                        value = game_sub(play['value'])
                        if play['subtype'] == 'pitching':
                            log_table['body'].append([
                                self._pitching(pitching, play['value'],
                                               colors[pitching]), ''
                            ])
                            plays_table['body'].append(['Pitching: ' + value])
                        elif play['subtype'] == 'batting':
                            log_table['body'].append([
                                self._atbat(batting, play['value'],
                                            colors[batting]), ''
                            ])
                        else:
                            log_table['body'].append([value, ''])
                    elif play['type'] == 'event':
                        for s in play['sequence']:
                            pitch, balls, strikes, value = s.split(' ', 3)
                            badge = self._badge(pitch, value)
                            count = '' if 'In play' in s else '{}-{}'.format(
                                balls, strikes)
                            log_table['body'].append([badge, count])
                        value = game_sub(play['value'])
                        if play['outs']:
                            outs += play['outs']
                            value += ' ' + bold('{} out.'.format(outs))
                        if play['runs']:
                            runs[batting] += play['runs']
                            value += ' ' + bold('{} {}, {} {}.'.format(
                                encoding_to_abbreviation(away_team),
                                runs[away_team],
                                encoding_to_abbreviation(home_team),
                                runs[home_team]))
                        log_table['body'].append([value, ''])
                        if outs < 3:
                            log_table['body'].append(['&nbsp;', '&nbsp;'])
                        plays_table['body'].append([value])
                if half['footer']:
                    log_table['fcols'] = [' colspan="2"']
                    log_table['foot'] = [game_sub(half['footer'])]
                    plays_table['foot'] = [game_sub(half['footer'])]
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

        schedule_tables = []
        schedule_tables.append(self._schedule_head(away_decoding))
        schedule_tables.append(
            self._schedule_body(away_team, game_id_, schedule_data))
        schedule_tables.append(self._schedule_head(home_decoding))
        schedule_tables.append(
            self._schedule_body(home_team, game_id_, schedule_data))
        ret['tabs']['tabs'].append({
            'name': 'schedule',
            'title': 'Schedule',
            'tables': schedule_tables
        })

        ret['tabs']['tabs'].append(plays)
        return ret


# from plugin.statsplus.statsplus import Statsplus
# from util.datetime_.datetime_ import datetime_now
# from util.jinja2_.jinja2_ import env

# date = datetime_now()
# e = env()
# statsplus = Statsplus(date=date, e=e)

# for encoded_date in statsplus.data['scores']:
#     for score in statsplus.data['scores'][encoded_date]:
#         id_ = re.findall('(\d+)\.html', score)[0]
#         statsplus._extract(encoded_date, id_)
# statsplus._extract('2024-07-14T00:00:00-07:00', '1887')

# gameday = Gameday(date=date, e=e)
# gameday.data['games'] = ['1887']
# gameday._check_games()
# gameday._setup_internal(date=date)
