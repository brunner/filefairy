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
_root = re.sub(r'/plugins/download', '', _path)
sys.path.append(_root)
from enums.activity.activity_enum import ActivityEnum  # noqa
from plugins.download.download_plugin import DownloadPlugin  # noqa
from utils.json.json_util import dumps  # noqa

DATA = DownloadPlugin._data()
INJ_AFTER = '20220817\t<a href=\"../teams/team_47.html\">Minnesota Twins</a>: 1B <a href=\"../players/player_34032.html\">Nick Castellanos</a> was injured while running the bases.  The Diagnosis: sprained ankle. This is a day-to-day injury expected to last 5 days.'
INJ_BEFORE = '20220815\t<a href=\"../teams/team_44.html\">Los Angeles Angels</a>: CF <a href=\"../players/player_0.html\">Alex Aristy</a> was injured while running the bases.  The Diagnosis: knee inflammation. He\'s expected to miss about 3 weeks.'
INJ_CONTENT = '20220817\t<a href=\"../teams/team_57.html\">Tampa Bay Rays</a>: <a href=\"../players/player_1.html\">Zack Weiss</a> diagnosed with a strained hamstring, will miss 4 weeks.\n20220817\t<a href=\"../teams/team_39.html\">Colorado Rockies</a>: RF <a href=\"../players/player_24198.html\">Eddie Hoffman</a> was injured being hit by a pitch.  The Diagnosis: bruised knee. This is a day-to-day injury expected to last 5 days.'
NEWS_AFTER = '20220818\t<a href=\"../teams/team_41.html\">Miami Marlins</a>: <a href=\"../players/player_131.html\">Jake Ehret</a> got suspended 3 games after ejection following a brawl.'
NEWS_BEFORE = '20220815\t<a href=\"../teams/team_57.html\">Tampa Bay Rays</a>: <a href=\"../players/player_27.html\">A.J. Reed</a> got suspended 4 games after ejection following arguing a strike call.'
NEWS_CONTENT = '20220818\t<a href=\"../teams/team_42.html\">Houston Astros</a>: <a href=\"../players/player_39044.html\">Mark Appel</a> pitches a 2-hit shutout against the <a href=\"../teams/team_44.html\">Los Angeles Angels</a> with 8 strikeouts and 0 BB allowed!\n20220818\t<a href=\"../teams/team_39.html\">Colorado Rockies</a>: <a href=\"../players/player_30965.html\">Spencer Taylor</a> got suspended 3 games after ejection following a brawl.'
TRANS_AFTER = '20220815\t<a href=\"../teams/team_33.html\">Baltimore Orioles</a>: Placed C <a href=\"../players/player_31093.html\">Salvador Perez</a> on waivers.\n'
TRANS_BEFORE = '20220815\t<a href=\"../teams/team_33.html\">Baltimore Orioles</a>: Placed 2B <a href=\"../players/player_292.html\">Austin Slater</a> on the 7-day disabled list, retroactive to 08/12/2022.\n'
TRANS_CONTENT = '20220815\t<a href=\"../teams/team_33.html\">Baltimore Orioles</a>: Placed C <a href=\"../players/player_1439.html\">Evan Skoug</a> on the active roster.\n\n20220815\t<a href=\"../teams/team_33.html\">Baltimore Orioles</a>: Activated C <a href=\"../players/player_1439.html\">Evan Skoug</a> from the disabled list.\n'
OLD_HASH = 'oldhash'
NEW_HASH = 'newhash'
THEN = datetime.datetime(1985, 10, 26, 0, 2, 30)


class DownloadPluginTest(unittest.TestCase):
    def setUp(self):
        patch_open = mock.patch(
            'apis.serializable.serializable_api.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]

    def reset_mocks(self):
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()

    def create_plugin(self, data):
        self.init_mocks(data)
        plugin = DownloadPlugin()

        self.mock_open.assert_called_once_with(DATA, 'r')
        self.mock_handle.write.assert_not_called()

        self.reset_mocks()
        self.init_mocks(data)

        return plugin

    @mock.patch('plugins.leaguefile.leaguefile_plugin.threading.Thread')
    @mock.patch.object(DownloadPlugin, '_download')
    def test_notify__with_file(self, mock_download, mock_thread):
        keys = ['injuries', 'news', 'transactions']
        leagues = {key: OLD_HASH for key in keys}
        read = {'downloaded': False, 'leagues': leagues}
        plugin = self.create_plugin(read)
        plugin._notify_internal(activity=ActivityEnum.FILE)

        mock_thread.assert_called_once_with(target=mock_download)
        mock_thread.return_value.start.assert_called_once_with()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch('plugins.leaguefile.leaguefile_plugin.threading.Thread')
    @mock.patch.object(DownloadPlugin, '_download')
    def test_notify__with_none(self, mock_download, mock_thread):
        keys = ['injuries', 'news', 'transactions']
        leagues = {key: OLD_HASH for key in keys}
        read = {'downloaded': False, 'leagues': leagues}
        plugin = self.create_plugin(read)
        plugin._notify_internal(activity=ActivityEnum.NONE)

        mock_thread.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    def test_on_message(self):
        keys = ['injuries', 'news', 'transactions']
        leagues = {key: OLD_HASH for key in keys}
        read = {'downloaded': False, 'leagues': leagues}
        plugin = self.create_plugin(read)
        ret = plugin._on_message_internal()
        self.assertEqual(ret, ActivityEnum.NONE)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    def test_run__with_downloaded_true(self):
        keys = ['injuries', 'news', 'transactions']
        leagues = {key: OLD_HASH for key in keys}
        read = {'downloaded': True, 'leagues': leagues}
        plugin = self.create_plugin(read)
        ret = plugin._run_internal(date=THEN)
        self.assertEqual(ret, ActivityEnum.DOWNLOAD)

        write = {'downloaded': False, 'leagues': leagues}
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    def test_run__with_downloaded_false(self):
        keys = ['injuries', 'news', 'transactions']
        leagues = {key: OLD_HASH for key in keys}
        read = {'downloaded': False, 'leagues': leagues}
        plugin = self.create_plugin(read)
        ret = plugin._run_internal(date=THEN)
        self.assertEqual(ret, ActivityEnum.NONE)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    def test_setup(self):
        keys = ['injuries', 'news', 'transactions']
        leagues = {key: OLD_HASH for key in keys}
        read = {'downloaded': False, 'leagues': leagues}
        plugin = self.create_plugin(read)
        plugin._setup_internal()

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(DownloadPlugin, '_leagues')
    @mock.patch('plugins.download.download_plugin.wget_file')
    def test_download(self, mock_file, mock_leagues):
        keys = ['injuries', 'news', 'transactions']
        leagues = {key: OLD_HASH for key in keys}
        read = {'downloaded': False, 'leagues': leagues}
        plugin = self.create_plugin(read)
        plugin._download()

        write = {'downloaded': True, 'leagues': leagues}
        mock_file.assert_called_once_with()
        mock_leagues.assert_called_once_with()
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch.object(DownloadPlugin, '_leagues_internal')
    @mock.patch('plugins.download.download_plugin.os.path.isfile')
    def test_leagues(self, mock_isfile, mock_leagues):
        mock_isfile.return_value = True

        keys = ['injuries', 'news', 'transactions']
        rleagues = {key: OLD_HASH for key in keys}
        read = {'leagues': rleagues}
        plugin = self.create_plugin(read)

        def fake_leagues(*args, **kwargs):
            key = args[0]
            plugin.data['leagues'][key] = NEW_HASH

        mock_leagues.side_effect = fake_leagues

        plugin._leagues()

        wleagues = {key: NEW_HASH for key in keys}
        write = {'leagues': wleagues}
        dpath = os.path.join(_root, 'download/leagues/{}.txt')
        dinjuries = dpath.format('injuries')
        dnews = dpath.format('news')
        dtransactions = dpath.format('transactions')
        fpath = os.path.join(_root, 'file/news/txt/leagues/league_100_{}.txt')
        finjuries = fpath.format('injuries')
        fnews = fpath.format('news')
        ftransactions = fpath.format('transactions')
        calls = [
            mock.call(dinjuries),
            mock.call(finjuries),
            mock.call(dnews),
            mock.call(fnews),
            mock.call(dtransactions),
            mock.call(ftransactions),
        ]
        mock_isfile.assert_has_calls(calls)
        calls = [
            mock.call('injuries', OLD_HASH, dinjuries, finjuries),
            mock.call('news', OLD_HASH, dnews, fnews),
            mock.call('transactions', OLD_HASH, dtransactions, ftransactions)
        ]
        mock_leagues.assert_has_calls(calls)
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch('plugins.download.download_plugin.open', create=True)
    @mock.patch('plugins.download.download_plugin.hash_file')
    @mock.patch('plugins.recap.recap_plugin.codecs.open')
    def test_leagues_internal__injuries(self, mock_copen, mock_hash,
                                        mock_open):
        cdata = '\n'.join([INJ_BEFORE, INJ_CONTENT, INJ_AFTER])
        cmo = mock.mock_open(read_data=cdata)
        mock_copen.side_effect = [cmo.return_value]
        mock_hash.return_value = NEW_HASH
        data = INJ_CONTENT
        mo = mock.mock_open(read_data=data)
        mock_handle = mo()
        mock_open.side_effect = [mo.return_value, mo.return_value]

        dname = 'download/injuries.txt'
        fname = 'file/news/txt/leagues/league_100_injuries.txt'
        keys = ['injuries', 'news', 'transactions']
        leagues = {key: OLD_HASH for key in keys}
        read = {'downloaded': False, 'leagues': leagues}
        plugin = self.create_plugin(read)
        plugin._leagues_internal('injuries', OLD_HASH, dname, fname)

        mock_copen.assert_called_once_with(
            fname, 'r', encoding='utf-8', errors='replace')
        calls = [mock.call(dname, 'r'), mock.call(dname, 'w')]
        mock_open.assert_has_calls(calls)
        mock_handle.write.assert_called_once_with(INJ_AFTER.strip())
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.assertEqual(plugin.data['leagues']['injuries'], NEW_HASH)

    @mock.patch('plugins.download.download_plugin.open', create=True)
    @mock.patch('plugins.download.download_plugin.hash_file')
    @mock.patch('plugins.recap.recap_plugin.codecs.open')
    def test_leagues_internal__news(self, mock_copen, mock_hash, mock_open):
        cdata = '\n'.join([NEWS_BEFORE, NEWS_CONTENT, NEWS_AFTER])
        cmo = mock.mock_open(read_data=cdata)
        mock_copen.side_effect = [cmo.return_value]
        mock_hash.return_value = NEW_HASH
        data = NEWS_CONTENT
        mo = mock.mock_open(read_data=data)
        mock_handle = mo()
        mock_open.side_effect = [mo.return_value, mo.return_value]

        dname = 'download/news.txt'
        fname = 'file/news/txt/leagues/league_100_news.txt'
        keys = ['injuries', 'news', 'transactions']
        leagues = {key: OLD_HASH for key in keys}
        read = {'downloaded': False, 'leagues': leagues}
        plugin = self.create_plugin(read)
        plugin._leagues_internal('news', OLD_HASH, dname, fname)

        mock_copen.assert_called_once_with(
            fname, 'r', encoding='utf-8', errors='replace')
        calls = [mock.call(dname, 'r'), mock.call(dname, 'w')]
        mock_open.assert_has_calls(calls)
        mock_handle.write.assert_called_once_with(NEWS_AFTER.strip())
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.assertEqual(plugin.data['leagues']['news'], NEW_HASH)

    @mock.patch('plugins.download.download_plugin.open', create=True)
    @mock.patch('plugins.download.download_plugin.hash_file')
    @mock.patch('plugins.recap.recap_plugin.codecs.open')
    def test_leagues_internal__transactions(self, mock_copen, mock_hash,
                                            mock_open):
        cdata = '\n'.join([TRANS_BEFORE, TRANS_CONTENT, TRANS_AFTER])
        cmo = mock.mock_open(read_data=cdata)
        mock_copen.side_effect = [cmo.return_value]
        mock_hash.return_value = NEW_HASH
        data = TRANS_CONTENT
        mo = mock.mock_open(read_data=data)
        mock_handle = mo()
        mock_open.side_effect = [mo.return_value, mo.return_value]

        dname = 'download/transactions.txt'
        fname = 'file/transactions/txt/leagues/league_100_transactions.txt'
        keys = ['injuries', 'news', 'transactions']
        leagues = {key: OLD_HASH for key in keys}
        read = {'downloaded': False, 'leagues': leagues}
        plugin = self.create_plugin(read)
        plugin._leagues_internal('transactions', OLD_HASH, dname, fname)

        mock_copen.assert_called_once_with(
            fname, 'r', encoding='utf-8', errors='replace')
        calls = [mock.call(dname, 'r'), mock.call(dname, 'w')]
        mock_open.assert_has_calls(calls)
        mock_handle.write.assert_called_once_with(TRANS_AFTER.strip())
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.assertEqual(plugin.data['leagues']['transactions'], NEW_HASH)


if __name__ == '__main__':
    unittest.main()
