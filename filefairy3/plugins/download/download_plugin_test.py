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
INJ_NOW = '20220817\t<a href=\"../teams/team_57.html\">Tampa Bay Rays' + \
          '</a>: <a href=\"../players/player_1.html\">Zack Weiss</a> ' + \
          'diagnosed with a strained hamstring, will miss 4 weeks.\n' + \
          '20220817\t<a href=\"../teams/team_39.html\">Colorado ' + \
          'Rockies</a>: RF <a href=\"../players/player_24198.html\">' + \
          'Eddie Hoffman</a> was injured being hit by a pitch.  The ' + \
          'Diagnosis: bruised knee. This is a day-to-day injury ' + \
          'expected to last 5 days.'
INJ_THEN = '20220814\t<a href=\"../teams/team_44.html\">Los Angeles ' + \
           'Angels</a>: CF <a href=\"../players/player_0.html\">Alex ' + \
           'Aristy</a> was injured while running the bases.  The ' + \
           'Diagnosis: knee inflammation. He\'s expected to miss about ' + \
           '3 weeks.'
NEWS_NOW = '20220816\t<a href=\"../teams/team_42.html\">Houston ' + \
           'Astros</a>: <a href=\"../players/player_39044.html\">Mark ' + \
           'Appel</a> pitches a 2-hit shutout against the <a ' + \
           'href=\"../teams/team_44.html\">Los Angeles Angels</a> ' + \
           'with 8 strikeouts and 0 BB allowed!\n20220817\t<a ' + \
           'href=\"../teams/team_39.html\">Colorado Rockies</a>: <a ' + \
           'href=\"../players/player_30965.html\">Spencer Taylor</a> ' + \
           'got suspended 3 games after ejection following a brawl.'
NEWS_THEN = '20220815\t<a href=\"../teams/team_57.html\">Tampa Bay Rays' + \
            '</a>: <a href=\"../players/player_27.html\">A.J. Reed</a> ' + \
            'got suspended 4 games after ejection following arguing a ' + \
            'strike call.'
TRANS_NOW = '20220816\t<a href=\"../teams/team_33.html\">Baltimore ' + \
            'Orioles</a>: Placed C <a href=\"../players/player_1439.' + \
            'html\">Evan Skoug</a> on the active roster.\n\n20220816\t' + \
            '<a href=\"../teams/team_33.html\">Baltimore Orioles</a>: ' + \
            'Activated C <a href=\"../players/player_1439.html\">Evan ' + \
            'Skoug</a> from the disabled list.\n'
TRANS_THEN = '20220815\t<a href=\"../teams/team_33.html\">Baltimore ' + \
             'Orioles</a>: Placed 2B <a href=\"../players/player_292.' + \
             'html\">Austin Slater</a> on the 7-day disabled list, ' + \
             'retroactive to 08/12/2022.\n'
THEN = datetime.datetime(2022, 8, 16)
THEN_ENCODED = '2022-08-16T00:00:00'
NOW = datetime.datetime(2022, 8, 17)
NOW_ENCODED = '2022-08-17T00:00:00'


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

    @mock.patch('plugins.download.download_plugin.threading.Thread')
    @mock.patch.object(DownloadPlugin, '_download')
    def test_notify__with_file(self, mock_download, mock_thread):
        read = {'downloaded': False, 'now': NOW_ENCODED, 'then': THEN_ENCODED}
        plugin = self.create_plugin(read)
        ret = plugin._notify_internal(activity=ActivityEnum.FILE)
        self.assertTrue(ret)

        mock_thread.assert_called_once_with(target=mock_download)
        mock_thread.return_value.start.assert_called_once_with()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch('plugins.download.download_plugin.threading.Thread')
    @mock.patch.object(DownloadPlugin, '_download')
    def test_notify__with_none(self, mock_download, mock_thread):
        read = {'downloaded': False, 'now': NOW_ENCODED, 'then': THEN_ENCODED}
        plugin = self.create_plugin(read)
        ret = plugin._notify_internal(activity=ActivityEnum.NONE)
        self.assertFalse(ret)

        mock_thread.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    def test_on_message(self):
        read = {'downloaded': False, 'now': NOW_ENCODED, 'then': THEN_ENCODED}
        plugin = self.create_plugin(read)
        ret = plugin._on_message_internal()
        self.assertEqual(ret, ActivityEnum.NONE)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    def test_run__with_downloaded_true(self):
        read = {'downloaded': True, 'now': NOW_ENCODED, 'then': THEN_ENCODED}
        plugin = self.create_plugin(read)
        ret = plugin._run_internal(date=THEN)
        self.assertEqual(ret, ActivityEnum.DOWNLOAD)

        write = {'downloaded': False, 'now': NOW_ENCODED, 'then': THEN_ENCODED}
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    def test_run__with_downloaded_false(self):
        read = {'downloaded': False, 'now': NOW_ENCODED, 'then': THEN_ENCODED}
        plugin = self.create_plugin(read)
        ret = plugin._run_internal(date=THEN)
        self.assertEqual(ret, ActivityEnum.NONE)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    def test_setup(self):
        read = {'downloaded': False, 'now': NOW_ENCODED, 'then': THEN_ENCODED}
        plugin = self.create_plugin(read)
        plugin._setup_internal()

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(DownloadPlugin, '_leagues')
    @mock.patch('plugins.download.download_plugin.wget_file')
    def test_download(self, mock_file, mock_leagues):
        read = {'downloaded': False, 'now': NOW_ENCODED, 'then': THEN_ENCODED}
        plugin = self.create_plugin(read)
        plugin._download()

        write = {'downloaded': True, 'now': NOW_ENCODED, 'then': NOW_ENCODED}
        mock_file.assert_called_once_with()
        mock_leagues.assert_called_once_with()
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch.object(DownloadPlugin, '_leagues_internal')
    @mock.patch('plugins.download.download_plugin.os.path.isfile')
    def test_leagues(self, mock_isfile, mock_leagues):
        mock_isfile.return_value = True

        read = {'downloaded': False, 'now': NOW_ENCODED, 'then': THEN_ENCODED}
        plugin = self.create_plugin(read)
        plugin._leagues()

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
            mock.call('injuries', dinjuries, finjuries),
            mock.call('news', dnews, fnews),
            mock.call('transactions', dtransactions, ftransactions)
        ]
        mock_leagues.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch('plugins.download.download_plugin.open', create=True)
    @mock.patch('plugins.download.download_plugin.codecs.open')
    def test_leagues_internal__injuries(self, mock_copen, mock_open):
        cdata = '\n'.join([INJ_THEN, INJ_NOW])
        cmo = mock.mock_open(read_data=cdata)
        mock_copen.side_effect = [cmo.return_value]
        mo = mock.mock_open()
        mock_handle = mo()
        mock_open.side_effect = [mo.return_value]

        dname = 'download/injuries.txt'
        fname = 'file/news/txt/leagues/league_100_injuries.txt'
        read = {'downloaded': False, 'now': THEN_ENCODED, 'then': THEN_ENCODED}
        plugin = self.create_plugin(read)
        plugin._leagues_internal('injuries', dname, fname)

        mock_copen.assert_called_once_with(
            fname, 'r', encoding='utf-8', errors='replace')
        mock_open.assert_called_once_with(dname, 'w')
        calls = [mock.call(s + '\n') for s in INJ_NOW.split('\n') if s]
        mock_handle.write.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.assertEqual(plugin.data['now'], NOW_ENCODED)

    @mock.patch('plugins.download.download_plugin.open', create=True)
    @mock.patch('plugins.download.download_plugin.codecs.open')
    def test_leagues_internal__news(self, mock_copen, mock_open):
        cdata = '\n'.join([NEWS_THEN, NEWS_NOW])
        cmo = mock.mock_open(read_data=cdata)
        mock_copen.side_effect = [cmo.return_value]
        mo = mock.mock_open()
        mock_handle = mo()
        mock_open.side_effect = [mo.return_value]

        dname = 'download/news.txt'
        fname = 'file/news/txt/leagues/league_100_news.txt'
        read = {'downloaded': False, 'now': THEN_ENCODED, 'then': THEN_ENCODED}
        plugin = self.create_plugin(read)
        plugin._leagues_internal('news', dname, fname)

        mock_copen.assert_called_once_with(
            fname, 'r', encoding='utf-8', errors='replace')
        mock_open.assert_called_once_with(dname, 'w')
        calls = [mock.call(s + '\n') for s in NEWS_NOW.split('\n') if s]
        mock_handle.write.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.assertEqual(plugin.data['now'], NOW_ENCODED)

    @mock.patch('plugins.download.download_plugin.open', create=True)
    @mock.patch('plugins.download.download_plugin.codecs.open')
    def test_leagues_internal__transactions(self, mock_copen, mock_open):
        cdata = '\n'.join([TRANS_THEN, TRANS_NOW])
        cmo = mock.mock_open(read_data=cdata)
        mock_copen.side_effect = [cmo.return_value]
        mo = mock.mock_open()
        mock_handle = mo()
        mock_open.side_effect = [mo.return_value]

        dname = 'download/transactions.txt'
        fname = 'file/transactions/txt/leagues/league_100_transactions.txt'
        read = {'downloaded': False, 'now': THEN_ENCODED, 'then': THEN_ENCODED}
        plugin = self.create_plugin(read)
        plugin._leagues_internal('transactions', dname, fname)

        mock_copen.assert_called_once_with(
            fname, 'r', encoding='utf-8', errors='replace')
        mock_open.assert_called_once_with(dname, 'w')
        calls = [mock.call(s + '\n') for s in TRANS_NOW.split('\n') if s]
        mock_handle.write.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.assertEqual(plugin.data['now'], THEN_ENCODED)


if __name__ == '__main__':
    unittest.main()
