#!/usr/bin/env python

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import slack

from utils import assertEquals


def test():
  response = slack.postMessage_("testing", "foo")
  obj = json.loads(response.read())
  channel = obj["channel"]
  ts = obj["message"]["ts"]
  assertEquals(obj["ok"], True)
  assertEquals(obj["message"]["text"], "foo")

  response = slack.postMessage_(channel, "bar", ts)
  obj = json.loads(response.read())
  thread_ts = obj["message"]["thread_ts"]
  reply_ts = obj["message"]["ts"]
  assertEquals(obj["ok"], True)
  assertEquals(obj["message"]["text"], "bar")
  assertEquals(ts, thread_ts)

  response = slack.update_(ts, channel, "baz")
  obj = json.loads(response.read())
  assertEquals(obj["ok"], True)
  assertEquals(obj["message"]["text"], "baz")
  assertEquals(obj["message"]["replies"][0]["ts"], reply_ts)

  path = os.path.expanduser("~") + "/orangeandblueleague/watchers/testing/"
  response = slack.upload_(path, "image.png", "testing")
  obj = json.loads(response.read())
  assertEquals(obj["ok"], True)

if __name__ == "__main__":
  test()

  print "Passed."
