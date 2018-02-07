#!/usr/bin/env python

import importlib
import json
import os
import sys
import threading
import time
import websocket

from apis.messageable.messageable_api import MessageableApi
from utils.logger.logger_util import log
from utils.slack.slack_util import rtm_connect


class App(MessageableApi):
    def __init__(self):
        super(App, self).__init__()

        self.keep_running = True
        self.lock = threading.Lock()
        self.sleep = 120
        self.ws = None

        self.plugins = {}

    def _on_message_internal(self, obj):
        pass

    def _setup(self):
        for p in ['exports', 'git', 'league_file']:
            self.load(a=p)

    def _connect(self):
        def _on_message(ws, message):
            self.lock.acquire()

            obj = json.loads(message)
            self._on_message(obj)
            for p, plugin in self.plugins.iteritems():
                plugin._on_message(obj)

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
            self.lock.acquire()

            if not self.ws or not self.ws.sock:
                if self.ws:
                    self.ws.close()
                self._connect()

            for p, plugin in self.plugins.iteritems():
                plugin._run()

            self.lock.release()
            time.sleep(self.sleep)

        self.ws.close()

    def load(self, **kwargs):
        p = kwargs.get('a', '')
        path = 'plugins.{0}.{0}_plugin'.format(p)
        camel = ''.join([w.capitalize() for w in p.split('_')])
        clazz = '{}Plugin'.format(camel)

        if p in self.plugins and path in sys.modules:
            del self.plugins[p]
            del sys.modules[path]
            log(self._name(), **dict(kwargs, s='Removed ' + p + '.'))

        plugin = getattr(importlib.import_module(path), clazz)()
        self.plugins[p] = plugin
        log(self._name(), **dict(kwargs, s='Loaded ' + p + '.'))

    def reboot(self, **kwargs):
        os.execv(sys.executable, ['python'] + sys.argv)

    def shutdown(self, **kwargs):
        self.keep_running = False
        log(self._name(), **dict(kwargs, s='Shutting down.'))


if __name__ == '__main__':
    app = App()

    app._setup()
    app._start()
