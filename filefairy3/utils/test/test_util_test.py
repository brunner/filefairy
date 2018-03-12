#!/usr/bin/env python

import mock
import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/utils/test', '', _path))
from utils.test.test_util import TestUtil  # noqa


class TestUtilTest(TestUtil):
    @mock.patch('utils.test.test_util.open', create=True)
    def test_write(self, mock_open):
        data = '{"a": 1, "b": true}'
        mo = mock.mock_open(read_data=data)
        mock_open.side_effect = [mo.return_value]
        actual = self.write('data.json', {'a': 2, 'b': False})
        self.assertEquals(actual, {'a': 1, 'b': True})
        handle = mo()
        calls = [mock.call('{\n  "a": 2, \n  "b": false\n}'), mock.call('\n')]
        handle.write.assert_has_calls(calls)


if __name__ == '__main__':
    unittest.main()
