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

from api.messageable.messageable import Messageable  # noqa
from api.renderable.renderable import Renderable  # noqa
from api.runnable.runnable import Runnable  # noqa
from api.serializable.serializable import Serializable  # noqa
from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.datetime_.datetime_ import encode_datetime  # noqa
from common.elements.elements import topper  # noqa
from common.json_.json_ import dumps  # noqa
from common.jinja2_.jinja2_ import env  # noqa
from common.test.test import Test  # noqa
from common.test.test import main  # noqa
from impl.dashboard.dashboard import Dashboard  # noqa
from impl.filefairy.filefairy import Filefairy  # noqa
from impl.reference.reference import Reference  # noqa
from types_.debug.debug import Debug  # noqa
from types_.notify.notify import Notify  # noqa
from types_.response.response import Response  # noqa
from types_.shadow.shadow import Shadow  # noqa
from types_.thread_.thread_ import Thread  # noqa

BG = threading.Thread()
ENV = env()

DATE_10250007 = datetime_datetime_pst(1985, 10, 25, 0, 7)
DATE_10260602 = datetime_datetime_pst(1985, 10, 26, 6, 2, 30)
DATE_10260604 = datetime_datetime_pst(1985, 10, 26, 6, 4)

TASKS_DIR = re.sub(r'/impl/filefairy', '/tasks', _path)


def _module(name):
    m = types.ModuleType(name, None)
    m.__file__ = name + '.py'
    sys.modules[name] = m
    return m


def set_date(filefairy, *args, **kwargs):
    filefairy.date = kwargs['date']


def set_keep_running(filefairy, keep_running, *args, **kwargs):
    filefairy.keep_running = keep_running


class Faketask(Messageable, Renderable, Runnable, Serializable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def _href():
        return '/faketask/'

    @staticmethod
    def _title():
        return 'Fake Task'

    def _render_data(self, **kwargs):
        return [('faketask/index.html', '', 'faketask.html', {})]

    def _shadow_data(self, **kwargs):
        return []

    def _on_message_internal(self, **kwargs):
        return Response(notify=[Notify.BASE])

    def _notify_internal(self, **kwargs):
        return Response()

    def _run_internal(self, **kwargs):
        return Response(notify=[Notify.BASE])

    def _setup_internal(self, **kwargs):
        return Response()


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

    def create_dashboard(self, date):
        self.init_mocks({})
        return Dashboard(date=date, e=ENV)

    def create_reference(self, date):
        self.init_mocks({})
        return Reference(date=date)

    def create_filefairy(self, date, dashboard, reference):
        self.init_mocks({})
        filefairy = Filefairy(date=date, d=dashboard, e=ENV, r=reference)
        filefairy.set_renderables(['faketask'])

        self.assertNotCalled(self.mock_log)
        self.assertEqual(filefairy.date, date)
        self.assertEqual(filefairy.day, date.day)
        self.assertEqual(filefairy.original, date)

        return filefairy

    def create_task(self, date):
        task = Faketask(date=date, e=ENV)

        self.assertNotCalled(self.mock_log)

        return task

    def test_init(self):
        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)

        self.assertIsNone(filefairy.bg)
        self.assertTrue(filefairy.keep_running)
        self.assertEqual(filefairy.runners, {
            'dashboard': dashboard,
            'reference': reference,
        })
        self.assertEqual(filefairy.sleep, 2)
        self.assertFalse(len(filefairy.threads))
        self.assertIsNone(filefairy.ws)
        self.assertNotCalled(self.mock_log)

    @mock.patch.object(Filefairy, '_index_html')
    def test_render_data(self, mock_index):
        index_html = {'external': []}
        mock_index.return_value = index_html

        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        actual = filefairy._render_data(date=DATE_10260602)
        expected = [('index.html', '', 'home.html', index_html)]
        self.assertEqual(actual, expected)

        self.assertNotCalled(self.mock_log)

    def test_on_message(self):
        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        response = filefairy._on_message_internal(date=DATE_10260602)
        self.assertEqual(response, Response())

        self.assertNotCalled(self.mock_log)

    @mock.patch('impl.filefairy.filefairy.os.execv')
    def test_reboot(self, mock_execv):
        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        filefairy.reboot(v=True)

        expected = ['python3'] + sys.argv
        mock_execv.assert_called_once_with(sys.executable, expected)
        self.mock_log.assert_called_once_with(logging.DEBUG,
                                              'Rebooting filefairy.')

    @mock.patch.object(Filefairy, '_try_all')
    @mock.patch.object(Filefairy, '_reload_services')
    @mock.patch.object(Filefairy, '_reload_internal')
    def test_reload__base(self, mock_reload, mock_services, mock_try_all):
        response = Response(notify=[Notify.BASE])
        mock_reload.return_value = response

        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        actual = filefairy.reload(*('faketask', ), date=DATE_10260604)
        self.assertEqual(actual, response)

        mock_reload.assert_called_once_with(
            'faketask', True, date=DATE_10260604)
        mock_services.assert_called_once_with()
        mock_try_all.assert_has_calls([
            mock.call('_setup', date=DATE_10260604),
            mock.call('_render', date=DATE_10260604)
        ])
        self.assertNotCalled(self.mock_log)
        self.assertEqual(filefairy.date, DATE_10260604)

    @mock.patch.object(Filefairy, '_try_all')
    @mock.patch.object(Filefairy, '_reload_services')
    @mock.patch.object(Filefairy, '_reload_internal')
    def test_reload__none(self, mock_reload, mock_services, mock_try_all):
        response = Response()
        mock_reload.return_value = response

        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        actual = filefairy.reload(*('faketask', ), date=DATE_10260604)
        self.assertEqual(actual, response)

        mock_reload.assert_called_once_with(
            'faketask', True, date=DATE_10260604)
        mock_services.assert_called_once_with()
        self.assertNotCalled(mock_try_all, self.mock_log)
        self.assertEqual(filefairy.date, DATE_10260602)

    def test_shutdown(self):
        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        filefairy.shutdown(v=True)

        self.mock_log.assert_called_once_with(logging.DEBUG,
                                              'Shutting down filefairy.')
        self.assertFalse(filefairy.keep_running)

    @mock.patch.object(Filefairy, '_try')
    @mock.patch('impl.filefairy.filefairy.time.sleep')
    def test_background(self, mock_sleep, mock_try):
        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)

        mock_sleep.side_effect = functools.partial(set_keep_running, filefairy,
                                                   False)

        thread_ = Thread(target='foo')
        filefairy.threads = [('faketask', thread_)]
        filefairy._background()

        mock_sleep.assert_called_once_with(2)
        mock_try.assert_called_once_with('faketask', 'foo')
        self.assertNotCalled(self.mock_log)
        self.assertEqual(filefairy.threads, [])

    @mock.patch('impl.filefairy.filefairy.websocket.WebSocketApp')
    @mock.patch('impl.filefairy.filefairy.threading.Thread')
    @mock.patch('impl.filefairy.filefairy.rtm_connect')
    @mock.patch.object(Filefairy, '_recv')
    def test_connect(self, mock_recv, mock_rtm, mock_thread, mock_ws):
        mock_rtm.return_value = {'ok': True, 'url': 'wss://...'}
        mock_ws.side_effect = FakeWebSocketApp

        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        filefairy._connect()

        message = '{"type":"message","channel":"ABC","text":"foo"}'
        filefairy.ws.send(message)

        mock_recv.assert_called_once_with(message)
        mock_rtm.assert_called_once_with()
        mock_thread.assert_called_once_with(target=filefairy.ws.run_forever)
        self.assertNotCalled(self.mock_log)

    @mock.patch('impl.filefairy.filefairy.getattr')
    def test_install__exception(self, mock_getattr):
        mock_getattr.side_effect = Exception()

        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)

        module = _module('faketask')
        actual = filefairy._install(
            'faketask', module, 'Faketask', date=DATE_10260604)
        expected = False
        self.assertEqual(actual, expected)

        mock_getattr.assert_called_once_with(module, 'Faketask')
        self.mock_log(logging.ERROR, 'Disabled faketask.', exc_info=True)
        self.assertNotIn('faketask', filefairy.runners)

    @mock.patch('impl.filefairy.filefairy.getattr')
    def test_install__ok(self, mock_getattr):
        mock_getattr.return_value = Faketask

        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)

        module = _module('faketask')
        actual = filefairy._install(
            'faketask', module, 'Faketask', date=DATE_10260604)
        expected = True
        self.assertEqual(actual, expected)

        mock_getattr.assert_called_once_with(module, 'Faketask')
        self.assertNotCalled(self.mock_log)
        self.assertTrue(isinstance(filefairy.runners['faketask'], Faketask))

    @mock.patch.object(Filefairy, '_try_all')
    @mock.patch.object(Filefairy, '_on_message')
    @mock.patch('impl.filefairy.filefairy.datetime_now')
    def test_recv(self, mock_now, mock_on_message, mock_try_all):
        mock_now.return_value = DATE_10260604

        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)

        message = '{"type":"message","channel":"ABC","text":"foo"}'
        filefairy._recv(message)

        obj = json.loads(message)
        mock_now.assert_called_once_with()
        mock_on_message.assert_called_once_with(obj=obj, date=DATE_10260604)
        mock_try_all.assert_called_once_with(
            '_on_message', obj=obj, date=DATE_10260604)
        self.assertNotCalled(self.mock_log)

    @mock.patch.object(Filefairy, '_install')
    @mock.patch('impl.filefairy.filefairy.importlib.import_module')
    def test_reload_internal__exception(self, mock_import, mock_install):
        mock_import.side_effect = Exception()

        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        actual = filefairy._reload_internal(
            'faketask', True, date=DATE_10260604)
        expected = Response()
        self.assertEqual(actual, expected)

        mock_import.assert_called_once_with('tasks.faketask.faketask')
        self.mock_log.assert_called_once_with(
            logging.ERROR, 'Disabled faketask.', exc_info=True)
        self.assertNotCalled(mock_install)

    @mock.patch.object(Filefairy, '_install')
    @mock.patch('impl.filefairy.filefairy.importlib.import_module')
    def test_reload_internal__ok_false(self, mock_import, mock_install):
        module = _module('faketask')
        mock_import.return_value = module
        mock_install.return_value = False

        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        actual = filefairy._reload_internal(
            'faketask', True, date=DATE_10260604)
        expected = Response()
        self.assertEqual(actual, expected)

        mock_import.assert_called_once_with('tasks.faketask.faketask')
        mock_install.assert_called_once_with(
            'faketask', module, 'Faketask', date=DATE_10260604)
        self.assertNotCalled(self.mock_log)

    @mock.patch.object(Filefairy, '_install')
    @mock.patch('impl.filefairy.filefairy.importlib.import_module')
    def test_reload_internal__ok_log_true(self, mock_import, mock_install):
        module = _module('faketask')
        mock_import.return_value = module
        mock_install.return_value = True

        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        actual = filefairy._reload_internal(
            'faketask', True, date=DATE_10260604)
        msg = 'Reloaded faketask.'
        expected = Response(notify=[Notify.BASE], debug=[Debug(msg=msg)])
        self.assertEqual(actual, expected)

        mock_import.assert_called_once_with('tasks.faketask.faketask')
        mock_install.assert_called_once_with(
            'faketask', module, 'Faketask', date=DATE_10260604)
        self.mock_log.assert_called_once_with(logging.INFO, msg)

    @mock.patch.object(Filefairy, '_install')
    @mock.patch('impl.filefairy.filefairy.importlib.import_module')
    def test_reload_internal__ok_log_false(self, mock_import, mock_install):
        module = _module('faketask')
        mock_import.return_value = module
        mock_install.return_value = True

        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        actual = filefairy._reload_internal(
            'faketask', False, date=DATE_10260604)
        expected = Response(notify=[Notify.BASE])
        self.assertEqual(actual, expected)

        mock_import.assert_called_once_with('tasks.faketask.faketask')
        mock_install.assert_called_once_with(
            'faketask', module, 'Faketask', date=DATE_10260604)
        self.assertNotCalled(self.mock_log)

    @mock.patch('impl.filefairy.filefairy.reload_services')
    def test_reload_services__exception(self, mock_reload):
        mock_reload.side_effect = Exception()

        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)

        filefairy._reload_services()

        mock_reload.assert_called_once_with()
        self.mock_log.assert_called_once_with(
            logging.ERROR, 'Error reloading services.', exc_info=True)

    @mock.patch('impl.filefairy.filefairy.reload_services')
    def test_reload_internal__ok(self, mock_reload):
        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)

        filefairy._reload_services()

        mock_reload.assert_called_once_with()
        self.assertNotCalled(self.mock_log)

    @mock.patch.object(Filefairy, '_try_all')
    @mock.patch.object(Filefairy, '_try')
    def test_response__empty(self, mock_try, mock_try_all):
        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        filefairy.runners['faketask'] = self.create_task(DATE_10260602)

        response = Response()
        filefairy._response('faketask', response, date=DATE_10260604)

        self.assertNotCalled(mock_try, mock_try_all, self.mock_log)
        self.assertEqual(filefairy.date, DATE_10260602)
        self.assertEqual(filefairy.runners['faketask'].date, DATE_10260602)
        self.assertFalse(len(filefairy.threads))

    @mock.patch.object(Filefairy, '_try_all')
    @mock.patch.object(Filefairy, '_try')
    def test_response__notify_base(self, mock_try, mock_try_all):
        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        filefairy.runners['faketask'] = self.create_task(DATE_10260602)

        response = Response(notify=[Notify.BASE])
        filefairy._response('faketask', response, date=DATE_10260604)

        self.assertNotCalled(mock_try, mock_try_all, self.mock_log)
        self.assertEqual(filefairy.date, DATE_10260604)
        self.assertEqual(filefairy.runners['faketask'].date, DATE_10260604)
        self.assertFalse(len(filefairy.threads))

    @mock.patch.object(Filefairy, '_try_all')
    @mock.patch.object(Filefairy, '_try')
    def test_response__notify_other(self, mock_try, mock_try_all):
        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        filefairy.runners['faketask'] = self.create_task(DATE_10260602)

        response = Response(notify=[Notify.OTHER])
        filefairy._response('faketask', response, date=DATE_10260604)

        mock_try_all.assert_called_once_with(
            '_notify', notify=Notify.OTHER, date=DATE_10260604)
        self.assertNotCalled(mock_try, self.mock_log)
        self.assertEqual(filefairy.date, DATE_10260604)
        self.assertEqual(filefairy.runners['faketask'].date, DATE_10260604)
        self.assertFalse(len(filefairy.threads))

    @mock.patch.object(Filefairy, '_try_all')
    @mock.patch.object(Filefairy, '_try')
    def test_response__shadow(self, mock_try, mock_try_all):
        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        filefairy.runners['faketask'] = self.create_task(DATE_10260602)

        shadow = Shadow(destination='bar', key='faketask.baz')
        response = Response(shadow=[shadow])
        filefairy._response('faketask', response, date=DATE_10260604)

        mock_try.assert_called_once_with(
            'bar', '_shadow', shadow=shadow, date=DATE_10260604)
        self.assertNotCalled(mock_try_all, self.mock_log)
        self.assertEqual(filefairy.date, DATE_10260602)
        self.assertEqual(filefairy.runners['faketask'].date, DATE_10260602)
        self.assertFalse(len(filefairy.threads))

    @mock.patch.object(Filefairy, '_try_all')
    @mock.patch.object(Filefairy, '_try')
    def test_response__thread(self, mock_try, mock_try_all):
        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        filefairy.runners['faketask'] = self.create_task(DATE_10260602)

        thread_ = Thread(target='faketask')
        response = Response(thread_=[thread_])
        filefairy._response('faketask', response, date=DATE_10260604)

        self.assertNotCalled(mock_try, mock_try_all, self.mock_log)
        self.assertEqual(filefairy.date, DATE_10260602)
        self.assertEqual(filefairy.runners['faketask'].date, DATE_10260602)
        self.assertCountEqual(filefairy.threads, [('faketask', thread_)])

    @mock.patch.object(Filefairy, '_try_all')
    @mock.patch.object(Filefairy, '_try')
    @mock.patch.object(Filefairy, '_render')
    @mock.patch('impl.filefairy.filefairy.datetime_now')
    def test_run__day(self, mock_now, mock_render, mock_try, mock_try_all):
        mock_now.return_value = DATE_10260604

        dashboard = self.create_dashboard(DATE_10250007)
        filefairy = self.create_filefairy(DATE_10250007, dashboard, reference)
        filefairy.day = 25
        filefairy.runners['git'] = self.create_task(DATE_10260602)

        filefairy._run()

        notify = Notify.FILEFAIRY_DAY
        mock_now.assert_called_once_with()
        mock_try_all.assert_has_calls([
            mock.call('_run', date=DATE_10260604),
            mock.call('_notify', notify=notify, date=DATE_10260604)
        ])
        self.assertNotCalled(mock_render, mock_try, self.mock_log)
        self.assertEqual(filefairy.day, 26)

    @mock.patch.object(Filefairy, '_try_all')
    @mock.patch.object(Filefairy, '_try')
    @mock.patch.object(Filefairy, '_render')
    @mock.patch('impl.filefairy.filefairy.datetime_now')
    def test_run__noop(self, mock_now, mock_render, mock_try, mock_try_all):
        mock_now.return_value = DATE_10260604

        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        filefairy.day = 26
        filefairy.runners['git'] = self.create_task(DATE_10260602)

        filefairy._run()

        mock_now.assert_called_once_with()
        mock_try_all.assert_called_once_with('_run', date=DATE_10260604)
        self.assertNotCalled(mock_render, mock_try, self.mock_log)
        self.assertEqual(filefairy.day, 26)

    @mock.patch.object(Filefairy, '_try_all')
    @mock.patch.object(Filefairy, '_try')
    @mock.patch.object(Filefairy, '_render')
    @mock.patch('impl.filefairy.filefairy.datetime_now')
    def test_run__render(self, mock_now, mock_render, mock_try, mock_try_all):
        mock_now.return_value = DATE_10260604

        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        filefairy.day = 26
        filefairy.runners['git'] = self.create_task(DATE_10260602)

        mock_try_all.side_effect = functools.partial(set_date, filefairy)

        filefairy._run()

        # notify = Notify.FILEFAIRY_DEPLOY
        mock_now.assert_called_once_with()
        mock_render.assert_called_once_with(date=DATE_10260604)
        # mock_try.assert_called_once_with(
        #     'git', '_notify', notify=notify, date=DATE_10260604)
        mock_try_all.assert_called_once_with('_run', date=DATE_10260604)
        self.assertNotCalled(self.mock_log)
        self.assertEqual(filefairy.day, 26)

    @mock.patch.object(Filefairy, '_try_all')
    @mock.patch.object(Filefairy, '_reload_services')
    @mock.patch.object(Filefairy, '_reload_internal')
    @mock.patch('impl.filefairy.filefairy.listdirs')
    def test_setup(self, mock_listdirs, mock_reload, mock_services,
                   mock_try_all):
        mock_listdirs.return_value = ['faketask']

        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        filefairy._setup(date=DATE_10260604)

        mock_listdirs.assert_called_once_with(TASKS_DIR)
        mock_reload.assert_called_once_with(
            'faketask', False, date=DATE_10260604)
        mock_services.assert_called_once_with()
        mock_try_all.assert_has_calls([
            mock.call('_setup', date=DATE_10260604),
            mock.call('_render', date=DATE_10260604)
        ])
        self.assertNotCalled(self.mock_log)

    @mock.patch('impl.filefairy.filefairy.threading.Thread')
    @mock.patch('impl.filefairy.filefairy.time.sleep')
    @mock.patch.object(Filefairy, '_run')
    @mock.patch.object(Filefairy, '_connect')
    def test_start__initial(self, mock_connect, mock_run, mock_sleep,
                            mock_thread):
        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)

        mock_sleep.side_effect = functools.partial(set_keep_running, filefairy,
                                                   False)

        filefairy._start(None)

        mock_connect.assert_called_once_with()
        mock_run.assert_called_once_with()
        mock_sleep.assert_called_once_with(2)
        mock_thread.assert_called_once_with(target=filefairy._background)
        self.assertNotCalled(self.mock_log)

    @mock.patch('impl.filefairy.filefairy.threading.Thread')
    @mock.patch('impl.filefairy.filefairy.time.sleep')
    @mock.patch.object(Filefairy, '_run')
    @mock.patch.object(Filefairy, '_connect')
    def test_start__running(self, mock_connect, mock_run, mock_sleep,
                            mock_thread):
        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)

        mock_sleep.side_effect = functools.partial(set_keep_running, filefairy,
                                                   False)

        filefairy.bg = BG
        filefairy.ws = FakeWebSocketApp(url='wss://...')
        filefairy._start(None)

        mock_run.assert_called_once_with()
        mock_sleep.assert_called_once_with(2)
        self.assertNotCalled(mock_connect, mock_thread, self.mock_log)

    @mock.patch.object(Faketask, '_run')
    @mock.patch.object(Filefairy, '_response')
    def test_try__exception(self, mock_response, mock_run):
        mock_run.side_effect = Exception()

        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        filefairy.runners['faketask'] = self.create_task(DATE_10260602)

        filefairy._try('faketask', '_run', date=DATE_10260604)

        mock_run.assert_called_once_with(date=DATE_10260604)
        self.mock_log.assert_called_once_with(
            logging.ERROR, 'Disabled faketask.', exc_info=True)
        self.assertNotCalled(mock_response)
        self.assertEqual(filefairy.runners['faketask'].date, DATE_10260604)
        self.assertEqual(filefairy.runners['faketask'].ok, False)

    @mock.patch.object(Faketask, '_run')
    @mock.patch.object(Filefairy, '_response')
    def test_try__response(self, mock_response, mock_run):
        response = Response(notify=[Notify.BASE])
        mock_run.return_value = response

        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        filefairy.runners['faketask'] = self.create_task(DATE_10260602)

        filefairy._try('faketask', '_run', date=DATE_10260604)

        mock_response.assert_called_once_with(
            'faketask', response, date=DATE_10260604)
        mock_run.assert_called_once_with(date=DATE_10260604)
        self.assertNotCalled(self.mock_log)
        self.assertEqual(filefairy.runners['faketask'].date, DATE_10260602)
        self.assertEqual(filefairy.runners['faketask'].ok, True)

    @mock.patch.object(Faketask, '_run')
    @mock.patch.object(Filefairy, '_response')
    def test_try__uncallable(self, mock_response, mock_run):
        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        filefairy.runners['faketask'] = self.create_task(DATE_10260602)

        filefairy._try('faketask', 'bar', date=DATE_10260604)

        self.assertNotCalled(mock_response, mock_run, self.mock_log)

    @mock.patch.object(Faketask, '_run')
    @mock.patch.object(Filefairy, '_response')
    def test_try__unhappy(self, mock_response, mock_run):
        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)

        task = self.create_task(DATE_10260602)
        task.ok = False
        filefairy.runners['faketask'] = task

        filefairy._try('faketask', '_run', date=DATE_10260604)

        self.assertNotCalled(mock_response, mock_run, self.mock_log)

    @mock.patch.object(Faketask, '_run')
    @mock.patch.object(Filefairy, '_response')
    def test_try__unregistered(self, mock_response, mock_run):
        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)

        filefairy._try('faketask', '_run', date=DATE_10260604)

        self.assertNotCalled(mock_response, mock_run, self.mock_log)

    @mock.patch.object(Filefairy, '_try')
    def test_try_all(self, mock_try):
        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        filefairy.runners['faketask'] = self.create_task(DATE_10260602)

        filefairy._try_all('_run', date=DATE_10260604)

        mock_try.assert_has_calls([
            mock.call('dashboard', '_run', date=DATE_10260604),
            mock.call('faketask', '_run', date=DATE_10260604)
        ])
        self.assertNotCalled(self.mock_log)

    @mock.patch('impl.filefairy.filefairy.sitelinks')
    def test_index_html(self, mock_sitelinks):
        sitelinks = [topper('Site Links')]
        mock_sitelinks.return_value = sitelinks

        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)

        actual = filefairy._index_html(date=DATE_10260602)
        expected = {'sitelinks': sitelinks}
        self.assertEqual(actual, expected)
        self.assertNotCalled(self.mock_log)


if __name__ in ['__main__', 'impl.filefairy.filefairy_test']:
    dashboard = Dashboard(date=DATE_10260602, e=ENV)
    reference = Reference(date=DATE_10260602)
    main(
        FilefairyTest,
        Filefairy,
        'impl.filefairy',
        'impl/filefairy', {},
        __name__ == '__main__',
        date=DATE_10260602,
        d=dashboard,
        e=ENV,
        r=reference)
