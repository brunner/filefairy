#!/usr/bin/env python

from app import App

import mock
import os
import sys
import unittest

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


class AppTest(unittest.TestCase):
    def test_init(self):
        app = App()
        self.assertTrue(app.keep_running)
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
        app.plugins['fake'] = FakePlugin()
        app._try('fake', '_run_internal', a=1, b=True)
        mock_run.assert_called_once_with(a=1, b=True)
        mock_log.assert_not_called()
        self.assertIn('fake', app.plugins)

    @mock.patch.object(FakePlugin, '_run_internal')
    @mock.patch('app.log')
    @mock.patch('app.traceback.format_exc')
    def test_try__with_thrown_exception(self, mock_exc, mock_log, mock_run):
        mock_exc.return_value = 'Traceback: ...'
        mock_run.side_effect = Exception()
        app = App()
        app.plugins['fake'] = FakePlugin()
        app._try('fake', '_run_internal', a=1, b=True)
        mock_run.assert_called_once_with(a=1, b=True)
        mock_log.assert_called_once_with(
            'FakePlugin', s='Exception.', r='Traceback: ...', v=True)
        self.assertNotIn('fake', app.plugins)

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
        app.plugins['fake'] = FakePlugin()
        app._try('fake', 'foo', a=1, b=True)
        mock_run.assert_not_called()
        mock_log.assert_not_called()

    @mock.patch.object(FakePlugin, '_run_internal')
    @mock.patch('app.log')
    def test_try__with_invalid_callable(self, mock_log, mock_run):
        app = App()
        app.plugins['fake'] = FakePlugin()
        app._try('fake', 'var', a=1, b=True)
        mock_run.assert_not_called()
        mock_log.assert_not_called()

    @mock.patch.object(FakePlugin, '_setup')
    @mock.patch('app.log')
    @mock.patch('app.importlib.import_module')
    @mock.patch('app.getattr')
    @mock.patch('app.traceback.format_exc')
    def test_install_with_valid_input(self, mock_exc, mock_getattr,
                                      mock_import, mock_log, mock_setup):
        mock_getattr.side_effect = [FakePlugin, FakePlugin._setup]
        app = App()
        app.install(a1='fake')
        self.assertIn('fake', app.plugins)
        mock_import.assert_called_once_with('plugins.fake.fake_plugin')
        mock_log.assert_called_once_with(
            'FakePlugin', a1='fake', s='Installed.', v=True)
        mock_setup.assert_called_once_with()
        mock_exc.assert_not_called()

    @mock.patch.object(FakePlugin, '_setup')
    @mock.patch('app.log')
    @mock.patch('app.importlib.import_module')
    @mock.patch('app.getattr')
    @mock.patch('app.traceback.format_exc')
    def test_install_with_invalid_input(self, mock_exc, mock_getattr,
                                        mock_import, mock_log, mock_setup):
        mock_getattr.return_value = Exception()
        mock_exc.return_value = 'Traceback: ...'
        app = App()
        app.install(a1='fake')
        self.assertNotIn('fake', app.plugins)
        mock_import.assert_called_once_with('plugins.fake.fake_plugin')
        mock_log.assert_called_once_with(
            'FakePlugin',
            a1='fake',
            s='Exception.',
            r='Traceback: ...',
            v=True)
        mock_setup.assert_not_called()
        mock_exc.assert_called_once_with()

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
