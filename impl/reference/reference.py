#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Data store for player info which is used by multiple tasks. Non-reloadable.

The stored data is a map of player ids to player identity information. When a
caller attempts to put new ids into the map, only new ids are parsed and
stored. At the end of each day, the entire map is refreshed to have up-to-date
information.
"""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/impl/reference', '', _path))

from api.runnable.runnable import Runnable  # noqa
from api.serializable.serializable import Serializable  # noqa
from common.re_.re_ import search  # noqa
from common.service.service import call_service  # noqa
from types_.notify.notify import Notify  # noqa
from types_.response.response import Response  # noqa

DATA_DIR = re.sub(r'/impl/reference', '', _path) + '/resources/data/reference'
STATSPLUS_LINK = 'https://statsplus.net/oblootp/reports/news/html'
STATSPLUS_PLAYERS = os.path.join(STATSPLUS_LINK, 'players')


class Reference(Runnable, Serializable):
    def __init__(self, **kwargs):
        super(Reference, self).__init__(**kwargs)

    def _notify_internal(self, **kwargs):
        notify = kwargs['notify']
        if notify == Notify.FILEFAIRY_DAY:
            encodings = list(sorted(self.data['players'].keys()))
            self.parse_players(encodings)
        return Response()

    def get_attribute(self, e, index, default):
        if e not in self.data['players']:
            return default
        return self.data['players'][e].split(' ', 4)[index]

    def parse_players(self, encodings):
        changed = False

        for e in encodings:
            n = e.strip('P')
            link = os.path.join(STATSPLUS_PLAYERS, 'player_{}.html'.format(n))
            data = call_service('statslab', 'parse_player', (link, ))

            if self.data['players'].get(e) != data:
                if data is None:
                    self.data['players'].pop(e, None)
                else:
                    self.data['players'][e] = data
                changed = True

        if changed:
            self._write()

    def put_players(self, encodings):
        encodings = [e for e in encodings if e not in self.data['players']]
        self.parse_players(encodings)

    def substitute(self, repl, text):
        pattern = '|'.join([e + r'(?!\d)' for e in self.data['players']])
        return re.sub(pattern, repl, text)
