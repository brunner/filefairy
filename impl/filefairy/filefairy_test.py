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
from types_.thread_.thread_ import Thread  # noqa

BG = threading.Thread()
ENV = env()

DATE_10250007 = datetime_datetime_pst(1985, 10, 25, 0, 7)
DATE_10260602 = datetime_datetime_pst(1985, 10, 26, 6, 2, 30)
DATE_10260604 = datetime_datetime_pst(1985, 10, 26, 6, 4)

TASKS_DIR = re.sub(r'/impl/filefairy', '/tasks', _path)


def create_module(name):
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
        log_patch = mock.patch('impl.filefairy.filefairy._logger.log')
        self.addCleanup(log_patch.stop)
        self.log_ = log_patch.start()

        open_patch = mock.patch('common.io_.io_.open', create=True)
        self.addCleanup(open_patch.stop)
        self.open_ = open_patch.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.open_.side_effect = [mo.return_value]

    def create_dashboard(self, date):
        self.init_mocks({})
        return Dashboard(date=date, e=ENV)

    def create_reference(self, date):
        self.init_mocks({})
        return Reference(date=date)

    def create_filefairy(self, date, dashboard, reference):
        self.init_mocks({})
        filefairy = Filefairy(date=date, d=dashboard, e=ENV, r=reference)
        filefairy.renderables(['faketask'])

        self.assertNotCalled(self.log_)
        self.assertEqual(filefairy.date, date)
        self.assertEqual(filefairy.day, date.day)
        self.assertEqual(filefairy.original, date)

        return filefairy

    def create_task(self, date):
        task = Faketask(date=date, e=ENV)

        self.assertNotCalled(self.log_)

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
        self.assertNotCalled(self.log_)

    @mock.patch.object(Filefairy, 'get_home_html')
    def test_render_data(self, get_home_html_):
        home_html = {'external': []}
        get_home_html_.return_value = home_html

        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        actual = filefairy._render_data(date=DATE_10260602)
        expected = [('index.html', '', 'home.html', home_html)]
        self.assertEqual(actual, expected)

        self.assertNotCalled(self.log_)

    def test_on_message(self):
        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        response = filefairy._on_message_internal(date=DATE_10260602)
        self.assertEqual(response, Response())

        self.assertNotCalled(self.log_)

    @mock.patch('impl.filefairy.filefairy.os.execv')
    def test_reboot(self, execv_):
        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        filefairy.reboot(v=True)

        expected = ['python3'] + sys.argv
        execv_.assert_called_once_with(sys.executable, expected)
        self.log_.assert_called_once_with(logging.DEBUG,
                                          'Rebooting filefairy.')

    @mock.patch.object(Filefairy, 'try_all')
    @mock.patch.object(Filefairy, 'reload_services')
    @mock.patch.object(Filefairy, 'reload_internal')
    def test_reload__base(self, reload_internal_, reload_services_, try_all_):
        response = Response(notify=[Notify.BASE])
        reload_internal_.return_value = response

        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        actual = filefairy.reload(*('faketask', ), date=DATE_10260604)
        self.assertEqual(actual, response)
        self.assertEqual(filefairy.date, DATE_10260604)

        reload_internal_.assert_called_once_with('faketask',
                                                 True,
                                                 date=DATE_10260604)
        reload_services_.assert_called_once_with()
        try_all_.assert_has_calls([
            mock.call('_setup', date=DATE_10260604),
            mock.call('_render', date=DATE_10260604)
        ])
        self.assertNotCalled(self.log_)

    @mock.patch.object(Filefairy, 'try_all')
    @mock.patch.object(Filefairy, 'reload_services')
    @mock.patch.object(Filefairy, 'reload_internal')
    def test_reload__none(self, reload_internal_, reload_services_, try_all_):
        response = Response()
        reload_internal_.return_value = response

        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        actual = filefairy.reload(*('faketask', ), date=DATE_10260604)
        self.assertEqual(actual, response)
        self.assertEqual(filefairy.date, DATE_10260602)

        reload_internal_.assert_called_once_with('faketask',
                                                 True,
                                                 date=DATE_10260604)
        reload_services_.assert_called_once_with()
        self.assertNotCalled(try_all_, self.log_)

    def test_shutdown(self):
        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        filefairy.shutdown(v=True)
        self.assertFalse(filefairy.keep_running)

        self.log_.assert_called_once_with(logging.DEBUG,
                                          'Shutting down filefairy.')

    @mock.patch.object(Filefairy, 'try_')
    @mock.patch('impl.filefairy.filefairy.time.sleep')
    def test_background(self, sleep_, try__):
        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)

        sleep_.side_effect = functools.partial(set_keep_running, filefairy,
                                               False)

        thread_ = Thread(target='foo')
        filefairy.threads = [('faketask', thread_)]
        filefairy.background()
        self.assertEqual(filefairy.threads, [])

        sleep_.assert_called_once_with(2)
        try__.assert_called_once_with('faketask', 'foo')
        self.assertNotCalled(self.log_)

    @mock.patch('impl.filefairy.filefairy.websocket.WebSocketApp')
    @mock.patch('impl.filefairy.filefairy.threading.Thread')
    @mock.patch('impl.filefairy.filefairy.rtm_connect')
    @mock.patch.object(Filefairy, 'recv')
    def test_connect(self, recv_, rtm_connect_, thread_, websocketapp_):
        rtm_connect_.return_value = {'ok': True, 'url': 'wss://...'}
        websocketapp_.side_effect = FakeWebSocketApp

        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        filefairy.connect()

        message = '{"type":"message","channel":"ABC","text":"foo"}'
        filefairy.ws.send(message)

        recv_.assert_called_once_with(message)
        rtm_connect_.assert_called_once_with()
        thread_.assert_called_once_with(target=filefairy.ws.run_forever)
        self.assertNotCalled(self.log_)

    @mock.patch.object(Filefairy, 'try_all')
    @mock.patch.object(Filefairy, 'try_')
    def test_handle_response__empty(self, try_, try_all_):
        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        filefairy.runners['faketask'] = self.create_task(DATE_10260602)

        response = Response()
        filefairy.handle_response('faketask', response, date=DATE_10260604)
        self.assertEqual(filefairy.date, DATE_10260602)
        self.assertEqual(filefairy.runners['faketask'].date, DATE_10260602)
        self.assertFalse(len(filefairy.threads))

        self.assertNotCalled(try_, try_all_, self.log_)

    @mock.patch.object(Filefairy, 'try_all')
    @mock.patch.object(Filefairy, 'try_')
    def test_handle_response__notify_base(self, try_, try_all_):
        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        filefairy.runners['faketask'] = self.create_task(DATE_10260602)

        response = Response(notify=[Notify.BASE])
        filefairy.handle_response('faketask', response, date=DATE_10260604)
        self.assertEqual(filefairy.date, DATE_10260604)
        self.assertEqual(filefairy.runners['faketask'].date, DATE_10260604)
        self.assertFalse(len(filefairy.threads))

        self.assertNotCalled(try_, try_all_, self.log_)

    @mock.patch.object(Filefairy, 'try_all')
    @mock.patch.object(Filefairy, 'try_')
    def test_handle_response__notify_other(self, try_, try_all_):
        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        filefairy.runners['faketask'] = self.create_task(DATE_10260602)

        response = Response(notify=[Notify.OTHER])
        filefairy.handle_response('faketask', response, date=DATE_10260604)
        self.assertEqual(filefairy.date, DATE_10260604)
        self.assertEqual(filefairy.runners['faketask'].date, DATE_10260604)
        self.assertFalse(len(filefairy.threads))

        try_all_.assert_called_once_with('_notify',
                                         notify=Notify.OTHER,
                                         date=DATE_10260604)
        self.assertNotCalled(try_, self.log_)

    @mock.patch.object(Filefairy, 'try_all')
    @mock.patch.object(Filefairy, 'try_')
    def test_handle_response__thread(self, try_, try_all_):
        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        filefairy.runners['faketask'] = self.create_task(DATE_10260602)

        thread_ = Thread(target='faketask')
        response = Response(thread_=[thread_])
        filefairy.handle_response('faketask', response, date=DATE_10260604)
        self.assertEqual(filefairy.date, DATE_10260602)
        self.assertEqual(filefairy.runners['faketask'].date, DATE_10260602)
        self.assertCountEqual(filefairy.threads, [('faketask', thread_)])

        self.assertNotCalled(try_, try_all_, self.log_)

    @mock.patch('impl.filefairy.filefairy.getattr')
    def test_install__exception(self, getattr_):
        getattr_.side_effect = Exception()

        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)

        module = create_module('faketask')
        actual = filefairy.install('faketask',
                                   module,
                                   'Faketask',
                                   date=DATE_10260604)
        expected = False
        self.assertEqual(actual, expected)
        self.assertNotIn('faketask', filefairy.runners)

        getattr_.assert_called_once_with(module, 'Faketask')
        self.log_(logging.ERROR, 'Disabled faketask.', exc_info=True)

    @mock.patch('impl.filefairy.filefairy.getattr')
    def test_install__ok(self, getattr_):
        getattr_.return_value = Faketask

        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)

        module = create_module('faketask')
        actual = filefairy.install('faketask',
                                   module,
                                   'Faketask',
                                   date=DATE_10260604)
        expected = True
        self.assertEqual(actual, expected)
        self.assertTrue(isinstance(filefairy.runners['faketask'], Faketask))

        getattr_.assert_called_once_with(module, 'Faketask')
        self.assertNotCalled(self.log_)

    @mock.patch.object(Filefairy, 'try_all')
    @mock.patch.object(Filefairy, '_on_message')
    @mock.patch('impl.filefairy.filefairy.datetime_now')
    def test_recv(self, datetime_now_, _on_message_, try_all_):
        datetime_now_.return_value = DATE_10260604

        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)

        message = '{"type":"message","channel":"ABC","text":"foo"}'
        filefairy.recv(message)

        obj = json.loads(message)
        datetime_now_.assert_called_once_with()
        _on_message_.assert_called_once_with(obj=obj, date=DATE_10260604)
        try_all_.assert_called_once_with('_on_message',
                                         obj=obj,
                                         date=DATE_10260604)
        self.assertNotCalled(self.log_)

    @mock.patch.object(Filefairy, 'install')
    @mock.patch('impl.filefairy.filefairy.importlib.import_module')
    def test_reload_internal__exception(self, import_module_, install_):
        import_module_.side_effect = Exception()

        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        actual = filefairy.reload_internal('faketask',
                                           True,
                                           date=DATE_10260604)
        expected = Response()
        self.assertEqual(actual, expected)

        import_module_.assert_called_once_with('tasks.faketask.faketask')
        self.log_.assert_called_once_with(logging.ERROR,
                                          'Disabled faketask.',
                                          exc_info=True)
        self.assertNotCalled(install_)

    @mock.patch.object(Filefairy, 'install')
    @mock.patch('impl.filefairy.filefairy.importlib.import_module')
    def test_reload_internal__ok_false(self, import_module_, install_):
        module = create_module('faketask')
        import_module_.return_value = module
        install_.return_value = False

        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        actual = filefairy.reload_internal('faketask',
                                           True,
                                           date=DATE_10260604)
        expected = Response()
        self.assertEqual(actual, expected)

        import_module_.assert_called_once_with('tasks.faketask.faketask')
        install_.assert_called_once_with('faketask',
                                         module,
                                         'Faketask',
                                         date=DATE_10260604)
        self.assertNotCalled(self.log_)

    @mock.patch.object(Filefairy, 'install')
    @mock.patch('impl.filefairy.filefairy.importlib.import_module')
    def test_reload_internal__ok_log_true(self, import_module_, install_):
        module = create_module('faketask')
        import_module_.return_value = module
        install_.return_value = True

        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        actual = filefairy.reload_internal('faketask',
                                           True,
                                           date=DATE_10260604)
        msg = 'Reloaded faketask.'
        expected = Response(notify=[Notify.BASE], debug=[Debug(msg=msg)])
        self.assertEqual(actual, expected)

        import_module_.assert_called_once_with('tasks.faketask.faketask')
        install_.assert_called_once_with('faketask',
                                         module,
                                         'Faketask',
                                         date=DATE_10260604)
        self.log_.assert_called_once_with(logging.INFO, msg)

    @mock.patch.object(Filefairy, 'install')
    @mock.patch('impl.filefairy.filefairy.importlib.import_module')
    def test_reload_internal__ok_log_false(self, import_module_, install_):
        module = create_module('faketask')
        import_module_.return_value = module
        install_.return_value = True

        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        actual = filefairy.reload_internal('faketask',
                                           False,
                                           date=DATE_10260604)
        expected = Response(notify=[Notify.BASE])
        self.assertEqual(actual, expected)

        import_module_.assert_called_once_with('tasks.faketask.faketask')
        install_.assert_called_once_with('faketask',
                                         module,
                                         'Faketask',
                                         date=DATE_10260604)
        self.assertNotCalled(self.log_)

    @mock.patch('impl.filefairy.filefairy.reload_services')
    def test_reload_services__exception(self, reload_services_):
        reload_services_.side_effect = Exception()

        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)

        filefairy.reload_services()

        reload_services_.assert_called_once_with()
        self.log_.assert_called_once_with(logging.ERROR,
                                          'Error reloading services.',
                                          exc_info=True)

    @mock.patch('impl.filefairy.filefairy.reload_services')
    def test_reload_internal__ok(self, reload_services_):
        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)

        filefairy.reload_services()

        reload_services_.assert_called_once_with()
        self.assertNotCalled(self.log_)

    @mock.patch.object(Filefairy, 'try_all')
    @mock.patch.object(Filefairy, 'try_')
    @mock.patch.object(Filefairy, '_render')
    @mock.patch('impl.filefairy.filefairy.datetime_now')
    def test_run__day(self, datetime_now_, _render_, try_, try_all_):
        datetime_now_.return_value = DATE_10260604

        dashboard = self.create_dashboard(DATE_10250007)
        filefairy = self.create_filefairy(DATE_10250007, dashboard, reference)
        filefairy.day = 25
        filefairy.runners['git'] = self.create_task(DATE_10260602)

        filefairy.run()
        self.assertEqual(filefairy.day, 26)

        notify = Notify.FILEFAIRY_DAY
        datetime_now_.assert_called_once_with()
        try_all_.assert_has_calls([
            mock.call('_run', date=DATE_10260604),
            mock.call('_notify', notify=notify, date=DATE_10260604)
        ])
        self.assertNotCalled(_render_, try_, self.log_)

    @mock.patch.object(Filefairy, 'try_all')
    @mock.patch.object(Filefairy, 'try_')
    @mock.patch.object(Filefairy, '_render')
    @mock.patch('impl.filefairy.filefairy.datetime_now')
    def test_run__noop(self, datetime_now_, _render_, try_, try_all_):
        datetime_now_.return_value = DATE_10260604

        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        filefairy.day = 26
        filefairy.runners['git'] = self.create_task(DATE_10260602)

        filefairy.run()
        self.assertEqual(filefairy.day, 26)

        datetime_now_.assert_called_once_with()
        try_all_.assert_called_once_with('_run', date=DATE_10260604)
        self.assertNotCalled(_render_, try_, self.log_)

    @mock.patch.object(Filefairy, 'try_all')
    @mock.patch.object(Filefairy, 'try_')
    @mock.patch.object(Filefairy, '_render')
    @mock.patch('impl.filefairy.filefairy.datetime_now')
    def test_run__render(self, datetime_now_, _render_, try_, try_all_):
        datetime_now_.return_value = DATE_10260604

        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        filefairy.day = 26
        filefairy.runners['git'] = self.create_task(DATE_10260602)

        try_all_.side_effect = functools.partial(set_date, filefairy)

        filefairy.run()
        self.assertEqual(filefairy.day, 26)

        # notify = Notify.FILEFAIRY_DEPLOY
        datetime_now_.assert_called_once_with()
        _render_.assert_called_once_with(date=DATE_10260604)
        # try_.assert_called_once_with('git',
        #                              '_notify',
        #                              notify=notify,
        #                              date=DATE_10260604)
        try_all_.assert_called_once_with('_run', date=DATE_10260604)
        self.assertNotCalled(self.log_)

    @mock.patch.object(Filefairy, 'try_all')
    @mock.patch.object(Filefairy, 'reload_services')
    @mock.patch.object(Filefairy, 'reload_internal')
    @mock.patch('impl.filefairy.filefairy.listdirs')
    def test_setup(self, listdirs_, reload_internal_, reload_services_,
                   try_all_):
        listdirs_.return_value = ['faketask']

        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        filefairy.setup(date=DATE_10260604)

        listdirs_.assert_called_once_with(TASKS_DIR)
        reload_internal_.assert_called_once_with('faketask',
                                                 False,
                                                 date=DATE_10260604)
        reload_services_.assert_called_once_with()
        try_all_.assert_has_calls([
            mock.call('_setup', date=DATE_10260604),
            mock.call('_render', date=DATE_10260604)
        ])
        self.assertNotCalled(self.log_)

    @mock.patch('impl.filefairy.filefairy.threading.Thread')
    @mock.patch('impl.filefairy.filefairy.time.sleep')
    @mock.patch.object(Filefairy, 'run')
    @mock.patch.object(Filefairy, 'connect')
    def test_start__initial(self, connect_, run_, sleep_, thread_):
        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)

        sleep_.side_effect = functools.partial(set_keep_running, filefairy,
                                               False)

        filefairy.start(None)

        connect_.assert_called_once_with()
        run_.assert_called_once_with()
        sleep_.assert_called_once_with(2)
        thread_.assert_called_once_with(target=filefairy.background)
        self.assertNotCalled(self.log_)

    @mock.patch('impl.filefairy.filefairy.threading.Thread')
    @mock.patch('impl.filefairy.filefairy.time.sleep')
    @mock.patch.object(Filefairy, 'run')
    @mock.patch.object(Filefairy, 'connect')
    def test_start__running(self, connect_, run_, sleep_, thread_):
        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)

        sleep_.side_effect = functools.partial(set_keep_running, filefairy,
                                               False)

        filefairy.bg = BG
        filefairy.ws = FakeWebSocketApp(url='wss://...')
        filefairy.start(None)

        run_.assert_called_once_with()
        sleep_.assert_called_once_with(2)
        self.assertNotCalled(connect_, thread_, self.log_)

    @mock.patch.object(Faketask, '_run')
    @mock.patch.object(Filefairy, 'handle_response')
    def test_try__exception(self, handle_response_, run_):
        run_.side_effect = Exception()

        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        filefairy.runners['faketask'] = self.create_task(DATE_10260602)

        filefairy.try_('faketask', '_run', date=DATE_10260604)
        self.assertEqual(filefairy.runners['faketask'].date, DATE_10260604)
        self.assertEqual(filefairy.runners['faketask'].ok, False)

        run_.assert_called_once_with(date=DATE_10260604)
        self.log_.assert_called_once_with(logging.ERROR,
                                          'Disabled faketask.',
                                          exc_info=True)
        self.assertNotCalled(handle_response_)

    @mock.patch.object(Faketask, '_run')
    @mock.patch.object(Filefairy, 'handle_response')
    def test_try__response(self, handle_response_, run_):
        response = Response(notify=[Notify.BASE])
        run_.return_value = response

        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        filefairy.runners['faketask'] = self.create_task(DATE_10260602)

        filefairy.try_('faketask', '_run', date=DATE_10260604)
        self.assertEqual(filefairy.runners['faketask'].date, DATE_10260602)
        self.assertEqual(filefairy.runners['faketask'].ok, True)

        handle_response_.assert_called_once_with('faketask',
                                                 response,
                                                 date=DATE_10260604)
        run_.assert_called_once_with(date=DATE_10260604)
        self.assertNotCalled(self.log_)

    @mock.patch.object(Faketask, '_run')
    @mock.patch.object(Filefairy, 'handle_response')
    def test_try__uncallable(self, handle_response_, run_):
        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        filefairy.runners['faketask'] = self.create_task(DATE_10260602)

        filefairy.try_('faketask', 'bar', date=DATE_10260604)

        self.assertNotCalled(handle_response_, run_, self.log_)

    @mock.patch.object(Faketask, '_run')
    @mock.patch.object(Filefairy, 'handle_response')
    def test_try__unhappy(self, handle_response_, run_):
        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)

        task = self.create_task(DATE_10260602)
        task.ok = False
        filefairy.runners['faketask'] = task

        filefairy.try_('faketask', '_run', date=DATE_10260604)

        self.assertNotCalled(handle_response_, run_, self.log_)

    @mock.patch.object(Faketask, '_run')
    @mock.patch.object(Filefairy, 'handle_response')
    def test_try__unregistered(self, handle_response_, run_):
        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)

        filefairy.try_('faketask', '_run', date=DATE_10260604)

        self.assertNotCalled(handle_response_, run_, self.log_)

    @mock.patch.object(Filefairy, 'try_')
    def test_try_all(self, try_):
        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)
        filefairy.runners['faketask'] = self.create_task(DATE_10260602)

        filefairy.try_all('_run', date=DATE_10260604)

        try_.assert_has_calls([
            mock.call('dashboard', '_run', date=DATE_10260604),
            mock.call('faketask', '_run', date=DATE_10260604)
        ])
        self.assertNotCalled(self.log_)

    @mock.patch('impl.filefairy.filefairy.sitelinks')
    def test_get_home_html(self, sitelinks_):
        sitelinks = [topper('Site Links')]
        sitelinks_.return_value = sitelinks

        dashboard = self.create_dashboard(DATE_10260602)
        reference = self.create_reference(DATE_10260602)
        filefairy = self.create_filefairy(DATE_10260602, dashboard, reference)

        actual = filefairy.get_home_html(date=DATE_10260602)
        expected = {'sitelinks': sitelinks}
        self.assertEqual(actual, expected)

        sitelinks_.assert_called_once_with(Filefairy._href())
        self.assertNotCalled(self.log_)


if __name__ in ['__main__', 'impl.filefairy.filefairy_test']:
    dashboard = Dashboard(date=DATE_10260602, e=ENV)
    reference = Reference(date=DATE_10260602)
    main(FilefairyTest,
         Filefairy,
         'impl.filefairy',
         'impl/filefairy', {},
         __name__ == '__main__',
         date=DATE_10260602,
         d=dashboard,
         e=ENV,
         r=reference)
