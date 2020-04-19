#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for snacks.py."""

import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.extend((_path, re.sub(r'/tasks/snacks', '', _path)))

from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.json_.json_ import dumps  # noqa
from common.nltk_.nltk_ import get_cfd  # noqa
from common.test.test import Test  # noqa
from tasks.snacks.snacks import Snacks  # noqa
from types_.notify.notify import Notify  # noqa
from types_.response.response import Response  # noqa
from types_.thread_.thread_ import Thread  # noqa

DATE_10260602 = datetime_datetime_pst(1985, 10, 26, 6, 2, 30)
DATE_10260604 = datetime_datetime_pst(1985, 10, 26, 6, 4)

CFD = get_cfd(2, ['The quick brown fox.', 'Jumps over the lazy dog.'])


class SnacksTest(Test):
    def create_snacks(self, cfds=None, users=None):
        snacks = Snacks(date=DATE_10260602)

        if cfds:
            snacks.cfds = cfds
        if users:
            snacks.users = users

        return snacks

    def test_notify__filefairy_day(self):
        snacks = self.create_snacks()
        actual = snacks._notify_internal(notify=Notify.FILEFAIRY_DAY)
        expected = Response(thread_=[Thread(target='refresh')])
        self.assertEqual(actual, expected)

    def test_notify__other(self):
        snacks = self.create_snacks()
        actual = snacks._notify_internal(notify=Notify.OTHER)
        expected = Response()
        self.assertEqual(actual, expected)

    @mock.patch('tasks.snacks.snacks.reactions_add')
    @mock.patch.object(Snacks, 'is_valid_message')
    @mock.patch('tasks.snacks.snacks.get_topic')
    @mock.patch('tasks.snacks.snacks.chat_post_message')
    @mock.patch('tasks.snacks.snacks.call_service')
    def test_on_message__invalid(self, call_service_, chat_post_message_,
                                 get_topic_, is_valid_message_,
                                 reactions_add_):
        is_valid_message_.return_value = False

        obj = {'channel': 'C123'}
        snacks = self.create_snacks()
        response = snacks._on_message_internal(date=DATE_10260604, obj=obj)
        self.assertEqual(response, Response())

        is_valid_message_.assert_called_once_with(obj)
        self.assertNotCalled(call_service_, chat_post_message_, reactions_add_,
                             get_topic_)

    @mock.patch('tasks.snacks.snacks.reactions_add')
    @mock.patch.object(Snacks, 'is_valid_message')
    @mock.patch('tasks.snacks.snacks.get_topic')
    @mock.patch('tasks.snacks.snacks.chat_post_message')
    @mock.patch('tasks.snacks.snacks.call_service')
    def test_on_message__choose(self, call_service_, chat_post_message_,
                                get_topic_, is_valid_message_, reactions_add_):
        call_service_.return_value = 'Definitely a.'
        is_valid_message_.return_value = True

        obj = {'channel': 'C123', 'text': '<@U3ULC7DBP> choose a or b'}
        snacks = self.create_snacks()
        response = snacks._on_message_internal(date=DATE_10260604, obj=obj)
        self.assertEqual(response, Response())

        call_service_.assert_called_once_with('circus', 'choose',
                                              (['a', 'b'], ))
        chat_post_message_.assert_called_once_with('C123', 'Definitely a.')
        is_valid_message_.assert_called_once_with(obj)
        self.assertNotCalled(reactions_add_, get_topic_)

    @mock.patch('tasks.snacks.snacks.reactions_add')
    @mock.patch.object(Snacks, 'is_valid_message')
    @mock.patch('tasks.snacks.snacks.get_topic')
    @mock.patch('tasks.snacks.snacks.chat_post_message')
    @mock.patch('tasks.snacks.snacks.call_service')
    def test_on_message__discuss_known(self, call_service_, chat_post_message_,
                                       get_topic_, is_valid_message_,
                                       reactions_add_):
        call_service_.return_value = 'A b c.'
        is_valid_message_.return_value = True

        obj = {'channel': 'C123', 'text': '<@U3ULC7DBP> discuss a'}
        snacks = self.create_snacks(cfds={'all': CFD})
        response = snacks._on_message_internal(date=DATE_10260604, obj=obj)
        self.assertEqual(response, Response())

        call_service_.assert_called_once_with('circus', 'discuss',
                                              ('a', CFD, 4, 8, 30))
        chat_post_message_.assert_called_once_with('C123', 'A b c.')
        is_valid_message_.assert_called_once_with(obj)
        self.assertNotCalled(reactions_add_, get_topic_)

    @mock.patch('tasks.snacks.snacks.reactions_add')
    @mock.patch.object(Snacks, 'is_valid_message')
    @mock.patch('tasks.snacks.snacks.get_topic')
    @mock.patch('tasks.snacks.snacks.chat_post_message')
    @mock.patch('tasks.snacks.snacks.call_service')
    def test_on_message__discuss_unknown(self, call_service_,
                                         chat_post_message_, get_topic_,
                                         is_valid_message_, reactions_add_):
        call_service_.return_value = None
        is_valid_message_.return_value = True

        obj = {'channel': 'C123', 'text': '<@U3ULC7DBP> discuss a'}
        snacks = self.create_snacks(cfds={'all': CFD})
        response = snacks._on_message_internal(date=DATE_10260604, obj=obj)
        self.assertEqual(response, Response())

        call_service_.assert_called_once_with('circus', 'discuss',
                                              ('a', CFD, 4, 8, 30))
        chat_post_message_.assert_called_once_with(
            'C123', 'I don\'t know anything about a.')
        is_valid_message_.assert_called_once_with(obj)
        self.assertNotCalled(reactions_add_, get_topic_)

    @mock.patch('tasks.snacks.snacks.reactions_add')
    @mock.patch.object(Snacks, 'is_valid_message')
    @mock.patch('tasks.snacks.snacks.get_topic')
    @mock.patch('tasks.snacks.snacks.chat_post_message')
    @mock.patch('tasks.snacks.snacks.call_service')
    def test_on_message__imitate_known(self, call_service_, chat_post_message_,
                                       get_topic_, is_valid_message_,
                                       reactions_add_):
        call_service_.return_value = 'A b c.'
        get_topic_.return_value = 'a'
        is_valid_message_.return_value = True

        obj = {'channel': 'C123', 'text': '<@U3ULC7DBP> imitate <@U123>'}
        snacks = self.create_snacks(cfds={'U123': CFD})
        response = snacks._on_message_internal(date=DATE_10260604, obj=obj)
        self.assertEqual(response, Response())

        call_service_.assert_called_once_with('circus', 'discuss',
                                              ('a', CFD, 4, 8, 30))
        chat_post_message_.assert_called_once_with('C123', 'A b c.')
        get_topic_.assert_called_once_with(CFD)
        is_valid_message_.assert_called_once_with(obj)
        self.assertNotCalled(reactions_add_)

    @mock.patch('tasks.snacks.snacks.reactions_add')
    @mock.patch.object(Snacks, 'is_valid_message')
    @mock.patch('tasks.snacks.snacks.get_topic')
    @mock.patch('tasks.snacks.snacks.chat_post_message')
    @mock.patch('tasks.snacks.snacks.call_service')
    def test_on_message__imitate_unknown(self, call_service_,
                                         chat_post_message_, get_topic_,
                                         is_valid_message_, reactions_add_):
        call_service_.return_value = None
        get_topic_.return_value = None
        is_valid_message_.return_value = True

        obj = {'channel': 'C123', 'text': '<@U3ULC7DBP> imitate <@U123>'}
        snacks = self.create_snacks()
        response = snacks._on_message_internal(date=DATE_10260604, obj=obj)
        self.assertEqual(response, Response())

        call_service_.assert_called_once_with('circus', 'discuss',
                                              (None, {}, 4, 8, 30))
        chat_post_message_.assert_called_once_with(
            'C123', '<@U123> doesn\'t know anything.')
        get_topic_.assert_called_once_with({})
        is_valid_message_.assert_called_once_with(obj)
        self.assertNotCalled(reactions_add_)

    @mock.patch('tasks.snacks.snacks.reactions_add')
    @mock.patch.object(Snacks, 'is_valid_message')
    @mock.patch('tasks.snacks.snacks.get_topic')
    @mock.patch('tasks.snacks.snacks.chat_post_message')
    @mock.patch('tasks.snacks.snacks.call_service')
    def test_on_message__imitate_topic_known(self, call_service_,
                                             chat_post_message_, get_topic_,
                                             is_valid_message_,
                                             reactions_add_):
        call_service_.return_value = 'A b c.'
        is_valid_message_.return_value = True

        obj = {'channel': 'C123', 'text': '<@U3ULC7DBP> imitate <@U123> a'}
        snacks = self.create_snacks(cfds={'U123': CFD})
        response = snacks._on_message_internal(date=DATE_10260604, obj=obj)
        self.assertEqual(response, Response())

        call_service_.assert_called_once_with('circus', 'discuss',
                                              ('a', CFD, 4, 8, 30))
        chat_post_message_.assert_called_once_with('C123', 'A b c.')
        is_valid_message_.assert_called_once_with(obj)
        self.assertNotCalled(reactions_add_, get_topic_)

    @mock.patch('tasks.snacks.snacks.reactions_add')
    @mock.patch.object(Snacks, 'is_valid_message')
    @mock.patch('tasks.snacks.snacks.get_topic')
    @mock.patch('tasks.snacks.snacks.chat_post_message')
    @mock.patch('tasks.snacks.snacks.call_service')
    def test_on_message__imitate_topic_unknown(self, call_service_,
                                               chat_post_message_, get_topic_,
                                               is_valid_message_,
                                               reactions_add_):
        call_service_.return_value = None
        is_valid_message_.return_value = True

        obj = {'channel': 'C123', 'text': '<@U3ULC7DBP> imitate <@U123> a'}
        snacks = self.create_snacks()
        response = snacks._on_message_internal(date=DATE_10260604, obj=obj)
        self.assertEqual(response, Response())

        call_service_.assert_called_once_with('circus', 'discuss',
                                              ('a', {}, 4, 8, 30))
        chat_post_message_.assert_called_once_with(
            'C123', '<@U123> doesn\'t know anything about a.')
        is_valid_message_.assert_called_once_with(obj)
        self.assertNotCalled(reactions_add_, get_topic_)

    @mock.patch('tasks.snacks.snacks.reactions_add')
    @mock.patch.object(Snacks, 'is_valid_message')
    @mock.patch('tasks.snacks.snacks.get_topic')
    @mock.patch('tasks.snacks.snacks.chat_post_message')
    @mock.patch('tasks.snacks.snacks.call_service')
    def test_on_message__say(self, call_service_, chat_post_message_,
                             get_topic_, is_valid_message_, reactions_add_):
        is_valid_message_.return_value = True

        obj = {'channel': 'C123', 'text': '<@U3ULC7DBP> say a'}
        snacks = self.create_snacks()
        response = snacks._on_message_internal(date=DATE_10260604, obj=obj)
        self.assertEqual(response, Response())

        chat_post_message_.assert_called_once_with('C123', 'a')
        is_valid_message_.assert_called_once_with(obj)
        self.assertNotCalled(call_service_, reactions_add_, get_topic_)

    @mock.patch('tasks.snacks.snacks.reactions_add')
    @mock.patch.object(Snacks, 'is_valid_message')
    @mock.patch('tasks.snacks.snacks.get_topic')
    @mock.patch('tasks.snacks.snacks.chat_post_message')
    @mock.patch('tasks.snacks.snacks.call_service')
    def test_on_message__snack_me(self, call_service_, chat_post_message_,
                                  get_topic_, is_valid_message_,
                                  reactions_add_):
        s = ['amphora', 'apple', 'avocado']
        call_service_.return_value = s
        is_valid_message_.return_value = True

        obj = {'channel': 'C123', 'text': '<@U3ULC7DBP> snack me', 'ts': '1'}
        snacks = self.create_snacks()
        response = snacks._on_message_internal(date=DATE_10260604, obj=obj)
        self.assertEqual(response, Response())

        call_service_.assert_called_once_with('bread', 'snack_me', ())
        reactions_add_.assert_has_calls([mock.call(x, 'C123', '1') for x in s])
        is_valid_message_.assert_called_once_with(obj)
        self.assertNotCalled(chat_post_message_, get_topic_)

    @mock.patch('tasks.snacks.snacks.reactions_add')
    @mock.patch.object(Snacks, 'is_valid_message')
    @mock.patch('tasks.snacks.snacks.get_topic')
    @mock.patch('tasks.snacks.snacks.chat_post_message')
    @mock.patch('tasks.snacks.snacks.call_service')
    def test_on_message__who(self, call_service_, chat_post_message_,
                             get_topic_, is_valid_message_, reactions_add_):
        call_service_.return_value = 'Definitely a.'
        is_valid_message_.return_value = True

        obj = {'channel': 'C123', 'text': '<@U3ULC7DBP> who foo'}
        snacks = self.create_snacks(users=['a', 'b'])
        response = snacks._on_message_internal(date=DATE_10260604, obj=obj)
        self.assertEqual(response, Response())

        call_service_.assert_called_once_with('circus', 'who', (['a', 'b'], ))
        chat_post_message_.assert_called_once_with('C123', 'Definitely a.')
        is_valid_message_.assert_called_once_with(obj)
        self.assertNotCalled(reactions_add_, get_topic_)

    def test_setup(self):
        snacks = self.create_snacks()
        actual = snacks._setup_internal(date=DATE_10260602)
        expected = Response(thread_=[Thread(target='refresh')])
        self.assertEqual(actual, expected)

    @mock.patch('tasks.snacks.snacks.get_users')
    @mock.patch('tasks.snacks.snacks.get_messages')
    @mock.patch('tasks.snacks.snacks.get_cfd')
    def test_refresh(self, get_cfd_, get_messages_, get_users_):
        get_cfd_.return_value = CFD
        get_messages_.return_value = {'U123': ['foo'], 'U456': ['bar', 'baz']}
        get_users_.return_value = ['a', 'b', 'c']

        snacks = self.create_snacks()
        actual = snacks.refresh()
        expected = Response()
        self.assertEqual(actual, expected)

        self.assertEqual(snacks.cfds, {'U123': CFD, 'U456': CFD, 'all': CFD})
        self.assertEqual(snacks.users, ['a', 'b', 'c'])

        get_cfd_.assert_has_calls([
            mock.call(4, ['foo']),
            mock.call(4, ['bar', 'baz']),
            mock.call(4, ['foo', 'bar', 'baz'])
        ])
        get_messages_.assert_called_once_with()
        get_users_.assert_called_once_with()

    def test_is_valid_message__false(self):
        obj = {'channel': 'C123', 'text': 'foo', 'ts': '1'}

        snacks = self.create_snacks()
        actual = snacks.is_valid_message(obj)
        expected = False
        self.assertEqual(actual, expected)

    def test_is_valid_message__true(self):
        obj = {'channel': 'C9YE6NQG0', 'text': '<@U3ULC7DBP> foo', 'ts': '1'}

        snacks = self.create_snacks()
        actual = snacks.is_valid_message(obj)
        expected = True
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
