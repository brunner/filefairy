#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for filefairy.py."""

import functools
import json
import logging
import os
import re
import sys
import threading
import types
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.extend((_path, re.sub(r'/impl/filefairy', '', _path)))

from api.registrable.registrable import Registrable  # noqa
from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.datetime_.datetime_ import encode_datetime  # noqa
from common.elements.elements import card  # noqa
from common.json_.json_ import dumps  # noqa
from common.jinja2_.jinja2_ import env  # noqa
from common.test.test import Test  # noqa
from common.test.test import main  # noqa
from data.debug.debug import Debug  # noqa
from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa
from data.shadow.shadow import Shadow  # noqa
from data.thread_.thread_ import Thread  # noqa
from impl.dashboard.dashboard import Dashboard  # noqa
from impl.filefairy.filefairy import Filefairy  # noqa

BG = threading.Thread()
ENV = env()

DATE_10250007 = datetime_datetime_pst(1985, 10, 25, 0, 7)
DATE_10260602 = datetime_datetime_pst(1985, 10, 26, 6, 2, 30)
DATE_10260604 = datetime_datetime_pst(1985, 10, 26, 6, 4)

TASKS_DIR = re.sub(r'/impl/filefairy', '/tasks', _path)


def _data(date):
    return {'date': encode_datetime(date)}


def _module(name):
    m = types.ModuleType(name, None)
    m.__file__ = name + '.py'
    sys.modules[name] = m
    return m


def set_date(filefairy, *args, **kwargs):
    filefairy.data['date'] = kwargs['date']


def set_keep_running(filefairy, keep_running, *args, **kwargs):
    filefairy.keep_running = keep_running


class FakeExternalRegistrable(Registrable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def _data():
        return re.sub(r'/impl/filefairy', '/tasks/snacks/data.json', _path)

    @staticmethod
    def _href():
        return '/foo/'

    @staticmethod
    def _info():
        return 'Description of foo.'

    @staticmethod
    def _title():
        return 'foo'

    def _on_message_internal(self, **kwargs):
        return Response(notify=[Notify.BASE])

    def _notify_internal(self, **kwargs):
        pass

    def _render_internal(self, **kwargs):
        return [('foo/index.html', '', 'foo.html', {})]

    def _run_internal(self, **kwargs):
        return Response(notify=[Notify.BASE])

    def _setup_internal(self, **kwargs):
        pass

    def _shadow_internal(self, **kwargs):
        return []


class FakeInternalRegistrable(Registrable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def _data():
        return re.sub(r'/impl/filefairy', '/tasks/snacks/data.json', _path)

    @staticmethod
    def _href():
        return ''

    @staticmethod
    def _info():
        return 'Description of bar.'

    @staticmethod
    def _title():
        return 'bar'

    def _on_message_internal(self, **kwargs):
        return Response(notify=[Notify.BASE])

    def _notify_internal(self, **kwargs):
        pass

    def _render_internal(self, **kwargs):
        return []

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


class FilefairyTest(Test):
    def setUp(self):
        patch_log = mock.patch('impl.filefairy.filefairy._logger.log')
        self.addCleanup(patch_log.stop)
        self.mock_log = patch_log.start()

        patch_open = mock.patch(
            'api.serializable.serializable.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]

    def reset_mocks(self):
        self.mock_log.reset_mock()
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()

    def create_dashboard(self, date):
        self.init_mocks({})
        dashboard = Dashboard(date=date, e=ENV)

        self.mock_open.assert_called_once_with(Dashboard._data(), 'r')
        self.assertNotCalled(self.mock_log, self.mock_handle.write)
        self.assertEqual(dashboard.data, {})

        self.reset_mocks()
        self.init_mocks({})

        return dashboard

    def create_filefairy(self, data, dashboard):
        self.init_mocks(data)
        filefairy = Filefairy(d=dashboard, e=ENV)

        self.mock_open.assert_called_once_with(Filefairy._data(), 'r')
        self.assertNotCalled(self.mock_log, self.mock_handle.write)
        self.assertEqual(filefairy.data, data)
        self.assertEqual(filefairy.original, data)

        self.reset_mocks()
        self.init_mocks(data)

        return filefairy

    def create_external_registrable(self, date):
        self.init_mocks({})
        registrable = FakeExternalRegistrable(date=date, e=ENV)

        self.mock_open.assert_called_once_with(FakeExternalRegistrable._data(),
                                               'r')
        self.assertNotCalled(self.mock_log, self.mock_handle.write)
        self.assertEqual(registrable.data, {})

        self.reset_mocks()
        self.init_mocks({})

        return registrable

    def create_internal_registrable(self, date):
        self.init_mocks({})
        registrable = FakeInternalRegistrable(date=date, e=ENV)

        self.mock_open.assert_called_once_with(FakeInternalRegistrable._data(),
                                               'r')
        self.assertNotCalled(self.mock_log, self.mock_handle.write)
        self.assertEqual(registrable.data, {})

        self.reset_mocks()
        self.init_mocks({})

        return registrable

    def test_init(self):
        dashboard = self.create_dashboard(DATE_10260602)
        filefairy = self.create_filefairy(_data(DATE_10260602), dashboard)

        self.assertIsNone(filefairy.bg)
        self.assertIsNone(filefairy.day)
        self.assertTrue(filefairy.keep_running)
        self.assertEqual(filefairy.registered, {'dashboard': dashboard})
        self.assertEqual(filefairy.sleep, 60)
        self.assertFalse(len(filefairy.threads))
        self.assertIsNone(filefairy.ws)
        self.assertNotCalled(self.mock_log, self.mock_open,
                             self.mock_handle.write)

    def test_on_message(self):
        dashboard = self.create_dashboard(DATE_10260602)
        filefairy = self.create_filefairy(_data(DATE_10260602), dashboard)
        response = filefairy._on_message_internal(date=DATE_10260602)
        self.assertEqual(response, Response())

        self.assertNotCalled(self.mock_log, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Filefairy, '_index_html')
    def test_render(self, mock_index):
        index_html = {'breadcrumbs': []}
        mock_index.return_value = index_html

        dashboard = self.create_dashboard(DATE_10260602)
        filefairy = self.create_filefairy(_data(DATE_10260602), dashboard)
        actual = filefairy._render_internal(date=DATE_10260602)
        expected = [('index.html', '', 'home.html', index_html)]
        self.assertEqual(actual, expected)

        self.assertNotCalled(self.mock_log, self.mock_open,
                             self.mock_handle.write)

    @mock.patch('impl.filefairy.filefairy.os.execv')
    def test_reboot(self, mock_execv):
        dashboard = self.create_dashboard(DATE_10260602)
        filefairy = self.create_filefairy(_data(DATE_10260602), dashboard)
        filefairy.reboot(v=True)

        expected = ['python3'] + sys.argv
        mock_execv.assert_called_once_with(sys.executable, expected)
        self.mock_log.assert_called_once_with(logging.DEBUG,
                                              'Rebooting filefairy.')
        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    @mock.patch.object(Filefairy, '_try_all')
    @mock.patch.object(Filefairy, '_reload_internal')
    def test_reload__base(self, mock_reload, mock_try_all):
        response = Response(notify=[Notify.BASE])
        mock_reload.return_value = response

        dashboard = self.create_dashboard(DATE_10260602)
        filefairy = self.create_filefairy(_data(DATE_10260602), dashboard)
        actual = filefairy.reload(*('foo', ), date=DATE_10260604)
        self.assertEqual(actual, response)

        mock_reload.assert_called_once_with('foo', date=DATE_10260604)
        mock_try_all.assert_called_once_with('_setup', date=DATE_10260604)
        self.assertNotCalled(self.mock_log, self.mock_open,
                             self.mock_handle.write)
        self.assertEqual(filefairy.data['date'],
                         encode_datetime(DATE_10260604))

    @mock.patch.object(Filefairy, '_try_all')
    @mock.patch.object(Filefairy, '_reload_internal')
    def test_reload__none(self, mock_reload, mock_try_all):
        response = Response()
        mock_reload.return_value = response

        dashboard = self.create_dashboard(DATE_10260602)
        filefairy = self.create_filefairy(_data(DATE_10260602), dashboard)
        actual = filefairy.reload(*('foo', ), date=DATE_10260604)
        self.assertEqual(actual, response)

        mock_reload.assert_called_once_with('foo', date=DATE_10260604)
        self.assertNotCalled(mock_try_all, self.mock_log, self.mock_open,
                             self.mock_handle.write)
        self.assertEqual(filefairy.data['date'],
                         encode_datetime(DATE_10260602))

    def test_shutdown(self):
        dashboard = self.create_dashboard(DATE_10260602)
        filefairy = self.create_filefairy(_data(DATE_10260602), dashboard)
        filefairy.shutdown(v=True)

        self.mock_log.assert_called_once_with(logging.DEBUG,
                                              'Shutting down filefairy.')
        self.assertNotCalled(self.mock_open, self.mock_handle.write)
        self.assertFalse(filefairy.keep_running)

    @mock.patch.object(Filefairy, '_try')
    @mock.patch('impl.filefairy.filefairy.time.sleep')
    def test_background(self, mock_sleep, mock_try):
        dashboard = self.create_dashboard(DATE_10260602)
        filefairy = self.create_filefairy(_data(DATE_10260602), dashboard)

        mock_sleep.side_effect = functools.partial(set_keep_running, filefairy,
                                                   False)

        thread_ = Thread(target='foo')
        filefairy.threads = [('task', thread_)]
        filefairy._background()

        mock_sleep.assert_called_once_with(60)
        mock_try.assert_called_once_with('task', 'foo')
        self.assertNotCalled(self.mock_log, self.mock_open,
                             self.mock_handle.write)
        self.assertEqual(filefairy.threads, [])

    @mock.patch('impl.filefairy.filefairy.websocket.WebSocketApp')
    @mock.patch('impl.filefairy.filefairy.threading.Thread')
    @mock.patch('impl.filefairy.filefairy.rtm_connect')
    @mock.patch.object(Filefairy, '_recv')
    def test_connect(self, mock_recv, mock_rtm, mock_thread, mock_ws):
        mock_rtm.return_value = {'ok': True, 'url': 'wss://...'}
        mock_ws.side_effect = FakeWebSocketApp

        dashboard = self.create_dashboard(DATE_10260602)
        filefairy = self.create_filefairy(_data(DATE_10260602), dashboard)
        filefairy._connect()

        message = '{"type":"message","channel":"ABC","text":"foo"}'
        filefairy.ws.send(message)

        mock_recv.assert_called_once_with(message)
        mock_rtm.assert_called_once_with()
        mock_thread.assert_called_once_with(target=filefairy.ws.run_forever)
        self.assertNotCalled(self.mock_log, self.mock_open,
                             self.mock_handle.write)

    @mock.patch('impl.filefairy.filefairy.getattr')
    def test_install__exception(self, mock_getattr):
        mock_getattr.side_effect = Exception()

        dashboard = self.create_dashboard(DATE_10260602)
        filefairy = self.create_filefairy(_data(DATE_10260602), dashboard)

        module = _module('task')
        actual = filefairy._install('foo', module, 'Task', date=DATE_10260604)
        expected = False
        self.assertEqual(actual, expected)

        mock_getattr.assert_called_once_with(module, 'Task')
        self.mock_log(logging.ERROR, 'Disabled foo.', exc_info=True)
        self.assertNotCalled(self.mock_open, self.mock_handle.write)
        self.assertNotIn('foo', filefairy.registered)

    @mock.patch('impl.filefairy.filefairy.getattr')
    def test_install__ok(self, mock_getattr):
        mock_getattr.return_value = FakeExternalRegistrable

        dashboard = self.create_dashboard(DATE_10260602)
        filefairy = self.create_filefairy(_data(DATE_10260602), dashboard)

        module = _module('task')
        actual = filefairy._install('foo', module, 'Task', date=DATE_10260604)
        expected = True
        self.assertEqual(actual, expected)

        mock_getattr.assert_called_once_with(module, 'Task')
        self.mock_open.assert_called_once_with(FakeExternalRegistrable._data(),
                                               'r')
        self.assertNotCalled(self.mock_log, self.mock_handle.write)
        self.assertTrue(
            isinstance(filefairy.registered['foo'], FakeExternalRegistrable))

    @mock.patch.object(Filefairy, '_try_all')
    @mock.patch.object(Filefairy, '_on_message')
    @mock.patch('impl.filefairy.filefairy.datetime_now')
    def test_recv(self, mock_now, mock_on_message, mock_try_all):
        mock_now.return_value = DATE_10260604

        dashboard = self.create_dashboard(DATE_10260602)
        filefairy = self.create_filefairy(_data(DATE_10260602), dashboard)

        message = '{"type":"message","channel":"ABC","text":"foo"}'
        filefairy._recv(message)

        obj = json.loads(message)
        mock_now.assert_called_once_with()
        mock_on_message.assert_called_once_with(obj=obj, date=DATE_10260604)
        mock_try_all.assert_called_once_with(
            '_on_message', obj=obj, date=DATE_10260604)
        self.assertNotCalled(self.mock_log, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Filefairy, '_install')
    @mock.patch('impl.filefairy.filefairy.importlib.import_module')
    def test_reload_internal__exception(self, mock_import, mock_install):
        mock_import.side_effect = Exception()

        dashboard = self.create_dashboard(DATE_10260602)
        filefairy = self.create_filefairy(_data(DATE_10260602), dashboard)
        actual = filefairy._reload_internal('task', date=DATE_10260604)
        expected = Response()
        self.assertEqual(actual, expected)

        mock_import.assert_called_once_with('tasks.task.task')
        self.mock_log.assert_called_once_with(
            logging.ERROR, 'Disabled task.', exc_info=True)
        self.assertNotCalled(mock_install, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Filefairy, '_install')
    @mock.patch('impl.filefairy.filefairy.importlib.import_module')
    def test_reload_internal__ok_false(self, mock_import, mock_install):
        module = _module('task')
        mock_import.return_value = module
        mock_install.return_value = False

        dashboard = self.create_dashboard(DATE_10260602)
        filefairy = self.create_filefairy(_data(DATE_10260602), dashboard)
        actual = filefairy._reload_internal('task', date=DATE_10260604)
        expected = Response()
        self.assertEqual(actual, expected)

        mock_import.assert_called_once_with('tasks.task.task')
        mock_install.assert_called_once_with(
            'task', module, 'Task', date=DATE_10260604)
        self.assertNotCalled(self.mock_log, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Filefairy, '_install')
    @mock.patch('impl.filefairy.filefairy.importlib.import_module')
    def test_reload_internal__ok_true(self, mock_import, mock_install):
        module = _module('task')
        mock_import.return_value = module
        mock_install.return_value = True

        dashboard = self.create_dashboard(DATE_10260602)
        filefairy = self.create_filefairy(_data(DATE_10260602), dashboard)
        actual = filefairy._reload_internal('task', date=DATE_10260604)
        msg = 'Reloaded task.'
        expected = Response(notify=[Notify.BASE], debug=[Debug(msg=msg)])
        self.assertEqual(actual, expected)

        mock_import.assert_called_once_with('tasks.task.task')
        mock_install.assert_called_once_with(
            'task', module, 'Task', date=DATE_10260604)
        self.mock_log.assert_called_once_with(logging.INFO, msg)
        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    @mock.patch.object(Filefairy, '_try_all')
    @mock.patch.object(Filefairy, '_try')
    def test_response__empty(self, mock_try, mock_try_all):
        dashboard = self.create_dashboard(DATE_10260602)
        filefairy = self.create_filefairy(_data(DATE_10260602), dashboard)
        filefairy.registered['foo'] = self.create_external_registrable(
            DATE_10260602)

        response = Response()
        filefairy._response('foo', response, date=DATE_10260604)

        self.assertNotCalled(mock_try, mock_try_all, self.mock_log,
                             self.mock_open, self.mock_handle.write)
        self.assertEqual(filefairy.data['date'],
                         encode_datetime(DATE_10260602))
        self.assertEqual(filefairy.registered['foo'].date, DATE_10260602)
        self.assertFalse(len(filefairy.threads))

    @mock.patch.object(Filefairy, '_try_all')
    @mock.patch.object(Filefairy, '_try')
    def test_response__notify_base(self, mock_try, mock_try_all):
        dashboard = self.create_dashboard(DATE_10260602)
        filefairy = self.create_filefairy(_data(DATE_10260602), dashboard)
        filefairy.registered['foo'] = self.create_external_registrable(
            DATE_10260602)

        response = Response(notify=[Notify.BASE])
        filefairy._response('foo', response, date=DATE_10260604)

        self.assertNotCalled(mock_try, mock_try_all, self.mock_log,
                             self.mock_open, self.mock_handle.write)
        self.assertEqual(filefairy.data['date'],
                         encode_datetime(DATE_10260604))
        self.assertEqual(filefairy.registered['foo'].date, DATE_10260604)
        self.assertFalse(len(filefairy.threads))

    @mock.patch.object(Filefairy, '_try_all')
    @mock.patch.object(Filefairy, '_try')
    def test_response__notify_other(self, mock_try, mock_try_all):
        dashboard = self.create_dashboard(DATE_10260602)
        filefairy = self.create_filefairy(_data(DATE_10260602), dashboard)
        filefairy.registered['foo'] = self.create_external_registrable(
            DATE_10260602)

        response = Response(notify=[Notify.OTHER])
        filefairy._response('foo', response, date=DATE_10260604)

        mock_try_all.assert_called_once_with(
            '_notify', notify=Notify.OTHER, date=DATE_10260604)
        self.assertNotCalled(mock_try, self.mock_log, self.mock_open,
                             self.mock_handle.write)
        self.assertEqual(filefairy.data['date'],
                         encode_datetime(DATE_10260604))
        self.assertEqual(filefairy.registered['foo'].date, DATE_10260604)
        self.assertFalse(len(filefairy.threads))

    @mock.patch.object(Filefairy, '_try_all')
    @mock.patch.object(Filefairy, '_try')
    def test_response__shadow(self, mock_try, mock_try_all):
        dashboard = self.create_dashboard(DATE_10260602)
        filefairy = self.create_filefairy(_data(DATE_10260602), dashboard)
        filefairy.registered['foo'] = self.create_external_registrable(
            DATE_10260602)

        shadow = Shadow(destination='bar', key='foo.baz')
        response = Response(shadow=[shadow])
        filefairy._response('foo', response, date=DATE_10260604)

        mock_try.assert_called_once_with(
            'bar', '_shadow', shadow=shadow, date=DATE_10260604)
        self.assertNotCalled(mock_try_all, self.mock_log, self.mock_open,
                             self.mock_handle.write)
        self.assertEqual(filefairy.data['date'],
                         encode_datetime(DATE_10260602))
        self.assertEqual(filefairy.registered['foo'].date, DATE_10260602)
        self.assertFalse(len(filefairy.threads))

    @mock.patch.object(Filefairy, '_try_all')
    @mock.patch.object(Filefairy, '_try')
    def test_response__thread(self, mock_try, mock_try_all):
        dashboard = self.create_dashboard(DATE_10260602)
        filefairy = self.create_filefairy(_data(DATE_10260602), dashboard)
        filefairy.registered['foo'] = self.create_external_registrable(
            DATE_10260602)

        thread_ = Thread(target='foo')
        response = Response(thread_=[thread_])
        filefairy._response('foo', response, date=DATE_10260604)

        self.assertNotCalled(mock_try, mock_try_all, self.mock_log,
                             self.mock_open, self.mock_handle.write)
        self.assertEqual(filefairy.data['date'],
                         encode_datetime(DATE_10260602))
        self.assertEqual(filefairy.registered['foo'].date, DATE_10260602)
        self.assertCountEqual(filefairy.threads, [('foo', thread_)])

    @mock.patch.object(Filefairy, '_try_all')
    @mock.patch.object(Filefairy, '_try')
    @mock.patch.object(Filefairy, '_render')
    @mock.patch('impl.filefairy.filefairy.datetime_now')
    def test_run__day(self, mock_now, mock_render, mock_try, mock_try_all):
        mock_now.return_value = DATE_10260604

        dashboard = self.create_dashboard(DATE_10250007)
        filefairy = self.create_filefairy(_data(DATE_10250007), dashboard)
        filefairy.day = 25
        filefairy.registered['git'] = self.create_external_registrable(
            DATE_10260602)

        filefairy._run()

        notify = Notify.FILEFAIRY_DAY
        mock_now.assert_called_once_with()
        mock_try_all.assert_has_calls([
            mock.call('_run', date=DATE_10260604),
            mock.call('_notify', notify=notify, date=DATE_10260604)
        ])
        self.assertNotCalled(mock_render, mock_try, self.mock_log,
                             self.mock_open, self.mock_handle.write)
        self.assertEqual(filefairy.day, 26)

    @mock.patch.object(Filefairy, '_try_all')
    @mock.patch.object(Filefairy, '_try')
    @mock.patch.object(Filefairy, '_render')
    @mock.patch('impl.filefairy.filefairy.datetime_now')
    def test_run__noop(self, mock_now, mock_render, mock_try, mock_try_all):
        mock_now.return_value = DATE_10260604

        dashboard = self.create_dashboard(DATE_10260602)
        filefairy = self.create_filefairy(_data(DATE_10260602), dashboard)
        filefairy.day = 26
        filefairy.registered['git'] = self.create_external_registrable(
            DATE_10260602)

        filefairy._run()

        mock_now.assert_called_once_with()
        mock_try_all.assert_called_once_with('_run', date=DATE_10260604)
        self.assertNotCalled(mock_render, mock_try, self.mock_log,
                             self.mock_open, self.mock_handle.write)
        self.assertEqual(filefairy.day, 26)

    @mock.patch.object(Filefairy, '_try_all')
    @mock.patch.object(Filefairy, '_try')
    @mock.patch.object(Filefairy, '_render')
    @mock.patch('impl.filefairy.filefairy.datetime_now')
    def test_run__render(self, mock_now, mock_render, mock_try, mock_try_all):
        mock_now.return_value = DATE_10260604

        dashboard = self.create_dashboard(DATE_10260602)
        filefairy = self.create_filefairy(_data(DATE_10260602), dashboard)
        filefairy.day = 26
        filefairy.registered['git'] = self.create_external_registrable(
            DATE_10260602)

        mock_try_all.side_effect = functools.partial(set_date, filefairy)

        filefairy._run()

        notify = Notify.FILEFAIRY_DEPLOY
        mock_now.assert_called_once_with()
        mock_render.assert_called_once_with(date=DATE_10260604)
        mock_try.assert_called_once_with(
            'git', '_notify', notify=notify, date=DATE_10260604)
        mock_try_all.assert_called_once_with('_run', date=DATE_10260604)
        self.assertNotCalled(self.mock_log, self.mock_open,
                             self.mock_handle.write)
        self.assertEqual(filefairy.day, 26)

    @mock.patch.object(Filefairy, '_try_all')
    @mock.patch.object(Filefairy, '_reload_internal')
    @mock.patch.object(Filefairy, '_get_dirs')
    def test_setup(self, mock_get_dirs, mock_reload, mock_try_all):
        mock_get_dirs.return_value = ['task']

        dashboard = self.create_dashboard(DATE_10260602)
        filefairy = self.create_filefairy(_data(DATE_10260602), dashboard)
        filefairy._setup(date=DATE_10260604)

        mock_get_dirs.assert_called_once_with(TASKS_DIR)
        mock_reload.assert_called_once_with('task', date=DATE_10260604)
        mock_try_all.assert_called_once_with('_setup', date=DATE_10260604)
        self.assertNotCalled(self.mock_log, self.mock_open,
                             self.mock_handle.write)

    @mock.patch('impl.filefairy.filefairy.threading.Thread')
    @mock.patch('impl.filefairy.filefairy.time.sleep')
    @mock.patch.object(Filefairy, '_run')
    @mock.patch.object(Filefairy, '_connect')
    def test_start__initial(self, mock_connect, mock_run, mock_sleep,
                            mock_thread):
        dashboard = self.create_dashboard(DATE_10260602)
        filefairy = self.create_filefairy(_data(DATE_10260602), dashboard)

        mock_sleep.side_effect = functools.partial(set_keep_running, filefairy,
                                                   False)

        filefairy._start()

        mock_connect.assert_called_once_with()
        mock_run.assert_called_once_with()
        mock_sleep.assert_called_once_with(60)
        mock_thread.assert_called_once_with(target=filefairy._background)
        self.assertNotCalled(self.mock_log, self.mock_open,
                             self.mock_handle.write)

    @mock.patch('impl.filefairy.filefairy.threading.Thread')
    @mock.patch('impl.filefairy.filefairy.time.sleep')
    @mock.patch.object(Filefairy, '_run')
    @mock.patch.object(Filefairy, '_connect')
    def test_start__running(self, mock_connect, mock_run, mock_sleep,
                            mock_thread):
        dashboard = self.create_dashboard(DATE_10260602)
        filefairy = self.create_filefairy(_data(DATE_10260602), dashboard)

        mock_sleep.side_effect = functools.partial(set_keep_running, filefairy,
                                                   False)

        filefairy.bg = BG
        filefairy.ws = FakeWebSocketApp(url='wss://...')
        filefairy._start()

        mock_run.assert_called_once_with()
        mock_sleep.assert_called_once_with(60)
        self.assertNotCalled(mock_connect, mock_thread, self.mock_log,
                             self.mock_open, self.mock_handle.write)

    @mock.patch.object(FakeExternalRegistrable, '_run')
    @mock.patch.object(Filefairy, '_response')
    def test_try__exception(self, mock_response, mock_run):
        mock_run.side_effect = Exception()

        dashboard = self.create_dashboard(DATE_10260602)
        filefairy = self.create_filefairy(_data(DATE_10260602), dashboard)
        filefairy.registered['foo'] = self.create_external_registrable(
            DATE_10260602)

        filefairy._try('foo', '_run', date=DATE_10260604)

        mock_run.assert_called_once_with(date=DATE_10260604)
        self.mock_log.assert_called_once_with(
            logging.ERROR, 'Disabled foo.', exc_info=True)
        self.assertNotCalled(mock_response, self.mock_open,
                             self.mock_handle.write)
        self.assertEqual(filefairy.registered['foo'].date, DATE_10260604)
        self.assertEqual(filefairy.registered['foo'].ok, False)

    @mock.patch.object(FakeExternalRegistrable, '_run')
    @mock.patch.object(Filefairy, '_response')
    def test_try__response(self, mock_response, mock_run):
        response = Response(notify=[Notify.BASE])
        mock_run.return_value = response

        dashboard = self.create_dashboard(DATE_10260602)
        filefairy = self.create_filefairy(_data(DATE_10260602), dashboard)
        filefairy.registered['foo'] = self.create_external_registrable(
            DATE_10260602)

        filefairy._try('foo', '_run', date=DATE_10260604)

        mock_response.assert_called_once_with(
            'foo', response, date=DATE_10260604)
        mock_run.assert_called_once_with(date=DATE_10260604)
        self.assertNotCalled(self.mock_log, self.mock_open,
                             self.mock_handle.write)
        self.assertEqual(filefairy.registered['foo'].date, DATE_10260602)
        self.assertEqual(filefairy.registered['foo'].ok, True)

    @mock.patch.object(FakeExternalRegistrable, '_run')
    @mock.patch.object(Filefairy, '_response')
    def test_try__uncallable(self, mock_response, mock_run):
        dashboard = self.create_dashboard(DATE_10260602)
        filefairy = self.create_filefairy(_data(DATE_10260602), dashboard)
        filefairy.registered['foo'] = self.create_external_registrable(
            DATE_10260602)

        filefairy._try('foo', 'bar', date=DATE_10260604)

        self.assertNotCalled(mock_response, mock_run, self.mock_log,
                             self.mock_open, self.mock_handle.write)

    @mock.patch.object(FakeExternalRegistrable, '_run')
    @mock.patch.object(Filefairy, '_response')
    def test_try__unhappy(self, mock_response, mock_run):
        dashboard = self.create_dashboard(DATE_10260602)
        filefairy = self.create_filefairy(_data(DATE_10260602), dashboard)

        registrable = self.create_external_registrable(DATE_10260602)
        registrable.ok = False
        filefairy.registered['foo'] = registrable

        filefairy._try('foo', '_run', date=DATE_10260604)

        self.assertNotCalled(mock_response, mock_run, self.mock_log,
                             self.mock_open, self.mock_handle.write)

    @mock.patch.object(FakeExternalRegistrable, '_run')
    @mock.patch.object(Filefairy, '_response')
    def test_try__unregistered(self, mock_response, mock_run):
        dashboard = self.create_dashboard(DATE_10260602)
        filefairy = self.create_filefairy(_data(DATE_10260602), dashboard)

        filefairy._try('foo', '_run', date=DATE_10260604)

        self.assertNotCalled(mock_response, mock_run, self.mock_log,
                             self.mock_open, self.mock_handle.write)

    @mock.patch.object(Filefairy, '_try')
    def test_try_all(self, mock_try):
        dashboard = self.create_dashboard(DATE_10260602)
        filefairy = self.create_filefairy(_data(DATE_10260602), dashboard)
        filefairy.registered['foo'] = self.create_external_registrable(
            DATE_10260602)

        filefairy._try_all('_run', date=DATE_10260604)

        mock_try.assert_has_calls([
            mock.call('dashboard', '_run', date=DATE_10260604),
            mock.call('foo', '_run', date=DATE_10260604)
        ])
        self.assertNotCalled(self.mock_log, self.mock_open,
                             self.mock_handle.write)

    def test_index_html__disabled(self):
        dashboard = self.create_dashboard(DATE_10260602)
        filefairy = self.create_filefairy(_data(DATE_10260602), dashboard)

        registrable = self.create_external_registrable(DATE_10260602)
        registrable.ok = False
        filefairy.registered['foo'] = registrable

        breadcrumbs = [{'href': '', 'name': 'Fairylab'}]
        external = [
            card(
                href='/dashboard/',
                title='dashboard',
                info='Tails exceptions and log messages.',
                ts='06:02:30 PDT (1985-10-26)'),
            card(
                href='/foo/',
                title='foo',
                info='Description of foo.',
                ts='06:02:30 PDT (1985-10-26)',
                danger='disabled')
        ]
        actual = filefairy._index_html(date=DATE_10260602)
        expected = {
            'breadcrumbs': breadcrumbs,
            'external': external,
            'internal': []
        }
        self.assertEqual(actual, expected)
        self.assertNotCalled(self.mock_log, self.mock_open,
                             self.mock_handle.write)

    def test_index_html__ok(self):
        dashboard = self.create_dashboard(DATE_10260602)
        filefairy = self.create_filefairy(_data(DATE_10260602), dashboard)
        filefairy.registered['foo'] = self.create_external_registrable(
            DATE_10260602)
        filefairy.registered['bar'] = self.create_internal_registrable(
            DATE_10260602)

        breadcrumbs = [{'href': '', 'name': 'Fairylab'}]
        external = [
            card(
                href='/dashboard/',
                title='dashboard',
                info='Tails exceptions and log messages.',
                ts='06:02:30 PDT (1985-10-26)'),
            card(
                href='/foo/',
                title='foo',
                info='Description of foo.',
                ts='06:02:30 PDT (1985-10-26)')
        ]
        internal = [
            card(
                title='bar',
                info='Description of bar.',
                ts='06:02:30 PDT (1985-10-26)')
        ]
        actual = filefairy._index_html(date=DATE_10260602)
        expected = {
            'breadcrumbs': breadcrumbs,
            'external': external,
            'internal': internal
        }
        self.assertEqual(actual, expected)
        self.assertNotCalled(self.mock_log, self.mock_open,
                             self.mock_handle.write)

    @mock.patch('impl.filefairy.filefairy.os.listdir')
    @mock.patch('impl.filefairy.filefairy.os.path.isdir')
    def test_get_dirs(self, mock_isdir, mock_listdir):
        dirs = ['__init__.py', '__pycache__', 'foo', 'bar']
        mock_isdir.side_effect = [False, True, True, True]
        mock_listdir.return_value = dirs

        dashboard = self.create_dashboard(DATE_10260602)
        filefairy = self.create_filefairy(_data(DATE_10260602), dashboard)
        actual = filefairy._get_dirs(TASKS_DIR)
        expected = ['bar', 'foo']
        self.assertEqual(actual, expected)

        mock_isdir.assert_has_calls(
            [mock.call(os.path.join(TASKS_DIR, d)) for d in dirs])
        mock_listdir.assert_called_once_with(TASKS_DIR)
        self.assertNotCalled(self.mock_log, self.mock_open,
                             self.mock_handle.write)


if __name__ in ['__main__', 'impl.filefairy.filefairy_test']:
    dashboard = Dashboard(date=DATE_10260602, e=ENV)
    main(
        FilefairyTest,
        Filefairy,
        'impl.filefairy',
        'impl/filefairy', {},
        __name__ == '__main__',
        d=dashboard,
        e=ENV)
