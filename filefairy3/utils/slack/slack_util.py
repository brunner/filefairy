#!/usr/bin/env python

import json
import os
import re
import sys
import urllib
import urllib2

sys.path.append(re.sub(r'/utils/slack', '', os.path.dirname(os.path.abspath(__file__))))
from private.tokens import filefairy  # noqa

testing_name = 'testing'
testing_id = 'G3SUFLMK4'


def contains_text(obj, text):
    return 'text' in obj and text in obj['text']


def from_channel(obj, id_):
    return 'channel' in obj and obj['channel'] == id_


def _call(method, params):
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
    return _call(
        'chat.postMessage', {
            'token': filefairy,
            'channel': channel,
            'text': text,
            'as_user': 'true',
            'link_names': 'true',
        })


def rtm_connect():
    return _call('rtm.connect', {'token': filefairy})
