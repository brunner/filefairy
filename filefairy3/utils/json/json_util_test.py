#!/usr/bin/env python

from json_util import dumps

import unittest


class JsonUtilTest(unittest.TestCase):
    def test_dumps(self):
        data = {'c': 1, 'b': 2, 'a': 3}
        actual = dumps(data)
        expected = '{\n  "a": 3, \n  "b": 2, \n  "c": 1\n}'
        self.assertEquals(actual, expected)


if __name__ == '__main__':
    unittest.main()
