#!/usr/bin/env python

import json
import os
import tokens
import urllib
import urllib2


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


def chat_post_message(channel, text, attachments=[], thread_ts=''):
  return call_('chat.postMessage', {
      'token': tokens.filefairy,
      'channel': channel,
      'text': text,
      'as_user': 'true',
      'attachments': attachments,
      'link_names': 'true',
      'thread_ts': thread_ts
  })


def files_upload(content, filename, channel):
  return call_('files.upload', {
      'token': tokens.filefairy,
      'content': content,
      'filename': filename,
      'channels': channel,
  })


def rtm_connect():
  return call_('rtm.connect', {'token': tokens.filefairy})
