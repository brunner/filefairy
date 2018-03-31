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
from plugins.snacks.snacks_plugin import _chooselist, _snacklist, SnacksPlugin  # noqa
from utils.json.json_util import dumps  # noqa

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

    def create_plugin(self, data):
        self.init_mocks(data)
        plugin = SnacksPlugin()

        self.mock_open.assert_called_once_with(DATA, 'r')
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

        self.reset_mocks()
        self.init_mocks(data)

        return plugin

    @mock.patch.object(SnacksPlugin, '_fnames')
    @mock.patch.object(SnacksPlugin, 'corpus')
    def test_setup(self, mock_corpus, mock_fnames):
        fnames = [os.path.join(_root, 'corpus', 'C1234.txt')]
        mock_fnames.return_value = fnames

        read = {'members': MEMBERS_THEN}
        plugin = self.create_plugin(read)
        plugin._setup(date=THEN)

        mock_corpus.assert_not_called()
        mock_fnames.assert_called_once_with()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_called_once_with(4, *fnames)
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()
        self.assertEqual(plugin.day, 26)

    @mock.patch('plugins.snacks.snacks_plugin.discuss')
    def test_on_message__with_discuss_text(self, mock_discuss):
        mock_discuss.return_value = 'response'

        obj = {
            'channel': 'G3SUFLMK4',
            'text': '<@U3ULC7DBP> discuss topic',
            'ts': '1000.789',
            'user': 'U1234',
        }
        read = {'members': MEMBERS_THEN}
        plugin = self.create_plugin(read)
        ret = plugin._on_message_internal(obj=obj)
        self.assertTrue(ret)

        write = {'members': MEMBERS_NOW}
        mock_discuss.assert_called_once_with('topic', {}, 4, 6, 30)
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_called_once_with('G3SUFLMK4', 'response')
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(SnacksPlugin, '_snacks')
    def test_on_message__with_snack_me_text(self, mock_snacks):
        mock_snacks.return_value = ['a', 'b']

        obj = {
            'channel': 'G3SUFLMK4',
            'text': '<@U3ULC7DBP> snack me',
            'ts': '1000.789',
            'user': 'U1234',
        }
        read = {'members': MEMBERS_THEN}
        plugin = self.create_plugin(read)
        ret = plugin._on_message_internal(obj=obj)
        self.assertTrue(ret)

        write = {'members': MEMBERS_NOW}
        mock_snacks.assert_called_once_with()
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        calls = [
            mock.call('a', 'G3SUFLMK4', '1000.789'),
            mock.call('b', 'G3SUFLMK4', '1000.789')
        ]
        self.mock_reactions.assert_has_calls(calls)

    @mock.patch('plugins.snacks.snacks_plugin.random.choice')
    def test_on_message__with_choose_text(self, mock_random):
        mock_random.side_effect = ['{}. Did you even need to ask?', 'a']

        obj = {
            'channel': 'G3SUFLMK4',
            'text': '<@U3ULC7DBP> choose a or b',
            'ts': '1000.789',
            'user': 'U1234',
        }
        read = {'members': MEMBERS_THEN}
        plugin = self.create_plugin(read)
        ret = plugin._on_message_internal(obj=obj)
        self.assertTrue(ret)

        write = {'members': MEMBERS_NOW}
        calls = [mock.call(_chooselist), mock.call(('a', 'b'))]
        mock_random.assert_has_calls(calls)
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_called_once_with('G3SUFLMK4',
                                               'A. Did you even need to ask?')
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_on_message__with_invalid_channel(self):
        obj = {
            'channel': 'C1234',
            'text': '<@U3ULC7DBP> discuss topic',
            'ts': '1000.789',
            'user': 'U1234',
        }
        read = {'members': MEMBERS_THEN}
        plugin = self.create_plugin(read)
        ret = plugin._on_message_internal(obj=obj)
        self.assertFalse(ret)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_on_message__with_invalid_text(self):
        obj = {
            'channel': 'G3SUFLMK4',
            'text': 'invalid',
            'ts': '1000.789',
            'user': 'U1234',
        }
        read = {'members': MEMBERS_THEN}
        plugin = self.create_plugin(read)
        ret = plugin._on_message_internal(obj=obj)
        self.assertFalse(ret)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_on_message__with_invalid_timestamp(self):
        obj = {
            'channel': 'G3SUFLMK4',
            'text': '<@U3ULC7DBP> discuss topic',
            'ts': '105.456',
            'user': 'U1234',
        }
        read = {'members': MEMBERS_THEN}
        plugin = self.create_plugin(read)
        ret = plugin._on_message_internal(obj=obj)
        self.assertFalse(ret)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(SnacksPlugin, '_fnames')
    @mock.patch.object(SnacksPlugin, 'corpus')
    def test_run__with_different_day(self, mock_corpus, mock_fnames):
        fnames = [os.path.join(_root, 'corpus', 'C1234.txt')]
        mock_fnames.return_value = fnames

        read = {'members': MEMBERS_THEN}
        plugin = self.create_plugin(read)
        plugin._setup(date=THEN)

        mock_corpus.reset_mock()
        mock_fnames.reset_mock()
        self.reset_mocks()

        plugin._run_internal(date=NOW)

        mock_corpus.assert_called_once_with()
        mock_fnames.assert_called_once_with()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_called_once_with(4, *fnames)
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()
        self.assertEqual(plugin.day, 27)

    @mock.patch.object(SnacksPlugin, '_fnames')
    @mock.patch.object(SnacksPlugin, 'corpus')
    def test_run__with_same_day(self, mock_corpus, mock_fnames):
        fnames = [os.path.join(_root, 'corpus', 'C1234.txt')]
        mock_fnames.return_value = fnames

        read = {'members': MEMBERS_THEN}
        plugin = self.create_plugin(read)
        plugin._setup(date=THEN)

        mock_corpus.reset_mock()
        mock_fnames.reset_mock()
        self.reset_mocks()

        plugin._run_internal(date=THEN)

        mock_corpus.assert_not_called()
        mock_fnames.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()
        self.assertEqual(plugin.day, 26)

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
    def test_members(self, mock_users):
        mock_users.return_value = {
            'ok': True,
            'members': [{
                'id': 'U1234',
                'name': 'user'
            }]
        }

        actual = SnacksPlugin._members()
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
    @mock.patch.object(SnacksPlugin, '_members')
    @mock.patch('plugins.snacks.snacks_plugin.channels_list')
    def test_corpus(self, mock_channels, mock_members, mock_open):
        mock_channels.return_value = {
            'ok': True,
            'channels': [{
                'id': 'C1234'
            }]
        }
        mock_members.return_value = {}
        mo = mock.mock_open(read_data='')
        mock_handle = mo()
        mock_open.side_effect = [mo.return_value]

        read = {'members': MEMBERS_THEN}
        plugin = self.create_plugin(read)
        plugin.corpus()

        mock_channels.assert_called_once_with()
        mock_members.assert_called_once_with()
        mock_open.assert_called_once_with(
            os.path.join(_root, 'corpus', 'C1234.txt'), 'w')
        mock_handle.write.assert_called_once_with(COLLECT)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_called_once_with('C1234', {})
        self.mock_reactions.assert_not_called()


if __name__ == '__main__':
    unittest.main()
