#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mock
import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/apis/plugin', '', _path))
from apis.plugin.plugin_api import PluginApi  # noqa
from apis.messageable.messageable_api import MessageableApi  # noqa
from apis.runnable.runnable_api import RunnableApi  # noqa
from apis.renderable.renderable_api import RenderableApi  # noqa
from utils.jinja2.jinja2_util import env  # noqa


class FakePlugin(PluginApi):
    def __init__(self, **kwargs):
        super(FakePlugin, self).__init__(**kwargs)

    @property
    def enabled(self):
        return True

    @staticmethod
    def _info():
        return 'Description.'

    def _setup(self, **kwargs):
        pass

    def _on_message_internal(self, **kwargs):
        pass

    def _run_internal(self, **kwargs):
        pass


class FakeRenderable(PluginApi, RenderableApi):
    def __init__(self, **kwargs):
        super(FakeRenderable, self).__init__(**kwargs)

    @property
    def enabled(self):
        return True

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _html():
        return 'foo/index.html'

    @staticmethod
    def _info():
        return 'Description.'

    @staticmethod
    def _title():
        return 'foo'

    @staticmethod
    def _tmpl():
        return 'foo.html'

    def _setup(self, **kwargs):
        pass

    def _on_message_internal(self, **kwargs):
        pass

    def _run_internal(self, **kwargs):
        pass

    def _render_internal(self, **kwargs):
        return {}


class PluginApiTest(unittest.TestCase):
    def test_enabled(self):
        plugin = FakePlugin()
        self.assertTrue(plugin.enabled)

    def test_inheritance(self):
        plugin = FakePlugin()
        self.assertTrue(isinstance(plugin, MessageableApi))
        self.assertTrue(isinstance(plugin, RunnableApi))

    @mock.patch('apis.serializable.serializable_api.open', create=True)
    def test_attachments__with_valid_input(self, mock_open):
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

    def test_attachments__with_invalid_input(self):
        plugin = FakePlugin()
        actual = plugin._attachments()
        expected = []
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
