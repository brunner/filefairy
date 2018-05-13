#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc
import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/util/abc', '', _path))
from util.abc.abc_ import abstractstatic  # noqa


class Foo(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(Foo, self).__init__()

    @abstractstatic
    def _data():
        pass


class Bar(Foo):
    def __init__(self):
        super(Bar, self).__init__()

    @staticmethod
    def _data():
        return 'Bar'


class AbcTest(unittest.TestCase):
    def test_abstractstatic(self):
        self.assertEqual(Bar._data(), 'Bar')


if __name__ == '__main__':
    unittest.main()
