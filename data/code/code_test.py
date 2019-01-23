#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for code.py."""

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/data/code', '', _path))

from data.code.code import Code  # noqa


class CodeTest(unittest.TestCase):
    def test_enum(self):
        self.assertEqual(Code.BATTER, 1)
        self.assertEqual(Code.PITCHER, 2)


if __name__ == '__main__':
    unittest.main()
