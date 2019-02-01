#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Builds playable live sim pages for sim results."""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/tasks/gameday', '', _path))

from api.registrable.registrable import Registrable  # noqa
from common.elements.elements import anchor  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import table  # noqa
from common.json_.json_ import loads  # noqa
from common.teams.teams import encoding_keys  # noqa
from common.teams.teams import encoding_to_decoding  # noqa
from common.teams.teams import icon_absolute  # noqa
from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa

GAMES_DIR = re.sub(r'/tasks/gameday', '/resource/games', _path)

LEAGUES = {
    'American League': [
        ('East', ('T33', 'T34', 'T48', 'T57', 'T59')),
        ('Central', ('T35', 'T38', 'T40', 'T43', 'T47')),
        ('West', ('T42', 'T44', 'T50', 'T54', 'T58')),
    ],
    'National League': [
        ('East', ('T32', 'T41', 'T49', 'T51', 'T60')),
        ('Central', ('T36', 'T37', 'T46', 'T52', 'T56')),
        ('West', ('T31', 'T39', 'T45', 'T53', 'T55')),
    ],
}


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
        return 'Builds playable live sim pages.'

    @staticmethod
    def _title():
        return 'Gameday'

    def _render_data(self, **kwargs):
        _index_html = self._index_html(**kwargs)
        return [('gameday/index.html', '', 'gameday.html', _index_html)]

    def _notify_internal(self, **kwargs):
        if kwargs['notify'] == Notify.STATSPLUS_FINISH:
            self._render(**kwargs)
        if kwargs['notify'] == Notify.STATSPLUS_PARSE:
            self._render(**kwargs)

        return Response()

    def _index_html(self, **kwargs):
        ret = {
            'tables': [],
        }

        games = {k: [] for k in encoding_keys()}
        for name in os.listdir(GAMES_DIR):
            num = name.strip('.json')
            data = loads(os.path.join(GAMES_DIR, name))
            date = data['date']

            for team in ['away', 'home']:
                encoding = data[team + '_team']
                games[encoding].append((date, num))

        games = {k: list(sorted(v)) for k, v in games.items()}
        for league in sorted(LEAGUES):
            abbr = ''.join(s[0] for s in league.split(' '))
            for subleague, teams in LEAGUES[league]:
                body = []
                for encoding in teams:
                    decoding = encoding_to_decoding(encoding)
                    if games[encoding]:
                        _, num = games[encoding][0]
                        url = '/gameday/' + num + '/index.html'
                        text = anchor(url, decoding)
                    else:
                        text = decoding

                    body.append([cell(content=icon_absolute(encoding, text))])

                ret['tables'].append(
                    table(
                        clazz='border mb-3',
                        head=[[cell(content=(abbr + ' ' + subleague))]],
                        bcols=[col(clazz='position-relative')],
                        body=body))

        return ret
