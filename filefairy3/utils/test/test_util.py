#!/usr/bin/env python

import json
import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/utils/test', '', _path))
from utils.json.json_util import dumps  # noqa


class TestUtil(unittest.TestCase):
    def write(self, fname, data):
        with open(fname, 'r+') as f:
            original = json.loads(f.read())
            f.seek(0)
            f.write(dumps(data))
            f.write('\n')
            f.truncate()
            return original
