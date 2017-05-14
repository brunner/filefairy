#!/usr/bin/env python

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import slack

from utils import assertEquals


def test():
  attachments = [{"fallback": "a", "pretext": "b", "fields": [
      {"value": "c", "short": "true"}, {"value": "d", "short": "true"}]}]
  response = slack.postMessage_("testing", "foo", attachments)
  obj = json.loads(response.read())
  channel = obj["channel"]
  ts = obj["message"]["ts"]
  assertEquals(obj["ok"], True)
  assertEquals(obj["message"]["text"], "foo")
  assertEquals(obj["message"]["attachments"][0]["fields"][0]["value"], "c")
  assertEquals(obj["message"]["attachments"][0]["fields"][1]["value"], "d")

  attachments = [{"fallback": "e", "pretext": "f", "fields": [
      {"value": "g", "short": "true"}, {"value": "h", "short": "true"}]}]
  response = slack.postMessage_(channel, "bar", attachments, ts)
  obj = json.loads(response.read())
  thread_ts = obj["message"]["thread_ts"]
  reply_ts = obj["message"]["ts"]
  assertEquals(obj["ok"], True)
  assertEquals(obj["message"]["text"], "bar")
  assertEquals(obj["message"]["attachments"][0]["fields"][0]["value"], "g")
  assertEquals(obj["message"]["attachments"][0]["fields"][1]["value"], "h")
  assertEquals(ts, thread_ts)

  attachments = [{"fallback": "a", "pretext": "b", "fields": [
      {"value": "i", "short": "true"}, {"value": "j", "short": "true"}]}]
  response = slack.update_(ts, channel, "baz", attachments)
  obj = json.loads(response.read())
  assertEquals(obj["ok"], True)
  assertEquals(obj["message"]["text"], "baz")
  assertEquals(obj["message"]["replies"][0]["ts"], reply_ts)
  assertEquals(obj["message"]["attachments"][0]["fields"][0]["value"], "i")
  assertEquals(obj["message"]["attachments"][0]["fields"][1]["value"], "j")

  attachments = [{"fallback": "e", "pretext": "f", "fields": [
      {"value": "k", "short": "true"}, {"value": "l", "short": "true"}]}]
  response = slack.update_(reply_ts, channel, "bar", attachments)
  obj = json.loads(response.read())
  thread_ts = obj["message"]["thread_ts"]
  assertEquals(obj["ok"], True)
  assertEquals(obj["message"]["text"], "bar")
  assertEquals(obj["message"]["attachments"][0]["fields"][0]["value"], "k")
  assertEquals(obj["message"]["attachments"][0]["fields"][1]["value"], "l")
  assertEquals(ts, thread_ts)

  path = os.path.expanduser("~") + "/orangeandblueleague/watchers/testing/"
  response = slack.upload_(path, "image.png", "testing")
  obj = json.loads(response.read())
  assertEquals(obj["ok"], True)

if __name__ == "__main__":
  test()

  print "Passed."
