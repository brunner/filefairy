#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mock
import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/utils/subprocess', '', _path))
from utils.subprocess.subprocess_util import check_output  # noqa


class UrllibUtilTest(unittest.TestCase):
    @mock.patch('utils.subprocess.subprocess_util.subprocess.check_output')
    def test_create_request(self, mock_check):
        mock_check.return_value = 'ret'
        actual = check_output(['cmd', 'foo', 'bar'])
        expected = 'ret'
        self.assertEqual(actual, expected)
        mock_check.assert_called_once_with(
            ['cmd', 'foo', 'bar'], stderr=mock.ANY)


if __name__ == '__main__':
    unittest.main()
