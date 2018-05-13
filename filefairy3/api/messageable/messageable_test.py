#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/api/messageable', '', _path))
from api.messageable.messageable import Messageable  # noqa
from value.notify.notify import Notify  # noqa
from value.response.response import Response  # noqa


class FakeMessageable(Messageable):
    var = True

    def __init__(self, **kwargs):
        super(FakeMessageable, self).__init__(**kwargs)

    def _on_message_internal(self, **kwargs):
        return Response()

    def foo(self, **kwargs):
        pass

    def _bar(self, **kwargs):
        pass


class MessageableTest(unittest.TestCase):
    def test_on_message__with_no_arguments(self):
        data = {'channel': 'G3SUFLMK4', 'text': 'FakeMessageable.foo()'}
        messageable = FakeMessageable()
        actual = messageable._on_message(obj=data)
        expected = Response(notify=[Notify.BASE])
        self.assertEqual(actual, expected)

    def test_on_message__with_one_argument(self):
        data = {'channel': 'G3SUFLMK4', 'text': 'FakeMessageable.foo(a)'}
        messageable = FakeMessageable()
        actual = messageable._on_message(obj=data)
        expected = Response(notify=[Notify.BASE])
        self.assertEqual(actual, expected)

    def test_on_message__with_two_arguments(self):
        data = {'channel': 'G3SUFLMK4', 'text': 'FakeMessageable.foo(a,b)'}
        messageable = FakeMessageable()
        actual = messageable._on_message(obj=data)
        expected = Response(notify=[Notify.BASE])
        self.assertEqual(actual, expected)

    def test_on_message__with_invalid_channel(self):
        data = {'channel': 'ABCDEFGH1', 'text': 'FakeMessageable.foo(a,b,c)'}
        messageable = FakeMessageable()
        actual = messageable._on_message(obj=data)
        expected = Response()
        self.assertEqual(actual, expected)

    def test_on_message__with_invalid_text(self):
        data = {'channel': 'G3SUFLMK4', 'text': '!FakeMessageable.foo(a,b,c)'}
        messageable = FakeMessageable()
        actual = messageable._on_message(obj=data)
        expected = Response()
        self.assertEqual(actual, expected)

    def test_on_message__with_invalid_private_attr(self):
        data = {'channel': 'G3SUFLMK4', 'text': 'FakeMessageable._bar(a,b,c)'}
        messageable = FakeMessageable()
        actual = messageable._on_message(obj=data)
        expected = Response()
        self.assertEqual(actual, expected)

    def test_on_message__with_invalid_uncallable_attr(self):
        data = {'channel': 'G3SUFLMK4', 'text': 'FakeMessageable.var(a,b,c)'}
        messageable = FakeMessageable()
        actual = messageable._on_message(obj=data)
        expected = Response()
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
