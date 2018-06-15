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
from util.ago.ago import delta  # noqa
from util.corpus.corpus import collect  # noqa
from util.component.component import card  # noqa
from util.component.component import table  # noqa
from util.datetime_.datetime_ import decode_datetime  # noqa
from util.datetime_.datetime_ import encode_datetime  # noqa
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
    'amphora', 'apple', 'avocado', 'baby_bottle', 'bacon', 'baguette_bread',
    'banana', 'beer', 'beers', 'bento', 'birthday', 'bowl_with_spoon', 'bread',
    'broccoli', 'burrito', 'cake', 'candy', 'canned_food', 'carrot',
    'champagne', 'cheese_wedge', 'cherries', 'chestnut', 'chocolate_bar',
    'chopsticks', 'clinking_glasses', 'cocktail', 'coconut', 'coffee',
    'cookie', 'corn', 'croissant', 'cucumber', 'cup_with_straw', 'cut_of_meat',
    'curry', 'custard', 'dango', 'doughnut', 'dumpling', 'egg', 'eggplant',
    'fish_cake', 'fork_and_knife', 'fortune_cookie', 'fried_egg',
    'fried_shrimp', 'fries', 'glass_of_milk', 'grapes', 'green_apple',
    'green_salad', 'hamburger', 'hocho', 'honey_pot', 'hot_pepper', 'hotdog',
    'ice_cream', 'icecream', 'kiwifruit', 'knife_fork_plate', 'lemon',
    'lollipop', 'meat_on_bone', 'melon', 'mushroom', 'oden', 'pancakes',
    'peach', 'peanuts', 'pear', 'pie', 'pineapple', 'pizza', 'popcorn',
    'potato', 'poultry_leg', 'pretzel', 'ramen', 'rice', 'rice_ball',
    'rice_cracker', 'sake', 'sandwich', 'shallow_pan_of_food', 'shaved_ice',
    'spaghetti', 'spoon', 'star', 'stew', 'strawberry', 'stuffed_flatbread',
    'sushi', 'sweet_potato', 'taco', 'takeout_box', 'tangerine', 'tea',
    'tomato', 'trophy', 'tropical_drink', 'tumbler_glass', 'watermelon',
    'wine_glass'
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
            data['members'][user] = ts
        else:
            ok = float(ts) - float(data['members'][user]) > 10

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
                edate = encode_datetime(kwargs['date'])
                for snack in self._snacks():
                    reactions_add(snack, channel, ts)
                    if snack == 'star' and user == 'U3ULC7DBP':
                        pins_add(channel, ts)
                    c = data['count'].get(snack, 0) + 1
                    data['count'][snack] = c
                    data['last'][snack] = edate
                response.notify = [Notify.BASE]
                self._render(**kwargs)

        if response.notify:
            data['members'][user] = ts

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
        self._render(**kwargs)
        return Response(task=[Task(target='_load_internal')])

    def _shadow_internal(self, **kwargs):
        return []

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
        users = users_list()
        members = {}
        if users['ok']:
            for member in users['members']:
                members[member['id']] = member['name']
        return members

    @staticmethod
    def _snacks():
        snacks = [random.choice(_snacklist) for _ in range(3)]
        if snacks[0] == snacks[1]:
            if snacks[1] == snacks[2]:
                snacks[2] = 'trophy'
            snacks[1] = 'star'
        elif snacks[1] == snacks[2]:
            snacks[2] = 'star'
        return snacks

    def _body_count(self):
        body = []
        count = self.data['count']
        for snack in sorted(count, key=lambda x: (-count[x], x)):
            body.append([snack, str(count[snack])])
            if len(body) == 15:
                break
        return body

    def _body_recent(self, now):
        body = []
        last = self.data['last']
        for snack in sorted(last, key=lambda x: (self._flip(last[x]), x)):
            body.append([snack, self._ts(last[snack], now)])
            if len(body) == 15:
                break
        return body

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
        data = self.data
        ret = {
            'breadcrumbs': [{
                'href': '/fairylab/',
                'name': 'Home'
            }, {
                'href': '',
                'name': 'Snacks'
            }]
        }

        date = kwargs['date']

        count, last = self._servings()
        ts = self._ts(last, date)
        servings = card(title=str(count), info='Total snacks served.', ts=ts)

        count = data['count'].get('star', 0)
        last = data['last'].get('star', '')
        ts = self._ts(last, date)
        stars = card(title=str(count), info='Total stars awarded.', ts=ts)

        count = data['count'].get('trophy', 0)
        last = data['last'].get('trophy', '')
        ts = self._ts(last, date)
        trophies = card(title=str(count), info='Total trophies lifted.', ts=ts)

        ret['statistics'] = [servings, stars, trophies]

        cols = ['', ' class="text-right"']
        if data['count']:
            ret['count'] = table(
                clazz='border mt-3',
                hcols=cols,
                bcols=cols,
                head=['Name', 'Count'],
                body=self._body_count())

        if data['last']:
            ret['recent'] = table(
                clazz='border mt-3',
                hcols=cols,
                bcols=cols,
                head=['Name', 'Last activity'],
                body=self._body_recent(date))

        return ret

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

    def _servings(self):
        data = self.data
        count = 0
        for snack in data['count']:
            count += data['count'][snack]
        last = ''
        for snack in data['last']:
            if not last or last < data['last'][snack]:
                last = data['last'][snack]
        return count // 3, last

    def _ts(self, then, now):
        if then:
            return delta(decode_datetime(then), now)
        return 'never'
