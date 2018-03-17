#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/utils/unicode', '', _path))
from utils.unicode.unicode_util import strip_accents  # noqa


class UnicodeUtilTest(unittest.TestCase):
    def test_strip_accents(self):
        actual = strip_accents('Jesús')
        expected = 'Jesu?s'
        self.assertEqual(actual, expected)
        actual = strip_accents('Jes�s')
        expected = 'Jes?s'
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
