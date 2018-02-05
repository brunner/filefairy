#!/usr/bin/env python

import json
import os
import re
import sys

sys.path.append(re.sub(r'/utils/testing', '', os.path.dirname(os.path.abspath(__file__))))
from utils.json.json_util import dumps  # noqa


def write(fname, data):
    with open(fname, 'r+') as f:
        original = json.loads(f.read())

        f.seek(0)
        f.write(dumps(data))
        f.truncate()

        return original
