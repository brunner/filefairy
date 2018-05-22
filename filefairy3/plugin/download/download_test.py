#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(_path)
_root = re.sub(r'/plugin/download', '', _path)
sys.path.append(_root)
from plugin.download.download import Download  # noqa
from util.json_.json_ import dumps  # noqa
from value.notify.notify import Notify  # noqa
from value.response.response import Response  # noqa
from value.task.task import Task  # noqa

DATA = Download._data()
BOX_NON_MLB = '<html>\n<head>\n<title>ABL Box Scores, Adelaide Bite at ' + \
              'Melbourne Aces, 08/16/2022</title>'
BOX_MLB_NOW = '<html>\n<head>\n<title>MLB Box Scores, Seattle Mariners at ' + \
              'Los Angeles Dodgers, 08/16/2022</title>'
BOX_MLB_THEN = '<html>\n<head>\n<title>MLB Box Scores, Seattle Mariners ' + \
               'at Los Angeles Dodgers, 08/15/2022</title>'
LOG = '[%T] Top of the 1st...'
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
YEAR = datetime.datetime(2023, 1, 1)
YEAR_ENCODED = '2023-01-01T00:00:00'


class DownloadTest(unittest.TestCase):
    def setUp(self):
        patch_open = mock.patch(
            'api.serializable.serializable.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

        patch_log = mock.patch('plugin.download.download.log')
        self.addCleanup(patch_log.stop)
        self.mock_log = patch_log.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]

    def reset_mocks(self):
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()
        self.mock_log.reset_mock()

    def create_plugin(self, data):
        self.init_mocks(data)
        plugin = Download()

        self.mock_open.assert_called_once_with(DATA, 'r')
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()

        self.reset_mocks()
        self.init_mocks(data)

        return plugin

    @mock.patch.object(Download, 'download')
    def test_notify__with_file(self, mock_download):
        mock_task = mock.MagicMock(spec=Task)
        mock_download.return_value = Response(task=[mock_task])
        read = {
            'downloaded': False,
            'now': NOW_ENCODED,
            'then': THEN_ENCODED,
            'year': False
        }
        plugin = self.create_plugin(read)
        response = plugin._notify_internal(notify=Notify.LEAGUEFILE_FINISH)
        self.assertEqual(response,
                         Response(notify=[Notify.BASE], task=[mock_task]))

        mock_download.assert_called_once_with(notify=Notify.LEAGUEFILE_FINISH)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()

    @mock.patch.object(Download, 'download')
    def test_notify__with_other(self, mock_download):
        read = {
            'downloaded': False,
            'now': NOW_ENCODED,
            'then': THEN_ENCODED,
            'year': False
        }
        plugin = self.create_plugin(read)
        response = plugin._notify_internal(notify=Notify.OTHER)
        self.assertEqual(response, Response())

        mock_download.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()

    def test_on_message(self):
        read = {
            'downloaded': False,
            'now': NOW_ENCODED,
            'then': THEN_ENCODED,
            'year': False
        }
        plugin = self.create_plugin(read)
        response = plugin._on_message_internal()
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()

    def test_run__with_downloaded(self):
        read = {
            'downloaded': True,
            'now': NOW_ENCODED,
            'then': THEN_ENCODED,
            'year': False
        }
        plugin = self.create_plugin(read)
        response = plugin._run_internal(date=THEN)
        self.assertEqual(response,
                         Response(
                             notify=[Notify.DOWNLOAD_FINISH],
                             shadow={
                                 'statsplus': {
                                     'download.now': NOW_ENCODED
                                 }
                             }))

        write = {
            'downloaded': False,
            'now': NOW_ENCODED,
            'then': THEN_ENCODED,
            'year': False
        }
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_log.assert_not_called()

    def test_run__with_year(self):
        read = {
            'downloaded': False,
            'now': YEAR_ENCODED,
            'then': THEN_ENCODED,
            'year': True
        }
        plugin = self.create_plugin(read)
        response = plugin._run_internal(date=THEN)
        self.assertEqual(response, Response(notify=[Notify.DOWNLOAD_YEAR]))

        write = {
            'downloaded': False,
            'now': YEAR_ENCODED,
            'then': THEN_ENCODED,
            'year': False
        }
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_log.assert_not_called()

    def test_setup(self):
        read = {
            'downloaded': False,
            'now': NOW_ENCODED,
            'then': THEN_ENCODED,
            'year': False
        }
        plugin = self.create_plugin(read)
        response = plugin._setup_internal()
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()

    def test_shadow(self):
        read = {
            'downloaded': False,
            'now': NOW_ENCODED,
            'then': THEN_ENCODED,
            'year': False
        }
        plugin = self.create_plugin(read)
        value = plugin._shadow_internal()
        self.assertEqual(value, {'statsplus': {'download.now': NOW_ENCODED}})

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()

    @mock.patch('plugin.download.download.ping')
    def test_download__with_ok_false(self, mock_ping):
        mock_ping.return_value = {'ok': False}

        read = {
            'downloaded': False,
            'now': NOW_ENCODED,
            'then': THEN_ENCODED,
            'year': False
        }
        plugin = self.create_plugin(read)
        response = plugin.download()
        self.assertEqual(response, Response())

        self.mock_log.assert_called_once_with('Download', **{
            'c': {
                'ok': False
            },
            's': 'Download failed.',
            'v': True
        })

    @mock.patch('plugin.download.download.ping')
    def test_download__with_ok_true(self, mock_ping):
        mock_ping.return_value = {'ok': True}

        read = {
            'downloaded': False,
            'now': NOW_ENCODED,
            'then': THEN_ENCODED,
            'year': False
        }
        plugin = self.create_plugin(read)
        response = plugin.download()
        self.assertEqual(
            response,
            Response(task=[Task(target=plugin._download_internal, kwargs={})]))

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_called_once_with('Download', **{
            's': 'Download started.'
        })

    @mock.patch.object(Download, '_leagues')
    @mock.patch('plugin.download.download.wget_file')
    @mock.patch.object(Download, '_games')
    def test_download_internal__with_new_year(self, mock_games, mock_file,
                                              mock_leagues):
        mock_file.return_value = {'ok': True}
        read = {
            'downloaded': False,
            'now': THEN_ENCODED,
            'then': THEN_ENCODED,
            'year': False
        }
        plugin = self.create_plugin(read)

        def fake_games(*args, **kwargs):
            plugin.data['now'] = YEAR_ENCODED

        mock_games.side_effect = fake_games

        plugin._download_internal(v=True)

        mock_games.assert_called_once_with()
        mock_file.assert_called_once_with()
        mock_leagues.assert_called_once_with()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_called_once_with('Download', **{
            's': 'Download finished.',
            'v': True
        })
        self.assertTrue(plugin.data['downloaded'])
        self.assertEqual(plugin.data['now'], YEAR_ENCODED)
        self.assertEqual(plugin.data['then'], THEN_ENCODED)
        self.assertTrue(plugin.data['year'])

    @mock.patch.object(Download, '_leagues')
    @mock.patch('plugin.download.download.wget_file')
    @mock.patch.object(Download, '_games')
    def test_download_internal__with_same_year(self, mock_games, mock_file,
                                               mock_leagues):
        mock_file.return_value = {'ok': True}

        read = {
            'downloaded': False,
            'now': THEN_ENCODED,
            'then': THEN_ENCODED,
            'year': False
        }
        plugin = self.create_plugin(read)

        def fake_games(*args, **kwargs):
            plugin.data['now'] = NOW_ENCODED

        mock_games.side_effect = fake_games

        plugin._download_internal(v=True)

        mock_games.assert_called_once_with()
        mock_file.assert_called_once_with()
        mock_leagues.assert_called_once_with()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_called_once_with('Download', **{
            's': 'Download finished.',
            'v': True
        })
        self.assertTrue(plugin.data['downloaded'])
        self.assertEqual(plugin.data['now'], NOW_ENCODED)
        self.assertEqual(plugin.data['then'], THEN_ENCODED)
        self.assertFalse(plugin.data['year'])

    @mock.patch('plugin.download.download.recreate')
    @mock.patch('plugin.download.download.os.listdir')
    @mock.patch('plugin.download.download.os.path.isfile')
    @mock.patch.object(Download, '_games_internal')
    def test_games(self, mock_games, mock_isfile, mock_listdir, mock_recreate):
        mock_isfile.return_value = True
        mock_listdir.return_value = ['game_box_123.html', 'game_box_456.html']

        read = {
            'downloaded': False,
            'now': NOW_ENCODED,
            'then': THEN_ENCODED,
            'year': False
        }
        plugin = self.create_plugin(read)
        plugin._games()

        box_scores = os.path.join(_root, 'extract/box_scores')
        game_logs = os.path.join(_root, 'extract/game_logs')
        boxes = 'download/news/html/box_scores'
        bdpath = os.path.join(box_scores, 'game_box_{}.html')
        bd123 = bdpath.format('123')
        bd456 = bdpath.format('456')
        bfpath = os.path.join(_root, boxes, 'game_box_{}.html')
        bf123 = bfpath.format('123')
        bf456 = bfpath.format('456')
        leagues = 'download/news/txt/leagues'
        ldpath = os.path.join(game_logs, 'log_{}.txt')
        ld123 = ldpath.format('123')
        ld456 = ldpath.format('456')
        lfpath = os.path.join(_root, leagues, 'log_{}.txt')
        lf123 = lfpath.format('123')
        lf456 = lfpath.format('456')
        calls = [
            mock.call(bf123),
            mock.call(lf123),
            mock.call(bf456),
            mock.call(lf456)
        ]
        mock_isfile.assert_has_calls(calls)
        calls = [
            mock.call(bd123, bf123, ld123, lf123),
            mock.call(bd456, bf456, ld456, lf456)
        ]
        mock_games.assert_has_calls(calls)
        calls = [mock.call(box_scores), mock.call(game_logs)]
        mock_recreate.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()

    @mock.patch('plugin.download.download.open', create=True)
    def test_games_internal__mlb_now(self, mock_open):
        bmo = mock.mock_open(read_data=BOX_MLB_NOW)
        mock_bhandle = bmo()
        lmo = mock.mock_open(read_data=LOG)
        mock_lhandle = lmo()
        mock_open.side_effect = [
            bmo.return_value, lmo.return_value, bmo.return_value,
            lmo.return_value
        ]

        bdname = 'extract/box_scores/game_box_12345.html'
        bfname = 'download/news/html/box_scores/game_box_12345.html'
        ldname = 'extract/game_logs/log_12345.txt'
        lfname = 'download/news/txt/leagues/log_12345.txt'
        read = {
            'downloaded': False,
            'now': THEN_ENCODED,
            'then': THEN_ENCODED,
            'year': False
        }
        plugin = self.create_plugin(read)
        plugin._games_internal(bdname, bfname, ldname, lfname)

        calls = [
            mock.call(bfname, 'r'),
            mock.call(lfname, 'r'),
            mock.call(bdname, 'w'),
            mock.call(ldname, 'w')
        ]
        mock_open.assert_has_calls(calls)
        mock_bhandle.write.assert_called_once_with(BOX_MLB_NOW)
        mock_lhandle.write.assert_called_once_with(LOG)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.assertEqual(plugin.data['now'], NOW_ENCODED)
        self.mock_log.assert_not_called()

    @mock.patch('plugin.download.download.open', create=True)
    def test_games_internal__mlb_then(self, mock_open):
        bmo = mock.mock_open(read_data=BOX_MLB_THEN)
        mock_bhandle = bmo()
        lmo = mock.mock_open(read_data=LOG)
        mock_lhandle = lmo()
        mock_open.side_effect = [bmo.return_value, lmo.return_value]

        bdname = 'extract/box_scores/game_box_12345.html'
        bfname = 'download/news/html/box_scores/game_box_12345.html'
        ldname = 'extract/game_logs/log_12345.txt'
        lfname = 'download/news/txt/leagues/log_12345.txt'
        read = {
            'downloaded': False,
            'now': THEN_ENCODED,
            'then': THEN_ENCODED,
            'year': False
        }
        plugin = self.create_plugin(read)
        plugin._games_internal(bdname, bfname, ldname, lfname)

        calls = [mock.call(bfname, 'r'), mock.call(lfname, 'r')]
        mock_open.assert_has_calls(calls)
        mock_bhandle.write.assert_not_called()
        mock_lhandle.write.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.assertEqual(plugin.data['now'], THEN_ENCODED)
        self.mock_log.assert_not_called()

    @mock.patch('plugin.download.download.open', create=True)
    def test_games_internal__non_mlb(self, mock_open):
        bmo = mock.mock_open(read_data=BOX_NON_MLB)
        mock_bhandle = bmo()
        lmo = mock.mock_open(read_data=LOG)
        mock_lhandle = lmo()
        mock_open.side_effect = [bmo.return_value, lmo.return_value]

        bdname = 'extract/box_scores/game_box_12345.html'
        bfname = 'download/news/html/box_scores/game_box_12345.html'
        ldname = 'extract/game_logs/log_12345.txt'
        lfname = 'download/news/txt/leagues/log_12345.txt'
        read = {
            'downloaded': False,
            'now': THEN_ENCODED,
            'then': THEN_ENCODED,
            'year': False
        }
        plugin = self.create_plugin(read)
        plugin._games_internal(bdname, bfname, ldname, lfname)

        calls = [mock.call(bfname, 'r'), mock.call(lfname, 'r')]
        mock_open.assert_has_calls(calls)
        mock_bhandle.write.assert_not_called()
        mock_lhandle.write.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.assertEqual(plugin.data['now'], THEN_ENCODED)
        self.mock_log.assert_not_called()

    @mock.patch.object(Download, '_leagues_internal')
    @mock.patch('plugin.download.download.os.path.isfile')
    def test_leagues(self, mock_isfile, mock_leagues):
        mock_isfile.return_value = True

        read = {
            'downloaded': False,
            'now': NOW_ENCODED,
            'then': THEN_ENCODED,
            'year': False
        }
        plugin = self.create_plugin(read)
        plugin._leagues()

        leagues = 'download/news/txt/leagues'
        dpath = os.path.join(_root, 'extract/leagues/{}.txt')
        dinjuries = dpath.format('injuries')
        dnews = dpath.format('news')
        dtransactions = dpath.format('transactions')
        fpath = os.path.join(_root, leagues, 'league_100_{}.txt')
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
        self.mock_log.assert_not_called()

    @mock.patch('plugin.download.download.open', create=True)
    def test_leagues_internal__injuries(self, mock_open):
        data_a = '\n'.join([INJ_THEN, INJ_NOW])
        mo_a = mock.mock_open(read_data=data_a)
        mock_handle_a = mo_a()
        mo_b = mock.mock_open()
        mock_handle_b = mo_b()
        mock_open.side_effect = [mo_a.return_value, mo_b.return_value]

        dname = 'extract/injuries.txt'
        fname = 'download/news/txt/leagues/league_100_injuries.txt'
        read = {
            'downloaded': False,
            'now': THEN_ENCODED,
            'then': THEN_ENCODED,
            'year': False
        }
        plugin = self.create_plugin(read)
        plugin._leagues_internal('injuries', dname, fname)

        calls = [
            mock.call(fname, 'r', encoding='iso-8859-1'),
            mock.call(dname, 'w')
        ]
        mock_open.assert_has_calls(calls)
        mock_handle_a.write.assert_not_called()
        calls = [mock.call(s + '\n') for s in INJ_NOW.split('\n') if s]
        mock_handle_b.write.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.assertEqual(plugin.data['now'], NOW_ENCODED)
        self.mock_log.assert_not_called()

    @mock.patch('plugin.download.download.open', create=True)
    def test_leagues_internal__news(self, mock_open):
        data_a = '\n'.join([NEWS_THEN, NEWS_NOW])
        mo_a = mock.mock_open(read_data=data_a)
        mock_handle_a = mo_a()
        mo_b = mock.mock_open()
        mock_handle_b = mo_b()
        mock_open.side_effect = [mo_a.return_value, mo_b.return_value]

        dname = 'extract/news.txt'
        fname = 'download/news/txt/leagues/league_100_news.txt'
        read = {
            'downloaded': False,
            'now': THEN_ENCODED,
            'then': THEN_ENCODED,
            'year': False
        }
        plugin = self.create_plugin(read)
        plugin._leagues_internal('news', dname, fname)

        calls = [
            mock.call(fname, 'r', encoding='iso-8859-1'),
            mock.call(dname, 'w')
        ]
        mock_open.assert_has_calls(calls)
        mock_handle_a.write.assert_not_called()
        calls = [mock.call(s + '\n') for s in NEWS_NOW.split('\n') if s]
        mock_handle_b.write.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.assertEqual(plugin.data['now'], NOW_ENCODED)
        self.mock_log.assert_not_called()

    @mock.patch('plugin.download.download.open', create=True)
    def test_leagues_internal__transactions(self, mock_open):
        data_a = '\n'.join([TRANS_THEN, TRANS_NOW])
        mo_a = mock.mock_open(read_data=data_a)
        mock_handle_a = mo_a()
        mo_b = mock.mock_open()
        mock_handle_b = mo_b()
        mock_open.side_effect = [mo_a.return_value, mo_b.return_value]

        dname = 'extract/transactions.txt'
        fname = 'download/transactions/txt/leagues/league_100_transactions.txt'
        read = {
            'downloaded': False,
            'now': THEN_ENCODED,
            'then': THEN_ENCODED,
            'year': False
        }
        plugin = self.create_plugin(read)
        plugin._leagues_internal('transactions', dname, fname)

        calls = [
            mock.call(fname, 'r', encoding='iso-8859-1'),
            mock.call(dname, 'w')
        ]
        mock_open.assert_has_calls(calls)
        mock_handle_a.write.assert_not_called()
        calls = [mock.call(s + '\n') for s in TRANS_NOW.split('\n') if s]
        mock_handle_b.write.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.assertEqual(plugin.data['now'], THEN_ENCODED)
        self.mock_log.assert_not_called()


if __name__ == '__main__':
    unittest.main()
