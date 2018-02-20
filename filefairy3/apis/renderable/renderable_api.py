#!/usr/bin/env python

import abc
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/apis/renderable', '', _path))
from utils.abc.abc_util import abstractstatic  # noqa


class RenderableApi(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(RenderableApi, self).__init__()
        self.read()

    @abstractstatic
    def _html():
        pass

    @abc.abstractmethod
    def _render_internal(self):
        pass

    def _render(self):
        with open(self._html(), 'w') as f:
            f.write(self._render_internal())
