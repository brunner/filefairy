#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for elements.py."""

import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/common/elements', '', _path))

from common.elements.elements import anchor  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import dialog  # noqa
from common.elements.elements import icon  # noqa
from common.elements.elements import menu  # noqa
from common.elements.elements import pre  # noqa
from common.elements.elements import ruleset  # noqa
from common.elements.elements import sitelinks  # noqa
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

SITELINKS_HCOLS = [col(clazz='font-weight-bold text-dark')]
SITELINKS_BCOLS = [col(clazz='position-relative')]


class ComponentTest(unittest.TestCase):
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

    def test_anchor(self):
        actual = anchor('http://url', 'content')
        expected = '<a href="http://url">content</a>'
        self.assertEqual(actual, expected)

    def test_dialog__default(self):
        actual = dialog()
        expected = {}
        self.assertEqual(actual, expected)

    def test_dialog__filled(self):
        actual = dialog(id_=ID_, icon='foo', tables=[TABLE])
        expected = {'id': ID_, 'icon': 'foo', 'tables': [TABLE]}
        self.assertEqual(actual, expected)

    def test_icon(self):
        actual = icon('menu')
        expected = span(
            ['oi', 'oi-menu', 'absolute-icon', 'left', 'text-secondary'], '')
        self.assertEqual(actual, expected)

    @mock.patch('common.elements.elements.sitelinks')
    def test_menu(self, mock_sitelinks):
        mock_sitelinks.return_value = [TABLE]

        actual = menu()
        icon_ = icon('menu') + span(['d-block', 'pl-4'], 'Menu')
        expected = dialog(id_='menu', icon=icon_, tables=[TABLE])
        self.assertEqual(actual, expected)

        mock_sitelinks.assert_called_once_with(home=True)

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

    def test_sitelinks__home_false(self):
        def _span(href, text):
            return span(['d-block pl-4'], anchor(href, text))

        gameday = icon('timer') + _span('/gameday/', 'Gameday')
        news = icon('people') + _span('/news/', 'News')
        standings = icon('spreadsheet') + _span('/standings/', 'Standings')
        dashboard = icon('dashboard') + _span('/dashboard/', 'Dashboard')
        home = icon('home') + _span('/', 'Home')

        actual = sitelinks()
        expected = [
            topper('Site Links'),
            table(
                clazz='border mb-3',
                hcols=SITELINKS_HCOLS,
                bcols=SITELINKS_BCOLS,
                head=[[cell(content='Tasks')]],
                body=[
                    [cell(content=gameday)],
                    [cell(content=news)],
                    [cell(content=standings)],
                ]),
            table(
                clazz='border mb-3',
                hcols=SITELINKS_HCOLS,
                bcols=SITELINKS_BCOLS,
                head=[[cell(content='Other')]],
                body=[
                    [cell(content=dashboard)],
                ])
        ]
        self.assertEqual(actual, expected)

    def test_sitelinks__home_true(self):
        def _span(href, text):
            return span(['d-block pl-4'], anchor(href, text))

        gameday = icon('timer') + _span('/gameday/', 'Gameday')
        news = icon('people') + _span('/news/', 'News')
        standings = icon('spreadsheet') + _span('/standings/', 'Standings')
        dashboard = icon('dashboard') + _span('/dashboard/', 'Dashboard')
        home = icon('home') + _span('/', 'Home')

        actual = sitelinks(home=True)
        expected = [
            topper('Site Links'),
            table(
                clazz='border mb-3',
                hcols=SITELINKS_HCOLS,
                bcols=SITELINKS_BCOLS,
                head=[[cell(content='Tasks')]],
                body=[
                    [cell(content=gameday)],
                    [cell(content=news)],
                    [cell(content=standings)],
                ]),
            table(
                clazz='border mb-3',
                hcols=SITELINKS_HCOLS,
                bcols=SITELINKS_BCOLS,
                head=[[cell(content='Other')]],
                body=[
                    [cell(content=dashboard)],
                    [cell(content=home)],
                ])
        ]
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
