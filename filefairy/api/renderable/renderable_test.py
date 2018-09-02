#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import jinja2
import logging
import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/api/renderable', '', _path)
sys.path.append(_root)
from api.renderable.renderable import Renderable  # noqa
from util.datetime_.datetime_ import datetime_datetime  # noqa
from util.jinja2_.jinja2_ import env  # noqa

_fairylab_root = re.sub(r'/orangeandblueleague/filefairy', '/fairylab/static',
                        _root)


class FakeRenderable(Renderable):
    def __init__(self, **kwargs):
        super(FakeRenderable, self).__init__(**kwargs)

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _href():
        return '/foo/'

    @staticmethod
    def _info():
        return 'Description.'

    @staticmethod
    def _title():
        return 'foo'

    def _render_internal(self, **kwargs):
        _foo = self._foo(**kwargs)
        _sub = self._sub(**kwargs)
        ret = [('foo/index.html', '', 'foo.html', _foo),
               ('foo/sub/index.html', 'sub', 'sub.html', _sub)]

        for i in range(3):
            html = 'foo/dyn/dyn_{}.html'.format(i)
            r = (html, 'dyn' + str(i), 'dyn.html', self._dyn(i, **kwargs))
            ret.append(r)

        return ret

    def _foo(self, **kwargs):
        return {'a': 1, 'b': True, 'd': kwargs['date']}

    def _sub(self, **kwargs):
        return {'m': 2, 'n': 'bar'}

    def _dyn(self, key, **kwargs):
        return {'z': key % 2 == 0}


class RenderableTest(unittest.TestCase):
    @mock.patch('api.serializable.serializable.open', create=True)
    def test_init__with_valid_input(self, mock_open):
        data = '{"a": 1, "b": true}'
        mo = mock.mock_open(read_data=data)
        mock_open.side_effect = [mo.return_value]
        FakeRenderable(e=env())

    @mock.patch('api.serializable.serializable.open', create=True)
    def test_init__with_invalid_input(self, mock_open):
        data = '{"a": 1, "b": true}'
        mo = mock.mock_open(read_data=data)
        mock_open.side_effect = [mo.return_value]
        with self.assertRaises(KeyError):
            FakeRenderable()

    @mock.patch('api.serializable.serializable.open', create=True)
    @mock.patch('api.renderable.renderable.chat_post_message')
    @mock.patch.object(FakeRenderable, '_attachments')
    def test_chat(self, mock_attachments, mock_chat, mock_open):
        attachments = [{'title': 'title', 'text': 'text'}]
        mock_attachments.return_value = attachments
        mock_chat.return_value = {'ok': True, 'message': {'text': 'foo'}}
        data = '{"a": 1, "b": true}'
        mo = mock.mock_open(read_data=data)
        mock_open.side_effect = [mo.return_value]
        plugin = FakeRenderable(e=env())
        actual = plugin._chat('channel', 'foo')
        expected = {'ok': True, 'message': {'text': 'foo'}}
        self.assertEqual(actual, expected)
        mock_attachments.assert_called_once_with()
        mock_chat.assert_called_once_with(
            'channel', 'foo', attachments=attachments)

    @mock.patch.object(jinja2.environment.Template, 'stream')
    @mock.patch('api.renderable.renderable.logger_.log')
    @mock.patch('api.serializable.serializable.open', create=True)
    @mock.patch('api.renderable.renderable.os.makedirs')
    @mock.patch.object(jinja2.environment.TemplateStream, 'dump')
    def test_render__with_valid_input(self, mock_dump, mock_makedirs,
                                      mock_open, mock_rlog, mock_stream):
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
        date = datetime_datetime(1985, 10, 26, 0, 2, 30)
        env = jinja2.Environment(loader=ldr)
        renderable = FakeRenderable(e=env)
        renderable._render(date=date)
        foo = '/foo/index.html'
        sub = '/foo/sub/index.html'
        rdyn = _fairylab_root + '/foo/dyn/dyn_{}.html'
        dump_calls = [
            mock.call(_fairylab_root + foo),
            mock.call(_fairylab_root + sub),
            mock.call(rdyn.format(0)),
            mock.call(rdyn.format(1)),
            mock.call(rdyn.format(2))
        ]
        mock_dump.assert_has_calls(dump_calls)
        calls = [
            mock.call(_fairylab_root + '/foo'),
            mock.call(_fairylab_root + '/foo/sub'),
            mock.call(_fairylab_root + '/foo/dyn'),
            mock.call(_fairylab_root + '/foo/dyn'),
            mock.call(_fairylab_root + '/foo/dyn'),
        ]
        mock_makedirs.assert_has_calls(calls)
        mock_open.assert_called_once_with(FakeRenderable._data(), 'r')
        stream_calls = [
            mock.call({
                'date': '00:02:30 EDT (1985-10-26)',
                'title': 'foo',
                'a': 1,
                'b': True,
                'd': date
            }),
            mock.call({
                'date': '00:02:30 EDT (1985-10-26)',
                'title': 'foo » sub',
                'm': 2,
                'n': 'bar'
            }),
            mock.call({
                'date': '00:02:30 EDT (1985-10-26)',
                'title': 'foo » dyn0',
                'z': True
            }),
            mock.call({
                'date': '00:02:30 EDT (1985-10-26)',
                'title': 'foo » dyn1',
                'z': False
            }),
            mock.call({
                'date': '00:02:30 EDT (1985-10-26)',
                'title': 'foo » dyn2',
                'z': True
            })
        ]
        mock_stream.assert_has_calls(stream_calls)
        self.assertEqual(renderable.data, {'a': 1, 'b': True})
        mock_rlog.assert_not_called()

    @mock.patch.object(jinja2.environment.Template, 'stream')
    @mock.patch('api.renderable.renderable.logger_.log')
    @mock.patch('api.serializable.serializable.open', create=True)
    @mock.patch('api.renderable.renderable.os.makedirs')
    @mock.patch.object(jinja2.environment.TemplateStream, 'dump')
    def test_render__with_test(self, mock_dump, mock_makedirs, mock_open,
                               mock_rlog, mock_stream):
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
        date = datetime_datetime(1985, 10, 26, 0, 2, 30)
        env = jinja2.Environment(loader=ldr)
        renderable = FakeRenderable(e=env)
        renderable._render(date=date, test=True)
        foo = '/foo/index.html'
        sub = '/foo/sub/index.html'
        rdyn = _root + '/foo/dyn/dyn_{}.html'
        dump_calls = [
            mock.call(_root + foo),
            mock.call(_root + sub),
            mock.call(rdyn.format(0)),
            mock.call(rdyn.format(1)),
            mock.call(rdyn.format(2))
        ]
        mock_dump.assert_has_calls(dump_calls)
        calls = [
            mock.call(_root + '/foo'),
            mock.call(_root + '/foo/sub'),
            mock.call(_root + '/foo/dyn'),
            mock.call(_root + '/foo/dyn'),
            mock.call(_root + '/foo/dyn'),
        ]
        mock_makedirs.assert_has_calls(calls)
        mock_open.assert_called_once_with(FakeRenderable._data(), 'r')
        stream_calls = [
            mock.call({
                'date': '00:02:30 EDT (1985-10-26)',
                'title': 'foo',
                'a': 1,
                'b': True,
                'd': date
            }),
            mock.call({
                'date': '00:02:30 EDT (1985-10-26)',
                'title': 'foo » sub',
                'm': 2,
                'n': 'bar'
            }),
            mock.call({
                'date': '00:02:30 EDT (1985-10-26)',
                'title': 'foo » dyn0',
                'z': True
            }),
            mock.call({
                'date': '00:02:30 EDT (1985-10-26)',
                'title': 'foo » dyn1',
                'z': False
            }),
            mock.call({
                'date': '00:02:30 EDT (1985-10-26)',
                'title': 'foo » dyn2',
                'z': True
            })
        ]
        mock_stream.assert_has_calls(stream_calls)
        self.assertEqual(renderable.data, {'a': 1, 'b': True})
        mock_rlog.assert_not_called()

    @mock.patch.object(jinja2.environment.Template, 'stream')
    @mock.patch('api.renderable.renderable.logger_.log')
    @mock.patch('api.serializable.serializable.open', create=True)
    @mock.patch('api.renderable.renderable.os.makedirs')
    @mock.patch.object(jinja2.environment.TemplateStream, 'dump')
    def test_render__with_thrown_exception(self, mock_dump, mock_makedirs,
                                           mock_open, mock_rlog, mock_stream):
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
        date = datetime_datetime(1985, 10, 26, 0, 2, 30)
        env = jinja2.Environment(loader=ldr)
        renderable = FakeRenderable(e=env)
        renderable._render(date=date)
        foo = '/foo/index.html'
        sub = '/foo/sub/index.html'
        dyn = '/foo/dyn/dyn_{}.html'
        dump_calls = [
            mock.call(_fairylab_root + foo),
            mock.call(_fairylab_root + sub),
            mock.call(_fairylab_root + dyn.format(0)),
            mock.call(_fairylab_root + dyn.format(1)),
            mock.call(_fairylab_root + dyn.format(2))
        ]
        mock_dump.assert_has_calls(dump_calls)
        calls = [
            mock.call(_fairylab_root + '/foo'),
            mock.call(_fairylab_root + '/foo/sub'),
            mock.call(_fairylab_root + '/foo/dyn'),
            mock.call(_fairylab_root + '/foo/dyn'),
            mock.call(_fairylab_root + '/foo/dyn'),
        ]
        mock_makedirs.assert_has_calls(calls)
        mock_open.assert_called_once_with(FakeRenderable._data(), 'r')
        log_calls = [
            mock.call(logging.WARNING, 'Handled warning.', exc_info=True),
            mock.call(logging.WARNING, 'Handled warning.', exc_info=True),
            mock.call(logging.WARNING, 'Handled warning.', exc_info=True),
            mock.call(logging.WARNING, 'Handled warning.', exc_info=True),
            mock.call(logging.WARNING, 'Handled warning.', exc_info=True)
        ]
        mock_rlog.assert_has_calls(log_calls)
        stream_calls = [
            mock.call({
                'date': '00:02:30 EDT (1985-10-26)',
                'title': 'foo',
                'a': 1,
                'b': True,
                'd': date
            }),
            mock.call({
                'date': '00:02:30 EDT (1985-10-26)',
                'title': 'foo » sub',
                'm': 2,
                'n': 'bar'
            }),
            mock.call({
                'date': '00:02:30 EDT (1985-10-26)',
                'title': 'foo » dyn0',
                'z': True
            }),
            mock.call({
                'date': '00:02:30 EDT (1985-10-26)',
                'title': 'foo » dyn1',
                'z': False
            }),
            mock.call({
                'date': '00:02:30 EDT (1985-10-26)',
                'title': 'foo » dyn2',
                'z': True
            })
        ]
        mock_stream.assert_has_calls(stream_calls)
        self.assertEqual(renderable.data, {'a': 1, 'b': True})

    @mock.patch('api.serializable.serializable.open', create=True)
    def test_attachments(self, mock_open):
        data = '{"a": 1, "b": true}'
        mo = mock.mock_open(read_data=data)
        mock_open.side_effect = [mo.return_value]
        plugin = FakeRenderable(e=env())
        actual = plugin._attachments()
        expected = [{
            'fallback': 'Description.',
            'title': 'Fairylab | foo',
            'title_link': 'http://fairylab.surge.sh/foo/',
            'text': 'Description.'
        }]
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
