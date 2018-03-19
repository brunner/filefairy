#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugins/snacks', '', _path)
sys.path.append(_root)
from apis.plugin.plugin_api import PluginApi  # noqa
from apis.serializable.serializable_api import SerializableApi  # noqa
from utils.slack.slack_util import channels_history, channels_list, users_list  # noqa
from utils.unicode.unicode_util import deunicode  # noqa

_subtypes = [
    'file_comment', 'me_message', 'message_changed', 'thread_broadcast'
]


class SnacksPlugin(PluginApi, SerializableApi):
    def __init__(self, **kwargs):
        super(SnacksPlugin, self).__init__(**kwargs)

    @property
    def enabled(self):
        return True

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _info():
        return 'Feeds the masses bread and circuses.'

    def _setup(self, **kwargs):
        data = self.data
        original = copy.deepcopy(data)

        self.names = self._names()
        for member in data['members']:
            self._collect(member)

        if data != original:
            self.write()

    def _on_message_internal(self, **kwargs):
        pass

    def _run_internal(self, **kwargs):
        pass

    @staticmethod
    def _names():
        users = users_list()
        names = {}
        for member in users['members']:
            _id = member['id']
            name = member['name']
            names[_id] = name
        return names

    def _collect(self, member):
        data = self.data
        channels = channels_list()
        if not channels['ok']:
            return

        messages = []
        for c in channels['channels']:
            _id = c['id']
            oldest = data['members'][member]['oldest'].get(_id, 0)
            history = channels_history(_id, oldest)
            if not history['ok']:
                continue

            latest = False
            for m in history['messages']:
                if 'user' in m and m['user'] == member:
                    if latest is False and 'ts' in m:
                        data['members'][member]['oldest'][_id] = m['ts']
                        latest = True
                    if 'subtype' in m and m['subtype'] not in _subtypes:
                        continue

                    text = m['text']
                    match = re.findall('<(https?://[^>]+)>', text)
                    for url in match:
                        text = text.replace(url, '')

                    match = re.findall('<@([^>]+)>', text)
                    for user in match:
                        name = self.names[user] if user in self.names else ''
                        text = text.replace('@' + user, name)

                    match = re.findall('<#([^\|]+)\|', text)
                    for channel in match:
                        text = text.replace('#' + channel, '')

                    text = deunicode(text, errors='ignore')
                    text = re.sub('([\"#~*_\\\/:\(\)<\|>\n])', '', text)
                    text = text.strip()
                    if text:
                        messages.append(text)

        fname = os.path.join(_root, 'corpus', member + '.txt')
        with open(fname, 'a') as f:
            f.write('\n'.join(messages))
