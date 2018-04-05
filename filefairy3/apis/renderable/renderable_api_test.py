#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
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
    def _href():
        return '/fairylab/foo/'

    @staticmethod
    def _title():
        return 'foo'

    def _render_internal(self, **kwargs):
        _foo = self._foo(**kwargs)
        _sub = self._sub(**kwargs)
        ret = [('html/fairylab/foo/index.html', '', 'foo.html', _foo),
               ('html/fairylab/foo/sub/index.html', 'sub', 'sub.html', _sub)]

        for i in range(3):
            html = 'html/fairylab/foo/dyn/dyn_{}.html'.format(i)
            r = (html, 'dyn' + str(i), 'dyn.html', self._dyn(i, **kwargs))
            ret.append(r)

        return ret

    def _foo(self, **kwargs):
        return {'a': 1, 'b': True, 'd': kwargs['date']}

    def _sub(self, **kwargs):
        return {'m': 2, 'n': 'bar'}

    def _dyn(self, key, **kwargs):
        return {'z': key % 2 == 0}


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
    @mock.patch('apis.renderable.renderable_api.check_output')
    @mock.patch('apis.renderable.renderable_api.log')
    def test_render__with_valid_input(self, mock_rlog, mock_check, mock_dump,
                                      mock_open, mock_slog, mock_stream):
        data = '{"a": 1, "b": true}'
        mo = mock.mock_open(read_data=data)
        mock_open.side_effect = [mo.return_value]
        mock_stream.return_value = jinja2.environment.TemplateStream(iter([]))
        ldr = jinja2.DictLoader({
            'foo.html':
            '{{ title }}: Hello {{ a }}, {{ b }} -- {{ date }}',
            'sub.html':
            '{{ title }}: Hello {{ m }}, {{ n }} -- {{ date }}',
            'dyn.html':
            '{{ title }}: Hello {{ z }} -- {{ date }}'
        })
        date = datetime.datetime(1985, 10, 26, 0, 2, 30)
        env = jinja2.Environment(loader=ldr)
        renderable = FakeRenderable(e=env)
        renderable._render(date=date)
        there = 'brunnerj@server:/var/www'
        foo = '/html/fairylab/foo/index.html'
        sub = '/html/fairylab/foo/sub/index.html'
        dyn = '/html/fairylab/foo/dyn/dyn_{}.html'
        check_calls = [
            mock.call(['scp', _root + foo, there + foo]),
            mock.call(['scp', _root + sub, there + sub]),
            mock.call(['scp', _root + dyn.format(0), there + dyn.format(0)]),
            mock.call(['scp', _root + dyn.format(1), there + dyn.format(1)]),
            mock.call(['scp', _root + dyn.format(2), there + dyn.format(2)])
        ]
        mock_check.assert_has_calls(check_calls)
        dump_calls = [
            mock.call(_root + foo),
            mock.call(_root + sub),
            mock.call(_root + dyn.format(0)),
            mock.call(_root + dyn.format(1)),
            mock.call(_root + dyn.format(2))
        ]
        mock_dump.assert_has_calls(dump_calls)
        mock_open.assert_called_once_with(FakeRenderable._data(), 'r')
        mock_slog.assert_called_once_with(renderable._name(), **{
            's': 'Read completed.',
        })
        stream_calls = [
            mock.call({
                'date': '1985-10-26 00:02:30 PST',
                'title': 'foo',
                'a': 1,
                'b': True,
                'd': date
            }),
            mock.call({
                'date': '1985-10-26 00:02:30 PST',
                'title': 'foo » sub',
                'm': 2,
                'n': 'bar'
            }),
            mock.call({
                'date': '1985-10-26 00:02:30 PST',
                'title': 'foo » dyn0',
                'z': True
            }),
            mock.call({
                'date': '1985-10-26 00:02:30 PST',
                'title': 'foo » dyn1',
                'z': False
            }),
            mock.call({
                'date': '1985-10-26 00:02:30 PST',
                'title': 'foo » dyn2',
                'z': True
            })
        ]
        mock_stream.assert_has_calls(stream_calls)
        self.assertEqual(renderable.data, {'a': 1, 'b': True})
        mock_rlog.assert_not_called()

    @mock.patch.object(jinja2.environment.Template, 'stream')
    @mock.patch('apis.serializable.serializable_api.log')
    @mock.patch('apis.renderable.renderable_api.server', 'server')
    @mock.patch('apis.renderable.renderable_api.log')
    @mock.patch('apis.serializable.serializable_api.open', create=True)
    @mock.patch('apis.renderable.renderable_api.traceback.format_exc')
    @mock.patch.object(jinja2.environment.TemplateStream, 'dump')
    @mock.patch('apis.renderable.renderable_api.check_output')
    def test_render__with_thrown_exception(self, mock_check, mock_dump,
                                           mock_exc, mock_open, mock_rlog,
                                           mock_slog, mock_stream):
        mock_exc.return_value = 'Traceback: ...'
        mock_dump.side_effect = Exception()
        data = '{"a": 1, "b": true}'
        mo = mock.mock_open(read_data=data)
        mock_open.side_effect = [mo.return_value]
        mock_stream.return_value = jinja2.environment.TemplateStream(iter([]))
        ldr = jinja2.DictLoader({
            'foo.html':
            '{{ title }}: Hello {{ a }}, {{ b }} -- {{ date }}',
            'sub.html':
            '{{ title }}: Hello {{ m }}, {{ n }} -- {{ date }}',
            'dyn.html':
            '{{ title }}: Hello {{ z }} -- {{ date }}'
        })
        date = datetime.datetime(1985, 10, 26, 0, 2, 30)
        env = jinja2.Environment(loader=ldr)
        renderable = FakeRenderable(e=env)
        renderable._render(date=date)
        foo = '/html/fairylab/foo/index.html'
        sub = '/html/fairylab/foo/sub/index.html'
        dyn = '/html/fairylab/foo/dyn/dyn_{}.html'
        mock_check.assert_not_called()
        dump_calls = [
            mock.call(_root + foo),
            mock.call(_root + sub),
            mock.call(_root + dyn.format(0)),
            mock.call(_root + dyn.format(1)),
            mock.call(_root + dyn.format(2))
        ]
        mock_dump.assert_has_calls(dump_calls)
        mock_open.assert_called_once_with(FakeRenderable._data(), 'r')
        log_calls = [
            mock.call(
                'FakeRenderable', c='Traceback: ...', s='Exception.', v=True),
            mock.call(
                'FakeRenderable', c='Traceback: ...', s='Exception.', v=True),
            mock.call(
                'FakeRenderable', c='Traceback: ...', s='Exception.', v=True),
            mock.call(
                'FakeRenderable', c='Traceback: ...', s='Exception.', v=True),
            mock.call(
                'FakeRenderable', c='Traceback: ...', s='Exception.', v=True)
        ]
        mock_rlog.assert_has_calls(log_calls)
        mock_slog.assert_called_once_with(renderable._name(), **{
            's': 'Read completed.',
        })
        stream_calls = [
            mock.call({
                'date': '1985-10-26 00:02:30 PST',
                'title': 'foo',
                'a': 1,
                'b': True,
                'd': date
            }),
            mock.call({
                'date': '1985-10-26 00:02:30 PST',
                'title': 'foo » sub',
                'm': 2,
                'n': 'bar'
            }),
            mock.call({
                'date': '1985-10-26 00:02:30 PST',
                'title': 'foo » dyn0',
                'z': True
            }),
            mock.call({
                'date': '1985-10-26 00:02:30 PST',
                'title': 'foo » dyn1',
                'z': False
            }),
            mock.call({
                'date': '1985-10-26 00:02:30 PST',
                'title': 'foo » dyn2',
                'z': True
            })
        ]
        mock_stream.assert_has_calls(stream_calls)
        self.assertEqual(renderable.data, {'a': 1, 'b': True})


if __name__ == '__main__':
    unittest.main()
