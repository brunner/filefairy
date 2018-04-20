#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/utils/component', '', _path))
from utils.component.component_util import card, table  # noqa


class ComponentUtilTest(unittest.TestCase):
    def test_card__default(self):
        actual = card()
        expected = {
            'href': '',
            'title': '',
            'info': '',
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
            'table': table,
            'ts': '4m ago',
            'success': '',
            'danger': 'stalled'
        }
        self.assertEqual(actual, expected)

    def test_table__default(self):
        actual = table()
        expected = {
            'clazz': 'border mt-3',
            'hcols': None,
            'bcols': None,
            'head': None,
            'body': None
        }
        self.assertEqual(actual, expected)

    def test_table__leaguefile(self):
        actual = table(
            clazz='table-sm',
            hcols=['', '', ''],
            bcols=['', '', ''],
            head=['Date', 'Time', 'Size'],
            body=[['Jan 1', '5h 0m', '300,000,000']])
        expected = {
            'clazz': 'table-sm',
            'hcols': ['', '', ''],
            'bcols': ['', '', ''],
            'head': ['Date', 'Time', 'Size'],
            'body': [['Jan 1', '5h 0m', '300,000,000']]
        }
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
