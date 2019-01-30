#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for service.py."""

import os
import re
import sys
import types
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/common/service', '', _path))

from common.service.service import call_service  # noqa
from common.service.service import reload_services  # noqa


def _module(name):
    m = types.ModuleType(name, None)
    m.__file__ = name + '.py'
    sys.modules[name] = m
    return m


A = _module('a')

SERVICES_DIR = re.sub(r'/common/service', '/services', _path)


class ServiceTest(unittest.TestCase):
    @mock.patch('common.service.service.listdirs')
    @mock.patch('common.service.service.importlib.import_module')
    @mock.patch('common.service.service.getattr')
    def test_get_method(self, mock_getattr, mock_import, mock_listdirs):
        def foo(x, y, *args, **kwargs):
            self.assertEqual(x, 1)
            self.assertEqual(y, 2)
            self.assertCountEqual(args, ['i', 'j'])
            self.assertEqual(kwargs, {'extra': True})

        mock_getattr.return_value = foo
        mock_import.return_value = A
        mock_listdirs.return_value = ['a']

        reload_services()

        mock_import.assert_called_once_with('services.a.a')
        mock_listdirs.assert_called_once_with(SERVICES_DIR)
        mock_getattr.assert_not_called()

        mock_getattr.reset_mock()
        mock_import.reset_mock()
        mock_listdirs.reset_mock()

        call_service('a', 'foo', (1, 2), *('i', 'j'), extra=True)

        mock_getattr.assert_called_once_with(A, 'foo')
        mock_import.assert_not_called()
        mock_listdirs.assert_not_called()


if __name__ == '__main__':
    unittest.main()
