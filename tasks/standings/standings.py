#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tracks league standings for the regular season, including sim results."""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/tasks/standings', '', _path))

from api.renderable.renderable import Renderable  # noqa
from api.runnable.runnable import Runnable  # noqa
from api.serializable.serializable import Serializable  # noqa
from common.datetime_.datetime_ import datetime_replace  # noqa
from common.datetime_.datetime_ import decode_datetime  # noqa
from common.datetime_.datetime_ import suffix  # noqa
from common.dict_.dict_ import merge  # noqa
from common.elements.elements import dialog  # noqa
from common.elements.elements import topper  # noqa
from common.io_.io_ import read_data  # noqa
from common.json_.json_ import loads  # noqa
from common.re_.re_ import search  # noqa
from common.record.record import add_records  # noqa
from common.record.record import decode_record  # noqa
from common.record.record import encode_record  # noqa
from common.service.service import call_service  # noqa
from common.teams.teams import encoding_keys  # noqa
from common.teams.teams import encoding_to_decoding  # noqa
from common.teams.teams import encoding_to_encodings  # noqa
from common.teams.teams import encoding_to_lower  # noqa
from common.teams.teams import icon_absolute  # noqa
from types_.notify.notify import Notify  # noqa
from types_.response.response import Response  # noqa

DATA_DIR = re.sub(r'/tasks/standings', '', _path) + '/resources/data/standings'
GAMES_DIR = re.sub(r'/tasks/standings', '/resources/games', _path)

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


class Standings(Renderable, Runnable, Serializable):
    def __init__(self, **kwargs):
        super(Standings, self).__init__(**kwargs)

    @staticmethod
    def _href():
        return '/fairylab/standings/'

    @staticmethod
    def _title():
        return 'Standings'

    def _render_data(self, **kwargs):
        standings_html = self.get_standings_html(**kwargs)
        return [('standings/index.html', '', 'standings.html', standings_html)]

    def _notify_internal(self, **kwargs):
        if kwargs['notify'] == Notify.DOWNLOAD_YEAR:
            self.clear_standings(**kwargs)
        if kwargs['notify'] == Notify.STATSPLUS_FINISH:
            self.handle_finish(**kwargs)
        if kwargs['notify'] == Notify.STATSPLUS_PARSE:
            self._render(**kwargs)
        if kwargs['notify'] == Notify.STATSPLUS_SAVE:
            self._render(**kwargs)
        if kwargs['notify'] == Notify.STATSPLUS_START:
            self.handle_start(**kwargs)

        return Response()

    def clear_standings(self, **kwargs):
        for encoding in self.data['table']:
            self.data['table'][encoding] = '0-0'

        self._write()
        self._render(**kwargs)

    def create_dialog_tables(self, data):
        curr = None
        tables = []
        for start, body, foot in sorted(data, key=lambda x: x[0]):
            date = datetime_replace(start, hour=0, minute=0)
            if curr != date:
                curr = date
                d = decode_datetime(date)
                suff = suffix(d.day)
                text = d.strftime('%A, %B %-d{S}, %Y').replace('{S}', suff)
                tables.append(topper(text))

            tables.append(body)
            if foot is not None:
                tables.append(foot)

        return tables

    def handle_finish(self, **kwargs):
        self.data['finished'] = True

        for name in os.listdir(GAMES_DIR):
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

        self._write()
        self._render(**kwargs)

    def handle_start(self, **kwargs):
        self.data['finished'] = False
        self._write()

    def get_standings_html(self, **kwargs):
        ret = {
            'dialogs': [],
            'expanded': [],
            'recent': [],
        }

        statsplus_data = read_data('statsplus')
        statsplus_scores = statsplus_data['scores']
        statsplus_table = statsplus_data['table']

        nums = [
            name[:-5] for name in os.listdir(GAMES_DIR)
            if name.endswith('.json')
        ]
        data = call_service('scoreboard', 'line_scores', (nums, ))
        line = data['scores']

        pending = call_service(
            'scoreboard',
            'pending_dialog',
            (statsplus_scores, ),
        )

        d = merge(line, pending, lambda x, y: x + y, [])

        for encoding in sorted(d):
            lower = encoding_to_lower(encoding)
            decoding = encoding_to_decoding(encoding)
            tables = self.create_dialog_tables(d[encoding])
            icon = icon_absolute(encoding, decoding)
            ret['dialogs'].append(dialog(lower, icon, tables))

        pending_table = {}
        for date in statsplus_scores:
            for num, s in statsplus_scores[date].items():
                t1, t2 = search(r'(\w+) \d+, (\w+) \d+', s)
                w1, l1 = decode_record(pending_table.get(t1, '0-0'))
                pending_table[t1] = encode_record(w1 + 1, l1)
                w2, l2 = decode_record(pending_table.get(t2, '0-0'))
                pending_table[t2] = encode_record(w2, l2 + 1)

        for league in sorted(LEAGUES):
            etables, rtables = [], []
            for subleague, teams in LEAGUES[league]:
                e, r = {}, {}
                for t in teams:
                    e[t] = self.data['table'][t]
                    pw, pl = decode_record(pending_table.get(t, '0-0'))
                    sw, sl = decode_record(statsplus_table.get(t, '0-0'))
                    r[t] = encode_record(pw + sw, pl + sl)

                if not self.data['finished']:
                    e = merge(e, r, add_records, '0-0')

                r = {k: (v, k in d) for k, v in r.items()}
                etables.append((subleague, e))
                rtables.append((subleague, r))

            e = call_service('division', 'expanded_league', (league, etables))
            r = call_service('division', 'condensed_league', (league, rtables))

            ret['expanded'] += e
            ret['recent'].append(r)

        return ret
