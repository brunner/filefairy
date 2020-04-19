#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Watches the statsplus channel for ongoing sims and saves their results."""

import datetime
import logging
import os
import re
import sys
import time

_logger = logging.getLogger('filefairy')
_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/tasks/statsplus', '', _path))

from api.messageable.messageable import Messageable  # noqa
from api.runnable.runnable import Runnable  # noqa
from api.serializable.serializable import Serializable  # noqa
from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.datetime_.datetime_ import decode_datetime  # noqa
from common.datetime_.datetime_ import encode_datetime  # noqa
from common.json_.json_ import dumps  # noqa
from common.json_.json_ import loads  # noqa
from common.messageable.messageable import messageable  # noqa
from common.re_.re_ import search  # noqae
from common.record.record import decode_record  # noqa
from common.record.record import encode_record  # noqa
from common.service.service import call_service  # noqa
from common.slack.slack import channels_history  # noqa
from common.slack.slack import chat_post_message  # noqa
from common.subprocess_.subprocess_ import check_output  # noqa
from common.teams.teams import decoding_to_encoding_sub  # noqa
from common.teams.teams import encoding_keys  # noqa
from common.teams.teams import precoding_to_encoding_sub  # noqa
from types_.debug.debug import Debug  # noqa
from types_.notify.notify import Notify  # noqa
from types_.response.response import Response  # noqa
from types_.shadow.shadow import Shadow  # noqa
from types_.thread_.thread_ import Thread  # noqa

DATA_DIR = re.sub(r'/tasks/statsplus', '', _path) + '/resources/data/statsplus'
EXTRACT_DIR = re.sub(r'/tasks/statsplus', '/resources/extract', _path)
EXTRACT_BOX_SCORES = os.path.join(EXTRACT_DIR, 'box_scores')
EXTRACT_GAME_LOGS = os.path.join(EXTRACT_DIR, 'game_logs')
GAMES_DIR = re.sub(r'/tasks/statsplus', '/resources/games', _path)

STATSPLUS_LINK = 'https://statsplus.net/oblootp/reports/news/html'
STATSPLUS_BOX_SCORES = os.path.join(STATSPLUS_LINK, 'box_scores')
STATSPLUS_GAME_LOGS = os.path.join(STATSPLUS_LINK, 'game_logs')


class Statsplus(Messageable, Runnable, Serializable):
    def __init__(self, **kwargs):
        super(Statsplus, self).__init__(**kwargs)

    def _shadow_data(self, **kwargs):
        return self.get_shadow_scores() + self.get_shadow_table()

    def _notify_internal(self, **kwargs):
        if kwargs['notify'] == Notify.DOWNLOAD_FINISH:
            return Response(thread_=[Thread(target='parse_extracted_scores')])

        return Response()

    def _on_message_internal(self, **kwargs):
        obj = kwargs['obj']
        if not self.is_valid_message(obj):
            return Response()

        text = obj['text']
        s = search(r'\d{2}\/\d{2}\/\d{4}', text)
        if not s:
            return Response()

        d = datetime.datetime.strptime(s, '%m/%d/%Y')
        date = datetime_datetime_pst(d.year, d.month, d.day)

        end = self.shadow.get('download.end')
        if not end or date < decode_datetime(end):
            return Response()

        date = encode_datetime(date)
        if not self.data['started'] and search(r'\d{4} Final Scores', text):
            return self.start()
        elif search(r'MAJOR LEAGUE BASEBALL Final Scores', text):
            return self.save_scores(date, text)

        return Response()

    @messageable
    def backfill(self, *args, **kwargs):
        if len(args) != 1:
            return Response()

        oldest = round(time.time()) - int(args[0]) * 3600
        history = channels_history('C7JSGHW8G', '', oldest)
        if not history['ok']:
            return Response(debug=[Debug(msg=history['error'])])

        self.data['started'] = False

        response = Response()
        for message in reversed(history['messages']):
            message['channel'] = 'C7JSGHW8G'
            inner = self._on_message_internal(**dict(kwargs, obj=message))
            for notify in inner.notify:
                response.append(notify=notify)
            for thread_ in inner.thread_:
                response.append(thread_=thread_)
            if inner.shadow:
                response.set_shadow(self._shadow_data())

        return response

    @messageable
    def extract(self, *args, **kwargs):
        self.data['started'] = False
        self._write()

        return Response(thread_=[Thread(target='parse_extracted_scores')])

    def cleanup(self):
        check_output(['rm', '-rf', GAMES_DIR])
        check_output(['mkdir', GAMES_DIR])

    def get_next_record(self, data, encoding, win):
        cw, cl = self.get_record(encoding, self.data['table'])
        return encode_record(cw + 1, cl) if win else encode_record(cw, cl + 1)

    def get_shadow_key(self, d, k):
        return [Shadow(destination=d, key='statsplus.' + k, info=self.data[k])]

    def get_shadow_scores(self):
        gameday_scores = self.get_shadow_key('gameday', 'scores')
        standings_scores = self.get_shadow_key('standings', 'scores')
        return gameday_scores + standings_scores

    def get_shadow_table(self):
        return self.get_shadow_key('standings', 'table')

    def parse_extracted_scores(self, *args, **kwargs):
        self.data['scores'] = {}
        self.data['table'] = {}

        if self.data['started']:
            self.data['started'] = False
        else:
            self.cleanup()

        for name in os.listdir(EXTRACT_BOX_SCORES):
            num = search(r'\D+(\d+)\.html', name)
            self.parse_score(num, None)

        for name in os.listdir(GAMES_DIR):
            data = loads(os.path.join(GAMES_DIR, name))
            for team, other in [('away', 'home'), ('home', 'away')]:
                encoding = data[team + '_team']
                win = int(data[team + '_runs']) > int(data[other + '_runs'])
                self.data['table'][encoding] = self.get_next_record(
                    data, encoding, win)

        _logger.log(logging.INFO, 'Download complete.')
        chat_post_message('fairylab', 'Download complete.')

        self._write()
        return Response(shadow=self._shadow_data(),
                        notify=[Notify.STATSPLUS_FINISH])

    def parse_saved_scores(self, date_, *args, **kwargs):
        if date_ not in self.data['scores']:
            return Response()

        unvisited = {}
        for num, s in sorted(self.data['scores'][date_].items()):
            data = self.parse_score(num, date_)
            if data is None:
                unvisited[num] = s
                continue

            for team, other in [('away', 'home'), ('home', 'away')]:
                encoding = data[team + '_team']
                win = int(data[team + '_runs']) > int(data[other + '_runs'])
                self.data['table'][encoding] = self.get_next_record(
                    data, encoding, win)

        if unvisited:
            thread_ = Thread(target='parse_saved_scores', args=(date_, ))

            if unvisited == self.data['scores'][date_]:
                return Response(thread_=[thread_])

            self.data['scores'][date_] = unvisited
            self._write()

            return Response(notify=[Notify.STATSPLUS_PARSE],
                            shadow=self._shadow_data(),
                            thread_=[thread_])

        self.data['scores'].pop(date_, None)
        self._write()
        return Response(notify=[Notify.STATSPLUS_PARSE],
                        shadow=self._shadow_data())

    def parse_score(self, num, date):
        out = os.path.join(GAMES_DIR, num + '.json')

        # TODO: Remove date check after game log 404 error is fixed.
        if date is not None and os.path.isfile(out):
            return True

        if self.data['started']:
            box = STATSPLUS_BOX_SCORES + '/game_box_{}.html'.format(num)
            log = STATSPLUS_GAME_LOGS + '/log_{}.html'.format(num)
        else:
            box = EXTRACT_BOX_SCORES + '/game_box_{}.html'.format(num)
            log = EXTRACT_GAME_LOGS + '/log_{}.txt'.format(num)

        return call_service('statslab', 'parse_game', (box, log, out, date))

    def save_scores(self, date, text):
        self.data['scores'][date] = {}

        text = precoding_to_encoding_sub(text)
        for line in text.splitlines():
            num, s = search(r'\D+(\d+)\.html\|([^>]+)>', line)
            if not num:
                continue

            self.data['scores'][date][num] = s

        self._write()
        thread_ = Thread(target='parse_saved_scores', args=(date, ))
        return Response(shadow=self.get_shadow_scores(), thread_=[thread_])

    def start(self):
        self.data['scores'] = {}
        self.data['started'] = True
        self.data['table'] = {}

        self.cleanup()

        _logger.log(logging.INFO, 'Sim in progress.')
        chat_post_message('fairylab', 'Sim in progress.')

        self._write()
        return Response(notify=[Notify.STATSPLUS_START])

    @staticmethod
    def get_record(encoding, table_):
        return decode_record(table_.get(encoding, '0-0'))

    @staticmethod
    def is_valid_message(obj):
        if any(k not in obj for k in ['bot_id', 'channel', 'text']):
            return False

        if obj['bot_id'] != 'B7KJ3362Y':
            return False

        if obj['channel'] != 'C7JSGHW8G':
            return False

        return True
