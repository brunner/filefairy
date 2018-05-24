#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/api/messageable', '', _path))
from api.messageable.messageable import Messageable  # noqa
from core.notify.notify import Notify  # noqa
from core.response.response import Response  # noqa
from core.task.task import Task  # noqa


class FakeMessageable(Messageable):
    var = True

    def __init__(self, **kwargs):
        super(FakeMessageable, self).__init__(**kwargs)

    def _on_message_internal(self, **kwargs):
        return Response()

    def foo(self, *args, **kwargs):
        pass

    def _bar(self):
        pass


class MessageableTest(unittest.TestCase):
    @mock.patch.object(FakeMessageable, 'foo')
    def test_on_message__with_no_arguments(self, mock_foo):
        data = {'channel': 'G3SUFLMK4', 'text': 'FakeMessageable.foo()'}
        messageable = FakeMessageable()
        actual = messageable._on_message(obj=data)
        expected = Response(notify=[Notify.BASE])
        self.assertEqual(actual, expected)
        mock_foo.assert_called_once_with(obj=data, v=True)

    @mock.patch.object(FakeMessageable, 'foo')
    def test_on_message__with_one_argument(self, mock_foo):
        data = {'channel': 'G3SUFLMK4', 'text': 'FakeMessageable.foo(a)'}
        messageable = FakeMessageable()
        actual = messageable._on_message(obj=data)
        expected = Response(notify=[Notify.BASE])
        self.assertEqual(actual, expected)
        mock_foo.assert_called_once_with('a', obj=data, v=True)

    @mock.patch.object(FakeMessageable, 'foo')
    def test_on_message__with_two_arguments(self, mock_foo):
        data = {'channel': 'G3SUFLMK4', 'text': 'FakeMessageable.foo(a,b)'}
        messageable = FakeMessageable()
        actual = messageable._on_message(obj=data)
        expected = Response(notify=[Notify.BASE])
        self.assertEqual(actual, expected)
        mock_foo.assert_called_once_with('a', 'b', obj=data, v=True)

    @mock.patch.object(FakeMessageable, 'foo')
    def test_on_message__with_response(self, mock_foo):
        data = {'channel': 'G3SUFLMK4', 'text': 'FakeMessageable.foo()'}
        messageable = FakeMessageable()
        mock_foo.return_value = Response(task=[Task(target='_bar')])
        actual = messageable._on_message(obj=data)
        expected = Response(notify=[Notify.BASE], task=[Task(target='_bar')])
        self.assertEqual(actual, expected)
        mock_foo.assert_called_once_with(obj=data, v=True)

    @mock.patch.object(FakeMessageable, 'foo')
    def test_on_message__with_invalid_channel(self, mock_foo):
        data = {'channel': 'ABCDEFGH1', 'text': 'FakeMessageable.foo(a,b,c)'}
        messageable = FakeMessageable()
        actual = messageable._on_message(obj=data)
        expected = Response()
        self.assertEqual(actual, expected)
        mock_foo.assert_not_called()

    @mock.patch.object(FakeMessageable, 'foo')
    def test_on_message__with_invalid_text(self, mock_foo):
        data = {'channel': 'G3SUFLMK4', 'text': '!FakeMessageable.foo(a,b,c)'}
        messageable = FakeMessageable()
        actual = messageable._on_message(obj=data)
        expected = Response()
        self.assertEqual(actual, expected)
        mock_foo.assert_not_called()

    @mock.patch.object(FakeMessageable, '_bar')
    def test_on_message__with_invalid_private_attr(self, mock_bar):
        data = {'channel': 'G3SUFLMK4', 'text': 'FakeMessageable._bar(a,b,c)'}
        messageable = FakeMessageable()
        actual = messageable._on_message(obj=data)
        expected = Response()
        self.assertEqual(actual, expected)
        mock_bar.assert_not_called()

    def test_on_message__with_invalid_uncallable_attr(self):
        data = {'channel': 'G3SUFLMK4', 'text': 'FakeMessageable.var(a,b,c)'}
        messageable = FakeMessageable()
        actual = messageable._on_message(obj=data)
        expected = Response()
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
