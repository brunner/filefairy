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
from common.json_.json_ import loads  # noqa


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

    @mock.patch('common.json_.json_.open', create=True)
    def test_loads__with_valid_input(self, mock_open):
        data = '{\n  "a": "foo",\n  "b": false,\n  "c": 1\n}'
        mo = mock.mock_open(read_data=data)
        mock_handle = mo()
        mock_open.side_effect = [mo.return_value]

        actual = loads('foo.json')
        expected = {'c': 1, 'b': False, 'a': 'foo'}
        self.assertEqual(actual, expected)

        mock_open.assert_called_once_with('foo.json')
        mock_handle.assert_not_called()
        self.mock_log.assert_not_called()

    @mock.patch('common.json_.json_.open', create=True)
    def test_loads__with_thrown_exception(self, mock_open):
        data = 'a foo b false c 1'
        mo = mock.mock_open(read_data=data)
        mock_handle = mo()
        mock_open.side_effect = [mo.return_value]

        actual = loads('foo.json')
        expected = {}
        self.assertEqual(actual, expected)

        mock_open.assert_called_once_with('foo.json')
        mock_handle.assert_not_called()
        self.mock_log.assert_called_once_with(
            logging.WARNING, 'Handled warning.', exc_info=True)


if __name__ == '__main__':
    unittest.main()
