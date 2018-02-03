#!/usr/bin/env python

import abc
import json
import os
import re
import sys

import logging
logging.basicConfig()

sys.path.append(re.sub(r'/apis/plugin', '', os.path.dirname(__file__)))
from apis.base_plugin.base_plugin_api import BasePluginApi  # noqa
from utils.abc.abc_util import abstractstatic  # noqa


class DataPluginApi(BasePluginApi):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(DataPluginApi, self).__init__()
        self.read()

    @abstractstatic
    def _data():
        pass

    def read(self, *args):
        with open(self._data(), 'r') as f:
            self.data = json.loads(f.read())
            return self._chats('Read completed.', None, args)

    def write(self, *args):
        with open(self._data(), 'w') as f:
            f.write(json.dumps(self.data, indent=2, sort_keys=True))
            return self._chats('Write completed.', None, args)

    def dump(self, *args):
        d = json.dumps(self.data, indent=2, sort_keys=True)
        return self._chats('Dumping data.', d, args)
