#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/plugins/exports', '', _path))
from apis.plugin.plugin_api import PluginApi  # noqa
from apis.renderable.renderable_api import RenderableApi  # noqa
from utils.component.component_util import table  # noqa
from utils.team.team_util import full_name  # noqa
from utils.urllib.urllib_util import urlopen  # noqa

_url = 'https://orangeandblueleaguebaseball.com/StatsLab/exports.php'


class ExportsPlugin(PluginApi, RenderableApi):
    def __init__(self, **kwargs):
        super(ExportsPlugin, self).__init__(**kwargs)

    @property
    def enabled(self):
        return True

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _href():
        return '/fairylab/exports/'

    @staticmethod
    def _title():
        return 'exports'

    @staticmethod
    def _info():
        return 'Tracks how often each manager exports.'

    def _setup(self, **kwargs):
        text = urlopen(_url)
        self.file_date = self._file_date(text)
        self.exports = self._exports(text)

    def _on_message_internal(self, **kwargs):
        pass

    def _run_internal(self, **kwargs):
        data = self.data

        text = urlopen(_url)
        file_date = self._file_date(text)

        if not file_date:
            pass
        elif not self.file_date:
            self.file_date = file_date
        elif file_date != self.file_date:
            for teamid, status in self.exports:
                if not data[teamid]['ai']:
                    s = status.lower()[0]
                    data[teamid]['form'] += s
                    while len(data[teamid]['form']) > 10:
                        data[teamid]['form'] = data[teamid]['form'][1:]
                    streak = 1
                    n, t = self._streak(teamid)
                    if s == t:
                        streak = min(int(n) + 1, 99)
                    data[teamid]['streak'] = '{}{}'.format(streak, s)
            self.file_date = file_date
            self.write()
            self._render(**kwargs)
            return True
        else:
            self.exports = self._exports(text)

    def _render_internal(self, **kwargs):
        html = 'html/fairylab/exports/index.html'
        _home = self._home(**kwargs)
        return [(html, '', 'exports.html', _home)]

    @staticmethod
    def _file_date(text):
        match = re.findall(r'League File Updated: ([^<]+)<', text)
        return match[0] if len(match) else ''

    @staticmethod
    def _exports(text):
        return re.findall(r"teams/team_(\d+)(?:[\s\S]+?)(New|Old) Export",
                          text)

    def _form(self, teamid):
        form = self.data[teamid]['form']
        return form.count('n'), form.count('o')

    def _streak(self, teamid):
        match = re.findall('(\d+)(n|o)', self.data[teamid]['streak'])
        return match[0] if len(match) else ('0', '')

    def _sorted(self, teamid):
        ret = []
        n, t = self._streak(teamid)
        n = int(n)
        if t == 'o':
            n *= -1
        ret.append(-n)
        n, o = self._form(teamid)
        ret.append(-(float(n) / ((n + o) or 1)))
        ret.append(-n)
        ret.append(-(float(1) / o if o else 2))
        ret.append(full_name(teamid))
        return ret

    def _home(self, **kwargs):
        data = self.data
        ret = {
            'breadcrumbs': [{
                'href': '/fairylab/',
                'name': 'Home'
            }, {
                'href': '',
                'name': 'Exports'
            }]
        }
        body = []
        for teamid in sorted(data, key=self._sorted):
            if data[teamid]['ai']:
                continue
            s, t = self._streak(teamid)
            if t == 'n':
                s = '+' + s
            if t == 'o':
                s = '-' + s
            n, o = self._form(teamid)
            l = '{0} - {1}'.format(n, o)
            body.append([full_name(teamid), s, l])
        ret['table'] = table(
            cols=['', 'text-center', 'text-center'],
            head=['Team', 'Streak', 'Last 10'],
            body=body)

        return ret
