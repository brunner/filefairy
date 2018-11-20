#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for json_.py."""

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
    def setUp(self):
        patch_log = mock.patch('common.json_.json_._logger.log')
        self.addCleanup(patch_log.stop)
        self.mock_log = patch_log.start()

    def test_dumps__with_valid_input(self):
        actual = dumps({'c': 1, 'b': False, 'a': 'foo'})
        expected = '{\n  "a": "foo",\n  "b": false,\n  "c": 1\n}'
        self.assertEqual(actual, expected)

        self.mock_log.assert_not_called()

    def test_dumps__with_thrown_exception(self):
        actual = dumps({'a': FakeObject()})
        expected = '{\n  "a": ""\n}'
        self.assertEqual(actual, expected)

        self.mock_log.assert_called_once_with(
            logging.WARNING, 'Handled warning.', exc_info=True)


if __name__ == '__main__':
    unittest.main()
