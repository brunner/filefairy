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


def _data(a, b):
    return {'a': a, 'b': b}


class DataSerializable(Serializable):
    def __init__(self, **kwargs):
        super(DataSerializable, self).__init__(**kwargs)

    @staticmethod
    def _data():
        return 'data.json'


class NoneSerializable(Serializable):
    def __init__(self, **kwargs):
        super(NoneSerializable, self).__init__(**kwargs)

    @staticmethod
    def _data():
        return None


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

    def create_data_serializable(self, data):
        self.init_mocks(data)
        serializable = DataSerializable()

        self.assertEqual(serializable.data, data)
        self.mock_open.assert_called_once_with(DataSerializable._data(), 'r')
        self.mock_handle.write.assert_not_called()
        self.reset_mocks()
        self.init_mocks(data)

        return serializable

    def create_none_serializable(self):
        self.init_mocks({})
        serializable = NoneSerializable()

        self.assertEqual(serializable.data, {})
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.reset_mocks()
        self.init_mocks({})

        return serializable

    def test_read__data(self):
        old = _data(1, True)
        serializable = self.create_data_serializable(old)

        new = _data(2, False)
        mo = mock.mock_open(read_data=dumps(new))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]

        serializable.read()
        self.assertEqual(serializable.data, new)

        self.mock_open.assert_called_once_with(DataSerializable._data(), 'r')
        self.mock_handle.write.assert_not_called()

    def test_read__none(self):
        serializable = self.create_none_serializable()
        serializable.read()
        self.assertEqual(serializable.data, {})

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    def test_write__data(self):
        old = _data(1, True)
        serializable = self.create_data_serializable(old)

        serializable.data['a'] = 2
        serializable.data['b'] = False

        serializable.write()
        new = _data(2, False)
        self.assertEqual(serializable.data, new)

        self.mock_open.assert_called_once_with(DataSerializable._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(new) + '\n')

    def test_write__none(self):
        serializable = self.create_none_serializable()
        serializable.write()
        self.assertEqual(serializable.data, {})

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()


if __name__ == '__main__':
    unittest.main()
