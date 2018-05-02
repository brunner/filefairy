#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mock
import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/utils/file', '', _path)
sys.path.append(_root)
from utils.file.file_util import recreate  # noqa
from utils.file.file_util import wget_file  # noqa

_download = os.path.join(_root, 'download')
_host = 'www.orangeandblueleaguebaseball.com'
_name = 'orange_and_blue_league_baseball.tar.gz'
_url = 'https://' + _host + '/StatsLab/league_file/' + _name

OK = {'ok': True}
TIMEOUT = {'ok': False, 'error': 'timeout'}


class FileUtilTest(unittest.TestCase):
    @mock.patch('utils.file.file_util.check_output')
    def test_recreate(self, mock_check):
        recreate(_download)
        calls = [
            mock.call(['rm', '-rf', _download]),
            mock.call(['mkdir', _download])
        ]
        mock_check.assert_has_calls(calls)

    @mock.patch('utils.file.file_util.check_output')
    def test_wget_file__ok(self, mock_check):
        mock_check.side_effect = [OK] * 5

        output = wget_file()
        self.assertEqual(output, OK)

        calls = [
            mock.call(['ping', '-c', '1', _host], timeout=2),
            mock.call(['rm', '-rf', _download]),
            mock.call(['mkdir', _download]),
            mock.call(['wget', _url]),
            mock.call(['tar', '-xzf', _name])
        ]
        mock_check.assert_has_calls(calls)

    @mock.patch('utils.file.file_util.check_output')
    def test_wget_file__timeout(self, mock_check):
        mock_check.side_effect = [TIMEOUT]

        output = wget_file()
        self.assertEqual(output, TIMEOUT)

        mock_check.assert_called_once_with(
            ['ping', '-c', '1', _host], timeout=2)


if __name__ == '__main__':
    unittest.main()
