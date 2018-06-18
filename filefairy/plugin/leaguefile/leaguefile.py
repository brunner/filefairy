#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import datetime
import logging
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugin/leaguefile', '', _path)
sys.path.append(_root)
from api.messageable.messageable import Messageable  # noqa
from api.registrable.registrable import Registrable  # noqa
from api.renderable.renderable import Renderable  # noqa
from api.runnable.runnable import Runnable  # noqa
from core.notify.notify import Notify  # noqa
from core.shadow.shadow import Shadow  # noqa
from core.task.task import Task  # noqa
from core.response.response import Response  # noqa
from util.ago.ago import delta  # noqa
from util.ago.ago import elapsed  # noqa
from util.component.component import card  # noqa
from util.component.component import table  # noqa
from util.datetime_.datetime_ import decode_datetime  # noqa
from util.datetime_.datetime_ import encode_datetime  # noqa
from util.file_.file_ import ping  # noqa
from util.file_.file_ import recreate  # noqa
from util.file_.file_ import wget_file  # noqa
from util.jinja2_.jinja2_ import env  # noqa
from util.news.news import box_scores  # noqa
from util.news.news import leagues  # noqa
from util.secrets.secrets import server  # noqa
from util.slack.slack import reactions_add  # noqa
from util.subprocess_.subprocess_ import check_output  # noqa

logger_ = logging.getLogger('fairylab')

_size_pattern = '(\d+)'
_date_pattern = '(\w+\s\d+\s\d+:\d+)'
_name_pattern = '(orange_and_blue_league_baseball.tar.gz(?:.filepart)?)'
_line_pattern = '\s'.join([_size_pattern, _date_pattern, _name_pattern])
_server = server()


class Leaguefile(Messageable, Registrable, Renderable, Runnable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _href():
        return '/fairylab/leaguefile/'

    @staticmethod
    def _info():
        return 'Reports current file upload progress.'

    @staticmethod
    def _title():
        return 'leaguefile'

    def _notify_internal(self, **kwargs):
        return Response()

    def _on_message_internal(self, **kwargs):
        return Response()

    def _run_internal(self, **kwargs):
        data = self.data
        original = copy.deepcopy(data)

        notify = Notify.BASE
        response = Response()

        if data['download'] and data['upload']:
            download, upload = data['download'], data['upload']
            size, date, name, fp = self._check_download()
            if fp:
                if download.get('size', 0) != size:
                    end = self._encode(kwargs['date'])
                    now = encode_datetime(kwargs['date'])
                    download.update({'size': size, 'end': end, 'now': now})
            elif upload['size'] == size:
                data['completed'].insert(0, self._completed(download, upload))
                if len(data['completed']) > 10:
                    data['completed'] = data['completed'][:10]
                data['download'], data['upload'] = None, None
        else:
            for size, date, name, fp in self._check_upload():
                if '.filepart' in name:
                    if not data['upload']:
                        data['upload'] = {'start': date}
                        self._chat('fairylab', 'Upload started.')
                        logger_.log(logging.INFO, 'Upload started.')
                        notify = Notify.LEAGUEFILE_START
                    if data['upload'].get('size') != size:
                        now = encode_datetime(kwargs['date'])
                        u = {'size': size, 'end': date, 'now': now}
                        data['upload'].update(u)
                elif data['upload'] and not fp:
                    upload = data['upload']
                    if upload.get('size', 0) != size:
                        now = encode_datetime(kwargs['date'])
                        upload.update({'size': size, 'date': date, 'now': now})
                        self._file_is_up(date)
                        notify = Notify.LEAGUEFILE_FINISH
                    response = self.download(**kwargs)

        if data != original:
            self.write()

        if data != original or data['upload']:
            response.append_notify(notify)
            self._render(**kwargs)

        return response

    def _render_internal(self, **kwargs):
        html = 'html/fairylab/leaguefile/index.html'
        _home = self._home(**kwargs)
        return [(html, '', 'leaguefile.html', _home)]

    def _setup_internal(self, **kwargs):
        data = self.data
        original = copy.deepcopy(data)

        response = Response()
        if data['download']:
            response = self._download_start(**kwargs)
        else:
            for size, date, name, fp in self._check_upload():
                if not fp:
                    data['upload'] = None
                elif '.filepart' in name:
                    if not data['upload']:
                        data['upload'] = {'start': date}
                    if data['upload'].get('size', 0) != size:
                        now = encode_datetime(kwargs['date'])
                        u = {'size': size, 'end': date, 'now': now}
                        data['upload'].update(u)

        if data != original:
            self.write()

        self._render(**kwargs)
        return response

    def _shadow_internal(self, **kwargs):
        return [
            Shadow(
                destination='statsplus',
                key='leaguefile.now',
                data=self.data['now'])
        ]

    @staticmethod
    def _card(start, time, size, ts, success, danger):
        cols = [' class="w-55p"', '']
        return card(
            title=Leaguefile._filedate(start),
            table=table(
                clazz='table-sm',
                hcols=cols,
                bcols=cols,
                body=[['Time: ', time], ['Size: ',
                                         Leaguefile._size(size)]]),
            ts=ts,
            success=success,
            danger=danger)

    @staticmethod
    def _check_download():
        download = os.path.join(_root, 'resource/download')
        output = check_output(['ls', '-l', download], timeout=8)
        if output.get('ok'):
            value = output.get('output', '')
            fp = 'news' not in value
            for line in value.splitlines():
                line = re.sub(r'\s+', ' ', line)
                match = re.findall(_line_pattern, line)
                if match:
                    return match[0] + (fp, )
        return ('0', '', '', False)

    @staticmethod
    def _check_upload():
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

    @staticmethod
    def _completed(download, upload):
        return {
            'size': upload['size'],
            'date': upload['date'],
            'ustart': upload['start'],
            'uend': upload['end'],
            'dstart': download['start'],
            'dend': download['end']
        }

    @staticmethod
    def _decode(date):
        return datetime.datetime.strptime(date, '%b %d %H:%M')

    @staticmethod
    def _encode(date):
        return date.strftime('%b %d %H:%M')

    @staticmethod
    def _seconds(then, now):
        diff = Leaguefile._decode(now) - Leaguefile._decode(then)
        return diff.total_seconds()

    @staticmethod
    def _filedate(s):
        return s.rsplit(' ', 1)[0]

    @staticmethod
    def _size(s):
        return '{:,}'.format(int(s))

    @staticmethod
    def _time(s, e):
        return elapsed(Leaguefile._decode(s), Leaguefile._decode(e))

    def download(self, **kwargs):
        data = self.data

        output = ping()
        if output.get('ok') and data['upload']:
            return self._download_start(**kwargs)
        else:
            logger_.log(
                logging.WARNING,
                'Download failed.',
                extra={
                    'output': output.get('output', '')
                })
            return Response()

    def _download_internal(self, *args, **kwargs):
        response = Response()
        output = wget_file()

        if output.get('ok'):
            now = decode_datetime(self.data['now'])
            then = now

            box_scores_now = box_scores(then)
            leagues_now = leagues(then)
            if box_scores_now > now:
                now = box_scores_now
            if leagues_now > then:
                now = leagues_now

            self.data['now'] = encode_datetime(now)
            self.data['then'] = encode_datetime(then)

            logger_.log(logging.INFO, 'Download finished.')
            response.append_notify(Notify.LEAGUEFILE_DOWNLOAD)
            if then.year != now.year:
                response.append_notify(Notify.LEAGUEFILE_YEAR)
            response.shadow = self._shadow_internal(**kwargs)
        else:
            logger_.log(logging.INFO, 'Download failed.')
            self.data['download'] = None

        self.write()
        return response

    def _download_start(self, **kwargs):
        now = encode_datetime(kwargs['date'])
        self.data['download'] = {
            'start': self._encode(kwargs['date']),
            'now': now
        }
        logger_.log(logging.INFO, 'Download started.')
        return Response(
            task=[Task(target='_download_internal', kwargs=kwargs)])

    def _file_is_up(self, date):
        obj = self._chat('fairylab', 'File is up.')
        logger_.log(logging.INFO, 'File is up.')
        channel = obj.get('channel')
        ts = obj.get('ts')
        if channel and ts:
            seconds = self._seconds(date, self.data['upload']['end'])
            if seconds < 10800:
                reactions_add('zap', channel, ts)
            elif seconds > 25200:
                reactions_add('timer_clock', channel, ts)

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

        ret['upload'] = None
        if data['upload']:
            upload = data['upload']
            time = self._time(upload['start'], upload['end'])
            ts = delta(decode_datetime(upload['now']), kwargs['date'])
            if data['download']:
                success, danger = 'completed', ''
            else:
                success = 'ongoing' if 's' in ts else ''
                danger = 'stalled' if 's' not in ts else ''
            ret['upload'] = self._card(upload['start'], time, upload['size'],
                                       ts, success, danger)

        ret['download'] = None
        if data['download'] and data['download'].get('end'):
            download = data['download']
            time = self._time(download['start'], download['end'])
            ts = delta(decode_datetime(download['now']), kwargs['date'])
            success = 'ongoing' if 's' in ts else ''
            danger = 'stalled' if 's' not in ts else ''
            ret['download'] = self._card(upload['start'], time,
                                         download['size'], ts, success, danger)

        body = []
        for c in data['completed']:
            utime, dtime = '-', '-'
            if c['ustart'] and c['uend']:
                utime = self._time(c['ustart'], c['uend'])
            if c['dstart'] and c['dend']:
                dtime = self._time(c['dstart'], c['dend'])
            body.append([
                self._filedate(c['date']), utime, dtime,
                self._size(c['size'])
            ])
        cols = [
            '', ' class="text-center"', ' class="text-center"',
            ' class="text-right"'
        ]
        ret['completed'] = table(
            hcols=cols,
            bcols=cols,
            head=['Date', 'Upload', 'Download', 'Size'],
            body=body)

        return ret
