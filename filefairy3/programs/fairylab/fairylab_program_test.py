#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import datetime
import functools
import mock
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(_path)
_root = re.sub(r'/programs/fairylab', '', _path)
sys.path.append(_root)
from apis.plugin.plugin_api import PluginApi  # noqa
from apis.renderable.renderable_api import RenderableApi  # noqa
from programs.fairylab.fairylab_program import FairylabProgram  # noqa
from utils.component.component_util import card  # noqa
from utils.json.json_util import dumps  # noqa
from utils.jinja2.jinja2_util import env  # noqa
from utils.test.test_util import main, TestUtil  # noqa


class BrowsablePlugin(PluginApi, RenderableApi):
    def __init__(self, **kwargs):
        super(BrowsablePlugin, self).__init__(**kwargs)

    @property
    def enabled(self):
        return True

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _href():
        return '/fairylab/browsable/'

    @staticmethod
    def _info():
        return 'Description of browsable.'

    @staticmethod
    def _title():
        return 'foo'

    def _setup(self, **kwargs):
        pass

    def _on_message_internal(self, **kwargs):
        return True

    def _run_internal(self, **kwargs):
        return True

    def _render_internal(self, **kwargs):
        return [('html/fairylab/browsable/index.html', '', 'browse.html', {})]


class InternalPlugin(PluginApi):
    var = True

    def __init__(self, **kwargs):
        super(InternalPlugin, self).__init__(**kwargs)

    @property
    def enabled(self):
        return True

    @staticmethod
    def _info():
        return 'Description of internal.'

    def _setup(self, **kwargs):
        pass

    def _on_message_internal(self, **kwargs):
        return True

    def _run_internal(self, **kwargs):
        return True


class DisabledPlugin(PluginApi):
    def __init__(self, **kwargs):
        super(DisabledPlugin, self).__init__(**kwargs)

    @property
    def enabled(self):
        return False

    @staticmethod
    def _info():
        return 'Description of disabled.'

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


DATA = FairylabProgram._data()
NOW = datetime.datetime(1985, 10, 26, 0, 2, 30)
NOW_ENCODED = '1985-10-26T00:02:30'
THEN = datetime.datetime(1985, 10, 26, 0, 0, 0)
THEN_ENCODED = '1985-10-26T00:00:00'
DIR_BAR = os.path.join(_root, 'plugins', 'bar')
DIR_BAZ = os.path.join(_root, 'plugins', 'baz')
DIR_FOO = os.path.join(_root, 'plugins', 'foo')
DIR_PLUGINS = os.path.join(_root, 'plugins')
HOME = {'breadcrumbs': [], 'browsable': [], 'internal': []}
INDEX = 'html/fairylab/index.html'
MODULES = {'plugins.internal.internal_plugin': None}
PINS_BOTH = {
    'browsable': BrowsablePlugin(e=env()),
    'internal': InternalPlugin()
}
PINS_INTERNAL = {'internal': InternalPlugin()}
PLUGIN_CANONICAL_ERROR = {'date': NOW_ENCODED, 'ok': False}
PLUGIN_CANONICAL_THEN = {'date': THEN_ENCODED, 'ok': True}
PLUGIN_CANONICAL_NOW = {'date': NOW_ENCODED, 'ok': True}
TRACEBACK = 'Traceback: ...'
BREADCRUMBS = [{'href': '', 'name': 'Home'}]


def set_date_now(program, *args, **kwargs):
    program._plugin('internal')['date'] = NOW_ENCODED


def set_running_false(program, *args, **kwargs):
    program.keep_running = False


class FairylabProgramTest(TestUtil):
    def setUp(self):
        patch_open = mock.patch(
            'apis.serializable.serializable_api.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

        patch_datetime = mock.patch(
            'programs.fairylab.fairylab_program.datetime')
        self.addCleanup(patch_datetime.stop)
        self.mock_datetime = patch_datetime.start()

        patch_log = mock.patch('programs.fairylab.fairylab_program.log')
        self.addCleanup(patch_log.stop)
        self.mock_log = patch_log.start()

        patch_traceback = mock.patch(
            'programs.fairylab.fairylab_program.traceback.format_exc')
        self.addCleanup(patch_traceback.stop)
        self.mock_traceback = patch_traceback.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]
        self.mock_datetime.datetime.now.return_value = THEN
        self.mock_traceback.return_value = TRACEBACK

    def reset_mocks(self):
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()
        self.mock_datetime.reset_mock()
        self.mock_log.reset_mock()
        self.mock_traceback.reset_mock()

    def create_program(self, data, pins={}):
        self.init_mocks(data)
        program = FairylabProgram(e=env())

        self.mock_open.assert_called_once_with(DATA, 'r')
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_traceback.assert_not_called()
        self.assertEqual(program.data, data)

        self.reset_mocks()
        self.init_mocks(data)

        if pins:
            program.pins = pins

        return program

    def test_init(self):
        read = {'plugins': {'internal': copy.deepcopy(PLUGIN_CANONICAL_THEN)}}
        program = self.create_program(read)

        self.assertEqual(program.data, read)
        self.assertEqual(program.pins, {})
        self.assertTrue(program.keep_running)
        self.assertEqual(program.sleep, 120)
        self.assertEqual(program.ws, None)

    @mock.patch('programs.fairylab.fairylab_program.os.listdir')
    @mock.patch('programs.fairylab.fairylab_program.os.path.isdir')
    @mock.patch.object(FairylabProgram, 'install')
    def test_setup(self, mock_install, mock_isdir, mock_listdir):
        mock_isdir.side_effect = [True, True, True]
        mock_listdir.return_value = ['foo', 'bar', 'baz']

        read = {'plugins': {'internal': copy.deepcopy(PLUGIN_CANONICAL_THEN)}}
        program = self.create_program(read, pins=PINS_INTERNAL)
        program._setup()

        calls = [
            mock.call(a1='foo', date=THEN),
            mock.call(a1='bar', date=THEN),
            mock.call(a1='baz', date=THEN)
        ]
        mock_install.assert_has_calls(calls)
        calls = [mock.call(DIR_FOO), mock.call(DIR_BAR), mock.call(DIR_BAZ)]
        mock_isdir.assert_has_calls(calls)
        mock_listdir.assert_called_once_with(DIR_PLUGINS)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_called_once_with()
        self.mock_log.assert_not_called()
        self.assertEqual(program.pins, PINS_INTERNAL)

    @mock.patch.object(FairylabProgram, '_home')
    def test_render(self, mock_home):
        mock_home.return_value = HOME

        read = {'plugins': {'internal': copy.deepcopy(PLUGIN_CANONICAL_THEN)}}
        program = self.create_program(read, pins=PINS_INTERNAL)
        ret = program._render_internal(date=NOW)
        self.assertEqual(ret, [(INDEX, '', 'home.html', HOME)])

        mock_home.assert_called_once_with(date=NOW)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(program.pins, PINS_INTERNAL)

    def test_plugin_path(self):
        actual = FairylabProgram._plugin_path('internal')
        expected = 'plugins.internal.internal_plugin'
        self.assertEqual(actual, expected)

    def test_plugin_clazz(self):
        actual = FairylabProgram._plugin_clazz('internal')
        expected = 'InternalPlugin'
        self.assertEqual(actual, expected)
        actual = FairylabProgram._plugin_clazz('foo_bar')
        expected = 'FooBarPlugin'
        self.assertEqual(actual, expected)

    @mock.patch.object(InternalPlugin, '_run_internal')
    def test_try__with_valid_input(self, mock_run):
        mock_run.return_value = True

        read = {'plugins': {'internal': copy.deepcopy(PLUGIN_CANONICAL_THEN)}}
        program = self.create_program(read, pins=PINS_INTERNAL)
        program._try('internal', '_run_internal', date=NOW)

        mock_run.assert_called_once_with(date=NOW)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(program._plugin('internal'), PLUGIN_CANONICAL_NOW)

    @mock.patch.object(InternalPlugin, '_run_internal')
    def test_try__with_no_change(self, mock_run):
        mock_run.return_value = False

        read = {'plugins': {'internal': copy.deepcopy(PLUGIN_CANONICAL_THEN)}}
        program = self.create_program(read, pins=PINS_INTERNAL)
        program._try('internal', '_run_internal', date=NOW)

        mock_run.assert_called_once_with(date=NOW)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(program._plugin('internal'), PLUGIN_CANONICAL_THEN)

    @mock.patch.object(InternalPlugin, '_run_internal')
    def test_try__without_date(self, mock_run):
        mock_run.return_value = True

        read = {'plugins': {'internal': copy.deepcopy(PLUGIN_CANONICAL_THEN)}}
        program = self.create_program(read, pins=PINS_INTERNAL)
        program._try('internal', '_run_internal')

        mock_run.assert_called_once_with(date=THEN)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_called_once_with()
        self.mock_log.assert_not_called()
        self.assertEqual(program._plugin('internal'), PLUGIN_CANONICAL_THEN)

    @mock.patch.object(InternalPlugin, '_run_internal')
    def test_try__with_thrown_exception(self, mock_run):
        mock_run.side_effect = Exception()

        read = {'plugins': {'internal': copy.deepcopy(PLUGIN_CANONICAL_THEN)}}
        program = self.create_program(read, pins=PINS_INTERNAL)
        program._try('internal', '_run_internal', date=NOW)

        mock_run.assert_called_once_with(date=NOW)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_called_once_with(
            'InternalPlugin', c='Traceback: ...', s='Exception.', v=True)
        self.assertEqual(program._plugin('internal'), PLUGIN_CANONICAL_ERROR)

    @mock.patch.object(InternalPlugin, '_run_internal')
    def test_try__with_plugin_error(self, mock_run):
        read = {'plugins': {'internal': copy.deepcopy(PLUGIN_CANONICAL_ERROR)}}
        program = self.create_program(read, pins=PINS_INTERNAL)
        program._try('internal', '_run_internal', date=NOW)

        mock_run.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(program._plugin('internal'), PLUGIN_CANONICAL_ERROR)

    @mock.patch.object(InternalPlugin, '_run_internal')
    def test_try__with_plugin_not_found(self, mock_run):
        read = {'plugins': {'internal': copy.deepcopy(PLUGIN_CANONICAL_THEN)}}
        program = self.create_program(read, pins=PINS_INTERNAL)
        program._try('foo', '_run_internal', date=NOW)

        mock_run.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(program._plugin('internal'), PLUGIN_CANONICAL_THEN)

    def test_try__with_item_not_found(self):
        read = {'plugins': {'internal': copy.deepcopy(PLUGIN_CANONICAL_THEN)}}
        program = self.create_program(read, pins=PINS_INTERNAL)
        program._try('internal', '_foo', date=NOW)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(program._plugin('internal'), PLUGIN_CANONICAL_THEN)

    def test_try__with_item_not_callable(self):
        read = {'plugins': {'internal': copy.deepcopy(PLUGIN_CANONICAL_THEN)}}
        program = self.create_program(read, pins=PINS_INTERNAL)
        program._try('internal', 'var', date=NOW)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(program._plugin('internal'), PLUGIN_CANONICAL_THEN)

    @mock.patch.object(FairylabProgram, '_try')
    @mock.patch.object(FairylabProgram, '_on_message')
    def test_recv__with_valid_input(self, mock_message, mock_try):
        read = {'plugins': {'internal': copy.deepcopy(PLUGIN_CANONICAL_THEN)}}
        program = self.create_program(read, pins=PINS_INTERNAL)

        mock_try.side_effect = functools.partial(set_date_now, program)
        program._recv('{"type":"message","channel":"ABC","text":"foo"}')

        write = {'plugins': {'internal': copy.deepcopy(PLUGIN_CANONICAL_NOW)}}
        obj = {'type': 'message', 'channel': 'ABC', 'text': 'foo'}
        mock_message.assert_called_once_with(obj=obj)
        mock_try.assert_called_once_with('internal', '_on_message', obj=obj)
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(program._plugin('internal'), PLUGIN_CANONICAL_NOW)

    @mock.patch.object(FairylabProgram, '_try')
    @mock.patch.object(FairylabProgram, '_on_message')
    def test_recv__with_no_change(self, mock_message, mock_try):
        read = {'plugins': {'internal': copy.deepcopy(PLUGIN_CANONICAL_THEN)}}
        program = self.create_program(read, pins=PINS_INTERNAL)
        program._recv('{"type":"message","channel":"ABC","text":"foo"}')

        obj = {'type': 'message', 'channel': 'ABC', 'text': 'foo'}
        mock_message.assert_called_once_with(obj=obj)
        mock_try.assert_called_once_with('internal', '_on_message', obj=obj)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(program._plugin('internal'), PLUGIN_CANONICAL_THEN)

    @mock.patch('programs.fairylab.fairylab_program.websocket.WebSocketApp')
    @mock.patch('programs.fairylab.fairylab_program.threading.Thread')
    @mock.patch('programs.fairylab.fairylab_program.rtm_connect')
    @mock.patch.object(FairylabProgram, '_recv')
    def test_connect__with_valid_input(self, mock_recv, mock_rtm, mock_thread,
                                       mock_ws):
        mock_rtm.return_value = {'ok': True, 'url': 'wss://...'}
        mock_ws.side_effect = FakeWebSocketApp

        read = {'plugins': {'internal': copy.deepcopy(PLUGIN_CANONICAL_THEN)}}
        program = self.create_program(read, pins=PINS_INTERNAL)
        program._connect()
        program.ws.send('{"type":"message","channel":"ABC","text":"foo"}')

        mock_recv.assert_called_once_with(
            '{"type":"message","channel":"ABC","text":"foo"}')
        mock_thread.assert_called_once_with(target=program.ws.run_forever)
        self.assertTrue(mock_thread.return_value.daemon)
        mock_thread.return_value.start.assert_called_once_with()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(program._plugin('internal'), PLUGIN_CANONICAL_THEN)
        self.assertIsNotNone(program.ws)

    @mock.patch('programs.fairylab.fairylab_program.websocket.WebSocketApp')
    @mock.patch('programs.fairylab.fairylab_program.threading.Thread')
    @mock.patch('programs.fairylab.fairylab_program.rtm_connect')
    @mock.patch.object(FairylabProgram, '_recv')
    def test_connect__with_error(self, mock_recv, mock_rtm, mock_thread,
                                 mock_ws):
        mock_rtm.return_value = {'ok': False}
        mock_ws.side_effect = FakeWebSocketApp

        read = {'plugins': {'internal': copy.deepcopy(PLUGIN_CANONICAL_THEN)}}
        program = self.create_program(read, pins=PINS_INTERNAL)
        program._connect()

        mock_recv.assert_not_called()
        mock_thread.assert_not_called()
        mock_thread.return_value.start.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(program._plugin('internal'), PLUGIN_CANONICAL_THEN)
        self.assertIsNone(program.ws)

    @mock.patch.object(FairylabProgram, '_try')
    @mock.patch('programs.fairylab.fairylab_program.time.sleep')
    @mock.patch.object(FairylabProgram, '_render')
    @mock.patch.object(FairylabProgram, '_connect')
    def test_start__with_valid_input(self, mock_connect, mock_render,
                                     mock_sleep, mock_try):
        read = {'plugins': {'internal': copy.deepcopy(PLUGIN_CANONICAL_THEN)}}
        program = self.create_program(read, pins=PINS_INTERNAL)

        mock_sleep.side_effect = functools.partial(set_running_false, program)
        mock_try.side_effect = functools.partial(set_date_now, program)
        program._start()

        write = {'plugins': {'internal': copy.deepcopy(PLUGIN_CANONICAL_NOW)}}
        mock_connect.assert_called_once_with()
        mock_sleep.assert_called_once_with(120)
        mock_try.assert_called_once_with('internal', '_run', date=THEN)
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_datetime.datetime.now.assert_called_once_with()
        self.mock_log.assert_not_called()
        self.assertEqual(program._plugin('internal'), PLUGIN_CANONICAL_NOW)

    @mock.patch.object(FairylabProgram, '_try')
    @mock.patch('programs.fairylab.fairylab_program.time.sleep')
    @mock.patch.object(FairylabProgram, '_render')
    @mock.patch.object(FairylabProgram, '_connect')
    def test_start__with_no_change(self, mock_connect, mock_render, mock_sleep,
                                   mock_try):
        read = {'plugins': {'internal': copy.deepcopy(PLUGIN_CANONICAL_THEN)}}
        program = self.create_program(read, pins=PINS_INTERNAL)

        mock_sleep.side_effect = functools.partial(set_running_false, program)
        program._start()

        mock_connect.assert_called_once_with()
        mock_sleep.assert_called_once_with(120)
        mock_try.assert_called_once_with('internal', '_run', date=THEN)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_called_once_with()
        self.mock_log.assert_not_called()
        self.assertEqual(program._plugin('internal'), PLUGIN_CANONICAL_THEN)

    @mock.patch('programs.fairylab.fairylab_program.delta')
    def test_home__with_valid_input(self, mock_delta):
        mock_delta.side_effect = ['2m ago', '2h ago']

        read = {
            'plugins': {
                k: copy.deepcopy(PLUGIN_CANONICAL_THEN)
                for k in ['browsable', 'internal']
            }
        }
        program = self.create_program(read, pins=PINS_BOTH)
        ret = program._home(date=NOW)
        browsable = card(
            href='/fairylab/browsable/',
            title='browsable',
            info='Description of browsable.',
            ts='2m ago')
        internal = card(
            title='internal', info='Description of internal.', ts='2h ago')
        expected = {
            'breadcrumbs': BREADCRUMBS,
            'browsable': [browsable],
            'internal': [internal],
        }
        self.assertEqual(ret, expected)

    @mock.patch('programs.fairylab.fairylab_program.delta')
    def test_home__with_success(self, mock_delta):
        mock_delta.return_value = '0s ago'

        read = {'plugins': {'internal': copy.deepcopy(PLUGIN_CANONICAL_THEN)}}
        program = self.create_program(read, pins=PINS_INTERNAL)
        ret = program._home(date=THEN)
        internal = card(
            title='internal',
            info='Description of internal.',
            ts='0s ago',
            success='just now')
        expected = {
            'breadcrumbs': BREADCRUMBS,
            'browsable': [],
            'internal': [internal],
        }
        self.assertEqual(ret, expected)

    @mock.patch('programs.fairylab.fairylab_program.delta')
    def test_home__with_danger(self, mock_delta):
        mock_delta.return_value = '2m ago'

        read = {'plugins': {'internal': copy.deepcopy(PLUGIN_CANONICAL_ERROR)}}
        program = self.create_program(read, pins=PINS_INTERNAL)
        ret = program._home(date=NOW)
        internal = card(
            title='internal',
            info='Description of internal.',
            ts='2m ago',
            danger='error')
        expected = {
            'breadcrumbs': BREADCRUMBS,
            'browsable': [],
            'internal': [internal],
        }
        self.assertEqual(ret, expected)

    @mock.patch.object(FairylabProgram, 'uninstall')
    @mock.patch.object(FairylabProgram, '_try')
    @mock.patch('programs.fairylab.fairylab_program.importlib.import_module')
    @mock.patch('programs.fairylab.fairylab_program.getattr')
    def test_install__with_valid_input(self, mock_getattr, mock_import,
                                       mock_try, mock_uninstall):
        mock_getattr.return_value = InternalPlugin

        read = {'plugins': {}}
        program = self.create_program(read)
        program.install(a1='internal', date=THEN)

        write = {'plugins': {'internal': copy.deepcopy(PLUGIN_CANONICAL_THEN)}}
        module = mock_import.return_value
        mock_getattr.assert_called_once_with(module, 'InternalPlugin')
        mock_import.assert_called_once_with('plugins.internal.internal_plugin')
        mock_try.assert_called_once_with('internal', '_setup', date=THEN)
        mock_uninstall.assert_called_once_with(
            a1='internal', date=THEN, v=False)
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_called_once_with(
            'InternalPlugin', a1='internal', date=THEN, s='Installed.', v=True)
        self.assertEqual(program._plugin('internal'), PLUGIN_CANONICAL_THEN)

    @mock.patch.object(FairylabProgram, 'uninstall')
    @mock.patch.object(FairylabProgram, '_try')
    @mock.patch('programs.fairylab.fairylab_program.importlib.import_module')
    @mock.patch('programs.fairylab.fairylab_program.getattr')
    def test_install__without_date(self, mock_getattr, mock_import, mock_try,
                                   mock_uninstall):
        mock_getattr.return_value = InternalPlugin

        read = {'plugins': {}}
        program = self.create_program(read)
        program.install(a1='internal', v=True)

        write = {'plugins': {'internal': copy.deepcopy(PLUGIN_CANONICAL_THEN)}}
        module = mock_import.return_value
        mock_getattr.assert_called_once_with(module, 'InternalPlugin')
        mock_import.assert_called_once_with('plugins.internal.internal_plugin')
        mock_try.assert_called_once_with('internal', '_setup', date=THEN)
        mock_uninstall.assert_called_once_with(a1='internal', v=False)
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_datetime.datetime.now.assert_called_once_with()
        self.mock_log.assert_called_once_with(
            'InternalPlugin', a1='internal', s='Installed.', v=True)
        self.assertEqual(program._plugin('internal'), PLUGIN_CANONICAL_THEN)

    @mock.patch.object(FairylabProgram, 'uninstall')
    @mock.patch.object(FairylabProgram, '_try')
    @mock.patch('programs.fairylab.fairylab_program.importlib.import_module')
    @mock.patch('programs.fairylab.fairylab_program.getattr')
    def test_install__with_thrown_exception(self, mock_getattr, mock_import,
                                            mock_try, mock_uninstall):
        mock_getattr.side_effect = Exception()

        read = {'plugins': {}}
        program = self.create_program(read)
        program.install(a1='internal', date=THEN)

        module = mock_import.return_value
        mock_getattr.assert_called_once_with(module, 'InternalPlugin')
        mock_import.assert_called_once_with('plugins.internal.internal_plugin')
        mock_try.assert_not_called()
        mock_uninstall.assert_called_once_with(
            a1='internal', date=THEN, v=False)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_called_once_with(
            'InternalPlugin',
            a1='internal',
            c=TRACEBACK,
            date=THEN,
            s='Exception.',
            v=True)
        self.assertEqual(program.data, read)

    @mock.patch.object(FairylabProgram, 'uninstall')
    @mock.patch.object(FairylabProgram, '_try')
    @mock.patch('programs.fairylab.fairylab_program.importlib.import_module')
    @mock.patch('programs.fairylab.fairylab_program.getattr')
    def test_install__with_disabled_plugin(self, mock_getattr, mock_import,
                                           mock_try, mock_uninstall):
        mock_getattr.return_value = DisabledPlugin

        read = {'plugins': {}}
        program = self.create_program(read)
        program.install(a1='disabled', date=THEN)

        module = mock_import.return_value
        mock_getattr.assert_called_once_with(module, 'DisabledPlugin')
        mock_import.assert_called_once_with('plugins.disabled.disabled_plugin')
        mock_try.assert_not_called()
        mock_uninstall.assert_called_once_with(
            a1='disabled', date=THEN, v=False)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_called_once_with(
            'DisabledPlugin', a1='disabled', date=THEN, s='Disabled.', v=True)
        self.assertEqual(program.data, read)

    @mock.patch.dict('programs.fairylab.fairylab_program.sys.modules', MODULES)
    def test_uninstall__with_valid_input(self):
        read = {'plugins': {'internal': copy.deepcopy(PLUGIN_CANONICAL_THEN)}}
        program = self.create_program(read, pins=PINS_INTERNAL)
        program.uninstall(a1='internal')

        write = {'plugins': {}}
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_called_once_with(
            'InternalPlugin', a1='internal', s='Uninstalled.')
        self.assertEqual(program.data, write)

    def test_uninstall__with_plugin_not_found(self):
        read = {'plugins': {}}
        program = self.create_program(read)
        program.uninstall(a1='internal')

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_called_once_with(
            'InternalPlugin', a1='internal', s='Not found.')
        self.assertEqual(program.data, read)

    @mock.patch('programs.fairylab.fairylab_program.os.execv')
    def test_reboot(self, mock_execv):
        read = {'plugins': {}}
        program = self.create_program(read)
        program.reboot()

        expected = ['python'] + sys.argv
        mock_execv.assert_called_once_with(sys.executable, expected)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_called_once_with(
            'FairylabProgram', s='Rebooting.', v=True)

    def test_shutdown(self):
        read = {'plugins': {}}
        program = self.create_program(read)
        program.shutdown()

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_called_once_with(
            'FairylabProgram', s='Shutting down.', v=True)
        self.assertFalse(program.keep_running)


if __name__ in ['__main__', 'programs.fairylab.fairylab_program_test']:
    _main = __name__ == '__main__'
    _pkg = 'programs.fairylab'
    _pth = 'programs/fairylab'
    _read = {'plugins': {'internal': copy.deepcopy(PLUGIN_CANONICAL_THEN)}}
    main(FairylabProgramTest, FairylabProgram, _pkg, _pth, _read, _main)
