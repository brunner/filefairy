#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Provides various entertainment when prompted in the #snacks channel."""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/tasks/snacks', '', _path))

from api.registrable.registrable import Registrable  # noqa
from common.nltk_.nltk_ import get_cfd  # noqa
from common.nltk_.nltk_ import get_messages  # noqa
from common.nltk_.nltk_ import get_topic  # noqa
from common.nltk_.nltk_ import get_users  # noqa
from common.re_.re_ import find  # noqa
from common.slack.slack import chat_post_message  # noqa
from common.slack.slack import reactions_add  # noqa
from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa
from data.thread_.thread_ import Thread  # noqa

NUM = 4
MIN = 8
MAX = 30


class Snacks(Registrable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cfds = {}
        self.users = []

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _href():
        return ''

    @staticmethod
    def _info():
        return 'Feeds the masses bread and circuses.'

    @staticmethod
    def _title():
        return 'snacks'

    def _reload_data(self, **kwargs):
        return {'bread': ['snack_me'], 'circus': ['choose', 'discuss', 'who']}

    def _notify_internal(self, **kwargs):
        if kwargs['notify'] == Notify.FILEFAIRY_DAY:
            return Response(thread_=[Thread(target='_refresh')])

        return Response()

    def _on_message_internal(self, **kwargs):
        obj = kwargs['obj']
        if not self._valid(obj):
            return Response()

        channel = obj['channel']
        text = obj['text']

        string = find(r'(?s)^<@U3ULC7DBP> choose (.+)$', text)
        if string:
            options = string.split(' or ')
            reply = self._call('choose', (options, ))
            chat_post_message(channel, reply)

        topic = find(r'(?s)^<@U3ULC7DBP> discuss (.+)$', text)
        if topic:
            cfd = self.cfds.get('all', {})
            reply = self._call('discuss', (topic, cfd, NUM, MIN, MAX))
            if not reply:
                reply = 'I don\'t know anything about {}.'.format(topic)
            chat_post_message(channel, reply)

        user = find(r'(?s)^<@U3ULC7DBP> imitate <@([^>]+)>$', text)
        if user:
            cfd = self.cfds.get(user, {})
            topic = get_topic(cfd)
            reply = self._call('discuss', (topic, cfd, NUM, MIN, MAX))
            if not reply:
                reply = '<@{}> doesn\'t know anything.'.format(user)
            chat_post_message(channel, reply)

        user, topic = find(r'(?s)^<@U3ULC7DBP> imitate <@([^>]+)> (.+)$', text)
        if user:
            cfd = self.cfds.get(user, {})
            reply = self._call('discuss', (topic, cfd, NUM, MIN, MAX))
            if not reply:
                reply = '<@{}> doesn\'t know anything about {}.'.format(
                    user, topic)
            chat_post_message(channel, reply)

        topic = find(r'(?s)^<@U3ULC7DBP> say (.+)$', text)
        if topic:
            chat_post_message(channel, topic)

        if find(r'(?s)^<@U3ULC7DBP> snack me$', text):
            for snack in self._call('snack_me', ()):
                reactions_add(snack, channel, obj['ts'])

        if find(r'(?s)^<@U3ULC7DBP> who .+$', text):
            reply = self._call('who', (self.users, ))
            chat_post_message(channel, reply)

        return Response()

    def _setup_internal(self, **kwargs):
        return Response(thread_=[Thread(target='_refresh')])

    def _refresh(self, *args, **kwargs):
        messages = get_messages()
        users = get_users()
        if not messages or not users:
            return Response()

        all_ = []
        for user in messages:
            self.cfds[user] = get_cfd(NUM, messages[user])
            all_ += messages[user]
        self.cfds['all'] = get_cfd(NUM, all_)

        self.users = users

        return Response()

    @staticmethod
    def _valid(obj):
        if any(k not in obj for k in ['channel', 'text', 'ts']):
            return False

        if obj['channel'] not in ['C9YE6NQG0', 'G3SUFLMK4']:
            return False

        if not find(r'(?s)^<@U3ULC7DBP>', obj['text']):
            return False

        return True
