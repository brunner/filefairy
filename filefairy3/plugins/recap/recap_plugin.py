#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import copy
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugins/recap', '', _path)
sys.path.append(_root)
from apis.plugin.plugin_api import PluginApi  # noqa
from apis.renderable.renderable_api import RenderableApi  # noqa
from utils.hash.hash_util import hash_file  # noqa
from utils.unicode.unicode_util import strip_accents  # noqa

_leagues = os.path.join(_root, 'file/news/txt/leagues')
_injuries = os.path.join(_leagues, 'league_100_injuries.txt')
_news = os.path.join(_leagues, 'league_100_news.txt')
_transactions = os.path.join(_leagues, 'league_100_transactions.txt')


class RecapPlugin(PluginApi, RenderableApi):
    def __init__(self, **kwargs):
        super(RecapPlugin, self).__init__(**kwargs)

    @property
    def enabled(self):
        return True

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _href():
        return '/fairylab/recap/'

    @staticmethod
    def _info():
        return 'Collects news from around the league.'

    @staticmethod
    def _title():
        return 'recap'

    def _setup(self, **kwargs):
        pass

    def _on_message_internal(self, **kwargs):
        pass

    def _run_internal(self, **kwargs):
        data = self.data
        original = copy.deepcopy(data)

        self._update('injuries', _injuries)
        self._update('news', _news)
        self._update('transactions', _transactions)

        if data != original:
            self.write()
            return True

    def _render_internal(self, **kwargs):
        pass

    @staticmethod
    def _content(fname, split):
        with codecs.open(fname, 'r', encoding='utf-8', errors='replace') as f:
            contents = strip_accents(f.read())
            if split:
                parts = contents.split(split)
                if len(parts) == 2 and parts[1]:
                    return parts[1]
            return contents

        return ''

    def _update(self, key, fname):
        if os.path.isfile(fname):
            _hash = hash_file(fname)
            if not self.data[key]['hash'] or _hash != self.data[key]['hash']:
                split = self.data[key]['content']
                _content = self._content(fname, split)
                self.data[key] = {'hash': _hash, 'content': _content}