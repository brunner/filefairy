#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for subprocess_.py."""

import logging
import os
import re
import subprocess
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/common/subprocess_', '', _path))

from common.subprocess_.subprocess_ import check_output  # noqa


class SubprocessTest(unittest.TestCase):
    def setUp(self):
        patch_log = mock.patch('common.subprocess_.subprocess_._logger.log')
        self.addCleanup(patch_log.stop)
        self.mock_log = patch_log.start()

    @mock.patch('common.subprocess_.subprocess_.subprocess.run')
    def test_run__with_valid_input(self, mock_run):
        cmd = ['cmd', 'foo', 'bar']
        t = 10
        mock_run.return_value = subprocess.CompletedProcess(
            args=cmd, returncode=0, stdout=b'out', stderr=b'err')

        actual = check_output(cmd, timeout=t)
        expected = {'ok': True, 'stdout': 'out', 'stderr': 'err'}
        self.assertEqual(actual, expected)

        mock_run.assert_called_once_with(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=t,
            check=True)
        self.mock_log.assert_not_called()

    @mock.patch('common.subprocess_.subprocess_.subprocess.run')
    def test_run__with_thrown_exception(self, mock_run):
        cmd = ['cmd', 'foo', 'bar']
        t = 10
        mock_run.side_effect = subprocess.TimeoutExpired(cmd, t)

        actual = check_output(cmd, timeout=t)
        e = 'Command \'{0}\' timed out after {1} seconds'.format(cmd, t)
        expected = {'ok': False, 'stdout': e, 'stderr': e}
        self.assertEqual(actual, expected)

        mock_run.assert_called_once_with(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=t,
            check=True)
        self.mock_log.assert_called_once_with(
            logging.WARNING, 'Handled warning.', exc_info=True)


if __name__ == '__main__':
    unittest.main()
