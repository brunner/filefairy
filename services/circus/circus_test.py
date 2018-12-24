#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for circus.py."""

import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/services/circus', '', _path))

from common.nltk_.nltk_ import get_cfd  # noqa
from services.circus.circus import DECIDES  # noqa
from services.circus.circus import WAFFLES  # noqa
from services.circus.circus import choose  # noqa
from services.circus.circus import discuss  # noqa
from services.circus.circus import who  # noqa

N = 2

CFD = get_cfd(N, ['The quick brown fox.', 'Jumps over the lazy dog.'])


class BreadTest(unittest.TestCase):
    @mock.patch('services.circus.circus.random.choice')
    def test_choose__one(self, mock_choice):
        mock_choice.side_effect = ['{}. Did you even need to ask?', 'a']

        actual = choose(['a'])
        expected = 'A. Did you even need to ask?'
        self.assertEqual(actual, expected)

        mock_choice.assert_has_calls([
            mock.call(DECIDES),
            mock.call(['a']),
        ])

    @mock.patch('services.circus.circus.random.choice')
    def test_choose__two(self, mock_choice):
        mock_choice.side_effect = ['{}. Did you even need to ask?', 'a']

        actual = choose(['a', 'b'])
        expected = 'A. Did you even need to ask?'
        self.assertEqual(actual, expected)

        mock_choice.assert_has_calls([
            mock.call(DECIDES + WAFFLES),
            mock.call(['a', 'b']),
        ])

    @mock.patch('services.circus.circus.random.randint')
    def test_discuss__first(self, mock_randint):
        mock_randint.return_value = 0

        actual = discuss('the', CFD, N, 6, 10)
        expected = 'The lazy dog. Jumps over the lazy dog.'
        self.assertEqual(actual, expected)

        mock_randint.assert_has_calls([
            mock.call(0, 2),
            mock.call(0, 1),
            mock.call(0, 1),
            mock.call(0, 1),
            mock.call(0, 1),
            mock.call(0, 1),
            mock.call(0, 2),
            mock.call(0, 1),
            mock.call(0, 1),
        ])

    @mock.patch('services.circus.circus.random.randint')
    def test_discuss__last(self, mock_randint):
        def fake_randint(*args, **kwargs):
            return args[1]

        mock_randint.side_effect = fake_randint

        actual = discuss('the', CFD, N, 6, 10)
        expected = 'The quick brown fox. Jumps over the quick brown...'
        self.assertEqual(actual, expected)

        mock_randint.assert_has_calls([
            mock.call(0, 2),
            mock.call(0, 1),
            mock.call(0, 1),
            mock.call(0, 1),
            mock.call(0, 1),
            mock.call(0, 1),
            mock.call(0, 1),
            mock.call(0, 2),
            mock.call(0, 1),
        ])

    @mock.patch('services.circus.circus.random.choice')
    def test_who(self, mock_choice):
        mock_choice.side_effect = ['{}. Did you even need to ask?', 'a']

        actual = who(['a', 'b', 'c'])
        expected = 'a. Did you even need to ask?'
        self.assertEqual(actual, expected)

        mock_choice.assert_has_calls([
            mock.call(DECIDES),
            mock.call(['a', 'b', 'c']),
        ])


if __name__ == '__main__':
    unittest.main()
