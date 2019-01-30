#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for nltk_.py."""

import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/common/nltk_', '', _path))

from common.nltk_.nltk_ import get_cfd  # noqa
from common.nltk_.nltk_ import get_messages  # noqa
from common.nltk_.nltk_ import get_topic  # noqa
from common.nltk_.nltk_ import get_users  # noqa
from common.nltk_.nltk_ import word_tokenize  # noqa

CFD = get_cfd(2, ['The quick brown fox.', 'Jumps over the lazy dog.'])


class JsonTest(unittest.TestCase):
    def test_get_cfd(self):
        expected = {
            '.': ['Jumps'],
            'brown': ['fox'],
            'dog': ['.'],
            'fox': ['.'],
            'jumps': ['over'],
            'lazy': ['dog'],
            'over': ['the'],
            'quick': ['brown'],
            'the': ['lazy', 'quick'],
        }
        for key in expected:
            self.assertEqual(sorted(CFD[(key, )]), expected[key])

    @mock.patch('common.nltk_.nltk_.channels_list')
    @mock.patch('common.nltk_.nltk_.channels_history')
    def test_get_messages(self, mock_history, mock_list):
        message1 = {'text': 'foo\nbar\nbaz', 'user': 'U123', 'ts': '2'}
        message2 = {'text': 'a!', 'user': 'U456', 'ts': '1'}
        message3 = {'text': 'b?', 'user': 'U456', 'ts': '3'}
        mock_history.side_effect = [
            {
                'ok': True,
                'messages': [message1],
                'has_more': True,
            },
            {
                'ok': True,
                'messages': [message2],
                'has_more': False,
            },
            {
                'ok': True,
                'messages': [message3],
                'has_more': False,
            },
        ]
        channel1 = {'id': 'C123', 'ok': True}
        channel2 = {'id': 'C456', 'ok': True}
        mock_list.return_value = {
            'channels': [channel1, channel2],
            'ok': True,
        }

        actual = get_messages()
        expected = {
            'U123': ['foo.', 'bar.', 'baz.'],
            'U456': ['a!', 'b?'],
        }
        self.assertEqual(actual, expected)

        mock_history.assert_has_calls([
            mock.call('C123', '', ''),
            mock.call('C123', '2', ''),
            mock.call('C456', '', ''),
        ])
        mock_list.assert_called_once_with()

    @mock.patch('common.nltk_.nltk_.random.randint')
    def test_get_topic__first(self, mock_randint):
        mock_randint.return_value = 0

        actual = get_topic(CFD)
        expected = 'brown'
        self.assertEqual(actual, expected)

    @mock.patch('common.nltk_.nltk_.random.randint')
    def test_get_topic__last(self, mock_randint):
        def fake_randint(*args, **kwargs):
            return args[1]

        mock_randint.side_effect = fake_randint

        actual = get_topic(CFD)
        expected = 'the'
        self.assertEqual(actual, expected)

    @mock.patch('common.nltk_.nltk_.users_list')
    def test_get_users(self, mock_list):
        member1 = {
            'deleted': False,
            'id': 'U123',
            'name': 'foo',
            'profile': {
                'display_name': ''
            }
        }
        member2 = {
            'deleted': False,
            'id': 'U456',
            'name': 'bar',
            'profile': {
                'display_name': 'Bar'
            }
        }
        member3 = {
            'deleted': True,
            'id': 'U789',
            'name': 'baz',
            'profile': {
                'display_name': ''
            }
        }
        mock_list.return_value = {
            'members': [member1, member2, member3],
            'ok': True,
        }

        actual = get_users()
        expected = ['foo', 'Bar']
        self.assertEqual(actual, expected)

        mock_list.assert_called_once_with()

    def test_word_tokenize__channel(self):
        actual = word_tokenize('before <#C123|channel> after')
        expected = ['before', '<#C123|channel>', 'after']
        self.assertEqual(actual, expected)

    def test_word_tokenize__emoji(self):
        actual = word_tokenize('before :+1: after')
        expected = ['before', ':+1:', 'after']
        self.assertEqual(actual, expected)

    def test_word_tokenize__user(self):
        actual = word_tokenize('before <@U123> after')
        expected = ['before', '<@U123>', 'after']
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
