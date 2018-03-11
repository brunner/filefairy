#!/usr/bin/env python

import datetime
import jinja2
import importlib
import mock
import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(_path)
_root = re.sub(r'/programs/fairylab', '', _path)
sys.path.append(_root)
from apis.plugin.plugin_api import PluginApi  # noqa
from apis.renderable.renderable_api import RenderableApi  # noqa
from programs.fairylab.fairylab_program import FairylabProgram  # noqa
from utils.testing.testing_util import write  # noqa

_data = FairylabProgram._data()


class FakePlugin(PluginApi, RenderableApi):
    var = True

    def __init__(self, **kwargs):
        super(FakePlugin, self).__init__(**kwargs)
        self.environment = kwargs.get('e', None)

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _html():
        return 'fake/index.html'

    @staticmethod
    def _info():
        return 'Description.'

    @staticmethod
    def _tmpl():
        return 'fake.html'

    def _setup(self, **kwargs):
        pass

    def _on_message_internal(self, **kwargs):
        return True

    def _run_internal(self, **kwargs):
        return True

    def _render_internal(self, **kwargs):
        return {'title': 'foo'}


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


class FairylabProgramTest(unittest.TestCase):
    def test_init(self):
        fairylab = FairylabProgram()
        self.assertEqual(fairylab.data, {'plugins': {}})
        self.assertIsNotNone(fairylab.environment)
        self.assertTrue(fairylab.keep_running)
        self.assertEqual(fairylab.sleep, 120)
        self.assertEqual(fairylab.ws, None)

    @mock.patch('programs.fairylab.fairylab_program.os.listdir')
    @mock.patch('programs.fairylab.fairylab_program.os.path.isdir')
    @mock.patch('programs.fairylab.fairylab_program.FairylabProgram.install')
    def test_setup(self, mock_install, mock_isdir, mock_listdir):
        mock_isdir.side_effect = [True, True, True]
        mock_listdir.return_value = ['foo', 'bar', 'baz']
        fairylab = FairylabProgram()
        fairylab._setup()
        mock_listdir.assert_called_once_with(os.path.join(_root, 'plugins'))
        self.assertEqual(mock_install.call_count, 3)
        calls = [mock.call(a1='foo'), mock.call(a1='bar'), mock.call(a1='baz')]
        mock_install.assert_has_calls(calls)

    @mock.patch.object(FakePlugin, '_run_internal')
    @mock.patch('programs.fairylab.fairylab_program.log')
    @mock.patch('programs.fairylab.fairylab_program.datetime')
    def test_try__with_valid_input(self, mock_datetime, mock_log, mock_run):
        fairylab = FairylabProgram()
        fairylab.data['plugins']['fake'] = {
            'ok': True,
            'date': datetime.datetime.now(),
            'info': 'Description.'
        }
        fairylab.pins['fake'] = FakePlugin()
        fairylab._try('fake', '_run_internal', a=1, b=True)
        mock_run.assert_called_once_with(a=1, b=True)
        mock_datetime.datetime.now.assert_called_once_with()
        mock_log.assert_not_called()
        self.assertTrue(fairylab.data['plugins']['fake']['ok'])
        self.assertEqual(fairylab.data['plugins']['fake']['info'],
                         'Description.')

    @mock.patch.object(FakePlugin, '_run_internal')
    @mock.patch('programs.fairylab.fairylab_program.log')
    @mock.patch('programs.fairylab.fairylab_program.traceback.format_exc')
    @mock.patch('programs.fairylab.fairylab_program.datetime')
    def test_try__with_thrown_exception(self, mock_datetime, mock_exc,
                                        mock_log, mock_run):
        mock_exc.return_value = 'Traceback: ...'
        mock_run.side_effect = Exception()
        fairylab = FairylabProgram()
        fairylab.data['plugins']['fake'] = {
            'ok': True,
            'date': datetime.datetime.now(),
            'info': 'Description.'
        }
        fairylab.pins['fake'] = FakePlugin()
        fairylab._try('fake', '_run_internal', a=1, b=True)
        mock_run.assert_called_once_with(a=1, b=True)
        mock_datetime.datetime.now.assert_called_once_with()
        mock_log.assert_called_once_with(
            'FakePlugin', c='Traceback: ...', s='Exception.', v=True)
        self.assertFalse(fairylab.data['plugins']['fake']['ok'])
        self.assertEqual(fairylab.data['plugins']['fake']['info'],
                         'Description.')

    @mock.patch.object(FakePlugin, '_run_internal')
    @mock.patch('programs.fairylab.fairylab_program.log')
    def test_try__with_invalid_plugin(self, mock_log, mock_run):
        fairylab = FairylabProgram()
        fairylab._try('fake', '_run_internal', a=1, b=True)
        mock_run.assert_not_called()
        mock_log.assert_not_called()

    @mock.patch.object(FakePlugin, '_run_internal')
    @mock.patch('programs.fairylab.fairylab_program.log')
    def test_try__with_invalid_attr(self, mock_log, mock_run):
        fairylab = FairylabProgram()
        fairylab.data['plugins']['fake'] = {
            'ok': True,
            'date': datetime.datetime.now(),
            'info': 'Description.'
        }
        fairylab.pins['fake'] = FakePlugin()
        fairylab._try('fake', 'foo', a=1, b=True)
        mock_run.assert_not_called()
        mock_log.assert_not_called()

    @mock.patch.object(FakePlugin, '_run_internal')
    @mock.patch('programs.fairylab.fairylab_program.log')
    def test_try__with_invalid_callable(self, mock_log, mock_run):
        fairylab = FairylabProgram()
        fairylab.data['plugins']['fake'] = {
            'ok': True,
            'date': datetime.datetime.now(),
            'info': 'Description.'
        }
        fairylab.pins['fake'] = FakePlugin()
        fairylab._try('fake', 'var', a=1, b=True)
        mock_run.assert_not_called()
        mock_log.assert_not_called()

    @mock.patch.object(FairylabProgram, '_try')
    @mock.patch.object(FairylabProgram, '_on_message')
    def test_recv(self, mock_message, mock_try):
        data = {'plugins': {}}
        original = write(_data, data)
        fairylab = FairylabProgram()
        fairylab.data['plugins']['fake'] = {
            'ok': True,
            'date': datetime.datetime.now(),
            'info': 'Description.'
        }
        fairylab.pins['fake'] = FakePlugin()
        fairylab._recv(
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
        self.assertEqual(actual, data)

    @mock.patch('programs.fairylab.fairylab_program.websocket.WebSocketApp')
    @mock.patch('programs.fairylab.fairylab_program.rtm_connect')
    @mock.patch.object(FairylabProgram, '_recv')
    def test_connect(self, mock_recv, mock_rtm, mock_ws):
        mock_rtm.return_value = {'ok': True, 'url': 'wss://...'}
        mock_ws.side_effect = FakeWebSocketApp
        fairylab = FairylabProgram()
        fairylab.data['plugins']['fake'] = {
            'ok': True,
            'date': datetime.datetime.now(),
            'info': 'Description.'
        }
        fairylab.pins['fake'] = FakePlugin()
        fairylab._connect()
        fairylab.ws.send(
            '{"type":"message","channel":"ABC","user":"XYZ","text":"foo"}')
        mock_recv.assert_called_once_with(
            '{"type":"message","channel":"ABC","user":"XYZ","text":"foo"}')

    @mock.patch.object(FairylabProgram, '_try')
    @mock.patch('programs.fairylab.fairylab_program.time.sleep')
    @mock.patch('programs.fairylab.fairylab_program.log')
    @mock.patch.object(jinja2.environment.TemplateStream, 'dump')
    @mock.patch.object(FairylabProgram, '_connect')
    def test_start(self, mock_connect, mock_dump, mock_log, mock_sleep,
                   mock_try):
        data = {'plugins': {}}
        original = write(_data, data)
        fairylab = FairylabProgram()
        fairylab.data['plugins']['fake'] = {
            'ok': True,
            'date': datetime.datetime.now(),
            'info': 'Description.'
        }
        fairylab.pins['fake'] = FakePlugin()
        mock_sleep.side_effect = lambda s: fairylab.shutdown()
        fairylab._start()
        mock_connect.assert_called_once_with()
        mock_try.assert_called_once_with('fake', '_run')
        actual = write(_data, original)
        self.assertEqual(actual, data)

    @mock.patch.object(jinja2.environment.TemplateStream, 'dump')
    @mock.patch('programs.fairylab.fairylab_program.delta')
    @mock.patch('programs.fairylab.fairylab_program.datetime')
    @mock.patch('apis.renderable.renderable_api.check_output')
    def test_render(self, mock_check, mock_datetime, mock_delta, mock_dump):
        then = datetime.datetime(1985, 10, 26, 0, 0, 0)
        now = datetime.datetime(1985, 10, 26, 0, 2, 30)
        mock_datetime.datetime.now.return_value = now
        mock_delta.return_value = '2m ago'
        data = {'plugins': {}}
        original = write(_data, data)
        fairylab = FairylabProgram()
        fairylab.data['plugins']['fake'] = {
            'ok': True,
            'date': then,
            'info': 'Description.'
        }
        fairylab.pins['fake'] = FakePlugin()
        actual = fairylab._render_internal()
        expected = {
            'title': 'home',
            'breadcrumbs': [{
                'href': '',
                'name': 'Home'
            }],
            'plugins': {
                'fake': {
                    'ok': True,
                    'date': '2m ago',
                    'href': '/fairylab/fake/',
                    'info': 'Description.'
                }
            }
        }
        self.assertEqual(actual, expected)
        write(_data, original)

    @mock.patch.object(FakePlugin, '_setup')
    @mock.patch('programs.fairylab.fairylab_program.log')
    @mock.patch('programs.fairylab.fairylab_program.importlib.import_module')
    @mock.patch('programs.fairylab.fairylab_program.getattr')
    @mock.patch('programs.fairylab.fairylab_program.traceback.format_exc')
    def test_install__with_valid_input(self, mock_exc, mock_getattr,
                                       mock_import, mock_log, mock_setup):
        mock_getattr.side_effect = [FakePlugin, FakePlugin._setup]
        data = {'plugins': {}}
        original = write(_data, data)
        fairylab = FairylabProgram()
        fairylab.install(a1='fake')
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
                    'date': '',
                    'info': 'Description.'
                }
            }
        }
        self.assertEqual(actual, expected)
        self.assertIsNotNone(fairylab.pins['fake'])

    @mock.patch.object(FakePlugin, '_setup')
    @mock.patch('programs.fairylab.fairylab_program.log')
    @mock.patch('programs.fairylab.fairylab_program.importlib.import_module')
    @mock.patch('programs.fairylab.fairylab_program.getattr')
    @mock.patch('programs.fairylab.fairylab_program.traceback.format_exc')
    def test_install__with_invalid_input(self, mock_exc, mock_getattr,
                                         mock_import, mock_log, mock_setup):
        mock_getattr.return_value = Exception()
        mock_exc.return_value = 'Traceback: ...'
        data = {'plugins': {}}
        original = write(_data, data)
        fairylab = FairylabProgram()
        fairylab.install(a1='fake')
        mock_import.assert_called_once_with('plugins.fake.fake_plugin')
        mock_log.assert_called_once_with(
            'FakePlugin',
            a1='fake',
            c='Traceback: ...',
            s='Exception.',
            v=True)
        mock_setup.assert_not_called()
        mock_exc.assert_called_once_with()
        actual = write(_data, original)
        expected = {'plugins': {'fake': {'ok': False, 'date': '', 'info': ''}}}
        self.assertEqual(actual, expected)
        self.assertIsNone(fairylab.pins['fake'])

    @mock.patch('programs.fairylab.fairylab_program.log')
    @mock.patch('programs.fairylab.fairylab_program.os.execv')
    def test_reboot(self, mock_execv, mock_log):
        fairylab = FairylabProgram()
        fairylab.reboot()
        mock_execv.assert_called_once_with(sys.executable,
                                           ['python'] + sys.argv)
        mock_log.assert_called_once_with(
            'FairylabProgram', s='Rebooting.', v=True)

    @mock.patch('programs.fairylab.fairylab_program.log')
    def test_shutdown(self, mock_log):
        fairylab = FairylabProgram()
        fairylab.shutdown()
        self.assertFalse(fairylab.keep_running)
        mock_log.assert_called_once_with(
            'FairylabProgram', s='Shutting down.', v=True)


class FairylabProgramGoldenTest(unittest.TestCase):
    @mock.patch('apis.renderable.renderable_api.datetime')
    @mock.patch.object(FairylabProgram, '_html')
    @mock.patch('programs.fairylab.fairylab_program.datetime')
    @mock.patch('apis.renderable.renderable_api.check_output')
    def test_golden__canonical(self, mock_check, mock_fdatetime, mock_html,
                               mock_rdatetime):
        now = datetime.datetime(1985, 10, 26, 0, 3, 0)
        mock_fdatetime.datetime.now.return_value = now
        mock_rdatetime.datetime.now.return_value = now
        golden = os.path.join(_path, 'goldens/canonical_golden.html')
        mock_html.return_value = golden
        sample = 'programs.fairylab.samples.canonical_sample'
        module = importlib.import_module(sample)
        data = getattr(module, 'data')
        fairylab = FairylabProgram()
        fairylab.data = data
        fairylab.pins['bar'] = FakePlugin()
        fairylab._render()


if __name__ == '__main__':
    unittest.main()
