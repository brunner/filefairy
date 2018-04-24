#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mock
import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/utils/urllib', '', _path))
from utils.urllib.urllib_util import create_request  # noqa
from utils.urllib.urllib_util import urlopen  # noqa


class UrllibUtilTest(unittest.TestCase):
    @mock.patch('utils.urllib.urllib_util.urllib2.urlopen')
    @mock.patch('utils.urllib.urllib_util.urllib.urlencode')
    @mock.patch('utils.urllib.urllib_util.urllib2.Request')
    def test_create_request(self, mock_request, mock_urlencode, mock_urlopen):
        mock_request.return_value = 'request'
        mock_urlencode.return_value = 'a=1&b=2'
        actual = create_request('http://url', {'a': 1, 'b': 2})
        expected = 'request'
        self.assertEqual(actual, expected)
        mock_request.assert_called_once_with('http://url', 'a=1&b=2')
        mock_urlencode.assert_called_once_with({'a': 1, 'b': 2})

    @mock.patch('utils.urllib.urllib_util.urllib2.urlopen')
    @mock.patch('utils.urllib.urllib_util.urllib.urlencode')
    @mock.patch('utils.urllib.urllib_util.urllib2.Request')
    def test_urlopen(self, mock_request, mock_urlencode, mock_urlopen):
        mock_urlopen.return_value.read.return_value = 'response'
        actual = urlopen('http://url')
        expected = 'response'
        self.assertEqual(actual, expected)
        mock_urlopen.assert_called_once_with('http://url')


if __name__ == '__main__':
    unittest.main()
