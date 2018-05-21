#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/util/nltk_', '', _path))
from util.nltk_.nltk_ import _capitalize  # noqa
from util.nltk_.nltk_ import _cond_samples  # noqa
from util.nltk_.nltk_ import _fix  # noqa
from util.nltk_.nltk_ import cfd  # noqa
from util.nltk_.nltk_ import discuss  # noqa
from util.nltk_.nltk_ import imitate  # noqa


class NltkTest(unittest.TestCase):
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
        self.assertCountEqual(actual, expected)

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

    @mock.patch('util.nltk_.nltk_.open', create=True)
    def test_cfd(self, mock_open):
        data_a = 'The quick brown fox jumps over the lazy dog.'
        mo_a = mock.mock_open(read_data=data_a)
        data_b = 'The quick grey wolf jumps over the lazy fox.'
        mo_b = mock.mock_open(read_data=data_b)
        mock_open.side_effect = [mo_a.return_value, mo_b.return_value]

        fnames = ['a.txt', 'b.txt']
        c = cfd(4, *fnames)

        ngram = ('the', )
        actual = (sorted(list(c[ngram].keys())), list(c[ngram].values()))
        expected = (['lazy', 'quick'], [2, 2])
        self.assertEqual(actual, expected)

        ngram = (
            'the',
            'quick',
        )
        actual = (sorted(list(c[ngram].keys())), list(c[ngram].values()))
        expected = (['brown', 'grey'], [1, 1])
        self.assertEqual(actual, expected)

        ngram = (
            'jumps',
            'over',
            'the',
        )
        actual = (list(c[ngram].keys()), list(c[ngram].values()))
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

    @mock.patch('util.nltk_.nltk_.random.randint')
    @mock.patch('util.nltk_.nltk_.open', create=True)
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
        expected = '<#C1234|channel> jumps over the lazy dog.'
        self.assertEqual(actual, expected)

    @mock.patch('util.nltk_.nltk_.random.randint')
    @mock.patch('util.nltk_.nltk_.open', create=True)
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
        expected = ':+1: jumps over the lazy dog.'
        self.assertEqual(actual, expected)

    @mock.patch('util.nltk_.nltk_.random.randint')
    @mock.patch('util.nltk_.nltk_.open', create=True)
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
        expected = '<@U1234> jumps over the lazy dog.'
        self.assertEqual(actual, expected)

    @mock.patch('util.nltk_.nltk_.random.randint')
    @mock.patch('util.nltk_.nltk_.open', create=True)
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
        expected = 'The lazy dog. The lazy dog.'
        self.assertEqual(actual, expected)

    @mock.patch('util.nltk_.nltk_.random.randint')
    @mock.patch('util.nltk_.nltk_.open', create=True)
    def test_discuss__with_randint_middle(self, mock_open, mock_randint):
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
        expected = 'The lazy dog. The quick brown fox jumps over...'
        self.assertEqual(actual, expected)

    @mock.patch('util.nltk_.nltk_.random.randint')
    @mock.patch('util.nltk_.nltk_.open', create=True)
    def test_discuss__with_randint_last(self, mock_open, mock_randint):
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
        expected = 'The quick grey wolf jumps over the quick grey wolf...'
        self.assertEqual(actual, expected)

    @mock.patch('util.nltk_.nltk_.random.randint')
    @mock.patch('util.nltk_.nltk_.open', create=True)
    def test_imitate__with_randint_first(self, mock_open, mock_randint):
        data_a = 'The quick brown fox jumps over the lazy dog.'
        mo_a = mock.mock_open(read_data=data_a)
        data_b = 'The quick grey wolf jumps over the lazy fox.'
        mo_b = mock.mock_open(read_data=data_b)
        mock_open.side_effect = [mo_a.return_value, mo_b.return_value]
        mock_randint.return_value = 0

        fnames = ['a.txt', 'b.txt']
        c = cfd(3, *fnames)
        actual = imitate(c, 3, 5, 10)
        expected = 'Brown fox. The lazy dog.'
        self.assertEqual(actual, expected)

    @mock.patch('util.nltk_.nltk_.random.randint')
    @mock.patch('util.nltk_.nltk_.open', create=True)
    def test_imitate__with_randint_middle(self, mock_open, mock_randint):
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
        actual = imitate(c, 3, 5, 10)
        expected = 'Over the lazy dog.'
        self.assertEqual(actual, expected)

    @mock.patch('util.nltk_.nltk_.random.randint')
    @mock.patch('util.nltk_.nltk_.open', create=True)
    def test_imitate__with_randint_last(self, mock_open, mock_randint):
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
        actual = imitate(c, 3, 5, 10)
        expected = 'Wolf jumps over the quick grey wolf jumps over the...'
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
