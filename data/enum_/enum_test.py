#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for enum_.py."""

import logging
import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/data/enum_', '', _path))

from data.enum_.enum_ import Enum  # noqa


class FakeEnum(Enum):
    FOO = 1


class JsonTest(unittest.TestCase):
    def setUp(self):
        patch_log = mock.patch('data.enum_.enum_._logger.log')
        self.addCleanup(patch_log.stop)
        self.mock_log = patch_log.start()

    def test_decode__args(self):
        actual = FakeEnum.decode('foo data 1')
        expected = (FakeEnum.FOO, ['data', '1'])
        self.assertEqual(actual, expected)

        self.mock_log.assert_not_called()

    def test_decode__exception(self):
        actual = FakeEnum.decode('bar')
        expected = (None, [])
        self.assertEqual(actual, expected)

        self.mock_log.assert_called_once_with(
            logging.WARNING, 'Handled warning.', exc_info=True)

    def test_decode__member(self):
        actual = FakeEnum.decode('foo')
        expected = (FakeEnum.FOO, [])
        self.assertEqual(actual, expected)

        self.mock_log.assert_not_called()

    def test_encode__args(self):
        actual = FakeEnum.FOO.encode('data', '1')
        expected = 'foo data 1'
        self.assertEqual(actual, expected)

        self.mock_log.assert_not_called()

    def test_encode__member(self):
        actual = FakeEnum.FOO.encode()
        expected = 'foo'
        self.assertEqual(actual, expected)

        self.mock_log.assert_not_called()


if __name__ == '__main__':
    unittest.main()
