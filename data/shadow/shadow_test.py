#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for shadow.py."""

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/data/shadow', '', _path))

from data.shadow.shadow import Shadow  # noqa


class ShadowTest(unittest.TestCase):
    def test_init__empty_destination(self):
        with self.assertRaises(ValueError):
            Shadow(key='plugin.bar', info={'key': 'value'})

    def test_init__empty_key(self):
        with self.assertRaises(ValueError):
            Shadow(destination='foo', info={'key': 'value'})

    def test_init__empty_info(self):
        shadow = Shadow(destination='foo', key='plugin.bar')
        self.assertEqual(shadow.destination, 'foo')
        self.assertEqual(shadow.key, 'plugin.bar')
        self.assertEqual(shadow.info, None)

    def test_init__invalid_destination(self):
        with self.assertRaises(ValueError):
            Shadow(destination=[1], key='plugin.bar', info={'key': 'value'})

    def test_init__invalid_key(self):
        with self.assertRaises(ValueError):
            Shadow(destination='foo', key=[1], info={'key': 'value'})

    def test_init__filled(self):
        shadow = Shadow(
            destination='foo', key='plugin.bar', info={'key': 'value'})
        self.assertEqual(shadow.destination, 'foo')
        self.assertEqual(shadow.key, 'plugin.bar')
        self.assertEqual(shadow.info, {'key': 'value'})


if __name__ == '__main__':
    unittest.main()
