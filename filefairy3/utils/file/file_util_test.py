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
from utils.file.file_util import wget_file  # noqa

_download = os.path.join(_root, 'download')
_name = 'orange_and_blue_league_baseball.tar.gz'
_url = 'https://www.orangeandblueleaguebaseball.com/StatsLab/league_file/' + _name


class FileUtilTest(unittest.TestCase):
    @mock.patch('utils.file.file_util.check_output')
    def test_wget(self, mock_check):
        wget_file()
        calls = [
            mock.call(['rm', '-rf', _download]),
            mock.call(['mkdir', _download]),
            mock.call(['wget', _url]),
            mock.call(['tar', '-xzf', _name])
        ]
        mock_check.assert_has_calls(calls)


if __name__ == '__main__':
    unittest.main()
