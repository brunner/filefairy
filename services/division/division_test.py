#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for division.py."""

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/services/division', '', _path))

from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import table  # noqa
from common.teams.teams import icon_inline  # noqa
from services.division.division import condensed  # noqa


class DivisionTest(unittest.TestCase):
    def test_condensed(self):
        tables = [
            {
                'T33': '1-1',
                'T34': '2-0',
                'T48': '0-2'
            },
            {
                'T35': '1-1',
                'T38': '2-0',
                'T40': '0-2'
            },
        ]
        actual = condensed('American League', tables)
        expected = table(
            clazz='table-fixed border mt-3',
            hcols=[col(clazz='text-center', colspan=3)],
            bcols=[col(clazz='td-sm position-relative text-center w-20')] * 3,
            head=[cell(content='American League')],
            body=[
                [
                    cell(content=icon_inline('T34', '2-0')),
                    cell(content=icon_inline('T33', '1-1')),
                    cell(content=icon_inline('T48', '0-2')),
                ],
                [
                    cell(content=icon_inline('T38', '2-0')),
                    cell(content=icon_inline('T35', '1-1')),
                    cell(content=icon_inline('T40', '0-2')),
                ],
            ])
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
