#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import datetime
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/plugins/leaguefile', '', _path))
from apis.plugin.plugin_api import PluginApi  # noqa
from apis.renderable.renderable_api import RenderableApi  # noqa
from utils.ago.ago_util import delta, elapsed  # noqa
from utils.component.component_util import card  # noqa
from utils.component.component_util import table  # noqa
from utils.datetime.datetime_util import decode_datetime  # noqa
from utils.datetime.datetime_util import encode_datetime  # noqa
from utils.jinja2.jinja2_util import env  # noqa
from utils.secrets.secrets_util import server  # noqa
from utils.slack.slack_util import chat_post_message  # noqa
from utils.subprocess.subprocess_util import check_output  # noqa
from values.notify.notify_value import NotifyValue  # noqa
from values.response.response_value import ResponseValue  # noqa

_size_pattern = '(\d+)'
_date_pattern = '(\w+\s\d+\s\d+:\d+)'
_name_pattern = '(orange_and_blue_league_baseball.tar.gz(?:.filepart)?)'
_line_pattern = '\s'.join([_size_pattern, _date_pattern, _name_pattern])


class LeaguefilePlugin(PluginApi, RenderableApi):
    def __init__(self, **kwargs):
        super(LeaguefilePlugin, self).__init__(**kwargs)

    @property
    def enabled(self):
        return True

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _href():
        return '/fairylab/leaguefile/'

    @staticmethod
    def _info():
        return 'Reports the progress of the file upload.'

    @staticmethod
    def _title():
        return 'leaguefile'

    def _notify_internal(self, **kwargs):
        return False

    def _on_message_internal(self, **kwargs):
        return ResponseValue()

    def _run_internal(self, **kwargs):
        data = self.data
        original = copy.deepcopy(data)

        response = ResponseValue()
        for size, date, name, fp in self._check():
            if '.filepart' in name:
                if not data['fp']:
                    chat_post_message(
                        'fairylab',
                        'File upload started.',
                        attachments=self._attachments())
                    data['fp'] = {'start': date}
                    response.notify = [NotifyValue.UPLOAD]
                if data['fp'].get('size', 0) != size:
                    data['fp']['size'] = size
                    data['fp']['end'] = date
                    data['fp']['now'] = encode_datetime(kwargs['date'])
            elif data['fp'] and not fp:
                data['fp']['size'] = size
                data['fp']['date'] = date
                del data['fp']['now']
                if not len(data['up']) or data['up'][0]['date'] != date:
                    data['up'].insert(0, copy.deepcopy(data['fp']))
                    if len(data['up']) > 10:
                        data['up'] = data['up'][:10]
                    chat_post_message('general', 'File is up.')
                    chat_post_message(
                        'fairylab',
                        'File upload completed.',
                        attachments=self._attachments())
                    response.notify = [NotifyValue.FILE]
                data['fp'] = None

        if data != original:
            self.write()

        if data != original or data['fp']:
            self._render(**kwargs)
            if not response.notify:
                response.notify = [NotifyValue.BASE]

        return response

    def _render_internal(self, **kwargs):
        html = 'html/fairylab/leaguefile/index.html'
        _home = self._home(**kwargs)
        return [(html, '', 'leaguefile.html', _home)]

    def _setup_internal(self, **kwargs):
        data = self.data
        original = copy.deepcopy(data)

        for size, date, name, fp in self._check():
            if not fp:
                data['fp'] = None

            if '.filepart' in name:
                if not data['fp']:
                    data['fp'] = {
                        'start': date,
                        'size': size,
                        'end': date,
                        'now': encode_datetime(kwargs['date'])
                    }
            elif not len(data['up']) or data['up'][0]['date'] != date:
                data['up'].insert(0, {
                    'date': date,
                    'start': date,
                    'size': size,
                    'end': date
                })

        if data != original:
            self.write()

        self._render(**kwargs)

    def _shadow_internal(self, **kwargs):
        return {}

    @staticmethod
    def _date(s):
        return s.rsplit(' ', 1)[0]

    @staticmethod
    def _size(s):
        return '{:,}'.format(int(s))

    @staticmethod
    def _time(s, e):
        sdate = datetime.datetime.strptime(s, '%b %d %H:%M')
        edate = datetime.datetime.strptime(e, '%b %d %H:%M')
        return elapsed(sdate, edate)

    @staticmethod
    def _check():
        ls = 'ls -l /var/www/html/StatsLab/league_file'
        out = check_output(['ssh', 'brunnerj@' + server, ls])
        fp = '.filepart' in out
        for line in out.splitlines():
            line = re.sub(r'\s+', ' ', line)
            match = re.findall(_line_pattern, line)
            if match:
                yield match[0] + (fp, )

    def _home(self, **kwargs):
        data = self.data
        ret = {
            'breadcrumbs': [{
                'href': '/fairylab/',
                'name': 'Home'
            }, {
                'href': '',
                'name': 'Leaguefile'
            }]
        }

        ret['fp'] = None
        if data['fp']:
            time = self._time(data['fp']['start'], data['fp']['end'])
            ts = delta(decode_datetime(data['fp']['now']), kwargs['date'])

            success = 'ongoing' if 's' in ts else ''
            danger = 'stalled' if 's' not in ts else ''
            cols = ['', ' class="w-100"']
            ret['fp'] = card(
                title=self._date(data['fp']['start']),
                table=table(
                    clazz='table-sm',
                    hcols=cols,
                    bcols=cols,
                    body=[['Time: ', time],
                          ['Size: ', self._size(data['fp']['size'])]]),
                ts=ts,
                success=success,
                danger=danger)

        body = []
        for up in data['up']:
            body.append([
                self._date(up['date']),
                self._time(up['start'], up['end']),
                self._size(up['size'])
            ])
        ret['up'] = table(
            hcols=['', '', ''],
            bcols=['', '', ''],
            head=['Date', 'Time', 'Size'],
            body=body)

        return ret
