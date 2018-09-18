#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
from util.component.component import replace  # noqa
from util.component.component import show  # noqa
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

        ret = []
        for id_ in self.data['games']:
            with open(_root + _game_path.format(id_), 'r') as f:
                game_data = json.loads(f.read())
                away_team = encoding_to_nickname(game_data['away_team'])
                home_team = encoding_to_nickname(game_data['home_team'])
                date = decode_datetime(game_data['date']).strftime('%m/%d/%Y')
                subtitle = '{} at {}, {}'.format(away_team, home_team, date)
                game = self._game(game_data, subtitle, **kwargs)
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

    def _game(self, game_data, subtitle, **kwargs):
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
            'inning': []
        }

        cs = [' colspan="2"']
        bs = [' class="w-50"', ' class="w-50"']
        game_sub = self._game_sub(game_data)
        away_team = game_data['away_team']
        away_decoding = encoding_to_decoding(away_team)
        home_team = game_data['home_team']
        home_decoding = encoding_to_decoding(home_team)
        date_decoding = decode_datetime(game_data['date']).strftime('%m/%d/%Y')

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

        ret['schedule'] = [
            table(
                clazz='table-fixed border border-bottom-0',
                hcols=[' class="text-center"'],
                head=[away_decoding]),
            table(
                clazz='table-fixed border border-bottom-0',
                bcols=[' class="text-center"'],
                body=[
                    [
                        replace('Previous game', 'Previous game not found') +
                        ' - ' + replace('Next game', 'Next game not found')
                    ],
                ]),
            table(
                clazz='table-fixed border',
                bcols=[' class="text-center"'],
                body=[
                    [
                        show('schedule-' + away_team.lower(),
                             'Toggle full schedule')
                    ],
                ]),
            table(
                clazz='table-fixed border collapse',
                id_='schedule-' + away_team.lower(),
                bcols=[' class="text-center"'],
                body=[
                    [
                        span(['text-secondary'], '{} @ {}'.format(
                            date_decoding, home_decoding))
                    ],
                ]),
            table(
                clazz='table-fixed border border-bottom-0 mt-3',
                hcols=[' class="text-center"'],
                head=[home_decoding]),
            table(
                clazz='table-fixed border border-bottom-0',
                bcols=[' class="text-center"'],
                body=[
                    [
                        replace('Previous game', 'Previous game not found') +
                        ' - ' + replace('Next game', 'Next game not found')
                    ],
                ]),
            table(
                clazz='table-fixed border',
                bcols=[' class="text-center"'],
                body=[
                    [
                        show('schedule-' + home_team.lower(),
                             'Toggle full schedule')
                    ],
                ]),
            table(
                clazz='table-fixed border collapse',
                id_='schedule-' + home_team.lower(),
                bcols=[' class="text-center"'],
                body=[
                    [
                        span(['text-secondary'], '{} v {}'.format(
                            date_decoding, away_decoding))
                    ],
                ]),
        ]

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
