#!/usr/bin/env python

from json_util import dumps

import unittest


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
