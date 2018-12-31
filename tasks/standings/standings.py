#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tracks league standings for the regular season, including sim results."""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/tasks/standings', '', _path))

from api.registrable.registrable import Registrable  # noqa
from common.json_.json_ import filts  # noqa
from common.json_.json_ import loads  # noqa
from common.record.record import decode_record  # noqa
from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa

GAME_KEYS = ['away_runs', 'away_team', 'home_runs', 'home_team']
GAMES_DIR = re.sub(r'/tasks/standings', '/resource/games', _path)

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


class Standings(Registrable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _href():
        return '/standings/'

    @staticmethod
    def _info():
        return 'Displays regular season standings and weekly tables.'

    @staticmethod
    def _title():
        return 'standings'

    def _reload_data(self, **kwargs):
        return {'division': ['condensed_league', 'expanded_league']}

    def _render_data(self, **kwargs):
        _index_html = self._index_html(**kwargs)
        return [('standings/index.html', '', 'standings.html', _index_html)]

    def _notify_internal(self, **kwargs):
        if kwargs['notify'] == Notify.DOWNLOAD_YEAR:
            self._clear(**kwargs)
        if kwargs['notify'] == Notify.STATSPLUS_FINISH:
            self._finish(**kwargs)
        if kwargs['notify'] == Notify.STATSPLUS_PARSE:
            self._parse(**kwargs)
        if kwargs['notify'] == Notify.STATSPLUS_START:
            self._start(**kwargs)

        return Response()

    def _shadow_internal(self, **kwargs):
        self._render(**kwargs)
        return Response()

    def _clear(self, **kwargs):
        for encoding in self.data['table']:
            self.data['table'][encoding] = '0-0'

        self.write()
        self._render(**kwargs)

    def _finish(self, **kwargs):
        self.data['finished'] = True

        for name in os.listdir(GAMES_DIR):
            data = loads(os.path.join(GAMES_DIR, name))
            for team in ['away', 'home']:
                encoding = data[team + '_team']

                curr_record = self.data['table'][encoding]
                cw, cl = decode_record(curr_record)

                next_record = data[team + '_record']
                nw, nl = decode_record(next_record)

                if nw + nl > cw + cl:
                    self.data['table'][encoding] = next_record

        self.write()
        self._render(**kwargs)

    def _parse(self, **kwargs):
        for name in os.listdir(GAMES_DIR):
            num = name.strip('.json')
            if num in self.data['games']:
                continue

            data = loads(os.path.join(GAMES_DIR, name))
            self.data['games'][num] = filts(data, GAME_KEYS)

        self.write()
        self._render(**kwargs)

    def _start(self, **kwargs):
        self.data['finished'] = False
        self.data['games'] = {}
        self.shadow['statsplus.table'] = {}

        self.write()

    def _index_html(self, **kwargs):
        ret = {
            'breadcrumbs': [{
                'href': '/',
                'name': 'Fairylab'
            }, {
                'href': '',
                'name': 'Standings'
            }],
            'recent': [],
        }

        statsplus = self.shadow.get('statsplus.table', {})
        expanded = []
        for league in sorted(LEAGUES):
            rtables, etables = [], []
            for subleague, teams in LEAGUES[league]:
                r = {team: statsplus.get(team, '0-0') for team in teams}
                rtables.append((subleague, r))

                e = {team: self.data['table'][team] for team in teams}
                etables.append((subleague, e))

            ret['recent'].append(
                self._call('condensed_league', (league, rtables)))
            expanded.append(self._call('expanded_league', (league, etables)))

        ret['expanded'] = [t for pair in zip(*expanded) for t in pair]

        return ret
