#!/usr/bin/env python

import argparse
import json
import os
import sys
import thread
import time
import websocket
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import slack

from utils import assertEquals


def testChat():
  attachments = [{"fallback": "a", "pretext": "b",
                  "fields": [{"value": "c"}, {"value": "d"}]}]
  response = slack.postMessage("testing", "foo", attachments)
  obj = json.loads(response.read())
  channel = obj["channel"]
  ts = obj["message"]["ts"]
  assertEquals(obj["ok"], True)
  assertEquals(obj["message"]["text"], "foo")
  assertEquals(obj["message"]["attachments"][0]["fields"][0]["value"], "c")
  assertEquals(obj["message"]["attachments"][0]["fields"][1]["value"], "d")

  attachments = [{"fallback": "e", "pretext": "f",
                  "fields": [{"value": "g"}, {"value": "h"}]}]
  response = slack.postMessage(channel, "bar", attachments, ts)
  obj = json.loads(response.read())
  thread_ts = obj["message"]["thread_ts"]
  reply_ts = obj["message"]["ts"]
  assertEquals(obj["ok"], True)
  assertEquals(obj["message"]["text"], "bar")
  assertEquals(obj["message"]["attachments"][0]["fields"][0]["value"], "g")
  assertEquals(obj["message"]["attachments"][0]["fields"][1]["value"], "h")
  assertEquals(ts, thread_ts)

  attachments = [{"fallback": "a", "pretext": "b",
                  "fields": [{"value": "i"}, {"value": "j"}]}]
  response = slack.update(ts, channel, "baz", attachments)
  obj = json.loads(response.read())
  assertEquals(obj["ok"], True)
  assertEquals(obj["message"]["text"], "baz")
  assertEquals(obj["message"]["replies"][0]["ts"], reply_ts)
  assertEquals(obj["message"]["attachments"][0]["fields"][0]["value"], "i")
  assertEquals(obj["message"]["attachments"][0]["fields"][1]["value"], "j")

  attachments = [{"fallback": "e", "pretext": "f",
                  "fields": [{"value": "k"}, {"value": "l"}]}]
  response = slack.update(reply_ts, channel, "bar", attachments)
  obj = json.loads(response.read())
  thread_ts = obj["message"]["thread_ts"]
  assertEquals(obj["ok"], True)
  assertEquals(obj["message"]["text"], "bar")
  assertEquals(obj["message"]["attachments"][0]["fields"][0]["value"], "k")
  assertEquals(obj["message"]["attachments"][0]["fields"][1]["value"], "l")
  assertEquals(ts, thread_ts)


def testUpload():
  path = os.path.expanduser("~") + "/orangeandblueleague/filefairy/testing/"
  response = slack.upload(path, "image.png", "testing", keep=True)


def testReactions():
  response = slack.postMessage("testing", "Snack me, @filefairy!")
  obj = json.loads(response.read())
  channel = obj["channel"]
  ts = obj["message"]["ts"]
  assertEquals(obj["ok"], True)

  response = slack.reactionsAdd("eggplant", channel, ts)
  obj = json.loads(response.read())
  assertEquals(obj["ok"], True)


def on_message(ws, message):
  obj = json.loads(message)
  if "text" in obj and "snack me" in obj["text"].lower():
    channel = obj["channel"]
    ts = obj["ts"]
    response = slack.reactionsAdd("eggplant", channel, ts)
    obj = json.loads(response.read())
    assertEquals(obj["ok"], True)


def on_open(ws):
  def run(*args):
    slack.postMessage("testing", "Snack me, @filefairy!")
    time.sleep(1)
    ws.close()

  thread.start_new_thread(run, ())


def testRtm():
  response = slack.rtmConnect()
  obj = json.loads(response.read())
  url = obj["url"]
  assertEquals(obj["ok"], True)

  ws = websocket.WebSocketApp(url, on_message=on_message)
  ws.on_open = on_open
  ws.run_forever()


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--mode', dest='mode')
  args = parser.parse_args()

  if args.mode == "chat" or args.mode == "all":
    testChat()

  if args.mode == "upload" or args.mode == "all":
    testUpload()

  if args.mode == "reactions" or args.mode == "all":
    testReactions()

  if args.mode == "rtm" or args.mode == "all":
    testRtm()

  print "Passed."
