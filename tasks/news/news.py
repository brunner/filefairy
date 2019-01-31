#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/tasks/news', '', _path))

from api.registrable.registrable import Registrable  # noqa
from common.datetime_.datetime_ import decode_datetime  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import table  # noqa
from common.datetime_.datetime_ import suffix  # noqa
from common.json_.json_ import loads  # noqa
from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa

EXTRACT_DIR = re.sub(r'/tasks/news', '/resource/extract', _path)
EXTRACT_LEAGUES = os.path.join(EXTRACT_DIR, 'leagues')


class News(Registrable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _href():
        return '/news/'

    @staticmethod
    def _info():
        return 'Reports league injuries and transactions.'

    @staticmethod
    def _title():
        return 'news'

    def _render_data(self, **kwargs):
        _index_html = self._index_html(**kwargs)
        return [('news/index.html', '', 'news.html', _index_html)]

    def _notify_internal(self, **kwargs):
        if kwargs['notify'] == Notify.STATSPLUS_FINISH:
            self._render(**kwargs)
        return Response()

    def _index_html(self, **kwargs):
        ret = {
            'breadcrumbs': [{
                'href': '/',
                'name': 'Fairylab'
            }, {
                'href': '',
                'name': 'News'
            }]
        }

        for name in ['injuries', 'news', 'transactions']:
            ret[name] = self._tables(name)

        return ret

    def _tables(self, name):
        data = loads(os.path.join(EXTRACT_LEAGUES, name + '.json'))

        tables = []
        for date in sorted(data, reverse=True):
            d = decode_datetime(date)
            suf = suffix(d.day)
            head = d.strftime('%A, %B %-d{S}, %Y').replace('{S}', suf)
            body = [[cell(content=text)] for text in data[date]]

            tables.append(
                table(
                    clazz='border mt-3',
                    head=[[cell(content=head)]],
                    body=body))

        return tables
