#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extend the serializable API to utilize persistent data storage for a task.

This base class configures a JSON data file for the task, and exposes functions
for performing read and write operations on the file.
"""

import abc
import json
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/api/serializable', '', _path))

from api.nameable.nameable import Nameable  # noqa
from common.abc_.abc_ import abstractstatic  # noqa
from common.json_.json_ import dumps  # noqa


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
