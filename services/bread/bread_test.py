#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for bread.py."""

import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/services/bread', '', _path))

from services.bread.bread import SNACKS  # noqa
from services.bread.bread import snack_me  # noqa


class BreadTest(unittest.TestCase):
    @mock.patch('services.bread.bread.random.choice')
    def test_snacks__diff_diff_diff(self, mock_random):
        mock_random.side_effect = ['a', 'b', 'c']

        actual = snack_me()
        expected = ('a', 'b', 'c')
        self.assertEqual(actual, expected)

        mock_random.assert_has_calls([mock.call(SNACKS)] * 3)

    @mock.patch('services.bread.bread.random.choice')
    def test_snacks__diff_same_same(self, mock_random):
        mock_random.side_effect = ['a', 'b', 'b']

        actual = snack_me()
        expected = ('b', 'star', 'a')
        self.assertEqual(actual, expected)

        mock_random.assert_has_calls([mock.call(SNACKS)] * 3)

    @mock.patch('services.bread.bread.random.choice')
    def test_snacks__same_diff_same(self, mock_random):
        mock_random.side_effect = ['a', 'b', 'a']

        actual = snack_me()
        expected = ('a', 'star', 'b')
        self.assertEqual(actual, expected)

        mock_random.assert_has_calls([mock.call(SNACKS)] * 3)

    @mock.patch('services.bread.bread.random.choice')
    def test_snacks_same_same_diff(self, mock_random):
        mock_random.side_effect = ['a', 'a', 'b']

        actual = snack_me()
        expected = ('a', 'star', 'b')
        self.assertEqual(actual, expected)

        mock_random.assert_has_calls([mock.call(SNACKS)] * 3)

    @mock.patch('services.bread.bread.random.choice')
    def test_snacks__same_same_same(self, mock_random):
        mock_random.side_effect = ['a', 'a', 'a']

        actual = snack_me()
        expected = ('a', 'star', 'trophy')
        self.assertEqual(actual, expected)

        mock_random.assert_has_calls([mock.call(SNACKS)] * 3)


if __name__ == '__main__':
    unittest.main()
