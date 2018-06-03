#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/api/plugin', '', _path))
from api.plugin.plugin import Plugin  # noqa
from api.messageable.messageable import Messageable  # noqa
from api.runnable.runnable import Runnable  # noqa
from api.renderable.renderable import Renderable  # noqa
from core.response.response import Response  # noqa
from core.shadow.shadow import Shadow  # noqa
from util.jinja2_.jinja2_ import env  # noqa

NOW = datetime.datetime(1985, 10, 27, 0, 0, 0)


class FakePlugin(Plugin):
    def __init__(self, **kwargs):
        super(FakePlugin, self).__init__(**kwargs)

    @property
    def enabled(self):
        return True

    @staticmethod
    def _info():
        return 'Description.'

    def _on_message_internal(self, **kwargs):
        return Response()

    def _run_internal(self, **kwargs):
        return Response()

    def _setup_internal(self, **kwargs):
        return Response()

    def _shadow_internal(self, **kwargs):
        return [Shadow(destination='foo', key='plugin.bar', data='baz')]


class FakeRenderable(Plugin, Renderable):
    def __init__(self, **kwargs):
        super(FakeRenderable, self).__init__(**kwargs)

    @property
    def enabled(self):
        return True

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

    @staticmethod
    def _tmpl():
        return 'foo.html'

    def _on_message_internal(self, **kwargs):
        return Response()

    def _run_internal(self, **kwargs):
        return Response()

    def _render_internal(self, **kwargs):
        return {}

    def _setup_internal(self, **kwargs):
        return Response()

    def _shadow_internal(self, **kwargs):
        return []


class PluginTest(unittest.TestCase):
    def test_init(self):
        plugin = FakePlugin(date=NOW)
        self.assertTrue(plugin.enabled)
        self.assertTrue(isinstance(plugin, Messageable))
        self.assertTrue(isinstance(plugin, Runnable))

    def test_setup(self):
        plugin = FakePlugin(date=NOW)
        response = plugin._setup()
        self.assertEqual(
            response,
            Response(shadow=[
                Shadow(destination='foo', key='plugin.bar', data='baz')
            ]))

    @mock.patch.object(FakePlugin, '_setup')
    def test_shadow(self, mock_setup):
        shadow = Shadow(destination='foo', key='plugin.bar', data='baz')
        plugin = FakePlugin(date=NOW)
        self.assertEqual(plugin.shadow, {})

        response = plugin._shadow(shadow=shadow)
        self.assertEqual(response, Response())

        mock_setup.assert_called_once_with(shadow=shadow)
        self.assertEqual(plugin.shadow, {'plugin.bar': 'baz'})


if __name__ == '__main__':
    unittest.main()
