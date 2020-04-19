#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for serializable.py."""

import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/common/io_', '', _path))

from common.io_.io_ import read_data  # noqa
from common.io_.io_ import write_data  # noqa
from common.json_.json_ import dumps  # noqa

DATA_DIR = re.sub(r'/common/io_', '', _path) + '/resources/data'


class IoTest(unittest.TestCase):
    def setUp(self):
        open_patch = mock.patch('common.io_.io_.open', create=True)
        self.addCleanup(open_patch.stop)
        self.open_ = open_patch.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.open_handle_ = mo()
        self.open_.side_effect = [mo.return_value]

    def test_read_data(self):
        data = {'a': 1}
        self.init_mocks(data)

        value = read_data('foo', 'a')
        self.assertEqual(value, 1)

        filename = os.path.join(DATA_DIR, 'foo', 'data.json')
        self.open_.assert_called_once_with(filename, 'r')
        self.open_handle_.write.assert_not_called()

    def test_write_data(self):
        data = {'a': 1}
        self.init_mocks(data)

        new = {'a': 2}
        write_data('foo', new)

        filename = os.path.join(DATA_DIR, 'foo', 'data.json')
        self.open_.assert_called_once_with(filename, 'w')
        self.open_handle_.write.assert_called_once_with(dumps(new) + '\n')


if __name__ == '__main__':
    unittest.main()
