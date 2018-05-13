#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mock
import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/api/plugin', '', _path))
from api.plugin.plugin import Plugin  # noqa
from api.messageable.messageable import Messageable  # noqa
from api.runnable.runnable import Runnable  # noqa
from api.renderable.renderable import Renderable  # noqa
from util.jinja2.jinja2_ import env  # noqa
from value.notify.notify import Notify  # noqa
from value.response.response import Response  # noqa


class FakePlugin(Plugin):
    def __init__(self, **kwargs):
        super(FakePlugin, self).__init__(**kwargs)

    @property
    def enabled(self):
        return True

    @staticmethod
    def _info():
        return 'Description.'

    def _notify_internal(self, **kwargs):
        return True

    def _on_message_internal(self, **kwargs):
        return Response()

    def _run_internal(self, **kwargs):
        return Response()

    def _setup_internal(self, **kwargs):
        pass

    def _shadow_internal(self, **kwargs):
        pass


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

    def _notify_internal(self, **kwargs):
        return False

    def _on_message_internal(self, **kwargs):
        return Response()

    def _run_internal(self, **kwargs):
        return Response()

    def _render_internal(self, **kwargs):
        return {}

    def _setup_internal(self, **kwargs):
        pass

    def _shadow_internal(self, **kwargs):
        pass


class PluginTest(unittest.TestCase):
    def test_init(self):
        plugin = FakePlugin()
        self.assertTrue(plugin.enabled)
        self.assertTrue(isinstance(plugin, Messageable))
        self.assertTrue(isinstance(plugin, Runnable))

    @mock.patch('api.serializable.serializable.open', create=True)
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

    def test_notify__with_true(self):
        plugin = FakePlugin()
        response = plugin._notify(notify=Notify.OTHER)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

    @mock.patch('api.serializable.serializable.open', create=True)
    def test_notify__with_false(self, mock_open):
        data = '{"a": 1, "b": true}'
        mo = mock.mock_open(read_data=data)
        mock_open.side_effect = [mo.return_value]
        plugin = FakeRenderable(e=env())
        response = plugin._notify(notify=Notify.OTHER)
        self.assertEqual(response, Response())

    @mock.patch.object(FakePlugin, '_shadow_internal')
    @mock.patch.object(FakePlugin, '_setup_internal')
    def test_setup(self, mock_setup, mock_shadow):
        shadow = {'foo': {'fake.bar': 'baz'}}
        mock_shadow.return_value = shadow

        plugin = FakePlugin()
        response = plugin._setup()
        self.assertEqual(response, Response(shadow=shadow))

        mock_setup.assert_called_once_with()
        mock_shadow.assert_called_once_with()

    def test_shadow(self):
        plugin = FakePlugin()
        self.assertEqual(plugin.shadow, {})

        response = plugin._shadow(shadow={'fake.bar': 'baz'})
        self.assertEqual(response, Response())
        self.assertEqual(plugin.shadow, {'fake.bar': 'baz'})


if __name__ == '__main__':
    unittest.main()
