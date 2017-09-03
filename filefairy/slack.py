#!/usr/bin/env python

import base64
import json
import os
import subprocess
import tokens
import urllib
import urllib2


def callApi(method, fields):
  url = "https://slack.com/api/{}".format(method)
  request = urllib2.Request(url, urllib.urlencode(fields))
  return urllib2.urlopen(request)


def postMessage(channel, text, attachments=[], thread_ts=""):
  return callApi("chat.postMessage", {
      "token": tokens.filefairy,
      "channel": channel,
      "text": text,
      "as_user": "true",
      "attachments": attachments,
      "link_names": "true",
      "thread_ts": thread_ts
  })


def update(ts, channel, text, attachments=[]):
  return callApi("chat.update", {
      "token": tokens.filefairy,
      "ts": ts,
      "channel": channel,
      "text": text,
      "as_user": "true",
      "attachments": attachments,
  })


def reactionsAdd(name, channel, timestamp):
  return callApi("reactions.add", {
      "token": tokens.filefairy,
      "name": name,
      "channel": channel,
      "timestamp": timestamp
  })


def rtmConnect():
  return callApi("rtm.connect", {"token": tokens.filefairy})


def upload(path, filename, channel, keep=False):
  """Uploads a file to the Slack team."""
  if not os.path.isfile(os.path.join(path, filename)):
    postMessage("Unable to upload {0}.".format(filename), "testing")
    return

  cwd = os.getcwd()
  os.chdir(path)

  fi = "file=@{0}".format(filename)
  ch = "channels=#{0}".format(channel)
  token = "token={0}".format(tokens.filefairy)
  url = "https://slack.com/api/files.upload"

  with open(os.devnull, "wb") as f:
    subprocess.call(["curl", "-F", fi, "-F", ch, "-F",
                     token, url], stderr=f, stdout=f)

  if not keep:
    subprocess.call(["rm", filename])

  os.chdir(cwd)

nicks = ["ARI", "ATL", "BAL", "BOS", "CWS", "CHC", "CIN", "CLE", "COL", "DET",
         "MIA", "HOU", "KC", "LAA", "LAD", "MIL", "MIN", "NYY", "NYM", "OAK",
         "PHI", "PIT", "SD", "SEA", "SF", "STL", "TB", "TEX", "TOR", "WAS"]


def getNickname(number):
  if number < 31 or number > 60:
    return "???"
  return nicks[number - 31]


emoji = [":dbacks:", ":braves:", ":orioles:", ":redsox:", ":whitesox:",
         ":cubs:", ":reds:", ":indians:", ":rockies:", ":tigers:", ":marlins:",
         ":astros:", ":royals:", ":angels:", ":dodgers:", ":brewers:",
         ":twins:", ":yankees:", ":mets:", ":athletics:", ":phillies:",
         ":pirates:", ":padres:", ":mariners:", ":giants:", ":cardinals:",
         ":rays:", ":rangers:", ":jays:", ":nationals:"]


def getEmoji(number):
  if number < 31 or number > 60:
    return ":grey_question:"
  return emoji[number - 31]


teamidsToNicks = dict(zip(range(31, 61), nicks))
teamidsToEmoji = dict(zip(range(31, 61), emoji))
nicksToEmoji = dict(zip(nicks, emoji))
