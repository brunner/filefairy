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
