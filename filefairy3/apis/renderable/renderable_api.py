#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc
import errno
import os
import re
import sys
import traceback

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/apis/renderable', '', _path)
sys.path.append(_root)
from apis.serializable.serializable_api import SerializableApi  # noqa
from utils.abc.abc_util import abstractstatic  # noqa
from utils.logger.logger_util import log  # noqa
from utils.secrets.secrets_util import server  # noqa
from utils.subprocess.subprocess_util import check_output  # noqa


class RenderableApi(SerializableApi):
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        super(RenderableApi, self).__init__(**kwargs)
        self.environment = kwargs['e']

    @abstractstatic
    def _href():
        pass

    @abstractstatic
    def _title():
        pass

    @abstractstatic
    def _render_internal():
        pass

    def _render(self, **kwargs):
        date = kwargs['date'].strftime('%Y-%m-%d %H:%M:%S') + ' PST'

        _title = self._title()
        for html, subtitle, tmpl, context in self._render_internal(**kwargs):
            try:
                subtitle = ' » ' + subtitle if subtitle else ''
                title = _title + subtitle
                tmpl = self.environment.get_template(tmpl)
                ts = tmpl.stream(dict(context, title=title, date=date))
                here = os.path.join(_root, html)
                there = 'brunnerj@' + server + ':/var/www/' + html
                self._mkdir_p(here.rsplit('/', 1)[0])
                ts.dump(here)
                check_output(['scp', here, there])
            except Exception:
                exc = traceback.format_exc()
                log(self._name(), s='Exception.', c=exc, v=True)

    @staticmethod
    def _mkdir_p(path):
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise
