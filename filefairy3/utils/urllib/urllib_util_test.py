#!/usr/bin/env python

from urllib_util import create_request, urlopen

import mock
import unittest


class UrllibUtilTest(unittest.TestCase):
    @mock.patch('urllib_util.urllib2.urlopen')
    @mock.patch('urllib_util.urllib.urlencode')
    @mock.patch('urllib_util.urllib2.Request')
    def test_create_request(self, mock_request, mock_urlencode, mock_urlopen):
        mock_request.return_value = 'request'
        mock_urlencode.return_value = 'a=1&b=2'
        actual = create_request('http://url', {'a': 1, 'b': 2})
        expected = 'request'
        self.assertEquals(actual, expected)
        mock_request.assert_called_once_with('http://url', 'a=1&b=2')
        mock_urlencode.assert_called_once_with({'a': 1, 'b': 2})

    @mock.patch('urllib_util.urllib2.urlopen')
    @mock.patch('urllib_util.urllib.urlencode')
    @mock.patch('urllib_util.urllib2.Request')
    def test_urlopen(self, mock_request, mock_urlencode, mock_urlopen):
        mock_urlopen.return_value.read.return_value = 'response'
        actual = urlopen('http://url')
        expected = 'response'
        self.assertEquals(actual, expected)
        mock_urlopen.assert_called_once_with('http://url')


if __name__ == '__main__':
    unittest.main()
