#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugins/snacks', '', _path)
sys.path.append(_root)
from apis.plugin.plugin_api import PluginApi  # noqa
from apis.serializable.serializable_api import SerializableApi  # noqa
from utils.corpus.corpus_util import collect  # noqa
from utils.nltk.nltk_util import cfd, discuss  # noqa
from utils.slack.slack_util import channels_list, chat_post_message, users_list  # noqa


class SnacksPlugin(PluginApi, SerializableApi):
    def __init__(self, **kwargs):
        super(SnacksPlugin, self).__init__(**kwargs)
        self.cfd = {}

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
        self.day = kwargs['date'].day

        self.corpus()
        self.cfd = cfd(4, *self._fnames())

    def _on_message_internal(self, **kwargs):
        obj = kwargs['obj']
        if obj.get('channel') != 'G3SUFLMK4':
            return False

        text = obj.get('text', '')

        match = re.findall('^<@U3ULC7DBP> discuss (.+)$', text)
        if match:
            response = discuss(match[0], self.cfd, 4, 10, 20)
            chat_post_message('testing', response)
            return True

        return False

    def _run_internal(self, **kwargs):
        day = kwargs['date'].day
        if self.day != day:
            self.corpus()
            self.cfd = cfd(4, *self._fnames())
            self.day = day

    @staticmethod
    def _fnames():
        d = os.path.join(_root, 'corpus')
        return [os.path.join(d, c) for c in os.listdir(d)]

    @staticmethod
    def _members():
        users = users_list()
        members = {}
        if users['ok']:
            for member in users['members']:
                members[member['id']] = member['name']
        return members

    def corpus(self):
        channels = channels_list()
        if not channels['ok']:
            return

        for c in channels['channels']:
            channelid = c['id']
            collected = collect(channelid, self._members())
            fname = os.path.join(_root, 'corpus', channelid + '.txt')
            with open(fname, 'w') as f:
                f.write(collected)
