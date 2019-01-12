#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Downloads and extracts league file."""

import logging
import os
import re
import sys

_logger = logging.getLogger('filefairy')
_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/tasks/leaguefile', '', _path))

from api.registrable.registrable import Registrable  # noqa
from common.datetime_.datetime_ import decode_datetime  # noqa
from common.datetime_.datetime_ import encode_datetime  # noqa
from common.subprocess_.subprocess_ import check_output  # noqa
from data.notify.notify import Notify  # noqa
from data.shadow.shadow import Shadow  # noqa
from data.thread_.thread_ import Thread  # noqa
from data.response.response import Response  # noqa

DOWNLOAD_DIR = re.sub(r'/tasks/leaguefile', '/resource/download', _path)
DOMAIN_NAME = 'statsplus.net'
FILE_NAME = 'orange%20and%20blue%20league%20baseball.zip'
FILE_URL = 'https://{}/oblootp/files/{}'.format(DOMAIN_NAME, FILE_NAME)


class Download(Registrable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _href():
        return ''

    @staticmethod
    def _info():
        return 'Manages file download and extraction.'

    @staticmethod
    def _title():
        return 'download'

    def _reload_data(self, **kwargs):
        return {'leaguefile': ['download_file', 'extract_file']}

    def _shadow_data(self, **kwargs):
        return [
            Shadow(
                destination='statsplus',
                key='download.end',
                info=self.data['end'])
        ]

    def _notify_internal(self, **kwargs):
        if kwargs['notify'] == Notify.UPLOAD_FINISH:
            return self.start(**kwargs)

        return Response()

    def start(self, *args, **kwargs):
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
        response = Response(notify=[Notify.DOWNLOAD_FINISH])

        self.data['end'] = encode_datetime(end)
        self.data['start'] = encode_datetime(start)
        if start.year != end.year:
            response.append(notify=Notify.DOWNLOAD_YEAR)
            response.shadow = self._shadow_data(**kwargs)

        self.write()
        return response
