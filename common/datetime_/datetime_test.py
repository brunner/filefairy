#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
import pytz
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/common/datetime_', '', _path))
from common.datetime_.datetime_ import datetime_as_pst  # noqa
from common.datetime_.datetime_ import datetime_datetime_est  # noqa
from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.datetime_.datetime_ import datetime_now  # noqa
from common.datetime_.datetime_ import decode_datetime  # noqa
from common.datetime_.datetime_ import encode_datetime  # noqa
from common.datetime_.datetime_ import suffix  # noqa
from common.datetime_.datetime_ import timedelta  # noqa
from common.datetime_.datetime_ import timestamp  # noqa

_est = pytz.timezone('America/New_York')
_pst = pytz.timezone('America/Los_Angeles')


class DatetimeTest(unittest.TestCase):
    def test_datetime_as_pst(self):
        d = datetime_datetime_est(2018, 3, 13)
        actual = datetime_as_pst(d)
        expected = d.astimezone(_pst)
        self.assertEqual(actual, expected)

    def test_datetime_datetime_est_minimal(self):
        actual = datetime_datetime_est(2018, 3, 13)
        expected = _est.localize(datetime.datetime(2018, 3, 13))
        self.assertEqual(actual, expected)

    def test_datetime_datetime_est_full(self):
        actual = datetime_datetime_est(2018, 3, 13, 22, 43, 13, 337756)
        expected = _est.localize(
            datetime.datetime(2018, 3, 13, 22, 43, 13, 337756))
        self.assertEqual(actual, expected)

    def test_datetime_datetime_pst_minimal(self):
        actual = datetime_datetime_pst(2018, 3, 13)
        expected = _pst.localize(datetime.datetime(2018, 3, 13))
        self.assertEqual(actual, expected)

    def test_datetime_datetime_pst_full(self):
        actual = datetime_datetime_pst(2018, 3, 13, 22, 43, 13, 337756)
        expected = _pst.localize(
            datetime.datetime(2018, 3, 13, 22, 43, 13, 337756))
        self.assertEqual(actual, expected)

    @mock.patch('common.datetime_.datetime_.datetime')
    def test_datetime_now(self, mock_datetime):
        date = datetime.datetime(2018, 3, 13, 22, 43, 13, 337756)
        mock_datetime.datetime.now.return_value = date
        actual = datetime_now()
        expected = _pst.localize(date)
        self.assertEqual(actual, expected)
        mock_datetime.datetime.now.assert_called_once_with()

    def test_decode(self):
        actual = decode_datetime('2018-03-13T22:43:13.337756-07:00')
        expected = _pst.localize(
            datetime.datetime(2018, 3, 13, 22, 43, 13, 337756))
        self.assertEqual(actual, expected)

    def test_encode(self):
        actual = encode_datetime(
            _pst.localize(datetime.datetime(2018, 3, 13, 22, 43, 13, 337756)))
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
