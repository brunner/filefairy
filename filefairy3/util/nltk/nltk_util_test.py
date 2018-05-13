#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mock
import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/util/nltk', '', _path))
from util.nltk.nltk_util import _capitalize  # noqa
from util.nltk.nltk_util import _cond_samples  # noqa
from util.nltk.nltk_util import _fix  # noqa
from util.nltk.nltk_util import cfd  # noqa
from util.nltk.nltk_util import discuss  # noqa


class NltkUtilTest(unittest.TestCase):
    def test_capitalize__one_match(self):
        actual = re.sub('^([a-z])', _capitalize, 'topic')
        expected = 'Topic'
        self.assertEqual(actual, expected)

    def test_capitalize__two_matches(self):
        actual = re.sub('([.?!]) ([a-z])', _capitalize, 'Foo. bar. baz.')
        expected = 'Foo. Bar. Baz.'
        self.assertEqual(actual, expected)

    def test_cond_samples(self):
        grams = [('foo', 'bar'), ('A', 'B', 'C')]
        actual = _cond_samples(grams)
        expected = iter([(('foo', ), 'bar'), ((
            'a',
            'b',
        ), 'C')])
        self.assertItemsEqual(actual, expected)

    def test_fix__channel(self):
        tokens = ['before', '<', '#', 'C1234|channel', '>', 'after']
        actual = _fix(tokens)
        expected = ['before', '<#C1234|channel>', 'after']
        self.assertEqual(actual, expected)

    def test_fix__emoji(self):
        tokens = ['before', ':+1', ':', 'middle', ':', 'v', ':', 'after']
        actual = _fix(tokens)
        expected = ['before', ':+1:', 'middle', ':v:', 'after']
        self.assertEqual(actual, expected)

    def test_fix__user(self):
        tokens = ['before', '<', '@', 'U1234', '>', 'after']
        actual = _fix(tokens)
        expected = ['before', '<@U1234>', 'after']
        self.assertEqual(actual, expected)

    @mock.patch('util.nltk.nltk_util.open', create=True)
    def test_cfd(self, mock_open):
        data_a = 'The quick brown fox jumps over the lazy dog.'
        mo_a = mock.mock_open(read_data=data_a)
        data_b = 'The quick grey wolf jumps over the lazy fox.'
        mo_b = mock.mock_open(read_data=data_b)
        mock_open.side_effect = [mo_a.return_value, mo_b.return_value]

        fnames = ['a.txt', 'b.txt']
        c = cfd(4, *fnames)

        ngram = ('the', )
        actual = (c[ngram].keys(), c[ngram].values())
        expected = (['quick', 'lazy'], [2, 2])
        self.assertEqual(actual, expected)

        ngram = (
            'the',
            'quick',
        )
        actual = (c[ngram].keys(), c[ngram].values())
        expected = (['brown', 'grey'], [1, 1])
        self.assertEqual(actual, expected)

        ngram = (
            'jumps',
            'over',
            'the',
        )
        actual = (c[ngram].keys(), c[ngram].values())
        expected = (['lazy'], [2])
        self.assertEqual(actual, expected)

        ngram = (
            'jumps',
            'over',
            'the',
            'lazy',
        )
        self.assertNotIn(ngram, c)

        calls = [mock.call('a.txt', 'r'), mock.call('b.txt', 'r')]
        mock_open.assert_has_calls(calls)

    @mock.patch('util.nltk.nltk_util.random.randint')
    @mock.patch('util.nltk.nltk_util.open', create=True)
    def test_discuss__channel(self, mock_open, mock_randint):
        data_a = 'The quick brown <#C1234|channel> jumps over the lazy dog.'
        mo_a = mock.mock_open(read_data=data_a)
        data_b = 'The quick grey wolf jumps over the lazy fox.'
        mo_b = mock.mock_open(read_data=data_b)
        mock_open.side_effect = [mo_a.return_value, mo_b.return_value]
        mock_randint.return_value = 0

        fnames = ['a.txt', 'b.txt']
        c = cfd(3, *fnames)
        actual = discuss('<#C1234|channel>', c, 3, 5, 10)
        expected = '<#C1234|channel> jumps over the quick brown ' + \
                   '<#C1234|channel> jumps over the...'
        self.assertEqual(actual, expected)

    @mock.patch('util.nltk.nltk_util.random.randint')
    @mock.patch('util.nltk.nltk_util.open', create=True)
    def test_discuss__emoji(self, mock_open, mock_randint):
        data_a = 'The quick brown :+1: jumps over the lazy dog.'
        mo_a = mock.mock_open(read_data=data_a)
        data_b = 'The quick grey wolf jumps over the lazy fox.'
        mo_b = mock.mock_open(read_data=data_b)
        mock_open.side_effect = [mo_a.return_value, mo_b.return_value]
        mock_randint.return_value = 0

        fnames = ['a.txt', 'b.txt']
        c = cfd(3, *fnames)
        actual = discuss(':+1:', c, 3, 5, 10)
        expected = ':+1: jumps over the quick brown :+1: jumps over the...'
        self.assertEqual(actual, expected)

    @mock.patch('util.nltk.nltk_util.random.randint')
    @mock.patch('util.nltk.nltk_util.open', create=True)
    def test_discuss__user(self, mock_open, mock_randint):
        data_a = 'The quick brown <@U1234> jumps over the lazy dog.'
        mo_a = mock.mock_open(read_data=data_a)
        data_b = 'The quick grey wolf jumps over the lazy fox.'
        mo_b = mock.mock_open(read_data=data_b)
        mock_open.side_effect = [mo_a.return_value, mo_b.return_value]
        mock_randint.return_value = 0

        fnames = ['a.txt', 'b.txt']
        c = cfd(3, *fnames)
        actual = discuss('<@U1234>', c, 3, 5, 10)
        expected = '<@U1234> jumps over the quick brown <@U1234> jumps ' + \
                   'over the...'
        self.assertEqual(actual, expected)

    @mock.patch('util.nltk.nltk_util.random.randint')
    @mock.patch('util.nltk.nltk_util.open', create=True)
    def test_discuss__with_randint_first(self, mock_open, mock_randint):
        data_a = 'The quick brown fox jumps over the lazy dog.'
        mo_a = mock.mock_open(read_data=data_a)
        data_b = 'The quick grey wolf jumps over the lazy fox.'
        mo_b = mock.mock_open(read_data=data_b)
        mock_open.side_effect = [mo_a.return_value, mo_b.return_value]
        mock_randint.return_value = 0

        fnames = ['a.txt', 'b.txt']
        c = cfd(3, *fnames)
        actual = discuss('the', c, 3, 5, 10)
        expected = 'The quick brown fox jumps over the quick brown fox...'
        self.assertEqual(actual, expected)

    @mock.patch('util.nltk.nltk_util.random.randint')
    @mock.patch('util.nltk.nltk_util.open', create=True)
    def test_discuss__with_randint_middle(self, mock_open, mock_randint):
        data_a = 'The quick brown fox jumps over the lazy dog.'
        mo_a = mock.mock_open(read_data=data_a)
        data_b = 'The quick grey wolf jumps over the lazy fox.'
        mo_b = mock.mock_open(read_data=data_b)
        mock_open.side_effect = [mo_a.return_value, mo_b.return_value]

        def fake_randint(*args, **kwargs):
            return args[1]

        mock_randint.side_effect = fake_randint

        fnames = ['a.txt', 'b.txt']
        c = cfd(3, *fnames)
        actual = discuss('the', c, 3, 5, 10)
        expected = 'The lazy dog. The lazy dog.'
        self.assertEqual(actual, expected)

    @mock.patch('util.nltk.nltk_util.random.randint')
    @mock.patch('util.nltk.nltk_util.open', create=True)
    def test_discuss__with_randint_last(self, mock_open, mock_randint):
        data_a = 'The quick brown fox jumps over the lazy dog.'
        mo_a = mock.mock_open(read_data=data_a)
        data_b = 'The quick grey wolf jumps over the lazy fox.'
        mo_b = mock.mock_open(read_data=data_b)
        mock_open.side_effect = [mo_a.return_value, mo_b.return_value]

        def fake_randint(*args, **kwargs):
            return args[1] / 2

        mock_randint.side_effect = fake_randint

        fnames = ['a.txt', 'b.txt']
        c = cfd(3, *fnames)
        actual = discuss('the', c, 3, 5, 10)
        expected = 'The quick brown fox jumps over the lazy fox.'
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
