#!/usr/bin/env python

import os
import subprocess
import tokens
import urllib
import urllib2


def postMessage(text):
  """Posts a text message to the Slack team."""
  url = "https://slack.com/api/chat.postMessage"
  fields = {"text": text, "token": tokens.filefairy, "channel": "testing",
            "link_names": "brunnerj,everyone", "as_user": "true"}
  full = "{0}?{1}".format(url, urllib.urlencode(fields))
  urllib2.urlopen(full)


def upload(filename):
  """Uploads a file to the Slack team."""
  fi = "file=@{0}".format(filename)
  token = "token={0}".format(tokens.filefairy)
  url = "https://slack.com/api/files.upload"

  with open(os.devnull, "wb") as f:
    subprocess.call(["curl", "-F", fi, "-F", "channels=#testing",
                     "-F", token, url], stderr=f, stdout=f)
