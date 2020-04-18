#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Feeds the masses bread and circuses."""

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
from common.re_.re_ import search  # noqa
from common.service.service import call_service  # noqa
from common.slack.slack import chat_post_message  # noqa
from common.slack.slack import reactions_add  # noqa
from types_.notify.notify import Notify  # noqa
from types_.response.response import Response  # noqa
from types_.thread_.thread_ import Thread  # noqa

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
        return None

    @staticmethod
    def _href():
        return ''

    @staticmethod
    def _title():
        return 'snacks'

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

        string = search(r'(?s)^<@U3ULC7DBP> choose (.+)$', text)
        if string:
            options = string.split(' or ')
            reply = call_service('circus', 'choose', (options, ))
            chat_post_message(channel, reply)

        topic = search(r'(?s)^<@U3ULC7DBP> discuss (.+)$', text)
        if topic:
            cfd = self.cfds.get('all', {})
            fargs = (topic, cfd, NUM, MIN, MAX)
            reply = call_service('circus', 'discuss', fargs)
            if not reply:
                reply = 'I don\'t know anything about {}.'.format(topic)
            chat_post_message(channel, reply)

        user = search(r'(?s)^<@U3ULC7DBP> imitate <@([^>]+)>$', text)
        if user:
            cfd = self.cfds.get(user, {})
            topic = get_topic(cfd)
            fargs = (topic, cfd, NUM, MIN, MAX)
            reply = call_service('circus', 'discuss', fargs)
            if not reply:
                reply = '<@{}> doesn\'t know anything.'.format(user)
            chat_post_message(channel, reply)

        user, topic = search(r'(?s)^<@U3ULC7DBP> imitate <@([^>]+)> (.+)$',
                             text)
        if user:
            cfd = self.cfds.get(user, {})
            fargs = (topic, cfd, NUM, MIN, MAX)
            reply = call_service('circus', 'discuss', fargs)
            if not reply:
                reply = '<@{}> doesn\'t know anything about {}.'.format(
                    user, topic)
            chat_post_message(channel, reply)

        topic = search(r'(?s)^<@U3ULC7DBP> say (.+)$', text)
        if topic:
            chat_post_message(channel, topic)

        if search(r'(?s)^<@U3ULC7DBP> snack me$', text):
            for snack in call_service('bread', 'snack_me', ()):
                reactions_add(snack, channel, obj['ts'])

        if search(r'(?s)^<@U3ULC7DBP> who .+$', text):
            reply = call_service('circus', 'who', (self.users, ))
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
        for user, message in sorted(messages.items()):
            self.cfds[user] = get_cfd(NUM, message)
            all_ += message
        self.cfds['all'] = get_cfd(NUM, all_)

        self.users = users

        return Response()

    @staticmethod
    def _valid(obj):
        if any(k not in obj for k in ['channel', 'text', 'ts']):
            return False

        if obj['channel'] not in ['C9YE6NQG0', 'G3SUFLMK4']:
            return False

        if not search(r'(?s)^<@U3ULC7DBP>', obj['text']):
            return False

        return True
