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
from common.subprocess_.subprocess_ import check_output  # noqa
from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa
from data.shadow.shadow import Shadow  # noqa
from data.thread_.thread_ import Thread  # noqa
from util.team.team import decoding_to_encoding_sub  # noqa
from util.team.team import precoding_to_encoding_sub  # noqa

GAMES_DIR = re.sub(r'/tasks/statsplus', '/resource/games', _path)


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

    def _notify_internal(self, **kwargs):
        if kwargs['notify'] == Notify.DOWNLOAD_FINISH:
            self.data['started'] = False
            self.write()

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

        if not self.data['started']:
            self._start()

        date = encode_datetime(date)
        if find(r'MAJOR LEAGUE BASEBALL Final Scores', text):
            return self._save_scores(date, text)
        elif find(r'MAJOR LEAGUE BASEBALL Live Table', text):
            return self._save_table(text)

        return Response()

    def _reload_internal(self, **kwargs):
        return {'statslab': ['parse_score']}

    def _shadow_internal(self, **kwargs):
        return [
            Shadow(
                destination='standings',
                key='statsplus.table',
                info=self.data['table'],
            ),
        ]

    def _parse_scores(self, date, *args, **kwargs):
        if date not in self.data['scores']:
            return Response()

        unvisited = []
        use_link = self.data['started']

        for num in self.data['scores'][date]:
            if self._call('parse_score', (date, num, use_link)) is None:
                unvisited.append(num)

        if unvisited:
            self.data['scores'][date] = unvisited
            self.write()

            thread_ = Thread(target='_parse_scores', args=(date, ))
            return Response(thread_=[thread_])

        self.data['scores'].pop(date)
        self.write()

        return Response()

    def _start(self):
        self.data['started'] = True

        self.data['scores'] = {}
        self.data['table'] = {}

        check_output(['rm', '-rf', GAMES_DIR])
        check_output(['mkdir', GAMES_DIR])

        self.write()

    def _save_scores(self, date, text):
        self.data['scores'][date] = []

        text = precoding_to_encoding_sub(text)
        for line in text.splitlines():
            num, s = find(r'\D+(\d+)\.html\|([^>]+)>', line)
            if not num:
                continue

            self.data['scores'][date].append(num)

        self.write()

        thread_ = Thread(target='_parse_scores', args=(date, ))
        return Response(thread_=[thread_])

    def _save_table(self, text):
        text = decoding_to_encoding_sub(text)
        for line in text.splitlines():
            encoding, wins = find(r'(\w+)\s(\d+)', line)
            if not encoding:
                continue

            curr = self.data['table'].get(encoding, '0-0')
            cw, cl = self._decode_wl(curr)

            prev = self.shadow.get('standings.table', {}).get(encoding, '0-0')
            pw, pl = self._decode_wl(prev)

            if int(wins) - cw - pw:
                curr = self._encode_wl(cw + 1, cl)
            else:
                curr = self._encode_wl(cw, cl + 1)

            self.data['table'][encoding] = curr

        self.write()

        return Response(shadow=self._shadow_internal())

    @staticmethod
    def _decode_wl(string):
        return tuple(int(x) for x in string.split('-'))

    @staticmethod
    def _encode_wl(w, l):
        return '{}-{}'.format(w, l)

    @staticmethod
    def _valid(obj):
        if any(k not in obj for k in ['bot_id', 'channel', 'text']):
            return False

        if obj['bot_id'] != 'B7KJ3362Y':
            return False

        if obj['channel'] != 'C7JSGHW8G':
            return False

        return True
