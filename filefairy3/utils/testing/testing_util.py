#!/usr/bin/env python

import json
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/utils/testing', '', _path))
from utils.json.json_util import dumps  # noqa


def write(fname, data):
    with open(fname, 'r+') as f:
        original = json.loads(f.read())

        f.seek(0)
        f.write(dumps(data))
        f.write('\n')
        f.truncate()

        return original
