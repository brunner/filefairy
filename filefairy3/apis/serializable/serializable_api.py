#!/usr/bin/env python

import abc
import json
import os
import re
import sys

sys.path.append(re.sub(r'/apis/serializable', '', os.path.dirname(os.path.abspath(__file__))))
from utils.abc.abc_util import abstractstatic  # noqa
from utils.json.json_util import dumps  # noqa


class SerializableApi(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(SerializableApi, self).__init__()
        self.read()

    @abstractstatic
    def _data():
        pass

    def read(self):
        with open(self._data(), 'r') as f:
            self.data = json.loads(f.read())

    def write(self):
        with open(self._data(), 'w') as f:
            f.write(dumps(self.data))
