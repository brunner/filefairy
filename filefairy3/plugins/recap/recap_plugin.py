#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import copy
import datetime
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugins/recap', '', _path)
sys.path.append(_root)
from apis.plugin.plugin_api import PluginApi  # noqa
from apis.renderable.renderable_api import RenderableApi  # noqa
from enums.activity.activity_enum import ActivityEnum  # noqa
from utils.datetime.datetime_util import suffix  # noqa
from utils.hash.hash_util import hash_file  # noqa
from utils.slack.slack_util import chat_post_message  # noqa
from utils.unicode.unicode_util import deunicode  # noqa

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
        return 'Displays news from around the league.'

    @staticmethod
    def _title():
        return 'recap'

    def _setup_internal(self, **kwargs):
        data = self.data
        original = copy.deepcopy(data)

        self._update('injuries', _injuries)
        self._update('news', _news)
        self._update('transactions', _transactions)

        if data != original:
            self.write()

        self._render(**kwargs)

    def _on_message_internal(self, **kwargs):
        return ActivityEnum.NONE

    def _run_internal(self, **kwargs):
        data = self.data
        original = copy.deepcopy(data)

        self._update('injuries', _injuries)
        self._update('news', _news)
        self._update('transactions', _transactions)

        if data != original:
            self.write()
            self._render(**kwargs)
            chat_post_message(
                'fairylab',
                'League news updated.',
                attachments=self._attachments())
            return ActivityEnum.BASE

        return ActivityEnum.NONE

    def _render_internal(self, **kwargs):
        html = 'html/fairylab/recap/index.html'
        _home = self._home(**kwargs)
        return [(html, '', 'recap.html', _home)]

    @staticmethod
    def _content(fname, split):
        with codecs.open(fname, 'r', encoding='utf-8', errors='replace') as f:
            contents = deunicode(f.read())
            if split:
                parts = contents.rsplit(split, 1)
                if len(parts) == 2:
                    return parts[1].strip() if parts[1] else split
            return contents

        return ''

    @staticmethod
    def _strip_teams(text):
        return re.sub(r'(<a href="../teams/team_\d{2}.html">)([^<]+)(</a>)',
                      r'\2', text)

    @staticmethod
    def _rewrite_players(text):
        return re.sub('<a href="../players/player',
                      '<a href="/StatsLab/reports/news/html/players/player',
                      text)

    def _home(self, **kwargs):
        ret = {
            'breadcrumbs': [{
                'href': '/fairylab/',
                'name': 'Home'
            }, {
                'href': '',
                'name': 'Recap'
            }]
        }
        ret['injuries'] = self._tables('injuries')
        ret['news'] = self._tables('news')
        ret['transactions'] = self._tables('transactions')
        return ret

    def _tables(self, key):
        data = self.data
        ret = []
        if data[key]:
            cdate = ''
            content = data[key].get('content', '')
            match = re.findall('(\d{8})\t([^\n]+)\n', content.strip() + '\n')
            for m in match:
                if m:
                    date, line = m
                    if date != cdate:
                        cdate = date
                        pdate = datetime.datetime.strptime(cdate, '%Y%m%d')
                        fdate = pdate.strftime('%A, %B %-d{S}, %Y').replace(
                            '{S}', suffix(pdate.day))
                        ret.insert(0, {
                            'cols': [''],
                            'head': [fdate],
                            'body': []
                        })
                    body = self._rewrite_players(self._strip_teams(line))
                    ret[0]['body'].append([body])
        return ret

    def _update(self, key, fname):
        if os.path.isfile(fname):
            _hash = hash_file(fname)
            if not self.data[key]['hash'] or _hash != self.data[key]['hash']:
                split = self.data[key]['content']
                _content = self._content(fname, split)
                self.data[key] = {'content': _content, 'hash': _hash}
