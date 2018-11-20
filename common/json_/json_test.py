#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/common/json_', '', _path))
from common.json_.json_ import dumps  # noqa


class FakeObject(object):
    def __init__(self):
        self.a = 1


class JsonTest(unittest.TestCase):
    @mock.patch('common.json_.json_.logger_.log')
    def test_dumps__with_valid_input(self, mock_log):
        data = {'c': 1, 'b': False, 'a': 'foo'}
        actual = dumps(data)
        expected = '{\n  "a": "foo",\n  "b": false,\n  "c": 1\n}'
        self.assertEqual(actual, expected)
        mock_log.assert_not_called()

    @mock.patch('common.json_.json_.logger_.log')
    def test_dumps__with_thrown_exception(self, mock_log):
        data = {'a': FakeObject()}
        actual = dumps(data)
        expected = '{\n  "a": ""\n}'
        self.assertEqual(actual, expected)
        mock_log.assert_called_once_with(
            logging.WARNING, 'Handled warning.', exc_info=True)


if __name__ == '__main__':
    unittest.main()
