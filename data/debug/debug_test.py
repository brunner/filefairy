#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for debug.py."""

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/data/debug', '', _path))

from data.debug.debug import Debug  # noqa


class DebugTest(unittest.TestCase):
    def test_init__empty_msg(self):
        extra = {'key': 'value'}
        with self.assertRaises(ValueError):
            Debug(extra=extra)

    def test_init__empty_extra(self):
        debug = Debug(msg='foo')
        self.assertEqual(debug.msg, 'foo')
        self.assertEqual(debug.extra, {})

    def test_init__filled(self):
        extra = {'key': 'value'}
        debug = Debug(msg='foo', extra=extra)
        self.assertEqual(debug.msg, 'foo')
        self.assertEqual(debug.extra, extra)

    def test_init__invalid_msg(self):
        with self.assertRaises(ValueError):
            Debug(msg=1)

    def test_init__invalid_extra(self):
        with self.assertRaises(ValueError):
            Debug(extra=1)


if __name__ == '__main__':
    unittest.main()
