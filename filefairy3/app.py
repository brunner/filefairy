#!/usr/bin/env python

import copy
import importlib
import json
import os
import sys
import threading
import time
import traceback
import websocket

from apis.messageable.messageable_api import MessageableApi
from apis.serializable.serializable_api import SerializableApi
from utils.logger.logger_util import log
from utils.slack.slack_util import rtm_connect

_path = os.path.dirname(os.path.abspath(__file__))


class App(MessageableApi, SerializableApi):
    def __init__(self):
        super(App, self).__init__()

        self.data = {'plugins': {}}
        self.keep_running = True
        self.lock = threading.Lock()
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
        data = self.data
        if p not in data['plugins'] or 'instance' not in data['plugins'][p]:
            return

        plugin = data['plugins'][p]['instance']
        item = getattr(plugin, method, None)
        if not item or not callable(item):
            return

        try:
            item(**kwargs)
        except Exception:
            exc = traceback.format_exc()
            log(plugin._name(), s='Exception.', r=exc, v=True)
            data['plugins'][p]['ok'] = False

    def _connect(self):
        def _on_message(ws, message):
            self.lock.acquire()
            data = self.data
            original = copy.deepcopy(data)
            obj = json.loads(message)
            self._on_message(obj=obj)
            ps = data['plugins'].keys()
            for p in ps:
                if data['plugins'][p].get('ok', False):
                    self._try(p, '_on_message', obj=obj)
            if data != original:
                self.write()
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
            data = self.data
            original = copy.deepcopy(data)
            ps = data['plugins'].keys()
            for p in ps:
                if data['plugins'][p].get('ok', False):
                    self._try(p, '_run')
            if data != original:
                self.write()
            self.lock.release()
            time.sleep(self.sleep)

        if self.ws:
            self.ws.close()

    def install(self, **kwargs):
        data = self.data
        original = copy.deepcopy(data)

        p = kwargs.get('a1', '')
        path = 'plugins.{0}.{0}_plugin'.format(p)
        camel = ''.join([w.capitalize() for w in p.split('_')])
        clazz = '{}Plugin'.format(camel)

        if p in data['plugins'] and path in sys.modules:
            data['plugins']['ok'] = False
            del sys.modules[path]

        try:
            plugin = getattr(importlib.import_module(path), clazz)()
            data['plugins'][p] = {'ok': True, 'instance': plugin}
            log(clazz, **dict(kwargs, s='Installed.', v=True))
        except Exception:
            data['plugins'][p] = {'ok': False, 'instance': None}
            exc = traceback.format_exc()
            log(clazz, **dict(kwargs, s='Exception.', r=exc, v=True))

        self._try(p, '_setup')

        if data != original:
            self.write()

    def reboot(self, **kwargs):
        log(self._name(), **dict(kwargs, s='Rebooting.', v=True))
        os.execv(sys.executable, ['python'] + sys.argv)

    def shutdown(self, **kwargs):
        log(self._name(), **dict(kwargs, s='Shutting down.', v=True))
        self.keep_running = False

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')


if __name__ == '__main__':
    app = App()
    app._setup()
    app._start()
