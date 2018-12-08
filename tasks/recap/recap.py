#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import datetime
import logging
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/tasks/recap', '', _path)
sys.path.append(_root)
from api.registrable.registrable import Registrable  # noqa
from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa
from data.shadow.shadow import Shadow  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import table  # noqa
from common.datetime_.datetime_ import suffix  # noqa
from common.slack.slack import reactions_add  # noqa
from util.standings.standings import standings_table  # noqa
from util.statslab.statslab import parse_game_data  # noqa
from util.team.team import decoding_to_nickname  # noqa
from util.team.team import encoding_to_teamid  # noqa
from util.team.team import teamid_to_decoding  # noqa
from util.team.team import teamid_to_nickname  # noqa

logger_ = logging.getLogger('filefairy')


class Recap(Registrable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _href():
        return '/recap/'

    @staticmethod
    def _info():
        return 'Surfaces league standings and logs.'

    @staticmethod
    def _title():
        return 'recap'

    def _notify_internal(self, **kwargs):
        notify = kwargs['notify']
        response = Response()
        if notify == Notify.LEAGUEFILE_DOWNLOAD:
            data = self.data
            data['then'] = copy.deepcopy(data['now'])

            self._standings()
            self.tables = self._tables()
            self.write()

            self._render(**kwargs)
            obj = self._chat('fairylab', 'News updated.')
            channel = obj.get('channel')
            ts = obj.get('ts')
            if channel and ts:
                if self._money():
                    reactions_add('moneybag', channel, ts)
                if self._death():
                    reactions_add('skull', channel, ts)

            response.notify = [Notify.BASE]
            response.shadow = self._shadow_internal(**kwargs)
        return response

    def _on_message_internal(self, **kwargs):
        return Response()

    def _run_internal(self, **kwargs):
        return Response()

    def _render_internal(self, **kwargs):
        html = 'recap/index.html'
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
                info=self.data['standings'])
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
        return re.sub(
            '<a href="../players/player',
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/repo' +
            'rts/news/html/players/player', text)

    @staticmethod
    def _teams():
        return sorted([(teamid_to_decoding(str(t)),
                        teamid_to_nickname(str(t)).replace(' ', '').lower())
                       for t in range(31, 60)])

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
                match = re.findall(pattern, row[0]['content'])
                if match:
                    for length in [int(m) for m in match[0].split('-')]:
                        if length > 6:
                            return True
        return False

    def _home(self, **kwargs):
        ret = {
            'breadcrumbs': [{
                'href': '/',
                'name': 'Fairylab'
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
                match = re.findall(pattern, row[0]['content'])
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
            _game_data = parse_game_data(None, bdname, '')
            if _game_data['ok']:
                away_teamid = encoding_to_teamid(_game_data['away_team'])
                away_record = _game_data['away_record']
                self._record(away_teamid, away_record)
                home_teamid = encoding_to_teamid(_game_data['home_team'])
                home_record = _game_data['home_record']
                self._record(home_teamid, home_record)

        if data != original:
            self.write()

    def _tables(self, team=''):
        ret = {}
        for key in ['injuries', 'news', 'transactions']:
            ret[key] = self._tables_internal(key, team)
        return ret

    def _tables_internal(self, key, team):
        ret = []

        dpath = os.path.join(_root, 'resource/extract/leagues/{}.txt')
        dname = dpath.format(key)
        if not os.path.isfile(dname):
            return ret

        with open(dname, 'r') as f:
            content = f.read()

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
                    ret.insert(0, table(head=[cell(content=fdate)]))
                if ret[0]['body'] is None:
                    ret[0]['body'] = []
                if then and then == self._encode(date, line):
                    ret[0]['body'] = []
                else:
                    body = self._rewrite_players(self._strip_teams(line))
                    if not team or team in body:
                        ret[0]['body'].append([cell(content=body)])

        ret = [table for table in ret if table['body']]
        self.data['now'][key] = self._encode(date, line)
        return ret
