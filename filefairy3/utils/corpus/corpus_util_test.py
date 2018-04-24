#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mock
import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/utils/corpus', '', _path))
from utils.corpus.corpus_util import _rewrite  # noqa
from utils.corpus.corpus_util import collect  # noqa

_members = {'U1234': 'user'}
_messages = [
    {
        'user': 'U1234',
        'text': 'foo\nbar\nbaz',
        'type': 'message',
        'ts': '4'
    },
    {
        'user': 'U5678',
        'text': 'abc!',
        'type': 'message',
        'ts': '3'
    },
    {
        'user': 'U9090',
        'text': '<U9090> has joined the channel',
        'type': 'message',
        'subtype': 'channel_join',
        'ts': '2'
    },
    {
        'user': 'U1234',
        'text': 'reply',
        'type': 'message',
        'subtype': 'thread_broadcast',
        'ts': '1'
    },
]


class CorpusUtilTest(unittest.TestCase):
    def test_rewrite__with_http_url(self):
        actual = _rewrite('foo: <http://foo>', _members)
        expected = 'foo:'
        self.assertEqual(actual, expected)

    def test_rewrite__with_https_url(self):
        actual = _rewrite('foo: <https://foo>', _members)
        expected = 'foo:'
        self.assertEqual(actual, expected)

    def test_rewrite__with_announcement(self):
        actual = _rewrite('<!channel> foo', _members)
        expected = 'foo'
        self.assertEqual(actual, expected)

    def test_rewrite__with_parens(self):
        actual = _rewrite('foo (bar) baz', _members)
        expected = 'foo bar baz'
        self.assertEqual(actual, expected)

    def test_rewrite__with_unicode(self):
        actual = _rewrite('(╯°□°）╯︵ ┻━┻ foo', _members)
        expected = 'foo'
        self.assertEqual(actual, expected)

    def test_rewrite__with_escaped_html(self):
        actual = _rewrite('&gt; foo', _members)
        expected = '> foo'
        self.assertEqual(actual, expected)

    @mock.patch('utils.corpus.corpus_util.channels_history')
    def test_collect(self, mock_history):
        mock_history.side_effect = [{
            'ok': True,
            'messages': _messages[:2]
        }, {
            'ok': True,
            'messages': _messages[2:]
        }, {
            'ok': True,
            'messages': []
        }]

        actual = collect('C1234', _members)
        expected = 'reply.\nabc!\nfoo.\nbar.\nbaz.'
        self.assertEqual(actual, expected)

        calls = [
            mock.call('C1234', ''),
            mock.call('C1234', '3'),
            mock.call('C1234', '1')
        ]
        mock_history.assert_has_calls(calls)


if __name__ == '__main__':
    unittest.main()
