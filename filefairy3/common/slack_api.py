#!/usr/bin/env python

import json
import os
import urllib
import urllib2
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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


def rtm_connect():
  return call_('rtm.connect', {'token': filefairy})
