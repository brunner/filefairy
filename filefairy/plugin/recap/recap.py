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
from api.messageable.messageable import Messageable  # noqa
from api.registrable.registrable import Registrable  # noqa
from api.renderable.renderable import Renderable  # noqa
from api.runnable.runnable import Runnable  # noqa
from core.notify.notify import Notify  # noqa
from core.response.response import Response  # noqa
from core.shadow.shadow import Shadow  # noqa
from util.component.component import table  # noqa
from util.datetime_.datetime_ import suffix  # noqa
from util.slack.slack import reactions_add  # noqa
from util.standings.standings import standings_table  # noqa
from util.statslab.statslab import box_score  # noqa
from util.team.team import encoding_to_teamid  # noqa


class Recap(Messageable, Registrable, Renderable, Runnable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
            data = self.data
            data['then'] = copy.deepcopy(data['now'])

            self._standings()
            self.tables = self._tables()
            self.write()

            self._render(**kwargs)
            obj = self._chat('fairylab', 'News updated.')
            ts = obj.get('ts')
            if ts:
                if self._money():
                    reactions_add('moneybag', 'fairylab', ts)
                if self._death():
                    reactions_add('skull', 'fairylab', ts)

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
        self.tables = self._tables()
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
    def _encode(date, line):
        line = re.sub(r'(<a href="../teams/team_)(\d+)(.html">[^<]+</a>)',
                      'T' + r'\2', line)
        line = re.sub(r'(<a href="../players/player_)(\d+)(.html">[^<]+</a>)',
                      'P' + r'\2', line)
        return '{}\t{}'.format(date, line)

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

    def _death(self):
        pattern = 'will miss ([\d-]+) months'
        injuries = self.tables['injuries']
        for table_ in injuries:
            body = table_['body']
            for row in body:
                match = re.findall(pattern, row[0])
                if match:
                    for length in [int(m) for m in match[0].split('-')]:
                        if length > 6:
                            return True
        return False

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
            ret[key] = self.tables[key]

        offseason = self.shadow.get('statsplus.offseason', True)
        postseason = self.shadow.get('statsplus.postseason', True)
        if not (offseason or postseason):
            ret['standings'] = standings_table(self.data['standings'])

        return ret

    def _money(self):
        pattern = 'worth a total of \$([\d,]+)'
        transactions = self.tables['transactions']
        for table_ in transactions:
            body = table_['body']
            for row in body:
                match = re.findall(pattern, row[0])
                if match:
                    amount = int(match[0].replace(',', ''))
                    if amount > 100000000:
                        return True
        return False

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

    def _tables(self):
        ret = {}
        for key in ['injuries', 'news', 'transactions']:
            ret[key] = self._tables_internal(key)
        return ret

    def _tables_internal(self, key):
        dpath = os.path.join(_root, 'resource/extract/leagues/{}.txt')
        dname = dpath.format(key)
        with open(dname, 'r') as f:
            content = f.read()

        ret = []

        date, line = '', ''
        cdate = ''
        then = self.data['then'][key]
        match = re.findall('(\d{8})\t([^\n]+)\n', content.strip() + '\n')
        for m in match:
            if m:
                date, line = m
                if date != cdate:
                    if cdate:
                        then = ''
                    cdate = date
                    pdate = datetime.datetime.strptime(cdate, '%Y%m%d')
                    fdate = pdate.strftime('%A, %B %-d{S}, %Y').replace(
                        '{S}', suffix(pdate.day))
                    ret.insert(0, table(head=[fdate]))
                if ret[0]['body'] is None:
                    ret[0]['body'] = []
                if then and then == self._encode(date, line):
                    ret[0]['body'] = []
                else:
                    body = self._rewrite_players(self._strip_teams(line))
                    ret[0]['body'].append([body])

        ret = [table for table in ret if table['body']]
        self.data['now'][key] = self._encode(date, line)
        return ret
