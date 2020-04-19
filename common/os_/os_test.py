#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for os_.py."""

import logging
import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/common/os_', '', _path))

from common.os_.os_ import chdir  # noqa
from common.os_.os_ import listdirs  # noqa

CWD = os.getcwd()


class OsTest(unittest.TestCase):
    def setUp(self):
        patch_log = mock.patch('common.os_.os_._logger.log')
        self.addCleanup(patch_log.stop)
        self.mock_log = patch_log.start()

    @mock.patch('common.os_.os_.os')
    def test_chdir__cwd(self, mock_os):
        mock_os.chdir = os.chdir
        mock_os.getcwd.side_effect = Exception()

        self.assertEqual(os.getcwd(), CWD)

        with chdir('/'):
            self.assertEqual(os.getcwd(), '/')

        self.assertEqual(os.getcwd(), CWD)
        self.mock_log.assert_called_once_with(logging.WARNING,
                                              'Handled warning.',
                                              exc_info=True)

    @mock.patch('common.os_.os_.os')
    def test_chdir__inner(self, mock_os):
        mock_os.chdir = os.chdir
        mock_os.getcwd.return_value = CWD

        self.assertEqual(os.getcwd(), CWD)

        with chdir('/'):
            self.assertEqual(os.getcwd(), '/')
            raise Exception()

        self.assertEqual(os.getcwd(), CWD)
        self.mock_log.assert_called_once_with(logging.WARNING,
                                              'Handled warning.',
                                              exc_info=True)

    @mock.patch('common.os_.os_.os')
    def test_chdir__ok(self, mock_os):
        mock_os.chdir = os.chdir
        mock_os.getcwd.return_value = CWD

        self.assertEqual(os.getcwd(), CWD)

        with chdir('/'):
            self.assertEqual(os.getcwd(), '/')

        self.assertEqual(os.getcwd(), CWD)
        self.mock_log.assert_not_called()

    @mock.patch('common.os_.os_.os.listdir')
    @mock.patch('common.os_.os_.os.path.isdir')
    def test_listdirs(self, mock_isdir, mock_listdir):
        dirs = ['__init__.py', '__pycache__', 'foo', 'bar']
        mock_isdir.side_effect = [False, True, True, True]
        mock_listdir.return_value = dirs

        actual = listdirs(CWD)
        expected = ['bar', 'foo']
        self.assertEqual(actual, expected)

        mock_isdir.assert_has_calls(
            [mock.call(os.path.join(CWD, d)) for d in dirs])
        mock_listdir.assert_called_once_with(CWD)
        self.mock_log.assert_not_called()


if __name__ == '__main__':
    unittest.main()
