#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reports current file upload progress. Downloads file when upload is done."""

import datetime
import logging
import os
import re
import sys

_logger = logging.getLogger('filefairy')
_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/tasks/leaguefile', '', _path))

from api.registrable.registrable import Registrable  # noqa
from api.reloadable.reloadable import Reloadable  # noqa
from common.datetime_.datetime_ import datetime_as_pst  # noqa
from common.datetime_.datetime_ import datetime_datetime_cst  # noqa
from common.datetime_.datetime_ import decode_datetime  # noqa
from common.datetime_.datetime_ import encode_datetime  # noqa
from common.datetime_.datetime_ import timedelta  # noqa
from common.datetime_.datetime_ import timestamp  # noqa
from common.elements.elements import card  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import table  # noqa
from common.re_.re_ import find  # noqa
from common.requests_.requests_ import get  # noqa
from common.secrets.secrets import server  # noqa
from common.subprocess_.subprocess_ import check_output  # noqa
from data.notify.notify import Notify  # noqa
from data.shadow.shadow import Shadow  # noqa
from data.thread_.thread_ import Thread  # noqa
from data.response.response import Response  # noqa

DOWNLOAD_DIR = re.sub(r'/tasks/leaguefile', '/resource/download', _path)
DOMAIN_NAME = 'statsplus.net'
EXPORTS_URL = 'https://{}/oblootp/exports/'.format(DOMAIN_NAME)
FILE_NAME = 'orange%20and%20blue%20league.zip'
FILE_URL = 'https://{}/oblootp/files/{}'.format(DOMAIN_NAME, FILE_NAME)


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
        return 'Reports current file upload status.'

    @staticmethod
    def _title():
        return 'leaguefile'

    def _notify_internal(self, **kwargs):
        return Response()

    def _on_message_internal(self, **kwargs):
        return Response()

    def _reload_internal(self, **kwargs):
        return {'leaguefile': ['download_file', 'extract_file']}

    def _render_internal(self, **kwargs):
        index_html = self._index_html(**kwargs)
        return [('leaguefile/index.html', '', 'leaguefile.html', index_html)]

    def _run_internal(self, **kwargs):
        completed = self._get_completed()
        response = Response()

        if completed is not None and completed != self.data['completed'][0]:
            self._chat('fairylab', 'File is up.')

            response.append(notify=Notify.BASE)
            response.append(notify=Notify.LEAGUEFILE_UPLOAD)
            response.append(
                thread_=Thread(target='_download_start', kwargs=kwargs))

            self.data['completed'].insert(0, completed)
            self.write()
            self._render(**kwargs)

        return response

    def _setup_internal(self, **kwargs):
        self._reload(**kwargs)
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
        output = self._call('download_file', (FILE_URL, ))
        if output.get('ok'):
            _logger.log(logging.INFO, 'Download finished.')
            response = self._extract_file(**kwargs)
        else:
            extra = {'stdout': output['stdout'], 'stderr': output['stderr']}
            _logger.log(logging.WARNING, 'Download failed.', extra=extra)
            response = Response(
                thread_=[Thread(target='_download_start', kwargs=kwargs)])

        return response

    def _download_start(self, **kwargs):
        output = check_output(['ping', '-c 1', DOMAIN_NAME], timeout=10)
        if output.get('ok'):
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

        cols = [col(), col(clazz='text-right')]
        head = [cell(content='Date'), cell(content='Size')]
        body = []
        for completed in self.data['completed']:
            date = decode_datetime(completed['date']).strftime('%b %d')
            body.append([
                cell(content=date),
                cell(content=completed['size'])
            ])
        ret['completed'] = table(hcols=cols, bcols=cols, head=head, body=body)

        return ret

    @staticmethod
    def _get_completed():
        text = get(EXPORTS_URL)

        match = find(r'(?s)League File: (.+?) CST', text)
        if match:
            date_string = re.sub('[.,]', '', match.title())
            d = datetime.datetime.strptime(date_string, '%b %d %Y %I:%M %p')
            c = datetime_datetime_cst(d.year, d.month, d.day, d.hour, d.minute)

            date = encode_datetime(datetime_as_pst(c))
            size = find(r'(?s)\(Size: ([^)]+)\)', text)

            return {'date': date, 'size': size}
