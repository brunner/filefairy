#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import random
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/tasks/snacks', '', _path)
sys.path.append(_root)

from api.registrable.registrable import Registrable  # noqa
from common.datetime_.datetime_ import decode_datetime  # noqa
from common.datetime_.datetime_ import encode_datetime  # noqa
from common.datetime_.datetime_ import timestamp  # noqa
from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa
from data.thread_.thread_ import Thread  # noqa
from util.corpus.corpus import collect  # noqa
from common.elements.elements import card  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import table  # noqa
from util.nltk_.nltk_ import cfd  # noqa
from util.nltk_.nltk_ import discuss  # noqa
from util.nltk_.nltk_ import imitate  # noqa
from common.slack.slack import channels_list  # noqa
from common.slack.slack import chat_post_message  # noqa
from common.slack.slack import pins_add  # noqa
from common.slack.slack import reactions_add  # noqa
from common.slack.slack import users_list  # noqa

_channels = ['C9YE6NQG0', 'G3SUFLMK4']
_n = 4

_chooselist = [
    '{}. Did you even need to ask?', 'Definitely {}.',
    'It\'s {}, any day of the week.', 'Easy, I prefer {}.',
    'I suppose {}, if I had to pick one.',
    'It\'s not ideal, but I\'ll go with {}.', '{}... I guess?',
    'That\'s a tough one. Maybe {}?'
]

_snackdict = {
    'amphora': '\U0001F3FA',
    'apple': '\U0001F34E',
    'avocado': '\U0001F951',
    'baby_bottle': '\U0001F37C',
    'bacon': '\U0001F953',
    'baguette_bread': '\U0001F956',
    'banana': '\U0001F34C',
    'beer': '\U0001F37A',
    'beers': '\U0001F37B',
    'bento': '\U0001F371',
    'birthday': '\U0001F382',
    'bowl_with_spoon': '\U0001F963',
    'bread': '\U0001F35E',
    'broccoli': '\U0001F966',
    'burrito': '\U0001F32F',
    'cake': '\U0001F370',
    'candy': '\U0001F36C',
    'canned_food': '\U0001F96B',
    'carrot': '\U0001F955',
    'champagne': '\U0001F37E',
    'cheese_wedge': '\U0001F9C0',
    'cherries': '\U0001F352',
    'chestnut': '\U0001F330',
    'chocolate_bar': '\U0001F36B',
    'chopsticks': '\U0001F962',
    'clinking_glasses': '\U0001F942',
    'cocktail': '\U0001F378',
    'coconut': '\U0001F965',
    'coffee': '\u2615',
    'cookie': '\U0001F36A',
    'corn': '\U0001F33D',
    'croissant': '\U0001F950',
    'cucumber': '\U0001F952',
    'cup_with_straw': '\U0001F964',
    'cut_of_meat': '\U0001F969',
    'curry': '\U0001F35B',
    'custard': '\U0001F36E',
    'dango': '\U0001F361',
    'doughnut': '\U0001F369',
    'dumpling': '\U0001F95F',
    'egg': '\U0001F95A',
    'eggplant': '\U0001F346',
    'fish_cake': '\U0001F365',
    'fork_and_knife': '\U0001F374',
    'fortune_cookie': '\U0001F960',
    'fried_egg': '\U0001F373',
    'fried_shrimp': '\U0001F364',
    'fries': '\U0001F35F',
    'glass_of_milk': '\U0001F95B',
    'grapes': '\U0001F347',
    'green_apple': '\U0001F34F',
    'green_salad': '\U0001F957',
    'hamburger': '\U0001F354',
    'hocho': '\U0001F52A',
    'honey_pot': '\U0001F36F',
    'hot_pepper': '\U0001F336',
    'hotdog': '\U0001F32D',
    'ice_cream': '\U0001F368',
    'icecream': '\U0001F366',
    'kiwifruit': '\U0001F95D',
    'knife_fork_plate': '\U0001F37D',
    'lemon': '\U0001F34B',
    'lollipop': '\U0001F36D',
    'meat_on_bone': '\U0001F356',
    'melon': '\U0001F348',
    'mushroom': '\U0001F344',
    'oden': '\U0001F362',
    'pancakes': '\U0001F95E',
    'peach': '\U0001F351',
    'peanuts': '\U0001F95C',
    'pear': '\U0001F350',
    'pie': '\U0001F967',
    'pineapple': '\U0001F34D',
    'pizza': '\U0001F355',
    'popcorn': '\U0001F37F',
    'potato': '\U0001F954',
    'poultry_leg': '\U0001F357',
    'pretzel': '\U0001F968',
    'ramen': '\U0001F35C',
    'rice': '\U0001F35A',
    'rice_ball': '\U0001F359',
    'rice_cracker': '\U0001F358',
    'sake': '\U0001F376',
    'sandwich': '\U0001F96A',
    'shallow_pan_of_food': '\U0001F958',
    'shaved_ice': '\U0001F367',
    'spaghetti': '\U0001F35D',
    'spoon': '\U0001F944',
    'star': '\u2B50',
    'stew': '\U0001F372',
    'strawberry': '\U0001F353',
    'stuffed_flatbread': '\U0001F959',
    'sushi': '\U0001F363',
    'sweet_potato': '\U0001F360',
    'taco': '\U0001F32E',
    'takeout_box': '\U0001F961',
    'tangerine': '\U0001F34A',
    'tea': '\U0001F375',
    'tomato': '\U0001F345',
    'trophy': '\U0001F3C6',
    'tropical_drink': '\U0001F379',
    'tumbler_glass': '\U0001F943',
    'watermelon': '\U0001F349',
    'wine_glass': '\U0001F377'
}

_snacklist = list(_snackdict.keys())
_snacklist.remove('star')
_snacklist.remove('trophy')

_wafflelist = [
    'Neither seems like a good option to me.',
    'Why not both?',
]


class Snacks(Registrable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.loaded = False

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

    def _notify_internal(self, **kwargs):
        notify = kwargs['notify']
        response = Response()
        if notify == Notify.FILEFAIRY_DAY:
            self.loaded = False
            response.append(thread_=Thread(target='_load'))
        return response

    def _on_message_internal(self, **kwargs):
        response = Response()

        if not self.loaded:
            return response

        obj = kwargs['obj']
        user = obj.get('user')
        ts = obj.get('ts')
        if obj.get('channel') not in _channels or not user or not ts:
            return response

        channel = obj.get('channel', '')
        text = obj.get('text', '')

        match = re.findall('^<@U3ULC7DBP> choose (.+)$', text)
        if match:
            choices = match[0].split(' or ')
            if len(choices) > 1:
                statement = random.choice(_chooselist + _wafflelist)
                choice = random.choice(choices)
                reply = re.sub('^([a-zA-Z])',
                               lambda x: x.groups()[0].upper(),
                               statement.format(choice), 1)
                chat_post_message(channel, reply)

        match = re.findall('^<@U3ULC7DBP> discuss (.+)$', text)
        if match:
            cfds = self.__dict__.get('cfds', {})
            cfd = cfds.get('all', {})
            reply = discuss(match[0], cfd, _n, 8, 30)
            if not reply:
                reply = 'I don\'t know anything about ' + match[0] + '.'
            chat_post_message(channel, reply)

        match = re.findall('^<@U3ULC7DBP> imitate <@([^>]+)>$', text)
        if match:
            cfds = self.__dict__.get('cfds', {})
            reply = ''
            if match[0] in cfds:
                cfd = cfds[match[0]]
                reply = imitate(cfd, _n, 8, 30)
            if not reply:
                reply = '<@' + match[0] + '> doesn\'t know anything.'
            chat_post_message(channel, reply)

        match = re.findall('^<@U3ULC7DBP> imitate <@([^>]+)> (.+)$', text)
        if match:
            target, topic = match[0]
            cfds = self.__dict__.get('cfds', {})
            reply = ''
            if target in cfds:
                cfd = cfds[target]
                reply = discuss(topic, cfd, _n, 8, 30)
            if not reply:
                reply = '<@' + target + '> doesn\'t know anything ' \
                        'about ' + topic + '.'
            chat_post_message(channel, reply)

        match = re.findall('^<@U3ULC7DBP> say (.+)$', text)
        if match:
            chat_post_message(channel, match[0])

        if text == '<@U3ULC7DBP> snack me':
            for snack in self._snacks():
                reactions_add(snack, channel, ts)
                if snack == 'star' and user == 'U3ULC7DBP':
                    pins_add(channel, ts)
            response.notify = [Notify.BASE]

        match = re.findall('^<@U3ULC7DBP> who .+$', text)
        if match:
            statement = random.choice(_chooselist)
            choice = random.choice(self.names)
            reply = statement.format(choice)
            chat_post_message(channel, reply)

        if response.notify:
            return response

        return Response()

    def _setup_internal(self, **kwargs):
        return Response(thread_=[Thread(target='_load_internal')])

    @staticmethod
    def _flip(s):
        r = ''
        for c in s:
            if c.isdigit():
                r += str(abs(9 - int(c)))
            else:
                r += c
        return r

    @staticmethod
    def _fnames():
        d = os.path.join(_root, 'resource/corpus')
        return [os.path.join(d, c) for c in os.listdir(d)]

    @staticmethod
    def _names():
        names = []
        users = users_list()
        if users['ok']:
            for member in users['members']:
                if member['deleted']:
                    continue
                if member['profile']['display_name']:
                    names.append(member['profile']['display_name'])
                else:
                    names.append(member['name'])
        return sorted(names)

    @staticmethod
    def _snacks():
        snacks = [random.choice(_snacklist) for _ in range(3)]
        if snacks[0] == snacks[1]:
            if snacks[1] == snacks[2]:
                snacks[2] = 'trophy'
            snacks[1] = 'star'
        elif snacks[0] == snacks[2]:
            snacks[1], snacks[2] = 'star', snacks[1]
        elif snacks[1] == snacks[2]:
            snacks[0], snacks[1], snacks[2] = snacks[1], 'star', snacks[0]
        return snacks

    def _corpus(self):
        channels = channels_list()
        if not channels['ok']:
            return

        collected = {}
        for c in channels['channels']:
            channelid = c['id']
            _collect = collect(channelid)
            for user in _collect:
                if user not in collected:
                    collected[user] = []
                collected[user] += _collect[user]

        for user in collected:
            fname = os.path.join(_root, 'resource/corpus', user + '.txt')
            with open(fname, 'w') as f:
                f.write('\n'.join(collected[user]))

    def _load(self, *args, **kwargs):
        self._corpus()
        return self._load_internal()

    def _load_internal(self, *args, **kwargs):
        self.cfds = {}

        fnames = self._fnames()

        for fname in fnames:
            key = fname.rstrip('.txt').rsplit('/', 1)[1]
            self.cfds[key] = cfd(_n, *[fname])

        self.cfds['all'] = cfd(_n, *fnames)

        self.names = self._names()
        self.loaded = True

        return Response()
