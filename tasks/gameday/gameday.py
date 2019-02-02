#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Builds playable live sim pages for sim results."""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/tasks/gameday', '', _path))

from api.registrable.registrable import Registrable  # noqa
from common.datetime_.datetime_ import decode_datetime  # noqa
from common.datetime_.datetime_ import suffix  # noqa
from common.dict_.dict_ import merge  # noqa
from common.elements.elements import anchor  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import table  # noqa
from common.elements.elements import topper  # noqa
from common.json_.json_ import loads  # noqa
from common.service.service import call_service  # noqa
from common.teams.teams import encoding_keys  # noqa
from common.teams.teams import encoding_to_decoding  # noqa
from common.teams.teams import icon_absolute  # noqa
from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa

GAMES_DIR = re.sub(r'/tasks/gameday', '/resource/games', _path)


class Gameday(Registrable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _href():
        return '/gameday/'

    @staticmethod
    def _info():
        return 'Builds playable live sim pages.'

    @staticmethod
    def _title():
        return 'Gameday'

    def _render_data(self, **kwargs):
        _index_html = self._index_html(**kwargs)
        return [('gameday/index.html', '', 'gameday.html', _index_html)]

    def _notify_internal(self, **kwargs):
        if kwargs['notify'] == Notify.STATSPLUS_FINISH:
            self._render(**kwargs)
        if kwargs['notify'] == Notify.STATSPLUS_PARSE:
            self._render(**kwargs)

        return Response()

    def _shadow_internal(self, **kwargs):
        self._render(**kwargs)
        return Response()

    def _index_html(self, **kwargs):
        ret = {
            'tables': [],
        }

        statsplus = self.shadow.get('statsplus.scores', {})

        line = call_service('scoreboard', 'line_scores', ())
        pending = call_service('scoreboard', 'pending_scores', (statsplus, ))
        d = merge(line, pending, lambda x, y: x + y, [])

        dates = {}
        for encoding in sorted(d):
            for date, body, foot in sorted(d[encoding], key=lambda x: x[0]):
                if date not in dates:
                    dates[date] = []
                if body in dates[date]:
                    continue
                dates[date].append(body)
                if foot is not None:
                    dates[date].append(foot)

        for date in sorted(dates):
            d = decode_datetime(date)
            suff = suffix(d.day)
            text = d.strftime('%A, %B %-d{S}, %Y').replace('{S}', suff)
            ret['tables'].append(topper(text))

            for t in dates[date]:
                ret['tables'].append(t)

            break

        return ret
