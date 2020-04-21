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
from common.elements.elements import dialog  # noqa
from common.elements.elements import topper  # noqa
from common.jinja2_.jinja2_ import env  # noqa
from common.json_.json_ import dumps  # noqa
from types_.response.response import Response  # noqa

ENV = env()

CONTAINING_DIR = re.sub(r'/filefairy/api/renderable', '', _path)
FAIRYLAB_DIR = CONTAINING_DIR + '/fairylab/static'
FILEFAIRY_DIR = CONTAINING_DIR + '/filefairy'

LDR = jinja2.DictLoader({
    'foo.html': '{{ title }}: Hello {{ a }}, {{ b }} -- {{ date }}',
    'sub.html': '{{ title }}: Hello {{ m }}, {{ n }} -- {{ date }}',
    'dyn.html': '{{ title }}: Hello {{ z }} -- {{ date }}'
})

MENU = dialog(id_='menu', icon='<img>', tables=[topper('Site Links')])
MENU_LIVE_CALLS = [
    mock.call('/fairylab/foo/'),
    mock.call('/fairylab/foo/sub/'),
    mock.call('/fairylab/foo/dyn/dyn_0.html'),
    mock.call('/fairylab/foo/dyn/dyn_1.html'),
    mock.call('/fairylab/foo/dyn/dyn_2.html'),
]
MENU_TEST_CALLS = [mock.call('/foo/')] * 5

THEN = datetime_datetime_pst(1985, 10, 26, 0, 2, 30)
THEN_DISPLAYED = '00:02:30 PDT (1985-10-26)'
STREAM_CALLS = [
    mock.call({
        'date': THEN_DISPLAYED,
        'menu': MENU,
        'title': 'foo',
        'a': 1,
        'b': True,
        'd': THEN
    }),
    mock.call({
        'date': THEN_DISPLAYED,
        'menu': MENU,
        'title': 'foo » sub',
        'm': 2,
        'n': 'bar'
    }),
    mock.call({
        'date': THEN_DISPLAYED,
        'menu': MENU,
        'title': 'foo » dyn0',
        'z': True
    }),
    mock.call({
        'date': THEN_DISPLAYED,
        'menu': MENU,
        'title': 'foo » dyn1',
        'z': False
    }),
    mock.call({
        'date': THEN_DISPLAYED,
        'menu': MENU,
        'title': 'foo » dyn2',
        'z': True
    }),
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
    def _href():
        return '/foo/'

    @staticmethod
    def _title():
        return 'foo'

    def _render_data(self, **kwargs):
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
        log_patch = mock.patch('api.renderable.renderable._logger.log')
        self.addCleanup(log_patch.stop)
        self.log_ = log_patch.start()

    def create_renderable(self, e):
        return FakeRenderable(e=e)

    @mock.patch.object(jinja2.environment.Template, 'stream')
    @mock.patch('api.renderable.renderable.menu')
    @mock.patch('api.renderable.renderable.os.makedirs')
    @mock.patch.object(jinja2.environment.TemplateStream, 'dump')
    def test_render__live(self, dump_, makedirs_, menu_, stream_):
        menu_.return_value = MENU
        stream_.return_value = jinja2.environment.TemplateStream(iter([]))

        renderable = self.create_renderable(jinja2.Environment(loader=LDR))
        actual = renderable._render(date=THEN)
        expected = Response()
        self.assertEqual(actual, expected)

        dump_.assert_has_calls(get_dump_calls(FAIRYLAB_DIR))
        makedirs_.assert_has_calls(get_makedirs_calls(FAIRYLAB_DIR))
        menu_.assert_has_calls(MENU_LIVE_CALLS)
        stream_.assert_has_calls(STREAM_CALLS)
        self.log_.assert_not_called()

    @mock.patch.object(jinja2.environment.Template, 'stream')
    @mock.patch('api.renderable.renderable.menu')
    @mock.patch('api.renderable.renderable.os.makedirs')
    @mock.patch.object(jinja2.environment.TemplateStream, 'dump')
    def test_render__test(self, dump_, makedirs_, menu_, stream_):
        menu_.return_value = MENU
        stream_.return_value = jinja2.environment.TemplateStream(iter([]))

        renderable = self.create_renderable(jinja2.Environment(loader=LDR))
        actual = renderable._render(date=THEN, test=True)
        expected = Response()
        self.assertEqual(actual, expected)

        dump_.assert_has_calls(get_dump_calls(FILEFAIRY_DIR))
        makedirs_.assert_has_calls(get_makedirs_calls(FILEFAIRY_DIR))
        menu_.assert_has_calls(MENU_TEST_CALLS)
        stream_.assert_has_calls(STREAM_CALLS)
        self.log_.assert_not_called()

    @mock.patch.object(jinja2.environment.Template, 'stream')
    @mock.patch('api.renderable.renderable.menu')
    @mock.patch('api.renderable.renderable.os.makedirs')
    @mock.patch.object(jinja2.environment.TemplateStream, 'dump')
    def test_render__exception(self, dump_, makedirs_, menu_, stream_):
        dump_.side_effect = Exception()
        menu_.return_value = MENU
        stream_.return_value = jinja2.environment.TemplateStream(iter([]))

        renderable = self.create_renderable(jinja2.Environment(loader=LDR))
        actual = renderable._render(date=THEN)
        expected = Response()
        self.assertEqual(actual, expected)

        log_calls = [
            mock.call(logging.WARNING, 'Handled warning.', exc_info=True),
            mock.call(logging.WARNING, 'Handled warning.', exc_info=True),
            mock.call(logging.WARNING, 'Handled warning.', exc_info=True),
            mock.call(logging.WARNING, 'Handled warning.', exc_info=True),
            mock.call(logging.WARNING, 'Handled warning.', exc_info=True)
        ]
        dump_.assert_has_calls(get_dump_calls(FAIRYLAB_DIR))
        makedirs_.assert_has_calls(get_makedirs_calls(FAIRYLAB_DIR))
        menu_.assert_has_calls(MENU_LIVE_CALLS)
        stream_.assert_has_calls(STREAM_CALLS)
        self.log_.assert_has_calls(log_calls)


if __name__ == '__main__':
    unittest.main()
