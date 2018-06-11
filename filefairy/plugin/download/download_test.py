#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import logging
import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(_path)
_root = re.sub(r'/plugin/download', '', _path)
sys.path.append(_root)
from core.notify.notify import Notify  # noqa
from core.response.response import Response  # noqa
from core.shadow.shadow import Shadow  # noqa
from core.task.task import Task  # noqa
from plugin.download.download import Download  # noqa
from util.json_.json_ import dumps  # noqa

_now = datetime.datetime(2022, 8, 17)
_now_encoded = '2022-08-17T00:00:00'
_then = datetime.datetime(2022, 8, 16)
_then_encoded = '2022-08-16T00:00:00'
_year_encoded = '2023-01-01T00:00:00'


def _data(downloaded=False, now=_now_encoded, then=_then_encoded, year=False):
    return {'downloaded': downloaded, 'now': now, 'then': then, 'year': year}


class DownloadTest(unittest.TestCase):
    def setUp(self):
        patch_open = mock.patch(
            'api.serializable.serializable.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

        patch_log = mock.patch('plugin.download.download.logger_.log')
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
        plugin = Download(date=_now)

        self.mock_open.assert_called_once_with(Download._data(), 'r')
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()

        self.reset_mocks()
        self.init_mocks(data)

        return plugin

    @mock.patch.object(Download, 'download')
    def test_notify__with_file(self, mock_download):
        mock_task = mock.MagicMock(spec=Task)
        mock_download.return_value = Response(task=[mock_task])
        plugin = self.create_plugin(_data())
        response = plugin._notify_internal(notify=Notify.LEAGUEFILE_FINISH)
        self.assertEqual(response,
                         Response(notify=[Notify.BASE], task=[mock_task]))

        mock_download.assert_called_once_with(notify=Notify.LEAGUEFILE_FINISH)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()

    @mock.patch.object(Download, 'download')
    def test_notify__with_other(self, mock_download):
        plugin = self.create_plugin(_data())
        response = plugin._notify_internal(notify=Notify.OTHER)
        self.assertEqual(response, Response())

        mock_download.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()

    def test_on_message(self):
        plugin = self.create_plugin(_data())
        response = plugin._on_message_internal()
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()

    def test_run__with_downloaded(self):
        plugin = self.create_plugin(_data(downloaded=True))
        response = plugin._run_internal(date=_then)
        self.assertEqual(response,
                         Response(
                             notify=[Notify.DOWNLOAD_FINISH],
                             shadow=[
                                 Shadow(
                                     destination='statsplus',
                                     key='download.now',
                                     data=_now_encoded)
                             ]))

        write = {
            'downloaded': False,
            'now': _now_encoded,
            'then': _then_encoded,
            'year': False
        }
        self.mock_open.assert_called_once_with(Download._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_log.assert_not_called()

    def test_run__with_year(self):
        plugin = self.create_plugin(_data(now=_year_encoded, year=True))
        response = plugin._run_internal(date=_then)
        self.assertEqual(response, Response(notify=[Notify.DOWNLOAD_YEAR]))

        write = {
            'downloaded': False,
            'now': _year_encoded,
            'then': _then_encoded,
            'year': False
        }
        self.mock_open.assert_called_once_with(Download._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_log.assert_not_called()

    def test_setup(self):
        plugin = self.create_plugin(_data())
        response = plugin._setup_internal()
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()

    def test_shadow(self):
        plugin = self.create_plugin(_data())
        value = plugin._shadow_internal()
        self.assertEqual(value, [
            Shadow(
                destination='statsplus', key='download.now', data=_now_encoded)
        ])

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()

    @mock.patch('plugin.download.download.ping')
    def test_download__with_ok_false(self, mock_ping):
        mock_ping.return_value = {'ok': False, 'output': 'ret'}

        plugin = self.create_plugin(_data())
        response = plugin.download()
        self.assertEqual(response, Response())

        self.mock_log.assert_called_once_with(
            logging.DEBUG, 'Download failed.', extra={
                'output': 'ret'
            })

    @mock.patch('plugin.download.download.ping')
    def test_download__with_ok_true(self, mock_ping):
        mock_ping.return_value = {'ok': True}

        plugin = self.create_plugin(_data())
        response = plugin.download()
        self.assertEqual(
            response,
            Response(task=[Task(target='_download_internal', kwargs={})]))

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_called_once_with(logging.INFO,
                                              'Download started.')

    @mock.patch.object(Download, '_leagues')
    @mock.patch('plugin.download.download.wget_file')
    @mock.patch.object(Download, '_games')
    def test_download_internal__with_new_year(self, mock_games, mock_file,
                                              mock_leagues):
        mock_file.return_value = {'ok': True}

        plugin = self.create_plugin(_data(now=_then_encoded))

        def fake_games(*args, **kwargs):
            plugin.data['now'] = _year_encoded

        mock_games.side_effect = fake_games

        response = plugin._download_internal(v=True)
        self.assertEqual(response, Response())

        mock_games.assert_called_once_with()
        mock_file.assert_called_once_with()
        mock_leagues.assert_called_once_with()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_called_once_with(logging.INFO,
                                              'Download finished.')
        self.assertTrue(plugin.data['downloaded'])
        self.assertEqual(plugin.data['now'], _year_encoded)
        self.assertEqual(plugin.data['then'], _then_encoded)
        self.assertTrue(plugin.data['year'])

    @mock.patch.object(Download, '_leagues')
    @mock.patch('plugin.download.download.wget_file')
    @mock.patch.object(Download, '_games')
    def test_download_internal__with_same_year(self, mock_games, mock_file,
                                               mock_leagues):
        mock_file.return_value = {'ok': True}

        plugin = self.create_plugin(_data(now=_then_encoded))

        def fake_games(*args, **kwargs):
            plugin.data['now'] = _now_encoded

        mock_games.side_effect = fake_games

        response = plugin._download_internal(v=True)
        self.assertEqual(response, Response())

        mock_games.assert_called_once_with()
        mock_file.assert_called_once_with()
        mock_leagues.assert_called_once_with()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_called_once_with(logging.INFO,
                                              'Download finished.')
        self.assertTrue(plugin.data['downloaded'])
        self.assertEqual(plugin.data['now'], _now_encoded)
        self.assertEqual(plugin.data['then'], _then_encoded)
        self.assertFalse(plugin.data['year'])

    @mock.patch('plugin.download.download.recreate')
    @mock.patch('plugin.download.download.os.listdir')
    @mock.patch('plugin.download.download.os.path.isfile')
    @mock.patch.object(Download, '_games_internal')
    def test_games(self, mock_games, mock_isfile, mock_listdir, mock_recreate):
        mock_isfile.return_value = True
        mock_listdir.return_value = ['game_box_123.html', 'game_box_456.html']

        plugin = self.create_plugin(_data())
        plugin._games()

        box_scores = os.path.join(_root, 'resource/extract/box_scores')
        game_logs = os.path.join(_root, 'resource/extract/game_logs')
        boxes = 'resource/download/news/html/box_scores'
        bdpath = os.path.join(box_scores, 'game_box_{}.html')
        bd123 = bdpath.format('123')
        bd456 = bdpath.format('456')
        bfpath = os.path.join(_root, boxes, 'game_box_{}.html')
        bf123 = bfpath.format('123')
        bf456 = bfpath.format('456')
        leagues = 'resource/download/news/txt/leagues'
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
        box = '<html>\n<head>\n<title>MLB Box Scores, Seattle Mariners at ' + \
              'Los Angeles Dodgers, 08/16/2022</title>'
        bmo = mock.mock_open(read_data=box)
        mock_bhandle = bmo()
        log = '[%T] Top of the 1st...'
        lmo = mock.mock_open(read_data=log)
        mock_lhandle = lmo()
        mock_open.side_effect = [
            bmo.return_value, lmo.return_value, bmo.return_value,
            lmo.return_value
        ]

        bdname = 'resource/extract/box_scores/game_box_12345.html'
        bfname = 'resource/download/news/html/box_scores/game_box_12345.html'
        ldname = 'resource/extract/game_logs/log_12345.txt'
        lfname = 'resource/download/news/txt/leagues/log_12345.txt'
        plugin = self.create_plugin(_data(now=_then_encoded))
        plugin._games_internal(bdname, bfname, ldname, lfname)

        calls = [
            mock.call(bfname, 'r', encoding='iso-8859-1'),
            mock.call(lfname, 'r', encoding='iso-8859-1'),
            mock.call(bdname, 'w'),
            mock.call(ldname, 'w')
        ]
        mock_open.assert_has_calls(calls)
        mock_bhandle.write.assert_called_once_with(box)
        mock_lhandle.write.assert_called_once_with(log)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.assertEqual(plugin.data['now'], _now_encoded)
        self.mock_log.assert_not_called()

    @mock.patch('plugin.download.download.open', create=True)
    def test_games_internal__mlb_then(self, mock_open):
        box = '<html>\n<head>\n<title>MLB Box Scores, Seattle Mariners at ' + \
              'Los Angeles Dodgers, 08/15/2022</title>'
        bmo = mock.mock_open(read_data=box)
        mock_bhandle = bmo()
        log = '[%T] Top of the 1st...'
        lmo = mock.mock_open(read_data=log)
        mock_lhandle = lmo()
        mock_open.side_effect = [bmo.return_value, lmo.return_value]

        bdname = 'resource/extract/box_scores/game_box_12345.html'
        bfname = 'resource/download/news/html/box_scores/game_box_12345.html'
        ldname = 'resource/extract/game_logs/log_12345.txt'
        lfname = 'resource/download/news/txt/leagues/log_12345.txt'
        plugin = self.create_plugin(_data(now=_then_encoded))
        plugin._games_internal(bdname, bfname, ldname, lfname)

        calls = [
            mock.call(bfname, 'r', encoding='iso-8859-1'),
            mock.call(lfname, 'r', encoding='iso-8859-1')
        ]
        mock_open.assert_has_calls(calls)
        mock_bhandle.write.assert_not_called()
        mock_lhandle.write.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.assertEqual(plugin.data['now'], _then_encoded)
        self.mock_log.assert_not_called()

    @mock.patch('plugin.download.download.open', create=True)
    def test_games_internal__non_mlb(self, mock_open):
        box = '<html>\n<head>\n<title>ABL Box Scores, Adelaide Bite at Mel' + \
              'bourne Aces, 08/16/2022</title>'
        bmo = mock.mock_open(read_data=box)
        mock_bhandle = bmo()
        log = '[%T] Top of the 1st...'
        lmo = mock.mock_open(read_data=log)
        mock_lhandle = lmo()
        mock_open.side_effect = [bmo.return_value, lmo.return_value]

        bdname = 'resource/extract/box_scores/game_box_12345.html'
        bfname = 'resource/download/news/html/box_scores/game_box_12345.html'
        ldname = 'resource/extract/game_logs/log_12345.txt'
        lfname = 'resource/download/news/txt/leagues/log_12345.txt'
        plugin = self.create_plugin(_data(now=_then_encoded))
        plugin._games_internal(bdname, bfname, ldname, lfname)

        calls = [
            mock.call(bfname, 'r', encoding='iso-8859-1'),
            mock.call(lfname, 'r', encoding='iso-8859-1')
        ]
        mock_open.assert_has_calls(calls)
        mock_bhandle.write.assert_not_called()
        mock_lhandle.write.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.assertEqual(plugin.data['now'], _then_encoded)
        self.mock_log.assert_not_called()

    @mock.patch.object(Download, '_leagues_internal')
    @mock.patch('plugin.download.download.os.path.isfile')
    def test_leagues(self, mock_isfile, mock_leagues):
        mock_isfile.return_value = True

        plugin = self.create_plugin(_data())
        plugin._leagues()

        leagues = 'resource/download/news/txt/leagues'
        dpath = os.path.join(_root, 'resource/extract/leagues/{}.txt')
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
        injuries_new = '20220817\t<a href=\"../teams/team_57.html\">Tampa ' + \
                       'Bay Rays</a>: <a href=\"../players/player_1.html\"' + \
                       '>Zack Weiss</a> diagnosed with a strained hamstrin' + \
                       'g, will miss 4 weeks.\n20220817\t<a href=\"../team' + \
                       's/team_39.html\">Colorado Rockies</a>: RF <a href=' + \
                       '\"../players/player_24198.html\">Eddie Hoffman</a>' + \
                       ' was injured being hit by a pitch.  The Diagnosis:' + \
                       ' bruised knee. This is a day-to-day injury expecte' + \
                       'd to last 5 days.'
        injuries_old = '20220814\t<a href=\"../teams/team_44.html\">Los An' + \
                       'geles Angels</a>: CF <a href=\"../players/player_0' + \
                       '.html\">Alex Aristy</a> was injured while running ' + \
                       'the bases.  The Diagnosis: knee inflammation. He\'' + \
                       's expected to miss about 3 weeks.'
        data_a = '\n'.join([injuries_old, injuries_new])
        mo_a = mock.mock_open(read_data=data_a)
        mock_handle_a = mo_a()
        mo_b = mock.mock_open()
        mock_handle_b = mo_b()
        mock_open.side_effect = [mo_a.return_value, mo_b.return_value]

        dname = 'resource/extract/injuries.txt'
        fname = 'resource/download/news/txt/leagues/league_100_injuries.txt'
        plugin = self.create_plugin(_data(now=_then_encoded))
        plugin._leagues_internal('injuries', dname, fname)

        calls = [
            mock.call(fname, 'r', encoding='iso-8859-1'),
            mock.call(dname, 'w')
        ]
        mock_open.assert_has_calls(calls)
        mock_handle_a.write.assert_not_called()
        calls = [mock.call(s + '\n') for s in injuries_new.split('\n') if s]
        mock_handle_b.write.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.assertEqual(plugin.data['now'], _now_encoded)
        self.mock_log.assert_not_called()

    @mock.patch('plugin.download.download.open', create=True)
    def test_leagues_internal__news(self, mock_open):
        news_new = '20220816\t<a href=\"../teams/team_42.html\">Houston As' + \
                   'tros</a>: <a href=\"../players/player_39044.html\">Mar' + \
                   'k Appel</a> pitches a 2-hit shutout against the <a hre' + \
                   'f=\"../teams/team_44.html\">Los Angeles Angels</a> wit' + \
                   'h 8 strikeouts and 0 BB allowed!\n20220817\t<a href=\"' + \
                   '../teams/team_39.html\">Colorado Rockies</a>: <a href=' + \
                   '\"../players/player_30965.html\">Spencer Taylor</a> go' + \
                   't suspended 3 games after ejection following a brawl.'
        news_old = '20220815\t<a href=\"../teams/team_57.html\">Tampa Bay ' + \
                   'Rays</a>: <a href=\"../players/player_27.html\">A.J. R' + \
                   'eed</a> got suspended 4 games after ejection following' + \
                   ' arguing a strike call.'
        data_a = '\n'.join([news_old, news_new])
        mo_a = mock.mock_open(read_data=data_a)
        mock_handle_a = mo_a()
        mo_b = mock.mock_open()
        mock_handle_b = mo_b()
        mock_open.side_effect = [mo_a.return_value, mo_b.return_value]

        dname = 'resource/extract/news.txt'
        fname = 'resource/download/news/txt/leagues/league_100_news.txt'
        plugin = self.create_plugin(_data(now=_then_encoded))
        plugin._leagues_internal('news', dname, fname)

        calls = [
            mock.call(fname, 'r', encoding='iso-8859-1'),
            mock.call(dname, 'w')
        ]
        mock_open.assert_has_calls(calls)
        mock_handle_a.write.assert_not_called()
        calls = [mock.call(s + '\n') for s in news_new.split('\n') if s]
        mock_handle_b.write.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.assertEqual(plugin.data['now'], _now_encoded)
        self.mock_log.assert_not_called()

    @mock.patch('plugin.download.download.open', create=True)
    def test_leagues_internal__transactions(self, mock_open):
        transactions_new = '20220816\t<a href=\"../teams/team_33.html\">Ba' + \
                           'ltimore Orioles</a>: Placed C <a href=\"../pla' + \
                           'yers/player_1439.html\">Evan Skoug</a> on the ' + \
                           'active roster.\n\n20220816\t<a href=\"../teams' + \
                           '/team_33.html\">Baltimore Orioles</a>: Activat' + \
                           'ed C <a href=\"../players/player_1439.html\">E' + \
                           'van Skoug</a> from the disabled list.\n'
        transactions_old = '20220815\t<a href=\"../teams/team_33.html\">Ba' + \
                           'ltimore Orioles</a>: Placed 2B <a href=\"../pl' + \
                           'ayers/player_292.html\">Austin Slater</a> on t' + \
                           'he 7-day disabled list, retroactive to 08/12/2' + \
                           '022.\n'
        data_a = '\n'.join([transactions_old, transactions_new])
        mo_a = mock.mock_open(read_data=data_a)
        mock_handle_a = mo_a()
        mo_b = mock.mock_open()
        mock_handle_b = mo_b()
        mock_open.side_effect = [mo_a.return_value, mo_b.return_value]

        dname = 'resource/extract/transactions.txt'
        fname = 'resource/download/transactions/txt/leagues/' + \
                'league_100_transactions.txt'
        plugin = self.create_plugin(_data(now=_then_encoded))
        plugin._leagues_internal('transactions', dname, fname)

        calls = [
            mock.call(fname, 'r', encoding='iso-8859-1'),
            mock.call(dname, 'w')
        ]
        mock_open.assert_has_calls(calls)
        mock_handle_a.write.assert_not_called()
        calls = [
            mock.call(s + '\n') for s in transactions_new.split('\n') if s
        ]
        mock_handle_b.write.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.assertEqual(plugin.data['now'], _then_encoded)
        self.mock_log.assert_not_called()


if __name__ == '__main__':
    unittest.main()
