#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
from utils.component.component_util import table  # noqa
from utils.datetime.datetime_util import suffix  # noqa
from utils.hash.hash_util import hash_file  # noqa
from utils.slack.slack_util import chat_post_message  # noqa
from utils.unicode.unicode_util import deunicode  # noqa


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

    def _notify_internal(self, **kwargs):
        activity = kwargs['activity']
        if activity == ActivityEnum.DOWNLOAD:
            self._render(**kwargs)
            chat_post_message(
                'fairylab',
                'League news updated.',
                attachments=self._attachments())

    def _on_message_internal(self, **kwargs):
        return ActivityEnum.NONE

    def _run_internal(self, **kwargs):
        return ActivityEnum.NONE

    def _render_internal(self, **kwargs):
        html = 'html/fairylab/recap/index.html'
        _home = self._home(**kwargs)
        return [(html, '', 'recap.html', _home)]

    def _setup_internal(self, **kwargs):
        self._render(**kwargs)

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
        for key in ['injuries', 'news', 'transactions']:
            ret[key] = self._tables(key)
        return ret

    def _tables(self, key):
        dpath = os.path.join(_root, 'download/leagues/{}.txt')
        dname = dpath.format(key)
        with open(dname, 'r') as f:
            content = f.read()

        ret = []

        cdate = ''
        match = re.findall('(\d{8})\t([^\n]+)\n', content.strip() + '\n')
        for m in match:
            if m:
                date, line = m
                if date != cdate:
                    cdate = date
                    pdate = datetime.datetime.strptime(cdate, '%Y%m%d')
                    fdate = pdate.strftime('%A, %B %-d{S}, %Y').replace(
                        '{S}', suffix(pdate.day))
                    ret.insert(0, table(cols=[''], head=[fdate]))
                body = self._rewrite_players(self._strip_teams(line))
                if ret[0]['body'] is None:
                    ret[0]['body'] = []
                ret[0]['body'].append([body])
        return ret
