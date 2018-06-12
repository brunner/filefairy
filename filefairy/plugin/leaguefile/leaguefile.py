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

        response = Response()
        for size, date, name, fp in self._check_upload():
            if '.filepart' in name:
                if not data['upload']:
                    data['upload'] = {'start': date}
                    self._chat('fairylab', 'Upload started.')
                    logger_.log(logging.INFO, 'Upload started.')
                    response.notify = [Notify.LEAGUEFILE_START]
                if data['upload'].get('size', 0) != size:
                    now = encode_datetime(kwargs['date'])
                    u = {'size': size, 'end': date, 'now': now}
                    data['upload'].update(u)
            elif data['upload'] and not data['download'] and not fp:
                if data['upload'].get('size', 0) != size:
                    now = encode_datetime(kwargs['date'])
                    data['upload'].update({
                        'size': size,
                        'date': date,
                        'now': now
                    })
                    self._file_is_up(date)
                    response.notify = [Notify.LEAGUEFILE_FINISH]
                if not data['download']:
                    response.task = self.download(**kwargs).task

        if data['upload'] and data['download']:
            upload = data['upload']
            download = data['download']
            size, date, name, fp = self._check_download()
            if fp:
                if download.get('size', 0) != size:
                    now = encode_datetime(kwargs['date'])
                    download.update({'size': size, 'end': date, 'now': now})
            elif upload['size'] == size:
                completed = {
                    'size': upload['size'],
                    'date': upload['date'],
                    'ustart': upload['start'],
                    'uend': upload['end'],
                    'dstart': download['start'],
                    'dend': download['end']
                }
                data['completed'].insert(0, copy.deepcopy(completed))
                if len(data['completed']) > 10:
                    data['completed'] = data['completed'][:10]
                data['upload'] = None
                data['download'] = None

        if data != original:
            self.write()

        if data != original or data['upload']:
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

        for size, date, name, fp in self._check_upload():
            if not fp:
                data['upload'] = None

            if '.filepart' in name:
                if not data['upload']:
                    now = encode_datetime(kwargs['date'])
                    u = {'start': date, 'size': size, 'end': date, 'now': now}
                    data['upload'] = u
            elif not len(
                    data['completed']) or data['completed'][0]['date'] != date:
                c = {'date': date, 'start': date, 'size': size, 'end': date}
                data['completed'].insert(0, c)

        data['download'] = None

        if data != original:
            self.write()

        self._render(**kwargs)
        return Response()

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
    def _decode(date):
        return datetime.datetime.strptime(date, '%b %d %H:%M')

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
            now = encode_datetime(kwargs['date'])
            self.data['download'] = {
                'start': data['upload']['end'],
                'now': now
            }
            logger_.log(logging.INFO, 'Download started.')
            return Response(
                task=[Task(target='_download_internal', kwargs=kwargs)])
        else:
            logger_.log(
                logging.WARNING,
                'Download failed.',
                extra={
                    'output': output.get('output', '')
                })
            return Response()

    def _download_internal(self, *args, **kwargs):
        data = self.data
        data['then'] = data['now']

        wget_file()
        self._games()
        self._leagues()

        logger_.log(logging.INFO, 'Download finished.')
        response = Response(notify=[Notify.LEAGUEFILE_DOWNLOAD])

        dthen = decode_datetime(data['then'])
        dnow = decode_datetime(data['now'])
        if dthen.year != dnow.year:
            response.append_notify(Notify.LEAGUEFILE_YEAR)

        response.shadow = self._shadow_internal(**kwargs)
        self.write()

        return response

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

    def _games(self):
        box_scores = os.path.join(_root, 'resource/extract/box_scores')
        game_logs = os.path.join(_root, 'resource/extract/game_logs')
        recreate(box_scores)
        recreate(game_logs)

        boxes = 'resource/download/news/html/box_scores'
        leagues = 'resource/download/news/txt/leagues'
        for box in os.listdir(os.path.join(_root, boxes)):
            bdname = os.path.join(box_scores, box)
            bfname = os.path.join(_root, boxes, box)
            log_ = box.replace('game_box', 'log').replace('html', 'txt')
            ldname = os.path.join(game_logs, log_)
            lfname = os.path.join(_root, leagues, log_)
            if not os.path.isfile(bfname) or not os.path.isfile(lfname):
                continue
            self._games_internal(bdname, bfname, ldname, lfname)

    def _games_internal(self, bdname, bfname, ldname, lfname):
        then = decode_datetime(self.data['then'])
        now = decode_datetime(self.data['now'])

        with open(bfname, 'r', encoding='iso-8859-1') as bff:
            bcontent = bff.read()
        with open(lfname, 'r', encoding='iso-8859-1') as lff:
            lcontent = lff.read()

        pattern = 'MLB Box Scores[^\d]+(\d{2}\/\d{2}\/\d{4})'
        match = re.findall(pattern, bcontent)
        if match:
            date = datetime.datetime.strptime(match[0], '%m/%d/%Y')
            if date >= then:
                with open(bdname, 'w') as bdf:
                    bdf.write(bcontent)
                with open(ldname, 'w') as ldf:
                    ldf.write(lcontent)
            if date >= now:
                now = date + datetime.timedelta(days=1)

        self.data['now'] = encode_datetime(now)

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
        if data['download']:
            download = data['download']
            time = self._time(download['start'], download['end'])
            ts = delta(decode_datetime(download['now']), kwargs['date'])
            success = 'ongoing' if 's' in ts else ''
            danger = 'stalled' if 's' not in ts else ''
            ret['download'] = self._card(download['start'], time,
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

    def _leagues(self):
        leagues = 'resource/download/news/txt/leagues'
        dpath = os.path.join(_root, 'resource/extract/leagues/{}.txt')
        fpath = os.path.join(_root, leagues, 'league_100_{}.txt')
        for key in ['injuries', 'news', 'transactions']:
            dname = dpath.format(key)
            fname = fpath.format(key)
            if not os.path.isfile(dname) or not os.path.isfile(fname):
                continue
            self._leagues_internal(key, dname, fname)

    def _leagues_internal(self, key, dname, fname):
        then = decode_datetime(self.data['then'])
        now = decode_datetime(self.data['now'])

        with open(fname, 'r', encoding='iso-8859-1') as ff:
            content = ff.read()

        with open(dname, 'w') as df:
            match = re.findall('\d{8}\t[^\n]+\n', content.strip() + '\n')
            for m in match:
                date = datetime.datetime.strptime(m[:8], '%Y%m%d')
                if date >= then:
                    df.write(m)
                if date > now:
                    now = date

        self.data['now'] = encode_datetime(now)
