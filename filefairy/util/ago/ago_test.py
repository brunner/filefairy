#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/util/ago', '', _path))
from util.ago.ago import delta  # noqa
from util.ago.ago import elapsed  # noqa
from util.ago.ago import timestamp  # noqa
from util.datetime_.datetime_ import datetime_datetime  # noqa


class AgoTest(unittest.TestCase):
    def test_delta__seconds_ago(self):
        then = datetime_datetime(1985, 10, 26, 0, 0, 0)
        now = datetime_datetime(1985, 10, 26, 0, 0, 30)
        actual = delta(then, now)
        expected = '30s ago'
        self.assertEqual(actual, expected)

    def test_delta__minutes_ago(self):
        then = datetime_datetime(1985, 10, 26, 0, 0, 0)
        now = datetime_datetime(1985, 10, 26, 0, 2, 30)
        actual = delta(then, now)
        expected = '2m ago'
        self.assertEqual(actual, expected)

    def test_delta__hours_ago(self):
        then = datetime_datetime(1985, 10, 26, 0, 0, 0)
        now = datetime_datetime(1985, 10, 26, 6, 2, 30)
        actual = delta(then, now)
        expected = '6h ago'
        self.assertEqual(actual, expected)

    def test_delta__days_ago(self):
        then = datetime_datetime(1985, 10, 26, 0, 0, 0)
        now = datetime_datetime(1985, 10, 31, 6, 2, 30)
        actual = delta(then, now)
        expected = '5d ago'
        self.assertEqual(actual, expected)

    def test_delta__in_seconds(self):
        then = datetime_datetime(1985, 10, 26, 0, 0, 30)
        now = datetime_datetime(1985, 10, 26, 0, 0, 0)
        actual = delta(then, now)
        expected = 'in 30s'
        self.assertEqual(actual, expected)

    def test_delta__in_minutes(self):
        then = datetime_datetime(1985, 10, 26, 0, 2, 30)
        now = datetime_datetime(1985, 10, 26, 0, 0, 0)
        actual = delta(then, now)
        expected = 'in 2m'
        self.assertEqual(actual, expected)

    def test_delta__in_hours(self):
        then = datetime_datetime(1985, 10, 26, 6, 2, 30)
        now = datetime_datetime(1985, 10, 26, 0, 0, 0)
        actual = delta(then, now)
        expected = 'in 6h'
        self.assertEqual(actual, expected)

    def test_delta__in_days(self):
        then = datetime_datetime(1985, 10, 31, 6, 2, 30)
        now = datetime_datetime(1985, 10, 26, 0, 0, 0)
        actual = delta(then, now)
        expected = 'in 5d'
        self.assertEqual(actual, expected)

    def test_elapsed__seconds_ago(self):
        then = datetime_datetime(1985, 10, 26, 0, 0, 0)
        now = datetime_datetime(1985, 10, 26, 0, 0, 30)
        actual = elapsed(then, now)
        expected = '0m'
        self.assertEqual(actual, expected)

    def test_elapsed__minutes_ago(self):
        then = datetime_datetime(1985, 10, 26, 0, 0, 0)
        now = datetime_datetime(1985, 10, 26, 0, 2, 30)
        actual = elapsed(then, now)
        expected = '2m'
        self.assertEqual(actual, expected)

    def test_elapsed__hours_ago(self):
        then = datetime_datetime(1985, 10, 26, 0, 0, 0)
        now = datetime_datetime(1985, 10, 26, 6, 0, 30)
        actual = elapsed(then, now)
        expected = '6h 0m'
        self.assertEqual(actual, expected)

    def test_elapsed__days_ago(self):
        then = datetime_datetime(1985, 10, 26, 0, 0, 0)
        now = datetime_datetime(1985, 10, 31, 6, 2, 30)
        actual = elapsed(then, now)
        expected = '127h 2m'
        self.assertEqual(actual, expected)

    def test_elapsed__in_seconds(self):
        then = datetime_datetime(1985, 10, 26, 0, 0, 30)
        now = datetime_datetime(1985, 10, 26, 0, 0, 0)
        actual = elapsed(then, now)
        expected = '0m'
        self.assertEqual(actual, expected)

    def test_elapsed__in_minutes(self):
        then = datetime_datetime(1985, 10, 26, 0, 2, 30)
        now = datetime_datetime(1985, 10, 26, 0, 0, 0)
        actual = elapsed(then, now)
        expected = '2m'
        self.assertEqual(actual, expected)

    def test_elapsed__in_hours(self):
        then = datetime_datetime(1985, 10, 26, 6, 0, 30)
        now = datetime_datetime(1985, 10, 26, 0, 0, 0)
        actual = elapsed(then, now)
        expected = '6h 0m'
        self.assertEqual(actual, expected)

    def test_elapsed__in_days(self):
        then = datetime_datetime(1985, 10, 31, 6, 2, 30)
        now = datetime_datetime(1985, 10, 26, 0, 0, 0)
        actual = elapsed(then, now)
        expected = '127h 2m'
        self.assertEqual(actual, expected)

    def test_timestamp(self):
        date = datetime_datetime(1985, 10, 31, 6, 2, 30)
        actual = timestamp(date)
        expected = '06:02:30 EST (1985-10-31)'
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
