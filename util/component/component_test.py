#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/util/component', '', _path))
from util.component.component import anchor  # noqa
from util.component.component import card  # noqa
from util.component.component import profile  # noqa
from util.component.component import replace  # noqa
from util.component.component import show  # noqa
from util.component.component import span  # noqa
from util.component.component import table  # noqa


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

    def test_card__home(self):
        actual = card(
            href='/fairylab/foo/',
            title='foo',
            info='Description of foo.',
            ts='0s ago',
            success='just now')
        expected = {
            'href': '/fairylab/foo/',
            'title': 'foo',
            'info': 'Description of foo.',
            'code': '',
            'table': None,
            'ts': '0s ago',
            'success': 'just now',
            'danger': ''
        }
        self.assertEqual(actual, expected)

    def test_card__leaguefile(self):
        table = [{
            'key': 'Time',
            'value': '6m'
        }, {
            'key': 'Size',
            'value': '800,000'
        }]
        actual = card(
            title='Jan 1', table=table, ts='4m ago', danger='stalled')
        expected = {
            'href': '',
            'title': 'Jan 1',
            'info': '',
            'code': '',
            'table': table,
            'ts': '4m ago',
            'success': '',
            'danger': 'stalled'
        }
        self.assertEqual(actual, expected)

    def test_profile__default(self):
        actual = profile('1', ('#000000', '#acacac', '#ffffff', ''))
        expected = '<svg viewBox="0,0,48,48">' + \
                   '<style>.text { font: bold 24px sans-serif; }</style>' + \
                   '<rect x="0" y="0" width="48" height="48" ' + \
                   'fill="#6c757d" rx="8" ry="8"></rect>' + \
                   '<rect x="1" y="1" width="46" height="46" ' + \
                   'fill="#000000" rx="7" ry="7"></rect>' + \
                   '<rect x="4" y="4" width="40" height="40" ' + \
                   'fill="#ffffff" rx="5" ry="5"></rect>' + \
                   '<rect x="6" y="6" width="36" height="36" ' + \
                   'fill="#acacac" rx="4" ry="4"></rect>' + \
                   '<text x="50%" y="32" text-anchor="middle" ' + \
                   'fill="#000000" class="text">1</text>' + \
                   '</svg>'
        self.assertEqual(actual, expected)

    def test_replace__default(self):
        actual = replace('text', 'replace')
        expected = '<a class="repl-toggler" href="#" role="button" ' + \
                   'data-repl="replace">text</a>'
        self.assertEqual(actual, expected)

    def test_show__default(self):
        actual = show('trigger', 'text')
        expected = '<a data-toggle="collapse" href="#trigger" ' + \
                   'role="button" aria-expanded="false" ' + \
                   'aria-controls="trigger">text</a>'
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

    def test_table__leaguefile(self):
        actual = table(
            clazz='table-sm',
            head=['Date', 'Time', 'Size'],
            body=[['Jan 1', '5h 0m', '300,000,000']])
        expected = {
            'clazz': 'table-sm',
            'id': '',
            'hcols': None,
            'bcols': None,
            'fcols': None,
            'head': ['Date', 'Time', 'Size'],
            'body': [['Jan 1', '5h 0m', '300,000,000']],
            'foot': None
        }
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
