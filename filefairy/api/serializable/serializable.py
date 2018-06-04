#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import abc
import json
import logging
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/api/serializable', '', _path))
from api.nameable.nameable import Nameable  # noqa
from util.abc_.abc_ import abstractstatic  # noqa
from util.json_.json_ import dumps  # noqa

logger_ = logging.getLogger('fairylab')


class Serializable(Nameable):
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.read()

    def _name(self):
        return self.__class__.__name__

    @abstractstatic
    def _data():
        pass

    def read(self, *args, **kwargs):
        with open(self._data(), 'r') as f:
            self.data = json.loads(f.read())

    def write(self, *args, **kwargs):
        with open(self._data(), 'w') as f:
            f.write(dumps(self.data) + '\n')

    def dump(self, *args, **kwargs):
        d = dumps(self.data)
        logger_._log(logging.DEBUG, 'Dump completed.', extra={'output': d})
