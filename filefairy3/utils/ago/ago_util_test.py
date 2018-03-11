#!/usr/bin/env python

import datetime
import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/utils/ago', '', _path))
from utils.ago.ago_util import delta, elapsed  # noqa


class JsonUtilTest(unittest.TestCase):
    def test_delta__seconds_ago(self):
        then = datetime.datetime(1985, 10, 26, 0, 0, 0)
        now = datetime.datetime(1985, 10, 26, 0, 0, 30)
        actual = delta(then, now)
        expected = '30s ago'
        self.assertEquals(actual, expected)

    def test_delta__minutes_ago(self):
        then = datetime.datetime(1985, 10, 26, 0, 0, 0)
        now = datetime.datetime(1985, 10, 26, 0, 2, 30)
        actual = delta(then, now)
        expected = '2m ago'
        self.assertEquals(actual, expected)

    def test_delta__hours_ago(self):
        then = datetime.datetime(1985, 10, 26, 0, 0, 0)
        now = datetime.datetime(1985, 10, 26, 6, 2, 30)
        actual = delta(then, now)
        expected = '6h ago'
        self.assertEquals(actual, expected)

    def test_delta__days_ago(self):
        then = datetime.datetime(1985, 10, 26, 0, 0, 0)
        now = datetime.datetime(1985, 10, 31, 6, 2, 30)
        actual = delta(then, now)
        expected = '5d ago'
        self.assertEquals(actual, expected)

    def test_delta__in_seconds(self):
        then = datetime.datetime(1985, 10, 26, 0, 0, 30)
        now = datetime.datetime(1985, 10, 26, 0, 0, 0)
        actual = delta(then, now)
        expected = 'in 30s'
        self.assertEquals(actual, expected)

    def test_delta__in_minutes(self):
        then = datetime.datetime(1985, 10, 26, 0, 2, 30)
        now = datetime.datetime(1985, 10, 26, 0, 0, 0)
        actual = delta(then, now)
        expected = 'in 2m'
        self.assertEquals(actual, expected)

    def test_delta__in_hours(self):
        then = datetime.datetime(1985, 10, 26, 6, 2, 30)
        now = datetime.datetime(1985, 10, 26, 0, 0, 0)
        actual = delta(then, now)
        expected = 'in 6h'
        self.assertEquals(actual, expected)

    def test_delta__in_days(self):
        then = datetime.datetime(1985, 10, 31, 6, 2, 30)
        now = datetime.datetime(1985, 10, 26, 0, 0, 0)
        actual = delta(then, now)
        expected = 'in 5d'
        self.assertEquals(actual, expected)

    def test_elapsed__seconds_ago(self):
        then = datetime.datetime(1985, 10, 26, 0, 0, 0)
        now = datetime.datetime(1985, 10, 26, 0, 0, 30)
        actual = elapsed(then, now)
        expected = '0m'
        self.assertEquals(actual, expected)

    def test_elapsed__minutes_ago(self):
        then = datetime.datetime(1985, 10, 26, 0, 0, 0)
        now = datetime.datetime(1985, 10, 26, 0, 2, 30)
        actual = elapsed(then, now)
        expected = '2m'
        self.assertEquals(actual, expected)

    def test_elapsed__hours_ago(self):
        then = datetime.datetime(1985, 10, 26, 0, 0, 0)
        now = datetime.datetime(1985, 10, 26, 6, 2, 30)
        actual = elapsed(then, now)
        expected = '6h 2m'
        self.assertEquals(actual, expected)

    def test_elapsed__days_ago(self):
        then = datetime.datetime(1985, 10, 26, 0, 0, 0)
        now = datetime.datetime(1985, 10, 31, 6, 2, 30)
        actual = elapsed(then, now)
        expected = '126h 2m'
        self.assertEquals(actual, expected)

    def test_elapsed__in_seconds(self):
        then = datetime.datetime(1985, 10, 26, 0, 0, 30)
        now = datetime.datetime(1985, 10, 26, 0, 0, 0)
        actual = elapsed(then, now)
        expected = '0m'
        self.assertEquals(actual, expected)

    def test_elapsed__in_minutes(self):
        then = datetime.datetime(1985, 10, 26, 0, 2, 30)
        now = datetime.datetime(1985, 10, 26, 0, 0, 0)
        actual = elapsed(then, now)
        expected = '2m'
        self.assertEquals(actual, expected)

    def test_elapsed__in_hours(self):
        then = datetime.datetime(1985, 10, 26, 6, 2, 30)
        now = datetime.datetime(1985, 10, 26, 0, 0, 0)
        actual = elapsed(then, now)
        expected = '6h 2m'
        self.assertEquals(actual, expected)

    def test_elapsed__in_days(self):
        then = datetime.datetime(1985, 10, 31, 6, 2, 30)
        now = datetime.datetime(1985, 10, 26, 0, 0, 0)
        actual = elapsed(then, now)
        expected = '126h 2m'
        self.assertEquals(actual, expected)


if __name__ == '__main__':
    unittest.main()
