#!/usr/bin/env python

import json
import os
import re
import sys
import urllib
import urllib2

sys.path.append(re.sub(r'/utils/slack', '', os.path.dirname(__file__)))
from private.tokens import filefairy

def call_(method, params):
  url = 'https://slack.com/api/{}'.format(method)
  obj = {'ok': False}
  try:
    request = urllib2.Request(url, urllib.urlencode(params))
    response = urllib2.urlopen(request)
    obj = json.loads(response.read())
  except:
    pass
  return obj


def chat_post_message(channel, text):
  return call_('chat.postMessage', {
      'token': filefairy,
      'channel': channel,
      'text': text,
      'as_user': 'true',
      'link_names': 'true',
  })


def rtm_connect():
  return call_('rtm.connect', {'token': filefairy})


def get_testing_name():
  return 'testing'
