#!/usr/bin/env python

import jinja2
import mock
import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/apis/renderable', '', _path)
sys.path.append(_root)
from apis.renderable.renderable_api import RenderableApi  # noqa


class FakeRenderable(RenderableApi):
    def __init__(self, **kwargs):
        super(FakeRenderable, self).__init__(**kwargs)

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _html():
        return os.path.join(_root, 'index.html')

    @staticmethod
    def _tmpl():
        return 'foo.html'

    def _render_internal(self, **kwargs):
        return {'title': 'foo'}


class RenderableApiTest(unittest.TestCase):
    @mock.patch('apis.serializable.serializable_api.log')
    @mock.patch.object(FakeRenderable, '_render_internal')
    @mock.patch('apis.serializable.serializable_api.open', create=True)
    @mock.patch.object(jinja2.environment.TemplateStream, 'dump')
    def test_render__with_valid_input(self, mock_dump, mock_open, mock_render,
                                      mock_slog):
        data = '{"a": 1, "b": true}'
        mo = mock.mock_open(read_data=data)
        mock_open.side_effect = [mo.return_value]
        _loader = jinja2.DictLoader({'foo.html': 'Hello {{ title }}'})
        environment = jinja2.Environment(loader=_loader)
        renderable = FakeRenderable(e=environment)
        renderable._render()
        mock_dump.assert_called_once_with(os.path.join(_root, 'index.html'))
        mock_open.assert_called_once_with(FakeRenderable._data(), 'r')
        mock_render.assert_called_once_with()
        mock_slog.assert_called_once_with(renderable._name(), **{
            's': 'Read completed.',
        })
        self.assertEquals(renderable.data, {'a': 1, 'b': True})

    @mock.patch('apis.serializable.serializable_api.log')
    @mock.patch('apis.renderable.renderable_api.log')
    @mock.patch.object(FakeRenderable, '_render_internal')
    @mock.patch('apis.serializable.serializable_api.open', create=True)
    @mock.patch('apis.renderable.renderable_api.traceback.format_exc')
    @mock.patch.object(jinja2.environment.TemplateStream, 'dump')
    def test_render__with_thrown_exception(self, mock_dump, mock_exc,
                                           mock_open, mock_render, mock_rlog,
                                           mock_slog):
        mock_exc.return_value = 'Traceback: ...'
        mock_dump.side_effect = Exception()
        data = '{"a": 1, "b": true}'
        mo = mock.mock_open(read_data=data)
        mock_open.side_effect = [mo.return_value]
        _loader = jinja2.DictLoader({'foo.html': 'Hello {{ title }}'})
        environment = jinja2.Environment(loader=_loader)
        renderable = FakeRenderable(e=environment)
        renderable._render()
        mock_dump.assert_called_once_with(os.path.join(_root, 'index.html'))
        mock_open.assert_called_once_with(FakeRenderable._data(), 'r')
        mock_render.assert_called_once_with()
        mock_rlog.assert_called_once_with(
            'FakeRenderable', c='Traceback: ...', s='Exception.', v=True)
        mock_slog.assert_called_once_with(renderable._name(), **{
            's': 'Read completed.',
        })
        self.assertEquals(renderable.data, {'a': 1, 'b': True})


if __name__ == '__main__':
    unittest.main()
