#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import datetime
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugin/recap', '', _path)
sys.path.append(_root)
from api.plugin.plugin import Plugin  # noqa
from api.renderable.renderable import Renderable  # noqa
from core.notify.notify import Notify  # noqa
from core.response.response import Response  # noqa
from core.shadow.shadow import Shadow  # noqa
from util.component.component import table  # noqa
from util.datetime_.datetime_ import suffix  # noqa
from util.standings.standings import standings_table  # noqa
from util.statslab.statslab import box_score  # noqa
from util.team.team import encoding_to_teamid  # noqa


class Recap(Plugin, Renderable):
    def __init__(self, **kwargs):
        super(Recap, self).__init__(**kwargs)

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
        return 'Surfaces league standings and logs.'

    @staticmethod
    def _title():
        return 'recap'

    def _notify_internal(self, **kwargs):
        notify = kwargs['notify']
        response = Response()
        if notify == Notify.DOWNLOAD_FINISH:
            self._standings()
            self._render(**kwargs)
            self._chat('fairylab', 'News updated.')
            response.notify = [Notify.BASE]
            response.shadow = self._shadow_internal(**kwargs)
        return response

    def _on_message_internal(self, **kwargs):
        return Response()

    def _run_internal(self, **kwargs):
        return Response()

    def _render_internal(self, **kwargs):
        html = 'html/fairylab/recap/index.html'
        _home = self._home(**kwargs)
        return [(html, '', 'recap.html', _home)]

    def _setup_internal(self, **kwargs):
        self._render(**kwargs)
        return Response()

    def _shadow_internal(self, **kwargs):
        return [
            Shadow(
                destination='statsplus',
                key='recap.standings',
                data=self.data['standings'])
        ]

    @staticmethod
    def _strip_teams(text):
        return re.sub(r'(<a href="../teams/team_\d{2}.html">)([^<]+)(</a>)',
                      r'\2', text)

    @staticmethod
    def _rewrite_players(text):
        return re.sub('<a href="../players/player',
                      '<a href="/StatsLab/reports/news/html/players/player',
                      text)

    @staticmethod
    def _total(record):
        if record.count('-') == 1:
            return sum(int(n) for n in record.split('-'))
        return 0

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

        offseason = self.shadow.get('statsplus.offseason', True)
        postseason = self.shadow.get('statsplus.postseason', True)
        if not (offseason or postseason):
            ret['standings'] = standings_table(self.data['standings'], 0)

        return ret

    def _record(self, teamid, record):
        ntotal = self._total(record)
        ttotal = self._total(self.data['standings'].get(teamid, ''))
        if ntotal > ttotal:
            self.data['standings'][teamid] = record

    def _standings(self):
        data = self.data
        original = copy.deepcopy(data)

        dpath = os.path.join(_root, 'resource/extract/box_scores')
        for box in os.listdir(dpath):
            bdname = os.path.join(dpath, box)
            box_score_ = box_score(bdname)
            if box_score_['ok']:
                away_teamid = encoding_to_teamid(box_score_['away_team'])
                away_record = box_score_['away_record']
                self._record(away_teamid, away_record)
                home_teamid = encoding_to_teamid(box_score_['home_team'])
                home_record = box_score_['home_record']
                self._record(home_teamid, home_record)

        if data != original:
            self.write()

    def _tables(self, key):
        dpath = os.path.join(_root, 'resource/extract/leagues/{}.txt')
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
                    ret.insert(0, table(hcols=[''], bcols=[''], head=[fdate]))
                body = self._rewrite_players(self._strip_teams(line))
                if ret[0]['body'] is None:
                    ret[0]['body'] = []
                ret[0]['body'].append([body])
        return ret
