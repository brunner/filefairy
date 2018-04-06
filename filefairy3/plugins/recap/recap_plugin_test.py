#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import mock
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(_path)
_root = re.sub(r'/plugins/recap', '', _path)
sys.path.append(_root)
from enums.activity.activity_enum import ActivityEnum  # noqa
from plugins.recap.recap_plugin import RecapPlugin  # noqa
from utils.component.component_util import table  # noqa
from utils.jinja2.jinja2_util import env  # noqa
from utils.json.json_util import dumps  # noqa
from utils.test.test_util import main, TestUtil  # noqa
from utils.unicode.unicode_util import deunicode  # noqa

_leagues = os.path.join(_root, 'file/news/txt/leagues')
_injuries = os.path.join(_leagues, 'league_100_injuries.txt')
_news = os.path.join(_leagues, 'league_100_news.txt')
_transactions = os.path.join(_leagues, 'league_100_transactions.txt')

DATA = RecapPlugin._data()
NOW = datetime.datetime(1985, 10, 26, 0, 2, 30)
INJ_AFTER = '20220817\t<a href=\"../teams/team_47.html\">Minnesota Twins</a>: 1B <a href=\"../players/player_34032.html\">Nick Castellanos</a> was injured while running the bases.  The Diagnosis: sprained ankle. This is a day-to-day injury expected to last 5 days.'
INJ_BEFORE = '20220815\t<a href=\"../teams/team_44.html\">Los Angeles Angels</a>: CF <a href=\"../players/player_0.html\">Alex Aristy</a> was injured while running the bases.  The Diagnosis: knee inflammation. He\'s expected to miss about 3 weeks.'
INJ_CONTENT = '20220817\t<a href=\"../teams/team_57.html\">Tampa Bay Rays</a>: <a href=\"../players/player_1.html\">Zack Weiss</a> diagnosed with a strained hamstring, will miss 4 weeks.\n20220817\t<a href=\"../teams/team_39.html\">Colorado Rockies</a>: RF <a href=\"../players/player_24198.html\">Eddie Hoffman</a> was injured being hit by a pitch.  The Diagnosis: bruised knee. This is a day-to-day injury expected to last 5 days.'
INJ_HASH = '965572a66c'
INJ_UPDATE = {'content': INJ_CONTENT, 'hash': INJ_HASH}
INJ_CALL = mock.call('injuries', _injuries)
INJ_TABLE = table(
    clazz='border mt-3',
    cols=[''],
    head=['Wednesday, August 17th, 2022'],
    body=[[
        'Minnesota Twins: 1B <a href=\"/StatsLab/reports/news/html/players/player_34032.html\">Nick Castellanos</a> was injured while running the bases.  The Diagnosis: sprained ankle. This is a day-to-day injury expected to last 5 days.'
    ]])
NEWS_AFTER = '20220818\t<a href=\"../teams/team_41.html\">Miami Marlins</a>: <a href=\"../players/player_131.html\">Jake Ehret</a> got suspended 3 games after ejection following a brawl.'
NEWS_BEFORE = '20220815\t<a href=\"../teams/team_57.html\">Tampa Bay Rays</a>: <a href=\"../players/player_27.html\">A.J. Reed</a> got suspended 4 games after ejection following arguing a strike call.'
NEWS_CONTENT = '20220818\t<a href=\"../teams/team_42.html\">Houston Astros</a>: <a href=\"../players/player_39044.html\">Mark Appel</a> pitches a 2-hit shutout against the <a href=\"../teams/team_44.html\">Los Angeles Angels</a> with 8 strikeouts and 0 BB allowed!\n20220818\t<a href=\"../teams/team_39.html\">Colorado Rockies</a>: <a href=\"../players/player_30965.html\">Spencer Taylor</a> got suspended 3 games after ejection following a brawl.'
NEWS_HASH = '2b9934d013'
NEWS_UPDATE = {'content': NEWS_CONTENT, 'hash': NEWS_HASH}
NEWS_CALL = mock.call('news', _news)
NEWS_TABLE = table(
    clazz='border mt-3',
    cols=[''],
    head=['Thursday, August 18th, 2022'],
    body=[[
        'Miami Marlins: <a href=\"/StatsLab/reports/news/html/players/player_131.html\">Jake Ehret</a> got suspended 3 games after ejection following a brawl.'
    ]])
TRANS_AFTER = '20220815\t<a href=\"../teams/team_33.html\">Baltimore Orioles</a>: Placed C <a href=\"../players/player_31093.html\">Salvador Perez</a> on waivers.\n'
TRANS_BEFORE = '20220815\t<a href=\"../teams/team_33.html\">Baltimore Orioles</a>: Placed 2B <a href=\"../players/player_292.html\">Austin Slater</a> on the 7-day disabled list, retroactive to 08/12/2022.\n'
TRANS_CONTENT = '20220815\t<a href=\"../teams/team_33.html\">Baltimore Orioles</a>: Placed C <a href=\"../players/player_1439.html\">Evan Skoug</a> on the active roster.\n\n20220815\t<a href=\"../teams/team_33.html\">Baltimore Orioles</a>: Activated C <a href=\"../players/player_1439.html\">Evan Skoug</a> from the disabled list.\n'
TRANS_HASH = 'a17f312e8e'
TRANS_UPDATE = {'content': TRANS_CONTENT, 'hash': TRANS_HASH}
TRANS_CALL = mock.call('transactions', _transactions)
TRANS_TABLE = table(
    clazz='border mt-3',
    cols=[''],
    head=['Monday, August 15th, 2022'],
    body=[[
        'Baltimore Orioles: Placed C <a href=\"/StatsLab/reports/news/html/players/player_31093.html\">Salvador Perez</a> on waivers.'
    ]])
TABLE_MAP = {
    'injuries': [INJ_TABLE],
    'news': [NEWS_TABLE],
    'transactions': [TRANS_TABLE]
}
UPDATE_MAP = {
    'injuries': INJ_UPDATE,
    'news': NEWS_UPDATE,
    'transactions': TRANS_UPDATE
}
AFTER_MAP = {
    'injuries': {
        'content': INJ_AFTER,
        'hash': INJ_HASH
    },
    'news': {
        'content': NEWS_AFTER,
        'hash': NEWS_HASH
    },
    'transactions': {
        'content': TRANS_AFTER,
        'hash': TRANS_HASH
    }
}
LINE = '<a href=\"../teams/team_47.html\">Minnesota Twins</a>: 1B <a href=\"../players/player_34032.html\">Nick Castellanos</a> was injured while running the bases.  The Diagnosis: sprained ankle. This is a day-to-day injury expected to last 5 days.'
LINE_STRIPPED = 'Minnesota Twins: 1B <a href=\"../players/player_34032.html\">Nick Castellanos</a> was injured while running the bases.  The Diagnosis: sprained ankle. This is a day-to-day injury expected to last 5 days.'
LINE_REWRITTEN = '<a href=\"../teams/team_47.html\">Minnesota Twins</a>: 1B <a href=\"/StatsLab/reports/news/html/players/player_34032.html\">Nick Castellanos</a> was injured while running the bases.  The Diagnosis: sprained ankle. This is a day-to-day injury expected to last 5 days.'
HOME = {'breadcrumbs': [], 'injuries': [], 'news': [], 'transactions': []}
INDEX = 'html/fairylab/recap/index.html'
BREADCRUMBS = [{
    'href': '/fairylab/',
    'name': 'Home'
}, {
    'href': '',
    'name': 'Recap'
}]


class RecapPluginTest(TestUtil):
    def setUp(self):
        patch_open = mock.patch(
            'apis.serializable.serializable_api.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()
        patch_chat = mock.patch('plugins.recap.recap_plugin.chat_post_message')
        self.addCleanup(patch_chat.stop)
        self.mock_chat = patch_chat.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]

    def reset_mocks(self):
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()
        self.mock_chat.reset_mock()

    def create_plugin(self, data):
        self.init_mocks(data)
        plugin = RecapPlugin(e=env())

        self.mock_open.assert_called_once_with(DATA, 'r')
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.assertEqual(plugin.data, data)

        self.reset_mocks()
        self.init_mocks(data)

        return plugin

    def test_notify(self):
        keys = ['injuries', 'news', 'transactions']
        read = {k: {'content': '', 'hash': ''} for k in keys}
        plugin = self.create_plugin(read)
        plugin._notify_internal()

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

    def test_on_message(self):
        keys = ['injuries', 'news', 'transactions']
        read = {k: {'content': '', 'hash': ''} for k in keys}
        plugin = self.create_plugin(read)
        ret = plugin._on_message_internal()
        self.assertEqual(ret, ActivityEnum.NONE)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

    @mock.patch.object(RecapPlugin, '_update')
    @mock.patch.object(RecapPlugin, '_render')
    def test_run__with_valid_input(self, mock_render, mock_update):
        keys = ['injuries', 'news', 'transactions']
        read = {k: {'content': '', 'hash': ''} for k in keys}
        plugin = self.create_plugin(read)

        def fake_update(*args, **kwargs):
            key = args[0]
            plugin.data[key] = UPDATE_MAP.get(key)

        mock_update.side_effect = fake_update

        ret = plugin._run_internal(date=NOW)
        self.assertEqual(ret, ActivityEnum.BASE)

        write = UPDATE_MAP
        mock_render.assert_called_once_with(date=NOW)
        mock_update.assert_has_calls([INJ_CALL, NEWS_CALL, TRANS_CALL])
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_called_once_with(
            'fairylab',
            'League news updated.',
            attachments=plugin._attachments())

    @mock.patch.object(RecapPlugin, '_update')
    @mock.patch.object(RecapPlugin, '_render')
    def test_run__with_no_change(self, mock_render, mock_update):
        keys = ['injuries', 'news', 'transactions']
        read = {k: {'content': '', 'hash': ''} for k in keys}
        plugin = self.create_plugin(read)
        ret = plugin._run_internal(date=NOW)
        self.assertEqual(ret, ActivityEnum.NONE)

        mock_render.assert_not_called()
        mock_update.assert_has_calls([INJ_CALL, NEWS_CALL, TRANS_CALL])
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

    @mock.patch.object(RecapPlugin, '_home')
    def test_render(self, mock_home):
        mock_home.return_value = HOME

        keys = ['injuries', 'news', 'transactions']
        read = {k: {'content': '', 'hash': ''} for k in keys}
        plugin = self.create_plugin(read)
        ret = plugin._render_internal(date=NOW)
        self.assertEqual(ret, [(INDEX, '', 'recap.html', HOME)])

        mock_home.assert_called_once_with(date=NOW)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

    @mock.patch.object(RecapPlugin, '_update')
    @mock.patch.object(RecapPlugin, '_render')
    def test_setup__with_valid_input(self, mock_render, mock_update):
        keys = ['injuries', 'news', 'transactions']
        read = {k: {'content': '', 'hash': ''} for k in keys}
        plugin = self.create_plugin(read)

        def fake_update(*args, **kwargs):
            key = args[0]
            plugin.data[key] = UPDATE_MAP.get(key)

        mock_update.side_effect = fake_update

        plugin._setup_internal(date=NOW)

        write = UPDATE_MAP
        mock_render.assert_called_once_with(date=NOW)
        mock_update.assert_has_calls([INJ_CALL, NEWS_CALL, TRANS_CALL])
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_not_called()

    @mock.patch.object(RecapPlugin, '_update')
    @mock.patch.object(RecapPlugin, '_render')
    def test_setup__with_no_change(self, mock_render, mock_update):
        keys = ['injuries', 'news', 'transactions']
        read = {k: {'content': '', 'hash': ''} for k in keys}
        plugin = self.create_plugin(read)
        plugin._setup_internal(date=NOW)

        mock_render.assert_called_once_with(date=NOW)
        mock_update.assert_has_calls([INJ_CALL, NEWS_CALL, TRANS_CALL])
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

    @mock.patch('plugins.recap.recap_plugin.codecs.open')
    def test_content__with_injuries(self, mock_open):
        data = '\n'.join([INJ_BEFORE, INJ_CONTENT, INJ_AFTER])
        mo = mock.mock_open(read_data=data)
        mock_open.side_effect = [mo.return_value]

        actual = RecapPlugin._content('injuries.txt', INJ_CONTENT)
        expected = INJ_AFTER.strip()
        self.assertEqual(actual, expected)

        mock_open.assert_called_once_with(
            'injuries.txt', 'r', encoding='utf-8', errors='replace')

    @mock.patch('plugins.recap.recap_plugin.codecs.open')
    def test_content__with_news(self, mock_open):
        data = '\n'.join([NEWS_BEFORE, NEWS_CONTENT, NEWS_AFTER])
        mo = mock.mock_open(read_data=data)
        mock_open.side_effect = [mo.return_value]

        actual = RecapPlugin._content('news.txt', NEWS_CONTENT)
        expected = NEWS_AFTER.strip()
        self.assertEqual(actual, expected)

        mock_open.assert_called_once_with(
            'news.txt', 'r', encoding='utf-8', errors='replace')

    @mock.patch('plugins.recap.recap_plugin.codecs.open')
    def test_content__with_transactions(self, mock_open):
        data = '\n'.join([TRANS_BEFORE, TRANS_CONTENT, TRANS_AFTER])
        mo = mock.mock_open(read_data=data)
        mock_open.side_effect = [mo.return_value]

        actual = RecapPlugin._content('transactions.txt', TRANS_CONTENT)
        expected = TRANS_AFTER.strip()
        self.assertEqual(actual, expected)

        mock_open.assert_called_once_with(
            'transactions.txt', 'r', encoding='utf-8', errors='replace')

    @mock.patch('plugins.recap.recap_plugin.codecs.open')
    def test_content__with_empty_split(self, mock_open):
        data = '\n'.join([INJ_BEFORE, INJ_CONTENT, INJ_AFTER])
        mo = mock.mock_open(read_data=data)
        mock_open.side_effect = [mo.return_value]

        actual = RecapPlugin._content('injuries.txt', '')
        expected = data
        self.assertEqual(actual, expected)

        mock_open.assert_called_once_with(
            'injuries.txt', 'r', encoding='utf-8', errors='replace')

    @mock.patch('plugins.recap.recap_plugin.codecs.open')
    def test_content__with_invalid_split(self, mock_open):
        data = '\n'.join([INJ_BEFORE, INJ_CONTENT, INJ_AFTER])
        mo = mock.mock_open(read_data=data)
        mock_open.side_effect = [mo.return_value]

        actual = RecapPlugin._content('injuries.txt', 'foobar')
        expected = data
        self.assertEqual(actual, expected)

        mock_open.assert_called_once_with(
            'injuries.txt', 'r', encoding='utf-8', errors='replace')

    @mock.patch('plugins.recap.recap_plugin.codecs.open')
    def test_content__with_end_split(self, mock_open):
        data = '\n'.join([INJ_BEFORE, INJ_CONTENT])
        mo = mock.mock_open(read_data=data)
        mock_open.side_effect = [mo.return_value]

        actual = RecapPlugin._content('injuries.txt', INJ_CONTENT)
        expected = INJ_CONTENT
        self.assertEqual(actual, expected)

        mock_open.assert_called_once_with(
            'injuries.txt', 'r', encoding='utf-8', errors='replace')

    def test_strip_teams(self):
        actual = RecapPlugin._strip_teams(LINE)
        expected = LINE_STRIPPED
        self.assertEqual(actual, expected)

    def test_rewrite_players(self):
        actual = RecapPlugin._rewrite_players(LINE)
        expected = LINE_REWRITTEN
        self.assertEqual(actual, expected)

    @mock.patch.object(RecapPlugin, '_tables')
    def test_home(self, mock_tables):

        keys = ['injuries', 'news', 'transactions']
        read = {k: {'content': '', 'hash': ''} for k in keys}
        plugin = self.create_plugin(read)

        def fake_tables(*args, **kwargs):
            key = args[0]
            return TABLE_MAP.get(key)

        mock_tables.side_effect = fake_tables

        ret = plugin._home(date=NOW)
        expected = {
            'breadcrumbs': BREADCRUMBS,
            'injuries': [INJ_TABLE],
            'news': [NEWS_TABLE],
            'transactions': [TRANS_TABLE]
        }
        self.assertEqual(ret, expected)

        mock_tables.assert_has_calls([
            mock.call('injuries'),
            mock.call('news'),
            mock.call('transactions')
        ])
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

    def test_tables__injuries(self):
        keys = ['injuries', 'news', 'transactions']
        read = {k: AFTER_MAP.get(k) for k in keys}
        plugin = self.create_plugin(read)
        actual = plugin._tables('injuries')
        expected = [INJ_TABLE]
        self.assertEqual(actual, expected)

    maxDiff = None
    def test_tables__news(self):
        keys = ['injuries', 'news', 'transactions']
        read = {k: AFTER_MAP.get(k) for k in keys}
        plugin = self.create_plugin(read)
        actual = plugin._tables('news')
        expected = [NEWS_TABLE]
        self.assertEqual(actual, expected)

    def test_tables__transactions(self):
        keys = ['injuries', 'news', 'transactions']
        read = {k: AFTER_MAP.get(k) for k in keys}
        plugin = self.create_plugin(read)
        actual = plugin._tables('transactions')
        expected = [TRANS_TABLE]
        self.assertEqual(actual, expected)

    @mock.patch('plugins.recap.recap_plugin.os.path.isfile')
    @mock.patch('plugins.recap.recap_plugin.hash_file')
    @mock.patch.object(RecapPlugin, '_content')
    def test_update__empty_data(self, mock_content, mock_hash, mock_isfile):
        mock_content.return_value = 'newcontent'
        mock_hash.return_value = 'newhash'
        mock_isfile.return_value = True

        read = {'injuries': {'content': '', 'hash': ''}}
        plugin = self.create_plugin(read)
        plugin._update('injuries', 'injuries.txt')

        mock_content.assert_called_once_with('injuries.txt', '')
        mock_hash.assert_called_once_with('injuries.txt')
        mock_isfile.assert_called_once_with('injuries.txt')
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        data = {'injuries': {'content': 'newcontent', 'hash': 'newhash'}}
        self.assertEqual(plugin.data, data)

    @mock.patch('plugins.recap.recap_plugin.os.path.isfile')
    @mock.patch('plugins.recap.recap_plugin.hash_file')
    @mock.patch.object(RecapPlugin, '_content')
    def test_update__new_hash(self, mock_content, mock_hash, mock_isfile):
        mock_content.return_value = 'newcontent'
        mock_hash.return_value = 'newhash'
        mock_isfile.return_value = True

        read = {'injuries': {'content': 'oldcontent', 'hash': 'oldhash'}}
        plugin = self.create_plugin(read)
        plugin._update('injuries', 'injuries.txt')

        mock_content.assert_called_once_with('injuries.txt', 'oldcontent')
        mock_hash.assert_called_once_with('injuries.txt')
        mock_isfile.assert_called_once_with('injuries.txt')
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        data = {'injuries': {'content': 'newcontent', 'hash': 'newhash'}}
        self.assertEqual(plugin.data, data)

    @mock.patch('plugins.recap.recap_plugin.os.path.isfile')
    @mock.patch('plugins.recap.recap_plugin.hash_file')
    @mock.patch.object(RecapPlugin, '_content')
    def test_update__old_hash(self, mock_content, mock_hash, mock_isfile):
        mock_content.return_value = 'newcontent'
        mock_hash.return_value = 'oldhash'
        mock_isfile.return_value = True

        read = {'injuries': {'content': 'oldcontent', 'hash': 'oldhash'}}
        plugin = self.create_plugin(read)
        plugin._update('injuries', 'injuries.txt')

        mock_content.assert_not_called()
        mock_hash.assert_called_once_with('injuries.txt')
        mock_isfile.assert_called_once_with('injuries.txt')
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.assertEqual(plugin.data, read)


if __name__ in ['__main__', 'plugins.recap.recap_plugin_test']:
    _main = __name__ == '__main__'
    _pkg = 'plugins.recap'
    _pth = 'plugins/recap'
    main(RecapPluginTest, RecapPlugin, _pkg, _pth, {}, _main)
