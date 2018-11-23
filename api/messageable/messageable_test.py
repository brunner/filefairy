#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for messageable.py."""

import logging
import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/api/messageable', '', _path))

from api.messageable.messageable import Messageable  # noqa
from data.debug.debug import Debug  # noqa
from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa
from data.thread_.thread_ import Thread  # noqa

TESTING_CHANNEL = 'G3SUFLMK4'


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
    def setUp(self):
        patch_log = mock.patch('api.messageable.messageable._logger.log')
        self.addCleanup(patch_log.stop)
        self.mock_log = patch_log.start()

    def reset_mocks(self):
        self.mock_log.reset_mock()

    def create_messageable(self):
        messageable = FakeMessageable()

        self.mock_log.assert_not_called()
        self.reset_mocks()

        return messageable

    @mock.patch.object(FakeMessageable, 'foo')
    def test_on_message__no_arguments(self, mock_foo):
        messageable = self.create_messageable()

        data = {'channel': TESTING_CHANNEL, 'text': 'FakeMessageable.foo()'}
        actual = messageable._on_message(obj=data)
        expected = Response(notify=[Notify.BASE])
        self.assertEqual(actual, expected)

        mock_foo.assert_called_once_with(obj=data, v=True)
        self.mock_log.assert_not_called()

    @mock.patch.object(FakeMessageable, 'foo')
    def test_on_message__one_argument(self, mock_foo):
        messageable = self.create_messageable()

        data = {'channel': TESTING_CHANNEL, 'text': 'FakeMessageable.foo(a)'}
        actual = messageable._on_message(obj=data)
        expected = Response(notify=[Notify.BASE])
        self.assertEqual(actual, expected)

        mock_foo.assert_called_once_with('a', obj=data, v=True)
        self.mock_log.assert_not_called()

    @mock.patch.object(FakeMessageable, 'foo')
    def test_on_message__two_arguments(self, mock_foo):
        messageable = self.create_messageable()

        data = {'channel': TESTING_CHANNEL, 'text': 'FakeMessageable.foo(a,b)'}
        actual = messageable._on_message(obj=data)
        expected = Response(notify=[Notify.BASE])
        self.assertEqual(actual, expected)

        mock_foo.assert_called_once_with('a', 'b', obj=data, v=True)
        self.mock_log.assert_not_called()

    @mock.patch.object(FakeMessageable, 'foo')
    def test_on_message__response(self, mock_foo):
        debug = Debug(msg='msg', extra={'a': 1})
        thread_ = Thread(target='_bar')
        mock_foo.return_value = Response(debug=[debug], thread_=[thread_])

        messageable = self.create_messageable()

        data = {'channel': TESTING_CHANNEL, 'text': 'FakeMessageable.foo()'}
        actual = messageable._on_message(obj=data)
        expected = Response(
            notify=[Notify.BASE], debug=[debug], thread_=[thread_])
        self.assertEqual(actual, expected)

        mock_foo.assert_called_once_with(obj=data, v=True)
        self.mock_log.assert_called_once_with(
            logging.DEBUG, 'msg', extra={'a': 1})

    @mock.patch.object(FakeMessageable, 'foo')
    def test_on_message__invalid_channel(self, mock_foo):
        messageable = self.create_messageable()

        data = {'channel': 'INVALID', 'text': 'FakeMessageable.foo()'}
        actual = messageable._on_message(obj=data)
        expected = Response()
        self.assertEqual(actual, expected)

        mock_foo.assert_not_called()
        self.mock_log.assert_not_called()

    @mock.patch.object(FakeMessageable, 'foo')
    def test_on_message__invalid_text(self, mock_foo):
        messageable = self.create_messageable()

        data = {'channel': TESTING_CHANNEL, 'text': 'Invalid.foo()'}
        actual = messageable._on_message(obj=data)
        expected = Response()
        self.assertEqual(actual, expected)

        mock_foo.assert_not_called()
        self.mock_log.assert_not_called()

    @mock.patch.object(FakeMessageable, '_bar')
    def test_on_message__private_attr(self, mock_bar):
        messageable = self.create_messageable()

        data = {'channel': TESTING_CHANNEL, 'text': 'FakeMessageable._bar()'}
        actual = messageable._on_message(obj=data)
        expected = Response()
        self.assertEqual(actual, expected)

        mock_bar.assert_not_called()
        self.mock_log.assert_not_called()

    def test_on_message__uncallable_attr(self):
        messageable = self.create_messageable()

        data = {'channel': TESTING_CHANNEL, 'text': 'FakeMessageable.var()'}
        actual = messageable._on_message(obj=data)
        expected = Response()
        self.assertEqual(actual, expected)

        self.mock_log.assert_not_called()


if __name__ == '__main__':
    unittest.main()
