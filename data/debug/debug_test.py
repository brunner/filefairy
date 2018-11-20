#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
        msg = 'foo'
        debug = Debug(msg=msg)
        self.assertEqual(debug.msg, msg)
        self.assertEqual(debug.extra, {})

    def test_init__debug_invalid_msg(self):
        extra = {'key': 'value'}
        with self.assertRaises(ValueError):
            Debug(msg=[1], extra=extra)

    def test_init__debug_valid(self):
        msg = 'foo'
        extra = {'key': 'value'}
        debug = Debug(msg=msg, extra=extra)
        self.assertEqual(debug.msg, msg)
        self.assertEqual(debug.extra, extra)


if __name__ == '__main__':
    unittest.main()
