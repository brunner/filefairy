#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for record.py."""

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/common/record', '', _path))

from common.record.record import add_records  # noqa
from common.record.record import decode_record  # noqa
from common.record.record import encode_record  # noqa


class RecordTest(unittest.TestCase):
    def test_add_records(self):
        actual = add_records('71-84', '4-2')
        expected = '75-86'
        self.assertEqual(actual, expected)

    def test_decode_record(self):
        actual = decode_record('75-86')
        expected = (75, 86)
        self.assertEqual(actual, expected)

    def test_encode_record(self):
        actual = encode_record(75, 86)
        expected = '75-86'
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
