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
from common.jinja2_.jinja2_ import env  # noqa
from common.json_.json_ import dumps  # noqa
from common.nltk_.nltk_ import get_cfd  # noqa
from common.test.test import Test  # noqa
from tasks.snacks.snacks import Snacks  # noqa
from types_.notify.notify import Notify  # noqa
from types_.response.response import Response  # noqa
from types_.thread_.thread_ import Thread  # noqa

ENV = env()

DATE_10260602 = datetime_datetime_pst(1985, 10, 26, 6, 2, 30)
DATE_10260604 = datetime_datetime_pst(1985, 10, 26, 6, 4)

CFD = get_cfd(2, ['The quick brown fox.', 'Jumps over the lazy dog.'])


class SnacksTest(Test):
    def setUp(self):
        patch_open = mock.patch(
            'api.serializable.serializable.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]

    def reset_mocks(self):
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()

    def create_snacks(self, cfds=None, users=None):
        self.init_mocks({})
        snacks = Snacks(date=DATE_10260602, e=ENV)

        self.mock_open.assert_called_once_with(Snacks._data(), 'r')
        self.mock_handle.write.assert_not_called()

        self.reset_mocks()
        self.init_mocks({})

        if cfds:
            snacks.cfds = cfds
        if users:
            snacks.users = users

        return snacks

    def test_notify__filefairy_day(self):
        snacks = self.create_snacks()
        actual = snacks._notify_internal(notify=Notify.FILEFAIRY_DAY)
        expected = Response(thread_=[Thread(target='_refresh')])
        self.assertEqual(actual, expected)

        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    def test_notify__other(self):
        snacks = self.create_snacks()
        actual = snacks._notify_internal(notify=Notify.OTHER)
        expected = Response()
        self.assertEqual(actual, expected)

        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    @mock.patch.object(Snacks, '_valid')
    @mock.patch('tasks.snacks.snacks.get_topic')
    @mock.patch('tasks.snacks.snacks.reactions_add')
    @mock.patch('tasks.snacks.snacks.chat_post_message')
    @mock.patch('tasks.snacks.snacks.call_service')
    def test_on_message__invalid(self, mock_call, mock_chat, mock_reactions,
                                 mock_topic, mock_valid):
        mock_valid.return_value = False

        obj = {'channel': 'C123'}
        snacks = self.create_snacks()
        response = snacks._on_message_internal(date=DATE_10260604, obj=obj)
        self.assertEqual(response, Response())

        mock_valid.assert_called_once_with(obj)
        self.assertNotCalled(mock_call, mock_chat, mock_reactions, mock_topic,
                             self.mock_open, self.mock_handle.write)

    @mock.patch.object(Snacks, '_valid')
    @mock.patch('tasks.snacks.snacks.get_topic')
    @mock.patch('tasks.snacks.snacks.reactions_add')
    @mock.patch('tasks.snacks.snacks.chat_post_message')
    @mock.patch('tasks.snacks.snacks.call_service')
    def test_on_message__choose(self, mock_call, mock_chat, mock_reactions,
                                mock_topic, mock_valid):
        mock_call.return_value = 'Definitely a.'
        mock_valid.return_value = True

        obj = {'channel': 'C123', 'text': '<@U3ULC7DBP> choose a or b'}
        snacks = self.create_snacks()
        response = snacks._on_message_internal(date=DATE_10260604, obj=obj)
        self.assertEqual(response, Response())

        mock_call.assert_called_once_with('circus', 'choose', (['a', 'b'], ))
        mock_chat.assert_called_once_with('C123', 'Definitely a.')
        mock_valid.assert_called_once_with(obj)
        self.assertNotCalled(mock_reactions, mock_topic, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Snacks, '_valid')
    @mock.patch('tasks.snacks.snacks.get_topic')
    @mock.patch('tasks.snacks.snacks.reactions_add')
    @mock.patch('tasks.snacks.snacks.chat_post_message')
    @mock.patch('tasks.snacks.snacks.call_service')
    def test_on_message__discuss_known(self, mock_call, mock_chat,
                                       mock_reactions, mock_topic, mock_valid):
        mock_call.return_value = 'A b c.'
        mock_valid.return_value = True

        obj = {'channel': 'C123', 'text': '<@U3ULC7DBP> discuss a'}
        snacks = self.create_snacks(cfds={'all': CFD})
        response = snacks._on_message_internal(date=DATE_10260604, obj=obj)
        self.assertEqual(response, Response())

        mock_call.assert_called_once_with('circus', 'discuss',
                                          ('a', CFD, 4, 8, 30))
        mock_chat.assert_called_once_with('C123', 'A b c.')
        mock_valid.assert_called_once_with(obj)
        self.assertNotCalled(mock_reactions, mock_topic, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Snacks, '_valid')
    @mock.patch('tasks.snacks.snacks.get_topic')
    @mock.patch('tasks.snacks.snacks.reactions_add')
    @mock.patch('tasks.snacks.snacks.chat_post_message')
    @mock.patch('tasks.snacks.snacks.call_service')
    def test_on_message__discuss_unknown(self, mock_call, mock_chat,
                                         mock_reactions, mock_topic,
                                         mock_valid):
        mock_call.return_value = None
        mock_valid.return_value = True

        obj = {'channel': 'C123', 'text': '<@U3ULC7DBP> discuss a'}
        snacks = self.create_snacks(cfds={'all': CFD})
        response = snacks._on_message_internal(date=DATE_10260604, obj=obj)
        self.assertEqual(response, Response())

        mock_call.assert_called_once_with('circus', 'discuss',
                                          ('a', CFD, 4, 8, 30))
        mock_chat.assert_called_once_with('C123',
                                          'I don\'t know anything about a.')
        mock_valid.assert_called_once_with(obj)
        self.assertNotCalled(mock_reactions, mock_topic, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Snacks, '_valid')
    @mock.patch('tasks.snacks.snacks.get_topic')
    @mock.patch('tasks.snacks.snacks.reactions_add')
    @mock.patch('tasks.snacks.snacks.chat_post_message')
    @mock.patch('tasks.snacks.snacks.call_service')
    def test_on_message__imitate_known(self, mock_call, mock_chat,
                                       mock_reactions, mock_topic, mock_valid):
        mock_call.return_value = 'A b c.'
        mock_topic.return_value = 'a'
        mock_valid.return_value = True

        obj = {'channel': 'C123', 'text': '<@U3ULC7DBP> imitate <@U123>'}
        snacks = self.create_snacks(cfds={'U123': CFD})
        response = snacks._on_message_internal(date=DATE_10260604, obj=obj)
        self.assertEqual(response, Response())

        mock_call.assert_called_once_with('circus', 'discuss',
                                          ('a', CFD, 4, 8, 30))
        mock_chat.assert_called_once_with('C123', 'A b c.')
        mock_topic.assert_called_once_with(CFD)
        mock_valid.assert_called_once_with(obj)
        self.assertNotCalled(mock_reactions, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Snacks, '_valid')
    @mock.patch('tasks.snacks.snacks.get_topic')
    @mock.patch('tasks.snacks.snacks.reactions_add')
    @mock.patch('tasks.snacks.snacks.chat_post_message')
    @mock.patch('tasks.snacks.snacks.call_service')
    def test_on_message__imitate_unknown(self, mock_call, mock_chat,
                                         mock_reactions, mock_topic,
                                         mock_valid):
        mock_call.return_value = None
        mock_topic.return_value = None
        mock_valid.return_value = True

        obj = {'channel': 'C123', 'text': '<@U3ULC7DBP> imitate <@U123>'}
        snacks = self.create_snacks()
        response = snacks._on_message_internal(date=DATE_10260604, obj=obj)
        self.assertEqual(response, Response())

        mock_call.assert_called_once_with('circus', 'discuss',
                                          (None, {}, 4, 8, 30))
        mock_chat.assert_called_once_with('C123',
                                          '<@U123> doesn\'t know anything.')
        mock_topic.assert_called_once_with({})
        mock_valid.assert_called_once_with(obj)
        self.assertNotCalled(mock_reactions, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Snacks, '_valid')
    @mock.patch('tasks.snacks.snacks.get_topic')
    @mock.patch('tasks.snacks.snacks.reactions_add')
    @mock.patch('tasks.snacks.snacks.chat_post_message')
    @mock.patch('tasks.snacks.snacks.call_service')
    def test_on_message__imitate_topic_known(self, mock_call, mock_chat,
                                             mock_reactions, mock_topic,
                                             mock_valid):
        mock_call.return_value = 'A b c.'
        mock_valid.return_value = True

        obj = {'channel': 'C123', 'text': '<@U3ULC7DBP> imitate <@U123> a'}
        snacks = self.create_snacks(cfds={'U123': CFD})
        response = snacks._on_message_internal(date=DATE_10260604, obj=obj)
        self.assertEqual(response, Response())

        mock_call.assert_called_once_with('circus', 'discuss',
                                          ('a', CFD, 4, 8, 30))
        mock_chat.assert_called_once_with('C123', 'A b c.')
        mock_valid.assert_called_once_with(obj)
        self.assertNotCalled(mock_reactions, mock_topic, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Snacks, '_valid')
    @mock.patch('tasks.snacks.snacks.get_topic')
    @mock.patch('tasks.snacks.snacks.reactions_add')
    @mock.patch('tasks.snacks.snacks.chat_post_message')
    @mock.patch('tasks.snacks.snacks.call_service')
    def test_on_message__imitate_topic_unknown(self, mock_call, mock_chat,
                                               mock_reactions, mock_topic,
                                               mock_valid):
        mock_call.return_value = None
        mock_valid.return_value = True

        obj = {'channel': 'C123', 'text': '<@U3ULC7DBP> imitate <@U123> a'}
        snacks = self.create_snacks()
        response = snacks._on_message_internal(date=DATE_10260604, obj=obj)
        self.assertEqual(response, Response())

        mock_call.assert_called_once_with('circus', 'discuss',
                                          ('a', {}, 4, 8, 30))
        mock_chat.assert_called_once_with(
            'C123', '<@U123> doesn\'t know anything about a.')
        mock_valid.assert_called_once_with(obj)
        self.assertNotCalled(mock_reactions, mock_topic, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Snacks, '_valid')
    @mock.patch('tasks.snacks.snacks.get_topic')
    @mock.patch('tasks.snacks.snacks.reactions_add')
    @mock.patch('tasks.snacks.snacks.chat_post_message')
    @mock.patch('tasks.snacks.snacks.call_service')
    def test_on_message__say(self, mock_call, mock_chat, mock_reactions,
                             mock_topic, mock_valid):
        mock_valid.return_value = True

        obj = {'channel': 'C123', 'text': '<@U3ULC7DBP> say a'}
        snacks = self.create_snacks()
        response = snacks._on_message_internal(date=DATE_10260604, obj=obj)
        self.assertEqual(response, Response())

        mock_chat.assert_called_once_with('C123', 'a')
        mock_valid.assert_called_once_with(obj)
        self.assertNotCalled(mock_call, mock_reactions, mock_topic,
                             self.mock_open, self.mock_handle.write)

    @mock.patch.object(Snacks, '_valid')
    @mock.patch('tasks.snacks.snacks.get_topic')
    @mock.patch('tasks.snacks.snacks.reactions_add')
    @mock.patch('tasks.snacks.snacks.chat_post_message')
    @mock.patch('tasks.snacks.snacks.call_service')
    def test_on_message__snack_me(self, mock_call, mock_chat, mock_reactions,
                                  mock_topic, mock_valid):
        s = ['amphora', 'apple', 'avocado']
        mock_call.return_value = s
        mock_valid.return_value = True

        obj = {'channel': 'C123', 'text': '<@U3ULC7DBP> snack me', 'ts': '1'}
        snacks = self.create_snacks()
        response = snacks._on_message_internal(date=DATE_10260604, obj=obj)
        self.assertEqual(response, Response())

        mock_call.assert_called_once_with('bread', 'snack_me', ())
        mock_reactions.assert_has_calls([mock.call(x, 'C123', '1') for x in s])
        mock_valid.assert_called_once_with(obj)
        self.assertNotCalled(mock_chat, mock_topic, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Snacks, '_valid')
    @mock.patch('tasks.snacks.snacks.get_topic')
    @mock.patch('tasks.snacks.snacks.reactions_add')
    @mock.patch('tasks.snacks.snacks.chat_post_message')
    @mock.patch('tasks.snacks.snacks.call_service')
    def test_on_message__who(self, mock_call, mock_chat, mock_reactions,
                             mock_topic, mock_valid):
        mock_call.return_value = 'Definitely a.'
        mock_valid.return_value = True

        obj = {'channel': 'C123', 'text': '<@U3ULC7DBP> who foo'}
        snacks = self.create_snacks(users=['a', 'b'])
        response = snacks._on_message_internal(date=DATE_10260604, obj=obj)
        self.assertEqual(response, Response())

        mock_call.assert_called_once_with('circus', 'who', (['a', 'b'], ))
        mock_chat.assert_called_once_with('C123', 'Definitely a.')
        mock_valid.assert_called_once_with(obj)
        self.assertNotCalled(mock_reactions, mock_topic, self.mock_open,
                             self.mock_handle.write)

    def test_setup(self):
        snacks = self.create_snacks()
        actual = snacks._setup_internal(date=DATE_10260602)
        expected = Response(thread_=[Thread(target='_refresh')])
        self.assertEqual(actual, expected)

        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    @mock.patch('tasks.snacks.snacks.get_users')
    @mock.patch('tasks.snacks.snacks.get_messages')
    @mock.patch('tasks.snacks.snacks.get_cfd')
    def test_refresh(self, mock_cfd, mock_messages, mock_users):
        mock_cfd.return_value = CFD
        mock_messages.return_value = {'U123': ['foo'], 'U456': ['bar', 'baz']}
        mock_users.return_value = ['a', 'b', 'c']

        snacks = self.create_snacks()
        actual = snacks._refresh()
        expected = Response()
        self.assertEqual(actual, expected)

        self.assertEqual(snacks.cfds, {'U123': CFD, 'U456': CFD, 'all': CFD})
        self.assertEqual(snacks.users, ['a', 'b', 'c'])

        mock_cfd.assert_has_calls([
            mock.call(4, ['foo']),
            mock.call(4, ['bar', 'baz']),
            mock.call(4, ['foo', 'bar', 'baz'])
        ])
        mock_messages.assert_called_once_with()
        mock_users.assert_called_once_with()
        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    def test_valid__false(self):
        obj = {'channel': 'C123', 'text': 'foo', 'ts': '1'}

        snacks = self.create_snacks()
        actual = snacks._valid(obj)
        expected = False
        self.assertEqual(actual, expected)

    def test_valid__true(self):
        obj = {'channel': 'C9YE6NQG0', 'text': '<@U3ULC7DBP> foo', 'ts': '1'}

        snacks = self.create_snacks()
        actual = snacks._valid(obj)
        expected = True
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
