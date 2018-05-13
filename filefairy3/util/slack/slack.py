#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/util/slack', '', _path))
from util.secrets.secrets import brunnerj  # noqa
from util.secrets.secrets import filefairy  # noqa
from util.urllib.urllib_ import urlopen  # noqa
from util.urllib.urllib_ import create_request  # noqa

_brunnerj = brunnerj()
_filefairy = filefairy()


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


def channels_kick(channel, user):
    return _call('channels.kick', {
        'token': _brunnerj,
        'channel': channel,
        'user': user,
    })


def channels_history(channel, latest):
    return _call('channels.history', {
        'token': _filefairy,
        'channel': channel,
        'count': 1000,
        'latest': latest,
    })


def channels_list():
    return _call('channels.list', {
        'token': _filefairy,
        'exclude_members': True,
        'exclude_archived': True
    })


def chat_post_message(channel, text, attachments=[]):
    return _call(
        'chat.postMessage', {
            'token': _filefairy,
            'channel': channel,
            'text': text,
            'as_user': 'true',
            'attachments': attachments,
            'link_names': 'true'
        })


def files_upload(content, filename, channel):
    return _call(
        'files.upload', {
            'token': _filefairy,
            'content': content,
            'filename': filename,
            'channels': channel,
        })


def reactions_add(name, channel, timestamp):
    return _call(
        'reactions.add', {
            'token': _filefairy,
            'name': name,
            'channel': channel,
            'timestamp': timestamp,
        })


def rtm_connect():
    return _call('rtm.connect', {'token': _filefairy})


def users_list():
    return _call('users.list', {'token': _filefairy})
