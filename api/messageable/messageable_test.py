#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/api/messageable', '', _path))
from api.messageable.messageable import Messageable  # noqa
from core.debug.debug import Debug  # noqa
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
    @mock.patch('plugin.git.git.logger_.log')
    @mock.patch.object(FakeMessageable, 'foo')
    def test_on_message__with_no_arguments(self, mock_foo, mock_log):
        data = {'channel': 'G3SUFLMK4', 'text': 'FakeMessageable.foo()'}
        messageable = FakeMessageable()
        actual = messageable._on_message(obj=data)
        expected = Response(notify=[Notify.BASE])
        self.assertEqual(actual, expected)
        mock_foo.assert_called_once_with(obj=data, v=True)
        mock_log.assert_not_called()

    @mock.patch('plugin.git.git.logger_.log')
    @mock.patch.object(FakeMessageable, 'foo')
    def test_on_message__with_one_argument(self, mock_foo, mock_log):
        data = {'channel': 'G3SUFLMK4', 'text': 'FakeMessageable.foo(a)'}
        messageable = FakeMessageable()
        actual = messageable._on_message(obj=data)
        expected = Response(notify=[Notify.BASE])
        self.assertEqual(actual, expected)
        mock_foo.assert_called_once_with('a', obj=data, v=True)
        mock_log.assert_not_called()

    @mock.patch('plugin.git.git.logger_.log')
    @mock.patch.object(FakeMessageable, 'foo')
    def test_on_message__with_two_arguments(self, mock_foo, mock_log):
        data = {'channel': 'G3SUFLMK4', 'text': 'FakeMessageable.foo(a,b)'}
        messageable = FakeMessageable()
        actual = messageable._on_message(obj=data)
        expected = Response(notify=[Notify.BASE])
        self.assertEqual(actual, expected)
        mock_foo.assert_called_once_with('a', 'b', obj=data, v=True)
        mock_log.assert_not_called()

    @mock.patch('plugin.git.git.logger_.log')
    @mock.patch.object(FakeMessageable, 'foo')
    def test_on_message__with_response(self, mock_foo, mock_log):
        data = {'channel': 'G3SUFLMK4', 'text': 'FakeMessageable.foo()'}
        messageable = FakeMessageable()
        debug = Debug(msg='msg', extra={'a': 1})
        task = Task(target='_bar')
        mock_foo.return_value = Response(debug=[debug], task=[task])
        actual = messageable._on_message(obj=data)
        expected = Response(notify=[Notify.BASE], debug=[debug], task=[task])
        self.assertEqual(actual, expected)
        mock_foo.assert_called_once_with(obj=data, v=True)
        mock_log.assert_called_once_with(logging.DEBUG, 'msg', extra={'a': 1})

    @mock.patch('plugin.git.git.logger_.log')
    @mock.patch.object(FakeMessageable, 'foo')
    def test_on_message__with_invalid_channel(self, mock_foo, mock_log):
        data = {'channel': 'ABCDEFGH1', 'text': 'FakeMessageable.foo(a,b,c)'}
        messageable = FakeMessageable()
        actual = messageable._on_message(obj=data)
        expected = Response()
        self.assertEqual(actual, expected)
        mock_foo.assert_not_called()
        mock_log.assert_not_called()

    @mock.patch('plugin.git.git.logger_.log')
    @mock.patch.object(FakeMessageable, 'foo')
    def test_on_message__with_invalid_text(self, mock_foo, mock_log):
        data = {'channel': 'G3SUFLMK4', 'text': '!FakeMessageable.foo(a,b,c)'}
        messageable = FakeMessageable()
        actual = messageable._on_message(obj=data)
        expected = Response()
        self.assertEqual(actual, expected)
        mock_foo.assert_not_called()
        mock_log.assert_not_called()

    @mock.patch('plugin.git.git.logger_.log')
    @mock.patch.object(FakeMessageable, '_bar')
    def test_on_message__with_invalid_private_attr(self, mock_bar, mock_log):
        data = {'channel': 'G3SUFLMK4', 'text': 'FakeMessageable._bar(a,b,c)'}
        messageable = FakeMessageable()
        actual = messageable._on_message(obj=data)
        expected = Response()
        self.assertEqual(actual, expected)
        mock_bar.assert_not_called()
        mock_log.assert_not_called()

    @mock.patch('plugin.git.git.logger_.log')
    def test_on_message__with_invalid_uncallable_attr(self, mock_log):
        data = {'channel': 'G3SUFLMK4', 'text': 'FakeMessageable.var(a,b,c)'}
        messageable = FakeMessageable()
        actual = messageable._on_message(obj=data)
        expected = Response()
        self.assertEqual(actual, expected)
        mock_log.assert_not_called()


if __name__ == '__main__':
    unittest.main()
