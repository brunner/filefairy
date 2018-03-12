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
from utils.jinja2.jinja2_util import env  # noqa


class FakeRenderable(RenderableApi):
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


class RenderableApiTest(unittest.TestCase):
    @mock.patch('apis.serializable.serializable_api.open', create=True)
    def test_init__with_valid_input(self, mock_open):
        data = '{"a": 1, "b": true}'
        mo = mock.mock_open(read_data=data)
        mock_open.side_effect = [mo.return_value]
        FakeRenderable(e=env())

    @mock.patch('apis.serializable.serializable_api.open', create=True)
    def test_init__with_invalid_input(self, mock_open):
        data = '{"a": 1, "b": true}'
        mo = mock.mock_open(read_data=data)
        mock_open.side_effect = [mo.return_value]
        with self.assertRaises(KeyError):
            FakeRenderable()

    @mock.patch.object(jinja2.environment.Template, 'stream')
    @mock.patch('apis.serializable.serializable_api.log')
    @mock.patch('apis.renderable.renderable_api.server', 'server')
    @mock.patch('apis.serializable.serializable_api.open', create=True)
    @mock.patch.object(jinja2.environment.TemplateStream, 'dump')
    @mock.patch('apis.renderable.renderable_api.datetime')
    @mock.patch('apis.renderable.renderable_api.check_output')
    def test_render__with_valid_input(self, mock_check, mock_datetime,
                                      mock_dump, mock_open,
                                      mock_slog, mock_stream):
        data = '{"a": 1, "b": true}'
        mo = mock.mock_open(read_data=data)
        mock_open.side_effect = [mo.return_value]
        date = '1985-10-26 00:02:30'
        mock_datetime.datetime.now.return_value.strftime.return_value = date
        mock_stream.return_value = jinja2.environment.TemplateStream(
            lambda: iter([]))
        ldr = jinja2.DictLoader({'foo.html': 'Hello {{ title }}'})
        env = jinja2.Environment(loader=ldr)
        renderable = FakeRenderable(e=env)
        renderable._render()
        here = os.path.join(_root, 'html/index.html')
        there = 'brunnerj@server:/var/www/html/fairylab/index.html'
        mock_check.assert_called_once_with(['scp', here, there])
        mock_dump.assert_called_once_with(here)
        mock_open.assert_called_once_with(FakeRenderable._data(), 'r')
        mock_slog.assert_called_once_with(renderable._name(), **{
            's': 'Read completed.',
        })
        mock_stream.assert_called_once_with({
            'date': '1985-10-26 00:02:30 PST',
            'title': 'foo'
        })
        self.assertEquals(renderable.data, {'a': 1, 'b': True})

    @mock.patch.object(jinja2.environment.Template, 'stream')
    @mock.patch('apis.serializable.serializable_api.log')
    @mock.patch('apis.renderable.renderable_api.server', 'server')
    @mock.patch('apis.renderable.renderable_api.log')
    @mock.patch('apis.serializable.serializable_api.open', create=True)
    @mock.patch('apis.renderable.renderable_api.traceback.format_exc')
    @mock.patch.object(jinja2.environment.TemplateStream, 'dump')
    @mock.patch('apis.renderable.renderable_api.datetime')
    @mock.patch('apis.renderable.renderable_api.check_output')
    def test_render__with_thrown_exception(
            self, mock_check, mock_datetime, mock_dump, mock_exc, mock_open,
            mock_rlog, mock_slog, mock_stream):
        mock_exc.return_value = 'Traceback: ...'
        mock_dump.side_effect = Exception()
        data = '{"a": 1, "b": true}'
        mo = mock.mock_open(read_data=data)
        mock_open.side_effect = [mo.return_value]
        date = '1985-10-26 00:02:30'
        mock_datetime.datetime.now.return_value.strftime.return_value = date
        mock_stream.return_value = jinja2.environment.TemplateStream(
            lambda: iter([]))
        ldr = jinja2.DictLoader({'foo.html': 'Hello {{ title }}'})
        env = jinja2.Environment(loader=ldr)
        renderable = FakeRenderable(e=env)
        renderable._render()
        here = os.path.join(_root, 'html/index.html')
        mock_check.assert_not_called()
        mock_dump.assert_called_once_with(here)
        mock_open.assert_called_once_with(FakeRenderable._data(), 'r')
        mock_rlog.assert_called_once_with(
            'FakeRenderable', c='Traceback: ...', s='Exception.', v=True)
        mock_slog.assert_called_once_with(renderable._name(), **{
            's': 'Read completed.',
        })
        mock_stream.assert_called_once_with({
            'date': '1985-10-26 00:02:30 PST',
            'title': 'foo'
        })
        self.assertEquals(renderable.data, {'a': 1, 'b': True})


if __name__ == '__main__':
    unittest.main()
