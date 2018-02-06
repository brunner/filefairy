#!/usr/bin/env python

import json
import os
import sys
import threading
import time
import websocket

from apis.messageable.messageable_api import MessageableApi
from plugins.exports.exports_plugin import ExportsPlugin
from plugins.git.git_plugin import GitPlugin
from plugins.league_file.league_file_plugin import LeagueFilePlugin
from utils.slack.slack_util import rtm_connect


class App(MessageableApi):
    def __init__(self):
        super(App, self).__init__()

        self.keep_running = True
        self.lock = threading.Lock()
        self.sleep = 2
        self.ws = None

        self.plugins = []

    def _on_message_internal(self, obj):
        pass

    def _setup(self):
        self.plugins.append(ExportsPlugin())
        self.plugins.append(GitPlugin())
        self.plugins.append(LeagueFilePlugin())

    def _connect(self):
        def _on_message(ws, message):
            self.lock.acquire()

            obj = json.loads(message)

            self._on_message(obj)
            for p in self.plugins:
                p._on_message(obj)

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

            if self.ws and not self.ws.sock:
                self.ws.close()
                self._connect()

            for p in self.plugins:
                p._run()

            self.lock.release()
            time.sleep(self.sleep)

        self.ws.close()

    def reboot(self, *args):
        os.execv(sys.executable, ['python'] + sys.argv)

    def shutdown(self, *args):
        self.keep_running = False


if __name__ == '__main__':
    app = App()

    app._setup()
    app._connect()
    app._start()
