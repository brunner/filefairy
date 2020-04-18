#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for nameable.py."""

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/api/nameable', '', _path))

from api.nameable.nameable import Nameable  # noqa


class FakeNameable(Nameable):
    def __init__(self, **kwargs):
        super(FakeNameable, self).__init__(**kwargs)


class NameableTest(unittest.TestCase):
    def test_name(self):
        nameable = FakeNameable()

        actual = nameable._name()
        expected = 'fakenameable'
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
