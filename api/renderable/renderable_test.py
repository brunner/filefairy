#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for renderable.py."""

import jinja2
import logging
import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/api/renderable', '', _path))

from api.renderable.renderable import Renderable  # noqa
from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.jinja2_.jinja2_ import env  # noqa
from common.json_.json_ import dumps  # noqa

ENV = env()

CONTAINING_DIR = re.sub(r'/filefairy/api/renderable', '', _path)
FAIRYLAB_DIR = CONTAINING_DIR + '/fairylab/static'
FILEFAIRY_DIR = CONTAINING_DIR + '/filefairy'
GITHUB_LINK = 'https://github.com/brunner/filefairy/'

LDR = jinja2.DictLoader({
    'foo.html':
    '{{ title }}: Hello {{ a }}, {{ b }} -- {{ date }}',
    'sub.html':
    '{{ title }}: Hello {{ m }}, {{ n }} -- {{ date }}',
    'dyn.html':
    '{{ title }}: Hello {{ z }} -- {{ date }}'
})

THEN = datetime_datetime_pst(1985, 10, 26, 0, 2, 30)
THEN_DISPLAYED = '00:02:30 PDT (1985-10-26)'
STREAM_CALLS = [
    mock.call({
        'date': THEN_DISPLAYED,
        'documentation': GITHUB_LINK,
        'title': 'foo',
        'a': 1,
        'b': True,
        'd': THEN
    }),
    mock.call({
        'date': THEN_DISPLAYED,
        'documentation': GITHUB_LINK,
        'title': 'foo » sub',
        'm': 2,
        'n': 'bar'
    }),
    mock.call({
        'date': THEN_DISPLAYED,
        'documentation': GITHUB_LINK,
        'title': 'foo » dyn0',
        'z': True
    }),
    mock.call({
        'date': THEN_DISPLAYED,
        'documentation': GITHUB_LINK,
        'title': 'foo » dyn1',
        'z': False
    }),
    mock.call({
        'date': THEN_DISPLAYED,
        'documentation': GITHUB_LINK,
        'title': 'foo » dyn2',
        'z': True
    })
]


def get_dump_calls(root_dir):
    return [
        mock.call(root_dir + '/foo/index.html'),
        mock.call(root_dir + '/foo/sub/index.html'),
        mock.call(root_dir + '/foo/dyn/dyn_0.html'),
        mock.call(root_dir + '/foo/dyn/dyn_1.html'),
        mock.call(root_dir + '/foo/dyn/dyn_2.html')
    ]


def get_makedirs_calls(root_dir):
    return [
        mock.call(root_dir + '/foo'),
        mock.call(root_dir + '/foo/sub'),
        mock.call(root_dir + '/foo/dyn'),
        mock.call(root_dir + '/foo/dyn'),
        mock.call(root_dir + '/foo/dyn'),
    ]


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
    def setUp(self):
        patch_log = mock.patch('api.renderable.renderable._logger.log')
        self.addCleanup(patch_log.stop)
        self.mock_log = patch_log.start()

        patch_open = mock.patch(
            'api.serializable.serializable.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

    def init_mocks(self):
        mo = mock.mock_open(read_data=dumps({}))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]

    def reset_mocks(self):
        self.mock_log.reset_mock()
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()

    def create_renderable(self, e):
        self.init_mocks()
        renderable = FakeRenderable(e=e)

        self.mock_log.assert_not_called()
        self.mock_open.assert_called_once_with(FakeRenderable._data(), 'r')
        self.mock_handle.write.assert_not_called()
        self.reset_mocks()
        self.init_mocks()

        return renderable

    def test_attachments(self):
        renderable = self.create_renderable(ENV)

        actual = renderable._attachments()
        expected = [{
            'fallback': 'Description.',
            'title': 'Fairylab | foo',
            'title_link': 'http://fairylab.surge.sh/foo/',
            'text': 'Description.'
        }]
        self.assertEqual(actual, expected)

        self.mock_log.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.assert_not_called()

    @mock.patch('api.renderable.renderable.chat_post_message')
    @mock.patch.object(FakeRenderable, '_attachments')
    def test_chat(self, mock_attachments, mock_chat):
        attachments = [{'title': 'title', 'text': 'text'}]
        mock_attachments.return_value = attachments
        mock_chat.return_value = {'ok': True, 'message': {'text': 'foo'}}

        renderable = self.create_renderable(ENV)

        actual = renderable._chat('channel', 'foo')
        expected = {'ok': True, 'message': {'text': 'foo'}}
        self.assertEqual(actual, expected)

        mock_attachments.assert_called_once_with()
        mock_chat.assert_called_once_with(
            'channel', 'foo', attachments=attachments)
        self.mock_log.assert_called_once_with(logging.INFO, 'foo')
        self.mock_open.assert_not_called()
        self.mock_handle.assert_not_called()

    @mock.patch.object(jinja2.environment.Template, 'stream')
    @mock.patch('api.renderable.renderable.os.makedirs')
    @mock.patch.object(jinja2.environment.TemplateStream, 'dump')
    def test_render__live(self, mock_dump, mock_makedirs, mock_stream):
        mock_stream.return_value = jinja2.environment.TemplateStream(iter([]))

        renderable = self.create_renderable(jinja2.Environment(loader=LDR))
        renderable._render(date=THEN)

        mock_dump.assert_has_calls(get_dump_calls(FAIRYLAB_DIR))
        mock_makedirs.assert_has_calls(get_makedirs_calls(FAIRYLAB_DIR))
        mock_stream.assert_has_calls(STREAM_CALLS)
        self.mock_log.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.assert_not_called()

    @mock.patch.object(jinja2.environment.Template, 'stream')
    @mock.patch('api.renderable.renderable.os.makedirs')
    @mock.patch.object(jinja2.environment.TemplateStream, 'dump')
    def test_render__test(self, mock_dump, mock_makedirs, mock_stream):
        mock_stream.return_value = jinja2.environment.TemplateStream(iter([]))

        renderable = self.create_renderable(jinja2.Environment(loader=LDR))
        renderable._render(date=THEN, test=True)

        mock_dump.assert_has_calls(get_dump_calls(FILEFAIRY_DIR))
        mock_makedirs.assert_has_calls(get_makedirs_calls(FILEFAIRY_DIR))
        mock_stream.assert_has_calls(STREAM_CALLS)
        self.mock_log.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.assert_not_called()

    @mock.patch.object(jinja2.environment.Template, 'stream')
    @mock.patch('api.renderable.renderable.os.makedirs')
    @mock.patch.object(jinja2.environment.TemplateStream, 'dump')
    def test_render__exception(self, mock_dump, mock_makedirs, mock_stream):
        mock_dump.side_effect = Exception()
        mock_stream.return_value = jinja2.environment.TemplateStream(iter([]))

        renderable = self.create_renderable(jinja2.Environment(loader=LDR))
        renderable._render(date=THEN)

        log_calls = [
            mock.call(logging.WARNING, 'Handled warning.', exc_info=True),
            mock.call(logging.WARNING, 'Handled warning.', exc_info=True),
            mock.call(logging.WARNING, 'Handled warning.', exc_info=True),
            mock.call(logging.WARNING, 'Handled warning.', exc_info=True),
            mock.call(logging.WARNING, 'Handled warning.', exc_info=True)
        ]
        mock_dump.assert_has_calls(get_dump_calls(FAIRYLAB_DIR))
        mock_makedirs.assert_has_calls(get_makedirs_calls(FAIRYLAB_DIR))
        mock_stream.assert_has_calls(STREAM_CALLS)
        self.mock_log.assert_has_calls(log_calls)
        self.mock_open.assert_not_called()
        self.mock_handle.assert_not_called()


if __name__ == '__main__':
    unittest.main()
