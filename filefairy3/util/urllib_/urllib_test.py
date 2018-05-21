#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest
import unittest.mock as mock
import urllib.parse as parse

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/util/urllib_', '', _path))
from util.urllib_.urllib_ import urlopen  # noqa


class UrllibTest(unittest.TestCase):
    @mock.patch('util.urllib_.urllib_.request.urlopen')
    def test_urlopen(self, mock_urlopen):
        mock_urlopen.return_value.__enter__.return_value.read.return_value = bytes('response', 'utf-8')

        data = {'a': 1, 'b': 2}
        actual = urlopen('http://url', data)
        expected = 'response'
        self.assertEqual(actual, expected)

        encoded_data = parse.urlencode(data).encode('utf-8')
        mock_urlopen.assert_called_once_with(
            'http://url', data=encoded_data, timeout=8)


if __name__ == '__main__':
    unittest.main()
