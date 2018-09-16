#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugin/gameday', '', _path)
sys.path.append(_root)
from api.registrable.registrable import Registrable  # noqa
from core.notify.notify import Notify  # noqa
from core.response.response import Response  # noqa
from util.component.component import table  # noqa
from util.datetime_.datetime_ import decode_datetime  # noqa
from util.file_.file_ import recreate  # noqa
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

        for inning in game_data['inning']:
            _table = table(head=[inning['id']], body=[[inning['intro']]])
            for pitch in inning['pitch']:
                for before in pitch.get('before', []):
                    _table['body'].append([before])
                _table['body'].append([pitch['result']])
                for after in pitch.get('after', []):
                    _table['body'].append([after])
            if inning['outro']:
                _table['body'].append([inning['outro']])
            ret['inning'].append(_table)

        return ret
