#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

    @staticmethod
    def _info():
        return 'Description.'

    def _name(self):
        return self.__class__.__name__


class NameableTest(unittest.TestCase):
    def test_info(self):
        nameable = FakeNameable()
        actual = nameable._info()
        expected = 'Description.'
        self.assertEqual(actual, expected)

    def test_name(self):
        nameable = FakeNameable()
        actual = nameable._name()
        expected = 'FakeNameable'
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()