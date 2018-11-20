#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/data/shadow', '', _path))
from data.shadow.shadow import Shadow  # noqa


class ShadowTest(unittest.TestCase):
    def test_init__empty_destination(self):
        key = 'plugin.bar'
        data = {'key': 'value'}
        with self.assertRaises(ValueError):
            Shadow(key=key, data=data)

    def test_init__empty_key(self):
        destination = 'foo'
        data = {'key': 'value'}
        with self.assertRaises(ValueError):
            Shadow(destination=destination, data=data)

    def test_init__empty_data(self):
        destination = 'foo'
        key = 'plugin.bar'
        shadow = Shadow(destination=destination, key=key)
        self.assertEqual(shadow.destination, destination)
        self.assertEqual(shadow.key, key)
        self.assertEqual(shadow.data, None)

    def test_init__shadow_invalid_destination(self):
        key = 'plugin.bar'
        data = {'key': 'value'}
        with self.assertRaises(ValueError):
            Shadow(destination=[1], key=key, data=data)

    def test_init__shadow_invalid_key(self):
        destination = 'foo'
        data = {'key': 'value'}
        with self.assertRaises(ValueError):
            Shadow(destination=destination, key=[1], data=data)

    def test_init__shadow_valid(self):
        destination = 'foo'
        key = 'plugin.bar'
        data = {'key': 'value'}
        shadow = Shadow(destination=destination, key=key, data=data)
        self.assertEqual(shadow.destination, destination)
        self.assertEqual(shadow.key, key)
        self.assertEqual(shadow.data, data)


if __name__ == '__main__':
    unittest.main()
