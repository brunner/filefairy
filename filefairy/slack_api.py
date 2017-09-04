#!/usr/bin/env python

import base64
import json
import os
import subprocess
import tokens
import urllib
import urllib2


class SlackApi(object):

  def __init__(self, logger):
    self.logger = logger

  def call_(self, method, params):
    url = "https://slack.com/api/{}".format(method)
    obj = {"ok": False}

    try:
      request = urllib2.Request(url, urllib.urlencode(params))
      response = urllib2.urlopen(request)
      obj = json.loads(response.read())
    except urllib2.URLError as e:
      if hasattr(e, "reason"):
        self.logger.log("Failed to reach server. {0}.".format(e.reason))
      elif hasattr(e, "code"):
        self.logger.log("Server failed to handle request. {0}.".format(e.code))
    except:
      self.logger.log("Unspecified exception.")

    return obj

  def chatPostMessage(self, channel, text, attachments=[], thread_ts=""):
    return self.call_("chat.postMessage", {
        "token": tokens.filefairy,
        "channel": channel,
        "text": text,
        "as_user": "true",
        "attachments": attachments,
        "link_names": "true",
        "thread_ts": thread_ts
    })

  def chatUpdate(self, ts, channel, text, attachments=[]):
    return self.call_("chat.update", {
        "token": tokens.filefairy,
        "ts": ts,
        "channel": channel,
        "text": text,
        "as_user": "true",
        "attachments": attachments,
    })

  def reactionsAdd(self, name, channel, timestamp):
    return self.call_("reactions.add", {
        "token": tokens.filefairy,
        "name": name,
        "channel": channel,
        "timestamp": timestamp
    })

  def rtmConnect(self):
    return self.call_("rtm.connect", {"token": tokens.filefairy})

  def filesUpload(self, path, filename, channel, keep=False):
    if not os.path.isfile(os.path.join(path, filename)):
      return chatPostMessage("testing", "Unable to upload {0}.".format(filename))

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
    return {"ok": True}


class TestSlackApi(SlackApi):

  def call_(self, method, params):
    self.logger.log("Test mocked {}.".format(method))
    return {"ok": True}

  def filesUpload(self, path, filename, channel, keep=False):
    params = {"filename": filename, "channel": channel}
    obj = json.dumps(params, sort_keys=True)
    self.logger.log("Test mocked files.upload.")
    return {"ok": True}


# TODO: Move the below utilities into a helper class.
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
