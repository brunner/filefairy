#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import mock
import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(_path)
_root = re.sub(r'/plugins/snacks', '', _path)
sys.path.append(_root)
from plugins.snacks.snacks_plugin import SnacksPlugin  # noqa
from plugins.snacks.snacks_plugin import _chooselist  # noqa
from plugins.snacks.snacks_plugin import _snacklist  # noqa
from utils.json.json_util import dumps  # noqa
from value.notify.notify_value import NotifyValue  # noqa
from value.response.response_value import ResponseValue  # noqa

COLLECT = 'collect'
DATA = SnacksPlugin._data()
MEMBERS_THEN = {'U1234': {'latest': '100.123'}}
MEMBERS_NOW = {'U1234': {'latest': '1000.789'}}
NOW = datetime.datetime(1985, 10, 27, 0, 0, 0)
THEN = datetime.datetime(1985, 10, 26, 0, 2, 30)


class SnacksPluginTest(unittest.TestCase):
    def setUp(self):
        patch_open = mock.patch(
            'apis.serializable.serializable_api.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

        patch_cfd = mock.patch('plugins.snacks.snacks_plugin.cfd')
        self.addCleanup(patch_cfd.stop)
        self.mock_cfd = patch_cfd.start()

        patch_chat = mock.patch(
            'plugins.snacks.snacks_plugin.chat_post_message')
        self.addCleanup(patch_chat.stop)
        self.mock_chat = patch_chat.start()

        patch_collect = mock.patch('plugins.snacks.snacks_plugin.collect')
        self.addCleanup(patch_collect.stop)
        self.mock_collect = patch_collect.start()

        patch_reactions = mock.patch(
            'plugins.snacks.snacks_plugin.reactions_add')
        self.addCleanup(patch_reactions.stop)
        self.mock_reactions = patch_reactions.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]
        self.mock_collect.return_value = COLLECT

    def reset_mocks(self):
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()
        self.mock_cfd.reset_mock()
        self.mock_chat.reset_mock()
        self.mock_collect.reset_mock()
        self.mock_reactions.reset_mock()

    def create_plugin(self, data, names=None):
        self.init_mocks(data)
        plugin = SnacksPlugin()
        plugin.loaded = True

        self.mock_open.assert_called_once_with(DATA, 'r')
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

        self.reset_mocks()
        self.init_mocks(data)

        if names:
            plugin.names = names

        return plugin

    @mock.patch('plugins.snacks.snacks_plugin.threading.Thread')
    @mock.patch.object(SnacksPlugin, '_load')
    def test_notify__with_day(self, mock_load, mock_thread):
        read = {'members': MEMBERS_THEN}
        plugin = self.create_plugin(read)
        plugin._setup(date=THEN)

        mock_load.reset_mock()
        mock_thread.reset_mock()
        self.reset_mocks()

        value = plugin._notify_internal(notify=NotifyValue.FAIRYLAB_DAY)
        self.assertFalse(value)

        mock_thread.assert_called_once_with(target=mock_load)
        mock_thread.return_value.start.assert_called_once_with()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch('plugins.snacks.snacks_plugin.threading.Thread')
    @mock.patch.object(SnacksPlugin, '_load')
    def test_notify__with_other(self, mock_load, mock_thread):
        read = {'members': MEMBERS_THEN}
        plugin = self.create_plugin(read)
        plugin._setup(date=THEN)

        mock_load.reset_mock()
        mock_thread.reset_mock()
        self.reset_mocks()

        value = plugin._notify_internal(notify=NotifyValue.OTHER)
        self.assertFalse(value)

        mock_thread.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch('plugins.snacks.snacks_plugin.random.choice')
    def test_on_message__with_choose_text(self, mock_random):
        mock_random.side_effect = ['{}. Did you even need to ask?', 'a']

        obj = {
            'channel': 'C9YE6NQG0',
            'text': '<@U3ULC7DBP> choose a or b',
            'ts': '1000.789',
            'user': 'U1234',
        }
        read = {'members': MEMBERS_THEN}
        plugin = self.create_plugin(read)
        response = plugin._on_message_internal(obj=obj)
        self.assertEqual(response, ResponseValue(notify=[NotifyValue.BASE]))

        write = {'members': MEMBERS_NOW}
        calls = [mock.call(_chooselist), mock.call(['a', 'b'])]
        mock_random.assert_has_calls(calls)
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_called_once_with('C9YE6NQG0',
                                               'A. Did you even need to ask?')
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch('plugins.snacks.snacks_plugin.discuss')
    def test_on_message__with_discuss_text(self, mock_discuss):
        mock_discuss.return_value = 'response'

        obj = {
            'channel': 'C9YE6NQG0',
            'text': '<@U3ULC7DBP> discuss topic',
            'ts': '1000.789',
            'user': 'U1234',
        }
        read = {'members': MEMBERS_THEN}
        plugin = self.create_plugin(read)
        response = plugin._on_message_internal(obj=obj)
        self.assertEqual(response, ResponseValue(notify=[NotifyValue.BASE]))

        write = {'members': MEMBERS_NOW}
        mock_discuss.assert_called_once_with('topic', {}, 4, 8, 30)
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_called_once_with('C9YE6NQG0', 'response')
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch('plugins.snacks.snacks_plugin.channels_kick')
    def test_on_message__with_kick_text(self, mock_kick):
        obj = {
            'channel': 'C9YE6NQG0',
            'text': '<@U3ULC7DBP> kick <@U5678>',
            'ts': '1000.789',
            'user': 'U1234',
        }
        read = {'members': MEMBERS_THEN}
        plugin = self.create_plugin(read, {'U5678': 'user'})
        response = plugin._on_message_internal(obj=obj)
        self.assertEqual(response, ResponseValue(notify=[NotifyValue.BASE]))

        write = {'members': MEMBERS_NOW}
        mock_kick.assert_called_once_with('C9YE6NQG0', 'U5678')
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_on_message__with_say_text(self):
        obj = {
            'channel': 'C9YE6NQG0',
            'text': '<@U3ULC7DBP> say topic',
            'ts': '1000.789',
            'user': 'U1234',
        }
        read = {'members': MEMBERS_THEN}
        plugin = self.create_plugin(read)
        response = plugin._on_message_internal(obj=obj)
        self.assertEqual(response, ResponseValue(notify=[NotifyValue.BASE]))

        write = {'members': MEMBERS_NOW}
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_called_once_with('C9YE6NQG0', 'topic')
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(SnacksPlugin, '_snacks')
    def test_on_message__with_snack_me_text(self, mock_snacks):
        mock_snacks.return_value = ['a', 'b']

        obj = {
            'channel': 'C9YE6NQG0',
            'text': '<@U3ULC7DBP> snack me',
            'ts': '1000.789',
            'user': 'U1234',
        }
        read = {'members': MEMBERS_THEN}
        plugin = self.create_plugin(read)
        response = plugin._on_message_internal(obj=obj)
        self.assertEqual(response, ResponseValue(notify=[NotifyValue.BASE]))

        write = {'members': MEMBERS_NOW}
        mock_snacks.assert_called_once_with()
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        calls = [
            mock.call('a', 'C9YE6NQG0', '1000.789'),
            mock.call('b', 'C9YE6NQG0', '1000.789')
        ]
        self.mock_reactions.assert_has_calls(calls)

    def test_on_message__with_invalid_channel(self):
        obj = {
            'channel': 'C1234',
            'text': '<@U3ULC7DBP> discuss topic',
            'ts': '1000.789',
            'user': 'U1234',
        }
        read = {'members': MEMBERS_THEN}
        plugin = self.create_plugin(read)
        response = plugin._on_message_internal(obj=obj)
        self.assertEqual(response, ResponseValue())

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
        read = {'members': MEMBERS_THEN}
        plugin = self.create_plugin(read)
        response = plugin._on_message_internal(obj=obj)
        self.assertEqual(response, ResponseValue())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_on_message__with_invalid_timestamp(self):
        obj = {
            'channel': 'C9YE6NQG0',
            'text': '<@U3ULC7DBP> discuss topic',
            'ts': '105.456',
            'user': 'U1234',
        }
        read = {'members': MEMBERS_THEN}
        plugin = self.create_plugin(read)
        response = plugin._on_message_internal(obj=obj)
        self.assertEqual(response, ResponseValue())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_run(self):
        read = {'members': MEMBERS_THEN}
        plugin = self.create_plugin(read)
        response = plugin._run_internal()
        self.assertEqual(response, ResponseValue())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch('plugins.download.download_plugin.threading.Thread')
    @mock.patch.object(SnacksPlugin, '_load_internal')
    def test_setup(self, mock_load_internal, mock_thread):
        read = {'members': MEMBERS_THEN}
        plugin = self.create_plugin(read)
        plugin._setup_internal(date=THEN)

        mock_thread.assert_called_once_with(target=mock_load_internal)
        mock_thread.return_value.start.assert_called_once_with()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_shadow(self):
        read = {'members': MEMBERS_THEN}
        plugin = self.create_plugin(read)
        value = plugin._shadow_internal()
        self.assertEqual(value, {})

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch('plugins.snacks.snacks_plugin.os.listdir')
    def test_fnames(self, mock_listdir):
        mock_listdir.return_value = ['C1234.txt', 'C5678.txt']

        actual = SnacksPlugin._fnames()
        expected = [
            os.path.join(_root, 'corpus', 'C1234.txt'),
            os.path.join(_root, 'corpus', 'C5678.txt')
        ]
        self.assertEqual(actual, expected)

    @mock.patch('plugins.snacks.snacks_plugin.users_list')
    def test_names(self, mock_users):
        mock_users.return_value = {
            'ok': True,
            'members': [{
                'id': 'U1234',
                'name': 'user'
            }]
        }

        actual = SnacksPlugin._names()
        expected = {'U1234': 'user'}
        self.assertEqual(actual, expected)

    @mock.patch('plugins.snacks.snacks_plugin.random.choice')
    def test_snacks__with_different_values(self, mock_random):
        mock_random.side_effect = ['a', 'b']

        actual = SnacksPlugin._snacks()
        expected = ['a', 'b']
        self.assertEqual(actual, expected)

        calls = [mock.call(_snacklist), mock.call(_snacklist)]
        mock_random.assert_has_calls(calls)

    @mock.patch('plugins.snacks.snacks_plugin.random.choice')
    def test_snacks__with_same_value(self, mock_random):
        mock_random.side_effect = ['a', 'a']

        actual = SnacksPlugin._snacks()
        expected = ['a', 'star']
        self.assertEqual(actual, expected)

        calls = [mock.call(_snacklist), mock.call(_snacklist)]
        mock_random.assert_has_calls(calls)

    @mock.patch('plugins.snacks.snacks_plugin.open', create=True)
    @mock.patch('plugins.snacks.snacks_plugin.channels_list')
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

        read = {'members': MEMBERS_THEN}
        plugin = self.create_plugin(read, names={'U1234': 'user'})
        plugin._corpus()

        mock_channels.assert_called_once_with()
        mock_open.assert_called_once_with(
            os.path.join(_root, 'corpus', 'C1234.txt'), 'w')
        mock_handle.write.assert_called_once_with(COLLECT)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_called_once_with('C1234', {'U1234': 'user'})
        self.mock_reactions.assert_not_called()

    @mock.patch.object(SnacksPlugin, '_load_internal')
    @mock.patch.object(SnacksPlugin, '_corpus')
    def test_load(self, mock_corpus, mock_load_internal):
        read = {'members': MEMBERS_THEN}
        plugin = self.create_plugin(read, names={'U1234': 'user'})
        plugin.loaded = False
        plugin._load()

        mock_corpus.assert_called_once_with()
        mock_load_internal.assert_called_once_with()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()
        self.assertFalse(plugin.loaded)

    @mock.patch.object(SnacksPlugin, '_names')
    @mock.patch.object(SnacksPlugin, '_fnames')
    def test_load_internal(self, mock_fnames, mock_names):
        fnames = [os.path.join(_root, 'corpus', 'C1234.txt')]
        mock_fnames.return_value = fnames

        read = {'members': MEMBERS_THEN}
        plugin = self.create_plugin(read, names={'U1234': 'user'})
        plugin.loaded = False
        plugin._load_internal()

        mock_fnames.assert_called_once_with()
        mock_names.assert_called_once_with()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_called_once_with(4, *fnames)
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()
        self.assertTrue(plugin.loaded)


if __name__ == '__main__':
    unittest.main()
