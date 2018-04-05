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
from utils.ago.ago_util import delta  # noqa
from utils.component.component_util import card, table  # noqa
from utils.datetime.datetime_util import decode_datetime, encode_datetime  # noqa
from utils.slack.slack_util import chat_post_message  # noqa
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
        else:
            return

        self.data['date'] = encode_datetime(kwargs['date'])

        if self.locked:
            self._render(**kwargs)

        self.write()

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
            self.data['date'] = encode_datetime(kwargs['date'])
            self._render(**kwargs)
            self.write()

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

        n, t = self._new()
        old = self._old()
        tab = [{'key': 'Rate', 'value': '{:.0f} %'.format(float(100) * n / t)}]
        if old:
            tab.append({'key': 'Old', 'value': old})
        ts = delta(decode_datetime(data['date']), kwargs['date'])
        danger = 'simming' if self.locked else ''
        ret['live'] = card(
            title='{0} / {1}'.format(n, t), table=tab, ts=ts, danger=danger)

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
            ret['standings'].append(
                table(
                    cols=['', 'text-center w-25', 'text-center w-25'],
                    head=[division, 'Last 10', 'Streak'],
                    body=body))

        return ret

    def _lock(self):
        self.locked = True
        chat_post_message(
            'fairylab',
            'Exports tracker locked.',
            attachments=self._attachments())

        data = self.data
        for teamid, status in self.exports:
            if teamid not in data['ai']:
                s = status.lower()[0]
                data['form'][teamid] += s
                while len(data['form'][teamid]) > 10:
                    data['form'][teamid] = data['form'][teamid][1:]

    def _old(self):
        old = []
        for teamid, status in self.exports:
            if teamid not in self.data['ai'] and status == 'Old':
                old.append(abbreviation(teamid))
        return ', '.join(old)

    def _new(self):
        n, t = 0, 0
        for teamid, status in self.exports:
            if teamid not in self.data['ai']:
                t += 1
                if status == 'New':
                    n += 1
        return (n, t)

    def _sorted(self, teamid):
        ret = []
        n, o = self._form(teamid)
        s = self._streak_internal(teamid)
        ret.append(-(float(n) / ((n + o) or 1)))
        ret.append(-n)
        ret.append(-s)
        ret.append(-(float(1) / o if o else 2))
        ret.append(abbreviation(teamid))
        return ret

    def _streak(self, teamid):
        n = self._streak_internal(teamid)
        if n:
            s = 'W' if n > 0 else 'L'
            return s + str(abs(n))
        return '-'

    def _streak_internal(self, teamid):
        match = re.findall('([n]+|[o]+)$', self.data['form'].get(teamid, ''))
        if match:
            n = len(match[0])
            return n if 'n' in match[0] else -n
        return 0

    def _unlock(self):
        self.locked = False
