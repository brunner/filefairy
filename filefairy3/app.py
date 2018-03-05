#!/usr/bin/env python

import importlib
import json
import os
import sys
import threading
import time
import traceback
import websocket

from apis.messageable.messageable_api import MessageableApi
from utils.logger.logger_util import log
from utils.slack.slack_util import rtm_connect

_path = os.path.dirname(os.path.abspath(__file__))


class App(MessageableApi):
    def __init__(self):
        super(App, self).__init__()

        self.keep_running = True
        self.lock = threading.Lock()
        self.plugins = {}
        self.sleep = 120
        self.ws = None

    def _on_message_internal(self, **kwargs):
        pass

    def _setup(self):
        d = os.path.join(_path, 'plugins')
        ps = filter(lambda x: os.path.isdir(os.path.join(d, x)), os.listdir(d))
        for p in ps:
            self.install(a1=p)

    def _try(self, p, method, **kwargs):
        if p not in self.plugins:
            return

        plugin = self.plugins[p]
        item = getattr(plugin, method, None)
        if not item or not callable(item):
            return

        try:
            item(**kwargs)
        except Exception:
            exc = traceback.format_exc()
            log(plugin._name(), s='Exception.', r=exc, v=True)
            del self.plugins[p]

    def _connect(self):
        def _on_message(ws, message):
            self.lock.acquire()
            obj = json.loads(message)
            self._on_message(obj=obj)
            ps = self.plugins.keys()
            for p in ps:
                self._try(p, '_on_message', obj=obj)
            self.lock.release()

        obj = rtm_connect()
        if obj['ok'] and 'url' in obj:
            self.ws = websocket.WebSocketApp(
                obj['url'], on_message=_on_message)
            t = threading.Thread(target=self.ws.run_forever)
            t.daemon = True
            t.start()

    def _start(self):
        while self.keep_running:
            if not self.ws or not self.ws.sock:
                if self.ws:
                    self.ws.close()
                self._connect()

            self.lock.acquire()
            ps = self.plugins.keys()
            for p in ps:
                self._try(p, '_run')
            self.lock.release()
            time.sleep(self.sleep)

        self.ws.close()

    def install(self, **kwargs):
        p = kwargs.get('a1', '')
        path = 'plugins.{0}.{0}_plugin'.format(p)
        camel = ''.join([w.capitalize() for w in p.split('_')])
        clazz = '{}Plugin'.format(camel)

        if p in self.plugins and path in sys.modules:
            del self.plugins[p]
            del sys.modules[path]

        try:
            plugin = getattr(importlib.import_module(path), clazz)()
            self.plugins[p] = plugin
            log(clazz, **dict(kwargs, s='Installed.', v=True))
        except Exception:
            exc = traceback.format_exc()
            log(clazz, s='Exception.', r=exc, v=True)

        self._try(p, '_setup')

    def reboot(self, **kwargs):
        os.execv(sys.executable, ['python'] + sys.argv)

    def shutdown(self, **kwargs):
        self.keep_running = False
        log(self._name(), **dict(kwargs, s='Shutting down.'))


if __name__ == '__main__':
    app = App()
    app._setup()
    app._start()
