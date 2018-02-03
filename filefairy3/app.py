#!/usr/bin/env python

import json
import threading
import time
import websocket

from utils.slack.slack_util import rtm_connect
from plugins.git.git_plugin import GitPlugin
from plugins.league_file.league_file_plugin import LeagueFilePlugin


class App(object):

  def __init__(self):
    self.lock = threading.Lock()
    self.plugins = []
    self.ws = None

  def setup(self):
    self.sleep = 2

    self.plugins.append(GitPlugin())
    self.plugins.append(LeagueFilePlugin())

  def connect(self):
    def _on_message(ws, message):
      self.lock.acquire()

      obj = json.loads(message)
      for p in self.plugins:
        p._on_message(obj)

      self.lock.release()

    obj = rtm_connect()
    if obj['ok'] and 'url' in obj:
      self.ws = websocket.WebSocketApp(obj['url'], on_message=_on_message)
      t = threading.Thread(target=self.ws.run_forever)
      t.daemon = True
      t.start()

  def run(self):
    while True:
      self.lock.acquire()

      if self.ws and not self.ws.sock:
        self.ws.close()
        self.connect()

      for p in self.plugins:
        p._run()

      self.lock.release()
      time.sleep(self.sleep)


if __name__ == '__main__':
  app = App()

  app.setup()
  app.connect()
  app.run()
