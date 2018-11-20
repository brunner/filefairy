#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import html
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/util/corpus', '', _path))
from common.slack.slack import channels_history  # noqa

_bots = ['U3ULC7DBP']
_snacks = ['C9YE6NQG0']
_subtypes = [
    'file_comment', 'me_message', 'message_changed', 'thread_broadcast'
]


def _rewrite(text):
    text = re.sub('(<https?://[^>]+>)|(<![^>]+>)|([()])', '', text)
    text = html.unescape(text).strip(' \t\n\r')
    return text


def collect(channelid):
    messages = {}

    latest = ''
    while True:
        history = channels_history(channelid, latest)
        if not history['ok']:
            break

        for m in history['messages']:
            if 'user' in m:
                user = m['user']

                if user in _bots and channelid not in _snacks:
                    continue
                if 'subtype' in m and m['subtype'] not in _subtypes:
                    continue

                for text in reversed(m['text'].splitlines()):
                    text = _rewrite(text)
                    if text:
                        match = re.findall('[?.!:]$', text)
                        if not match:
                            text += '.'

                        user = m['user']
                        if user not in messages:
                            messages[user] = []

                        messages[user].insert(0, text)

        if history['messages']:
            latest = history['messages'][-1].get('ts')
        else:
            break

    return messages
