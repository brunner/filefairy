#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mock
import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/util/hash', '', _path))
from util.hash.hash import hash_file  # noqa


class HashTest(unittest.TestCase):
    @mock.patch('util.hash.hash.open', create=True)
    def test_hash_file(self, mock_open):
        data = 'abcdefgh12345678'
        mo = mock.mock_open(read_data=data)
        mock_open.side_effect = [mo.return_value]
        actual = hash_file('foo.txt')
        expected = '25f94a2a5c7fbaf499c665bc73d67c1c87e496da8985131633ee0a95819db2e8'
        self.assertEqual(actual, expected)
        mock_open.assert_called_once_with('foo.txt', 'rb', buffering=0)


if __name__ == '__main__':
    unittest.main()
