#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import datetime
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugins/statsplus', '', _path)
sys.path.append(_root)
from apis.plugin.plugin_api import PluginApi  # noqa
from apis.renderable.renderable_api import RenderableApi  # noqa
from enums.activity.activity_enum import ActivityEnum  # noqa
from utils.box.box_util import clarify  # noqa
from utils.component.component_util import table  # noqa
from utils.datetime.datetime_util import decode_datetime  # noqa
from utils.datetime.datetime_util import encode_datetime  # noqa
from utils.datetime.datetime_util import suffix  # noqa
from utils.standings.standings_util import sort  # noqa
from utils.team.team_util import divisions  # noqa
from utils.team.team_util import hometown_by_teamid  # noqa
from utils.team.team_util import hometowns  # noqa
from utils.team.team_util import ilogo  # noqa
from utils.team.team_util import nickname_by_hometown  # noqa

_hometowns = hometowns()
_html = 'https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/'
_game_box = 'box_scores/game_box_'
_player = 'players/player_'


class StatsplusPlugin(PluginApi, RenderableApi):
    def __init__(self, **kwargs):
        super(StatsplusPlugin, self).__init__(**kwargs)

    @property
    def enabled(self):
        return False

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _href():
        return '/fairylab/statsplus/'

    @staticmethod
    def _info():
        return 'Collects live sim results.'

    @staticmethod
    def _title():
        return 'statsplus'

    def _notify_internal(self, **kwargs):
        activity = kwargs['activity']
        if activity == ActivityEnum.DOWNLOAD:
            self.data['finished'] = True
            self.write()
        return False

    def _on_message_internal(self, **kwargs):
        obj = kwargs['obj']
        bot_id = obj.get('bot_id')
        channel = obj.get('channel')
        if bot_id != 'B7KJ3362Y' or channel != 'C7JSGHW8G':
            return ActivityEnum.NONE

        data = self.data
        original = copy.deepcopy(data)

        if self.data['finished']:
            self.data['finished'] = False
            self._clear()

        text = obj.get('text', '')
        pattern = '\d{2}\/\d{2}\/\d{4} MAJOR LEAGUE BASEBALL Final Scores\n'
        if re.findall(pattern, text):
            self._final_scores(text)

        pattern = '\d{2}\/\d{2}\/\d{4} Rain delay'
        if re.findall(pattern, text):
            self._injuries(text)

        pattern = '\d{2}\/\d{2}\/\d{4} \w+ <([^|]+)\|([^<]+)> was injured'
        if re.findall(pattern, text):
            self._injuries(text)

        pattern = '\d{2}\/\d{2}\/\d{4} <([^|]+)\|([^<]+)> (?:sets|ties)'
        if re.findall(pattern, text):
            self._highlights(text)

        if data != original:
            self.write()

        return ActivityEnum.BASE

    def _run_internal(self, **kwargs):
        if self.data['updated']:
            self.data['updated'] = False
            self._render(**kwargs)
            self.write()
            return ActivityEnum.BASE

        return ActivityEnum.NONE

    def _render_internal(self, **kwargs):
        html = 'html/fairylab/statsplus/index.html'
        _home = self._home(**kwargs)
        return [(html, '', 'statsplus.html', _home)]

    def _setup_internal(self, **kwargs):
        self._render(**kwargs)

    @staticmethod
    def _hometown_repl(matchobj):
        _hometown = matchobj.group(0)
        _nickname = nickname_by_hometown(_hometown)
        if _nickname:
            return _hometown + ' ' + _nickname
        return _hometown

    @staticmethod
    def _live_tables_header(title):
        return table(
            clazz='table-fixed border border-bottom-0 mt-3',
            hcols=[' class="text-center"'],
            bcols=[],
            head=[title],
            body=[])

    @staticmethod
    def _logo(team_tuple):
        teamid, t = team_tuple
        return ilogo(teamid, t)

    @staticmethod
    def _rewrite(date, text):
        pattern = '|'.join(_hometowns)
        text = re.sub(pattern, StatsplusPlugin._hometown_repl, text)

        match = re.findall('<([^|]+)\|([^<]+)>', text)
        if match:
            link, content = match[0]
            chlany = ['Chicago', 'Los Angeles', 'New York']
            if any(ht in content for ht in chlany):
                ddate = decode_datetime(date)
                content = clarify(ddate, link, content)
            repl = '<a href="{0}">{1}</a>'.format(link, content)
            text = re.sub('<[^|]+\|[^<]+>', repl, text)

        return text

    def _clear(self):
        self.data['scores'] = {}

    def _final_scores(self, text):
        match = re.findall('\d{2}\/\d{2}\/\d{4}', text)
        if match:
            date = datetime.datetime.strptime(match[0], '%m/%d/%Y')
            part = text.split('\n', 1)[1]
            score = part.replace(_html + _game_box, '{0}{1}').replace('*', '')
            self.data['scores'][encode_datetime(date)] = score
            self.data['updated'] = True

    def _injuries(self, text):
        match = re.findall('\d{2}\/\d{2}\/\d{4}', text)
        if match:
            date = datetime.datetime.strptime(match[0], '%m/%d/%Y')
            encoded_date = encode_datetime(date)
            if encoded_date not in self.data['injuries']:
                self.data['injuries'][encoded_date] = []

            pattern = '\w+ <[^|]+\|[^<]+> was injured [^)]+\)'
            match = re.findall(pattern, text)
            for m in match:
                injury = m.replace(_html + _player, '{0}{1}')
                self.data['injuries'][encoded_date].append(injury)
                self.data['updated'] = True

    def _highlights(self, text):
        match = re.findall('\d{2}\/\d{2}\/\d{4}', text)
        if match:
            date = datetime.datetime.strptime(match[0], '%m/%d/%Y')
            encoded_date = encode_datetime(date)
            if encoded_date not in self.data['highlights']:
                self.data['highlights'][encoded_date] = []

            pattern = '<[^|]+\|[^<]+> (?:sets|ties) [^)]+\)'
            match = re.findall(pattern, text)
            for m in match:
                highlights = m.replace(_html + _player, '{0}{1}')
                self.data['highlights'][encoded_date].append(highlights)
                self.data['updated'] = True

    def _home(self, **kwargs):
        data = self.data
        ret = {
            'breadcrumbs': [{
                'href': '/fairylab/',
                'name': 'Home'
            }, {
                'href': '',
                'name': 'Statsplus'
            }],
            'scores': [],
            'injuries': [],
            'highlights': []
        }

        status = data['status']
        if status == 'season':
            ret['live'] = self._live_tables_season()

        for date in sorted(data['scores'].keys(), reverse=True):
            ret['scores'].append(self._scores_table(date))

        for date in sorted(data['injuries'].keys(), reverse=True):
            ret['injuries'].append(self._injuries_table(date))

        for date in sorted(data['highlights'].keys(), reverse=True):
            ret['highlights'].append(self._highlights_table(date))

        return ret

    def _live_tables_season(self):
        div = divisions()
        size = len(div) / 2
        al, nl = div[:size], div[size:]
        return [
            self._live_tables_header('American League'),
            self._live_tables_season_internal(al),
            self._live_tables_header('National League'),
            self._live_tables_season_internal(nl)
        ]

    def _live_tables_season_internal(self, league):
        body = []
        for division in league:
            group = [(teamid, self._record(teamid)) for teamid in division[1]]
            inner = [self._logo(team_tuple) for team_tuple in sort(group)]
            body.append(inner)
        return table(
            clazz='table-fixed border',
            hcols=[],
            bcols=[' class="td-sm position-relative text-center w-20"'] * 5,
            head=[],
            body=body)

    def _record(self, teamid):
        ht = hometown_by_teamid(teamid)
        hw, hl = 0, 0
        for date in self.data['scores']:
            score = self.data['scores'][date]
            hw += len(re.findall(r'\|' + re.escape(ht), score))
            hl += len(re.findall(r', ' + re.escape(ht), score))
        return '{0}-{1}'.format(hw, hl)

    def _scores_table(self, date):
        lines = self.data['scores'][date].splitlines()
        body = self._table_body(date, lines, _game_box)
        head = self._table_head(date)
        return table(hcols=[''], bcols=[''], head=head, body=body)

    def _injuries_table(self, date):
        lines = self.data['injuries'][date]
        body = self._table_body(date, lines, _player)
        head = self._table_head(date)
        return table(hcols=[''], bcols=[''], head=head, body=body)

    def _highlights_table(self, date):
        lines = self.data['highlights'][date]
        body = self._table_body(date, lines, _player)
        head = self._table_head(date)
        return table(hcols=[''], bcols=[''], head=head, body=body)

    def _table_body(self, date, lines, path):
        body = []
        for line in lines:
            text = line.format(_html, path)
            link = self._rewrite(date, text)
            body.append([link])
        return body

    def _table_head(self, date):
        ddate = decode_datetime(date)
        fdate = ddate.strftime('%A, %B %-d{S}, %Y')
        return [fdate.replace('{S}', suffix(ddate.day))]
