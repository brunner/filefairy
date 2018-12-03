#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import logging
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/tasks/exports', '', _path))

from api.registrable.registrable import Registrable  # noqa
from common.datetime_.datetime_ import encode_datetime  # noqa
from common.datetime_.datetime_ import timestamp  # noqa
from common.elements.elements import card  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import span  # noqa
from common.elements.elements import table  # noqa
from common.slack.slack import reactions_add  # noqa
from common.slack.slack import reactions_get  # noqa
from common.slack.slack import reactions_remove  # noqa
from common.urllib_.urllib_ import urlopen  # noqa
from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa
from util.team.team import divisions  # noqa
from util.team.team import logo_absolute  # noqa
from util.team.team import teamid_to_abbreviation  # noqa
from util.team.team import teamid_to_hometown  # noqa

logger_ = logging.getLogger('fairylab')

_emails = [(k, 'New') for k in ('33', '43', '44', '50')]
_lock_values = [Notify.STATSPLUS_SIM, Notify.LEAGUEFILE_START]
_unlock_values = [Notify.LEAGUEFILE_FINISH]
_url = 'https://orangeandblueleaguebaseball.com/StatsLab/exports.php'


class Exports(Registrable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _href():
        return '/exports/'

    @staticmethod
    def _title():
        return 'exports'

    @staticmethod
    def _info():
        return 'Displays recent manager export rate.'

    def _notify_internal(self, **kwargs):
        notify = kwargs['notify']
        data = self.data
        if not data['locked'] and notify in _lock_values:
            self._lock()
        elif data['locked'] and notify in _unlock_values:
            self._unlock()
        else:
            return Response()

        self._render(**kwargs)
        self.write()
        return Response(notify=[Notify.BASE])

    def _on_message_internal(self, **kwargs):
        return Response()

    def _run_internal(self, **kwargs):
        response = Response()

        data = self.data
        if data['locked']:
            return response

        text = urlopen(_url).decode('utf-8')
        teams = self._teams(text)
        original = copy.deepcopy(data)

        if not teams:
            return response

        if teams != self.teams:
            self.teams = teams
            self._remove()

        if not data['emails'] and any([e in _emails for e in teams]):
            self._emails()
            response.notify = [Notify.EXPORTS_EMAILS]

        if data != original:
            self.write()
            self._render(**kwargs)

        return response

    def _render_internal(self, **kwargs):
        html = 'exports/index.html'
        _home = self._home(**kwargs)
        return [(html, '', 'exports.html', _home)]

    def _setup_internal(self, **kwargs):
        text = urlopen(_url).decode('utf-8')
        self.teams = self._teams(text)
        self._remove()
        self._render(**kwargs)
        return Response()

    def _shadow_internal(self, **kwargs):
        return []

    @staticmethod
    def _teams(text):
        return re.findall(r"team_(\d+)(?:[\s\S]+?)(New|Old) Export", text)

    def _emails(self):
        self._lock_internal()
        self.data['emails'] = True

    def _form(self, teamid):
        form = self.data['form'][teamid]
        return form.count('n'), form.count('o')

    def _ghost(self):
        for teamid in self.data['form']:
            form = self.data['form'][teamid]
            if form.endswith('ooooooo'):
                return True
        return False

    def _home(self, **kwargs):
        data = self.data
        ret = {
            'breadcrumbs': [{
                'href': '/',
                'name': 'Fairylab'
            }, {
                'href': '',
                'name': 'Exports'
            }],
            'standings': []
        }

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
                body.append(
                    [cell(content=t),
                     cell(content=l),
                     cell(content=s)])
            cols = [
                col(clazz='position-relative'),
                col(clazz='text-center w-25'),
                col(clazz='text-center w-25')
            ]
            ret['standings'].append(
                table(
                    hcols=cols,
                    bcols=cols,
                    head=[
                        cell(content=division),
                        cell(content='Last 10'),
                        cell(content='Streak')
                    ],
                    body=body))

        return ret

    def _lock(self):
        data = self.data
        form = data['form']

        self._lock_internal()
        data['locked'] = True

        for teamid, status in self.teams:
            s = status.lower()[0]
            form[teamid] += s
            while len(form[teamid]) > 10:
                form[teamid] = form[teamid][1:]

            if 'n' not in form[teamid]:
                form[teamid] = ''
                if teamid not in data['ai']:
                    data['ai'].append(teamid)

    def _lock_internal(self):
        data = self.data

        if not data['emails']:
            logger_.log(logging.INFO, 'Tracker locked.')
            obj = self._chat('fairylab', 'Tracker locked.')
            data['channel'] = obj.get('channel', '')
            data['ts'] = obj.get('ts', '')

        if data['channel'] and data['ts']:
            channel, ts = data['channel'], data['ts']
            reactions = self._reactions_get(channel, ts)

            ghost = self._ghost()
            if ghost and 'ghost' not in reactions:
                reactions_add('ghost', channel, ts)
            elif not ghost and 'ghost' in reactions:
                reactions_remove('ghost', channel, ts)

            percent = self._percent()
            if percent == 100 and '100' not in reactions:
                reactions_add('100', channel, ts)
            elif percent < 50 and 'palm_tree' not in reactions:
                reactions_add('palm_tree', channel, ts)
            elif percent >= 50 and 'palm_tree' in reactions:
                reactions_remove('palm_tree', channel, ts)

    def _new(self):
        n, t = 0, 0
        for teamid, status in self.teams:
            if teamid not in self.data['ai']:
                t += 1
                if status == 'New':
                    n += 1
        return (n, t)

    def _percent(self):
        n, t = self._new()
        return (100 * n / t) if t else 0

    def _reactions_get(self, channel, ts):
        obj = reactions_get(channel, ts)
        value = []
        if obj.get('ok'):
            message = obj.get('message', {})
            reactions = message.get('reactions', [])
            for reaction in reactions:
                if 'U3ULC7DBP' in reaction.get('users', []):
                    value.append(reaction.get('name'))
        return value

    def _remove(self):
        for teamid, status in self.teams:
            if teamid in self.data['ai'] and status == 'New':
                self.data['ai'].remove(teamid)

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

    def _unlock(self):
        self.data['emails'] = False
        self.data['locked'] = False
