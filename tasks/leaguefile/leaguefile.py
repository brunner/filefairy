#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reports current file upload progress. Downloads file when upload is done."""

import copy
import datetime
import logging
import os
import re
import sys

_logger = logging.getLogger('fairylab')
_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/tasks/leaguefile', '', _path))

from api.registrable.registrable import Registrable  # noqa
from api.reloadable.reloadable import Reloadable  # noqa
from common.datetime_.datetime_ import decode_datetime  # noqa
from common.datetime_.datetime_ import encode_datetime  # noqa
from common.datetime_.datetime_ import timedelta  # noqa
from common.datetime_.datetime_ import timestamp  # noqa
from common.elements.elements import card  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import table  # noqa
from common.secrets.secrets import server  # noqa
from common.subprocess_.subprocess_ import check_output  # noqa
from data.notify.notify import Notify  # noqa
from data.shadow.shadow import Shadow  # noqa
from data.thread_.thread_ import Thread  # noqa
from data.response.response import Response  # noqa

COLS = [col(clazz=c) for c in ('', 'text-center', 'text-center', 'text-right')]
DELTA_2_MIN = datetime.timedelta(minutes=2)
DOWNLOAD_DIR = re.sub(r'/tasks/leaguefile', '/resource/download', _path)
FILE_HOST = 'www.orangeandblueleaguebaseball.com'
FILE_NAME = 'orange_and_blue_league_baseball.tar.gz'
FILE_URL = 'https://{}/StatsLab/league_file/{}'.format(FILE_HOST, FILE_NAME)
HEAD = [cell(content=c) for c in ('Date', 'Upload', 'Download', 'Size')]


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
        return {
            'leaguefile':
            ['download_file', 'extract_file', 'find_download', 'find_upload']
        }

    def _run_internal(self, **kwargs):
        data = self.data

        if data['download'] and data['upload']:
            response = self._get_download(**kwargs)
        else:
            response = self._get_upload(**kwargs)

        if data['upload'] and not response.notify:
            now = kwargs['date']
            if decode_datetime(data['date']) < now - DELTA_2_MIN:
                data['date'] = encode_datetime(now)
                response.notify = [Notify.BASE]
                self.write()

        if response.notify:
            self._render(**kwargs)

        return response

    def _render_internal(self, **kwargs):
        index_html = self._index_html(**kwargs)
        return [('leaguefile/index.html', '', 'leaguefile.html', index_html)]

    def _setup_internal(self, **kwargs):
        self._reload(**kwargs)

        if self.data['download']:
            return Response(
                thread_=[Thread(target='_download_start', kwargs=kwargs)])

        data = self.data
        original = copy.deepcopy(data)

        now = kwargs['date']
        upload = self._call('find_upload', (now, ))
        if upload:
            size, time, ongoing = upload
            if ongoing:
                encoded_time = encode_datetime(time)
                data['upload'] = {
                    'end': encoded_time,
                    'now': encode_datetime(now),
                    'size': size,
                    'start': encoded_time
                }

        if data != original:
            self.write()

        self._render(**kwargs)
        return Response()

    def _shadow_internal(self, **kwargs):
        return [
            Shadow(
                destination='statsplus',
                key='leaguefile.end',
                info=self.data['end'])
        ]

    def download(self, *args, **kwargs):
        return Response(
            thread_=[Thread(target='_download_start', kwargs=kwargs)])

    def _download_file(self, *args, **kwargs):
        now = encode_datetime(kwargs['date'])
        self.data['download'] = {'end': now, 'start': now}

        output = self._call('download_file', (FILE_URL, ))
        if output.get('ok'):
            _logger.log(logging.INFO, 'Download finished.')
            response = self._extract_file(**kwargs)
        else:
            extra = {'stdout': output['stdout'], 'stderr': output['stderr']}
            _logger.log(logging.WARNING, 'Download failed.', extra=extra)
            response = Response(
                thread_=[Thread(target='_download_start', kwargs=kwargs)])

        self.write()
        return response

    def _download_start(self, **kwargs):
        output = check_output(['ping', '-c 1', FILE_HOST], timeout=8)
        if output.get('ok') and self.data['upload']:
            _logger.log(logging.INFO, 'Download started.')
            return self._download_file(**kwargs)

        extra = {'stdout': output['stdout'], 'stderr': output['stderr']}
        _logger.log(logging.WARNING, 'Download failed.', extra=extra)
        return Response(
            thread_=[Thread(target='_download_start', kwargs=kwargs)])

    def _extract_file(self, **kwargs):
        start = decode_datetime(self.data['end'])
        end = self._call('extract_file', (start, ))
        response = Response(notify=[Notify.LEAGUEFILE_DOWNLOAD])

        self.data['end'] = encode_datetime(end)
        self.data['start'] = encode_datetime(start)
        if start.year != end.year:
            response.append(notify=Notify.LEAGUEFILE_YEAR)
            response.shadow = self._shadow_internal(**kwargs)

        self.write()
        return response

    def _get_download(self, **kwargs):
        now = kwargs['date']

        download = self._call('find_download', (now, ))
        if download is None:
            return Response()

        size, timestamp, ongoing = download
        if ongoing:
            self.data['download'].update({
                'end': encode_datetime(timestamp),
                'now': encode_datetime(now),
                'size': size
            })
            self.write()
        else:
            self._set_completed()

        return Response(notify=[Notify.BASE])

    def _get_upload(self, **kwargs):
        response = Response()
        upload = self._call('find_upload', (kwargs['date'], ))
        if upload is None:
            return response

        size, timestamp, ongoing = upload
        if ongoing:
            response = self._handle_ongoing(size, timestamp, **kwargs)
        elif self.data['upload']:
            response = self._handle_uploaded(size, timestamp, **kwargs)

        return response

    def _handle_ongoing(self, size, timestamp, **kwargs):
        data = self.data
        original = copy.deepcopy(data)

        response = Response()

        now = kwargs['date']
        encoded_date = encode_datetime(timestamp)
        encoded_now = encode_datetime(now)

        if not data['upload']:
            data['upload'] = {'start': encoded_date}
            self._chat('fairylab', 'Upload started.')
            response.notify = [Notify.LEAGUEFILE_START]

        if data['upload'].get('size') != size:
            data['upload'].update({
                'end': encoded_date,
                'now': encoded_now,
                'size': size
            })
            if data['stalled'] and not response.notify:
                response.notify = [Notify.BASE]
            data['stalled'] = False
        elif timestamp < now - DELTA_2_MIN:
            if not data['stalled'] and not response.notify:
                response.notify = [Notify.BASE]
            data['stalled'] = True

        if data != original:
            self.write()

        return response

    def _handle_uploaded(self, size, timestamp, **kwargs):
        encoded_now = encode_datetime(kwargs['date'])
        encoded_time = encode_datetime(timestamp)

        self.data['upload'].update({
            'end': encoded_time,
            'now': encoded_now,
            'size': size
        })
        self.write()

        self._chat('fairylab', 'File is up.')
        return Response(
            notify=[Notify.LEAGUEFILE_FINISH],
            thread_=[Thread(target='_download_start', kwargs=kwargs)])

    def _set_completed(self):
        download = self.data['download']
        download_end = decode_datetime(download['end'])
        download_start = decode_datetime(download['start'])

        upload = self.data['upload']
        upload_end = decode_datetime(upload['end'])
        upload_start = decode_datetime(upload['start'])

        completed = {
            'download': timedelta(download_start, download_end),
            'size': upload['size'],
            'start': upload['start'],
            'upload': timedelta(upload_start, upload_end),
        }
        self.data['completed'].insert(0, completed)
        self.data['download'] = None
        self.data['upload'] = None

        self.write()

    def _index_html(self, **kwargs):
        ret = {
            'breadcrumbs': [{
                'href': '/',
                'name': 'Fairylab'
            }, {
                'href': '',
                'name': 'Leaguefile'
            }]
        }

        download = self.data['download']
        upload = self.data['upload']
        stalled = self.data['stalled']

        if upload:
            ts = timestamp(decode_datetime(upload['now']))
            success = 'completed' if download else '' if stalled else 'ongoing'
            danger = 'stalled' if stalled else ''
            ret['upload'] = self._card(upload, ts, success, danger)

        if download:
            ts = timestamp(decode_datetime(download['end']))
            ret['download'] = self._card(download, ts, 'ongoing', '')

        body = []
        for completed in self.data['completed']:
            date = decode_datetime(completed['start']).strftime('%b %d')
            body.append([
                cell(content=date),
                cell(content=completed['upload']),
                cell(content=completed['download']),
                cell(content='{:,}'.format(int(completed['size'])))
            ])
        ret['completed'] = table(hcols=COLS, bcols=COLS, head=HEAD, body=body)

        return ret

    @staticmethod
    def _card(obj, ts, success, danger):
        decoded_start = decode_datetime(obj['start'])
        decoded_end = decode_datetime(obj['end'])

        return card(
            title=decoded_start.strftime('%b %d'),
            table=table(
                clazz='table-sm',
                bcols=[col(clazz='w-55p'), col()],
                body=[[
                    cell(content='Time: '),
                    cell(content=timedelta(decoded_start, decoded_end))
                ], [
                    cell(content='Size: '),
                    cell(content='{:,}'.format(int(obj['size'])))
                ]]),
            ts=ts,
            success=success,
            danger=danger)
