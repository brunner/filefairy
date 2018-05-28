#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import datetime
import functools
import os
import re
import sys
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(_path)
_root = re.sub(r'/core/fairylab', '', _path)
sys.path.append(_root)
from api.plugin.plugin import Plugin  # noqa
from api.renderable.renderable import Renderable  # noqa
from core.dashboard.dashboard import Dashboard  # noqa
from core.fairylab.fairylab import Fairylab  # noqa
from core.notify.notify import Notify  # noqa
from core.response.response import Response  # noqa
from core.shadow.shadow import Shadow  # noqa
from core.task.task import Task  # noqa
from util.component.component import card  # noqa
from util.json_.json_ import dumps  # noqa
from util.jinja2_.jinja2_ import env  # noqa
from util.test.test import Test  # noqa
from util.test.test import main  # noqa


class Browsable(Plugin, Renderable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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

    def _notify_internal(self, **kwargs):
        pass

    def _on_message_internal(self, **kwargs):
        return Response(notify=[Notify.BASE])

    def _run_internal(self, **kwargs):
        return Response(notify=[Notify.BASE])

    def _render_internal(self, **kwargs):
        return [('html/fairylab/browsable/index.html', '', 'browse.html', {})]

    def _setup_internal(self, **kwargs):
        pass

    def _shadow_internal(self, **kwargs):
        return []


class Internal(Plugin):
    var = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def enabled(self):
        return True

    @staticmethod
    def _info():
        return 'Description of internal.'

    def _notify_internal(self, **kwargs):
        pass

    def _on_message_internal(self, **kwargs):
        return Response(notify=[Notify.BASE])

    def _run_internal(self, **kwargs):
        return Response(notify=[Notify.BASE])

    def _setup_internal(self, **kwargs):
        pass

    def _shadow_internal(self, **kwargs):
        return []


class Disabled(Plugin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def enabled(self):
        return False

    @staticmethod
    def _info():
        return 'Description of disabled.'

    def _notify_internal(self, **kwargs):
        pass

    def _on_message_internal(self, **kwargs):
        return Response(notify=[Notify.BASE])

    def _run_internal(self, **kwargs):
        return Response(notify=[Notify.BASE])

    def _setup_internal(self, **kwargs):
        pass

    def _shadow_internal(self, **kwargs):
        return []


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


DATA = Fairylab._data()
NOW = datetime.datetime(1985, 10, 26, 0, 2, 30)
NOW_ENCODED = '1985-10-26T00:02:30'
THEN = datetime.datetime(1985, 10, 25, 0, 0, 0)
THEN_ENCODED = '1985-10-25T00:00:00'
DIR_INTERNAL = os.path.join(_root, 'plugin', 'internal')
DIR_PLUGINS = os.path.join(_root, 'plugin')
HOME = {'breadcrumbs': [], 'browsable': [], 'internal': []}
INDEX = 'html/fairylab/index.html'
MODULES = {'plugin.internal.internal': None}
ENV = env()
BROWSABLE = Browsable(date=THEN, e=ENV)
DASHBOARD = Dashboard(date=THEN, e=ENV)
INTERNAL = Internal(date=THEN)
REGISTERED = {
    'browsable': BROWSABLE,
    'dashboard': DASHBOARD,
    'internal': INTERNAL
}
TRACEBACK = 'Traceback: ...'
BREADCRUMBS = [{'href': '', 'name': 'Home'}]


def set_date_now(program, *args, **kwargs):
    p = args[0]
    program.registered[p].date = NOW


def set_running_false(program, *args, **kwargs):
    program.keep_running = False


class FairylabTest(Test):
    def setUp(self):
        patch_open = mock.patch(
            'api.serializable.serializable.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

        patch_datetime = mock.patch('core.fairylab.fairylab.datetime')
        self.addCleanup(patch_datetime.stop)
        self.mock_datetime = patch_datetime.start()

        patch_log = mock.patch('core.fairylab.fairylab.log')
        self.addCleanup(patch_log.stop)
        self.mock_log = patch_log.start()

        patch_traceback = mock.patch(
            'core.fairylab.fairylab.traceback.format_exc')
        self.addCleanup(patch_traceback.stop)
        self.mock_traceback = patch_traceback.start()

        for p in REGISTERED:
            REGISTERED[p].date = THEN
            REGISTERED[p].ok = True

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]
        self.mock_datetime.datetime.now.return_value = NOW
        self.mock_traceback.return_value = TRACEBACK

    def reset_mocks(self):
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()
        self.mock_datetime.reset_mock()
        self.mock_log.reset_mock()
        self.mock_traceback.reset_mock()

    def create_program(self, registered=None, tasks=None):
        self.init_mocks({})
        program = Fairylab(d=DASHBOARD, e=ENV)
        program.day = NOW.day

        self.mock_open.assert_called_once_with(DATA, 'r')
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_traceback.assert_not_called()
        self.assertEqual(program.data, {})

        self.reset_mocks()
        self.init_mocks({})

        if registered:
            program.registered = registered

        if tasks:
            program.tasks = tasks

        return program

    def test_init(self):
        program = self.create_program()

        self.assertEqual(program.data, {})
        self.assertEqual(program.day, NOW.day)
        self.assertEqual(program.registered, {'dashboard': DASHBOARD})
        self.assertTrue(program.keep_running)
        self.assertEqual(program.sleep, 120)
        self.assertEqual(program.ws, None)

    @mock.patch.object(Fairylab, '_try')
    @mock.patch.object(Fairylab, '_reload_internal')
    @mock.patch('core.fairylab.fairylab.os.listdir')
    @mock.patch('core.fairylab.fairylab.os.path.isdir')
    def test_setup(self, mock_isdir, mock_listdir, mock_reload, mock_try):
        mock_isdir.return_value = True
        mock_listdir.return_value = ['internal']

        program = self.create_program(registered=REGISTERED)
        program.day = THEN.day
        program._setup()

        calls = [mock.call('plugin', 'internal', date=NOW, v=True)]
        mock_reload.assert_has_calls(calls)
        calls = [mock.call(DIR_INTERNAL)]
        mock_isdir.assert_has_calls(calls)
        mock_listdir.assert_called_once_with(DIR_PLUGINS)
        mock_try.assert_has_calls(
            [mock.call('internal', '_setup', date=NOW, v=True)])
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_called_once_with()
        self.mock_log.assert_called_once_with(
            'Fairylab', s='Completed setup.', date=NOW, v=True)
        self.assertEqual(program.day, NOW.day)
        self.assertEqual(program.registered['browsable'].date, THEN)
        self.assertEqual(program.registered['browsable'].ok, True)
        self.assertEqual(program.registered['dashboard'].date, THEN)
        self.assertEqual(program.registered['dashboard'].ok, True)
        self.assertEqual(program.registered['internal'].date, THEN)
        self.assertEqual(program.registered['internal'].ok, True)

    @mock.patch.object(Fairylab, '_home')
    def test_render(self, mock_home):
        mock_home.return_value = HOME

        program = self.create_program(registered=REGISTERED)
        ret = program._render_internal(date=NOW)
        self.assertEqual(ret, [(INDEX, '', 'home.html', HOME)])

        mock_home.assert_called_once_with(date=NOW)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(program.registered['browsable'].date, THEN)
        self.assertEqual(program.registered['browsable'].ok, True)
        self.assertEqual(program.registered['dashboard'].date, THEN)
        self.assertEqual(program.registered['dashboard'].ok, True)
        self.assertEqual(program.registered['internal'].date, THEN)
        self.assertEqual(program.registered['internal'].ok, True)

    def test_package(self):
        actual = Fairylab._package('plugin', 'internal')
        expected = 'plugin.internal.internal'
        self.assertEqual(actual, expected)

    @mock.patch.object(Internal, '_run_internal')
    @mock.patch.object(Internal, '_notify')
    @mock.patch.object(Browsable, '_notify')
    def test_try__with_valid_input(self, mock_bnotify, mock_inotify, mock_run):
        mock_run.return_value = Response(notify=[Notify.BASE])

        program = self.create_program(registered=REGISTERED)
        program._try('internal', '_run_internal', date=NOW)

        mock_bnotify.assert_not_called()
        mock_inotify.assert_not_called()
        mock_run.assert_called_once_with(date=NOW)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(program.registered['browsable'].date, THEN)
        self.assertEqual(program.registered['browsable'].ok, True)
        self.assertEqual(program.registered['dashboard'].date, THEN)
        self.assertEqual(program.registered['dashboard'].ok, True)
        self.assertEqual(program.registered['internal'].date, NOW)
        self.assertEqual(program.registered['internal'].ok, True)

    @mock.patch.object(Internal, '_run_internal')
    @mock.patch.object(Internal, '_notify')
    @mock.patch.object(Browsable, '_notify')
    def test_try__with_notify(self, mock_bnotify, mock_inotify, mock_run):
        mock_bnotify.return_value = Response()
        mock_run.return_value = Response(notify=[Notify.OTHER])

        program = self.create_program(registered=REGISTERED)
        program._try('internal', '_run_internal', date=NOW)

        mock_bnotify.assert_called_once_with(notify=Notify.OTHER, date=NOW)
        mock_inotify.assert_called_once_with(notify=Notify.OTHER, date=NOW)
        mock_run.assert_called_once_with(date=NOW)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(program.registered['browsable'].date, THEN)
        self.assertEqual(program.registered['browsable'].ok, True)
        self.assertEqual(program.registered['dashboard'].date, THEN)
        self.assertEqual(program.registered['dashboard'].ok, True)
        self.assertEqual(program.registered['internal'].date, NOW)
        self.assertEqual(program.registered['internal'].ok, True)
        self.assertEqual(program.tasks, [])

    @mock.patch.object(Internal, '_run_internal')
    @mock.patch.object(Internal, '_shadow')
    @mock.patch.object(Internal, '_notify')
    @mock.patch.object(Browsable, '_shadow')
    @mock.patch.object(Browsable, '_notify')
    def test_try__with_shadow(self, mock_bnotify, mock_bshadow, mock_inotify,
                              mock_ishadow, mock_run):
        shadow = Shadow(destination='browsable', key='internal.foo')
        mock_bshadow.return_value = Response()
        mock_run.return_value = Response(shadow=[shadow])

        program = self.create_program(registered=REGISTERED)
        program._try('internal', '_run_internal', date=NOW)

        mock_bnotify.assert_not_called()
        mock_bshadow.assert_called_once_with(shadow=shadow, date=NOW)
        mock_inotify.assert_not_called()
        mock_ishadow.assert_not_called()
        mock_run.assert_called_once_with(date=NOW)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(program.registered['browsable'].date, THEN)
        self.assertEqual(program.registered['browsable'].ok, True)
        self.assertEqual(program.registered['dashboard'].date, THEN)
        self.assertEqual(program.registered['dashboard'].ok, True)
        self.assertEqual(program.registered['internal'].date, THEN)
        self.assertEqual(program.registered['internal'].ok, True)
        self.assertEqual(program.tasks, [])

    @mock.patch.object(Internal, '_run_internal')
    @mock.patch.object(Internal, '_notify')
    @mock.patch.object(Browsable, '_notify')
    def test_try__with_task(self, mock_bnotify, mock_inotify, mock_run):
        mock_run.return_value = Response(task=[Task(target='foo')])

        program = self.create_program(registered=REGISTERED)
        program._try('internal', '_run_internal', date=NOW)

        mock_bnotify.assert_not_called()
        mock_inotify.assert_not_called()
        mock_run.assert_called_once_with(date=NOW)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(program.registered['browsable'].date, THEN)
        self.assertEqual(program.registered['browsable'].ok, True)
        self.assertEqual(program.registered['dashboard'].date, THEN)
        self.assertEqual(program.registered['dashboard'].ok, True)
        self.assertEqual(program.registered['internal'].date, THEN)
        self.assertEqual(program.registered['internal'].ok, True)
        self.assertEqual(program.tasks, [('internal', Task(target='foo'))])

    @mock.patch.object(Internal, '_run_internal')
    @mock.patch.object(Internal, '_notify')
    @mock.patch.object(Browsable, '_notify')
    def test_try__with_no_change(self, mock_bnotify, mock_inotify, mock_run):
        mock_run.return_value = Response()

        program = self.create_program(registered=REGISTERED)
        program._try('internal', '_run_internal', date=NOW)

        mock_bnotify.assert_not_called()
        mock_inotify.assert_not_called()
        mock_run.assert_called_once_with(date=NOW)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(program.registered['browsable'].date, THEN)
        self.assertEqual(program.registered['browsable'].ok, True)
        self.assertEqual(program.registered['dashboard'].date, THEN)
        self.assertEqual(program.registered['dashboard'].ok, True)
        self.assertEqual(program.registered['internal'].date, THEN)
        self.assertEqual(program.registered['internal'].ok, True)
        self.assertEqual(program.tasks, [])

    @mock.patch.object(Internal, '_run_internal')
    @mock.patch.object(Internal, '_notify')
    @mock.patch.object(Browsable, '_notify')
    def test_try__without_date(self, mock_bnotify, mock_inotify, mock_run):
        mock_run.return_value = Response(notify=[Notify.BASE])

        program = self.create_program(registered=REGISTERED)
        program._try('internal', '_run_internal')

        mock_bnotify.assert_not_called()
        mock_inotify.assert_not_called()
        mock_run.assert_called_once_with(date=NOW)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_called_once_with()
        self.mock_log.assert_not_called()
        self.assertEqual(program.registered['browsable'].date, THEN)
        self.assertEqual(program.registered['browsable'].ok, True)
        self.assertEqual(program.registered['dashboard'].date, THEN)
        self.assertEqual(program.registered['dashboard'].ok, True)
        self.assertEqual(program.registered['internal'].date, NOW)
        self.assertEqual(program.registered['internal'].ok, True)
        self.assertEqual(program.tasks, [])

    @mock.patch.object(Internal, '_run_internal')
    @mock.patch.object(Internal, '_notify')
    @mock.patch.object(Browsable, '_notify')
    def test_try__with_thrown_exception(self, mock_bnotify, mock_inotify,
                                        mock_run):
        mock_run.side_effect = Exception()

        program = self.create_program(registered=REGISTERED)
        program._try('internal', '_run_internal', date=NOW)

        mock_bnotify.assert_not_called()
        mock_inotify.assert_not_called()
        mock_run.assert_called_once_with(date=NOW)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_called_once_with(
            'Internal', c='Traceback: ...', s='Exception.', v=True)
        self.assertEqual(program.registered['browsable'].date, THEN)
        self.assertEqual(program.registered['browsable'].ok, True)
        self.assertEqual(program.registered['dashboard'].date, THEN)
        self.assertEqual(program.registered['dashboard'].ok, True)
        self.assertEqual(program.registered['internal'].date, NOW)
        self.assertEqual(program.registered['internal'].ok, False)
        self.assertEqual(program.tasks, [])

    @mock.patch.object(Internal, '_run_internal')
    @mock.patch.object(Internal, '_notify')
    @mock.patch.object(Browsable, '_notify')
    def test_try__with_plugin_error(self, mock_bnotify, mock_inotify,
                                    mock_run):
        program = self.create_program(registered=REGISTERED)
        program.registered['internal'].ok = False
        program._try('internal', '_run_internal', date=NOW)

        mock_bnotify.assert_not_called()
        mock_inotify.assert_not_called()
        mock_run.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(program.registered['browsable'].date, THEN)
        self.assertEqual(program.registered['browsable'].ok, True)
        self.assertEqual(program.registered['dashboard'].date, THEN)
        self.assertEqual(program.registered['dashboard'].ok, True)
        self.assertEqual(program.registered['internal'].date, THEN)
        self.assertEqual(program.registered['internal'].ok, False)
        self.assertEqual(program.tasks, [])

    @mock.patch.object(Internal, '_run_internal')
    @mock.patch.object(Internal, '_notify')
    @mock.patch.object(Browsable, '_notify')
    def test_try__with_plugin_not_found(self, mock_bnotify, mock_inotify,
                                        mock_run):
        program = self.create_program(registered=REGISTERED)
        program._try('foo', '_run_internal', date=NOW)

        mock_bnotify.assert_not_called()
        mock_inotify.assert_not_called()
        mock_run.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(program.registered['browsable'].date, THEN)
        self.assertEqual(program.registered['browsable'].ok, True)
        self.assertEqual(program.registered['dashboard'].date, THEN)
        self.assertEqual(program.registered['dashboard'].ok, True)
        self.assertEqual(program.registered['internal'].date, THEN)
        self.assertEqual(program.registered['internal'].ok, True)
        self.assertEqual(program.tasks, [])

    @mock.patch.object(Internal, '_notify')
    @mock.patch.object(Browsable, '_notify')
    def test_try__with_item_not_found(self, mock_bnotify, mock_inotify):
        program = self.create_program(registered=REGISTERED)
        program._try('internal', '_foo', date=NOW)

        mock_bnotify.assert_not_called()
        mock_inotify.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(program.registered['browsable'].date, THEN)
        self.assertEqual(program.registered['browsable'].ok, True)
        self.assertEqual(program.registered['dashboard'].date, THEN)
        self.assertEqual(program.registered['dashboard'].ok, True)
        self.assertEqual(program.registered['internal'].date, THEN)
        self.assertEqual(program.registered['internal'].ok, True)
        self.assertEqual(program.tasks, [])

    @mock.patch.object(Internal, '_notify')
    @mock.patch.object(Browsable, '_notify')
    def test_try__with_item_not_callable(self, mock_bnotify, mock_inotify):
        program = self.create_program(registered=REGISTERED)
        program._try('internal', 'var', date=NOW)

        mock_bnotify.assert_not_called()
        mock_inotify.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(program.registered['browsable'].date, THEN)
        self.assertEqual(program.registered['browsable'].ok, True)
        self.assertEqual(program.registered['dashboard'].date, THEN)
        self.assertEqual(program.registered['dashboard'].ok, True)
        self.assertEqual(program.registered['internal'].date, THEN)
        self.assertEqual(program.registered['internal'].ok, True)
        self.assertEqual(program.tasks, [])

    @mock.patch.object(Fairylab, '_try')
    @mock.patch('core.fairylab.fairylab.time.sleep')
    def test_background(self, mock_sleep, mock_try):
        args = (True, False)
        kwargs = {'key': 'value'}
        task = Task(target='foo', args=args, kwargs=kwargs)
        program = self.create_program(
            registered=REGISTERED, tasks=[('internal', task)])

        mock_sleep.side_effect = functools.partial(set_running_false, program)
        program._background()

        mock_sleep.assert_called_once_with(120)
        mock_try.assert_called_once_with('internal', 'foo', *args, **kwargs)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(program.tasks, [])

    @mock.patch.object(Fairylab, '_try')
    @mock.patch.object(Fairylab, '_on_message')
    def test_recv__with_valid_input(self, mock_message, mock_try):
        program = self.create_program(registered=REGISTERED)

        mock_try.side_effect = functools.partial(set_date_now, program)
        program._recv('{"type":"message","channel":"ABC","text":"foo"}')

        obj = {'type': 'message', 'channel': 'ABC', 'text': 'foo'}
        mock_message.assert_called_once_with(obj=obj, date=NOW)
        calls = [
            mock.call('browsable', '_on_message', obj=obj, date=NOW),
            mock.call('dashboard', '_on_message', obj=obj, date=NOW),
            mock.call('internal', '_on_message', obj=obj, date=NOW),
        ]
        mock_try.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_called_once_with()
        self.mock_log.assert_not_called()

    @mock.patch.object(Fairylab, '_try')
    @mock.patch.object(Fairylab, '_on_message')
    def test_recv__with_no_change(self, mock_message, mock_try):
        program = self.create_program(registered=REGISTERED)
        program._recv('{"type":"message","channel":"ABC","text":"foo"}')

        obj = {'type': 'message', 'channel': 'ABC', 'text': 'foo'}
        mock_message.assert_called_once_with(obj=obj, date=NOW)
        calls = [
            mock.call('browsable', '_on_message', obj=obj, date=NOW),
            mock.call('dashboard', '_on_message', obj=obj, date=NOW),
            mock.call('internal', '_on_message', obj=obj, date=NOW),
        ]
        mock_try.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_called_once_with()
        self.mock_log.assert_not_called()

    @mock.patch('core.fairylab.fairylab.websocket.WebSocketApp')
    @mock.patch('core.fairylab.fairylab.threading.Thread')
    @mock.patch('core.fairylab.fairylab.rtm_connect')
    @mock.patch.object(Fairylab, '_recv')
    def test_connect__with_valid_input(self, mock_recv, mock_rtm, mock_thread,
                                       mock_ws):
        mock_rtm.return_value = {'ok': True, 'url': 'wss://...'}
        mock_ws.side_effect = FakeWebSocketApp

        program = self.create_program(registered=REGISTERED)
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
        self.assertIsNotNone(program.ws)

    @mock.patch('core.fairylab.fairylab.websocket.WebSocketApp')
    @mock.patch('core.fairylab.fairylab.threading.Thread')
    @mock.patch('core.fairylab.fairylab.rtm_connect')
    @mock.patch.object(Fairylab, '_recv')
    def test_connect__with_error(self, mock_recv, mock_rtm, mock_thread,
                                 mock_ws):
        mock_rtm.return_value = {'ok': False}
        mock_ws.side_effect = FakeWebSocketApp

        program = self.create_program(registered=REGISTERED)
        program._connect()

        mock_recv.assert_not_called()
        mock_thread.assert_not_called()
        mock_thread.return_value.start.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertIsNone(program.ws)

    @mock.patch.object(Fairylab, '_try')
    @mock.patch('core.fairylab.fairylab.threading.Thread')
    @mock.patch('core.fairylab.fairylab.time.sleep')
    @mock.patch.object(Fairylab, '_render')
    @mock.patch.object(Fairylab, '_connect')
    @mock.patch.object(Fairylab, '_background')
    def test_start__with_valid_input(self, mock_bg, mock_connect, mock_render,
                                     mock_sleep, mock_thread, mock_try):
        program = self.create_program(registered=REGISTERED)

        mock_sleep.side_effect = functools.partial(set_running_false, program)
        mock_try.side_effect = functools.partial(set_date_now, program)
        program._start()

        mock_connect.assert_called_once_with()
        mock_sleep.assert_called_once_with(120)
        mock_thread.assert_called_once_with(target=mock_bg)
        mock_thread.return_value.start.assert_called_once_with()
        calls = [
            mock.call('browsable', '_run', date=NOW),
            mock.call('dashboard', '_run', date=NOW),
            mock.call('internal', '_run', date=NOW),
        ]
        mock_try.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_called_once_with()
        self.mock_log.assert_not_called()
        self.assertEqual(program.registered['browsable'].date, NOW)
        self.assertEqual(program.registered['dashboard'].date, NOW)
        self.assertEqual(program.registered['internal'].date, NOW)

    @mock.patch.object(Fairylab, '_try')
    @mock.patch('core.fairylab.fairylab.threading.Thread')
    @mock.patch('core.fairylab.fairylab.time.sleep')
    @mock.patch.object(Fairylab, '_render')
    @mock.patch.object(Fairylab, '_connect')
    @mock.patch.object(Fairylab, '_background')
    def test_start__with_date_change(self, mock_bg, mock_connect, mock_render,
                                     mock_sleep, mock_thread, mock_try):
        program = self.create_program(registered=REGISTERED)
        program.day = THEN.day

        mock_sleep.side_effect = functools.partial(set_running_false, program)
        program._start()

        mock_connect.assert_called_once_with()
        mock_sleep.assert_called_once_with(120)
        mock_thread.assert_called_once_with(target=mock_bg)
        mock_thread.return_value.start.assert_called_once_with()
        calls = [
            mock.call('browsable', '_run', date=NOW),
            mock.call('dashboard', '_run', date=NOW),
            mock.call('internal', '_run', date=NOW),
            mock.call('browsable', '_notify', notify=Notify.FAIRYLAB_DAY),
            mock.call('dashboard', '_notify', notify=Notify.FAIRYLAB_DAY),
            mock.call('internal', '_notify', notify=Notify.FAIRYLAB_DAY),
        ]
        mock_try.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_called_once_with()
        self.mock_log.assert_not_called()
        self.assertEqual(program.registered['browsable'].date, THEN)
        self.assertEqual(program.registered['dashboard'].date, THEN)
        self.assertEqual(program.registered['internal'].date, THEN)

    @mock.patch.object(Fairylab, '_try')
    @mock.patch('core.fairylab.fairylab.threading.Thread')
    @mock.patch('core.fairylab.fairylab.time.sleep')
    @mock.patch.object(Fairylab, '_render')
    @mock.patch.object(Fairylab, '_connect')
    @mock.patch.object(Fairylab, '_background')
    def test_start__with_no_change(self, mock_bg, mock_connect, mock_render,
                                   mock_sleep, mock_thread, mock_try):
        program = self.create_program(registered=REGISTERED)

        mock_sleep.side_effect = functools.partial(set_running_false, program)
        program._start()

        mock_connect.assert_called_once_with()
        mock_sleep.assert_called_once_with(120)
        mock_thread.assert_called_once_with(target=mock_bg)
        mock_thread.return_value.start.assert_called_once_with()
        mock_try.assert_has_calls([mock.call('internal', '_run', date=NOW)])
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_called_once_with()
        self.mock_log.assert_not_called()
        self.assertEqual(program.registered['browsable'].date, THEN)
        self.assertEqual(program.registered['dashboard'].date, THEN)
        self.assertEqual(program.registered['internal'].date, THEN)

    @mock.patch('core.fairylab.fairylab.delta')
    def test_home__with_valid_input(self, mock_delta):
        mock_delta.side_effect = ['2m ago', '15m ago', '2h ago']

        program = self.create_program(registered=REGISTERED)
        ret = program._home(date=NOW)
        browsable = card(
            href='/fairylab/browsable/',
            title='browsable',
            info='Description of browsable.',
            ts='2m ago')
        dashboard = card(
            href='/fairylab/dashboard/',
            title='dashboard',
            info='Tails exceptions and log messages.',
            ts='15m ago')
        internal = card(
            title='internal', info='Description of internal.', ts='2h ago')
        expected = {
            'breadcrumbs': BREADCRUMBS,
            'browsable': [browsable, dashboard],
            'internal': [internal],
        }
        self.assertEqual(ret, expected)

    maxDiff = None
    @mock.patch('core.fairylab.fairylab.delta')
    def test_home__with_success(self, mock_delta):
        mock_delta.side_effect = ['0s ago', '15m ago', '2h ago']

        program = self.create_program(registered=REGISTERED)
        ret = program._home(date=THEN)
        browsable = card(
            href='/fairylab/browsable/',
            title='browsable',
            info='Description of browsable.',
            ts='0s ago',
            success='just now')
        dashboard = card(
            href='/fairylab/dashboard/',
            title='dashboard',
            info='Tails exceptions and log messages.',
            ts='15m ago')
        internal = card(
            title='internal', info='Description of internal.', ts='2h ago')
        expected = {
            'breadcrumbs': BREADCRUMBS,
            'browsable': [browsable, dashboard],
            'internal': [internal],
        }
        self.assertEqual(ret, expected)

    @mock.patch('core.fairylab.fairylab.delta')
    def test_home__with_danger(self, mock_delta):
        mock_delta.side_effect = ['2m ago', '15m ago', '2h ago']

        program = self.create_program(registered=REGISTERED)
        program.registered['internal'].ok = False
        ret = program._home(date=NOW)
        browsable = card(
            href='/fairylab/browsable/',
            title='browsable',
            info='Description of browsable.',
            ts='2m ago')
        dashboard = card(
            href='/fairylab/dashboard/',
            title='dashboard',
            info='Tails exceptions and log messages.',
            ts='15m ago')
        internal = card(
            title='internal',
            info='Description of internal.',
            ts='2h ago',
            danger='error')
        expected = {
            'breadcrumbs': BREADCRUMBS,
            'browsable': [browsable, dashboard],
            'internal': [internal],
        }
        self.assertEqual(ret, expected)

    @mock.patch.object(Fairylab, '_try')
    @mock.patch('core.fairylab.fairylab.importlib.import_module')
    @mock.patch('core.fairylab.fairylab.getattr')
    def test_reload__with_valid_input(self, mock_getattr, mock_import,
                                      mock_try):
        mock_getattr.return_value = Internal

        args = ('plugin', 'internal')
        kwargs = {'date': THEN, 'v': True}
        program = self.create_program()
        program.reload(*args, **kwargs)

        module = mock_import.return_value
        mock_getattr.assert_called_once_with(module, 'Internal')
        mock_import.assert_called_once_with('plugin.internal.internal')
        calls = [
            mock.call('dashboard', '_setup', **dict(kwargs)),
            mock.call('internal', '_setup', **dict(kwargs)),
        ]
        mock_try.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        calls = [
            mock.call('Internal', **dict(kwargs, s='Installed.', c=None)),
            mock.call('Fairylab', **dict(kwargs, s='Completed setup.'))
        ]
        self.mock_log.assert_has_calls(calls)
        self.assertNotIn('browsable', program.registered)
        self.assertEqual(program.registered['dashboard'].date, THEN)
        self.assertEqual(program.registered['dashboard'].ok, True)
        self.assertEqual(program.registered['internal'].date, THEN)
        self.assertEqual(program.registered['internal'].ok, True)

    @mock.patch.object(Fairylab, '_try')
    @mock.patch('core.fairylab.fairylab.importlib.import_module')
    @mock.patch('core.fairylab.fairylab.getattr')
    def test_reload__with_thrown_exception(self, mock_getattr, mock_import,
                                           mock_try):
        mock_getattr.side_effect = Exception()

        args = ('plugin', 'internal')
        kwargs = {'date': THEN, 'v': True}
        program = self.create_program()
        program.reload(*args, **kwargs)

        module = mock_import.return_value
        mock_getattr.assert_called_once_with(module, 'Internal')
        mock_import.assert_called_once_with('plugin.internal.internal')
        mock_try.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_called_once_with('Internal',
                                              **dict(
                                                  kwargs,
                                                  c=TRACEBACK,
                                                  s='Exception.'))
        self.assertNotIn('browsable', program.registered)
        self.assertEqual(program.registered['dashboard'].date, THEN)
        self.assertEqual(program.registered['dashboard'].ok, True)
        self.assertNotIn('internal', program.registered)

    @mock.patch.object(Fairylab, '_try')
    @mock.patch('core.fairylab.fairylab.importlib.import_module')
    @mock.patch('core.fairylab.fairylab.getattr')
    def test_reload__with_disabled(self, mock_getattr, mock_import, mock_try):
        mock_getattr.return_value = Disabled

        args = ('plugin', 'disabled')
        kwargs = {'date': THEN, 'v': True}
        program = self.create_program()
        program.reload(*args, **kwargs)

        module = mock_import.return_value
        mock_getattr.assert_called_once_with(module, 'Disabled')
        mock_import.assert_called_once_with('plugin.disabled.disabled')
        mock_try.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_called_once_with('Disabled',
                                              **dict(
                                                  kwargs,
                                                  s='Disabled.',
                                                  c=None))
        self.assertNotIn('browsable', program.registered)
        self.assertEqual(program.registered['dashboard'].date, THEN)
        self.assertEqual(program.registered['dashboard'].ok, True)
        self.assertNotIn('internal', program.registered)

    @mock.patch('core.fairylab.fairylab.os.execv')
    def test_reboot(self, mock_execv):
        program = self.create_program()
        program.reboot(v=True)

        expected = ['python'] + sys.argv
        mock_execv.assert_called_once_with(sys.executable, expected)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_called_once_with(
            'Fairylab', s='Rebooting.', v=True)

    def test_shutdown(self):
        program = self.create_program()
        program.shutdown(v=True)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_called_once_with(
            'Fairylab', s='Shutting down.', v=True)
        self.assertFalse(program.keep_running)


if __name__ in ['__main__', 'core.fairylab.fairylab_test']:
    _main = __name__ == '__main__'
    _pkg = 'core.fairylab'
    _pth = 'core/fairylab'
    main(FairylabTest, Fairylab, _pkg, _pth, {}, _main, d=DASHBOARD, e=ENV)
