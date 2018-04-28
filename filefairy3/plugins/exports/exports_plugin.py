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
from utils.component.component_util import card  # noqa
from utils.component.component_util import table  # noqa
from utils.datetime.datetime_util import decode_datetime  # noqa
from utils.datetime.datetime_util import encode_datetime  # noqa
from utils.slack.slack_util import chat_post_message  # noqa
from utils.team.team_util import divisions  # noqa
from utils.team.team_util import logo_absolute  # noqa
from utils.team.team_util import teamid_to_abbreviation  # noqa
from utils.team.team_util import teamid_to_hometown  # noqa
from utils.urllib.urllib_util import urlopen  # noqa

_emails = [(k, 'New') for k in ('33', '43', '44', '50')]
_lock_activities = [ActivityEnum.SIM, ActivityEnum.UPLOAD]
_unlock_activities = [ActivityEnum.FILE]
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

    def _notify_internal(self, **kwargs):
        activity = kwargs['activity']
        data = self.data
        if not data['locked'] and activity in _lock_activities:
            self._lock()
        elif data['locked'] and activity in _unlock_activities:
            self._unlock()
        else:
            return False

        data['date'] = encode_datetime(kwargs['date'])
        self._render(**kwargs)
        self.write()
        return True

    def _on_message_internal(self, **kwargs):
        return ActivityEnum.NONE

    def _run_internal(self, **kwargs):
        ret = ActivityEnum.NONE

        data = self.data
        if data['locked']:
            return ret

        text = urlopen(_url)
        exports = self._exports(text)

        if not exports:
            return ret

        if exports != self.exports:
            self.exports = exports
            ret = ActivityEnum.BASE

        if any([True for e in exports if e in _emails]):
            self._lock()
            ret = ActivityEnum.EXPORT

        if ret != ActivityEnum.NONE:
            data['date'] = encode_datetime(kwargs['date'])
            self.write()

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

    @staticmethod
    def _secondary(text):
        s = '<span class="text-secondary">{}</span>'
        return s.format(text)

    @staticmethod
    def _success(text):
        s = '<span class="text-success border px-1">{}</span>'
        return s.format(text)

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
        title = '{:.0f}%'.format(float(100) * n / t)
        breakdown = ', '.join([
            self._success(str(n) + ' new'),
            str(t - n) + ' old',
            self._secondary(str(len(data['ai'])) + ' ai')
        ])
        status = 'Ongoing' if data['locked'] else 'Upcoming'
        info = '{0} sim contains {1}.'.format(status, breakdown)
        ts = delta(decode_datetime(data['date']), kwargs['date'])
        ret['live'] = card(title=title, info=info, table=self._table(), ts=ts)

        for division, teamids in divisions():
            body = []
            for teamid in sorted(teamids, key=self._sorted):
                t = logo_absolute(teamid, teamid_to_hometown(teamid), 'left')
                if teamid in data['ai']:
                    l, s = '-', '-'
                else:
                    n, o = self._form(teamid)
                    l = '{0} - {1}'.format(n, o)
                    s = self._streak(teamid)
                body.append([t, l, s])
            cols = [
                'class="position-relative"', ' class="text-center w-25"',
                ' class="text-center w-25"'
            ]
            ret['standings'].append(
                table(
                    hcols=cols,
                    bcols=cols,
                    head=[division, 'Last 10', 'Streak'],
                    body=body))

        return ret

    def _lock(self):
        data = self.data
        data['locked'] = True
        chat_post_message(
            'fairylab',
            'Tracker locked and exports recorded.',
            attachments=self._attachments())

        for teamid, status in self.exports:
            s = status.lower()[0]
            if teamid in data['ai']:
                if s == 'n':
                    data['ai'].remove(teamid)
                else:
                    continue

            data['form'][teamid] += s
            while len(data['form'][teamid]) > 10:
                data['form'][teamid] = data['form'][teamid][1:]

            if 'n' not in data['form'][teamid]:
                data['ai'].append(teamid)
                data['form'][teamid] = ''

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
        ret.append(teamid_to_abbreviation(teamid))
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

    def _table(self):
        div = divisions()
        size = len(self.exports) / len(div)
        cols = [''] + [' class="text-center"'] * size
        body = map(lambda t: [t[0]], div)
        for i, export in enumerate(self.exports):
            teamid, status = export
            text = teamid_to_abbreviation(teamid)
            if teamid in self.data['ai']:
                text = self._secondary(text)
            if status == 'New':
                text = self._success(text)
            body[i / size].append(text)
        return table(clazz='table-sm', hcols=cols, bcols=cols, body=body)

    def _unlock(self):
        self.data['locked'] = False
