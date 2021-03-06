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
from common.elements.elements import media  # noqa
from common.elements.elements import menu  # noqa
from common.elements.elements import pre  # noqa
from common.elements.elements import row  # noqa
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
ROW = row(cells=[CELL])
TABLE = table(body=[ROW])

FAIRYLAB_ICON = 'https://brunnerj.com/fairylab/images/icon.png'

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
        actual = icon_img(FAIRYLAB_ICON, '16', ['absolute-icon', 'left'], '')
        expected = ('<img src="{}" width="16" height="16" border="0" class="ab'
                    'solute-icon left">').format(FAIRYLAB_ICON)
        self.assertEqual(actual, expected)

    def test_icon_span(self):
        actual = icon_span(name='menu', classes=['left', 'text-secondary'])
        expected = span(classes=[
            'oi', 'oi-menu', 'absolute-icon', 'left', 'text-secondary'
        ])
        self.assertEqual(actual, expected)

    def test_media(self):
        actual = media('576px', [])
        expected = {'is_media': True, 'min': '576px', 'rulesets': []}
        self.assertEqual(actual, expected)

    @mock.patch('common.elements.elements.sitelinks')
    def test_menu(self, mock_sitelinks):
        mock_sitelinks.return_value = [TABLE]

        current = '/fairylab/sandbox/'
        actual = menu(current)
        img = icon_img(FAIRYLAB_ICON, '16', ['absolute-icon', 'left'], '')
        span_ = span(classes=['d-block', 'px-4'], text='Fairylab')
        expected = dialog(id_='menu', icon=(img + span_), tables=[TABLE])
        self.assertEqual(actual, expected)

        mock_sitelinks.assert_called_once_with(current)

    def test_pre(self):
        actual = pre('content')
        expected = '<pre>content</pre>'
        self.assertEqual(actual, expected)

    def test_ruleset(self):
        actual = ruleset('.class', ['font-size: 16px'])
        expected = {'is_media': False, 'selector': '.class', 'rules': ['font-size: 16px']}
        self.assertEqual(actual, expected)

    def test_span(self):
        actual = span(classes=['foo', 'bar'], text='text')
        expected = '<span class="foo bar">text</span>'
        self.assertEqual(actual, expected)

    def test_sitelinks__current_home(self):
        def _content(name, href, text):
            icon = icon_span(name=name, classes=['left', 'text-secondary'])
            text = span(classes=['d-block pl-4'], text=anchor(href, text))
            return icon + text

        gameday = _content('timer', '/fairylab/gameday/', 'Gameday')
        news = _content('people', '/fairylab/news/', 'News')
        standings = _content('spreadsheet', '/fairylab/standings/',
                             'Standings')
        dashboard = _content('dashboard', '/fairylab/dashboard/', 'Dashboard')
        sandbox = _content('lightbulb', '/fairylab/sandbox/', 'Sandbox')

        actual = sitelinks('/fairylab/')
        expected = [
            topper('Site Links'),
            table(clazz='border mb-3',
                  hcols=SITELINKS_HCOLS,
                  bcols=SITELINKS_BCOLS,
                  head=[row(cells=[cell(content='Tasks')])],
                  body=[
                      row(cells=[cell(content=gameday)]),
                      row(cells=[cell(content=news)]),
                      row(cells=[cell(content=standings)]),
                  ]),
            table(clazz='border mb-3',
                  hcols=SITELINKS_HCOLS,
                  bcols=SITELINKS_BCOLS,
                  head=[row(cells=[cell(content='Other')])],
                  body=[
                      row(cells=[cell(content=dashboard)]),
                      row(cells=[cell(content=sandbox)]),
                  ])
        ]
        self.assertEqual(actual, expected)

    def test_sitelinks__current_standings(self):
        def _content(name, href, text):
            icon = icon_span(name=name, classes=['left', 'text-secondary'])
            text = span(classes=['d-block pl-4'], text=anchor(href, text))
            return icon + text

        gameday = _content('timer', '/fairylab/gameday/', 'Gameday')
        news = _content('people', '/fairylab/news/', 'News')
        dashboard = _content('dashboard', '/fairylab/dashboard/', 'Dashboard')
        home = _content('home', '/fairylab/', 'Home')
        sandbox = _content('lightbulb', '/fairylab/sandbox/', 'Sandbox')

        actual = sitelinks('/fairylab/standings/')
        expected = [
            topper('Site Links'),
            table(clazz='border mb-3',
                  hcols=SITELINKS_HCOLS,
                  bcols=SITELINKS_BCOLS,
                  head=[row(cells=[cell(content='Tasks')])],
                  body=[
                      row(cells=[cell(content=gameday)]),
                      row(cells=[cell(content=news)]),
                  ]),
            table(clazz='border mb-3',
                  hcols=SITELINKS_HCOLS,
                  bcols=SITELINKS_BCOLS,
                  head=[row(cells=[cell(content='Other')])],
                  body=[
                      row(cells=[cell(content=dashboard)]),
                      row(cells=[cell(content=home)]),
                      row(cells=[cell(content=sandbox)]),
                  ])
        ]
        self.assertEqual(actual, expected)

    def test_table__default(self):
        actual = table()
        expected = {}
        self.assertEqual(actual, expected)

    def test_table__filled(self):
        actual = table(clazz=CLAZZ,
                       id_=ID_,
                       attributes={'data-key': 'value'},
                       hcols=COLS,
                       bcols=COLS,
                       fcols=COLS,
                       head=[ROW],
                       body=[ROW],
                       foot=[ROW])
        expected = {
            'clazz': CLAZZ,
            'id': ID_,
            'attributes': ' data-key="value"',
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
            'body': [row(cells=[cell(content='text')])]
        }
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
