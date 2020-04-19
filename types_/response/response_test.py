#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for response.py."""

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/types_/response', '', _path))

from types_.debug.debug import Debug  # noqa
from types_.notify.notify import Notify  # noqa
from types_.response.response import Response  # noqa
from types_.thread_.thread_ import Thread  # noqa

DEBUG = Debug(msg='foo')
NOTIFY = Notify.BASE
THREAD = Thread(target='foo')


class ResponseTest(unittest.TestCase):
    def test_init__empty(self):
        response = Response()
        self.assertEqual(response.debug, [])
        self.assertEqual(response.notify, [])
        self.assertEqual(response.thread_, [])

    def test_init__filled(self):
        response = Response(debug=[DEBUG], notify=[NOTIFY], thread_=[THREAD])
        self.assertEqual(response.debug, [DEBUG])
        self.assertEqual(response.notify, [NOTIFY])
        self.assertEqual(response.thread_, [THREAD])

    def test_init__invalid_debug_type(self):
        with self.assertRaises(TypeError):
            Response(debug=Debug(msg='foo'))

    def test_init__invalid_debug_element_value(self):
        with self.assertRaises(ValueError):
            Response(debug=[1])

    def test_init__invalid_notify_type(self):
        with self.assertRaises(TypeError):
            Response(notify=Notify.BASE)

    def test_init__invalid_notify_element_value(self):
        with self.assertRaises(ValueError):
            Response(notify=[1])

    def test_init__invalid_thread_type(self):
        with self.assertRaises(TypeError):
            Response(thread_=Thread(target='foo'))

    def test_init__invalid_thread_element_value(self):
        with self.assertRaises(ValueError):
            Response(thread_=[1])

    def test_append__empty(self):
        response = Response()
        response.append()
        self.assertEqual(response.debug, [])
        self.assertEqual(response.notify, [])
        self.assertEqual(response.thread_, [])

    def test_append__filled(self):
        response = Response()
        response.append(debug=DEBUG, notify=NOTIFY, thread_=THREAD)
        self.assertEqual(response.debug, [DEBUG])
        self.assertEqual(response.notify, [NOTIFY])
        self.assertEqual(response.thread_, [THREAD])

    def test_append__invalid_debug_element_value(self):
        response = Response()
        with self.assertRaises(ValueError):
            response.append(debug=1)

    def test_append__invalid_notify_element_value(self):
        response = Response()
        with self.assertRaises(ValueError):
            response.append(notify=1)

    def test_append_thread__invalid_element_value(self):
        response = Response()
        with self.assertRaises(ValueError):
            response.append(thread_=1)


if __name__ == '__main__':
    unittest.main()
