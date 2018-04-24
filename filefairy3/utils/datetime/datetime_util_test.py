#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/utils/datetime', '', _path))
from utils.datetime.datetime_util import decode_datetime  # noqa
from utils.datetime.datetime_util import encode_datetime  # noqa
from utils.datetime.datetime_util import suffix  # noqa


class DatetimeUtilTest(unittest.TestCase):
    def test_decode(self):
        actual = decode_datetime('2018-03-13T22:43:13.337756')
        expected = datetime.datetime(2018, 3, 13, 22, 43, 13, 337756)
        self.assertEqual(actual, expected)

    def test_encode(self):
        actual = encode_datetime(
            datetime.datetime(2018, 3, 13, 22, 43, 13, 337756))
        expected = '2018-03-13T22:43:13.337756'
        self.assertEqual(actual, expected)

    def test_suffix(self):
        actual = [suffix(n) for n in range(1, 32)]
        expected = [
            'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th',
            'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'st', 'nd',
            'rd', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'st'
        ]
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
