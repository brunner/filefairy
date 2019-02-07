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
from common.elements.elements import pre  # noqa
from common.elements.elements import ruleset  # noqa
from common.elements.elements import span  # noqa
from common.elements.elements import table  # noqa
from common.elements.elements import topper  # noqa

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

    def test_card__default(self):
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

    def test_cell__default(self):
        actual = cell()
        expected = {}
        self.assertEqual(actual, expected)

    def test_cell__filled(self):
        actual = cell(col=COL, content='foo')
        expected = {'col': COL, 'content': 'foo'}
        self.assertEqual(actual, expected)

    def test_col__default(self):
        actual = col()
        expected = {}
        self.assertEqual(actual, expected)

    def test_col__filled(self):
        actual = col(clazz='foo', colspan='2')
        expected = {'clazz': 'foo', 'colspan': '2'}
        self.assertEqual(actual, expected)

    def test_dialog__default(self):
        actual = dialog()
        expected = {}
        self.assertEqual(actual, expected)

    def test_dialog__filled(self):
        actual = dialog(id_=ID_, icon='foo', tables=[TABLE])
        expected = {'id': ID_, 'icon': 'foo', 'tables': [TABLE]}
        self.assertEqual(actual, expected)

    def test_pre(self):
        actual = pre('content')
        expected = '<pre>content</pre>'
        self.assertEqual(actual, expected)

    def test_ruleset__default(self):
        actual = ruleset()
        expected = {}
        self.assertEqual(actual, expected)

    def test_ruleset__filled(self):
        actual = ruleset(selector='.class', rules=['font-size: 16px'])
        expected = {'selector': '.class', 'rules': ['font-size: 16px']}
        self.assertEqual(actual, expected)

    def test_span(self):
        actual = span(['foo', 'bar'], 'text')
        expected = '<span class="foo bar">text</span>'
        self.assertEqual(actual, expected)

    def test_table__default(self):
        actual = table()
        expected = {}
        self.assertEqual(actual, expected)

    def test_table__filled(self):
        actual = table(
            clazz=CLAZZ,
            id_=ID_,
            hcols=COLS,
            bcols=COLS,
            fcols=COLS,
            head=[ROW],
            body=[ROW],
            foot=[ROW])
        expected = {
            'clazz': CLAZZ,
            'id': ID_,
            'hcols': COLS,
            'bcols': COLS,
            'fcols': COLS,
            'head': [ROW],
            'body': [ROW],
            'foot': [ROW]
        }
        self.assertEqual(actual, expected)

    def test_topper(self):
        actual = topper('text')
        bc = 'border-0 font-weight-bold px-0 text-secondary'
        expected = {
            'clazz': 'topper',
            'bcols': [col(clazz=bc)],
            'body': [[cell(content='text')]]
        }
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
