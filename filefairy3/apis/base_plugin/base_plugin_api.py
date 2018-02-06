#!/usr/bin/env python

import abc
import os
import re
import sys

sys.path.append(re.sub(r'/apis/plugin', '', os.path.dirname(os.path.abspath(__file__))))
from apis.messageable.messageable_api import MessageableApi  # noqa
from apis.runnable.runnable_api import RunnableApi  # noqa


class BasePluginApi(MessageableApi, RunnableApi):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(BasePluginApi, self).__init__()
