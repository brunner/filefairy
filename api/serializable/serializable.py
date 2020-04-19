#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extend the serializable API to utilize persistent data storage for a task.

This base class configures a JSON data file for the task, and exposes functions
for performing read and write operations on the file, as well as archiving the
file data.
"""

import abc
import json
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/api/serializable', '', _path))

from common.json_.json_ import dumps  # noqa

DATA_DIR = re.sub(r'/api/serializable', '', _path) + '/resources/data'


class Serializable():
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        super(Serializable, self).__init__(**kwargs)

        self.data = self.read()

    def _data(self):
        d = self.__class__.__name__.lower()
        return os.path.join(DATA_DIR, d, 'data.json')

    def read(self, *args, **kwargs):
        try:
            with open(self._data(), 'r') as f:
                return json.loads(f.read())
        except FileNotFoundError:
            return {}

    def write(self, *args, **kwargs):
        with open(self._data(), 'w') as f:
            f.write(dumps(self.data) + '\n')
