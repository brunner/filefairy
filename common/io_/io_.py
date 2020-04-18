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


def _get_filename(name):
    return os.path.join(DATA_DIR, name, 'data.json')


def read(name):
    """Reads data from a specified file.

    Args:
        name: The lowercase name of the Renderable class to read the data from.
    Returns:
        The read data.
    """
    filename = _get_filename(name)
    with open(filename, 'r') as f:
        return json.loads(f.read())


def write(name, data):
    """Writes data to a specified file.

    Args:
        name: The lowercase name of the Renderable class to write the data to.
        data: The data to write.
    """
    filename = _get_filename(name)
    with open(filename, 'w') as f:
        f.write(dumps(data) + '\n')
