#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for abc_.py."""

import abc
import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/common/abc_', '', _path))

from common.abc_.abc_ import abstractstatic  # noqa


class Foo(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(Foo, self).__init__()

    @abstractstatic
    def _baz():
        pass


class Bar(Foo):
    def __init__(self):
        super(Bar, self).__init__()

    @staticmethod
    def _baz():
        return 'Bar'


class AbcTest(unittest.TestCase):
    def test_abstractstatic(self):
        self.assertEqual(Bar._baz(), 'Bar')


if __name__ == '__main__':
    unittest.main()
