#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import datetime
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/plugin/leaguefile', '', _path))
from api.plugin.plugin import Plugin  # noqa
from api.renderable.renderable import Renderable  # noqa
from util.ago.ago import delta, elapsed  # noqa
from util.component.component import card  # noqa
from util.component.component import table  # noqa
from util.datetime.datetime_ import decode_datetime  # noqa
from util.datetime.datetime_ import encode_datetime  # noqa
from util.jinja2.jinja2_ import env  # noqa
from util.secrets.secrets import server  # noqa
from util.slack.slack import chat_post_message  # noqa
from util.subprocess.subprocess_ import check_output  # noqa
from value.notify.notify import Notify  # noqa
from value.response.response import Response  # noqa

_size_pattern = '(\d+)'
_date_pattern = '(\w+\s\d+\s\d+:\d+)'
_name_pattern = '(orange_and_blue_league_baseball.tar.gz(?:.filepart)?)'
_line_pattern = '\s'.join([_size_pattern, _date_pattern, _name_pattern])
_server = server()


class Leaguefile(Plugin, Renderable):
    def __init__(self, **kwargs):
        super(Leaguefile, self).__init__(**kwargs)

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
        return Response()

    def _run_internal(self, **kwargs):
        data = self.data
        original = copy.deepcopy(data)

        response = Response()
        for size, date, name, fp in self._check():
            if '.filepart' in name:
                if not data['fp']:
                    chat_post_message(
                        'fairylab',
                        'File upload started.',
                        attachments=self._attachments())
                    data['fp'] = {'start': date}
                    response.notify = [Notify.LEAGUEFILE_START]
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
                    response.notify = [Notify.LEAGUEFILE_FINISH]
                data['fp'] = None

        if data != original:
            self.write()

        if data != original or data['fp']:
            self._render(**kwargs)
            if not response.notify:
                response.notify = [Notify.BASE]

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
        output = check_output(['ssh', 'brunnerj@' + _server, ls], timeout=8)
        if output.get('ok'):
            value = output.get('output', '')
            fp = '.filepart' in value
            for line in value.splitlines():
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