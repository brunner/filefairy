#!/usr/bin/env python

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/apis/nameable', '', _path))
from apis.nameable.nameable_api import NameableApi  # noqa


class FakeNameable(NameableApi):
    def __init__(self, **kwargs):
        super(FakeNameable, self).__init__(**kwargs)

    def _name(self):
        return self.__class__.__name__


class NameableApiTest(unittest.TestCase):
    def test_name(self):
        nameable = FakeNameable()
        actual = nameable._name()
        expected = 'FakeNameable'
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
