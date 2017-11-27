#!/usr/bin/env python

import argparse
import json
import os
import sys
import thread
import time
import websocket
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from slack_api import chatPostMessage, filesUpload, rtmConnect
from utils import assertEquals, assertContains


def test_chatPostMessage():
  attachments = [{'fields': [{'value': 'a1'}]}]
  obj = chatPostMessage('testing', 'm1', attachments)
  channel = obj['channel']
  ts = obj['message']['ts']
  assertEquals(obj['ok'], True)
  assertEquals(obj['message']['text'], 'm1')
  assertEquals(obj['message']['attachments'][0]['fields'][0]['value'], 'a1')

  attachments = [{'fields': [{'value': 'a2'}]}]
  obj = chatPostMessage(channel, 'm2', attachments, ts)
  thread_ts = obj['message']['thread_ts']
  reply_ts = obj['message']['ts']
  assertEquals(obj['ok'], True)
  assertEquals(obj['message']['text'], 'm2')
  assertEquals(obj['message']['attachments'][0]['fields'][0]['value'], 'a2')
  assertEquals(ts, thread_ts)


def test_filesUpload():
  obj = filesUpload('hello world', 'hello.txt', 'testing')
  assertEquals(obj['ok'], True)


def test_rtmConnect():
  def on_message(ws, message):
    obj = json.loads(message)
    if 'text' in obj and 'hello' in obj['text'].lower():
      channel = obj['channel']
      ts = obj['ts']
      obj = chatPostMessage(channel, 'world', [], ts)
      assertEquals(obj['ok'], True)

  def on_close(ws):
    pass

  def on_open(ws):
    def run(*args):
      chatPostMessage('testing', 'hello')
      assertEquals(obj['ok'], True)
      time.sleep(1)
      ws.close()

    thread.start_new_thread(run, ())

  obj = rtmConnect()
  url = obj['url']
  assertEquals(obj['ok'], True)

  ws = websocket.WebSocketApp(url, on_message=on_message)
  ws.on_open = on_open
  ws.run_forever()


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--mode', dest='mode')
  args = parser.parse_args()

  if args.mode == 'post' or args.mode == 'all':
    test_chatPostMessage()

  if args.mode == 'upload' or args.mode == 'all':
    test_filesUpload()

  if args.mode == 'rtm' or args.mode == 'all':
    test_rtmConnect()

  print 'Passed.'
