#!/usr/bin/env python

from app import App

import mock
import os
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
from apis.plugin.plugin_api import PluginApi  # noqa
from utils.testing.testing_util import write  # noqa

_data = App._data()


class FakePlugin(PluginApi):
    var = True

    def __init__(self):
        super(FakePlugin, self).__init__()

    @staticmethod
    def _info():
        return 'Description.'

    def _setup(self, **kwargs):
        pass

    def _on_message_internal(self, **kwargs):
        pass

    def _run_internal(self, **kwargs):
        pass


class FakeWebSocketApp(object):
    def __init__(self, url, on_message=None):
        self.url = url
        self.on_message = on_message

        self.keep_running = True
        self.sock = True

    def close(self):
        self.keep_running = False

    def send(self, message):
        if self.on_message:
            self.on_message(self, message)
        self.close()

    def run_forever(self):
        while self.keep_running:
            pass


class AppTest(unittest.TestCase):
    def test_init(self):
        app = App()
        self.assertEqual(app.data, {'plugins': {}})
        self.assertTrue(app.keep_running)
        self.assertEqual(app.sleep, 120)
        self.assertEqual(app.ws, None)

    @mock.patch('app.os.listdir')
    @mock.patch('app.os.path.isdir')
    @mock.patch('app.App.install')
    def test_setup(self, mock_install, mock_isdir, mock_listdir):
        mock_isdir.side_effect = [True, True, True]
        mock_listdir.return_value = ['foo', 'bar', 'baz']
        app = App()
        app._setup()
        mock_listdir.assert_called_once_with(os.path.join(_path, 'plugins'))
        self.assertEqual(mock_install.call_count, 3)
        calls = [mock.call(a1='foo'), mock.call(a1='bar'), mock.call(a1='baz')]
        mock_install.assert_has_calls(calls)

    @mock.patch.object(FakePlugin, '_run_internal')
    @mock.patch('app.log')
    def test_try__with_valid_input(self, mock_log, mock_run):
        app = App()
        app.data['plugins']['fake'] = {
            'ok': True,
            'instance': FakePlugin(),
            'info': 'Description.'
        }
        app._try('fake', '_run_internal', a=1, b=True)
        mock_run.assert_called_once_with(a=1, b=True)
        mock_log.assert_not_called()
        self.assertTrue(app.data['plugins']['fake']['ok'])
        self.assertEqual(app.data['plugins']['fake']['info'], 'Description.')

    @mock.patch.object(FakePlugin, '_run_internal')
    @mock.patch('app.log')
    @mock.patch('app.traceback.format_exc')
    def test_try__with_thrown_exception(self, mock_exc, mock_log, mock_run):
        mock_exc.return_value = 'Traceback: ...'
        mock_run.side_effect = Exception()
        app = App()
        app.data['plugins']['fake'] = {
            'ok': True,
            'instance': FakePlugin(),
            'info': 'Description.'
        }
        app._try('fake', '_run_internal', a=1, b=True)
        mock_run.assert_called_once_with(a=1, b=True)
        mock_log.assert_called_once_with(
            'FakePlugin', s='Exception.', r='Traceback: ...', v=True)
        self.assertFalse(app.data['plugins']['fake']['ok'])
        self.assertEqual(app.data['plugins']['fake']['info'], 'Description.')

    @mock.patch.object(FakePlugin, '_run_internal')
    @mock.patch('app.log')
    def test_try__with_invalid_plugin(self, mock_log, mock_run):
        app = App()
        app._try('fake', '_run_internal', a=1, b=True)
        mock_run.assert_not_called()
        mock_log.assert_not_called()

    @mock.patch.object(FakePlugin, '_run_internal')
    @mock.patch('app.log')
    def test_try__with_invalid_attr(self, mock_log, mock_run):
        app = App()
        app.data['plugins']['fake'] = {
            'ok': True,
            'instance': FakePlugin(),
            'info': 'Description.'
        }
        app._try('fake', 'foo', a=1, b=True)
        mock_run.assert_not_called()
        mock_log.assert_not_called()

    @mock.patch.object(FakePlugin, '_run_internal')
    @mock.patch('app.log')
    def test_try__with_invalid_callable(self, mock_log, mock_run):
        app = App()
        app.data['plugins']['fake'] = {
            'ok': True,
            'instance': FakePlugin(),
            'info': 'Description.'
        }
        app._try('fake', 'var', a=1, b=True)
        mock_run.assert_not_called()
        mock_log.assert_not_called()

    @mock.patch('app.websocket.WebSocketApp')
    @mock.patch.object(App, '_try')
    @mock.patch('app.rtm_connect')
    @mock.patch.object(App, '_on_message')
    def test_connect(self, mock_message, mock_rtm, mock_try, mock_ws):
        mock_rtm.return_value = {'ok': True, 'url': 'wss://...'}
        mock_ws.side_effect = FakeWebSocketApp
        data = {'plugins': {}}
        original = write(_data, data)
        app = App()
        app.data['plugins']['fake'] = {
            'ok': True,
            'instance': FakePlugin(),
            'info': 'Description.'
        }
        app._connect()
        app.ws.send(
            '{"type":"message","channel":"ABC","user":"XYZ","text":"foo"}')
        expected = {
            'type': 'message',
            'channel': 'ABC',
            'user': 'XYZ',
            'text': 'foo'
        }
        mock_message.assert_called_once_with(obj=expected)
        mock_try.assert_called_once_with('fake', '_on_message', obj=expected)
        actual = write(_data, original)
        expected = {
            'plugins': {
                'fake': {
                    'ok': True,
                    'instance': '',
                    'info': 'Description.'
                }
            }
        }
        self.assertEqual(actual, expected)

    @mock.patch.object(App, '_try')
    @mock.patch('app.time.sleep')
    @mock.patch('app.log')
    @mock.patch.object(App, '_connect')
    def test_start(self, mock_connect, mock_log, mock_sleep, mock_try):
        data = {'plugins': {}}
        original = write(_data, data)
        app = App()
        app.data['plugins']['fake'] = {
            'ok': True,
            'instance': FakePlugin(),
            'info': 'Description.'
        }
        mock_sleep.side_effect = lambda s: app.shutdown()
        app._start()
        mock_connect.assert_called_once_with()
        mock_try.assert_called_once_with('fake', '_run')
        actual = write(_data, original)
        expected = {
            'plugins': {
                'fake': {
                    'ok': True,
                    'instance': '',
                    'info': 'Description.'
                }
            }
        }
        self.assertEqual(actual, expected)

    @mock.patch.object(FakePlugin, '_setup')
    @mock.patch('app.log')
    @mock.patch('app.importlib.import_module')
    @mock.patch('app.getattr')
    @mock.patch('app.traceback.format_exc')
    def test_install_with_valid_input(self, mock_exc, mock_getattr,
                                      mock_import, mock_log, mock_setup):
        mock_getattr.side_effect = [FakePlugin, FakePlugin._setup]
        data = {'plugins': {}}
        original = write(_data, data)
        app = App()
        app.install(a1='fake')
        mock_import.assert_called_once_with('plugins.fake.fake_plugin')
        mock_log.assert_called_once_with(
            'FakePlugin', a1='fake', s='Installed.', v=True)
        mock_setup.assert_called_once_with()
        mock_exc.assert_not_called()
        actual = write(_data, original)
        expected = {
            'plugins': {
                'fake': {
                    'ok': True,
                    'instance': '',
                    'info': 'Description.'
                }
            }
        }
        self.assertEqual(actual, expected)

    @mock.patch.object(FakePlugin, '_setup')
    @mock.patch('app.log')
    @mock.patch('app.importlib.import_module')
    @mock.patch('app.getattr')
    @mock.patch('app.traceback.format_exc')
    def test_install_with_invalid_input(self, mock_exc, mock_getattr,
                                        mock_import, mock_log, mock_setup):
        mock_getattr.return_value = Exception()
        mock_exc.return_value = 'Traceback: ...'
        data = {'plugins': {}}
        original = write(_data, data)
        app = App()
        app.install(a1='fake')
        mock_import.assert_called_once_with('plugins.fake.fake_plugin')
        mock_log.assert_called_once_with(
            'FakePlugin',
            a1='fake',
            s='Exception.',
            r='Traceback: ...',
            v=True)
        mock_setup.assert_not_called()
        mock_exc.assert_called_once_with()
        actual = write(_data, original)
        expected = {
            'plugins': {
                'fake': {
                    'ok': False,
                    'instance': None,
                    'info': ''
                }
            }
        }
        self.assertEqual(actual, expected)

    @mock.patch('app.log')
    @mock.patch('app.os.execv')
    def test_reboot(self, mock_execv, mock_log):
        app = App()
        app.reboot()
        mock_execv.assert_called_once_with(sys.executable,
                                           ['python'] + sys.argv)
        mock_log.assert_called_once_with('App', s='Rebooting.', v=True)

    @mock.patch('app.log')
    def test_shutdown(self, mock_log):
        app = App()
        app.shutdown()
        self.assertFalse(app.keep_running)
        mock_log.assert_called_once_with('App', s='Shutting down.', v=True)


if __name__ == '__main__':
    unittest.main()
