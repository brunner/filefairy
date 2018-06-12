#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/util/file_', '', _path)
sys.path.append(_root)
from util.file_.file_ import ping  # noqa
from util.file_.file_ import recreate  # noqa
from util.file_.file_ import wget_file  # noqa

_download = os.path.join(_root, 'resource/download')
_host = 'www.orangeandblueleaguebaseball.com'
_name = 'orange_and_blue_league_baseball.tar.gz'
_url = 'https://' + _host + '/StatsLab/league_file/' + _name


class FileTest(unittest.TestCase):
    @mock.patch('util.file_.file_.check_output')
    def test_ping(self, mock_check):
        ok = {'ok': True}
        mock_check.return_value = ok

        output = ping()
        self.assertEqual(output, ok)

        mock_check.assert_called_once_with(
            ['ping', '-c', '1', _host], timeout=8)

    @mock.patch('util.file_.file_.check_output')
    def test_recreate(self, mock_check):
        ok = {'ok': True}
        mock_check.return_value = ok

        recreate(_download)

        calls = [
            mock.call(['rm', '-rf', _download]),
            mock.call(['mkdir', _download])
        ]
        mock_check.assert_has_calls(calls)

    @mock.patch('util.file_.file_.check_output')
    def test_wget(self, mock_check):
        ok = {'ok': True}
        mock_check.return_value = ok

        wget_file()

        calls = [
            mock.call(['rm', '-rf', _download]),
            mock.call(['mkdir', _download]),
            mock.call(['wget', _url], timeout=7200),
            mock.call(['tar', '-xzf', _name])
        ]
        mock_check.assert_has_calls(calls)


if __name__ == '__main__':
    unittest.main()
