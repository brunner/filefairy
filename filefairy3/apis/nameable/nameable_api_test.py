#!/usr/bin/env python

from nameable_api import NameableApi

import unittest


class FakeNameable(NameableApi):
    def __init__(self):
        super(FakeNameable, self).__init__()

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
