#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/plugin/gameday', '', _path))
from api.registrable.registrable import Registrable  # noqa
from core.response.response import Response  # noqa
from util.team.team import encoding_to_nickname  # noqa


class Gameday(Registrable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _href():
        return '/fairylab/gameday/'

    @staticmethod
    def _info():
        return 'Exposes remote commands to admins.'

    @staticmethod
    def _title():
        return 'gameday'

    def _notify_internal(self, **kwargs):
        return Response()

    def _on_message_internal(self, **kwargs):
        return Response()

    def _render_internal(self, **kwargs):
        games = {'2022-10-09T00:00:00': ['T31']}

        ret = []
        for date in games:
            for encoding in games[date]:
                nickname = encoding_to_nickname(encoding)
                subtitle = nickname.lower().replace(' ', '')
                html = 'html/fairylab/gameday/{}/index.html'.format(subtitle)
                _game = self._game(nickname, **kwargs)
                ret.append((html, subtitle, 'game.html', _game))

        return ret

    def _run_internal(self, **kwargs):
        return Response()

    def _setup_internal(self, **kwargs):
        self._render(**kwargs)
        return Response()

    def _shadow_internal(self, **kwargs):
        return []

    def _game(self, nickname, **kwargs):
        ret = {
            'breadcrumbs': [{
                'href': '/fairylab/',
                'name': 'Home'
            }, {
                'href': '/fairylab/gameday/',
                'name': 'Gameday'
            }, {
                'href': '',
                'name': nickname
            }]
        }

        return ret
