#!/usr/bin/env python

from app import App

import mock
import os
import unittest
import websocket

_path = os.path.dirname(os.path.abspath(__file__))
from apis.plugin.plugin_api import PluginApi  # noqa


class FakePlugin(PluginApi):
    var = True

    def __init__(self):
        super(FakePlugin, self).__init__()

    def _setup(self, **kwargs):
        pass

    def _on_message_internal(self, **kwargs):
        pass

    def _run_internal(self, **kwargs):
        pass


class FakeWebSocketApp(websocket.WebSocketApp):
    sock = None


class AppTest(unittest.TestCase):
    def test_init(self):
        app = App()
        self.assertEqual(app.keep_running, True)
        self.assertEqual(app.plugins, {})
        self.assertEqual(app.sleep, 120)
        self.assertEqual(app.ws, None)

    @mock.patch('app.os.listdir')
    @mock.patch('app.os.path.isdir')
    @mock.patch('app.App.install')
    def test_setup(self, mock_install, mock_isdir, mock_listdir):
        mock_isdir.side_effect = [True, True, True]
        mock_listdir.return_value = ['foo', 'bar', 'ba_z']
        app = App()
        app._setup()
        mock_listdir.assert_called_once_with(os.path.join(_path, 'plugins'))
        self.assertEqual(mock_install.call_count, 3)
        calls = [
            mock.call(a1='foo'),
            mock.call(a1='bar'),
            mock.call(a1='ba_z')
        ]
        mock_install.assert_has_calls(calls)

    @mock.patch.object(FakePlugin, '_run_internal')
    @mock.patch('app.log')
    def test_try__with_valid_input(self, mock_log, mock_run):
        app = App()
        app.plugins['fake_plugin'] = FakePlugin()
        app._try('fake_plugin', '_run_internal', a=1, b=True)
        mock_run.assert_called_once_with(a=1, b=True)
        mock_log.assert_not_called()
        self.assertIn('fake_plugin', app.plugins)

    @mock.patch.object(FakePlugin, '_run_internal')
    @mock.patch('app.log')
    @mock.patch('app.traceback.format_exc')
    def test_try__with_thrown_exception(self, mock_exc, mock_log, mock_run):
        mock_exc.return_value = 'Traceback: ...'
        mock_run.side_effect = Exception('Error message.')
        app = App()
        app.plugins['fake_plugin'] = FakePlugin()
        app._try('fake_plugin', '_run_internal', a=1, b=True)
        mock_run.assert_called_once_with(a=1, b=True)
        mock_log.assert_called_once_with(
            'FakePlugin', s='Exception.', r='Traceback: ...', v=True)
        self.assertNotIn('fake_plugin', app.plugins)

    @mock.patch.object(FakePlugin, '_run_internal')
    @mock.patch('app.log')
    def test_try__with_invalid_plugin(self, mock_log, mock_run):
        app = App()
        app._try('fake_plugin', '_run_internal', a=1, b=True)
        mock_run.assert_not_called()
        mock_log.assert_not_called()

    @mock.patch.object(FakePlugin, '_run_internal')
    @mock.patch('app.log')
    def test_try__with_invalid_attr(self, mock_log, mock_run):
        app = App()
        app.plugins['fake_plugin'] = FakePlugin()
        app._try('fake_plugin', 'foo', a=1, b=True)
        mock_run.assert_not_called()
        mock_log.assert_not_called()

    @mock.patch.object(FakePlugin, '_run_internal')
    @mock.patch('app.log')
    def test_try__with_invalid_callable(self, mock_log, mock_run):
        app = App()
        app.plugins['fake_plugin'] = FakePlugin()
        app._try('fake_plugin', 'var', a=1, b=True)
        mock_run.assert_not_called()
        mock_log.assert_not_called()


if __name__ == '__main__':
    unittest.main()
