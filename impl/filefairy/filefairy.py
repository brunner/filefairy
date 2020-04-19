#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import json
import importlib
import logging
import os
import re
import sys
import threading
import time
import websocket

_logger = logging.getLogger('filefairy')
_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/impl/filefairy', '', _path))

from api.messageable.messageable import Messageable  # noqa
from api.runnable.runnable import Runnable  # noqa
from api.renderable.renderable import Renderable  # noqa
from common.datetime_.datetime_ import datetime_now  # noqa
from common.datetime_.datetime_ import encode_datetime  # noqa
from common.datetime_.datetime_ import timestamp  # noqa
from common.elements.elements import sitelinks  # noqa
from common.jinja2_.jinja2_ import env  # noqa
from common.messageable.messageable import messageable  # noqa
from common.os_.os_ import listdirs  # noqa
from common.reference.reference import set_reference  # noqa
from common.service.service import reload_services  # noqa
from common.slack.slack import rtm_connect  # noqa
from impl.dashboard.dashboard import Dashboard  # noqa
from impl.dashboard.dashboard import LoggingHandler  # noqa
from impl.reference.reference import Reference  # noqa
from types_.debug.debug import Debug  # noqa
from types_.notify.notify import Notify  # noqa
from types_.response.response import Response  # noqa

TASKS_DIR = re.sub(r'/impl/filefairy', '/tasks', _path)


class Filefairy(Messageable, Renderable):
    """The main app implementation."""
    def __init__(self, **kwargs):
        """Create a Filefairy object.

        Attributes:
            bg: Reference to the app's background thread.
            date: Date object describing the current datetime.
            day: Number describing the current day.
            keep_running: Coordinate shutdown of the various threads.
            lock: Synchronize some thread behavior.
            original: Backup copy of date, to determine when it changes.
            runners: List of Runnable instances belonging to the app.
            sleep: Duration to wait between repetitive task calls.
            threads: List of queued Thread instances to run in the background.
            ws: Reference to the app's WebSocket object.
        """
        date = kwargs.pop('date')
        d = kwargs.pop('d')
        r = kwargs.pop('r')
        super(Filefairy, self).__init__(**kwargs)

        self.bg = None
        self.date = date
        self.day = date.day
        self.keep_running = True
        self.original = date
        self.renderables_ = []
        self.runners = {'dashboard': d, 'reference': r}
        self.sleep = 2  # TODO: change back to 60 after finishing refactors.
        self.threads = []
        self.ws = None

    @staticmethod
    def _href():
        return '/fairylab/'

    @staticmethod
    def _title():
        return 'Fairylab'

    def _render_data(self, **kwargs):
        home_html = self.get_home_html(**kwargs)
        return [('index.html', '', 'home.html', home_html)]

    def _on_message_internal(self, **kwargs):
        return Response()

    @messageable
    def reboot(self, *args, **kwargs):
        _logger.log(logging.DEBUG, 'Rebooting filefairy.')
        os.execv(sys.executable, ['python3'] + sys.argv)

    @messageable
    def reload(self, *args, **kwargs):
        if len(args) != 1:
            return Response()

        self.reload_services()

        t = args[0]
        response = self.reload_internal(t, True, **kwargs)

        if response.notify:
            self.setup_all(*args, **kwargs)
            self.date = kwargs['date']

        return response

    @messageable
    def renderables(self, *args, **kwargs):
        if len(args) != 1 or not isinstance(args[0], list):
            return
        self.renderables_ = args[0]

    @messageable
    def shutdown(self, *args, **kwargs):
        _logger.log(logging.DEBUG, 'Shutting down filefairy.')
        self.keep_running = False

    def background(self):
        while self.keep_running:
            original = list(self.threads)
            self.threads = []

            for t, thread_ in original:
                self.try_(t, thread_.target, *thread_.args, **thread_.kwargs)

            time.sleep(self.sleep)

    def connect(self):
        def _recv(ws, message):
            self.recv(message)

        obj = rtm_connect()
        if obj['ok'] and 'url' in obj:
            self.ws = websocket.WebSocketApp(obj['url'], on_message=_recv)

            t = threading.Thread(target=self.ws.run_forever)
            t.daemon = True
            t.start()

    def handle_response(self, t, response, **kwargs):
        if response.notify:
            self.date = kwargs['date']
            self.runners[t].date = kwargs['date']
        for notify in response.notify:
            if notify != Notify.BASE:
                self.try_all('_notify', **dict(kwargs, notify=notify))
        for thread_ in response.thread_:
            self.threads.append((t, thread_))

    def install(self, t, module, clazz, **kwargs):
        date = kwargs['date']
        try:
            runnable = getattr(module, clazz)
            runargs = {'date': date}
            if t in self.renderables_:
                runargs['e'] = self.environment

            self.runners[t] = runnable(**runargs)
        except Exception:
            _logger.log(logging.ERROR, 'Disabled ' + t + '.', exc_info=True)
            return False

        return True

    def recv(self, message):
        date = datetime_now()
        obj = json.loads(message)

        self._on_message(obj=obj, date=date)
        self.try_all('_on_message', obj=obj, date=date)

    def reload_internal(self, t, log, **kwargs):
        response = Response()

        clazz = t.capitalize()
        package = 'tasks.{}.{}'.format(t, t)

        if package in sys.modules:
            sys.modules.pop(package, None)

        msg = '{} {}.'.format('{}', t)
        try:
            module = importlib.import_module(package)
            if self.install(t, module, clazz, **kwargs):
                response.append(notify=Notify.BASE)
                if log:
                    m = msg.format('Reloaded')
                    _logger.log(logging.INFO, m)
                    response.append(debug=Debug(msg=m))
        except Exception:
            _logger.log(logging.ERROR, msg.format('Disabled'), exc_info=True)

        return response

    def reload_services(self):
        try:
            reload_services()
        except Exception:
            _logger.log(logging.ERROR,
                        'Error reloading services.',
                        exc_info=True)

    def run(self):
        date = datetime_now()
        self.try_all('_run', date=date)

        if self.day != date.day:
            notify = Notify.FILEFAIRY_DAY
            self.try_all('_notify', notify=notify, date=date)
            self.day = date.day

        if self.date != self.original:
            self._render(date=date)
            # TODO: uncomment after finishing refactors.
            # if 'git' in self.runners.keys():
            #     notify = Notify.FILEFAIRY_DEPLOY
            #     self.try_('git', '_notify', notify=notify, date=date)
            self.original = self.date

    def setup(self, *args, **kwargs):
        self.reload_services()

        for t in listdirs(TASKS_DIR):
            self.reload_internal(t, False, **kwargs)

        self.setup_all(*args, **kwargs)

    def setup_all(self, *args, **kwargs):
        self.try_all('_setup', **kwargs)
        self.try_all('_render', **kwargs)

    def start(self, duration):
        count = 0
        while self.keep_running and (duration is None or count < duration):
            if not self.bg:
                self.bg = threading.Thread(target=self.background)
                self.bg.daemon = True
                self.bg.start()

            if not self.ws or not self.ws.sock:
                if self.ws:
                    self.ws.close()
                self.connect()

            self.run()
            time.sleep(self.sleep)
            count += 1

        if self.ws:
            self.ws.close()

    def try_(self, t, method, *args, **kwargs):
        if t not in self.runners:
            return

        instance = self.runners[t]
        if not instance.ok:
            return

        item = getattr(instance, method, None)
        if not item or not callable(item):
            return

        date = kwargs.get('date') or datetime_now()
        kwargs['date'] = date
        try:
            response = item(*args, **kwargs)
            self.handle_response(t, response, **kwargs)
        except Exception:
            _logger.log(logging.ERROR, 'Disabled ' + t + '.', exc_info=True)
            self.runners[t].date = date
            self.runners[t].ok = False

    def try_all(self, method, *args, **kwargs):
        tasks = sorted(self.runners.keys())
        for t in tasks:
            self.try_(t, method, *args, **kwargs)

    def get_home_html(self, **kwargs):
        return {'sitelinks': sitelinks()}


def main():
    date = datetime_now()
    e = env()
    dashboard = Dashboard(date=date, e=e)
    reference = Reference(date=date)

    handler = LoggingHandler(dashboard)
    _logger.addHandler(handler)
    _logger.setLevel(logging.DEBUG)

    set_reference(reference)

    filefairy = Filefairy(date=date, d=dashboard, e=e, r=reference)
    filefairy.renderables(['gameday', 'news', 'standings'])
    filefairy.setup(date=date)
    filefairy.start(2)


if __name__ == '__main__':
    main()
