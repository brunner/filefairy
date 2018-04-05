#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/plugins/exports', '', _path))
from apis.plugin.plugin_api import PluginApi  # noqa
from apis.renderable.renderable_api import RenderableApi  # noqa
from enums.activity.activity_enum import ActivityEnum  # noqa
from utils.component.component_util import table  # noqa
from utils.team.team_util import abbreviation, divisions  # noqa
from utils.urllib.urllib_util import urlopen  # noqa

_emails = [(k, 'New') for k in ('33', '43', '44', '50')]
_lock_activities = [ActivityEnum.SIM, ActivityEnum.UPLOAD]
_unlock_activities = [ActivityEnum.FILE]
_url = 'https://orangeandblueleaguebaseball.com/StatsLab/exports.php'


class ExportsPlugin(PluginApi, RenderableApi):
    def __init__(self, **kwargs):
        super(ExportsPlugin, self).__init__(**kwargs)
        self.locked = False

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

    def _notify_internal(self, **kwargs):
        activity = kwargs['activity']
        if not self.locked and activity in _lock_activities:
            self._lock()
        elif self.locked and activity in _unlock_activities:
            self._unlock()

    def _on_message_internal(self, **kwargs):
        return ActivityEnum.NONE

    def _run_internal(self, **kwargs):
        if self.locked:
            return ActivityEnum.NONE

        text = urlopen(_url)
        exports = self._exports(text)
        ret = ActivityEnum.NONE

        if exports != self.exports:
            self.exports = exports
            ret = ActivityEnum.BASE

        if any([True for e in exports if e in _emails]):
            self._lock()
            ret = ActivityEnum.EXPORT

        if ret != ActivityEnum.NONE:
            self._render(**kwargs)

        return ret

    def _render_internal(self, **kwargs):
        html = 'html/fairylab/exports/index.html'
        _home = self._home(**kwargs)
        return [(html, '', 'exports.html', _home)]

    def _setup_internal(self, **kwargs):
        text = urlopen(_url)
        self.exports = self._exports(text)
        self._render(**kwargs)

    @staticmethod
    def _exports(text):
        return re.findall(r"team_(\d+)(?:[\s\S]+?)(New|Old) Export", text)

    def _form(self, teamid):
        form = self.data['form'][teamid]
        return form.count('n'), form.count('o')

    def _home(self, **kwargs):
        data = self.data
        ret = {
            'breadcrumbs': [{
                'href': '/fairylab/',
                'name': 'Home'
            }, {
                'href': '',
                'name': 'Exports'
            }],
            'standings': []
        }
        for division, teamids in divisions():
            body = []
            for teamid in sorted(teamids, key=self._sorted):
                if teamid in data['ai']:
                    body.append([abbreviation(teamid), '-', '-'])
                else:
                    n, o = self._form(teamid)
                    l = '{0} - {1}'.format(n, o)
                    s = self._streak(teamid)
                    body.append([abbreviation(teamid), l, s])
            ret['standings'].append(table(
                cols=['', 'text-center w-25', 'text-center w-25'],
                head=[division, 'Last 10', 'Streak'],
                body=body))

        return ret

    def _lock(self):
        self.locked = True

        data = self.data
        for teamid, status in self.exports:
            if teamid not in data['ai']:
                s = status.lower()[0]
                data['form'][teamid] += s
                while len(data['form'][teamid]) > 10:
                    data['form'][teamid] = data['form'][teamid][1:]

        self.write()

    def _sorted(self, teamid):
        ret = []
        n, o = self._form(teamid)
        ret.append(-(float(n) / ((n + o) or 1)))
        ret.append(-n)
        ret.append(-(float(1) / o if o else 2))
        ret.append(abbreviation(teamid))
        return ret

    def _streak(self, teamid):
        match = re.findall('([n]+|[o]+)$', self.data['form'].get(teamid, ''))
        if match:
            n = len(match[0])
            s = 'W' if 'n' in match[0] else 'L'
            return s + str(n)
        return '-'

    def _unlock(self):
        self.locked = False
