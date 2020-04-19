#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extend the serializable API to utilize persistent data storage for a task.

This base class configures a JSON data file for the task, and exposes functions
for performing read and write operations on the file, as well as archiving the
file data.
"""

import abc
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/api/serializable', '', _path))

from common.io_.io_ import read_data  # noqa
from common.io_.io_ import write_data  # noqa

DATA_DIR = re.sub(r'/api/serializable', '', _path) + '/resources/data'


class Serializable():
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        super(Serializable, self).__init__(**kwargs)

        self.data = self._read()

    def _data_name(self):
        return self.__class__.__name__.lower()

    def _read(self, *args, **kwargs):
        return read_data(self._data_name())

    def _write(self, *args, **kwargs):
        write_data(self._data_name(), self.data)
