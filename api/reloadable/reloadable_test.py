#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for reloadable.py."""

import os
import re
import sys
import types
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/api/reloadable', '', _path))

from api.reloadable.reloadable import Reloadable  # noqa


def _foo():
    pass


def _bar():
    pass


def _baz():
    pass


def _module(name):
    m = types.ModuleType(name, None)
    m.__file__ = name + '.py'
    sys.modules[name] = m
    return m


class FakeReloadable(Reloadable):
    def __init__(self, **kwargs):
        super(FakeReloadable, self).__init__(**kwargs)

    def _reload_data(self, **kwargs):
        return {'a': ['foo', 'bar'], 'b': ['baz']}


class ReloadableTest(unittest.TestCase):
    def create_reloadable(self):
        return FakeReloadable()

    def test_call(self):
        def a(x, y, z, *args, **kwargs):
            self.assertEqual(x, 1)
            self.assertEqual(y, 2)
            self.assertEqual(z, 3)
            self.assertCountEqual(args, ['i', 'j', 'k'])
            self.assertEqual(kwargs, {'extra': True})

        reloadable = self.create_reloadable()
        reloadable.attrs = {'a': a}
        reloadable._call('a', (1, 2, 3), *('i', 'j', 'k'), extra=True)

    @mock.patch('api.reloadable.reloadable.importlib.import_module')
    @mock.patch('api.reloadable.reloadable.getattr')
    def test_reload(self, mock_getattr, mock_import):
        a = _module('a')
        b = _module('b')
        mock_getattr.side_effect = [_foo, _bar, _baz]
        mock_import.side_effect = [a, b]

        reloadable = self.create_reloadable()
        reloadable._reload()
        expected = {'foo': _foo, 'bar': _bar, 'baz': _baz}
        self.assertEqual(reloadable.attrs, expected)

        mock_getattr.assert_has_calls(
            [mock.call(a, 'foo'),
             mock.call(a, 'bar'),
             mock.call(b, 'baz')])
        mock_import.assert_has_calls(
            [mock.call('services.a.a'),
             mock.call('services.b.b')])


if __name__ == '__main__':
    unittest.main()
