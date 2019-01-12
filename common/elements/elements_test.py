#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for elements.py."""

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/common/elements', '', _path))

from common.elements.elements import anchor  # noqa
from common.elements.elements import card  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import dialog  # noqa
from common.elements.elements import span  # noqa
from common.elements.elements import table  # noqa

CLAZZ = 'clazz'
COL = col(clazz=CLAZZ, colspan='2')
CELL = cell(col=COL, content='content')
COLS = [COL]
ID_ = 'id'
ROW = [CELL]
TABLE = table(body=[ROW])


class ComponentTest(unittest.TestCase):
    def test_anchor(self):
        actual = anchor('http://url', 'content')
        expected = '<a href="http://url">content</a>'
        self.assertEqual(actual, expected)

    def test_card__empty(self):
        actual = card()
        expected = {
            'href': '',
            'title': '',
            'info': '',
            'code': '',
            'table': None,
            'ts': '',
            'success': '',
            'danger': ''
        }
        self.assertEqual(actual, expected)

    def test_card__filled(self):
        actual = card(
            href='/foo/',
            title='foo',
            info='Description of foo.',
            code='exc',
            table=TABLE,
            ts='06:02:30 EDT (1985-10-26)',
            success='yes',
            danger='no')
        expected = {
            'href': '/foo/',
            'title': 'foo',
            'info': 'Description of foo.',
            'code': 'exc',
            'table': TABLE,
            'ts': '06:02:30 EDT (1985-10-26)',
            'success': 'yes',
            'danger': 'no'
        }
        self.assertEqual(actual, expected)

    def test_cell__empty(self):
        actual = cell()
        expected = {'col': None, 'content': ''}
        self.assertEqual(actual, expected)

    def test_cell__filled(self):
        actual = cell(col=COL, content='foo')
        expected = {'col': COL, 'content': 'foo'}
        self.assertEqual(actual, expected)

    def test_col__empty(self):
        actual = col()
        expected = {'clazz': '', 'colspan': ''}
        self.assertEqual(actual, expected)

    def test_col__filled(self):
        actual = col(clazz='foo', colspan='2')
        expected = {'clazz': 'foo', 'colspan': '2'}
        self.assertEqual(actual, expected)

    def test_dialog__default(self):
        actual = dialog()
        expected = {'id': '', 'header': '', 'tables': []}
        self.assertEqual(actual, expected)

    def test_dialog__filled(self):
        actual = dialog(id_=ID_, header='foo', tables=[TABLE])
        expected = {'id': ID_, 'header': 'foo', 'tables': [TABLE]}
        self.assertEqual(actual, expected)

    def test_span(self):
        actual = span(['foo', 'bar'], 'text')
        expected = '<span class="foo bar">text</span>'
        self.assertEqual(actual, expected)

    def test_table__default(self):
        actual = table()
        expected = {
            'clazz': 'border mt-3',
            'id': '',
            'hcols': None,
            'bcols': None,
            'fcols': None,
            'head': None,
            'body': None,
            'foot': None
        }
        self.assertEqual(actual, expected)

    def test_table__filled(self):
        actual = table(
            clazz=CLAZZ,
            id_=ID_,
            hcols=COLS,
            bcols=COLS,
            fcols=COLS,
            head=ROW,
            body=[ROW],
            foot=ROW)
        expected = {
            'clazz': CLAZZ,
            'id': ID_,
            'hcols': COLS,
            'bcols': COLS,
            'fcols': COLS,
            'head': ROW,
            'body': [ROW],
            'foot': ROW
        }
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
