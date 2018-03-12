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
from utils.jinja2.jinja2_util import env  # noqa
from utils.testing.testing_util import write  # noqa

_data = FairylabProgram._data()


class BrowsablePlugin(PluginApi, RenderableApi):
    def __init__(self, **kwargs):
        super(BrowsablePlugin, self).__init__(**kwargs)

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _html():
        return 'browsable/index.html'

    @staticmethod
    def _info():
        return 'Description of browsable.'

    @staticmethod
    def _tmpl():
        return 'browsable.html'

    def _setup(self, **kwargs):
        pass

    def _on_message_internal(self, **kwargs):
        return True

    def _run_internal(self, **kwargs):
        return True

    def _render_internal(self, **kwargs):
        return {'title': 'foo'}


class InternalPlugin(PluginApi):
    var = True

    def __init__(self, **kwargs):
        super(InternalPlugin, self).__init__(**kwargs)

    @staticmethod
    def _info():
        return 'Description of internal.'

    def _setup(self, **kwargs):
        pass

    def _on_message_internal(self, **kwargs):
        return True

    def _run_internal(self, **kwargs):
        return True


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
        fairylab = FairylabProgram(e=env())
        self.assertEqual(fairylab.data, {'plugins': {}})
        self.assertTrue(fairylab.keep_running)
        self.assertEqual(fairylab.sleep, 120)
        self.assertEqual(fairylab.ws, None)

    @mock.patch('programs.fairylab.fairylab_program.os.listdir')
    @mock.patch('programs.fairylab.fairylab_program.os.path.isdir')
    @mock.patch('programs.fairylab.fairylab_program.FairylabProgram.install')
    def test_setup(self, mock_install, mock_isdir, mock_listdir):
        mock_isdir.side_effect = [True, True, True]
        mock_listdir.return_value = ['foo', 'bar', 'baz']
        fairylab = FairylabProgram(e=env())
        fairylab._setup()
        mock_listdir.assert_called_once_with(os.path.join(_root, 'plugins'))
        self.assertEqual(mock_install.call_count, 3)
        calls = [mock.call(a1='foo'), mock.call(a1='bar'), mock.call(a1='baz')]
        mock_install.assert_has_calls(calls)

    @mock.patch.object(InternalPlugin, '_run_internal')
    @mock.patch('programs.fairylab.fairylab_program.log')
    @mock.patch('programs.fairylab.fairylab_program.datetime')
    def test_try__with_valid_input(self, mock_datetime, mock_log, mock_run):
        fairylab = FairylabProgram(e=env())
        fairylab.data['plugins']['internal'] = {
            'ok': True,
            'date': datetime.datetime.now()
        }
        fairylab.pins['internal'] = InternalPlugin()
        fairylab._try('internal', '_run_internal', a=1, b=True)
        mock_run.assert_called_once_with(a=1, b=True)
        mock_datetime.datetime.now.assert_called_once_with()
        mock_log.assert_not_called()
        self.assertTrue(fairylab.data['plugins']['internal']['ok'])

    @mock.patch.object(InternalPlugin, '_run_internal')
    @mock.patch('programs.fairylab.fairylab_program.log')
    @mock.patch('programs.fairylab.fairylab_program.traceback.format_exc')
    @mock.patch('programs.fairylab.fairylab_program.datetime')
    def test_try__with_thrown_exception(self, mock_datetime, mock_exc,
                                        mock_log, mock_run):
        mock_exc.return_value = 'Traceback: ...'
        mock_run.side_effect = Exception()
        fairylab = FairylabProgram(e=env())
        fairylab.data['plugins']['internal'] = {
            'ok': True,
            'date': datetime.datetime.now()
        }
        fairylab.pins['internal'] = InternalPlugin()
        fairylab._try('internal', '_run_internal', a=1, b=True)
        mock_run.assert_called_once_with(a=1, b=True)
        mock_datetime.datetime.now.assert_called_once_with()
        mock_log.assert_called_once_with(
            'InternalPlugin', c='Traceback: ...', s='Exception.', v=True)
        self.assertFalse(fairylab.data['plugins']['internal']['ok'])

    @mock.patch.object(InternalPlugin, '_run_internal')
    @mock.patch('programs.fairylab.fairylab_program.log')
    def test_try__with_invalid_plugin(self, mock_log, mock_run):
        fairylab = FairylabProgram(e=env())
        fairylab._try('internal', '_run_internal', a=1, b=True)
        mock_run.assert_not_called()
        mock_log.assert_not_called()

    @mock.patch.object(InternalPlugin, '_run_internal')
    @mock.patch('programs.fairylab.fairylab_program.log')
    def test_try__with_invalid_attr(self, mock_log, mock_run):
        fairylab = FairylabProgram(e=env())
        fairylab.data['plugins']['internal'] = {
            'ok': True,
            'date': datetime.datetime.now()
        }
        fairylab.pins['internal'] = InternalPlugin()
        fairylab._try('internal', 'foo', a=1, b=True)
        mock_run.assert_not_called()
        mock_log.assert_not_called()

    @mock.patch.object(InternalPlugin, '_run_internal')
    @mock.patch('programs.fairylab.fairylab_program.log')
    def test_try__with_invalid_callable(self, mock_log, mock_run):
        fairylab = FairylabProgram(e=env())
        fairylab.data['plugins']['internal'] = {
            'ok': True,
            'date': datetime.datetime.now()
        }
        fairylab.pins['internal'] = InternalPlugin()
        fairylab._try('internal', 'var', a=1, b=True)
        mock_run.assert_not_called()
        mock_log.assert_not_called()

    @mock.patch.object(FairylabProgram, '_try')
    @mock.patch.object(FairylabProgram, '_on_message')
    def test_recv(self, mock_message, mock_try):
        data = {'plugins': {}}
        original = write(_data, data)
        fairylab = FairylabProgram(e=env())
        fairylab.data['plugins']['internal'] = {
            'ok': True,
            'date': datetime.datetime.now()
        }
        fairylab.pins['internal'] = InternalPlugin()
        fairylab._recv(
            '{"type":"message","channel":"ABC","user":"XYZ","text":"foo"}')
        expected = {
            'type': 'message',
            'channel': 'ABC',
            'user': 'XYZ',
            'text': 'foo'
        }
        mock_message.assert_called_once_with(obj=expected)
        mock_try.assert_called_once_with(
            'internal', '_on_message', obj=expected)
        actual = write(_data, original)
        self.assertEqual(actual, data)

    @mock.patch('programs.fairylab.fairylab_program.websocket.WebSocketApp')
    @mock.patch('programs.fairylab.fairylab_program.rtm_connect')
    @mock.patch.object(FairylabProgram, '_recv')
    def test_connect(self, mock_recv, mock_rtm, mock_ws):
        mock_rtm.return_value = {'ok': True, 'url': 'wss://...'}
        mock_ws.side_effect = FakeWebSocketApp
        fairylab = FairylabProgram(e=env())
        fairylab.data['plugins']['internal'] = {
            'ok': True,
            'date': datetime.datetime.now()
        }
        fairylab.pins['internal'] = InternalPlugin()
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
        fairylab = FairylabProgram(e=env())
        fairylab.data['plugins']['internal'] = {
            'ok': True,
            'date': datetime.datetime.now()
        }
        fairylab.pins['internal'] = InternalPlugin()
        mock_sleep.side_effect = lambda s: fairylab.shutdown()
        fairylab._start()
        mock_connect.assert_called_once_with()
        mock_try.assert_called_once_with('internal', '_run')
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
        environment = env()
        fairylab = FairylabProgram(e=environment)
        fairylab.data['plugins']['browsable'] = {'ok': True, 'date': then}
        fairylab.pins['browsable'] = BrowsablePlugin(e=environment)
        fairylab.data['plugins']['internal'] = {'ok': True, 'date': then}
        fairylab.pins['internal'] = InternalPlugin(e=environment)
        actual = fairylab._render_internal()
        expected = {
            'title':
            'home',
            'breadcrumbs': [{
                'href': '',
                'name': 'Home'
            }],
            'browsable': [{
                'name': 'browsable',
                'ok': True,
                'delta': '2m ago',
                'href': '/fairylab/browsable/',
                'info': 'Description of browsable.'
            }],
            'internal': [{
                'name': 'internal',
                'ok': True,
                'delta': '2m ago',
                'href': '',
                'info': 'Description of internal.'
            }],
        }
        self.assertEqual(actual, expected)
        write(_data, original)

    @mock.patch.object(InternalPlugin, '_setup')
    @mock.patch('programs.fairylab.fairylab_program.log')
    @mock.patch('programs.fairylab.fairylab_program.importlib.import_module')
    @mock.patch('programs.fairylab.fairylab_program.getattr')
    @mock.patch('programs.fairylab.fairylab_program.traceback.format_exc')
    def test_install__with_valid_input(self, mock_exc, mock_getattr,
                                       mock_import, mock_log, mock_setup):
        mock_getattr.side_effect = [InternalPlugin, InternalPlugin._setup]
        data = {'plugins': {}}
        original = write(_data, data)
        fairylab = FairylabProgram(e=env())
        fairylab.install(a1='internal')
        mock_import.assert_called_once_with('plugins.internal.internal_plugin')
        mock_log.assert_called_once_with(
            'InternalPlugin', a1='internal', s='Installed.', v=True)
        mock_setup.assert_called_once_with()
        mock_exc.assert_not_called()
        actual = write(_data, original)
        expected = {
            'plugins': {
                'internal': {
                    'ok': True,
                    'date': '',
                }
            }
        }
        self.assertEqual(actual, expected)
        self.assertIsNotNone(fairylab.pins['internal'])

    @mock.patch.object(InternalPlugin, '_setup')
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
        fairylab = FairylabProgram(e=env())
        fairylab.install(a1='internal')
        mock_import.assert_called_once_with('plugins.internal.internal_plugin')
        mock_log.assert_called_once_with(
            'InternalPlugin',
            a1='internal',
            c='Traceback: ...',
            s='Exception.',
            v=True)
        mock_setup.assert_not_called()
        mock_exc.assert_called_once_with()
        actual = write(_data, original)
        expected = {'plugins': {'internal': {'ok': False, 'date': ''}}}
        self.assertEqual(actual, expected)
        self.assertIsNone(fairylab.pins['internal'])

    @mock.patch('programs.fairylab.fairylab_program.log')
    @mock.patch('programs.fairylab.fairylab_program.os.execv')
    def test_reboot(self, mock_execv, mock_log):
        fairylab = FairylabProgram(e=env())
        fairylab.reboot()
        mock_execv.assert_called_once_with(sys.executable,
                                           ['python'] + sys.argv)
        mock_log.assert_called_once_with(
            'FairylabProgram', s='Rebooting.', v=True)

    @mock.patch('programs.fairylab.fairylab_program.log')
    def test_shutdown(self, mock_log):
        fairylab = FairylabProgram(e=env())
        fairylab.shutdown()
        self.assertFalse(fairylab.keep_running)
        mock_log.assert_called_once_with(
            'FairylabProgram', s='Shutting down.', v=True)


class FairylabProgramGoldenTest(unittest.TestCase):
    @mock.patch.object(FairylabProgram, '_render_internal')
    @mock.patch.object(FairylabProgram, '_html')
    @mock.patch('apis.renderable.renderable_api.datetime')
    @mock.patch('apis.renderable.renderable_api.check_output')
    def test_golden__canonical(self, mock_check, mock_datetime, mock_html,
                               mock_render):
        now = datetime.datetime(1985, 10, 26, 0, 3, 0)
        mock_datetime.datetime.now.return_value = now
        golden = os.path.join(_path, 'goldens/canonical_golden.html')
        mock_html.return_value = golden
        sample = 'programs.fairylab.samples.canonical_sample'
        module = importlib.import_module(sample)
        mock_render.return_value = getattr(module, 'sample')
        fairylab = FairylabProgram(e=env())
        fairylab._render()


if __name__ == '__main__':
    unittest.main()
