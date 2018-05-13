#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import datetime
import importlib
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

from api.messageable.messageable_api import MessageableApi  # noqa
from api.plugin.plugin_api import PluginApi  # noqa
from api.renderable.renderable_api import RenderableApi  # noqa
from utils.ago.ago_util import delta  # noqa
from utils.component.component_util import card  # noqa
from utils.datetime.datetime_util import decode_datetime  # noqa
from utils.datetime.datetime_util import encode_datetime  # noqa
from utils.jinja2.jinja2_util import env  # noqa
from utils.logger.logger_util import log  # noqa
from utils.slack.slack_util import rtm_connect  # noqa
from value.notify.notify_value import NotifyValue  # noqa


class FairylabProgram(MessageableApi, RenderableApi):
    def __init__(self, **kwargs):
        super(FairylabProgram, self).__init__(**dict(kwargs))
        self.day = None
        self.pins = {}
        self.keep_running = True
        self.lock = threading.Lock()
        self.sleep = 120
        self.ws = None

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _href():
        return '/fairylab/'

    @staticmethod
    def _title():
        return 'home'

    def _setup(self):
        data = self.data
        original = copy.deepcopy(data)

        date = datetime.datetime.now()
        kwargs = {'date': date, 'v': True}
        self.day = date.day

        d = os.path.join(_root, 'plugins')
        ps = filter(lambda x: os.path.isdir(os.path.join(d, x)), os.listdir(d))
        for p in sorted(ps):
            self._reload_internal(**dict(kwargs, a1='plugin', a2=p))

        self._try_all('_setup', **kwargs)
        log(self._name(), **dict(kwargs, s='Completed setup.'))

        if data != original:
            self.write()

    def _on_message_internal(self, **kwargs):
        pass

    def _render_internal(self, **kwargs):
        _home = self._home(**kwargs)
        return [('html/fairylab/index.html', '', 'home.html', _home)]

    @staticmethod
    def _clazz(name):
        camel = ''.join([w.capitalize() for w in name.split('_')])
        return '{}Plugin'.format(camel)

    @staticmethod
    def _package(path, name):
        return '{0}s.{1}.{1}_{0}'.format(path, name)

    def _plugin(self, p):
        return self.data['plugins'].get(p, {})

    def _try_all(self, method, **kwargs):
        ps = sorted(self.data['plugins'].keys())
        for p in ps:
            self._try(p, method, **kwargs)

    def _try(self, p, method, **kwargs):
        data = self.data
        if p not in data['plugins']:
            return

        plugin = self._plugin(p)
        instance = self.pins.get(p, None)
        if not plugin.get('ok') or not instance:
            return

        item = getattr(instance, method, None)
        if not item or not callable(item):
            return

        date = kwargs.get('date') or datetime.datetime.now()
        edate = encode_datetime(date)

        try:
            response = item(**dict(kwargs, date=date))
            if response.notify:
                data['plugins'][p]['date'] = edate
            for n in response.notify:
                if n != NotifyValue.BASE:
                    self._try_all('_notify', **dict(kwargs, notify=n))
            for s in response.shadow:
                shadow = response.shadow[s]
                self._try(s, '_shadow', **dict(kwargs, shadow=shadow))
        except Exception:
            exc = traceback.format_exc()
            log(instance._name(), s='Exception.', c=exc, v=True)
            data['plugins'][p]['ok'] = False
            data['plugins'][p]['date'] = edate

    def _recv(self, message):
        self.lock.acquire()
        data = self.data
        original = copy.deepcopy(data)

        date = datetime.datetime.now()
        obj = json.loads(message)
        self._on_message(obj=obj, date=date)
        self._try_all('_on_message', obj=obj, date=date)

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

            date = datetime.datetime.now()
            self._try_all('_run', date=date)

            if self.day != date.day:
                self.day = date.day
                self._try_all('_notify', notify=NotifyValue.FAIRYLAB_DAY)

            if data != original:
                self.write()

            self._render(date=date)
            self.lock.release()

            time.sleep(self.sleep)

        if self.ws:
            self.ws.close()

    def _home(self, **kwargs):
        data = self.data
        ret = {
            'breadcrumbs': [{
                'href': '',
                'name': 'Home'
            }],
            'browsable': [],
            'internal': []
        }

        date = kwargs['date']
        ps = sorted(data['plugins'].keys())
        for p in ps:
            plugin = self._plugin(p)
            instance = self.pins.get(p, None)
            info = ''
            if isinstance(instance, PluginApi):
                info = instance._info()

            href = ''
            renderable = isinstance(instance, RenderableApi)
            if renderable:
                href = instance._href()

            pdate = plugin.get('date', datetime.datetime.now())
            ts = delta(decode_datetime(pdate), date)

            success = 'just now' if 's' in ts else ''
            danger = 'error' if not plugin.get('ok') else ''
            c = card(
                href=href,
                title=p,
                info=info,
                ts=ts,
                success=success,
                danger=danger)

            if renderable:
                ret['browsable'].append(c)
            else:
                ret['internal'].append(c)

        return ret

    def reload(self, **kwargs):
        data = self.data
        original = copy.deepcopy(data)

        value = self._reload_internal(**kwargs)
        if value:
            self._try_all('_setup', **kwargs)
            log(self._name(), **dict(kwargs, s='Completed setup.'))

        if data != original:
            self.write()

    def _reload_internal(self, **kwargs):
        data = self.data
        original = copy.deepcopy(data)

        path = kwargs.get('a1', '')
        name = kwargs.get('a2', '')
        package = self._package(path, name)

        if package in sys.modules:
            del sys.modules[package]

        try:
            module = importlib.import_module(package)

            if path == 'plugin':
                clazz = self._clazz(name)
                return self._install(name, module, clazz, **kwargs)
            else:
                s = 'Reloaded {}.'.format(name)
                log(self._name(), **dict(kwargs, s=s))
        except Exception:
            exc = traceback.format_exc()
            log(clazz, **dict(kwargs, s='Exception.', c=exc))

        return False

    def _install(self, name, module, clazz, **kwargs):
        try:
            date = kwargs['date']
            ok = True
            plugin = getattr(module, clazz)
            instance = plugin(**dict(kwargs, e=self.environment))
            enabled = instance.enabled
            exc = None
        except Exception:
            date = None
            ok = False
            instance = None
            enabled = False
            exc = traceback.format_exc()

        s = 'Exception.' if exc else 'Installed.' if enabled else 'Disabled.'
        log(clazz, **dict(kwargs, s=s, c=exc))

        if enabled:
            self.data['plugins'][name] = {
                'date': encode_datetime(date),
                'ok': True,
            }
            self.pins[name] = instance

        return enabled

    def reboot(self, **kwargs):
        log(self._name(), **dict(kwargs, s='Rebooting.'))
        os.execv(sys.executable, ['python'] + sys.argv)

    def shutdown(self, **kwargs):
        log(self._name(), **dict(kwargs, s='Shutting down.'))
        self.keep_running = False


if __name__ == '__main__':
    fairylab = FairylabProgram(e=env())
    fairylab._setup()
    fairylab._start()
