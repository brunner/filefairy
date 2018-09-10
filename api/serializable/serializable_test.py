#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/api/serializable', '', _path))
from api.serializable.serializable import Serializable  # noqa


class FakeSerializable(Serializable):
    def __init__(self, **kwargs):
        super(FakeSerializable, self).__init__(**kwargs)

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')


class SerializableTest(unittest.TestCase):
    @mock.patch('api.serializable.serializable.logger_.log')
    @mock.patch('api.serializable.serializable.open', create=True)
    def test_init(self, mock_open, mock_log):
        data = '{"a": 1, "b": true}'
        mo = mock.mock_open(read_data=data)
        mock_open.side_effect = [mo.return_value]
        serializable = FakeSerializable()
        mock_open.assert_called_once_with(FakeSerializable._data(), 'r')
        mock_log.assert_not_called()
        self.assertEqual(serializable.data, {'a': 1, 'b': True})

    @mock.patch('api.serializable.serializable.logger_.log')
    @mock.patch('api.serializable.serializable.open', create=True)
    def test_read(self, mock_open, mock_log):
        data = '{"a": 1, "b": true}'
        mo = mock.mock_open(read_data=data)
        mock_open.side_effect = [mo.return_value]
        serializable = FakeSerializable()
        data = '{"a": 2, "b": false}'
        mock_open.reset_mock()
        mo = mock.mock_open(read_data=data)
        mock_open.side_effect = [mo.return_value]
        mock_log.reset_mock()
        serializable.read()
        mock_open.assert_called_once_with(FakeSerializable._data(), 'r')
        mock_log.assert_not_called()
        self.assertEqual(serializable.data, {'a': 2, 'b': False})

    @mock.patch('api.serializable.serializable.logger_.log')
    @mock.patch('api.serializable.serializable.open', create=True)
    def test_write(self, mock_open, mock_log):
        data = '{"a": 1, "b": true}'
        mo = mock.mock_open(read_data=data)
        mock_open.side_effect = [mo.return_value]
        serializable = FakeSerializable()
        serializable.data['a'] = 2
        serializable.data['b'] = False
        mock_open.reset_mock()
        mock_open.side_effect = [mo.return_value]
        mock_log.reset_mock()
        serializable.write()
        mock_open.assert_called_once_with(serializable._data(), 'w')
        handle = mo()
        calls = [mock.call('{\n  "a": 2,\n  "b": false\n}\n')]
        handle.write.assert_has_calls(calls)
        mock_log.assert_not_called()
        self.assertEqual(serializable.data, {'a': 2, 'b': False})

    @mock.patch('api.serializable.serializable.logger_.log')
    @mock.patch('api.serializable.serializable.open', create=True)
    def test_dump(self, mock_open, mock_log):
        data = '{"a": 1, "b": true}'
        mo = mock.mock_open(read_data=data)
        mock_open.side_effect = [mo.return_value]
        serializable = FakeSerializable()
        mock_log.reset_mock()
        mock_log.return_value = {'a': 1, 'b': True}
        serializable.dump()
        mock_log.assert_called_once_with(
            logging.DEBUG,
            'Dump completed.',
            extra={
                'stdout': '{\n  "a": 1,\n  "b": true\n}'
            })


if __name__ == '__main__':
    unittest.main()
