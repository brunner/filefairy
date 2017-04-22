#!/usr/bin/env python

import os
import subprocess
import tokens
import urllib
import urllib2


def postMessage(text, channel):
  """Posts a text message to the Slack team."""
  url = "https://slack.com/api/chat.postMessage"
  fields = {"text": text, "token": tokens.filefairy, "channel": channel,
            "link_names": "brunnerj,everyone", "as_user": "true"}
  full = "{0}?{1}".format(url, urllib.urlencode(fields))
  urllib2.urlopen(full)


def upload(path, filename, channel):
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
  subprocess.call(["rm", filename])

  os.chdir(cwd)

nicks = ["ARI", "ATL", "BAL", "BOS", "CWS", "CHC", "CIN", "CLE", "COL", "DET",
         "MIA", "HOU", "KC", "LAA", "LAD", "MIL", "MIN", "NYY", "NYM", "OAK",
         "PHI", "PIT", "SD", "SEA", "SF", "STL", "TB", "TEX", "TOR", "WAS"]


emoji = [":dbacks:", ":braves:", ":orioles:", ":redsox:", ":whitesox:",
         ":cubs:", ":reds:", ":indians:", ":rockies:", ":tigers:", ":marlins:",
         ":astros:", ":royals:", ":angels:", ":dodgers:", ":brewers:",
         ":twins:", ":yankees:", ":mets:", ":athletics:", ":phillies:",
         ":pirates:", ":padres:", ":mariners:", ":giants:", ":cardinals:",
         ":rays:", ":rangers:", ":jays:", ":nationals:"]

teamidsToEmoji = dict(zip(range(31,61), emoji))
nicksToEmoji = dict(zip(nicks, emoji))