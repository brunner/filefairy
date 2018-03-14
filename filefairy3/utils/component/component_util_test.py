#!/usr/bin/env python

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/utils/component', '', _path))
from utils.component.component_util import card  # noqa


class ComponentUtilTest(unittest.TestCase):
    def test_card__default(self):
        actual = card()
        expected = {
            'href': '',
            'title': '',
            'info': '',
            'table': [],
            'ts': '',
            'success': '',
            'danger': ''
        }
        self.assertEquals(actual, expected)

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
            'table': [],
            'ts': '0s ago',
            'success': 'just now',
            'danger': ''
        }
        self.assertEquals(actual, expected)

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
        self.assertEquals(actual, expected)


if __name__ == '__main__':
    unittest.main()
