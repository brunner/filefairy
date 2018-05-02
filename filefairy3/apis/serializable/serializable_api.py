#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc
import json
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/apis/serializable', '', _path))
from apis.nameable.nameable_api import NameableApi  # noqa
from utils.abc.abc_util import abstractstatic  # noqa
from utils.json.json_util import dumps  # noqa
from utils.logger.logger_util import log  # noqa


class SerializableApi(NameableApi):
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        super(SerializableApi, self).__init__(**kwargs)
        self.read()

    def _name(self):
        return self.__class__.__name__

    @abstractstatic
    def _data():
        pass

    def read(self, **kwargs):
        with open(self._data(), 'r') as f:
            self.data = json.loads(f.read())
            log(self._name(), **dict(kwargs, s='Read completed.'))

    def write(self, **kwargs):
        with open(self._data(), 'w') as f:
            f.write(dumps(self.data) + '\n')
            log(self._name(), **dict(kwargs, s='Write completed.'))

    def dump(self, **kwargs):
        d = dumps(self.data)
        log(self._name(), **dict(kwargs, s='Dump completed.', c=d))
