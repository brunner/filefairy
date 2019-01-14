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
from common.json_.json_ import filts  # noqa
from common.json_.json_ import loads  # noqa
from common.re_.re_ import find  # noqa
from common.record.record import decode_record  # noqa
from common.record.record import encode_record  # noqa
from common.teams.teams import encoding_keys  # noqa
from common.teams.teams import encoding_to_decoding  # noqa
from common.teams.teams import encoding_to_teamid  # noqa
from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa
from data.shadow.shadow import Shadow  # noqa

GAME_KEYS = [
    'away_errors', 'away_hits', 'away_homeruns', 'away_line', 'away_record',
    'away_runs', 'away_team', 'date', 'home_errors', 'home_hits',
    'home_homeruns', 'home_line', 'home_record', 'home_runs', 'home_team',
    'losing_pitcher', 'recap', 'saving_pitcher', 'winning_pitcher',
]  # yapf: disable

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
        return {
            'division': [
                'condensed_league',
                'expanded_league',
            ],
            'scoreboard': [
                'line_score_body',
                'line_score_foot',
                'line_score_head',
                'unofficial_score_body',
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

        dialogs = {encoding: [] for encoding in encoding_keys()}
        statsplus_scores = self.shadow.get('statsplus.scores', {})
        for date in statsplus_scores:
            scores = {}
            for s in sorted(statsplus_scores[date].values()):
                for t in find(r'(\w+) \d+, (\w+) \d+', s):
                    if t not in scores:
                        scores[t] = []
                    scores[t].append(s)
            for t in sorted(scores):
                body = self._call('unofficial_score_body', (scores[t], ))
                if t == 'TCH':
                    dialogs['T35'].append((date, body, None))
                    dialogs['T36'].append((date, body, None))
                elif t == 'TLA':
                    dialogs['T44'].append((date, body, None))
                    dialogs['T45'].append((date, body, None))
                elif t == 'TNY':
                    dialogs['T48'].append((date, body, None))
                    dialogs['T49'].append((date, body, None))
                else:
                    dialogs[t].append((date, body, None))

        for num in self.data['games']:
            data = self.data['games'][num]
            body = self._call('line_score_body', (data, ))
            foot = self._call('line_score_foot', (data, ))

            dialogs[data['away_team']].append((data['date'], body, foot))
            dialogs[data['home_team']].append((data['date'], body, foot))

        for encoding in dialogs:
            if dialogs[encoding]:
                teamid = encoding_to_teamid(encoding)
                decoding = encoding_to_decoding(encoding)
                tables = []

                curr = None
                for date, body, foot in sorted(dialogs[encoding]):
                    head = self._call('line_score_head', (date, ))

                    if curr == head:
                        body['clazz'] += ' mt-3'
                    else:
                        tables += [head]

                    t = [body] if foot is None else [body, foot]
                    tables += t
                    curr = head

                ret['dialogs'].append(dialog(teamid, decoding, tables))

        statsplus_table = self.shadow.get('statsplus.table', {})
        for league in sorted(LEAGUES):
            rtables, etables = [], []
            for subleague, teams in LEAGUES[league]:
                r = {}
                e = {}

                for t in teams:
                    record = statsplus_table.get(t, '0-0')
                    rw, rl = decode_record(record)
                    tw, tl = decode_record(self.data['table'][t])
                    e[t] = encode_record(rw + tw, rl + tl)
                    r[t] = (record, bool(dialogs[t]))

                etables.append((subleague, e))
                rtables.append((subleague, r))

            ret['expanded'] += self._call('expanded_league', (league, etables))
            ret['recent'].append(
                self._call('condensed_league', (league, rtables)))

        return ret
