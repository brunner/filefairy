#!/usr/bin/env python
# -*- coding: utf-8 -*-

import HTMLParser
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/util/corpus', '', _path))
from util.slack.slack import channels_history  # noqa
from util.unicode.unicode import deunicode  # noqa

_h = HTMLParser.HTMLParser()
_bots = ['U3ULC7DBP']
_subtypes = [
    'file_comment', 'me_message', 'message_changed', 'thread_broadcast'
]


def _rewrite(text, members):
    text = re.sub('(<https?://[^>]+>)|(<![^>]+>)|([()])', '', text)
    text = deunicode(text, errors='ignore')
    text = _h.unescape(text).strip(' \t\n\r')
    return text


def collect(channelid, members):
    messages = []

    latest = ''
    while True:
        history = channels_history(channelid, latest)
        if not history['ok']:
            break

        for m in history['messages']:
            if 'user' in m and m['user'] not in _bots:
                if 'subtype' in m and m['subtype'] not in _subtypes:
                    continue

                for text in reversed(m['text'].splitlines()):
                    text = _rewrite(text, members)
                    if text:
                        match = re.findall('[?.!:]$', text)
                        if not match:
                            text += '.'

                        messages.insert(0, text)

        if history['messages']:
            latest = history['messages'][-1].get('ts')
        else:
            break

    return '\n'.join(messages)
