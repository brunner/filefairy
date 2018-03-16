#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mock
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(_path)
_root = re.sub(r'/plugins/recap', '', _path)
sys.path.append(_root)
from plugins.recap.recap_plugin import RecapPlugin  # noqa
from utils.jinja2.jinja2_util import env  # noqa
from utils.test.test_util import main, TestUtil  # noqa
from utils.unicode.unicode_util import strip_accents  # noqa

_data = RecapPlugin._data()

_before = """20220101 <a href="../teams/team_31.html">Team X</a> or <a href="../players/player_00000.html">David Player</a> did something.
"""

_injuries = """20220101 <a href="../teams/team_31.html">Team X</a>: LF <a href="../players/player_00000.html">David Player</a> was injured while A.  The Diagnosis: B.
20220101  <a href="../teams/team_32.html">Team Y</a>: SS <a href="../players/player_00001.html">Jesús Player</a> was injured while C.  The Diagnosis: D.
"""

_news = """20220101 <a href="../teams/team_33.html">Team Z</a>: <a href="../players/player_00002.html">Mike Player</a> goes 5-5 against the <a href="../teams/team_31.html">Team X</a>, with 2 2B, 2 RBI and 2 R.
"""

_transactions = """20220101 <a href="../teams/team_32.html">Team Y</a>: Signed <a href="../players/player_00003.html">Kyle Player</a> to a minor league contract with a signing bonus of $1,000,000.
"""

_after = """20220101 <a href="../teams/team_31.html">Team Z</a> or <a href="../players/player_000003.html">Kyle Player</a> did something.
"""


class RecapPluginTest(TestUtil):
    @mock.patch('plugins.recap.recap_plugin.codecs.open')
    def test_content__empty_split(self, mock_open):
        data = _before + _injuries + _after
        mo = mock.mock_open(read_data=data)
        mock_open.side_effect = [mo.return_value]
        actual = RecapPlugin._content('foo.txt', '')
        self.assertEqual(actual, strip_accents(data))
        mock_open.assert_called_once_with(
            'foo.txt', 'r', encoding='utf-8', errors='replace')

    @mock.patch('plugins.recap.recap_plugin.codecs.open')
    def test_content__with_split(self, mock_open):
        data = _before + _injuries + _after
        mo = mock.mock_open(read_data=data)
        mock_open.side_effect = [mo.return_value]
        actual = RecapPlugin._content('foo.txt', strip_accents(_injuries))
        self.assertEqual(actual, _after)
        mock_open.assert_called_once_with(
            'foo.txt', 'r', encoding='utf-8', errors='replace')

    @mock.patch('plugins.recap.recap_plugin.codecs.open')
    def test_content__without_split(self, mock_open):
        data = _before + _injuries
        mo = mock.mock_open(read_data=data)
        mock_open.side_effect = [mo.return_value]
        actual = RecapPlugin._content('foo.txt', strip_accents(_injuries))
        self.assertEqual(actual, strip_accents(data))
        mock_open.assert_called_once_with(
            'foo.txt', 'r', encoding='utf-8', errors='replace')

    @mock.patch('plugins.recap.recap_plugin.os.path.isfile')
    @mock.patch('plugins.recap.recap_plugin.hash_file')
    @mock.patch.object(RecapPlugin, '_content')
    def test_update__empty_data(self, mock_content, mock_hash, mock_isfile):
        mock_content.return_value = 'newcontent'
        mock_hash.return_value = 'newhash'
        mock_isfile.return_value = True
        plugin = RecapPlugin(e=env())
        plugin.data['injuries'] = {'hash': '', 'content': ''}
        plugin._update('injuries', 'foo.txt')
        actual = plugin.data['injuries']
        expected = {'hash': 'newhash', 'content': 'newcontent'}
        self.assertEqual(actual, expected)
        mock_content.assert_called_once_with('foo.txt', '')

    @mock.patch('plugins.recap.recap_plugin.os.path.isfile')
    @mock.patch('plugins.recap.recap_plugin.hash_file')
    @mock.patch.object(RecapPlugin, '_content')
    def test_update__new_hash(self, mock_content, mock_hash, mock_isfile):
        mock_content.return_value = 'newcontent'
        mock_hash.return_value = 'newhash'
        mock_isfile.return_value = True
        plugin = RecapPlugin(e=env())
        plugin.data['injuries'] = {'hash': 'oldhash', 'content': 'oldcontent'}
        plugin._update('injuries', 'foo.txt')
        actual = plugin.data['injuries']
        expected = {'hash': 'newhash', 'content': 'newcontent'}
        self.assertEqual(actual, expected)
        mock_content.assert_called_once_with('foo.txt', 'oldcontent')

    @mock.patch('plugins.recap.recap_plugin.os.path.isfile')
    @mock.patch('plugins.recap.recap_plugin.hash_file')
    @mock.patch.object(RecapPlugin, '_content')
    def test_update__old_hash(self, mock_content, mock_hash, mock_isfile):
        mock_content.return_value = 'newcontent'
        mock_hash.return_value = 'oldhash'
        mock_isfile.return_value = True
        plugin = RecapPlugin(e=env())
        plugin.data['injuries'] = {'hash': 'oldhash', 'content': 'oldcontent'}
        plugin._update('injuries', 'foo.txt')
        actual = plugin.data['injuries']
        expected = {'hash': 'oldhash', 'content': 'oldcontent'}
        self.assertEqual(actual, expected)
        mock_content.assert_not_called()

    @mock.patch.object(RecapPlugin, '_update')
    def test_run__without_change(self, mock_update):
        data = {
            'injuries': {
                'hash': '1ab',
                'content': ''
            },
            'news': {
                'hash': '2cd',
                'content': ''
            },
            'transactions': {
                'hash': '3ef',
                'content': ''
            }
        }
        original = self.write(_data, data)
        plugin = RecapPlugin(e=env())
        ret = plugin._run()
        self.assertFalse(ret)
        actual = self.write(_data, original)
        self.assertEqual(actual, data)

    @mock.patch.object(RecapPlugin, '_update')
    def test_run__with_injuries_change(self, mock_update):
        injuries = strip_accents(_injuries)
        data = {
            'injuries': {
                'hash': '1ab',
                'content': ''
            },
            'news': {
                'hash': '2cd',
                'content': ''
            },
            'transactions': {
                'hash': '3ef',
                'content': ''
            }
        }
        original = self.write(_data, data)
        plugin = RecapPlugin(e=env())

        def update_injuries(key, fname):
            if key == 'injuries':
                plugin.data['injuries'] = {'hash': '4gh', 'content': injuries}

        mock_update.side_effect = update_injuries

        ret = plugin._run()
        self.assertTrue(ret)
        actual = self.write(_data, original)
        expected = {
            'injuries': {
                'hash': '4gh',
                'content': injuries
            },
            'news': {
                'hash': '2cd',
                'content': ''
            },
            'transactions': {
                'hash': '3ef',
                'content': ''
            }
        }
        self.assertEqual(actual, expected)

    @mock.patch.object(RecapPlugin, '_update')
    def test_run__with_news_change(self, mock_update):
        news = strip_accents(_news)
        data = {
            'injuries': {
                'hash': '1ab',
                'content': ''
            },
            'news': {
                'hash': '2cd',
                'content': ''
            },
            'transactions': {
                'hash': '3ef',
                'content': ''
            }
        }
        original = self.write(_data, data)
        plugin = RecapPlugin(e=env())

        def update_news(key, fname):
            if key == 'news':
                plugin.data['news'] = {'hash': '4gh', 'content': news}

        mock_update.side_effect = update_news

        ret = plugin._run()
        self.assertTrue(ret)
        actual = self.write(_data, original)
        expected = {
            'injuries': {
                'hash': '1ab',
                'content': ''
            },
            'news': {
                'hash': '4gh',
                'content': news
            },
            'transactions': {
                'hash': '3ef',
                'content': ''
            }
        }
        self.assertEqual(actual, expected)

    @mock.patch.object(RecapPlugin, '_update')
    def test_run__with_transactions_change(self, mock_update):
        transactions = strip_accents(_transactions)
        data = {
            'injuries': {
                'hash': '1ab',
                'content': ''
            },
            'news': {
                'hash': '2cd',
                'content': ''
            },
            'transactions': {
                'hash': '3ef',
                'content': ''
            }
        }
        original = self.write(_data, data)
        plugin = RecapPlugin(e=env())

        def update_transactions(key, fname):
            if key == 'transactions':
                plugin.data['transactions'] = {
                    'hash': '4gh',
                    'content': transactions
                }

        mock_update.side_effect = update_transactions

        ret = plugin._run()
        self.assertTrue(ret)
        actual = self.write(_data, original)
        expected = {
            'injuries': {
                'hash': '1ab',
                'content': ''
            },
            'news': {
                'hash': '2cd',
                'content': ''
            },
            'transactions': {
                'hash': '4gh',
                'content': transactions
            }
        }
        self.assertEqual(actual, expected)


if __name__ in ['__main__', 'plugins.recap.recap_plugin_test']:
    _main = __name__ == '__main__'
    _pkg = 'plugins.recap'
    _pth = 'plugins/recap'
    main(RecapPluginTest, RecapPlugin, _pkg, _pth, _main)
