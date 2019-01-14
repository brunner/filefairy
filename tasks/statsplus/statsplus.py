#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Watches the statsplus channel for ongoing sims and saves their results."""

import datetime
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/tasks/statsplus', '', _path))

from api.registrable.registrable import Registrable  # noqa
from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.datetime_.datetime_ import decode_datetime  # noqa
from common.datetime_.datetime_ import encode_datetime  # noqa
from common.json_.json_ import dumps  # noqa
from common.re_.re_ import find  # noqae
from common.record.record import decode_record  # noqa
from common.record.record import encode_record  # noqa
from common.subprocess_.subprocess_ import check_output  # noqa
from common.teams.teams import decoding_to_encoding_sub  # noqa
from common.teams.teams import encoding_keys  # noqa
from common.teams.teams import precoding_to_encoding_sub  # noqa
from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa
from data.shadow.shadow import Shadow  # noqa
from data.thread_.thread_ import Thread  # noqa

EXTRACT_DIR = re.sub(r'/tasks/statsplus', '/resource/extract', _path)
EXTRACT_BOX_SCORES = os.path.join(EXTRACT_DIR, 'box_scores')
GAMES_DIR = re.sub(r'/tasks/statsplus', '/resource/games', _path)

STATSPLUS_LINK = 'https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html'


class Statsplus(Registrable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _href():
        return ''

    @staticmethod
    def _info():
        return 'Collects results from ongoing sims.'

    @staticmethod
    def _title():
        return 'statsplus'

    def _reload_data(self, **kwargs):
        return {'statslab': ['parse_score']}

    def _shadow_data(self, **kwargs):
        return self._shadow_scores() + self._shadow_table()

    def _shadow_key(self, d, k):
        return [Shadow(destination=d, key='statsplus.' + k, info=self.data[k])]

    def _shadow_scores(self):
        return self._shadow_key('standings', 'scores')

    def _shadow_table(self):
        return self._shadow_key('standings', 'table')

    def _notify_internal(self, **kwargs):
        if kwargs['notify'] == Notify.DOWNLOAD_FINISH:
            return Response(thread_=[Thread(target='_parse_extracted_scores')])

        return Response()

    def _on_message_internal(self, **kwargs):
        obj = kwargs['obj']
        if not self._valid(obj):
            return Response()

        text = obj['text']
        s = find(r'\d{2}\/\d{2}\/\d{4}', text)
        if not s:
            return Response()

        d = datetime.datetime.strptime(s, '%m/%d/%Y')
        date = datetime_datetime_pst(d.year, d.month, d.day)

        end = self.shadow.get('download.end')
        if not end or date < decode_datetime(end):
            return Response()

        date = encode_datetime(date)
        if not self.data['started']:
            return self._start()
        elif find(r'MAJOR LEAGUE BASEBALL Final Scores', text):
            return self._save_scores(date, text)
        elif find(r'MAJOR LEAGUE BASEBALL Live Table', text):
            return self._save_table(date, text)

        return Response()

    def _parse_extracted_scores(self, *args, **kwargs):
        self.data['started'] = False

        for name in os.listdir(EXTRACT_BOX_SCORES):
            num = find(r'\D+(\d+)\.html', name)
            self._parse_score(num, None)

        self.data['scores'] = {}
        self.write()

        return Response(
            shadow=self._shadow_scores(), notify=[Notify.STATSPLUS_FINISH])

    def _parse_saved_scores(self, date_, *args, **kwargs):
        if date_ not in self.data['scores']:
            return Response()

        unvisited = {}
        for num, s in self.data['scores'][date_].items():
            if self._parse_score(num, date_) is None:
                unvisited[num] = s

        if unvisited:
            thread_ = Thread(target='_parse_saved_scores', args=(date_, ))

            if unvisited == self.data['scores'][date_]:
                return Response(thread_=[thread_])

            self.data['scores'][date_] = unvisited
            self.write()

            return Response(
                notify=[Notify.STATSPLUS_PARSE],
                shadow=self._shadow_scores(),
                thread_=[thread_])

        self.data['scores'].pop(date_, None)
        self.write()

        return Response(
            notify=[Notify.STATSPLUS_PARSE], shadow=self._shadow_scores())

    def _parse_score(self, num, date):
        out = os.path.join(GAMES_DIR, num + '.json')

        if os.path.isfile(out):
            return True

        prefix = STATSPLUS_LINK if self.data['started'] else EXTRACT_DIR
        in_ = prefix + '/box_scores/game_box_{}.html'.format(num)

        return self._call('parse_score', (in_, out, date))

    def _save_scores(self, date, text):
        self.data['scores'][date] = {}

        text = precoding_to_encoding_sub(text)
        for line in text.splitlines():
            num, s = find(r'\D+(\d+)\.html\|([^>]+)>', line)
            if not num:
                continue

            self.data['scores'][date][num] = s

        for encoding in encoding_keys():
            games = text.count(encoding)
            if games > 1:
                if date not in self.data['games']:
                    self.data['games'][date] = {}

                self.data['games'][date][encoding] = games

        self.write()
        thread_ = Thread(target='_parse_saved_scores', args=(date, ))
        return Response(shadow=self._shadow_scores(), thread_=[thread_])

    def _save_table(self, date, text):
        text = decoding_to_encoding_sub(text)
        for line in text.splitlines():
            encoding, wins = find(r'(\w+)\s(\d+)', line)
            if not encoding:
                continue

            curr = self.data['table'].get(encoding, '0-0')
            cw, cl = decode_record(curr)

            prev = self.shadow.get('standings.table', {}).get(encoding, '0-0')
            pw, pl = decode_record(prev)

            nw = int(wins) - cw - pw
            nl = self.data['games'].get(date, {}).get(encoding, 1) - nw
            next_ = encode_record(cw + nw, cl + nl)

            self.data['table'][encoding] = next_

        if date in self.data['games']:
            self.data['games'].pop(date)

        self.write()
        return Response(shadow=self._shadow_table())

    def _start(self):
        self.data['started'] = True

        self.data['games'] = {}
        self.data['scores'] = {}
        self.data['table'] = {}

        check_output(['rm', '-rf', GAMES_DIR])
        check_output(['mkdir', GAMES_DIR])

        self.write()
        return Response(notify=[Notify.STATSPLUS_START])

    @staticmethod
    def _valid(obj):
        if any(k not in obj for k in ['bot_id', 'channel', 'text']):
            return False

        if obj['bot_id'] != 'B7KJ3362Y':
            return False

        if obj['channel'] != 'C7JSGHW8G':
            return False

        return True
