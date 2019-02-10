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
from common.elements.elements import icon_img  # noqa
from common.elements.elements import icon_span  # noqa
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

FAVICON_LINK = 'https://fairylab.surge.sh/favicon-32x32.png'

SITELINKS_HCOLS = [col(clazz='font-weight-bold text-dark')]
SITELINKS_BCOLS = [col(clazz='position-relative')]


class ElemementsTest(unittest.TestCase):
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

    def test_icon_img(self):
        actual = icon_img(FAVICON_LINK, '16', ['absolute-icon', 'left'])
        expected = ('<img src="{}" width="16" height="16" border="0" class="ab'
                    'solute-icon left">').format(FAVICON_LINK)
        self.assertEqual(actual, expected)

    def test_icon_span(self):
        actual = icon_span('menu', ['left', 'text-secondary'])
        expected = span(
            ['oi', 'oi-menu', 'absolute-icon', 'left', 'text-secondary'], '')
        self.assertEqual(actual, expected)

    @mock.patch('common.elements.elements.sitelinks')
    def test_menu(self, mock_sitelinks):
        mock_sitelinks.return_value = [TABLE]

        actual = menu()
        img = icon_img(FAVICON_LINK, '16', ['absolute-icon', 'left'])
        span_ = span(['d-block', 'px-4'], 'Fairylab')
        expected = dialog(id_='menu', icon=(img + span_), tables=[TABLE])
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
        def _content(name, href, text):
            text = span(['d-block pl-4'], anchor(href, text))
            return icon_span(name, ['left', 'text-secondary']) + text

        gameday = _content('timer', '/gameday/', 'Gameday')
        news = _content('people', '/news/', 'News')
        standings = _content('spreadsheet', '/standings/', 'Standings')
        dashboard = _content('dashboard', '/dashboard/', 'Dashboard')

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
        def _content(name, href, text):
            text = span(['d-block pl-4'], anchor(href, text))
            return icon_span(name, ['left', 'text-secondary']) + text

        gameday = _content('timer', '/gameday/', 'Gameday')
        news = _content('people', '/news/', 'News')
        standings = _content('spreadsheet', '/standings/', 'Standings')
        dashboard = _content('dashboard', '/dashboard/', 'Dashboard')
        home = _content('home', '/', 'Home')

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
