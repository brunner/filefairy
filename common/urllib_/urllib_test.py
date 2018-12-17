#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import re
import sys
import unittest
import unittest.mock as mock
import urllib.parse as parse

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/common/urllib_', '', _path))
from common.urllib_.urllib_ import urlopen  # noqa


class UrllibTest(unittest.TestCase):
    @mock.patch('common.urllib_.urllib_.request.urlopen')
    @mock.patch('common.urllib_.urllib_._logger.log')
    def test_urlopen__exception(self, mock_log, mock_urlopen):
        e = Exception()
        mock_urlopen.return_value.__enter__.return_value.read.side_effect = e

        data = {'a': 1, 'b': 2}
        actual = urlopen('http://url', data)
        self.assertEqual(actual, b'')

        mock_log.assert_called_once_with(
            logging.WARNING, 'Handled warning.', exc_info=True)
        encoded_data = parse.urlencode(data).encode('utf-8')
        mock_urlopen.assert_called_once_with(
            'http://url', data=encoded_data, timeout=10)

    @mock.patch('common.urllib_.urllib_.request.urlopen')
    @mock.patch('common.urllib_.urllib_._logger.log')
    def test_urlopen__ok(self, mock_log, mock_urlopen):
        r = bytes('response', 'utf-8')
        mock_urlopen.return_value.__enter__.return_value.read.return_value = r

        data = {'a': 1, 'b': 2}
        actual = urlopen('http://url', data)
        self.assertEqual(actual, r)

        mock_log.assert_not_called()
        encoded_data = parse.urlencode(data).encode('utf-8')
        mock_urlopen.assert_called_once_with(
            'http://url', data=encoded_data, timeout=10)


if __name__ == '__main__':
    unittest.main()
