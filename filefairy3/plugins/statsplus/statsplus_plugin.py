#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import datetime
import os
import re
import sys
import threading

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugins/statsplus', '', _path)
sys.path.append(_root)
from apis.plugin.plugin_api import PluginApi  # noqa
from apis.renderable.renderable_api import RenderableApi  # noqa
from utils.box.box_util import clarify  # noqa
from utils.component.component_util import table  # noqa
from utils.datetime.datetime_util import decode_datetime  # noqa
from utils.datetime.datetime_util import encode_datetime  # noqa
from utils.datetime.datetime_util import suffix  # noqa
from utils.standings.standings_util import sort  # noqa
from utils.team.team_util import chlany  # noqa
from utils.team.team_util import decoding_to_encoding_sub  # noqa
from utils.team.team_util import divisions  # noqa
from utils.team.team_util import encoding_to_decoding_sub  # noqa
from utils.team.team_util import encoding_to_precoding  # noqa
from utils.team.team_util import encoding_to_teamid  # noqa
from utils.team.team_util import encodings  # noqa
from utils.team.team_util import logo_absolute  # noqa
from utils.team.team_util import logo_inline  # noqa
from utils.team.team_util import precoding_to_encoding_sub  # noqa
from utils.team.team_util import precodings  # noqa
from utils.team.team_util import teamid_to_encoding  # noqa
from utils.team.team_util import teamid_to_hometown  # noqa
from values.notify.notify_value import NotifyValue  # noqa
from values.response.response_value import ResponseValue  # noqa

_html = 'https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/'
_game_box = 'box_scores/game_box_'
_player = 'players/player_'
_shorten = '{}(?:{}|{})'.format(_html, _game_box, _player)
_encodings = '|'.join(encodings())
_precodings = '|'.join(precodings())
_chlany = chlany()
_lhclazz = 'table-fixed border border-bottom-0 mt-3'
_lhcols = [' class="text-center"']
_lbclazz = 'table-fixed border'
_lbpcols = [
    ' class="position-relative w-40"', ' class="text-center w-10"',
    ' class="text-center w-10"', ' class="position-relative text-right w-40"'
]
_lbrcols = [' class="td-sm position-relative text-center w-20"'] * 5


class StatsplusPlugin(PluginApi, RenderableApi):
    def __init__(self, **kwargs):
        super(StatsplusPlugin, self).__init__(**kwargs)

    @property
    def enabled(self):
        return True

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _href():
        return '/fairylab/statsplus/'

    @staticmethod
    def _info():
        return 'Collects sim results in real time.'

    @staticmethod
    def _title():
        return 'statsplus'

    def _notify_internal(self, **kwargs):
        notify = kwargs['notify']
        if notify == NotifyValue.DOWNLOAD_FINISH:
            self.data['finished'] = True
            self.write()
        if notify == NotifyValue.DOWNLOAD_YEAR:
            self.data['offseason'] = True
            self.write()
        return False

    def _on_message_internal(self, **kwargs):
        obj = kwargs['obj']
        bot_id = obj.get('bot_id')
        channel = obj.get('channel')
        if bot_id != 'B7KJ3362Y' or channel != 'C7JSGHW8G':
            return ResponseValue()

        data = self.data
        original = copy.deepcopy(data)

        text = obj.get('text', '')
        date = re.findall('\d{2}\/\d{2}\/\d{4}', text)
        if not date:
            return ResponseValue()

        ddate = datetime.datetime.strptime(date[0], '%m/%d/%Y')
        edate = encode_datetime(ddate)
        ndate = decode_datetime(self.shadow.get('download.now', edate))
        if ndate < ddate:
            return ResponseValue()

        if self.data['finished']:
            self.data['finished'] = False
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

        pattern = 'MAJOR LEAGUE BASEBALL Live Table'
        if re.findall(pattern, text):
            self._handle_table(edate, text)
            if data['offseason']:
                data['offseason'] = False

        if data != original:
            self.write()

        return ResponseValue(notify=[NotifyValue.BASE])

    def _run_internal(self, **kwargs):
        data = self.data
        response = ResponseValue()

        if data['updated']:
            data['updated'] = False
            self._render(**kwargs)
            self.write()
            response.notify = [NotifyValue.BASE]

        if data['unresolved']:
            original = copy.deepcopy(data)
            t = threading.Thread(
                target=self._resolve_all, args=(original['unresolved'], ))
            t.daemon = True
            t.start()

        return response

    def _render_internal(self, **kwargs):
        html = 'html/fairylab/statsplus/index.html'
        _home = self._home(**kwargs)
        return [(html, '', 'statsplus.html', _home)]

    def _setup_internal(self, **kwargs):
        self._render(**kwargs)

    def _shadow_internal(self, **kwargs):
        return {}

    def _clear(self):
        self.data['highlights'] = {}
        self.data['injuries'] = {}
        self.data['scores'] = {}
        self.data['table'] = {}

    def _handle_key(self, key, encoded_date, text, pattern, append):
        if not append or encoded_date not in self.data[key]:
            self.data[key][encoded_date] = []

        match = re.findall(pattern, text)
        for m in match:
            e = re.sub(_shorten, '{0}{1}', precoding_to_encoding_sub(m))
            self.data[key][encoded_date].append(e)
            if key == 'scores' and encoded_date not in self.data['unresolved']:
                if any(c in e for c in _chlany):
                    self.data['unresolved'].append(encoded_date)

    def _handle_table(self, encoded_date, text):
        if encoded_date not in self.data['table']:
            self.data['table'][encoded_date] = []

        prechlany = [encoding_to_precoding(c) for c in _chlany]
        pattern = '(?:{})[^\d]+\d+\n'.format('|'.join(prechlany))
        match = re.findall(pattern, text)
        for m in match:
            s = decoding_to_encoding_sub(m)
            e = re.sub('\s{2,}', ' ', s).strip('\n')
            self.data['table'][encoded_date].append(e)

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

        if data['postseason']:
            ret['live'] = self._live_postseason()
        else:
            ret['live'] = self._live_regular()

        for date in sorted(data['highlights'].keys(), reverse=True):
            ret['highlights'].append(self._table('highlights', date, _player))

        for date in sorted(data['injuries'].keys(), reverse=True):
            ret['injuries'].append(self._table('injuries', date, _player))

        for date in sorted(data['scores'].keys(), reverse=True):
            ret['scores'].append(self._table('scores', date, _game_box))

        return ret

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
        size = len(div) / 2
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

    def _record(self, teamid):
        encoding = teamid_to_encoding(teamid)
        hw, hl = 0, 0
        for date in self.data['scores']:
            scores = '\n'.join(self.data['scores'][date])
            hw += len(re.findall(r'\|' + re.escape(encoding), scores))
            hl += len(re.findall(r', ' + re.escape(encoding), scores))
        return '{0}-{1}'.format(hw, hl)

    def _resolve_all(self, unresolved):
        for encoded_date in unresolved:
            scores = self.data['scores'].get(encoded_date, [])
            original = copy.deepcopy(scores)
            for i in range(len(scores)):
                if any(e in scores[i] for e in _chlany):
                    self._resolve(encoded_date, i)
            scores = self.data['scores'].get(encoded_date, [])
            if not any(e in '\n'.join(scores) for e in _chlany):
                self.data['unresolved'].remove(encoded_date)
            if scores != original:
                self.data['updated'] = True

    def _resolve(self, encoded_date, i):
        score = self.data['scores'][encoded_date][i]
        pattern = '<([^|]+)\|([^<]+)>'
        match = re.findall(pattern, score)
        if match:
            link, encoding = match[0]
            value = clarify(encoded_date, link.format(_html, _game_box),
                            encoding)
            if encoding != value['encoding']:
                encoding = value['encoding']
                self.data['scores'][encoded_date][i] = '<{0}|{1}>'.format(
                    link, encoding)

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
