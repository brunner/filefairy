#!/usr/bin/env python

from subprocess_util import check_output

import mock
import unittest


class UrllibUtilTest(unittest.TestCase):
    @mock.patch('subprocess_util.subprocess.check_output')
    def test_create_request(self, mock_check):
        mock_check.return_value = 'ret'
        actual = check_output(['cmd', 'foo', 'bar'])
        expected = 'ret'
        self.assertEquals(actual, expected)
        mock_check.assert_called_once_with(
            ['cmd', 'foo', 'bar'], stderr=mock.ANY)


if __name__ == '__main__':
    unittest.main()
