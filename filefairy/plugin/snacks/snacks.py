#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import os
import random
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugin/snacks', '', _path)
sys.path.append(_root)
from api.messageable.messageable import Messageable  # noqa
from api.registrable.registrable import Registrable  # noqa
from api.renderable.renderable import Renderable  # noqa
from api.runnable.runnable import Runnable  # noqa
from core.notify.notify import Notify  # noqa
from core.response.response import Response  # noqa
from core.task.task import Task  # noqa
from util.corpus.corpus import collect  # noqa
from util.nltk_.nltk_ import cfd  # noqa
from util.nltk_.nltk_ import discuss  # noqa
from util.nltk_.nltk_ import imitate  # noqa
from util.slack.slack import channels_list  # noqa
from util.slack.slack import chat_post_message  # noqa
from util.slack.slack import pins_add  # noqa
from util.slack.slack import reactions_add  # noqa
from util.slack.slack import users_list  # noqa

_channels = ['C9YE6NQG0', 'G3SUFLMK4']
_n = 4

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


class Snacks(Messageable, Registrable, Renderable, Runnable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.loaded = False

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _href():
        return '/fairylab/snacks/'

    @staticmethod
    def _info():
        return 'Feeds the masses bread and circuses.'

    @staticmethod
    def _title():
        return 'snacks'

    def _notify_internal(self, **kwargs):
        notify = kwargs['notify']
        response = Response()
        if notify == Notify.FAIRYLAB_DAY:
            self.loaded = False
            response.append_task(Task(target='_load'))
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

        data = self.data
        original = copy.deepcopy(data)

        channel = obj.get('channel', '')
        text = obj.get('text', '')

        ok = True
        if user not in data['members']:
            data['members'][user] = {'latest': ts}
        else:
            ok = float(ts) - float(data['members'][user]['latest']) > 10

        if ok:
            match = re.findall('^<@U3ULC7DBP> choose (.+)$', text)
            if match:
                choices = match[0].split(' or ')
                if len(choices) > 1:
                    statement = random.choice(_chooselist)
                    choice = random.choice(choices)
                    reply = re.sub('^([a-zA-Z])',
                                   lambda x: x.groups()[0].upper(),
                                   statement.format(choice), 1)
                    chat_post_message(channel, reply)
                    response.notify = [Notify.BASE]

            match = re.findall('^<@U3ULC7DBP> discuss (.+)$', text)
            if match:
                cfds = self.__dict__.get('cfds', {})
                cfd = cfds.get('all', {})
                reply = discuss(match[0], cfd, _n, 8, 30)
                if not reply:
                    reply = 'I don\'t know anything about ' + match[0] + '.'
                chat_post_message(channel, reply)
                response.notify = [Notify.BASE]

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
                response.notify = [Notify.BASE]

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
                response.notify = [Notify.BASE]

            match = re.findall('^<@U3ULC7DBP> say (.+)$', text)
            if match:
                chat_post_message(channel, match[0])
                response.notify = [Notify.BASE]

            if text == '<@U3ULC7DBP> snack me':
                for snack in self._snacks():
                    reactions_add(snack, channel, ts)
                    if snack == 'star' and user == 'U3ULC7DBP':
                        pins_add(channel, ts)
                response.notify = [Notify.BASE]

        if response.notify:
            data['members'][user]['latest'] = ts

        if data != original:
            self.write()

        return response

    def _render_internal(self, **kwargs):
        html = 'html/fairylab/snacks/index.html'
        _home = self._home(**kwargs)
        return [(html, '', 'snacks.html', _home)]

    def _run_internal(self, **kwargs):
        return Response()

    def _setup_internal(self, **kwargs):
        return Response(task=[Task(target='_load_internal')])

    def _shadow_internal(self, **kwargs):
        return []

    @staticmethod
    def _fnames():
        d = os.path.join(_root, 'resource/corpus')
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

        collected = {}
        for c in channels['channels']:
            channelid = c['id']
            _collect = collect(channelid, self.names)
            for user in _collect:
                if user not in collected:
                    collected[user] = []
                collected[user] += _collect[user]

        for user in collected:
            fname = os.path.join(_root, 'resource/corpus', user + '.txt')
            with open(fname, 'w') as f:
                f.write('\n'.join(collected[user]))

    def _home(self, **kwargs):
        return {}

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
