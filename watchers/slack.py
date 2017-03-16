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


icons = {
    "ATL": ":braves:",
    "ARI": ":dbacks:",
    "BAL": ":orioles:",
    "BOS": ":redsox:",
    "CHC": ":cubs:",
    "CIN": ":reds:",
    "CLE": ":indians:",
    "COL": ":rockies:",
    "CWS": ":whitesox:",
    "DET": ":tigers:",
    "HOU": ":astros:",
    "KC": ":royals:",
    "LAA": ":angels:",
    "LAD": ":dodgers:",
    "MIA": ":marlins:",
    "MIL": ":brewers:",
    "MIN": ":twins:",
    "NYM": ":mets:",
    "NYY": ":yankees:",
    "OAK": ":athletics:",
    "PHI": ":phillies:",
    "PIT": ":pirates:",
    "SD": ":padres:",
    "SF": ":giants:",
    "SEA": ":mariners:",
    "STL": ":cardinals:",
    "TB": ":rays:",
    "TEX": ":rangers:",
    "TOR": ":jays:",
    "WAS": ":nationals:",
}
