#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for dict_.py."""

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/common/dict_', '', _path))

from common.dict_.dict_ import merge  # noqa


class DictTest(unittest.TestCase):
    def test_findall__empty_multiple_group(self):
        d1 = {'foo': 1, 'bar': 2}
        d2 = {'bar': 3, 'baz': 4}
        actual = merge(d1, d2, lambda x, y: x + y, 0)
        expected = {'foo': 1, 'bar': 5, 'baz': 4}
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
