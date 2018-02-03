#!/usr/bin/env python

from league_file_plugin import LeagueFilePlugin

import mock
import os
import re
import unittest
import sys

sys.path.append(re.sub(r'/plugins/league_file', '', os.path.dirname(__file__)))
from utils.testing.testing_util import write  # noqa

_data = LeagueFilePlugin._data()

started = """total 321012
-rwxrwxrwx 1 user user       421 Aug 19 13:48 index.html
-rwxrwxrwx 1 user user 345678901 Jan 27 12:00 orange_and_blue_league_baseball.tar.gz
-rwxrwxrwx 1 user user 310000000 Jan 29 19:26 orange_and_blue_league_baseball.tar.gz.filepart
"""

stopped = """total 321012
-rwxrwxrwx 1 user user       421 Aug 19 13:48 index.html
-rwxrwxrwx 1 user user 328706052 Jan 29 14:55 orange_and_blue_league_baseball.tar.gz
"""


class LeagueFilePluginTest(unittest.TestCase):
    @mock.patch('subprocess.check_output', return_value=started)
    def test_run__started__with_null_data(self, subprocess_check_output_mock):
        data = {'fp': None, 'up': []}
        original = write(_data, data)
        plugin = LeagueFilePlugin()
        plugin._run()
        actual = write(_data, original)
        expected = {
            'fp': {
                'size': '310000000',
                'start': 'Jan 29 19:26',
                'end': 'Jan 29 19:26'
            },
            'up': []
        }
        self.assertEqual(actual, expected)

    @mock.patch('subprocess.check_output', return_value=started)
    def test_run__started__with_filepart(self, subprocess_check_output_mock):
        data = {
            'fp': {
                'size': '300000000',
                'start': 'Jan 29 15:00',
                'end': 'Jan 29 19:23'
            },
            'up': []
        }
        original = write(_data, data)
        plugin = LeagueFilePlugin()
        plugin._run()
        actual = write(_data, original)
        expected = {
            'fp': {
                'size': '310000000',
                'start': 'Jan 29 15:00',
                'end': 'Jan 29 19:26'
            },
            'up': [],
        }
        self.assertEqual(actual, expected)

    @mock.patch('subprocess.check_output', return_value=started)
    def test_run__started__with_finished(self, subprocess_check_output_mock):
        data = {
            'fp':
            None,
            'up': [{
                'size': '345678901',
                'start': 'Jan 27 12:05',
                'end': 'Jan 27 16:00',
                'date': 'Jan 27 12:00'
            }]
        }
        original = write(_data, data)
        plugin = LeagueFilePlugin()
        plugin._run()
        actual = write(_data, original)
        expected = {
            'fp': {
                'size': '310000000',
                'start': 'Jan 29 19:26',
                'end': 'Jan 29 19:26'
            },
            'up': [{
                'size': '345678901',
                'start': 'Jan 27 12:05',
                'end': 'Jan 27 16:00',
                'date': 'Jan 27 12:00'
            }]
        }
        self.assertEqual(actual, expected)

    @mock.patch('subprocess.check_output', return_value=started)
    def test_run__started__with_filepart_and_finished(
            self, subprocess_check_output_mock):
        data = {
            'fp': {
                'size': '300000000',
                'start': 'Jan 29 15:00',
                'end': 'Jan 29 19:23'
            },
            'up': [{
                'size': '345678901',
                'start': 'Jan 27 12:05',
                'end': 'Jan 27 16:00',
                'date': 'Jan 27 12:00'
            }]
        }
        original = write(_data, data)
        plugin = LeagueFilePlugin()
        plugin._run()
        actual = write(_data, original)
        expected = {
            'fp': {
                'size': '310000000',
                'start': 'Jan 29 15:00',
                'end': 'Jan 29 19:26'
            },
            'up': [{
                'size': '345678901',
                'start': 'Jan 27 12:05',
                'end': 'Jan 27 16:00',
                'date': 'Jan 27 12:00'
            }]
        }
        self.assertEqual(actual, expected)

    @mock.patch('subprocess.check_output', return_value=stopped)
    def test_run__stopped__with_null_data(self, subprocess_check_output_mock):
        data = {'fp': None, 'up': []}
        original = write(_data, data)
        plugin = LeagueFilePlugin()
        plugin._run()
        actual = write(_data, original)
        expected = {'fp': None, 'up': []}
        self.assertEqual(actual, expected)

    @mock.patch('subprocess.check_output', return_value=stopped)
    def test_run__stopped__with_filepart(self, subprocess_check_output_mock):
        data = {
            'fp': {
                'size': '300000000',
                'start': 'Jan 29 15:00',
                'end': 'Jan 29 19:23'
            },
            'up': []
        }
        original = write(_data, data)
        plugin = LeagueFilePlugin()
        plugin._run()
        actual = write(_data, original)
        expected = {
            'fp':
            None,
            'up': [{
                'size': '328706052',
                'start': 'Jan 29 15:00',
                'end': 'Jan 29 19:23',
                'date': 'Jan 29 14:55'
            }]
        }
        self.assertEqual(actual, expected)

    @mock.patch('subprocess.check_output', return_value=stopped)
    def test_run__stopped__with_finished(self, subprocess_check_output_mock):
        data = {
            'fp':
            None,
            'up': [{
                'size': '345678901',
                'start': 'Jan 27 12:05',
                'end': 'Jan 27 16:00',
                'date': 'Jan 27 12:00'
            }]
        }
        original = write(_data, data)
        plugin = LeagueFilePlugin()
        plugin._run()
        actual = write(_data, original)
        expected = {
            'fp':
            None,
            'up': [{
                'size': '345678901',
                'start': 'Jan 27 12:05',
                'end': 'Jan 27 16:00',
                'date': 'Jan 27 12:00'
            }]
        }
        self.assertEqual(actual, expected)

    @mock.patch('subprocess.check_output', return_value=stopped)
    def test_run__stopped__with_filepart_and_finished(
            self, subprocess_check_output_mock):
        data = {
            'fp': {
                'size': '300000000',
                'start': 'Jan 29 15:00',
                'end': 'Jan 29 19:23'
            },
            'up': [{
                'size': '345678901',
                'start': 'Jan 27 12:05',
                'end': 'Jan 27 16:00',
                'date': 'Jan 27 12:00'
            }]
        }
        original = write(_data, data)
        plugin = LeagueFilePlugin()
        plugin._run()
        actual = write(_data, original)
        expected = {
            'fp':
            None,
            'up': [{
                'size': '328706052',
                'start': 'Jan 29 15:00',
                'end': 'Jan 29 19:23',
                'date': 'Jan 29 14:55'
            }, {
                'size': '345678901',
                'start': 'Jan 27 12:05',
                'end': 'Jan 27 16:00',
                'date': 'Jan 27 12:00'
            }]
        }
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
