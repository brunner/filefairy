#!/usr/bin/env python

import abc
import os
import re
import sys
import traceback

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/apis/renderable', '', _path))
from apis.serializable.serializable_api import SerializableApi  # noqa
from utils.abc.abc_util import abstractstatic  # noqa
from utils.logger.logger_util import log  # noqa


class RenderableApi(SerializableApi):
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        super(RenderableApi, self).__init__(**kwargs)
        self.environment = kwargs.get('e', None)

    @abstractstatic
    def _html():
        pass

    @abstractstatic
    def _tmpl():
        pass

    @abc.abstractmethod
    def _render_internal(self, **kwargs):
        pass

    def _render(self, **kwargs):
        try:
            tmpl = self.environment.get_template(self._tmpl())
            tmpl.stream(self._render_internal(**kwargs)).dump(self._html())
        except Exception:
            exc = traceback.format_exc()
            log(self._name(), s='Exception.', c=exc, v=True)
