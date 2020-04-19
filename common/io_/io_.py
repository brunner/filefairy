#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Common (non-reloadable) util methods for reading and writing data."""

import json
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/common/io_', '', _path))

from common.json_.json_ import dumps  # noqa

DATA_DIR = re.sub(r'/common/io_', '', _path) + '/resources/data'


def read_data(name, key=None):
    """Reads data from a specified file.

    If the data key is provided, returns the specific corresponding value.
    Otherwise, returns all of the read data.

    Args:
        name: The lowercase name of the data directory to read from.
        key: The optional data key to read.
    Returns:
        The read data.
    """
    filename = os.path.join(DATA_DIR, name, 'data.json')
    with open(filename, 'r') as f:
        data = json.loads(f.read())
        return data if key is None else data[key]


def write_data(name, data):
    """Writes data to a specified file.
    Args:
        name: The lowercase name of the data directory to write to.
        data: The data to write.
    """
    filename = os.path.join(DATA_DIR, name, 'data.json')
    with open(filename, 'w') as f:
        f.write(dumps(data) + '\n')
