#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/utils/unicode', '', _path))
from utils.unicode.unicode_util import deunicode  # noqa


class UnicodeUtilTest(unittest.TestCase):
    def test_deunicode(self):
        actual = deunicode('Jesús')
        expected = 'Jesu?s'
        actual = deunicode('Jesús', errors='ignore')
        expected = 'Jesus'
        self.assertEqual(actual, expected)
        actual = deunicode('Jes�s')
        expected = 'Jes?s'
        self.assertEqual(actual, expected)
        actual = deunicode('Jes�s', errors='ignore')
        expected = 'Jess'
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
