#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(_path)
_root = re.sub(r'/tasks/snacks', '', _path)
sys.path.append(_root)
from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa
from data.thread_.thread_ import Thread  # noqa
from tasks.snacks.snacks import Snacks  # noqa
from tasks.snacks.snacks import _chooselist  # noqa
from tasks.snacks.snacks import _snacklist  # noqa
from tasks.snacks.snacks import _wafflelist  # noqa
from common.elements.elements import card  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import table  # noqa
from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.jinja2_.jinja2_ import env  # noqa
from common.json_.json_ import dumps  # noqa
from common.test.test import Test  # noqa
from common.test.test import main  # noqa

_collect = {'U1234': ['reply.', 'foo.', 'bar.', 'baz.']}
_cols = [col(clazz='text-center w-75p'), col(), col(clazz='text-right')]
_env = env()
_members_new = {'U1234': '1000.789', 'U5678': '100.456'}
_members_old = {'U1234': '100.123', 'U5678': '100.456'}
_members_bot = {
    'U1234': '100.123',
    'U5678': '100.456',
    'U3ULC7DBP': '1000.789'
}
_now = datetime_datetime_pst(1985, 10, 27, 0, 0, 0)
_now_encoded = '1985-10-27T00:00:00-07:00'
_then = datetime_datetime_pst(1985, 10, 26, 0, 2, 30)
_then_encoded = '1985-10-26T00:02:30-07:00'


class SnacksTest(Test):
    def setUp(self):
        patch_open = mock.patch(
            'api.serializable.serializable.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

        patch_cfd = mock.patch('tasks.snacks.snacks.cfd')
        self.addCleanup(patch_cfd.stop)
        self.mock_cfd = patch_cfd.start()

        patch_chat = mock.patch('tasks.snacks.snacks.chat_post_message')
        self.addCleanup(patch_chat.stop)
        self.mock_chat = patch_chat.start()

        patch_collect = mock.patch('tasks.snacks.snacks.collect')
        self.addCleanup(patch_collect.stop)
        self.mock_collect = patch_collect.start()

        patch_reactions = mock.patch('tasks.snacks.snacks.reactions_add')
        self.addCleanup(patch_reactions.stop)
        self.mock_reactions = patch_reactions.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]
        self.mock_collect.return_value = _collect

    def reset_mocks(self):
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()
        self.mock_cfd.reset_mock()
        self.mock_chat.reset_mock()
        self.mock_collect.reset_mock()
        self.mock_reactions.reset_mock()

    def create_snacks(self, cfds=None, names=None):
        self.init_mocks({})
        snacks = Snacks(date=_now, e=_env)
        snacks.loaded = True

        self.mock_open.assert_called_once_with(Snacks._data(), 'r')
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

        self.reset_mocks()
        self.init_mocks({})

        if cfds:
            snacks.cfds = cfds
        if names:
            snacks.names = names

        return snacks

    def test_notify__with_day(self):
        snacks = self.create_snacks()
        snacks._setup(date=_then)

        self.reset_mocks()

        response = snacks._notify_internal(notify=Notify.FILEFAIRY_DAY)
        self.assertEqual(response, Response(thread_=[Thread(target='_load')]))

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_notify__with_other(self):
        snacks = self.create_snacks()
        snacks._setup(date=_then)

        self.reset_mocks()

        response = snacks._notify_internal(notify=Notify.OTHER)
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch('tasks.snacks.snacks.random.choice')
    def test_on_message__with_choose_text_multiple(self, mock_random):
        mock_random.side_effect = ['{}. Did you even need to ask?', 'a']

        obj = {
            'channel': 'C9YE6NQG0',
            'text': '<@U3ULC7DBP> choose a or b',
            'ts': '1000.789',
            'user': 'U1234',
        }
        snacks = self.create_snacks()
        response = snacks._on_message_internal(date=_now, obj=obj)
        self.assertEqual(response, Response())

        calls = [mock.call(_chooselist + _wafflelist), mock.call(['a', 'b'])]
        mock_random.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_called_once_with('C9YE6NQG0',
                                               'A. Did you even need to ask?')
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch('tasks.snacks.snacks.random.choice')
    def test_on_message__with_choose_text_single(self, mock_random):
        obj = {
            'channel': 'C9YE6NQG0',
            'text': '<@U3ULC7DBP> choose a',
            'ts': '1000.789',
            'user': 'U1234',
        }
        snacks = self.create_snacks()
        response = snacks._on_message_internal(date=_now, obj=obj)
        self.assertEqual(response, Response())

        mock_random.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch('tasks.snacks.snacks.discuss')
    def test_on_message__with_discuss_text_empty(self, mock_discuss):
        mock_discuss.return_value = ''

        obj = {
            'channel': 'C9YE6NQG0',
            'text': '<@U3ULC7DBP> discuss topic',
            'ts': '1000.789',
            'user': 'U1234',
        }
        snacks = self.create_snacks()
        response = snacks._on_message_internal(date=_now, obj=obj)
        self.assertEqual(response, Response())

        mock_discuss.assert_called_once_with('topic', {}, 4, 8, 30)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_called_once_with(
            'C9YE6NQG0', 'I don\'t know anything about topic.')
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch('tasks.snacks.snacks.discuss')
    def test_on_message__with_discuss_text_valid(self, mock_discuss):
        mock_discuss.return_value = 'response'

        obj = {
            'channel': 'C9YE6NQG0',
            'text': '<@U3ULC7DBP> discuss topic',
            'ts': '1000.789',
            'user': 'U1234',
        }
        snacks = self.create_snacks()
        response = snacks._on_message_internal(date=_now, obj=obj)
        self.assertEqual(response, Response())

        mock_discuss.assert_called_once_with('topic', {}, 4, 8, 30)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_called_once_with('C9YE6NQG0', 'response')
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch('tasks.snacks.snacks.imitate')
    def test_on_message__with_imitate_text_empty(self, mock_imitate):
        mock_imitate.return_value = ''

        obj = {
            'channel': 'C9YE6NQG0',
            'text': '<@U3ULC7DBP> imitate <@U5678>',
            'ts': '1000.789',
            'user': 'U1234',
        }
        cfds = {'U5678': {}}
        names = ['user']
        snacks = self.create_snacks(cfds=cfds, names=names)
        response = snacks._on_message_internal(date=_now, obj=obj)
        self.assertEqual(response, Response())

        mock_imitate.assert_called_once_with({}, 4, 8, 30)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_called_once_with(
            'C9YE6NQG0', '<@U5678> doesn\'t know anything.')
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch('tasks.snacks.snacks.imitate')
    def test_on_message__with_imitate_text_valid(self, mock_imitate):
        mock_imitate.return_value = 'response'

        obj = {
            'channel': 'C9YE6NQG0',
            'text': '<@U3ULC7DBP> imitate <@U5678>',
            'ts': '1000.789',
            'user': 'U1234',
        }
        cfds = {'U5678': {}}
        names = ['user']
        snacks = self.create_snacks(cfds=cfds, names=names)
        response = snacks._on_message_internal(date=_now, obj=obj)
        self.assertEqual(response, Response())

        mock_imitate.assert_called_once_with({}, 4, 8, 30)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_called_once_with('C9YE6NQG0', 'response')
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch('tasks.snacks.snacks.discuss')
    def test_on_message__with_imitate_topic_text_empty(self, mock_discuss):
        mock_discuss.return_value = ''

        obj = {
            'channel': 'C9YE6NQG0',
            'text': '<@U3ULC7DBP> imitate <@U5678> topic',
            'ts': '1000.789',
            'user': 'U1234',
        }
        cfds = {'U5678': {}}
        names = ['user']
        snacks = self.create_snacks(cfds=cfds, names=names)
        response = snacks._on_message_internal(date=_now, obj=obj)
        self.assertEqual(response, Response())

        mock_discuss.assert_called_once_with('topic', {}, 4, 8, 30)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_called_once_with(
            'C9YE6NQG0', '<@U5678> doesn\'t know anything about topic.')
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch('tasks.snacks.snacks.discuss')
    def test_on_message__with_imitate_topic_text_user(self, mock_discuss):
        mock_discuss.return_value = 'response'

        obj = {
            'channel': 'C9YE6NQG0',
            'text': '<@U3ULC7DBP> imitate <@U5678> <@U1234>',
            'ts': '1000.789',
            'user': 'U1234',
        }
        cfds = {'U5678': {}}
        names = ['user']
        snacks = self.create_snacks(cfds=cfds, names=names)
        response = snacks._on_message_internal(date=_now, obj=obj)
        self.assertEqual(response, Response())

        mock_discuss.assert_called_once_with('<@U1234>', {}, 4, 8, 30)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_called_once_with('C9YE6NQG0', 'response')
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch('tasks.snacks.snacks.discuss')
    def test_on_message__with_imitate_topic_text_valid(self, mock_discuss):
        mock_discuss.return_value = 'response'

        obj = {
            'channel': 'C9YE6NQG0',
            'text': '<@U3ULC7DBP> imitate <@U5678> topic',
            'ts': '1000.789',
            'user': 'U1234',
        }
        cfds = {'U5678': {}}
        names = ['user']
        snacks = self.create_snacks(cfds=cfds, names=names)
        response = snacks._on_message_internal(date=_now, obj=obj)
        self.assertEqual(response, Response())

        mock_discuss.assert_called_once_with('topic', {}, 4, 8, 30)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_called_once_with('C9YE6NQG0', 'response')
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_on_message__with_say_text(self):
        obj = {
            'channel': 'C9YE6NQG0',
            'text': '<@U3ULC7DBP> say topic',
            'ts': '1000.789',
            'user': 'U1234',
        }
        snacks = self.create_snacks()
        response = snacks._on_message_internal(date=_now, obj=obj)
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_called_once_with('C9YE6NQG0', 'topic')
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Snacks, '_snacks')
    @mock.patch('tasks.snacks.snacks.pins_add')
    def test_on_message__with_snack_me_text_pin(self, mock_pins,
                                                mock_snacks):
        mock_snacks.return_value = ['a', 'star', 'b']

        obj = {
            'channel': 'C9YE6NQG0',
            'text': '<@U3ULC7DBP> snack me',
            'ts': '1000.789',
            'user': 'U3ULC7DBP',
        }
        snacks = self.create_snacks()
        response = snacks._on_message_internal(date=_now, obj=obj)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        mock_pins.assert_called_once_with('C9YE6NQG0', '1000.789')
        mock_snacks.assert_called_once_with()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        calls = [
            mock.call('a', 'C9YE6NQG0', '1000.789'),
            mock.call('star', 'C9YE6NQG0', '1000.789'),
            mock.call('b', 'C9YE6NQG0', '1000.789')
        ]
        self.mock_reactions.assert_has_calls(calls)

    @mock.patch.object(Snacks, '_snacks')
    @mock.patch('tasks.snacks.snacks.pins_add')
    def test_on_message__with_snack_me_text_star(self, mock_pins,
                                                 mock_snacks):
        mock_snacks.return_value = ['a', 'star', 'b']

        obj = {
            'channel': 'C9YE6NQG0',
            'text': '<@U3ULC7DBP> snack me',
            'ts': '1000.789',
            'user': 'U1234',
        }
        snacks = self.create_snacks()
        response = snacks._on_message_internal(date=_now, obj=obj)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        mock_pins.assert_not_called()
        mock_snacks.assert_called_once_with()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        calls = [
            mock.call('a', 'C9YE6NQG0', '1000.789'),
            mock.call('star', 'C9YE6NQG0', '1000.789'),
            mock.call('b', 'C9YE6NQG0', '1000.789')
        ]
        self.mock_reactions.assert_has_calls(calls)

    @mock.patch('tasks.snacks.snacks.random.choice')
    def test_on_message__with_who_text(self, mock_random):
        mock_random.side_effect = ['{}. Did you even need to ask?', 'a']

        obj = {
            'channel': 'C9YE6NQG0',
            'text': '<@U3ULC7DBP> who deserves a star?',
            'ts': '1000.789',
            'user': 'U1234',
        }
        cfds = {'U5678': {}}
        names = ['a', 'b']
        snacks = self.create_snacks(cfds=cfds, names=names)
        response = snacks._on_message_internal(date=_now, obj=obj)
        self.assertEqual(response, Response())

        calls = [mock.call(_chooselist), mock.call(['a', 'b'])]
        mock_random.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_called_once_with('C9YE6NQG0',
                                               'a. Did you even need to ask?')
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_on_message__with_invalid_channel(self):
        obj = {
            'channel': 'C1234',
            'text': '<@U3ULC7DBP> discuss topic',
            'ts': '1000.789',
            'user': 'U1234',
        }
        snacks = self.create_snacks()
        response = snacks._on_message_internal(date=_now, obj=obj)
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_on_message__with_invalid_text(self):
        obj = {
            'channel': 'C9YE6NQG0',
            'text': 'invalid',
            'ts': '1000.789',
            'user': 'U1234',
        }
        snacks = self.create_snacks()
        response = snacks._on_message_internal(date=_now, obj=obj)
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_render(self):
        snacks = self.create_snacks()
        response = snacks._render_internal(date=_now)
        self.assertEqual(response, [])

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_run(self):
        snacks = self.create_snacks()
        response = snacks._run_internal(date=_then)
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_setup(self):
        snacks = self.create_snacks()
        response = snacks._setup_internal(date=_then)
        self.assertEqual(response,
                         Response(thread_=[Thread(target='_load_internal')]))

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_shadow(self):
        snacks = self.create_snacks()
        value = snacks._shadow_internal()
        self.assertEqual(value, [])

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch('tasks.snacks.snacks.os.listdir')
    def test_fnames(self, mock_listdir):
        mock_listdir.return_value = ['C1234.txt', 'C5678.txt']

        actual = Snacks._fnames()
        expected = [
            os.path.join(_root, 'resource/corpus', 'C1234.txt'),
            os.path.join(_root, 'resource/corpus', 'C5678.txt')
        ]
        self.assertEqual(actual, expected)

    @mock.patch('tasks.snacks.snacks.users_list')
    def test_names(self, mock_users):
        mock_users.return_value = {
            'ok':
            True,
            'members': [
                {
                    'deleted': False,
                    'id': 'U1234',
                    'name': 'foo',
                    'profile': {
                        'display_name': 'foo1'
                    }
                },
                {
                    'deleted': True,
                    'id': 'U5678',
                    'name': 'bar',
                    'profile': {
                        'display_name': 'bar1'
                    }
                },
                {
                    'deleted': False,
                    'id': 'U9012',
                    'name': 'baz',
                    'profile': {
                        'display_name': ''
                    }
                },
            ]
        }

        actual = Snacks._names()
        expected = ['baz', 'foo1']
        self.assertEqual(actual, expected)

    @mock.patch('tasks.snacks.snacks.random.choice')
    def test_snacks__with_all_different_values(self, mock_random):
        mock_random.side_effect = ['a', 'b', 'c']

        actual = Snacks._snacks()
        expected = ['a', 'b', 'c']
        self.assertEqual(actual, expected)

        calls = [mock.call(_snacklist), mock.call(_snacklist)]
        mock_random.assert_has_calls(calls)

    @mock.patch('tasks.snacks.snacks.random.choice')
    def test_snacks__with_same_same_different(self, mock_random):
        mock_random.side_effect = ['a', 'a', 'b']

        actual = Snacks._snacks()
        expected = ['a', 'star', 'b']
        self.assertEqual(actual, expected)

        calls = [mock.call(_snacklist), mock.call(_snacklist)]
        mock_random.assert_has_calls(calls)

    @mock.patch('tasks.snacks.snacks.random.choice')
    def test_snacks__with_different_same_same(self, mock_random):
        mock_random.side_effect = ['a', 'b', 'b']

        actual = Snacks._snacks()
        expected = ['b', 'star', 'a']
        self.assertEqual(actual, expected)

        calls = [mock.call(_snacklist), mock.call(_snacklist)]
        mock_random.assert_has_calls(calls)

    @mock.patch('tasks.snacks.snacks.random.choice')
    def test_snacks__with_same_different_same(self, mock_random):
        mock_random.side_effect = ['a', 'b', 'a']

        actual = Snacks._snacks()
        expected = ['a', 'star', 'b']
        self.assertEqual(actual, expected)

        calls = [mock.call(_snacklist), mock.call(_snacklist)]
        mock_random.assert_has_calls(calls)

    @mock.patch('tasks.snacks.snacks.random.choice')
    def test_snacks__with_all_same_values(self, mock_random):
        mock_random.side_effect = ['a', 'a', 'a']

        actual = Snacks._snacks()
        expected = ['a', 'star', 'trophy']
        self.assertEqual(actual, expected)

        calls = [mock.call(_snacklist), mock.call(_snacklist)]
        mock_random.assert_has_calls(calls)

    @mock.patch('tasks.snacks.snacks.open', create=True)
    @mock.patch('tasks.snacks.snacks.channels_list')
    def test_corpus(self, mock_channels, mock_open):
        mock_channels.return_value = {
            'ok': True,
            'channels': [{
                'id': 'C1234'
            }]
        }
        mo = mock.mock_open(read_data='')
        mock_handle = mo()
        mock_open.side_effect = [mo.return_value]

        names = {'U1234': 'foo', 'U5678': 'bar'}
        snacks = self.create_snacks(names=names)
        snacks._corpus()

        mock_channels.assert_called_once_with()
        mock_open.assert_called_once_with(
            os.path.join(_root, 'resource/corpus', 'U1234.txt'), 'w')
        mock_handle.write.assert_called_once_with('reply.\nfoo.\nbar.\nbaz.')
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_called_once_with('C1234')
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Snacks, '_load_internal')
    @mock.patch.object(Snacks, '_corpus')
    def test_load(self, mock_corpus, mock_load_internal):
        mock_load_internal.return_value = Response()

        names = {'U1234': 'foo', 'U5678': 'bar'}
        snacks = self.create_snacks(names=names)
        snacks.loaded = False
        response = snacks._load()
        self.assertEqual(response, Response())

        mock_corpus.assert_called_once_with()
        mock_load_internal.assert_called_once_with()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()
        self.assertFalse(snacks.loaded)

    @mock.patch.object(Snacks, '_names')
    @mock.patch.object(Snacks, '_fnames')
    def test_load_internal(self, mock_fnames, mock_names):
        fpath = os.path.join(_root, 'resource/corpus', '{}.txt')
        fnames = [fpath.format(u) for u in ['U1234', 'U5678']]
        mock_fnames.return_value = fnames

        names = ['foo', 'bar']
        snacks = self.create_snacks(names=names)
        snacks.loaded = False
        response = snacks._load_internal()
        self.assertEqual(response, Response())

        mock_fnames.assert_called_once_with()
        mock_names.assert_called_once_with()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        calls = [
            mock.call(4, *[fnames[0]]),
            mock.call(4, *[fnames[1]]),
            mock.call(4, *fnames)
        ]
        self.mock_cfd.assert_has_calls(calls)
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()
        self.assertTrue(snacks.loaded)


if __name__ in ['__main__', 'tasks.snacks.snacks_test']:
    _main = __name__ == '__main__'
    _pkg = 'tasks.snacks'
    _pth = 'tasks/snacks'
    main(SnacksTest, Snacks, _pkg, _pth, {}, _main, date=_now, e=_env)
