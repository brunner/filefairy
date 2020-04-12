#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for shadow.py."""

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/types_/shadow', '', _path))

from types_.shadow.shadow import Shadow  # noqa


class ShadowTest(unittest.TestCase):
    def test_init__empty_destination(self):
        with self.assertRaises(ValueError):
            Shadow(key='foo.baz', info={'key': 'value'})

    def test_init__empty_key(self):
        with self.assertRaises(ValueError):
            Shadow(destination='bar', info={'key': 'value'})

    def test_init__empty_info(self):
        shadow = Shadow(destination='bar', key='foo.baz')
        self.assertEqual(shadow.destination, 'bar')
        self.assertEqual(shadow.key, 'foo.baz')
        self.assertEqual(shadow.info, None)

    def test_init__invalid_destination(self):
        with self.assertRaises(ValueError):
            Shadow(destination=[1], key='foo.baz', info={'key': 'value'})

    def test_init__invalid_key(self):
        with self.assertRaises(ValueError):
            Shadow(destination='bar', key=[1], info={'key': 'value'})

    def test_init__filled(self):
        shadow = Shadow(
            destination='bar', key='foo.baz', info={'key': 'value'})
        self.assertEqual(shadow.destination, 'bar')
        self.assertEqual(shadow.key, 'foo.baz')
        self.assertEqual(shadow.info, {'key': 'value'})


if __name__ == '__main__':
    unittest.main()
