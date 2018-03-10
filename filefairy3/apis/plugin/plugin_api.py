#!/usr/bin/env python

import abc
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/apis/plugin', '', _path))
from apis.messageable.messageable_api import MessageableApi  # noqa
from apis.runnable.runnable_api import RunnableApi  # noqa
from utils.abc.abc_util import abstractstatic  # noqa


class PluginApi(MessageableApi, RunnableApi):
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        super(PluginApi, self).__init__(**kwargs)

    @abstractstatic
    def _info():
        pass

    @abc.abstractmethod
    def _setup(self, **kwargs):
        pass
