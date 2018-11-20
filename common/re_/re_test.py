#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for re_.py."""

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/common/re_', '', _path))
from common.re_.re_ import find  # noqa


class ReTest(unittest.TestCase):
    def test_find__empty_multiple_match(self):
        actual = find(r'(\d)\D(\d)', 'abcd1234')
        expected = [None, None]
        self.assertEqual(actual, expected)

    def test_find__empty_single_match(self):
        actual = find(r'\d(\D)\d', 'abcd1234')
        expected = None
        self.assertEqual(actual, expected)

    def test_find__found_multiple_match(self):
        actual = find(r'(\d)\D(\d)', 'a1b2c3d4')
        expected = ['1', '2']
        self.assertEqual(actual, expected)

    def test_find__found_single_match(self):
        actual = find(r'\d(\D)\d', 'a1b2c3d4')
        expected = 'b'
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
