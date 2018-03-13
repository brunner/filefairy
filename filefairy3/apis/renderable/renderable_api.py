#!/usr/bin/env python

import abc
import datetime
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
    def _html():
        pass

    @abstractstatic
    def _title():
        pass

    @abstractstatic
    def _tmpl():
        pass

    @abc.abstractmethod
    def _render_internal(self, **kwargs):
        pass

    def _render(self, **kwargs):
        try:
            title = self._title()
            html = self._html()
            here = os.path.join(_root, 'html', html)
            there = 'brunnerj@' + server + ':/var/www/html/fairylab/' + html
            now = datetime.datetime.now()
            date = now.strftime('%Y-%m-%d %H:%M:%S') + ' PST'
            tmpl = self.environment.get_template(self._tmpl())
            ret = self._render_internal(**kwargs)
            ts = tmpl.stream(dict(ret, title=title, date=date))
            ts.dump(here)
            check_output(['scp', here, there])
        except Exception:
            exc = traceback.format_exc()
            log(self._name(), s='Exception.', c=exc, v=True)
