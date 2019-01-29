#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tracks league standings for the regular season, including sim results."""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/tasks/standings', '', _path))

from api.registrable.registrable import Registrable  # noqa
from common.elements.elements import dialog  # noqa
from common.json_.json_ import loads  # noqa
from common.re_.re_ import find  # noqa
from common.record.record import add_records  # noqa
from common.record.record import decode_record  # noqa
from common.record.record import encode_record  # noqa
from common.teams.teams import encoding_keys  # noqa
from common.teams.teams import encoding_to_decoding  # noqa
from common.teams.teams import encoding_to_encodings  # noqa
from common.teams.teams import encoding_to_teamid  # noqa
from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa
from data.shadow.shadow import Shadow  # noqa

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
        return 'Tracks regular season and weekly tables.'

    @staticmethod
    def _title():
        return 'standings'

    def _reload_data(self, **kwargs):
        return {
            'division': [
                'condensed_league',
                'expanded_league',
            ],
            'scoreboard': [
                'line_score_body',
                'line_score_foot',
                'line_score_head',
                'pending_score_body',
            ],
        }

    def _render_data(self, **kwargs):
        _index_html = self._index_html(**kwargs)
        return [('standings/index.html', '', 'standings.html', _index_html)]

    def _shadow_data(self, **kwargs):
        return [
            Shadow(
                destination='statsplus',
                key='standings.table',
                info=self.data['table'])
        ]

    def _notify_internal(self, **kwargs):
        if kwargs['notify'] == Notify.DOWNLOAD_YEAR:
            self._clear(**kwargs)
        if kwargs['notify'] == Notify.STATSPLUS_FINISH:
            self._finish(**kwargs)
        if kwargs['notify'] == Notify.STATSPLUS_PARSE:
            self._render(**kwargs)
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

    def _dialog_tables(self, data):
        curr = None
        tables = []
        for date, body, foot in sorted(data, key=lambda x: x[0]):
            head = self._call('line_score_head', (date, ))
            if curr == head:
                body['clazz'] += ' mt-3'
            else:
                tables += [head]
            curr = head

            tables.append(body)
            if foot is not None:
                tables.append(foot)

        return tables

    def _finish(self, **kwargs):
        self.data['finished'] = True

        for name in os.listdir(GAMES_DIR):
            if not name.startswith('game_box_'):
                continue

            data = loads(os.path.join(GAMES_DIR, name))
            for team in ['away', 'home']:
                encoding = data[team + '_team']

                curr_record = self.data['table'][encoding]
                cw, cl = decode_record(curr_record)

                next_record = data[team + '_record']
                if next_record:
                    nw, nl = decode_record(next_record)
                    if nw + nl > cw + cl:
                        self.data['table'][encoding] = next_record

        self.write()
        self._render(**kwargs)

    def _line_scores(self):
        d = {}
        for name in os.listdir(GAMES_DIR):
            if not name.startswith('game_box_'):
                continue

            data = loads(os.path.join(GAMES_DIR, name))
            body = self._call('line_score_body', (data, ))
            foot = self._call('line_score_foot', (data, ))

            for team in ['away', 'home']:
                e = data[team + '_team']
                if e not in d:
                    d[e] = []
                d[e].append((data['date'], body, foot))

        return d

    def _pending_scores(self):
        d = {}
        statsplus_scores = self.shadow.get('statsplus.scores', {})
        for date in statsplus_scores:
            scores = {}
            for s in sorted(statsplus_scores[date].values()):
                for t in find(r'(\w+) \d+, (\w+) \d+', s):
                    if t not in scores:
                        scores[t] = []
                    scores[t].append(s)

            for t in sorted(scores):
                body = self._call('pending_score_body', (scores[t], ))
                for e in encoding_to_encodings(t):
                    if e not in d:
                        d[e] = []
                    d[e].append((date, body, None))

        return d

    def _start(self, **kwargs):
        self.data['finished'] = False
        self.shadow['statsplus.scores'] = {}
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
            'dialogs': [],
            'expanded': [],
            'recent': [],
        }

        line_scores = self._line_scores()
        pending_scores = self._pending_scores()
        d = self._merge(line_scores, pending_scores, lambda x, y: x + y, [])

        for encoding in sorted(d):
            teamid = encoding_to_teamid(encoding)
            decoding = encoding_to_decoding(encoding)
            tables = self._dialog_tables(d[encoding])
            ret['dialogs'].append(dialog(teamid, decoding, tables))

        statsplus_table = self.shadow.get('statsplus.table', {})
        for league in sorted(LEAGUES):
            etables, rtables = [], []
            for subleague, teams in LEAGUES[league]:
                e = {t: self.data['table'][t] for t in teams}
                r = {t: statsplus_table.get(t, '0-0') for t in teams}
                if not self.data['finished']:
                    e = self._merge(e, r, add_records, '0-0')

                r = {k: (v, k in d) for k, v in r.items()}
                etables.append((subleague, e))
                rtables.append((subleague, r))

            ret['expanded'] += self._call('expanded_league', (league, etables))
            ret['recent'].append(
                self._call('condensed_league', (league, rtables)))

        return ret

    @staticmethod
    def _merge(d1, d2, f, empty):
        keys = set(d1).union(d2)
        return {k: f(d1.get(k, empty), d2.get(k, empty)) for k in keys}
