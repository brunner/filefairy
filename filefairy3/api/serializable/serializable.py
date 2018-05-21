#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import abc
import json
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/api/serializable', '', _path))
from api.nameable.nameable import Nameable  # noqa
from util.abc_.abc_ import abstractstatic  # noqa
from util.json_.json_ import dumps  # noqa
from util.logger.logger import log  # noqa


class Serializable(Nameable):
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        super(Serializable, self).__init__(**kwargs)
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
