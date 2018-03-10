#!/usr/bin/env python

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/utils/json', '', _path))
from utils.json.json_util import dumps  # noqa


class FakeObject(object):
    def __init__(self):
        self.a = 1


class JsonUtilTest(unittest.TestCase):
    def test_dumps(self):
        data = {'c': 1, 'b': FakeObject(), 'a': 'foo'}
        actual = dumps(data)
        expected = '{\n  "a": "foo", \n  "b": "", \n  "c": 1\n}'
        self.assertEquals(actual, expected)


if __name__ == '__main__':
    unittest.main()
