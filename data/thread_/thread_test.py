#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for thread_.py."""

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/data/thread_', '', _path))

from data.thread_.thread_ import Thread  # noqa


class ThreadTest(unittest.TestCase):
    def test_init__empty_target(self):
        with self.assertRaises(ValueError):
            Thread()

    def test_init__empty_args(self):
        kwargs = {'key': 'value'}
        thread = Thread(target='foo', kwargs=kwargs)
        self.assertEqual(thread.target, 'foo')
        self.assertEqual(thread.args, tuple())
        self.assertEqual(thread.kwargs, kwargs)

    def test_init__empty_kwargs(self):
        args = (True, False)
        thread = Thread(target='foo', args=args)
        self.assertEqual(thread.target, 'foo')
        self.assertEqual(thread.args, args)
        self.assertEqual(thread.kwargs, dict())

    def test_init__filled(self):
        args = (True, False)
        kwargs = {'key': 'value'}
        thread = Thread(target='foo', args=args, kwargs=kwargs)
        self.assertEqual(thread.target, 'foo')
        self.assertEqual(thread.args, args)
        self.assertEqual(thread.kwargs, kwargs)

    def test_init__invalid_target(self):
        args = (True, False)
        kwargs = {'key': 'value'}
        with self.assertRaises(ValueError):
            Thread(target=[1], args=args, kwargs=kwargs)

    def test_init__invalid_args(self):
        kwargs = {'key': 'value'}
        with self.assertRaises(ValueError):
            Thread(target='foo', args=[1], kwargs=kwargs)

    def test_init__invalid_kwargs(self):
        args = (True, False)
        with self.assertRaises(ValueError):
            Thread(target='foo', args=args, kwargs=[1])


if __name__ == '__main__':
    unittest.main()
