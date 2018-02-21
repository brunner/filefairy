#!/usr/bin/env python

from abc_util import abstractstatic  # noqa

import abc
import unittest


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


class AbcUtilTest(unittest.TestCase):
    def test_abstractstatic(self):
        self.assertEquals(Bar._data(), 'Bar')


if __name__ == '__main__':
    unittest.main()
