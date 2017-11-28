#!/usr/bin/env python

import json
import os
import sys
import thread
import time
import websocket
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from slack_api import chat_post_message, files_upload, rtm_connect
from utils import assert_equals


def test_chat_post_message():
  attachments = [{'fields': [{'value': 'a1'}]}]
  obj = chat_post_message('testing', 'm1', attachments)
  channel = obj['channel']
  ts = obj['message']['ts']
  assert_equals(obj['ok'], True)
  assert_equals(obj['message']['text'], 'm1')
  assert_equals(obj['message']['attachments'][0]['fields'][0]['value'], 'a1')

  attachments = [{'fields': [{'value': 'a2'}]}]
  obj = chat_post_message(channel, 'm2', attachments, ts)
  thread_ts = obj['message']['thread_ts']
  reply_ts = obj['message']['ts']
  assert_equals(obj['ok'], True)
  assert_equals(obj['message']['text'], 'm2')
  assert_equals(obj['message']['attachments'][0]['fields'][0]['value'], 'a2')
  assert_equals(ts, thread_ts)


def test_files_upload():
  obj = files_upload('hello world', 'hello.txt', 'testing')
  assert_equals(obj['ok'], True)


def test_rtm_connect():
  def on_message(ws, message):
    obj = json.loads(message)
    if 'text' in obj and 'hello' in obj['text'].lower():
      channel = obj['channel']
      ts = obj['ts']
      obj = chat_post_message(channel, 'world', [], ts)
      assert_equals(obj['ok'], True)

  def on_close(ws):
    pass

  def on_open(ws):
    def run(*args):
      chat_post_message('testing', 'hello')
      assert_equals(obj['ok'], True)
      time.sleep(1)
      ws.close()

    thread.start_new_thread(run, ())

  obj = rtm_connect()
  url = obj['url']
  assert_equals(obj['ok'], True)

  ws = websocket.WebSocketApp(url, on_message=on_message)
  ws.on_open = on_open
  ws.run_forever()


if __name__ == '__main__':
  test_chat_post_message()
  test_files_upload()
  test_rtm_connect()
