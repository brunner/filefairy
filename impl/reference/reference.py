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

from api.registrable.registrable import Registrable  # noqa
from common.re_.re_ import find  # noqa
from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa

STATSPLUS_LINK = 'https://statsplus.net/oblootp/reports/news/html'
STATSPLUS_PLAYERS = os.path.join(STATSPLUS_LINK, 'players')


class Reference(Registrable):
    def __init__(self, **kwargs):
        super(Reference, self).__init__(**kwargs)

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _href():
        return ''

    @staticmethod
    def _info():
        return 'Stores player identity information.'

    @staticmethod
    def _title():
        return 'reference'

    def _reload_data(self, **kwargs):
        return {'statslab': ['parse_player']}

    def _notify_internal(self, **kwargs):
        notify = kwargs['notify']
        if notify == Notify.FILEFAIRY_DAY:
            encodings = list(sorted(self.data['players'].keys()))
            self._parse(encodings)
        return Response()

    def _get(self, e, index, default):
        if e not in self.data['players']:
            return default
        return self.data['players'][e].split(' ', 4)[index]

    def _parse(self, encodings):
        write = False

        for e in encodings:
            n = e.strip('P')
            link = os.path.join(STATSPLUS_PLAYERS, 'player_{}.html'.format(n))
            data = self._call('parse_player', (link, ))

            if self.data['players'].get(e) != data:
                if data is None:
                    del self.data['players'][e]
                else:
                    self.data['players'][e] = data
                write = True

        if write:
            self.write()

    def _put(self, encodings):
        encodings = [e for e in encodings if e not in self.data['players']]
        self._parse(encodings)

    def _sub(self, repl, text):
        pattern = '|'.join([e + r'(?!\d)' for e in self.data['players']])
        return re.sub(pattern, repl, text)
