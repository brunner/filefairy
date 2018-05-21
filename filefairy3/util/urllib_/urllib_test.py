#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/util/urllib_', '', _path))
from util.urllib_.urllib_ import create_request  # noqa
from util.urllib_.urllib_ import urlopen  # noqa


class UrllibTest(unittest.TestCase):
    @mock.patch('util.urllib_.urllib_.urllib.request.urlopen')
    @mock.patch('util.urllib_.urllib_.urllib.parse.urlencode')
    @mock.patch('util.urllib_.urllib_.urllib.request.Request')
    def test_create_request(self, mock_request, mock_urlencode, mock_urlopen):
        mock_request.return_value = 'request'
        mock_urlencode.return_value = 'a=1&b=2'
        actual = create_request('http://url', {'a': 1, 'b': 2})
        expected = 'request'
        self.assertEqual(actual, expected)
        mock_request.assert_called_once_with('http://url', 'a=1&b=2')
        mock_urlencode.assert_called_once_with({'a': 1, 'b': 2})

    @mock.patch('util.urllib_.urllib_.urllib.request.urlopen')
    @mock.patch('util.urllib_.urllib_.urllib.parse.urlencode')
    @mock.patch('util.urllib_.urllib_.urllib.request.Request')
    def test_urlopen(self, mock_request, mock_urlencode, mock_urlopen):
        mock_urlopen.return_value.read.return_value = 'response'
        actual = urlopen('http://url')
        expected = 'response'
        self.assertEqual(actual, expected)
        mock_urlopen.assert_called_once_with('http://url', timeout=8)


if __name__ == '__main__':
    unittest.main()
