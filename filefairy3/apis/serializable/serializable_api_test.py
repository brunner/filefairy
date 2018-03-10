#!/usr/bin/env python

from serializable_api import SerializableApi

import mock
import os
import unittest

_path = os.path.dirname(os.path.abspath(__file__))


class FakeSerializable(SerializableApi):
    def __init__(self):
        super(FakeSerializable, self).__init__()

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')


class SerializableApiTest(unittest.TestCase):
    @mock.patch('serializable_api.log')
    @mock.patch('serializable_api.open', create=True)
    def test_init(self, mock_open, mock_log):
        data = '{"a": 1, "b": true}'
        mo = mock.mock_open(read_data=data)
        mock_open.side_effect = [mo.return_value]
        serializable = FakeSerializable()
        mock_open.assert_called_once_with(FakeSerializable._data(), 'r')
        mock_log.assert_called_once_with(serializable._name(), **{
            's': 'Read completed.',
        })
        self.assertEquals(serializable.data, {'a': 1, 'b': True})

    @mock.patch('serializable_api.log')
    @mock.patch('serializable_api.open', create=True)
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
        mock_log.assert_called_once_with(serializable._name(), **{
            's': 'Read completed.',
        })
        self.assertEquals(serializable.data, {'a': 2, 'b': False})

    @mock.patch('serializable_api.log')
    @mock.patch('serializable_api.open', create=True)
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
        calls = [mock.call('{\n  "a": 2, \n  "b": false\n}'), mock.call('\n')]
        handle.write.assert_has_calls(calls)
        mock_log.assert_called_once_with(serializable._name(), **{
            's': 'Write completed.'
        })
        self.assertEquals(serializable.data, {'a': 2, 'b': False})

    @mock.patch('serializable_api.log')
    @mock.patch('serializable_api.open', create=True)
    def test_dump(self, mock_open, mock_log):
        data = '{"a": 1, "b": true}'
        mo = mock.mock_open(read_data=data)
        mock_open.side_effect = [mo.return_value]
        serializable = FakeSerializable()
        mock_log.reset_mock()
        mock_log.return_value = {'a': 1, 'b': True}
        expected = {'a': 1, 'b': True}
        self.assertEquals(serializable.dump(), expected)
        mock_log.assert_called_once_with(serializable._name(), **{
            'r': '{\n  "a": 1, \n  "b": true\n}',
            's': 'Dump completed.'
        })


if __name__ == '__main__':
    unittest.main()
