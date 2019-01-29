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
from common.re_.re_ import findall  # noqa
from common.re_.re_ import match  # noqa


class ReTest(unittest.TestCase):
    def test_find__empty_multiple_group(self):
        actual = find(r'(\d)\D(\d)', '1234abcd')
        expected = [None, None]
        self.assertEqual(actual, expected)

    def test_find__empty_single_group(self):
        actual = find(r'\d(\D)\d', '1234abcd')
        expected = None
        self.assertEqual(actual, expected)

    def test_find__empty_single_match(self):
        actual = find(r'\d\D\d', '1234abcd')
        expected = None
        self.assertEqual(actual, expected)

    def test_find__found_anywhere_group(self):
        actual = find(r'(\d)\D(\d)', 'a1b2c3d4')
        expected = ['1', '2']
        self.assertEqual(actual, expected)

    def test_find__found_multiple_group(self):
        actual = find(r'(\d)\D(\d)', '1a2b3c4d')
        expected = ['1', '2']
        self.assertEqual(actual, expected)

    def test_find__found_single_group(self):
        actual = find(r'\d(\D)\d', '1a2b3c4d')
        expected = 'a'
        self.assertEqual(actual, expected)

    def test_find__found_single_match(self):
        actual = find(r'\d\D\d', '1a2b3c4d')
        expected = '1a2'
        self.assertEqual(actual, expected)

    def test_findall__empty_multiple_group(self):
        actual = findall(r'(\d)\D(\d)', '1234abcd')
        expected = []
        self.assertEqual(actual, expected)

    def test_findall__empty_single_group(self):
        actual = findall(r'\d(\D)\d', '1234abcd')
        expected = []
        self.assertEqual(actual, expected)

    def test_findall__empty_single_match(self):
        actual = findall(r'\d\D\d', '1234abcd')
        expected = []
        self.assertEqual(actual, expected)

    def test_findall__found_multiple_group(self):
        actual = findall(r'(\d)\D(\d)', '1a2b3c4d')
        expected = [['1', '2'], ['3', '4']]
        self.assertEqual(actual, expected)

    def test_findall__found_single_group(self):
        actual = findall(r'\d(\D)\d', '1a2b3c4d')
        expected = ['a', 'c']
        self.assertEqual(actual, expected)

    def test_findall__found_single_match(self):
        actual = findall(r'\d\D\d', '1a2b3c4d')
        expected = ['1a2', '3c4']
        self.assertEqual(actual, expected)

    def test_match__empty_multiple_group(self):
        actual = match(r'(\d)\D(\d)', '1234abcd')
        expected = None
        self.assertEqual(actual, expected)

    def test_match__empty_single_group(self):
        actual = match(r'\d(\D)\d', '1234abcd')
        expected = None
        self.assertEqual(actual, expected)

    def test_match__empty_single_match(self):
        actual = match(r'\d\D\d', '1234abcd')
        expected = None
        self.assertEqual(actual, expected)

    def test_match__found_anywhere_group(self):
        actual = match(r'(\d)\D(\d)', 'a1b2c3d4')
        expected = None
        self.assertEqual(actual, expected)

    def test_match__found_multiple_group(self):
        actual = match(r'(\d)\D(\d)', '1a2b3c4d')
        expected = ['1', '2']
        self.assertEqual(actual, expected)

    def test_match__found_single_group(self):
        actual = match(r'\d(\D)\d', '1a2b3c4d')
        expected = ['a']
        self.assertEqual(actual, expected)

    def test_match__found_single_match(self):
        actual = match(r'\d\D\d', '1a2b3c4d')
        expected = []
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
