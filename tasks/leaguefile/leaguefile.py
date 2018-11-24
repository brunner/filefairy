#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import datetime
import logging
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/tasks/leaguefile', '', _path))

from api.registrable.registrable import Registrable  # noqa
from api.reloadable.reloadable import Reloadable  # noqa
from common.datetime_.datetime_ import datetime_as_pst  # noqa
from common.datetime_.datetime_ import datetime_datetime_est  # noqa
from common.datetime_.datetime_ import decode_datetime  # noqa
from common.datetime_.datetime_ import encode_datetime  # noqa
from common.datetime_.datetime_ import timedelta  # noqa
from common.datetime_.datetime_ import timestamp  # noqa
from common.elements.elements import card  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import table  # noqa
from common.jinja2_.jinja2_ import env  # noqa
from common.secrets.secrets import server  # noqa
from common.slack.slack import reactions_add  # noqa
from common.subprocess_.subprocess_ import check_output  # noqa
from data.notify.notify import Notify  # noqa
from data.shadow.shadow import Shadow  # noqa
from data.thread_.thread_ import Thread  # noqa
from data.response.response import Response  # noqa

_logger = logging.getLogger('fairylab')

FILE_HOST = 'www.orangeandblueleaguebaseball.com'
FILE_NAME = 'orange_and_blue_league_baseball.tar.gz'
FILE_URL = 'https://{}/StatsLab/league_file/{}'.format(FILE_HOST, FILE_NAME)

_size_pattern = '(\d+)'
_date_pattern = '(\w+\s\d+\s\d+:\d+)'
_name_pattern = '(orange_and_blue_league_baseball.tar.gz(?:.filepart)?)'
_line_pattern = '\s'.join([_size_pattern, _date_pattern, _name_pattern])
_server = server()
_td = datetime.timedelta(minutes=2)


class Leaguefile(Registrable, Reloadable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _href():
        return '/leaguefile/'

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

    def _reload_internal(self, **kwargs):
        return {'leaguefile': ['download_file', 'extract_file']}

    def _run_internal(self, **kwargs):
        data = self.data
        original = copy.deepcopy(data)

        notify = Notify.BASE
        response = Response()

        render = False
        now = encode_datetime(kwargs['date'])

        if data['download'] and data['upload']:
            download, upload = data['download'], data['upload']
            size, date, name, fp = self._check_download()
            if fp:
                if download.get('size', 0) != size:
                    end = self._encode(kwargs['date'])
                    download.update({'size': size, 'end': end, 'now': now})
            elif upload['size'] == size:
                render = True
                data['completed'].insert(0, self._completed(download, upload))
                if len(data['completed']) > 10:
                    data['completed'] = data['completed'][:10]
                data['download'], data['upload'] = None, None
        else:
            for size, date, name, fp in self._check_upload():
                ddate = self._decode(date, kwargs['date'])
                if '.filepart' in name:
                    if not data['upload']:
                        render = True
                        data['upload'] = {'start': date}
                        self._chat('fairylab', 'Upload started.')
                        _logger.log(logging.INFO, 'Upload started.')
                        notify = Notify.LEAGUEFILE_START
                    if data['upload'].get('size') != size:
                        u = {'size': size, 'end': date, 'now': now}
                        data['upload'].update(u)
                        if data['stalled']:
                            render = True
                            data['stalled'] = False
                    elif ddate < kwargs['date'] - _td:
                        if not data['stalled']:
                            render = True
                            data['stalled'] = True
                elif data['upload'] and not fp:
                    render = True
                    upload = data['upload']
                    if upload.get('size', 0) != size:
                        upload.update({'size': size, 'date': date, 'now': now})
                        self._file_is_up(**kwargs)
                        notify = Notify.LEAGUEFILE_FINISH
                    response = self.download(**kwargs)

        if data != original:
            self.write()

        wait = decode_datetime(data['date']) < kwargs['date'] - _td
        if render or data['upload'] and wait:
            data['date'] = now
            response.append(notify=notify)
            self._render(**kwargs)

        return response

    def _render_internal(self, **kwargs):
        html = 'leaguefile/index.html'
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
                info=self.data['now'])
        ]

    @staticmethod
    def _card(start, time, size, ts, success, danger):
        cols = [col(clazz='w-55p'), col()]
        return card(
            title=Leaguefile._filedate(start),
            table=table(
                clazz='table-sm',
                hcols=cols,
                bcols=cols,
                body=[[cell(content='Time: '),
                       cell(content=time)], [
                           cell(content='Size: '),
                           cell(content=Leaguefile._size(size))
                       ]]),
            ts=ts,
            success=success,
            danger=danger)

    @staticmethod
    def _check_download():
        download = re.sub(r'/tasks/leaguefile', '/resource/download', _path)
        output = check_output(['ls', '-l', download], timeout=8)
        if output.get('ok'):
            stdout = output.get('stdout', '')
            fp = 'news' not in stdout
            for line in stdout.splitlines():
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
            stdout = output.get('stdout', '')
            fp = '.filepart' in stdout
            for line in stdout.splitlines():
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
    def _decode(date, n):
        d = datetime.datetime.strptime(date, '%b %d %H:%M')
        est = datetime_datetime_est(n.year, d.month, d.day, d.hour, d.minute)
        return datetime_as_pst(est)

    @staticmethod
    def _encode(date):
        return date.strftime('%b %d %H:%M')

    @staticmethod
    def _seconds(then, now, n):
        diff = Leaguefile._decode(now, n) - Leaguefile._decode(then, n)
        return diff.total_seconds()

    @staticmethod
    def _filedate(s):
        return s.rsplit(' ', 1)[0]

    @staticmethod
    def _size(s):
        return '{:,}'.format(int(s))

    @staticmethod
    def _time(s, e, n):
        return timedelta(Leaguefile._decode(s, n), Leaguefile._decode(e, n))

    def download(self, **kwargs):
        data = self.data

        output = check_output(['ping', '-c 1', FILE_HOST], timeout=8)
        if output.get('ok') and data['upload']:
            return self._download_start(**kwargs)
        else:
            _logger.log(
                logging.WARNING,
                'Download failed.',
                extra={
                    'stdout': output.get('stdout', ''),
                    'stderr': output.get('stderr', '')
                })
            return Response()

    def _download_internal(self, *args, **kwargs):
        response = Response()
        output = self._call('download_file', (FILE_URL, ))

        if output.get('ok'):
            then = decode_datetime(self.data['now'])
            now = self._call('extract_file', (then, ))

            self.data['now'] = encode_datetime(now)
            self.data['then'] = encode_datetime(then)

            _logger.log(logging.INFO, 'Download finished.')
            response.append(notify=Notify.LEAGUEFILE_DOWNLOAD)
            if then.year != now.year:
                response.append(notify=Notify.LEAGUEFILE_YEAR)
            response.shadow = self._shadow_internal(**kwargs)
        else:
            _logger.log(logging.INFO, 'Download failed.')
            self.data['download'] = None

        self.write()
        return response

    def _download_start(self, **kwargs):
        now = encode_datetime(kwargs['date'])
        self.data['download'] = {
            'start': self._encode(kwargs['date']),
            'now': now
        }
        _logger.log(logging.INFO, 'Download started.')
        return Response(
            thread_=[Thread(target='_download_internal', kwargs=kwargs)])

    def _file_is_up(self, **kwargs):
        obj = self._chat('fairylab', 'File is up.')
        _logger.log(logging.INFO, 'File is up.')
        channel = obj.get('channel')
        upload = self.data['upload']
        ts = obj.get('ts')
        if channel and ts:
            max_, min_ = 0, 0
            for c in self.data['completed']:
                seconds = self._seconds(c['ustart'], c['uend'], kwargs['date'])
                if not max_ or max_ < seconds:
                    max_ = seconds
                if not min_ or min_ > seconds:
                    min_ = seconds
            seconds = self._seconds(upload['start'], upload['end'],
                                    kwargs['date'])
            if seconds < min_:
                reactions_add('zap', channel, ts)
            elif seconds > max_:
                reactions_add('timer_clock', channel, ts)

    def _home(self, **kwargs):
        data = self.data
        ret = {
            'breadcrumbs': [{
                'href': '/',
                'name': 'Fairylab'
            }, {
                'href': '',
                'name': 'Leaguefile'
            }]
        }

        ret['upload'] = None
        if data['upload']:
            upload = data['upload']
            time = self._time(upload['start'], upload['end'], kwargs['date'])
            ts = timestamp(decode_datetime(upload['now']))
            if data['download']:
                success, danger = 'completed', ''
            else:
                success = 'ongoing' if not data['stalled'] else ''
                danger = 'stalled' if data['stalled'] else ''
            ret['upload'] = self._card(upload['start'], time, upload['size'],
                                       ts, success, danger)

        ret['download'] = None
        if data['download'] and data['download'].get('end'):
            download = data['download']
            time = self._time(download['start'], download['end'],
                              kwargs['date'])
            ts = timestamp(decode_datetime(download['now']))
            ret['download'] = self._card(upload['start'], time,
                                         download['size'], ts, 'ongoing', '')

        body = []
        for c in data['completed']:
            utime, dtime = '-', '-'
            if c['ustart'] and c['uend']:
                utime = self._time(c['ustart'], c['uend'], kwargs['date'])
            if c['dstart'] and c['dend']:
                dtime = self._time(c['dstart'], c['dend'], kwargs['date'])
            body.append([
                cell(content=self._filedate(c['date'])),
                cell(content=utime),
                cell(content=dtime),
                cell(content=self._size(c['size']))
            ])
        cols = [
            col(),
            col(clazz='text-center'),
            col(clazz='text-center'),
            col(clazz='text-right')
        ]
        ret['completed'] = table(
            hcols=cols,
            bcols=cols,
            head=[
                cell(content='Date'),
                cell(content='Upload'),
                cell(content='Download'),
                cell(content='Size')
            ],
            body=body)

        return ret
