#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for serializable.py."""

import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/api/serializable', '', _path))

from api.serializable.serializable import Serializable  # noqa
from common.json_.json_ import dumps  # noqa

DATA_DIR = re.sub(r'/api/serializable', '', _path) + '/resources/data'
_DATA = os.path.join(DATA_DIR, 'fakeserializable', 'data.json')


class FakeSerializable(Serializable):
    def __init__(self, **kwargs):
        super(FakeSerializable, self).__init__(**kwargs)


class SerializableTest(unittest.TestCase):
    def setUp(self):
        patch_open = mock.patch(
            'api.serializable.serializable.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]

    def reset_mocks(self):
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()

    def create_serializable(self, data):
        self.init_mocks(data)
        serializable = FakeSerializable()

        self.assertEqual(serializable.data, data)
        self.mock_open.assert_called_once_with(_DATA, 'r')
        self.mock_handle.write.assert_not_called()
        self.reset_mocks()
        self.init_mocks(data)

        return serializable

    def test_read(self):
        old = {'a': 1, 'b': True}
        serializable = self.create_serializable(old)

        new = {'a': 2, 'b': False}
        mo = mock.mock_open(read_data=dumps(new))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]

        data = serializable._read()
        self.assertEqual(new, data)

        self.mock_open.assert_called_once_with(_DATA, 'r')
        self.mock_handle.write.assert_not_called()

    def test_write(self):
        old = {'a': 1, 'b': True}
        serializable = self.create_serializable(old)

        serializable.data['a'] = 2
        serializable.data['b'] = False

        serializable._write()

        new = {'a': 2, 'b': False}
        self.mock_open.assert_called_once_with(_DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(new) + '\n')


if __name__ == '__main__':
    unittest.main()
