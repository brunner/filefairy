#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Builds playable live sim pages for sim results."""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/tasks/gameday', '', _path))

from api.registrable.registrable import Registrable  # noqa
from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.datetime_.datetime_ import datetime_replace  # noqa
from common.datetime_.datetime_ import decode_datetime  # noqa
from common.datetime_.datetime_ import encode_datetime  # noqa
from common.datetime_.datetime_ import suffix  # noqa
from common.dict_.dict_ import merge  # noqa
from common.elements.elements import anchor  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import row  # noqa
from common.elements.elements import topper  # noqa
from common.io_.io_ import io_read  # noqa
from common.io_.io_ import io_write  # noqa
from common.json_.json_ import loads  # noqa
from common.os_.os_ import listdirs  # noqa
from common.service.service import call_service  # noqa
from common.subprocess_.subprocess_ import check_output  # noqa
from common.teams.teams import encoding_keys  # noqa
from common.teams.teams import encoding_to_decoding  # noqa
from common.teams.teams import icon_absolute  # noqa
from types_.notify.notify import Notify  # noqa
from types_.response.response import Response  # noqa

CONTAINING_DIR = re.sub(r'/filefairy/tasks/gameday', '', _path)
DATA_DIR = re.sub(r'/tasks/gameday', '', _path) + '/resources/data/gameday'
FAIRYLAB_DIR = CONTAINING_DIR + '/fairylab/static'
GAMEDAY_DIR = os.path.join(FAIRYLAB_DIR, 'gameday')

GAMES_DIR = re.sub(r'/tasks/gameday', '/resources/games', _path)


class Gameday(Registrable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.read()

    @staticmethod
    def _href():
        return '/fairylab/gameday/'

    @staticmethod
    def _title():
        return 'Gameday'

    def _render_data(self, **kwargs):
        _index_html = self._index_html(**kwargs)
        datas = [('gameday/index.html', '', 'gameday.html', _index_html)]

        nums = listdirs(GAMEDAY_DIR)
        for name in os.listdir(GAMES_DIR):
            num = name.strip('.json')
            if num in nums:
                continue

            _in = os.path.join(GAMES_DIR, name)
            _livesim_html = call_service('livesim', 'get_html', (_in, ))
            if _livesim_html:
                url = 'gameday/{}/index.html'.format(num)
                datas.append((url, num, 'livesim.html', _livesim_html))
                check_output(['mkdir', os.path.join(GAMEDAY_DIR, num)])

        return datas

    def _notify_internal(self, **kwargs):
        if kwargs['notify'] == Notify.STATSPLUS_FINISH:
            if not self.data['started']:
                self._rm()
            self.data['started'] = False
            self._render(**kwargs)
        if kwargs['notify'] == Notify.STATSPLUS_PARSE:
            self._render(**kwargs)
        if kwargs['notify'] == Notify.STATSPLUS_START:
            self._rm()
            self.data['started'] = True

        return Response()

    def _shadow_internal(self, **kwargs):
        self._render(**kwargs)
        return Response()

    def _index_html(self, **kwargs):
        ret = {
            'days': [],
            'dialogs': [],
        }

        nums = [
            name[:-5] for name in os.listdir(GAMES_DIR)
            if name.endswith('.json')
        ]
        data = call_service('scoreboard', 'line_scores', (nums, ), hidden=True)
        line = data['scores']

        ret['dialogs'] += data['dialogs']

        dates = {}
        for e in sorted(line):
            for start, body, foot in sorted(line[e], key=lambda x: x[0]):
                date = datetime_replace(start, hour=0, minute=0)
                if date not in dates:
                    dates[date] = []

                dates[date].append((start, body, foot))

        statsplus_scores = self.shadow.get('statsplus.scores', {})
        data = call_service(
            'scoreboard',
            'pending_carousel',
            (statsplus_scores, ),
            hidden=True,
        )
        pending = data['scores']
        ret['dialogs'] += data['dialogs']

        for date in sorted(pending):
            if date not in dates:
                dates[date] = []

            for start, body in pending[date]:
                dates[date].append((start, body, None))

        for date in sorted(dates):
            d = decode_datetime(date)
            suff = suffix(d.day)
            text = d.strftime('%A, %B %-d{S}, %Y').replace('{S}', suff)
            tables = [topper(text)]

            for _, body, foot in sorted(dates[date], key=lambda x: x[0]):
                if body in tables:
                    continue

                tables.append(body)
                if foot is not None:
                    tables.append(foot)

            ret['days'].append(tables)

        return ret

    def _rm(self):
        check_output(['rm', '-rf', GAMEDAY_DIR])
        check_output(['mkdir', GAMEDAY_DIR])
        pass

    def read(self, *args, **kwargs):
        self.data = io_read(self._name())

    def write(self, *args, **kwargs):
        io_write(self._name(), self.data)


# from common.datetime_.datetime_ import datetime_now
# from common.jinja2_.jinja2_ import env
# from common.reference.reference import set_reference
# from common.service.service import reload_service_for_test
# from impl.reference.reference import Reference

# date = datetime_now()
# e = env()

# reference = Reference(date=date, e=e)
# set_reference(reference)

# reload_service_for_test('roster')
# reload_service_for_test('state')
# reload_service_for_test('tables')
# reload_service_for_test('livesim')
# reload_service_for_test('scoreboard')
# reload_service_for_test('uniforms')

# gameday = Gameday(date=date, e=e)
# gameday._rm()
# gameday._render(date=date)
