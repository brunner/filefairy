#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugins/snacks', '', _path)
sys.path.append(_root)
from apis.plugin.plugin_api import PluginApi  # noqa
from apis.serializable.serializable_api import SerializableApi  # noqa
from utils.corpus.corpus_util import collect  # noqa
from utils.nltk.nltk_util import cfd, discuss  # noqa
from utils.slack.slack_util import channels_list, chat_post_message, reactions_add, users_list  # noqa

_snacklist = [
    "green_apple", "apple", "pear", "tangerine", "lemon", "banana",
    "watermelon", "grapes", "strawberry", "melon", "cherries", "peach",
    "pineapple", "tomato", "eggplant", "hot_pepper", "corn", "sweet_potato",
    "honey_pot", "bread", "cheese_wedge", "poultry_leg", "meat_on_bone",
    "fried_shrimp", "egg", "hamburger", "fries", "hotdog", "pizza",
    "spaghetti", "taco", "burrito", "ramen", "stew", "fish_cake", "sushi",
    "bento", "curry", "rice_ball", "rice", "rice_cracker", "oden", "dango",
    "shaved_ice", "ice_cream", "icecream", "cake", "birthday", "custard",
    "candy", "lollipop", "chocolate_bar", "popcorn", "doughnut", "cookie",
    "beer", "beers", "wine_glass", "cocktail", "tropical_drink", "champagne",
    "sake", "tea", "coffee", "baby_bottle", "fork_and_knife",
    "knife_fork_plate"
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
        self.cfd = cfd(4, *self._fnames())
        self.day = kwargs['date'].day

    def _on_message_internal(self, **kwargs):
        obj = kwargs['obj']
        if obj.get('channel') != 'G3SUFLMK4':
            return False

        channel = obj.get('channel', '')
        text = obj.get('text', '')
        ts = obj.get('ts', '')

        match = re.findall('^<@U3ULC7DBP> discuss (.+)$', text)
        if match:
            cfd = self.__dict__.get('cfd', {})
            response = discuss(match[0], cfd, 4, 10, 20)
            chat_post_message('testing', response)
            return True

        if text == '<@U3ULC7DBP> snack me':
            for snack in self._snacks():
                reactions_add(snack, channel, ts)
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

    @staticmethod
    def _snacks():
        snacks = [random.choice(_snacklist) for _ in range(2)]
        if snacks[0] == snacks[1]:
            snacks[1] = 'star'
        return snacks

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
