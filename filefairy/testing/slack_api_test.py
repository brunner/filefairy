#!/usr/bin/env python

import argparse
import json
import os
import sys
import thread
import time
import websocket
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logger import TestLogger
from slack_api import SlackApi, TestSlackApi
from utils import assertEquals


def slackApi_chatPostMessage():
  logger = TestLogger()
  slackApi = SlackApi(logger)

  attachments = [{"fields": [{"value": "a1"}]}]
  obj = slackApi.chatPostMessage("testing", "m1", attachments)
  channel = obj["channel"]
  ts = obj["message"]["ts"]
  assertEquals(obj["ok"], True)
  assertEquals(obj["message"]["text"], "m1")
  assertEquals(obj["message"]["attachments"][0]["fields"][0]["value"], "a1")

  attachments = [{"fields": [{"value": "a2"}]}]
  obj = slackApi.chatPostMessage(channel, "m2", attachments, ts)
  thread_ts = obj["message"]["thread_ts"]
  reply_ts = obj["message"]["ts"]
  assertEquals(obj["ok"], True)
  assertEquals(obj["message"]["text"], "m2")
  assertEquals(obj["message"]["attachments"][0]["fields"][0]["value"], "a2")
  assertEquals(ts, thread_ts)

  attachments = [{"fields": [{"value": "a3"}]}]
  obj = slackApi.chatUpdate(ts, channel, "m3", attachments)
  assertEquals(obj["ok"], True)
  assertEquals(obj["message"]["text"], "m3")
  assertEquals(obj["message"]["replies"][0]["ts"], reply_ts)
  assertEquals(obj["message"]["attachments"][0]["fields"][0]["value"], "a3")

  attachments = [{"fields": [{"value": "a4"}]}]
  obj = slackApi.chatUpdate(reply_ts, channel, "m4", attachments)
  thread_ts = obj["message"]["thread_ts"]
  assertEquals(obj["ok"], True)
  assertEquals(obj["message"]["text"], "m4")
  assertEquals(obj["message"]["attachments"][0]["fields"][0]["value"], "a4")
  assertEquals(ts, thread_ts)

  assertEquals(slackApi.logger.collect(), [])


def slackApi_filesUpload():
  logger = TestLogger()
  slackApi = SlackApi(logger)

  path = os.path.expanduser("~") + "/orangeandblueleague/filefairy/testing/"
  obj = slackApi.filesUpload(path, "image.png", "testing", keep=True)
  assertEquals(obj["ok"], True)

  assertEquals(slackApi.logger.collect(), [])


def slackApi_reactionsAdd():
  logger = TestLogger()
  slackApi = SlackApi(logger)

  obj = slackApi.chatPostMessage("testing", "Snack me, @filefairy!")
  channel = obj["channel"]
  ts = obj["message"]["ts"]
  assertEquals(obj["ok"], True)

  obj = slackApi.reactionsAdd("eggplant", channel, ts)
  assertEquals(obj["ok"], True)

  assertEquals(slackApi.logger.collect(), [])


def slackApi_rtmConnect():
  logger = TestLogger()
  slackApi = SlackApi(logger)

  def on_message(ws, message):
    obj = json.loads(message)
    if "text" in obj and "snack me" in obj["text"].lower():
      channel = obj["channel"]
      ts = obj["ts"]
      obj = slackApi.reactionsAdd("eggplant", channel, ts)
      assertEquals(obj["ok"], True)

  def on_close(ws):
    assertEquals(slackApi.logger.collect(), [])

  def on_open(ws):
    def run(*args):
      slackApi.chatPostMessage("testing", "Snack me, @filefairy!")
      assertEquals(obj["ok"], True)
      time.sleep(1)
      ws.close()

    thread.start_new_thread(run, ())

  obj = slackApi.rtmConnect()
  url = obj["url"]
  assertEquals(obj["ok"], True)

  ws = websocket.WebSocketApp(url, on_message=on_message)
  ws.on_open = on_open
  ws.run_forever()


def testSlackApi_chatPostMessage():
  logger = TestLogger()
  slackApi = TestSlackApi(logger)

  attachments = [{"fields": [{"value": "a1"}]}]
  obj = slackApi.chatPostMessage("testing", "m1", attachments)
  assertEquals(obj, {"ok": True})
  assertEquals(slackApi.logger.collect(), ["Test mocked chat.postMessage."])

  channel = "testing"
  ts = u"1234"
  reply_ts = u"5678"

  attachments = [{"fields": [{"value": "a2"}]}]
  obj = slackApi.chatPostMessage(channel, "m2", attachments, ts)
  assertEquals(obj, {"ok": True})
  assertEquals(slackApi.logger.collect(), ["Test mocked chat.postMessage."])

  attachments = [{"fields": [{"value": "a3"}]}]
  obj = slackApi.chatUpdate(ts, channel, "m3", attachments)
  assertEquals(obj, {"ok": True})
  assertEquals(slackApi.logger.collect(), ["Test mocked chat.update."])

  attachments = [{"fields": [{"value": "a4"}]}]
  obj = slackApi.chatUpdate(reply_ts, channel, "m4", attachments)
  assertEquals(obj, {"ok": True})
  assertEquals(slackApi.logger.collect(), ["Test mocked chat.update."])


def testSlackApi_filesUpload():
  logger = TestLogger()
  slackApi = TestSlackApi(logger)

  path = os.path.expanduser("~") + "/orangeandblueleague/filefairy/testing/"
  obj = slackApi.filesUpload(path, "image.png", "testing", keep=True)
  assertEquals(obj["ok"], True)
  assertEquals(slackApi.logger.collect(), ["Test mocked files.upload."])


def testSlackApi_reactionsAdd():
  logger = TestLogger()
  slackApi = TestSlackApi(logger)

  obj = slackApi.chatPostMessage("testing", "Snack me, @filefairy!")
  
  channel = "testing"
  ts = u"1234"
  
  assertEquals(obj["ok"], True)
  assertEquals(slackApi.logger.collect(), ["Test mocked chat.postMessage."])

  obj = slackApi.reactionsAdd("eggplant", channel, ts)
  assertEquals(obj["ok"], True)
  assertEquals(slackApi.logger.collect(), ["Test mocked reactions.add."])


def testSlackApi_rtmConnect():
  logger = TestLogger()
  slackApi = TestSlackApi(logger)

  def on_message(ws, message):
    obj = json.loads(message)
    if "text" in obj and "snack me" in obj["text"].lower():
      channel = "testing"
      ts = u"1234"

      obj = slackApi.reactionsAdd("eggplant", channel, ts)
      assertEquals(obj["ok"], True)
      assertEquals(slackApi.logger.collect(), ["Test mocked reactions.add."])

  def on_close(ws):
    assertEquals(slackApi.logger.collect(), [])

  def on_open(ws):
    def run(*args):
      obj = slackApi.chatPostMessage("testing", "Snack me, @filefairy!")
      assertEquals(obj["ok"], True)
      assertEquals(slackApi.logger.collect(), ["Test mocked chat.postMessage."])
      time.sleep(1)
      ws.close()

    thread.start_new_thread(run, ())

  obj = slackApi.rtmConnect()

  url = "wss://..."

  assertEquals(obj["ok"], True)
  assertEquals(slackApi.logger.collect(), ["Test mocked rtm.connect."])

  ws = websocket.WebSocketApp(url, on_message=on_message)
  ws.on_open = on_open
  ws.run_forever()


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--mode', dest='mode')
  args = parser.parse_args()

  if args.mode == "post" or args.mode == "all":
    slackApi_chatPostMessage()

  if args.mode == "upload" or args.mode == "all":
    slackApi_filesUpload()

  if args.mode == "reactions" or args.mode == "all":
    slackApi_reactionsAdd()

  if args.mode == "rtm" or args.mode == "all":
    slackApi_rtmConnect()

  if args.mode == "test" or args.mode == "all":
    testSlackApi_chatPostMessage()
    testSlackApi_filesUpload()
    testSlackApi_reactionsAdd()
    testSlackApi_rtmConnect()

  print "Passed."
