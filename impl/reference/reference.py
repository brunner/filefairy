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
            self._refresh()
        return Response()

    def _get(self, num, index, default):
        encoding = 'P' + num
        if encoding not in self.data['players']:
            return default
        return self.data['players'][encoding].split(' ', 4)[index]

    def _get_bats(self, num):
        return self._get(num, 2, 'R')

    def _get_name(self, num):
        return self._get(num, 4, 'Jim Unknown')

    def _get_number(self, num):
        return self._get(num, 1, '0')

    def _get_team(self, num):
        return self._get(num, 0, 'T??')

    def _get_throws(self, num):
        return self._get(num, 3, 'R')

    def _parse(self, encoding):
        num = encoding.strip('P')
        link = os.path.join(STATSPLUS_PLAYERS, 'player_{}.html'.format(num))
        data = self._call('parse_player', (link, ))

        if data is not None and self.data['players'].get(encoding) != data:
            self.data['players'][encoding] = data
            self.write()

    def _put(self, players):
        for num in players:
            encoding = 'P' + num
            if encoding not in self.data['players']:
                self._parse(encoding)

    def _refresh(self):
        for encoding in self.data['players']:
            self._parse(encoding)

    def _repl(self, m):
        return self._get_name(m.group(0).strip('P'))

    def _sub(self, text):
        pattern = '|'.join([e + r'(?!\d)' for e in self.data['players']])
        return re.sub(pattern, self._repl, text)
