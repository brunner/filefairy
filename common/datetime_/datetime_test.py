#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for datetime_.py."""

import datetime
import os
import pytz
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/common/datetime_', '', _path))

from common.datetime_.datetime_ import datetime_as_est  # noqa
from common.datetime_.datetime_ import datetime_as_pst  # noqa
from common.datetime_.datetime_ import datetime_datetime_est  # noqa
from common.datetime_.datetime_ import datetime_datetime_cst  # noqa
from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.datetime_.datetime_ import datetime_now  # noqa
from common.datetime_.datetime_ import datetime_replace  # noqa
from common.datetime_.datetime_ import decode_datetime  # noqa
from common.datetime_.datetime_ import encode_datetime  # noqa
from common.datetime_.datetime_ import suffix  # noqa
from common.datetime_.datetime_ import timedelta  # noqa
from common.datetime_.datetime_ import timestamp  # noqa

EST = pytz.timezone('America/New_York')
CST = pytz.timezone('America/Winnipeg')
PST = pytz.timezone('America/Los_Angeles')


class DatetimeTest(unittest.TestCase):
    def test_datetime_as_est(self):
        d = datetime_datetime_pst(2018, 3, 13)
        actual = datetime_as_est(d)
        expected = d.astimezone(EST)
        self.assertEqual(actual, expected)

    def test_datetime_as_pst(self):
        d = datetime_datetime_cst(2018, 3, 13)
        actual = datetime_as_pst(d)
        expected = d.astimezone(PST)
        self.assertEqual(actual, expected)

    def test_datetime_datetime_est_minimal(self):
        actual = datetime_datetime_est(2018, 3, 13)
        expected = EST.localize(datetime.datetime(2018, 3, 13))
        self.assertEqual(actual, expected)

    def test_datetime_datetime_est_full(self):
        actual = datetime_datetime_est(2018, 3, 13, 22, 43, 13, 337756)
        expected = EST.localize(
            datetime.datetime(2018, 3, 13, 22, 43, 13, 337756))
        self.assertEqual(actual, expected)

    def test_datetime_datetime_cst_minimal(self):
        actual = datetime_datetime_cst(2018, 3, 13)
        expected = CST.localize(datetime.datetime(2018, 3, 13))
        self.assertEqual(actual, expected)

    def tcst_datetime_datetime_cst_full(self):
        actual = datetime_datetime_cst(2018, 3, 13, 22, 43, 13, 337756)
        expected = CST.localize(
            datetime.datetime(2018, 3, 13, 22, 43, 13, 337756))
        self.assertEqual(actual, expected)

    def test_datetime_datetime_pst_minimal(self):
        actual = datetime_datetime_pst(2018, 3, 13)
        expected = PST.localize(datetime.datetime(2018, 3, 13))
        self.assertEqual(actual, expected)

    def test_datetime_datetime_pst_full(self):
        actual = datetime_datetime_pst(2018, 3, 13, 22, 43, 13, 337756)
        expected = PST.localize(
            datetime.datetime(2018, 3, 13, 22, 43, 13, 337756))
        self.assertEqual(actual, expected)

    @mock.patch('common.datetime_.datetime_.datetime')
    def test_datetime_now(self, mock_datetime):
        date = datetime.datetime(2018, 3, 13, 22, 43, 13, 337756)
        mock_datetime.datetime.now.return_value = date
        actual = datetime_now()
        expected = PST.localize(date)
        self.assertEqual(actual, expected)
        mock_datetime.datetime.now.assert_called_once_with()

    def test_datetime_replace(self):
        actual = datetime_replace('2018-03-13T22:43:00-07:00', hour=0)
        expected = '2018-03-13T00:43:00-07:00'
        self.assertEqual(actual, expected)

    def test_decode_datetime(self):
        actual = decode_datetime('2018-03-13T22:43:13.337756-07:00')
        expected = PST.localize(
            datetime.datetime(2018, 3, 13, 22, 43, 13, 337756))
        self.assertEqual(actual, expected)

    def test_encode_datetime(self):
        actual = encode_datetime(
            PST.localize(datetime.datetime(2018, 3, 13, 22, 43, 13, 337756)))
        expected = '2018-03-13T22:43:13.337756-07:00'
        self.assertEqual(actual, expected)

    def test_suffix(self):
        actual = [suffix(n) for n in range(1, 32)]
        expected = [
            'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th',
            'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'st', 'nd',
            'rd', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'st'
        ]
        self.assertEqual(actual, expected)

    def test_timedelta__seconds_ago(self):
        then = datetime_datetime_pst(1985, 10, 26, 0, 0, 0)
        now = datetime_datetime_pst(1985, 10, 26, 0, 0, 30)
        actual = timedelta(then, now)
        expected = '0m'
        self.assertEqual(actual, expected)

    def test_timedelta__minutes_ago(self):
        then = datetime_datetime_pst(1985, 10, 26, 0, 0, 0)
        now = datetime_datetime_pst(1985, 10, 26, 0, 2, 30)
        actual = timedelta(then, now)
        expected = '2m'
        self.assertEqual(actual, expected)

    def test_timedelta__hours_ago(self):
        then = datetime_datetime_pst(1985, 10, 26, 0, 0, 0)
        now = datetime_datetime_pst(1985, 10, 26, 6, 0, 30)
        actual = timedelta(then, now)
        expected = '6h 0m'
        self.assertEqual(actual, expected)

    def test_timedelta__days_ago(self):
        then = datetime_datetime_pst(1985, 10, 26, 0, 0, 0)
        now = datetime_datetime_pst(1985, 10, 31, 6, 2, 30)
        actual = timedelta(then, now)
        expected = '127h 2m'
        self.assertEqual(actual, expected)

    def test_timedelta__in_seconds(self):
        then = datetime_datetime_pst(1985, 10, 26, 0, 0, 30)
        now = datetime_datetime_pst(1985, 10, 26, 0, 0, 0)
        actual = timedelta(then, now)
        expected = '0m'
        self.assertEqual(actual, expected)

    def test_timedelta__in_minutes(self):
        then = datetime_datetime_pst(1985, 10, 26, 0, 2, 30)
        now = datetime_datetime_pst(1985, 10, 26, 0, 0, 0)
        actual = timedelta(then, now)
        expected = '2m'
        self.assertEqual(actual, expected)

    def test_timedelta__in_hours(self):
        then = datetime_datetime_pst(1985, 10, 26, 6, 0, 30)
        now = datetime_datetime_pst(1985, 10, 26, 0, 0, 0)
        actual = timedelta(then, now)
        expected = '6h 0m'
        self.assertEqual(actual, expected)

    def test_timedelta__in_days(self):
        then = datetime_datetime_pst(1985, 10, 31, 6, 2, 30)
        now = datetime_datetime_pst(1985, 10, 26, 0, 0, 0)
        actual = timedelta(then, now)
        expected = '127h 2m'
        self.assertEqual(actual, expected)

    def test_timestamp(self):
        date = datetime_datetime_pst(1985, 10, 31, 6, 2, 30)
        actual = timestamp(date)
        expected = '06:02:30 PST (1985-10-31)'
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
