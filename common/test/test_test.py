#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for test.py."""

import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/common/test', '', _path))

from api.renderable.renderable import Renderable  # noqa
from common.test.test import Test  # noqa
from common.test.test import get_testdata  # noqa
from common.test.test import main  # noqa

ISO = 'iso-8859-1'


class FakeRenderable(Renderable):
    def __init__(self, **kwargs):
        super(FakeRenderable, self).__init__(**kwargs)

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _html():
        return 'index.html'

    @staticmethod
    def _tmpl():
        return 'foo.html'

    def _render_internal(self, **kwargs):
        return {'title': 'foo'}


class FakeRenderableTest(Test):
    pass


class TestTest(unittest.TestCase):
    @mock.patch('common.test.test.open', create=True)
    @mock.patch('common.test.test.os.listdir')
    @mock.patch('common.test.test.os.path.isfile')
    def test_get_testdata(self, mock_isfile, mock_listdir, mock_open):
        mock_isfile.side_effect = [False, True, True]
        mock_listdir.return_value = ['__init__.py', '__pycache__', 'foo.html']
        mo = mock.mock_open(read_data='<html>foo</html>')
        mock_open.side_effect = [mo.return_value]

        actual = get_testdata(_path)
        expected = {'foo.html': '<html>foo</html>'}
        self.assertEqual(actual, expected)

        mock_isfile.assert_has_calls([
            mock.call(os.path.join(_path, '__pycache__')),
            mock.call(os.path.join(_path, 'foo.html'))
        ])
        mock_listdir.assert_called_once_with(_path)
        mock_open.assert_called_once_with(
            os.path.join(_path, 'foo.html'), 'r', encoding=ISO)

    @mock.patch('common.test.test.os.listdir')
    def test_main(self, mock_listdir):
        mock_listdir.return_value = ['foo.py', 'bar.py']

        root = re.sub(r'/common/test', '', _path)
        main(FakeRenderableTest, FakeRenderable, 'path.to.fake',
             os.path.join(root, 'path/to/fake'), {}, False)

        self.assertTrue(hasattr(FakeRenderableTest, 'test_golden__foo'))
        self.assertTrue(hasattr(FakeRenderableTest, 'test_golden__bar'))


if __name__ == '__main__':
    unittest.main()
