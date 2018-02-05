#!/usr/bin/env python

from exports_plugin import ExportsPlugin

import mock
import os
import re
import unittest
import sys

sys.path.append(re.sub(r'/plugins/exports', '', os.path.dirname(__file__)))
from utils.testing.testing_util import write  # noqa

_data = ExportsPlugin._data()

_after = """
<tr class="title"><td>League File Updated: Sunday February 4, 2018 20:42:30 EST</td></tr>
"""

_before = """
<tr class="title"><td>League File Updated: Friday February 2, 2018 19:53:16 EST</td></tr>
"""

_new = """
<td width="262px" valign="top">
<a href="https://www.orangeandblueleaguebaseball.com/StatsLab/reports/news/html/teams/team_31.html">
Arizona Diamondbacks</a><br>
<span style="color:#339933;">Saturday February 3, 2018 23:50:22 EST
<br>New Export</span></td>
<td width="262px" valign="top">
<a href="https://www.orangeandblueleaguebaseball.com/StatsLab/reports/news/html/teams/team_32.html">
Atlanta Braves</a><br>
<span style="color:#AA3333;">Monday January 29, 2018 17:34:19 EST
<br>Old Export</span></td>
"""

_old = """
<td width="262px" valign="top">
<a href="https://www.orangeandblueleaguebaseball.com/StatsLab/reports/news/html/teams/team_31.html">
Arizona Diamondbacks</a><br>
<span style="color:#AA3333;">Thursday February 1, 2018 08:03:23 EST
<br>Old Export</span></td>
<td width="262px" valign="top">
<a href="https://www.orangeandblueleaguebaseball.com/StatsLab/reports/news/html/teams/team_32.html">
Atlanta Braves</a><br>
<span style="color:#AA3333;">Monday January 29, 2018 17:34:19 EST
<br>Old Export</span></td>
"""


class ExportsPluginTest(unittest.TestCase):
    @mock.patch('urllib2.urlopen')
    def test_run__new__with_empty_data(self, urllib2_urlopen_mock):
        m = mock.Mock()
        m.read.side_effect = [_before + _new, _after + _new]
        urllib2_urlopen_mock.return_value = m

        data = {
            '31': {
                'ai': False,
                'form': [],
                'new': 0,
                'old': 0
            },
            '32': {
                'ai': False,
                'form': [],
                'new': 0,
                'old': 0
            }
        }
        original = write(_data, data)
        plugin = ExportsPlugin()
        plugin._run()
        actual = write(_data, original)
        expected = {
            '31': {
                'ai': False,
                'form': ['new'],
                'new': 1,
                'old': 0
            },
            '32': {
                'ai': False,
                'form': ['old'],
                'new': 0,
                'old': 1
            }
        }
        self.assertEqual(actual, expected)

    @mock.patch('urllib2.urlopen')
    def test_run__old__with_empty_data(self, urllib2_urlopen_mock):
        m = mock.Mock()
        m.read.side_effect = [_before + _old, _after + _old]
        urllib2_urlopen_mock.return_value = m

        data = {
            '31': {
                'ai': False,
                'form': [],
                'new': 0,
                'old': 0
            },
            '32': {
                'ai': False,
                'form': [],
                'new': 0,
                'old': 0
            }
        }
        original = write(_data, data)
        plugin = ExportsPlugin()
        plugin._run()
        actual = write(_data, original)
        expected = {
            '31': {
                'ai': False,
                'form': ['old'],
                'new': 0,
                'old': 1
            },
            '32': {
                'ai': False,
                'form': ['old'],
                'new': 0,
                'old': 1
            }
        }
        self.assertEqual(actual, expected)

    @mock.patch('urllib2.urlopen')
    def test_run__old__with_ai_true(self, urllib2_urlopen_mock):
        m = mock.Mock()
        m.read.side_effect = [_before + _old, _after + _old]
        urllib2_urlopen_mock.return_value = m

        data = {
            '31': {
                'ai': True,
                'form': [],
                'new': 0,
                'old': 0
            },
            '32': {
                'ai': False,
                'form': [],
                'new': 0,
                'old': 0
            }
        }
        original = write(_data, data)
        plugin = ExportsPlugin()
        plugin._run()
        actual = write(_data, original)
        expected = {
            '31': {
                'ai': True,
                'form': [],
                'new': 0,
                'old': 0
            },
            '32': {
                'ai': False,
                'form': ['old'],
                'new': 0,
                'old': 1
            }
        }
        self.assertEqual(actual, expected)

    @mock.patch('urllib2.urlopen')
    def test_run__new__with_long_form(self, urllib2_urlopen_mock):
        m = mock.Mock()
        m.read.side_effect = [_before + _new, _after + _new]
        urllib2_urlopen_mock.return_value = m

        data = {
            '31': {
                'ai':
                False,
                'form': [
                    'new', 'new', 'new', 'new', 'old', 'new', 'new', 'old',
                    'new', 'new', 'old', 'new', 'old', 'old', 'new', 'new',
                    'old', 'new', 'new', 'new'
                ],
                'new':
                14,
                'old':
                6
            },
            '32': {
                'ai': False,
                'form': [],
                'new': 0,
                'old': 0
            }
        }
        original = write(_data, data)
        plugin = ExportsPlugin()
        plugin._run()
        actual = write(_data, original)
        expected = {
            '31': {
                'ai':
                False,
                'form': [
                    'new', 'new', 'new', 'old', 'new', 'new', 'old', 'new',
                    'new', 'old', 'new', 'old', 'old', 'new', 'new', 'old',
                    'new', 'new', 'new', 'new'
                ],
                'new':
                15,
                'old':
                6
            },
            '32': {
                'ai': False,
                'form': ['old'],
                'new': 0,
                'old': 1
            }
        }
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
