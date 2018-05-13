#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import os
import random
import re
import sys
import threading

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugin/snacks', '', _path)
sys.path.append(_root)
from api.plugin.plugin import Plugin  # noqa
from api.serializable.serializable import Serializable  # noqa
from util.corpus.corpus import collect  # noqa
from util.nltk.nltk_ import cfd  # noqa
from util.nltk.nltk_ import discuss  # noqa
from util.slack.slack import channels_kick  # noqa
from util.slack.slack import channels_list  # noqa
from util.slack.slack import chat_post_message  # noqa
from util.slack.slack import reactions_add  # noqa
from util.slack.slack import users_list  # noqa
from util.unicode.unicode import deunicode  # noqa
from value.notify.notify import Notify  # noqa
from value.response.response import Response  # noqa

_channels = ['C9YE6NQG0', 'G3SUFLMK4']

_chooselist = [
    '{}. Did you even need to ask?',
    'Definitely {}.',
    'It\'s {}, any day of the week.',
    'Easy, I prefer {}.',
    'I suppose {}, if I had to pick one.',
    'It\'s not ideal, but I\'ll go with {}.',
    '{}... I guess?',
    'That\'s a tough one. Maybe {}?',
    'Neither seems like a good option to me.',
    'Why not both?',
]

_snacklist = [
    'green_apple', 'apple', 'pear', 'tangerine', 'lemon', 'banana',
    'watermelon', 'grapes', 'strawberry', 'melon', 'cherries', 'peach',
    'pineapple', 'tomato', 'eggplant', 'hot_pepper', 'corn', 'sweet_potato',
    'honey_pot', 'bread', 'cheese_wedge', 'poultry_leg', 'meat_on_bone',
    'fried_shrimp', 'egg', 'hamburger', 'fries', 'hotdog', 'pizza',
    'spaghetti', 'taco', 'burrito', 'ramen', 'stew', 'fish_cake', 'sushi',
    'bento', 'curry', 'rice_ball', 'rice', 'rice_cracker', 'oden', 'dango',
    'shaved_ice', 'ice_cream', 'icecream', 'cake', 'birthday', 'custard',
    'candy', 'lollipop', 'chocolate_bar', 'popcorn', 'doughnut', 'cookie',
    'beer', 'beers', 'wine_glass', 'cocktail', 'tropical_drink', 'champagne',
    'sake', 'tea', 'coffee', 'baby_bottle', 'fork_and_knife',
    'knife_fork_plate'
]


class Snacks(Plugin, Serializable):
    def __init__(self, **kwargs):
        super(Snacks, self).__init__(**kwargs)
        self.loaded = False

    @property
    def enabled(self):
        return True

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _info():
        return 'Feeds the masses bread and circuses.'

    def _notify_internal(self, **kwargs):
        notify = kwargs['notify']
        if notify == Notify.FAIRYLAB_DAY:
            self.loaded = False
            t = threading.Thread(target=self._load)
            t.daemon = True
            t.start()
        return False

    def _on_message_internal(self, **kwargs):
        response = Response()

        if not self.loaded:
            return response

        obj = kwargs['obj']
        user = obj.get('user')
        ts = obj.get('ts')
        if obj.get('channel') not in _channels or not user or not ts:
            return response

        data = self.data
        original = copy.deepcopy(data)

        channel = obj.get('channel', '')
        text = deunicode(obj.get('text', ''), errors='ignore')

        ok = True
        if user not in data['members']:
            data['members'][user] = {'latest': ts}
        else:
            ok = float(ts) - float(data['members'][user]['latest']) > 10

        if ok:
            match = re.findall('^<@U3ULC7DBP> choose (.+)$', text)
            if match:
                statement = random.choice(_chooselist)
                choice = random.choice(match[0].split(' or '))
                reply = re.sub('^([a-zA-Z])', lambda x: x.groups()[0].upper(),
                               statement.format(choice), 1)
                chat_post_message(channel, reply)
                response.notify = [Notify.BASE]

            match = re.findall('^<@U3ULC7DBP> discuss (.+)$', text)
            if match:
                cfd = self.__dict__.get('cfd', {})
                reply = discuss(match[0], cfd, 4, 8, 30)
                chat_post_message(channel, reply)
                response.notify = [Notify.BASE]

            match = re.findall('^<@U3ULC7DBP> kick <@(.+)>$', text)
            if match and match[0] in self.names:
                channels_kick(channel, match[0])
                response.notify = [Notify.BASE]

            match = re.findall('^<@U3ULC7DBP> say (.+)$', text)
            if match:
                chat_post_message(channel, match[0])
                response.notify = [Notify.BASE]

            if text == '<@U3ULC7DBP> snack me':
                for snack in self._snacks():
                    reactions_add(snack, channel, ts)
                response.notify = [Notify.BASE]

        if response.notify:
            data['members'][user]['latest'] = ts

        if data != original:
            self.write()

        return response

    def _run_internal(self, **kwargs):
        return Response()

    def _setup_internal(self, **kwargs):
        t = threading.Thread(target=self._load_internal)
        t.daemon = True
        t.start()

    def _shadow_internal(self, **kwargs):
        return {}

    @staticmethod
    def _fnames():
        d = os.path.join(_root, 'corpus')
        return [os.path.join(d, c) for c in os.listdir(d)]

    @staticmethod
    def _names():
        users = users_list()
        members = {}
        if users['ok']:
            for member in users['members']:
                members[member['id']] = member['name']
        return members

    @staticmethod
    def _snacks():
        snacks = [random.choice(_snacklist) for _ in range(2)]
        if snacks[0] == snacks[1]:
            snacks[1] = 'star'
        return snacks

    def _corpus(self):
        channels = channels_list()
        if not channels['ok']:
            return

        for c in channels['channels']:
            channelid = c['id']
            collected = collect(channelid, self.names)
            fname = os.path.join(_root, 'corpus', channelid + '.txt')
            with open(fname, 'w') as f:
                f.write(collected)

    def _load(self):
        self._corpus()
        self._load_internal()

    def _load_internal(self):
        self.cfd = cfd(4, *self._fnames())
        self.names = self._names()
        self.loaded = True
