#!/usr/bin/env python

import json
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/utils/slack', '', _path))
from utils.secrets.secrets_util import filefairy  # noqa
from utils.urllib.urllib_util import urlopen, create_request  # noqa


def _call(method, params):
    url = 'https://slack.com/api/{}'.format(method)
    obj = {'ok': False}
    try:
        request = create_request(url, params)
        response = urlopen(request)
        obj = json.loads(response)
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


def files_upload(content, filename, channel):
    return _call(
        'files.upload', {
            'token': filefairy,
            'content': content,
            'filename': filename,
            'channels': channel,
        })


def rtm_connect():
    return _call('rtm.connect', {'token': filefairy})
