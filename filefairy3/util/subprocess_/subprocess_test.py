#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import subprocess
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/util/subprocess_', '', _path))
from util.subprocess_.subprocess_ import Command  # noqa
from util.subprocess_.subprocess_ import check_output  # noqa


class SubprocessTest(unittest.TestCase):
    @mock.patch('util.subprocess_.subprocess_.threading.Thread')
    @mock.patch.object(Command, '_target')
    @mock.patch('util.subprocess_.subprocess_.subprocess.Popen')
    def test_run__ok(self, mock_popen, mock_target, mock_thread):
        mock_proc = mock.Mock()
        mock_popen.return_value = mock_proc
        mock_t = mock.Mock()
        mock_t.is_alive.return_value = False
        mock_t.start.side_effect = mock_target
        mock_thread.return_value = mock_t

        timeout = 10
        command = Command(['cmd', 'foo', 'bar'])

        def fake_target(*args, **kwargs):
            command.output.update({'output': 'ret'})

        mock_target.side_effect = fake_target

        actual = command.run(timeout)
        expected = {'ok': True, 'output': 'ret'}
        self.assertEqual(actual, expected)

        mock_popen.assert_called_once_with(
            ['cmd', 'foo', 'bar'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        mock_proc.terminate.assert_not_called()
        mock_t.start.assert_called_once_with()
        mock_t.join.has_calls([mock.call(timeout), mock.call()])
        mock_t.is_alive.assert_called_once_with()
        mock_target.assert_called_once_with()
        mock_thread.assert_called_once_with(target=mock_target)

    @mock.patch('util.subprocess_.subprocess_.threading.Thread')
    @mock.patch.object(Command, '_target')
    @mock.patch('util.subprocess_.subprocess_.subprocess.Popen')
    def test_run__exception(self, mock_popen, mock_target, mock_thread):
        mock_proc = mock.Mock()
        mock_popen.return_value = mock_proc
        mock_t = mock.Mock()
        mock_t.is_alive.return_value = False
        mock_t.start.side_effect = mock_target
        mock_target.side_effect = Exception('Error.')
        mock_thread.return_value = mock_t

        timeout = 10
        command = Command(['cmd', 'foo', 'bar'])
        actual = command.run(timeout)
        expected = {'ok': False, 'error': 'exception', 'exception': 'Error.'}
        self.assertEqual(actual, expected)

        mock_popen.assert_called_once_with(
            ['cmd', 'foo', 'bar'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        mock_proc.terminate.assert_not_called()
        mock_target.assert_called_once_with()
        mock_t.start.assert_called_once_with()
        mock_t.join.assert_not_called()
        mock_t.is_alive.assert_not_called()
        mock_thread.assert_called_once_with(target=mock_target)

    @mock.patch('util.subprocess_.subprocess_.threading.Thread')
    @mock.patch.object(Command, '_target')
    @mock.patch('util.subprocess_.subprocess_.subprocess.Popen')
    def test_run__timeout(self, mock_popen, mock_target, mock_thread):
        mock_proc = mock.Mock()
        mock_popen.return_value = mock_proc
        mock_t = mock.Mock()
        mock_t.is_alive.return_value = True
        mock_t.start.side_effect = mock_target
        mock_thread.return_value = mock_t

        timeout = 10
        command = Command(['cmd', 'foo', 'bar'])
        actual = command.run(timeout)
        expected = {'ok': False, 'error': 'timeout'}
        self.assertEqual(actual, expected)

        mock_popen.assert_called_once_with(
            ['cmd', 'foo', 'bar'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        mock_proc.terminate.assert_called_once_with()
        mock_t.start.assert_called_once_with()
        mock_t.join.has_calls([mock.call(timeout), mock.call()])
        mock_t.is_alive.assert_called_once_with()
        mock_target.assert_called_once_with()
        mock_thread.assert_called_once_with(target=mock_target)

    @mock.patch('util.subprocess_.subprocess_.subprocess.Popen')
    def test_target(self, mock_popen):
        mock_proc = mock.Mock()
        mock_proc.communicate.return_value = ('ret', '')
        mock_popen.return_value = mock_proc

        command = Command(['cmd', 'foo', 'bar'])
        command._target()
        self.assertEqual(command.output, {'ok': True, 'output': 'ret'})

        mock_popen.assert_called_once_with(
            ['cmd', 'foo', 'bar'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        mock_proc.communicate.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
