#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/common/test', '', _path)
sys.path.append(_root)
from api.renderable.renderable import Renderable  # noqa
from common.test.test import Test  # noqa
from common.test.test import main  # noqa


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
    def test_write(self, mock_open):
        data = '{"a": 1, "b": true}'
        mo = mock.mock_open(read_data=data)
        mock_open.side_effect = [mo.return_value]
        actual = FakeRenderableTest.write('data.json', {'a': 2, 'b': False})
        self.assertEqual(actual, {'a': 1, 'b': True})
        handle = mo()
        calls = [mock.call('{\n  "a": 2,\n  "b": false\n}\n')]
        handle.write.assert_has_calls(calls)

    @mock.patch('common.test.test.os.listdir')
    def test_main(self, mock_listdir):
        mock_listdir.return_value = ['foo.py', 'bar.py']
        main(FakeRenderableTest, FakeRenderable, 'path.to.fake',
             os.path.join(_root, 'path/to/fake'), {}, False)
        self.assertTrue(hasattr(FakeRenderableTest, 'test_golden__foo'))
        self.assertTrue(hasattr(FakeRenderableTest, 'test_golden__bar'))


if __name__ == '__main__':
    unittest.main()
