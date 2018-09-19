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
from util.component.component import span  # noqa
from util.component.component import table  # noqa
from util.datetime_.datetime_ import decode_datetime  # noqa
from util.file_.file_ import recreate  # noqa
from util.team.team import encoding_to_decoding  # noqa
from util.team.team import encoding_to_nickname  # noqa

_fairylab_root = re.sub(r'/filefairy', '/fairylab/static', _root)
_game_path = '/resource/games/game_{}.json'


class Gameday(Registrable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
        return Response()

    def _on_message_internal(self, **kwargs):
        return Response()

    def _render_internal(self, **kwargs):
        recreate(_fairylab_root + '/gameday/')

        games = copy.deepcopy(self.data['games'])
        schedule_data = self._schedule_data(games)

        ret = []
        for id_ in games:
            with open(_root + _game_path.format(id_), 'r') as f:
                game_data = json.loads(f.read())
                away_team = encoding_to_nickname(game_data['away_team'])
                home_team = encoding_to_nickname(game_data['home_team'])
                date = decode_datetime(game_data['date']).strftime('%m/%d/%Y')
                subtitle = '{} at {}, {}'.format(away_team, home_team, date)
                game = self._game(id_, subtitle, game_data, schedule_data,
                                  **kwargs)
                html = 'gameday/{}/index.html'.format(id_)
                ret.append((html, subtitle, 'game.html', game))

        return ret

    def _run_internal(self, **kwargs):
        response = Response()
        if self._check_games(**kwargs):
            response.append_notify(Notify.BASE)
        return response

    def _setup_internal(self, **kwargs):
        self._check_games(**kwargs)
        return Response()

    def _shadow_internal(self, **kwargs):
        return []

    @staticmethod
    def _game_repl(game_data, m):
        a = m.group(0)
        if a.startswith('P'):
            return game_data['player'][a] if a in game_data['player'] else a
        if a.startswith('T'):
            return encoding_to_decoding(a)
        return a

    @staticmethod
    def _game_sub(game_data):
        pattern = '|'.join(
            list(game_data['player'].keys()) +
            [game_data['away_team'], game_data['home_team']])
        return partial(re.sub, pattern, partial(Gameday._game_repl, game_data))

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
    def _schedule_head(decoding, margin_top):
        margin_top = ' mt-3' if margin_top else ''
        return table(
            clazz='table-fixed border border-bottom-0' + margin_top,
            hcols=[' class="text-center"'],
            head=[decoding])

    @staticmethod
    def _schedule_body(encoding, id_, schedule_data):
        body = []
        for sdate, steam, ssymbol, sid in schedule_data[encoding]:
            sdate = sdate.strftime('%m/%d/%Y')
            steam = encoding_to_decoding(steam)
            stext = '{} {} {}'.format(sdate, ssymbol, steam)
            if id_ == sid:
                body.append([span(['text-secondary'], stext)])
            else:
                url = '/gameday/{}/'.format(sid)
                body.append([anchor(url, stext)])

        return table(
            clazz='table-fixed border',
            bcols=[' class="text-center"'],
            body=body)

    def _check_games(self, **kwargs):
        games = []
        for game in os.listdir(_root + '/resource/games/'):
            id_ = re.findall('game_(\d+).json', game)[0]
            games.append(id_)

        if games != self.data['games']:
            self.data['games'] = games
            self.write()
            self._render(**kwargs)
            return True

        return False

    def _game(self, id_, subtitle, game_data, schedule_data, **kwargs):
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
            'inning': [],
            'schedule': []
        }

        cs = [' colspan="2"']
        bs = [' class="w-50"', ' class="w-50"']
        game_sub = self._game_sub(game_data)
        away_team = game_data['away_team']
        away_decoding = encoding_to_decoding(away_team)
        home_team = game_data['home_team']
        home_decoding = encoding_to_decoding(home_team)

        for inning in game_data['inning']:
            _table = table(
                hcols=cs, head=[game_sub(inning['intro'])], bcols=bs, body=[])
            for pitch in inning['pitch']:
                before_list = pitch.get('before', [''])
                for before in before_list[:-1]:
                    _table['body'].append([game_sub(before), ''])
                _table['body'].append(
                    [game_sub(before_list[-1]),
                     game_sub(pitch['result'])])
                for after in pitch.get('after', []):
                    _table['body'].append(['', game_sub(after)])
            if inning['outro']:
                _table['fcols'] = cs
                _table['foot'] = [game_sub(inning['outro'])]
            ret['inning'].append(_table)

        ret['schedule'].append(self._schedule_head(away_decoding, False))
        ret['schedule'].append(
            self._schedule_body(away_team, id_, schedule_data))
        ret['schedule'].append(self._schedule_head(home_decoding, True))
        ret['schedule'].append(
            self._schedule_body(home_team, id_, schedule_data))

        return ret


# import copy  # noqa
# from plugin.statsplus.statsplus import Statsplus  # noqa
# from util.jinja2_.jinja2_ import env  # noqa
# from util.datetime_.datetime_ import datetime_now  # noqa

# e = env()
# now = datetime_now()

# statsplus = Statsplus(date=now, e=e)
# unchecked = []
# for date in statsplus.data['scores']:
#     id_ = re.findall('\{1\}(\d+).h', statsplus.data['scores'][date][0])[0]
#     unchecked.append([date, id_])
# statsplus.data['unchecked'] = unchecked
# statsplus.data['finished'] = False
# statsplus._extract_all(copy.deepcopy(unchecked), date=now)
# statsplus.data['finished'] = True
# statsplus.write()

# gameday = Gameday(date=now, e=e)
# gameday.data['games'] = []
# gameday._setup_internal(date=now)
