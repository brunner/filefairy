#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import functools
import logging
import os
import re
import sys
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(_path)
_root = re.sub(r'/core/fairylab', '', _path)
sys.path.append(_root)
from api.messageable.messageable import Messageable  # noqa
from api.registrable.registrable import Registrable  # noqa
from api.renderable.renderable import Renderable  # noqa
from api.runnable.runnable import Runnable  # noqa
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


class Browsable(Messageable, Registrable, Renderable, Runnable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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


class Internal(Messageable, Registrable, Runnable):
    var = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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


_env = env()
_now = datetime.datetime(1985, 10, 26, 0, 2, 30)
_then = datetime.datetime(1985, 10, 25, 0, 0, 0)

_dashboard = Dashboard(date=_then, e=_env)
_registered = {
    'browsable': Browsable(date=_then, e=_env),
    'dashboard': _dashboard,
    'internal': Internal(date=_then)
}


def set_date_now(program, *args, **kwargs):
    p = args[0]
    program.registered[p].date = _now


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

        patch_log = mock.patch('core.fairylab.fairylab.logger_.log')
        self.addCleanup(patch_log.stop)
        self.mock_log = patch_log.start()

        for p in _registered:
            _registered[p].date = _then
            _registered[p].ok = True

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]
        self.mock_datetime.datetime.now.return_value = _now

    def reset_mocks(self):
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()
        self.mock_datetime.reset_mock()
        self.mock_log.reset_mock()

    def create_program(self, registered=None, tasks=None):
        self.init_mocks({})
        program = Fairylab(d=_dashboard, e=_env)
        program.day = _now.day

        self.mock_open.assert_called_once_with(Fairylab._data(), 'r')
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()
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
        self.assertEqual(program.day, _now.day)
        self.assertEqual(program.registered, {'dashboard': _dashboard})
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

        program = self.create_program(registered=_registered)
        program.day = _then.day
        program._setup(date=_now)

        calls = [mock.call('plugin', 'internal', date=_now)]
        mock_reload.assert_has_calls(calls)
        dir_internal = os.path.join(_root, 'plugin', 'internal')
        mock_isdir.assert_called_once_with(dir_internal)
        dir_plugin = os.path.join(_root, 'plugin')
        mock_listdir.assert_called_once_with(dir_plugin)
        mock_try.assert_has_calls([
            mock.call('dashboard', 'resolve', 'dashboard', date=_now),
            mock.call('browsable', '_setup', date=_now),
            mock.call('dashboard', '_setup', date=_now),
            mock.call('internal', '_setup', date=_now)
        ])
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_called_once_with(logging.INFO, 'Completed setup.')
        self.assertEqual(program.day, _now.day)
        self.assertEqual(program.registered['browsable'].date, _then)
        self.assertEqual(program.registered['browsable'].ok, True)
        self.assertEqual(program.registered['dashboard'].date, _then)
        self.assertEqual(program.registered['dashboard'].ok, True)
        self.assertEqual(program.registered['internal'].date, _then)
        self.assertEqual(program.registered['internal'].ok, True)

    @mock.patch.object(Fairylab, '_home')
    def test_render(self, mock_home):
        home = {'breadcrumbs': [], 'browsable': [], 'internal': []}
        mock_home.return_value = home

        program = self.create_program(registered=_registered)
        ret = program._render_internal(date=_now)
        index = 'html/fairylab/index.html'
        self.assertEqual(ret, [(index, '', 'home.html', home)])

        mock_home.assert_called_once_with(date=_now)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(program.registered['browsable'].date, _then)
        self.assertEqual(program.registered['browsable'].ok, True)
        self.assertEqual(program.registered['dashboard'].date, _then)
        self.assertEqual(program.registered['dashboard'].ok, True)
        self.assertEqual(program.registered['internal'].date, _then)
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

        program = self.create_program(registered=_registered)
        program._try('internal', '_run_internal', date=_now)

        mock_bnotify.assert_not_called()
        mock_inotify.assert_not_called()
        mock_run.assert_called_once_with(date=_now)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(program.registered['browsable'].date, _then)
        self.assertEqual(program.registered['browsable'].ok, True)
        self.assertEqual(program.registered['dashboard'].date, _then)
        self.assertEqual(program.registered['dashboard'].ok, True)
        self.assertEqual(program.registered['internal'].date, _now)
        self.assertEqual(program.registered['internal'].ok, True)

    @mock.patch.object(Internal, '_run_internal')
    @mock.patch.object(Internal, '_notify')
    @mock.patch.object(Browsable, '_notify')
    def test_try__with_notify(self, mock_bnotify, mock_inotify, mock_run):
        mock_bnotify.return_value = Response()
        mock_run.return_value = Response(notify=[Notify.OTHER])

        program = self.create_program(registered=_registered)
        program._try('internal', '_run_internal', date=_now)

        mock_bnotify.assert_called_once_with(notify=Notify.OTHER, date=_now)
        mock_inotify.assert_called_once_with(notify=Notify.OTHER, date=_now)
        mock_run.assert_called_once_with(date=_now)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(program.registered['browsable'].date, _then)
        self.assertEqual(program.registered['browsable'].ok, True)
        self.assertEqual(program.registered['dashboard'].date, _then)
        self.assertEqual(program.registered['dashboard'].ok, True)
        self.assertEqual(program.registered['internal'].date, _now)
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

        program = self.create_program(registered=_registered)
        program._try('internal', '_run_internal', date=_now)

        mock_bnotify.assert_not_called()
        mock_bshadow.assert_called_once_with(shadow=shadow, date=_now)
        mock_inotify.assert_not_called()
        mock_ishadow.assert_not_called()
        mock_run.assert_called_once_with(date=_now)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(program.registered['browsable'].date, _then)
        self.assertEqual(program.registered['browsable'].ok, True)
        self.assertEqual(program.registered['dashboard'].date, _then)
        self.assertEqual(program.registered['dashboard'].ok, True)
        self.assertEqual(program.registered['internal'].date, _then)
        self.assertEqual(program.registered['internal'].ok, True)
        self.assertEqual(program.tasks, [])

    @mock.patch.object(Internal, '_run_internal')
    @mock.patch.object(Internal, '_notify')
    @mock.patch.object(Browsable, '_notify')
    def test_try__with_task(self, mock_bnotify, mock_inotify, mock_run):
        mock_run.return_value = Response(task=[Task(target='foo')])

        program = self.create_program(registered=_registered)
        program._try('internal', '_run_internal', date=_now)

        mock_bnotify.assert_not_called()
        mock_inotify.assert_not_called()
        mock_run.assert_called_once_with(date=_now)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(program.registered['browsable'].date, _then)
        self.assertEqual(program.registered['browsable'].ok, True)
        self.assertEqual(program.registered['dashboard'].date, _then)
        self.assertEqual(program.registered['dashboard'].ok, True)
        self.assertEqual(program.registered['internal'].date, _then)
        self.assertEqual(program.registered['internal'].ok, True)
        self.assertEqual(program.tasks, [('internal', Task(target='foo'))])

    @mock.patch.object(Internal, '_run_internal')
    @mock.patch.object(Internal, '_notify')
    @mock.patch.object(Browsable, '_notify')
    def test_try__with_no_change(self, mock_bnotify, mock_inotify, mock_run):
        mock_run.return_value = Response()

        program = self.create_program(registered=_registered)
        program._try('internal', '_run_internal', date=_now)

        mock_bnotify.assert_not_called()
        mock_inotify.assert_not_called()
        mock_run.assert_called_once_with(date=_now)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(program.registered['browsable'].date, _then)
        self.assertEqual(program.registered['browsable'].ok, True)
        self.assertEqual(program.registered['dashboard'].date, _then)
        self.assertEqual(program.registered['dashboard'].ok, True)
        self.assertEqual(program.registered['internal'].date, _then)
        self.assertEqual(program.registered['internal'].ok, True)
        self.assertEqual(program.tasks, [])

    @mock.patch.object(Internal, '_run_internal')
    @mock.patch.object(Internal, '_notify')
    @mock.patch.object(Browsable, '_notify')
    def test_try__without_date(self, mock_bnotify, mock_inotify, mock_run):
        mock_run.return_value = Response(notify=[Notify.BASE])

        program = self.create_program(registered=_registered)
        program._try('internal', '_run_internal')

        mock_bnotify.assert_not_called()
        mock_inotify.assert_not_called()
        mock_run.assert_called_once_with(date=_now)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_called_once_with()
        self.mock_log.assert_not_called()
        self.assertEqual(program.registered['browsable'].date, _then)
        self.assertEqual(program.registered['browsable'].ok, True)
        self.assertEqual(program.registered['dashboard'].date, _then)
        self.assertEqual(program.registered['dashboard'].ok, True)
        self.assertEqual(program.registered['internal'].date, _now)
        self.assertEqual(program.registered['internal'].ok, True)
        self.assertEqual(program.tasks, [])

    @mock.patch.object(Internal, '_run_internal')
    @mock.patch.object(Internal, '_notify')
    @mock.patch.object(Browsable, '_notify')
    def test_try__with_thrown_exception(self, mock_bnotify, mock_inotify,
                                        mock_run):
        mock_run.side_effect = Exception()

        program = self.create_program(registered=_registered)
        program._try('internal', '_run_internal', date=_now)

        mock_bnotify.assert_not_called()
        mock_inotify.assert_not_called()
        mock_run.assert_called_once_with(date=_now)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_called_once_with(
            logging.ERROR, 'Disabled internal.', exc_info=True)
        self.assertEqual(program.registered['browsable'].date, _then)
        self.assertEqual(program.registered['browsable'].ok, True)
        self.assertEqual(program.registered['dashboard'].date, _then)
        self.assertEqual(program.registered['dashboard'].ok, True)
        self.assertEqual(program.registered['internal'].date, _now)
        self.assertEqual(program.registered['internal'].ok, False)
        self.assertEqual(program.tasks, [])

    @mock.patch.object(Internal, '_run_internal')
    @mock.patch.object(Internal, '_notify')
    @mock.patch.object(Browsable, '_notify')
    def test_try__with_plugin_error(self, mock_bnotify, mock_inotify,
                                    mock_run):
        program = self.create_program(registered=_registered)
        program.registered['internal'].ok = False
        program._try('internal', '_run_internal', date=_now)

        mock_bnotify.assert_not_called()
        mock_inotify.assert_not_called()
        mock_run.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(program.registered['browsable'].date, _then)
        self.assertEqual(program.registered['browsable'].ok, True)
        self.assertEqual(program.registered['dashboard'].date, _then)
        self.assertEqual(program.registered['dashboard'].ok, True)
        self.assertEqual(program.registered['internal'].date, _then)
        self.assertEqual(program.registered['internal'].ok, False)
        self.assertEqual(program.tasks, [])

    @mock.patch.object(Internal, '_run_internal')
    @mock.patch.object(Internal, '_notify')
    @mock.patch.object(Browsable, '_notify')
    def test_try__with_plugin_not_found(self, mock_bnotify, mock_inotify,
                                        mock_run):
        program = self.create_program(registered=_registered)
        program._try('foo', '_run_internal', date=_now)

        mock_bnotify.assert_not_called()
        mock_inotify.assert_not_called()
        mock_run.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(program.registered['browsable'].date, _then)
        self.assertEqual(program.registered['browsable'].ok, True)
        self.assertEqual(program.registered['dashboard'].date, _then)
        self.assertEqual(program.registered['dashboard'].ok, True)
        self.assertEqual(program.registered['internal'].date, _then)
        self.assertEqual(program.registered['internal'].ok, True)
        self.assertEqual(program.tasks, [])

    @mock.patch.object(Internal, '_notify')
    @mock.patch.object(Browsable, '_notify')
    def test_try__with_item_not_found(self, mock_bnotify, mock_inotify):
        program = self.create_program(registered=_registered)
        program._try('internal', '_foo', date=_now)

        mock_bnotify.assert_not_called()
        mock_inotify.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(program.registered['browsable'].date, _then)
        self.assertEqual(program.registered['browsable'].ok, True)
        self.assertEqual(program.registered['dashboard'].date, _then)
        self.assertEqual(program.registered['dashboard'].ok, True)
        self.assertEqual(program.registered['internal'].date, _then)
        self.assertEqual(program.registered['internal'].ok, True)
        self.assertEqual(program.tasks, [])

    @mock.patch.object(Internal, '_notify')
    @mock.patch.object(Browsable, '_notify')
    def test_try__with_item_not_callable(self, mock_bnotify, mock_inotify):
        program = self.create_program(registered=_registered)
        program._try('internal', 'var', date=_now)

        mock_bnotify.assert_not_called()
        mock_inotify.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(program.registered['browsable'].date, _then)
        self.assertEqual(program.registered['browsable'].ok, True)
        self.assertEqual(program.registered['dashboard'].date, _then)
        self.assertEqual(program.registered['dashboard'].ok, True)
        self.assertEqual(program.registered['internal'].date, _then)
        self.assertEqual(program.registered['internal'].ok, True)
        self.assertEqual(program.tasks, [])

    @mock.patch.object(Fairylab, '_try')
    @mock.patch('core.fairylab.fairylab.time.sleep')
    def test_background(self, mock_sleep, mock_try):
        args = (True, False)
        kwargs = {'key': 'value'}
        task = Task(target='foo', args=args, kwargs=kwargs)
        program = self.create_program(
            registered=_registered, tasks=[('internal', task)])

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
        program = self.create_program(registered=_registered)

        mock_try.side_effect = functools.partial(set_date_now, program)
        program._recv('{"type":"message","channel":"ABC","text":"foo"}')

        obj = {'type': 'message', 'channel': 'ABC', 'text': 'foo'}
        mock_message.assert_called_once_with(obj=obj, date=_now)
        calls = [
            mock.call('browsable', '_on_message', obj=obj, date=_now),
            mock.call('dashboard', '_on_message', obj=obj, date=_now),
            mock.call('internal', '_on_message', obj=obj, date=_now),
        ]
        mock_try.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_called_once_with()
        self.mock_log.assert_not_called()

    @mock.patch.object(Fairylab, '_try')
    @mock.patch.object(Fairylab, '_on_message')
    def test_recv__with_no_change(self, mock_message, mock_try):
        program = self.create_program(registered=_registered)
        program._recv('{"type":"message","channel":"ABC","text":"foo"}')

        obj = {'type': 'message', 'channel': 'ABC', 'text': 'foo'}
        mock_message.assert_called_once_with(obj=obj, date=_now)
        calls = [
            mock.call('browsable', '_on_message', obj=obj, date=_now),
            mock.call('dashboard', '_on_message', obj=obj, date=_now),
            mock.call('internal', '_on_message', obj=obj, date=_now),
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

        program = self.create_program(registered=_registered)
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

        program = self.create_program(registered=_registered)
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
        program = self.create_program(registered=_registered)

        mock_sleep.side_effect = functools.partial(set_running_false, program)
        mock_try.side_effect = functools.partial(set_date_now, program)
        program._start()

        mock_connect.assert_called_once_with()
        mock_sleep.assert_called_once_with(120)
        mock_thread.assert_called_once_with(target=mock_bg)
        mock_thread.return_value.start.assert_called_once_with()
        calls = [
            mock.call('browsable', '_run', date=_now),
            mock.call('dashboard', '_run', date=_now),
            mock.call('internal', '_run', date=_now),
        ]
        mock_try.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_called_once_with()
        self.mock_log.assert_not_called()
        self.assertEqual(program.registered['browsable'].date, _now)
        self.assertEqual(program.registered['dashboard'].date, _now)
        self.assertEqual(program.registered['internal'].date, _now)

    @mock.patch.object(Fairylab, '_try')
    @mock.patch('core.fairylab.fairylab.threading.Thread')
    @mock.patch('core.fairylab.fairylab.time.sleep')
    @mock.patch.object(Fairylab, '_render')
    @mock.patch.object(Fairylab, '_connect')
    @mock.patch.object(Fairylab, '_background')
    def test_start__with_date_change(self, mock_bg, mock_connect, mock_render,
                                     mock_sleep, mock_thread, mock_try):
        program = self.create_program(registered=_registered)
        program.day = _then.day

        mock_sleep.side_effect = functools.partial(set_running_false, program)
        program._start()

        mock_connect.assert_called_once_with()
        mock_sleep.assert_called_once_with(120)
        mock_thread.assert_called_once_with(target=mock_bg)
        mock_thread.return_value.start.assert_called_once_with()
        calls = [
            mock.call('browsable', '_run', date=_now),
            mock.call('dashboard', '_run', date=_now),
            mock.call('internal', '_run', date=_now),
            mock.call('browsable', '_notify', notify=Notify.FAIRYLAB_DAY),
            mock.call('dashboard', '_notify', notify=Notify.FAIRYLAB_DAY),
            mock.call('internal', '_notify', notify=Notify.FAIRYLAB_DAY),
        ]
        mock_try.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_called_once_with()
        self.mock_log.assert_not_called()
        self.assertEqual(program.registered['browsable'].date, _then)
        self.assertEqual(program.registered['dashboard'].date, _then)
        self.assertEqual(program.registered['internal'].date, _then)

    @mock.patch.object(Fairylab, '_try')
    @mock.patch('core.fairylab.fairylab.threading.Thread')
    @mock.patch('core.fairylab.fairylab.time.sleep')
    @mock.patch.object(Fairylab, '_render')
    @mock.patch.object(Fairylab, '_connect')
    @mock.patch.object(Fairylab, '_background')
    def test_start__with_no_change(self, mock_bg, mock_connect, mock_render,
                                   mock_sleep, mock_thread, mock_try):
        program = self.create_program(registered=_registered)

        mock_sleep.side_effect = functools.partial(set_running_false, program)
        program._start()

        mock_connect.assert_called_once_with()
        mock_sleep.assert_called_once_with(120)
        mock_thread.assert_called_once_with(target=mock_bg)
        mock_thread.return_value.start.assert_called_once_with()
        mock_try.assert_has_calls([mock.call('internal', '_run', date=_now)])
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_called_once_with()
        self.mock_log.assert_not_called()
        self.assertEqual(program.registered['browsable'].date, _then)
        self.assertEqual(program.registered['dashboard'].date, _then)
        self.assertEqual(program.registered['internal'].date, _then)

    @mock.patch('core.fairylab.fairylab.delta')
    def test_home__with_valid_input(self, mock_delta):
        mock_delta.side_effect = ['2m ago', '15m ago', '2h ago']

        program = self.create_program(registered=_registered)
        ret = program._home(date=_now)
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
        breadcrumbs = [{'href': '', 'name': 'Home'}]
        expected = {
            'breadcrumbs': breadcrumbs,
            'browsable': [browsable, dashboard],
            'internal': [internal],
        }
        self.assertEqual(ret, expected)

    @mock.patch('core.fairylab.fairylab.delta')
    def test_home__with_success(self, mock_delta):
        mock_delta.side_effect = ['0s ago', '15m ago', '2h ago']

        program = self.create_program(registered=_registered)
        ret = program._home(date=_then)
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
        breadcrumbs = [{'href': '', 'name': 'Home'}]
        expected = {
            'breadcrumbs': breadcrumbs,
            'browsable': [browsable, dashboard],
            'internal': [internal],
        }
        self.assertEqual(ret, expected)

    @mock.patch('core.fairylab.fairylab.delta')
    def test_home__with_danger(self, mock_delta):
        mock_delta.side_effect = ['2m ago', '15m ago', '2h ago']

        program = self.create_program(registered=_registered)
        program.registered['internal'].ok = False
        ret = program._home(date=_now)
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
        breadcrumbs = [{'href': '', 'name': 'Home'}]
        expected = {
            'breadcrumbs': breadcrumbs,
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
        kwargs = {'date': _then, 'v': True}
        program = self.create_program()
        program.reload(*args, **kwargs)

        module = mock_import.return_value
        mock_getattr.assert_called_once_with(module, 'Internal')
        mock_import.assert_called_once_with('plugin.internal.internal')
        calls = [
            mock.call('dashboard', 'resolve', 'internal', **dict(kwargs)),
            mock.call('dashboard', '_setup', **dict(kwargs)),
            mock.call('internal', '_setup', **dict(kwargs)),
        ]
        mock_try.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        calls = [
            mock.call(logging.INFO, 'Reloaded internal.'),
            mock.call(logging.DEBUG, 'Reloaded internal.'),
            mock.call(logging.INFO, 'Completed setup.'),
            mock.call(logging.DEBUG, 'Completed setup.')
        ]
        self.mock_log.assert_has_calls(calls)
        self.assertNotIn('browsable', program.registered)
        self.assertEqual(program.registered['dashboard'].date, _then)
        self.assertEqual(program.registered['dashboard'].ok, True)
        self.assertEqual(program.registered['internal'].date, _then)
        self.assertEqual(program.registered['internal'].ok, True)

    @mock.patch.object(Fairylab, '_try')
    @mock.patch('core.fairylab.fairylab.importlib.import_module')
    @mock.patch('core.fairylab.fairylab.getattr')
    def test_reload__with_thrown_exception(self, mock_getattr, mock_import,
                                           mock_try):
        mock_getattr.side_effect = Exception()

        args = ('plugin', 'internal')
        kwargs = {'date': _then, 'v': True}
        program = self.create_program()
        program.reload(*args, **kwargs)

        module = mock_import.return_value
        mock_getattr.assert_called_once_with(module, 'Internal')
        mock_import.assert_called_once_with('plugin.internal.internal')
        mock_try.assert_called_once_with('dashboard', 'resolve', 'internal',
                                         **dict(kwargs))
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_called_once_with(
            logging.ERROR, 'Disabled internal.', exc_info=True)
        self.assertNotIn('browsable', program.registered)
        self.assertEqual(program.registered['dashboard'].date, _then)
        self.assertEqual(program.registered['dashboard'].ok, True)
        self.assertNotIn('internal', program.registered)

    @mock.patch('core.fairylab.fairylab.os.execv')
    def test_reboot(self, mock_execv):
        program = self.create_program()
        program.reboot(v=True)

        expected = ['python3'] + sys.argv
        mock_execv.assert_called_once_with(sys.executable, expected)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_called_once_with(logging.INFO,
                                              'Restarted fairylab.')

    def test_shutdown(self):
        program = self.create_program()
        program.shutdown(v=True)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_datetime.datetime.now.assert_not_called()
        self.mock_log.assert_called_once_with(logging.INFO, 'Killed fairylab.')
        self.assertFalse(program.keep_running)


if __name__ in ['__main__', 'core.fairylab.fairylab_test']:
    _main = __name__ == '__main__'
    _pkg = 'core.fairylab'
    _pth = 'core/fairylab'
    main(FairylabTest, Fairylab, _pkg, _pth, {}, _main, d=_dashboard, e=_env)
