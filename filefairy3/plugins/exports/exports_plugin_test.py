#!/usr/bin/env python

import mock
import os
import re
import unittest
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/plugins/exports', '', _path))
from plugins.exports.exports_plugin import ExportsPlugin  # noqa
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
    @mock.patch('plugins.exports.exports_plugin.urlopen')
    def test_run__returns(self, mock_urlopen):
        mock_urlopen.side_effect = [
            _before + _new, _before + _new, _after + _new
        ]
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
        plugin._setup()
        ret = plugin._run()
        self.assertFalse(ret)
        actual = write(_data, original)
        self.assertEqual(actual, data)
        write(_data, actual)
        ret = plugin._run()
        self.assertTrue(ret)
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

    @mock.patch('plugins.exports.exports_plugin.urlopen')
    def test_run__with_empty_new(self, mock_urlopen):
        mock_urlopen.side_effect = [_before + _new, _after + _new]
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
        plugin._setup()
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

    @mock.patch('plugins.exports.exports_plugin.urlopen')
    def test_run__with_empty_old(self, mock_urlopen):
        mock_urlopen.side_effect = [_before + _old, _after + _old]
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
        plugin._setup()
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

    @mock.patch('plugins.exports.exports_plugin.urlopen')
    def test_run__with_ai_old(self, mock_urlopen):
        mock_urlopen.side_effect = [_before + _old, _after + _old]
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
        plugin._setup()
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

    @mock.patch('plugins.exports.exports_plugin.urlopen')
    def test_run__with_form_new(self, mock_urlopen):
        mock_urlopen.side_effect = [_before + _new, _after + _new]
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
        plugin._setup()
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
