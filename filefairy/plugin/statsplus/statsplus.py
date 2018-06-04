#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import datetime
import logging
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugin/statsplus', '', _path)
sys.path.append(_root)
from api.messageable.messageable import Messageable  # noqa
from api.registrable.registrable import Registrable  # noqa
from api.renderable.renderable import Renderable  # noqa
from api.runnable.runnable import Runnable  # noqa
from core.notify.notify import Notify  # noqa
from core.response.response import Response  # noqa
from core.shadow.shadow import Shadow  # noqa
from core.task.task import Task  # noqa
from util.component.component import table  # noqa
from util.datetime_.datetime_ import decode_datetime  # noqa
from util.datetime_.datetime_ import encode_datetime  # noqa
from util.datetime_.datetime_ import suffix  # noqa
from util.standings.standings import sort  # noqa
from util.standings.standings import standings_table  # noqa
from util.statslab.statslab import box_score  # noqa
from util.statslab.statslab import player  # noqa
from util.team.team import chlany  # noqa
from util.team.team import decoding_to_encoding_sub  # noqa
from util.team.team import divisions  # noqa
from util.team.team import encoding_to_chlany  # noqa
from util.team.team import encoding_to_crosstown  # noqa
from util.team.team import encoding_to_decoding  # noqa
from util.team.team import encoding_to_decoding_sub  # noqa
from util.team.team import encoding_to_precoding  # noqa
from util.team.team import encoding_to_teamid  # noqa
from util.team.team import encodings  # noqa
from util.team.team import logo_absolute  # noqa
from util.team.team import logo_inline  # noqa
from util.team.team import precoding_to_encoding_sub  # noqa
from util.team.team import precodings  # noqa
from util.team.team import teamid_to_encoding  # noqa
from util.team.team import teamid_to_hometown  # noqa
from util.team.team import teamids  # noqa

logger_ = logging.getLogger('fairylab')

_html = 'https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/'
_game_box = 'box_scores/game_box_'
_player = 'players/player_'
_shorten = '{}(?:{}|{})'.format(_html, _game_box, _player)
_encodings = '|'.join(encodings())
_precodings = '|'.join(precodings())
_url_pattern = '<([^|]+)\|([^<]+)>'
_chlany = chlany()
_lhclazz = 'table-fixed border border-bottom-0 mt-3'
_lhcols = [' class="text-center"']
_lbclazz = 'table-fixed border'
_lbpcols = [
    ' class="position-relative w-40"', ' class="text-center w-10"',
    ' class="text-center w-10"', ' class="position-relative text-right w-40"'
]
_lbrcols = [' class="td-sm position-relative text-center w-20"'] * 5


class Statsplus(Messageable, Registrable, Renderable, Runnable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _href():
        return '/fairylab/statsplus/'

    @staticmethod
    def _info():
        return 'Collects results from ongoing sim.'

    @staticmethod
    def _title():
        return 'statsplus'

    def _notify_internal(self, **kwargs):
        notify = kwargs['notify']
        if notify == Notify.DOWNLOAD_FINISH:
            self.data['finished'] = True
            self.write()
        if notify == Notify.DOWNLOAD_YEAR:
            self.data['offseason'] = True
            self.write()
        return Response()

    def _on_message_internal(self, **kwargs):
        response = Response()

        obj = kwargs['obj']
        bot_id = obj.get('bot_id')
        channel = obj.get('channel')
        if bot_id != 'B7KJ3362Y' or channel != 'C7JSGHW8G':
            return response

        data = self.data
        original = copy.deepcopy(data)

        text = obj.get('text', '')
        date = re.findall('\d{2}\/\d{2}\/\d{4}', text)
        if not date:
            return response

        ddate = datetime.datetime.strptime(date[0], '%m/%d/%Y')
        edate = encode_datetime(ddate)
        ndate = decode_datetime(self.shadow.get('download.now', edate))
        if ddate < ndate:
            return response

        response.append_notify(Notify.BASE)
        shadow = False

        if self.data['finished']:
            self.data['finished'] = False
            self.data['started'] = True
            self._clear()

        highlights = '<[^|]+\|[^<]+> (?:sets|ties) [^)]+\)'
        pattern = '<([^|]+)\|([^<]+)> (?:sets|ties)'
        if re.findall(pattern, text):
            self._handle_key('highlights', edate, text, highlights, True)

        injuries = '\w+ <[^|]+\|[^<]+> was injured [^)]+\)'
        pattern = '\w+ <([^|]+)\|([^<]+)> was injured'
        if re.findall(pattern, text):
            self._handle_key('injuries', edate, text, injuries, True)

        scores = '<[^|]+\|[^<]+>'
        pattern = 'MAJOR LEAGUE BASEBALL Final Scores\n'
        if re.findall(pattern, text):
            self._handle_key('scores', edate, text, scores, False)
            if data['offseason'] and data['postseason']:
                data['postseason'] = False
                shadow = True
            if data['offseason']:
                self._render(**kwargs)
            if self.data['started']:
                self.data['started'] = False
                self._chat('fairylab', 'Sim in progress.')
                logger_.log(logging.INFO, 'Sim in progress.')
                response.notify = [Notify.STATSPLUS_SIM]

        pattern = 'MAJOR LEAGUE BASEBALL Live Table'
        if re.findall(pattern, text):
            self._handle_table(edate, text)
            if data['offseason']:
                data['offseason'] = False
                shadow = True
            else:
                self._render(**kwargs)

        if shadow:
            response.shadow = self._shadow_internal(**kwargs)

        if data != original:
            self.write()

        return response

    def _run_internal(self, **kwargs):
        data = self.data
        response = Response()

        if data['unresolved']:
            unresolved = copy.deepcopy(data)['unresolved']
            response.append_task(
                Task(target='_resolve_all', args=(unresolved, )))

        return response

    def _render_internal(self, **kwargs):
        html = 'html/fairylab/statsplus/index.html'
        _home = self._home(**kwargs)
        return [(html, '', 'statsplus.html', _home)]

    def _setup_internal(self, **kwargs):
        self._render(**kwargs)
        return Response()

    def _shadow_internal(self, **kwargs):
        return [
            Shadow(
                destination='recap',
                key='statsplus.offseason',
                data=self.data['offseason']),
            Shadow(
                destination='recap',
                key='statsplus.postseason',
                data=self.data['postseason'])
        ]

    def _clear(self):
        self.data['highlights'] = {}
        self.data['injuries'] = {}
        self.data['scores'] = {}
        self.data['table'] = {}
        self.data['unresolved'] = []

    def _handle_key(self, key, encoded_date, text, pattern, append):
        if not append or encoded_date not in self.data[key]:
            self.data[key][encoded_date] = []

        match = re.findall(pattern, text)
        for m in match:
            e = re.sub(_shorten, '{0}{1}', self._encode(key, m))
            self.data[key][encoded_date].append(e)
            if key == 'scores' and encoded_date not in self.data['unresolved']:
                if any(c in e for c in _chlany):
                    self.data['unresolved'].append(encoded_date)

    def _handle_table(self, encoded_date, text):
        if encoded_date not in self.data['table']:
            self.data['table'][encoded_date] = {}

        prechlany = [encoding_to_precoding(c) for c in _chlany]
        pattern = '(?:{})[^\d]+\d+\n'.format('|'.join(prechlany))
        match = re.findall(pattern, text)
        for m in match:
            s = decoding_to_encoding_sub(m)
            e = re.sub('\s{2,}', ' ', s).strip('\n').rsplit(' ', 1)
            if len(e) == 2:
                team, wins = e
                self.data['table'][encoded_date][team] = int(wins)

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
            'highlights': [],
            'forecast': {}
        }

        if data['postseason']:
            ret['live'] = self._live_postseason()
        else:
            ret['live'] = self._live_regular()

        for date in sorted(data['highlights'].keys()):
            ret['highlights'].append(self._table('highlights', date, _player))

        for date in sorted(data['injuries'].keys()):
            ret['injuries'].append(self._table('injuries', date, _player))

        for date in sorted(data['scores'].keys()):
            ret['scores'].append(self._table('scores', date, _game_box))

        if not (data['finished'] or data['offseason'] or data['postseason']):
            ret['forecast'] = standings_table(self._forecast())

        return ret

    @staticmethod
    def _combine(r1, r2):
        (w1, l1) = r1.split('-')
        (w2, l2) = r2.split('-')
        return '{0}-{1}'.format(int(w1) + int(w2), int(l1) + int(l2))

    @staticmethod
    def _encode(key, text):
        if key == 'scores':
            return precoding_to_encoding_sub(text)

        match = re.findall('\([^)]+\)', text)
        for m in match:
            text = re.sub(re.escape(m), precoding_to_encoding_sub(m), text)
        return text

    @staticmethod
    def _unresolve(encoding):
        chlany_ = encoding_to_chlany(encoding)
        return chlany_ if chlany_ else encoding

    @staticmethod
    def _wl(scores, encoding):
        w = len(re.findall(r'\|' + re.escape(encoding), scores))
        l = len(re.findall(r', ' + re.escape(encoding), scores))
        return w, l

    def _forecast(self):
        forecast = {}
        standings = self.shadow.get('recap.standings', {})
        for teamid in teamids():
            srecord = standings.get(teamid, '0-0')
            lrecord = self._record(teamid)
            forecast[teamid] = self._combine(srecord, lrecord)
        return forecast

    def _live_postseason(self):
        lpb = self._live_postseason_body()

        lh = table(clazz=_lhclazz, hcols=_lhcols, head=['Postseason'])
        lb = table(clazz=_lbclazz, bcols=_lbpcols, body=lpb)
        return [lh, lb]

    def _live_postseason_body(self):
        body = []
        for m in self._live_postseason_series():
            group = sort([self._team_tuple(encoding_to_teamid(e)) for e in m])
            (t1, r1), (t2, r2) = group
            w1, w2 = [r.split('-')[0] for r in (r1, r2)]
            inner = [
                logo_absolute(t1, teamid_to_hometown(t1), 'left'), w1, w2,
                logo_absolute(t2, teamid_to_hometown(t2), 'right')
            ]
            body.append(inner)
        return body

    def _live_postseason_series(self):
        series = []
        for date in self.data['scores']:
            scores = '\n'.join(self.data['scores'][date])
            match = re.findall('\|(\w+) \d+, (\w+) \d+>', scores)
            for m in match:
                m = sorted(m)
                if not any(e in m for e in _chlany) and m not in series:
                    series.append(m)
        return series

    def _live_regular(self):
        div = divisions()
        size = len(div) // 2
        al, nl = div[:size], div[size:]

        lrba = self._live_regular_body(al)
        lrbn = self._live_regular_body(nl)

        lhal = table(clazz=_lhclazz, hcols=_lhcols, head=['American League'])
        lbal = table(clazz=_lbclazz, bcols=_lbrcols, body=lrba)
        lhnl = table(clazz=_lhclazz, hcols=_lhcols, head=['National League'])
        lbnl = table(clazz=_lbclazz, bcols=_lbrcols, body=lrbn)

        return [lhal, lbal, lhnl, lbnl]

    def _live_regular_body(self, league):
        body = []
        for division in league:
            group = [self._team_tuple(teamid) for teamid in division[1]]
            inner = [logo_inline(*team_tuple) for team_tuple in sort(group)]
            body.append(inner)
        return body

    def _lookup(self, date, encoding):
        dates = list(self.data['table'].keys())
        ret = None
        for d in sorted(dates):
            if d == date:
                return ret
            if encoding in self.data['table'][d]:
                ret = self.data['table'][d][encoding]
        return ret

    def _narrow(self, encoding, date, tw, tl):
        crosstown = encoding_to_crosstown(encoding)
        table_ = self.data['table'].get(date, {})

        if encoding in table_ and crosstown in table_:
            ethen = self._lookup(date, encoding)
            cthen = self._lookup(date, crosstown)
            if ethen is not None and cthen is not None:
                total = tw + tl
                enow, cnow = table_[encoding], table_[crosstown]
                ew, cw = enow - ethen, cnow - cthen
                if total != 3:
                    el, cl = total // 2 - ew, total // 2 - cw
                else:
                    el, cl = 0 if ew else 1, 0 if cw else 1
                if ew + cw == tw and el + cl <= tl:
                    return ew, el
        elif encoding in table_:
            return tw, tl

        return 0, 0

    def _record(self, teamid):
        encoding = teamid_to_encoding(teamid)
        chlany_ = encoding_to_chlany(encoding)
        hw, hl, cw, cl = 0, 0, 0, 0
        for date in sorted(self.data['scores']):
            scores = '\n'.join(self.data['scores'][date])
            ew, el = self._wl(scores, encoding)
            if chlany_:
                tw, tl = self._wl(scores, chlany_)
                if tw or tl:
                    cw, cl = self._narrow(encoding, date, tw, tl)
            hw += ew + cw
            hl += el + cl
        return '{0}-{1}'.format(hw, hl)

    def _resolve_all(self, *args, **kwargs):
        if len(args) != 1:
            return Response()

        data = self.data
        original = copy.deepcopy(data)

        unresolved = args[0]
        for encoded_date in unresolved:
            scores = self.data['scores'].get(encoded_date, [])
            for i in range(len(scores)):
                self._resolve(encoded_date, i)
            scores = self.data['scores'].get(encoded_date, [])
            if not any(e in '\n'.join(scores) for e in _chlany):
                self.data['unresolved'].remove(encoded_date)

        if data != original:
            self._render(**kwargs)
            self.write()

        return Response()

    def _clarify(self, key, encoded_date, before_team1, before_team2,
                 after_team1, after_team2, count):
        a = '{} @ {}'
        before = a.format(before_team1, before_team2)
        after = a.format(after_team1, after_team2)
        lines = self.data[key].get(encoded_date, [])
        for i in range(len(lines)):
            if before in lines[i]:
                if count == 1:
                    line = re.sub(before, after, lines[i])
                    self.data[key][encoded_date][i] = line
                else:
                    url_match = re.findall(_url_pattern, lines[i])
                    if url_match:
                        url, content = url_match[0]
                        link = url.format(_html, _player)
                        player_ = player(link)
                        if player_['ok']:
                            name = player_['name']
                            team = player_['team']
                            if name == content:
                                if team == after_team1 or team == after_team2:
                                    line = re.sub(before, after, lines[i])
                                    self.data[key][encoded_date][i] = line

    def _resolve(self, encoded_date, i):
        scores = self.data['scores'][encoded_date]
        count = len([True for e in _chlany if e in scores[i]])
        if count not in [1, 2]:
            return

        finished = self.data['finished']
        score_pattern = '(\w+) (\d+), (\w+) (\d+)'
        url_match = re.findall(_url_pattern, scores[i])
        if url_match:
            url, content = url_match[0]
            score_pattern = '(\w+) (\d+), (\w+) (\d+)'
            score_match = re.findall(score_pattern, content)
            if score_match:
                cteam1, cruns1, cteam2, cruns2 = score_match[0]
                if finished:
                    link = url.format(_root + '/resource/extract/', _game_box)
                else:
                    link = url.format(_html, _game_box)
                box_score_ = box_score(link)
                if box_score_['ok']:
                    ddate = decode_datetime(encoded_date)
                    if ddate != box_score_['date']:
                        return
                    bruns1 = box_score_['away_runs']
                    bteam1 = box_score_['away_team']
                    bruns2 = box_score_['home_runs']
                    bteam2 = box_score_['home_team']
                    swap = False
                    if bruns1 < bruns2:
                        bruns1, bruns2 = bruns2, bruns1
                        bteam1, bteam2 = bteam2, bteam1
                        swap = True
                    if self._unresolve(bteam1) != cteam1:
                        return
                    if self._unresolve(bteam2) != cteam2:
                        return
                    if bruns1 != int(cruns1) or bruns2 != int(cruns2):
                        return
                    s = '{} {}, {} {}'
                    score = s.format(bteam1, bruns1, bteam2, bruns2)
                    scores[i] = '<{0}|{1}>'.format(url, score)
                    if swap:
                        bteam1, bteam2 = bteam2, bteam1
                        cteam1, cteam2 = cteam2, cteam1
                    for key in ['highlights', 'injuries']:
                        self._clarify(key, encoded_date, cteam1, cteam2,
                                      bteam1, bteam2, count)

    def _table(self, key, date, path):
        lines = self.data[key][date]
        body = self._table_body(date, lines, path)
        head = self._table_head(date)
        return table(hcols=[''], bcols=[''], head=head, body=body)

    def _table_body(self, date, lines, path):
        body = []
        for line in lines:
            line = re.sub('<([^|]+)\|([^<]+)>', r'<a href="\1">\2</a>', line)
            body.append([encoding_to_decoding_sub(line).format(_html, path)])
        return body

    def _table_head(self, date):
        ddate = decode_datetime(date)
        fdate = ddate.strftime('%A, %B %-d{S}, %Y')
        return [fdate.replace('{S}', suffix(ddate.day))]

    def _team_tuple(self, teamid):
        return (teamid, self._record(teamid))
