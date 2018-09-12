#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/util/news', '', _path)
sys.path.append(_root)
from util.datetime_.datetime_ import datetime_datetime_pst  # noqa
from util.news.news import extract_box_scores  # noqa
from util.news.news import extract_leagues  # noqa

_now = datetime_datetime_pst(2022, 10, 16)
_then = datetime_datetime_pst(2022, 10, 9)

_box_sub = '<html> <title>MLB Box Scores, Arizona Diamondbacks at Lo' + \
           's Angeles Dodgers, {}</title> </html>'
_box_here = os.path.join(_root, 'resource/download/news/html/box_scores')
_box_there = os.path.join(_root, 'resource/extract/box_scores')
_game = '[%T]\tTop of the 1st -  Arizona Diamondbacks batting'
_game_here = os.path.join(_root, 'resource/download/news/txt/leagues')
_game_there = os.path.join(_root, 'resource/extract/game_logs')
_leagues_here = os.path.join(_root, 'resource/download/news/txt/leagues')
_leagues_there = os.path.join(_root, 'resource/extract/leagues')
_injuries_here = os.path.join(_leagues_here, 'league_100_injuries.txt')
_injuries_there = os.path.join(_leagues_there, 'injuries.txt')
_news_here = os.path.join(_leagues_here, 'league_100_news.txt')
_news_there = os.path.join(_leagues_there, 'news.txt')
_transactions_here = os.path.join(_leagues_here, 'league_100_transactions.txt')
_transactions_there = os.path.join(_leagues_there, 'transactions.txt')
_leagues_isfile_calls = [
    mock.call(_injuries_here),
    mock.call(_news_here),
    mock.call(_transactions_here),
]
_leagues_open_calls = [
    mock.call(_injuries_here, 'r', encoding='iso-8859-1'),
    mock.call(_injuries_there, 'w'),
    mock.call(_news_here, 'r', encoding='iso-8859-1'),
    mock.call(_news_there, 'w'),
    mock.call(_transactions_here, 'r', encoding='iso-8859-1'),
    mock.call(_transactions_there, 'w'),
]
_injuries_then = '20221008\t<a href=\"../teams/team_44.html\">Los Angeles ' + \
                 'Angels</a>: CF <a href=\"../players/player_0.html\">Alex' + \
                 'Aristy</a> was injured while running the bases.  The Dia' + \
                 'gnosis: knee inflammation. He\'s expected to miss about ' + \
                 '3 weeks.'
_news_then = '20221008\t<a href=\"../teams/team_57.html\">Tampa Bay Rays</' + \
             'a>: <a href=\"../players/player_27.html\">A.J. Reed</a> got ' + \
             'suspended 4 games after ejection following arguing a strike ' + \
             'call.'
_transactions_then = '20221008\t<a href=\"../teams/team_33.html\">Baltimor' + \
                    'e Orioles</a>: Placed 2B <a href=\"../players/player_' + \
                    '292.html\">Austin Slater</a> on the 7-day disabled li' + \
                    'st, retroactive to 10/06/2022.\n'


class NewsTest(unittest.TestCase):
    @mock.patch('util.news.news.recreate')
    @mock.patch('util.news.news.open', create=True)
    @mock.patch('util.news.news.os.listdir')
    @mock.patch('util.news.news.os.path.isfile')
    def test_box_scores__with_now_date(self, mock_isfile, mock_listdir,
                                       mock_open, mock_recreate):
        mock_isfile.return_value = True
        mock_listdir.return_value = ['game_box_123.html']
        box = _box_sub.format('10/15/2022')
        mo_box_here = mock.mock_open(read_data=box)
        mo_box_there = mock.mock_open()
        mock_handle_box_there = mo_box_there()
        mo_game_here = mock.mock_open(read_data=_game)
        mo_game_there = mock.mock_open()
        mock_handle_game_there = mo_game_there()
        mock_open.side_effect = [
            mo_box_here.return_value, mo_game_here.return_value,
            mo_box_there.return_value, mo_game_there.return_value
        ]

        actual = extract_box_scores(_then)
        self.assertEqual(actual, _now)

        box_here_123 = os.path.join(_box_here, 'game_box_123.html')
        box_there_123 = os.path.join(_box_there, 'game_box_123.html')
        game_here_123 = os.path.join(_game_here, 'log_123.txt')
        game_there_123 = os.path.join(_game_there, 'log_123.txt')
        isfile_calls = [
            mock.call(box_here_123),
            mock.call(game_here_123),
        ]
        mock_isfile.assert_has_calls(isfile_calls)
        mock_listdir.assert_called_once_with(_box_here)
        open_calls = [
            mock.call(box_here_123, 'r', encoding='iso-8859-1'),
            mock.call(game_here_123, 'r', encoding='iso-8859-1'),
            mock.call(box_there_123, 'w'),
            mock.call(game_there_123, 'w')
        ]
        mock_open.assert_has_calls(open_calls)
        mock_handle_box_there.write.assert_called_once_with(box)
        mock_handle_game_there.write.assert_called_once_with(_game)
        calls = [mock.call(_box_there), mock.call(_game_there)]
        mock_recreate.assert_has_calls(calls)

    @mock.patch('util.news.news.recreate')
    @mock.patch('util.news.news.open', create=True)
    @mock.patch('util.news.news.os.listdir')
    @mock.patch('util.news.news.os.path.isfile')
    def test_box_scores__with_then_date(self, mock_isfile, mock_listdir,
                                        mock_open, mock_recreate):
        mock_isfile.return_value = True
        mock_listdir.return_value = ['game_box_123.html']
        box = _box_sub.format('10/01/2022')
        mo_box_here = mock.mock_open(read_data=box)
        mo_game_here = mock.mock_open(read_data=_game)
        mock_open.side_effect = [
            mo_box_here.return_value, mo_game_here.return_value
        ]

        actual = extract_box_scores(_then)
        self.assertEqual(actual, _then)

        box_here_123 = os.path.join(_box_here, 'game_box_123.html')
        game_here_123 = os.path.join(_game_here, 'log_123.txt')
        isfile_calls = [
            mock.call(box_here_123),
            mock.call(game_here_123),
        ]
        mock_isfile.assert_has_calls(isfile_calls)
        mock_listdir.assert_called_once_with(_box_here)
        open_calls = [
            mock.call(box_here_123, 'r', encoding='iso-8859-1'),
            mock.call(game_here_123, 'r', encoding='iso-8859-1')
        ]
        mock_open.assert_has_calls(open_calls)
        calls = [mock.call(_box_there), mock.call(_game_there)]
        mock_recreate.assert_has_calls(calls)

    @mock.patch('util.news.news.recreate')
    @mock.patch('util.news.news.open', create=True)
    @mock.patch('util.news.news.os.path.isfile')
    def test_leagues__with_now_date_injuries(self, mock_isfile, mock_open,
                                             mock_recreate):
        mock_isfile.return_value = True
        injuries_now = '20221016\t<a href=\"../teams/team_57.html\">Tampa ' + \
                       'Bay Rays</a>: <a href=\"../players/player_1.html\"' + \
                       '>Zack Weiss</a> diagnosed with a strained hamstrin' + \
                       'g, will miss 4 weeks.\n20221016\t<a href=\"../team' + \
                       's/team_39.html\">Colorado Rockies</a>: RF <a href=' + \
                       '\"../players/player_24198.html\">Eddie Hoffman</a>' + \
                       ' was injured being hit by a pitch.  The Diagnosis:' + \
                       ' bruised knee. This is a day-to-day injury expecte' + \
                       'd to last 5 days.'
        injuries = '\n'.join([_injuries_then, injuries_now])
        mo_injuries_here = mock.mock_open(read_data=injuries)
        mo_injuries_there = mock.mock_open()
        mo_news_here = mock.mock_open()
        mo_news_there = mock.mock_open()
        mo_transactions_here = mock.mock_open()
        mo_transactions_there = mock.mock_open()
        mock_handle_injuries_there = mo_injuries_there()
        mock_handle_news_there = mo_news_there()
        mock_handle_transactions_there = mo_transactions_there()
        mock_open.side_effect = [
            mo_injuries_here.return_value, mo_injuries_there.return_value,
            mo_news_here.return_value, mo_news_there.return_value,
            mo_transactions_here.return_value,
            mo_transactions_there.return_value
        ]

        actual = extract_leagues(_then)
        self.assertEqual(actual, _now)

        mock_isfile.assert_has_calls(_leagues_isfile_calls)
        mock_open.assert_has_calls(_leagues_open_calls)
        calls = [mock.call(s + '\n') for s in injuries_now.split('\n') if s]
        mock_handle_injuries_there.write.assert_has_calls(calls)
        mock_handle_news_there.write.assert_not_called()
        mock_handle_transactions_there.write.assert_not_called()
        mock_recreate.assert_called_once_with(_leagues_there)

    @mock.patch('util.news.news.recreate')
    @mock.patch('util.news.news.open', create=True)
    @mock.patch('util.news.news.os.path.isfile')
    def test_leagues__with_then_date_injuries(self, mock_isfile, mock_open,
                                              mock_recreate):
        mock_isfile.return_value = True
        mo_injuries_here = mock.mock_open(read_data=_injuries_then)
        mo_injuries_there = mock.mock_open()
        mo_news_here = mock.mock_open()
        mo_news_there = mock.mock_open()
        mo_transactions_here = mock.mock_open()
        mo_transactions_there = mock.mock_open()
        mock_handle_injuries_there = mo_injuries_there()
        mock_handle_news_there = mo_news_there()
        mock_handle_transactions_there = mo_transactions_there()
        mock_open.side_effect = [
            mo_injuries_here.return_value, mo_injuries_there.return_value,
            mo_news_here.return_value, mo_news_there.return_value,
            mo_transactions_here.return_value,
            mo_transactions_there.return_value
        ]

        actual = extract_leagues(_then)
        self.assertEqual(actual, _then)

        mock_isfile.assert_has_calls(_leagues_isfile_calls)
        mock_open.assert_has_calls(_leagues_open_calls)
        mock_handle_injuries_there.write.assert_not_called()
        mock_handle_news_there.write.assert_not_called()
        mock_handle_transactions_there.write.assert_not_called()
        mock_recreate.assert_called_once_with(_leagues_there)

    @mock.patch('util.news.news.recreate')
    @mock.patch('util.news.news.open', create=True)
    @mock.patch('util.news.news.os.path.isfile')
    def test_leagues__with_now_date_news(self, mock_isfile, mock_open,
                                         mock_recreate):
        mock_isfile.return_value = True
        news_now = '20221016\t<a href=\"../teams/team_42.html\">Houston As' + \
                   'tros</a>: <a href=\"../players/player_39044.html\">Mar' + \
                   'k Appel</a> pitches a 2-hit shutout against the <a hre' + \
                   'f=\"../teams/team_44.html\">Los Angeles Angels</a> wit' + \
                   'h 8 strikeouts and 0 BB allowed!\n20221016\t<a href=\"' + \
                   '../teams/team_39.html\">Colorado Rockies</a>: <a href=' + \
                   '\"../players/player_30965.html\">Spencer Taylor</a> go' + \
                   't suspended 3 games after ejection following a brawl.'
        news = '\n'.join([_news_then, news_now])
        mo_injuries_here = mock.mock_open()
        mo_injuries_there = mock.mock_open()
        mo_news_here = mock.mock_open(read_data=news)
        mo_news_there = mock.mock_open()
        mo_transactions_here = mock.mock_open()
        mo_transactions_there = mock.mock_open()
        mock_handle_injuries_there = mo_injuries_there()
        mock_handle_news_there = mo_news_there()
        mock_handle_transactions_there = mo_transactions_there()
        mock_open.side_effect = [
            mo_injuries_here.return_value, mo_injuries_there.return_value,
            mo_news_here.return_value, mo_news_there.return_value,
            mo_transactions_here.return_value,
            mo_transactions_there.return_value
        ]

        actual = extract_leagues(_then)
        self.assertEqual(actual, _now)

        mock_isfile.assert_has_calls(_leagues_isfile_calls)
        mock_open.assert_has_calls(_leagues_open_calls)
        mock_handle_injuries_there.write.assert_not_called()
        calls = [mock.call(s + '\n') for s in news_now.split('\n') if s]
        mock_handle_news_there.write.assert_has_calls(calls)
        mock_handle_transactions_there.write.assert_not_called()
        mock_recreate.assert_called_once_with(_leagues_there)

    @mock.patch('util.news.news.recreate')
    @mock.patch('util.news.news.open', create=True)
    @mock.patch('util.news.news.os.path.isfile')
    def test_leagues__with_then_date_news(self, mock_isfile, mock_open,
                                          mock_recreate):
        mock_isfile.return_value = True
        mo_injuries_here = mock.mock_open()
        mo_injuries_there = mock.mock_open()
        mo_news_here = mock.mock_open(read_data=_news_then)
        mo_news_there = mock.mock_open()
        mo_transactions_here = mock.mock_open()
        mo_transactions_there = mock.mock_open()
        mock_handle_injuries_there = mo_injuries_there()
        mock_handle_news_there = mo_news_there()
        mock_handle_transactions_there = mo_transactions_there()
        mock_open.side_effect = [
            mo_injuries_here.return_value, mo_injuries_there.return_value,
            mo_news_here.return_value, mo_news_there.return_value,
            mo_transactions_here.return_value,
            mo_transactions_there.return_value
        ]

        actual = extract_leagues(_then)
        self.assertEqual(actual, _then)

        mock_isfile.assert_has_calls(_leagues_isfile_calls)
        mock_open.assert_has_calls(_leagues_open_calls)
        mock_handle_injuries_there.write.assert_not_called()
        mock_handle_news_there.write.assert_not_called()
        mock_handle_transactions_there.write.assert_not_called()
        mock_recreate.assert_called_once_with(_leagues_there)

    @mock.patch('util.news.news.recreate')
    @mock.patch('util.news.news.open', create=True)
    @mock.patch('util.news.news.os.path.isfile')
    def test_leagues__with_now_date_transactions(self, mock_isfile, mock_open,
                                                 mock_recreate):
        mock_isfile.return_value = True
        transactions_now = '20221016\t<a href=\"../teams/team_33.html\">Ba' + \
                           'ltimore Orioles</a>: Placed C <a href=\"../pla' + \
                           'yers/player_1439.html\">Evan Skoug</a> on the ' + \
                           'active roster.\n\n20221016\t<a href=\"../teams' + \
                           '/team_33.html\">Baltimore Orioles</a>: Activat' + \
                           'ed C <a href=\"../players/player_1439.html\">E' + \
                           'van Skoug</a> from the disabled list.\n'
        transactions = '\n'.join([_transactions_then, transactions_now])
        mo_injuries_here = mock.mock_open()
        mo_injuries_there = mock.mock_open()
        mo_news_here = mock.mock_open()
        mo_news_there = mock.mock_open()
        mo_transactions_here = mock.mock_open(read_data=transactions)
        mo_transactions_there = mock.mock_open()
        mock_handle_injuries_there = mo_injuries_there()
        mock_handle_news_there = mo_news_there()
        mock_handle_transactions_there = mo_transactions_there()
        mock_open.side_effect = [
            mo_injuries_here.return_value, mo_injuries_there.return_value,
            mo_news_here.return_value, mo_news_there.return_value,
            mo_transactions_here.return_value,
            mo_transactions_there.return_value
        ]

        actual = extract_leagues(_then)
        self.assertEqual(actual, _now)

        mock_isfile.assert_has_calls(_leagues_isfile_calls)
        mock_open.assert_has_calls(_leagues_open_calls)
        mock_handle_injuries_there.write.assert_not_called()
        mock_handle_news_there.write.assert_not_called()
        calls = [
            mock.call(s + '\n') for s in transactions_now.split('\n') if s
        ]
        mock_handle_transactions_there.write.assert_has_calls(calls)
        mock_recreate.assert_called_once_with(_leagues_there)

    @mock.patch('util.news.news.recreate')
    @mock.patch('util.news.news.open', create=True)
    @mock.patch('util.news.news.os.path.isfile')
    def test_leagues__with_then_date_transactions(self, mock_isfile, mock_open,
                                                  mock_recreate):
        mock_isfile.return_value = True
        mo_injuries_here = mock.mock_open()
        mo_injuries_there = mock.mock_open()
        mo_news_here = mock.mock_open()
        mo_news_there = mock.mock_open()
        mo_transactions_here = mock.mock_open(read_data=_transactions_then)
        mo_transactions_there = mock.mock_open()
        mock_handle_injuries_there = mo_injuries_there()
        mock_handle_news_there = mo_news_there()
        mock_handle_transactions_there = mo_transactions_there()
        mock_open.side_effect = [
            mo_injuries_here.return_value, mo_injuries_there.return_value,
            mo_news_here.return_value, mo_news_there.return_value,
            mo_transactions_here.return_value,
            mo_transactions_there.return_value
        ]

        actual = extract_leagues(_then)
        self.assertEqual(actual, _then)

        mock_isfile.assert_has_calls(_leagues_isfile_calls)
        mock_open.assert_has_calls(_leagues_open_calls)
        mock_handle_injuries_there.write.assert_not_called()
        mock_handle_news_there.write.assert_not_called()
        mock_handle_transactions_there.write.assert_not_called()
        mock_recreate.assert_called_once_with(_leagues_there)


if __name__ == '__main__':
    unittest.main()
