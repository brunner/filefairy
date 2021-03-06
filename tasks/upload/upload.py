#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Alerts whenever a new league file is uploaded."""

import datetime
import logging
import os
import re
import sys

_logger = logging.getLogger('filefairy')
_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/tasks/upload', '', _path))

from api.runnable.runnable import Runnable  # noqa
from api.serializable.serializable import Serializable  # noqa
from common.datetime_.datetime_ import datetime_as_pst  # noqa
from common.datetime_.datetime_ import datetime_datetime_cst  # noqa
from common.datetime_.datetime_ import encode_datetime  # noqa
from common.re_.re_ import search  # noqa
from common.requests_.requests_ import get  # noqa
from common.slack.slack import chat_post_message  # noqa
from types_.notify.notify import Notify  # noqa
from types_.response.response import Response  # noqa

DATA_DIR = re.sub(r'/tasks/upload', '', _path) + '/resources/data/upload'
EXPORTS_URL = 'https://statsplus.net/oblootp/exports/'


class Upload(Runnable, Serializable):
    def __init__(self, **kwargs):
        super(Upload, self).__init__(**kwargs)

    def _run_internal(self, **kwargs):
        # TODO: uncomment after finishing refactors.
        # date = self.get_file_date()
        # if date is not None and date != self.data['date']:
        #     _logger.log(logging.INFO, 'File is up.')
        #     chat_post_message('fairylab', 'File is up.')

        #     self.data['date'] = date
        #     self._write()

        #     return Response(notify=[Notify.UPLOAD_FINISH])

        return Response()

    @staticmethod
    def get_file_date():
        text = re.sub('[.,]', '', get(EXPORTS_URL))
        match = search(r'(?s)League File: (\w+ \d+ \d+ [\d:]+ \w+) C', text)
        if match:
            month, day, year, time, period = match.split()
            if ':' not in time:
                time = time + ':00'

            match = ' '.join([month[:3], day, year, time, period])
            d = datetime.datetime.strptime(match.title(), '%b %d %Y %I:%M %p')
            c = datetime_datetime_cst(d.year, d.month, d.day, d.hour, d.minute)

            return encode_datetime(datetime_as_pst(c))
