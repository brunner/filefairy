#!/usr/bin/env python

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/apis/messageable', '', _path))
from apis.messageable.messageable_api import MessageableApi  # noqa


class FakeMessageable(MessageableApi):
    var = True

    def __init__(self, **kwargs):
        super(FakeMessageable, self).__init__(**kwargs)

    def _on_message_internal(self, **kwargs):
        return dict(kwargs, m='internal')

    def foo(self, **kwargs):
        return dict(kwargs, m='foo')

    def _bar(self, **kwargs):
        return dict(kwargs, m='bar')


class MessageableApiTest(unittest.TestCase):
    def test_on_message__with_no_arguments(self):
        data = {'channel': 'G3SUFLMK4', 'text': 'FakeMessageable.foo()'}
        messageable = FakeMessageable()
        actual = messageable._on_message(obj=data)
        expected = {'m': 'foo', 'obj': data, 'a1': '', 'v': True}
        self.assertEqual(actual, expected)

    def test_on_message__with_one_argument(self):
        data = {'channel': 'G3SUFLMK4', 'text': 'FakeMessageable.foo(a)'}
        messageable = FakeMessageable()
        actual = messageable._on_message(obj=data)
        expected = {'m': 'foo', 'obj': data, 'a1': 'a', 'v': True}
        self.assertEqual(actual, expected)

    def test_on_message__with_two_arguments(self):
        data = {'channel': 'G3SUFLMK4', 'text': 'FakeMessageable.foo(a,b)'}
        messageable = FakeMessageable()
        actual = messageable._on_message(obj=data)
        expected = {'m': 'foo', 'obj': data, 'a1': 'a', 'a2': 'b', 'v': True}
        self.assertEqual(actual, expected)

    def test_on_message__with_invalid_channel(self):
        data = {'channel': 'ABCDEFGH1', 'text': 'FakeMessageable.foo(a,b,c)'}
        messageable = FakeMessageable()
        actual = messageable._on_message(obj=data)
        expected = {'m': 'internal', 'obj': data}
        self.assertEqual(actual, expected)

    def test_on_message__with_invalid_text(self):
        data = {'channel': 'G3SUFLMK4', 'text': '!FakeMessageable.foo(a,b,c)'}
        messageable = FakeMessageable()
        actual = messageable._on_message(obj=data)
        expected = {'m': 'internal', 'obj': data}
        self.assertEqual(actual, expected)

    def test_on_message__with_invalid_private_attr(self):
        data = {'channel': 'G3SUFLMK4', 'text': 'FakeMessageable._bar(a,b,c)'}
        messageable = FakeMessageable()
        actual = messageable._on_message(obj=data)
        expected = {'m': 'internal', 'obj': data}
        self.assertEqual(actual, expected)

    def test_on_message__with_invalid_uncallable_attr(self):
        data = {'channel': 'G3SUFLMK4', 'text': 'FakeMessageable.var(a,b,c)'}
        messageable = FakeMessageable()
        actual = messageable._on_message(obj=data)
        expected = {'m': 'internal', 'obj': data}
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
