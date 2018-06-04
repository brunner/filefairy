#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import jinja2
import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/api/renderable', '', _path)
sys.path.append(_root)
from api.renderable.renderable import Renderable  # noqa
from util.jinja2_.jinja2_ import env  # noqa
from util.secrets.secrets import server  # noqa

_server = server()


class FakeRenderable(Renderable):
    def __init__(self, **kwargs):
        super(FakeRenderable, self).__init__(**kwargs)

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _href():
        return '/fairylab/foo/'

    @staticmethod
    def _info():
        return 'Description.'

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
    @mock.patch('api.renderable.renderable.server')
    @mock.patch('api.renderable.renderable.log')
    @mock.patch('api.serializable.serializable.open', create=True)
    @mock.patch('api.renderable.renderable.os.makedirs')
    @mock.patch.object(jinja2.environment.TemplateStream, 'dump')
    @mock.patch('api.renderable.renderable.check_output')
    def test_render__with_valid_input(self, mock_check, mock_dump,
                                      mock_makedirs, mock_open, mock_rlog,
                                      mock_server, mock_stream):
        mock_server.return_value = 'server'
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
        there = 'brunnerj@' + _server + ':/var/www'
        foo = '/html/fairylab/foo/index.html'
        sub = '/html/fairylab/foo/sub/index.html'
        rdyn = _root + '/resource/html/fairylab/foo/dyn/dyn_{}.html'
        tdyn = there + '/html/fairylab/foo/dyn/dyn_{}.html'
        check_calls = [
            mock.call(
                ['scp', _root + '/resource' + foo, there + foo], timeout=8),
            mock.call(
                ['scp', _root + '/resource' + sub, there + sub], timeout=8),
            mock.call(
                ['scp', rdyn.format(0), tdyn.format(0)], timeout=8),
            mock.call(
                ['scp', rdyn.format(1), tdyn.format(1)], timeout=8),
            mock.call(
                ['scp', rdyn.format(2), tdyn.format(2)], timeout=8),
        ]
        mock_check.assert_has_calls(check_calls)
        dump_calls = [
            mock.call(_root + '/resource' + foo),
            mock.call(_root + '/resource' + sub),
            mock.call(rdyn.format(0)),
            mock.call(rdyn.format(1)),
            mock.call(rdyn.format(2))
        ]
        mock_dump.assert_has_calls(dump_calls)
        calls = [
            mock.call(_root + '/resource/html/fairylab/foo'),
            mock.call(_root + '/resource/html/fairylab/foo/sub'),
            mock.call(_root + '/resource/html/fairylab/foo/dyn'),
            mock.call(_root + '/resource/html/fairylab/foo/dyn'),
            mock.call(_root + '/resource/html/fairylab/foo/dyn'),
        ]
        mock_makedirs.assert_has_calls(calls)
        mock_open.assert_called_once_with(FakeRenderable._data(), 'r')
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
    @mock.patch('api.renderable.renderable.server')
    @mock.patch('api.renderable.renderable.log')
    @mock.patch('api.serializable.serializable.open', create=True)
    @mock.patch('api.renderable.renderable.os.makedirs')
    @mock.patch.object(jinja2.environment.TemplateStream, 'dump')
    @mock.patch('api.renderable.renderable.check_output')
    def test_render__with_test(self, mock_check, mock_dump, mock_makedirs,
                               mock_open, mock_rlog, mock_server, mock_stream):
        mock_server.return_value = 'server'
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
        renderable._render(date=date, test=True)
        there = 'brunnerj@' + _server + ':/var/www'
        foo = '/html/fairylab/foo/index.html'
        sub = '/html/fairylab/foo/sub/index.html'
        rdyn = _root + '/html/fairylab/foo/dyn/dyn_{}.html'
        tdyn = there + '/html/fairylab/foo/dyn/dyn_{}.html'
        check_calls = [
            mock.call(['scp', _root + foo, there + foo], timeout=8),
            mock.call(['scp', _root + sub, there + sub], timeout=8),
            mock.call(
                ['scp', rdyn.format(0), tdyn.format(0)], timeout=8),
            mock.call(
                ['scp', rdyn.format(1), tdyn.format(1)], timeout=8),
            mock.call(
                ['scp', rdyn.format(2), tdyn.format(2)], timeout=8),
        ]
        mock_check.assert_has_calls(check_calls)
        dump_calls = [
            mock.call(_root + foo),
            mock.call(_root + sub),
            mock.call(rdyn.format(0)),
            mock.call(rdyn.format(1)),
            mock.call(rdyn.format(2))
        ]
        mock_dump.assert_has_calls(dump_calls)
        calls = [
            mock.call(_root + '/html/fairylab/foo'),
            mock.call(_root + '/html/fairylab/foo/sub'),
            mock.call(_root + '/html/fairylab/foo/dyn'),
            mock.call(_root + '/html/fairylab/foo/dyn'),
            mock.call(_root + '/html/fairylab/foo/dyn'),
        ]
        mock_makedirs.assert_has_calls(calls)
        mock_open.assert_called_once_with(FakeRenderable._data(), 'r')
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
    @mock.patch('api.renderable.renderable.server')
    @mock.patch('api.renderable.renderable.log')
    @mock.patch('api.serializable.serializable.open', create=True)
    @mock.patch('api.renderable.renderable.os.makedirs')
    @mock.patch('api.renderable.renderable.traceback.format_exc')
    @mock.patch.object(jinja2.environment.TemplateStream, 'dump')
    @mock.patch('api.renderable.renderable.check_output')
    def test_render__with_thrown_exception(
            self, mock_check, mock_dump, mock_exc, mock_makedirs, mock_open,
            mock_rlog, mock_server, mock_stream):
        mock_exc.return_value = 'Traceback: ...'
        mock_dump.side_effect = Exception()
        mock_server.return_value = 'server'
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
            mock.call(_root + '/resource' + foo),
            mock.call(_root + '/resource' + sub),
            mock.call(_root + '/resource' + dyn.format(0)),
            mock.call(_root + '/resource' + dyn.format(1)),
            mock.call(_root + '/resource' + dyn.format(2))
        ]
        mock_dump.assert_has_calls(dump_calls)
        calls = [
            mock.call(_root + '/resource/html/fairylab/foo'),
            mock.call(_root + '/resource/html/fairylab/foo/sub'),
            mock.call(_root + '/resource/html/fairylab/foo/dyn'),
            mock.call(_root + '/resource/html/fairylab/foo/dyn'),
            mock.call(_root + '/resource/html/fairylab/foo/dyn'),
        ]
        mock_makedirs.assert_has_calls(calls)
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

    @mock.patch('api.serializable.serializable.open', create=True)
    def test_attachments(self, mock_open):
        data = '{"a": 1, "b": true}'
        mo = mock.mock_open(read_data=data)
        mock_open.side_effect = [mo.return_value]
        plugin = FakeRenderable(e=env())
        actual = plugin._attachments()
        expected = [{
            'fallback':
            'Description.',
            'title':
            'Fairylab | foo',
            'title_link':
            'http://orangeandblueleaguebaseball.com/fairylab/foo/',
            'text':
            'Description.'
        }]
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
