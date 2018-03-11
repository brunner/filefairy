#!/usr/bin/env python

import copy
import datetime
import importlib
import jinja2
import json
import os
import re
import sys
import threading
import time
import traceback
import websocket

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/programs/fairylab', '', _path)
sys.path.append(_root)

from apis.messageable.messageable_api import MessageableApi  # noqa
from apis.renderable.renderable_api import RenderableApi  # noqa
from utils.ago.ago_util import delta  # noqa
from utils.logger.logger_util import log  # noqa
from utils.slack.slack_util import rtm_connect  # noqa


class FairylabProgram(MessageableApi, RenderableApi):
    def __init__(self, **kwargs):
        ldr = jinja2.FileSystemLoader(os.path.join(_root, 'templates'))
        env = jinja2.Environment(
            loader=ldr, trim_blocks=True, lstrip_blocks=True)
        super(FairylabProgram, self).__init__(**dict(kwargs, e=env))
        self.data = {'plugins': {}}
        self.keep_running = True
        self.lock = threading.Lock()
        self.sleep = 120
        self.ws = None

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _html():
        return 'index.html'

    @staticmethod
    def _tmpl():
        return 'home.html'

    def _on_message_internal(self, **kwargs):
        pass

    def _render_internal(self, **kwargs):
        date = datetime.datetime.now()
        ret = copy.deepcopy(self.data)
        ret['title'] = 'home'
        ret['breadcrumbs'] = [{'href': '', 'name': 'Home'}]

        ps = ret['plugins'].keys()
        for p in ps:
            del ret['plugins'][p]['instance']
            pdate = ret['plugins'][p]['date']
            t = delta(pdate, date)
            ret['plugins'][p]['date'] = t

        return ret

    def _setup(self):
        d = os.path.join(_root, 'plugins')
        ps = filter(lambda x: os.path.isdir(os.path.join(d, x)), os.listdir(d))
        for p in ps:
            self.install(a1=p)

    def _try(self, p, method, **kwargs):
        data = self.data
        if p not in data['plugins']:
            return

        plugin = data['plugins'][p]
        if 'instance' not in plugin or not plugin.get('ok', False):
            return

        instance = data['plugins'][p]['instance']
        item = getattr(instance, method, None)
        if not item or not callable(item):
            return

        try:
            if item(**kwargs):
                data['plugins'][p]['date'] = datetime.datetime.now()
        except Exception:
            exc = traceback.format_exc()
            log(instance._name(), s='Exception.', c=exc, v=True)
            data['plugins'][p]['ok'] = False
            data['plugins'][p]['date'] = datetime.datetime.now()

    def _recv(self, message):
        self.lock.acquire()
        data = self.data
        original = copy.deepcopy(data)

        obj = json.loads(message)
        self._on_message(obj=obj)

        ps = data['plugins'].keys()
        for p in ps:
            self._try(p, '_on_message', obj=obj)

        if data != original:
            self.write()

        self.lock.release()

    def _connect(self):
        def _recv(ws, message):
            self._recv(message)

        obj = rtm_connect()
        if obj['ok'] and 'url' in obj:
            self.ws = websocket.WebSocketApp(obj['url'], on_message=_recv)
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
                self._try(p, '_run')

            if data != original:
                self.write()

            self._render()
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
            del data['plugins'][p]
            del sys.modules[path]

        date = datetime.datetime.now()
        try:
            plugin = getattr(importlib.import_module(path), clazz)
            info = plugin._info()
            instance = plugin(**dict(kwargs, e=self.environment))
            ok = True
            log(clazz, **dict(kwargs, s='Installed.', v=True))
        except Exception:
            info = ''
            instance = None
            ok = False
            exc = traceback.format_exc()
            log(clazz, **dict(kwargs, s='Exception.', c=exc, v=True))

        data['plugins'][p] = {
            'date': date,
            'info': info,
            'instance': instance,
            'ok': ok,
        }

        self._try(p, '_setup')

        if data != original:
            self.write()

    def reboot(self, **kwargs):
        log(self._name(), **dict(kwargs, s='Rebooting.', v=True))
        os.execv(sys.executable, ['python'] + sys.argv)

    def shutdown(self, **kwargs):
        log(self._name(), **dict(kwargs, s='Shutting down.', v=True))
        self.keep_running = False


if __name__ == '__main__':
    fairylab = FairylabProgram()
    fairylab._setup()
    fairylab._start()
