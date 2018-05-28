#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/util/statslab', '', _path))
from util.statslab.statslab import box_score  # noqa
from util.statslab.statslab import player  # noqa
from util.team.team import decoding_to_encoding  # noqa

_html = 'https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/'
_game_box = 'box_scores/game_box_{}.html'
_player = 'players/player_{}.html'

GAME_BOX_FILE = _path + _game_box.format('2998')
GAME_BOX_LINK = _html + _game_box.format('2998')
PLAYER_LINK = _html + _player.format('29663')
INVALID_TITLE = {'ok': False, 'error': 'invalid_title'}
INVALID_LINE = {'ok': False, 'error': 'invalid_line'}
INVALID_TEAM = {'ok': False, 'error': 'invalid_team'}
DATE = datetime.datetime(2022, 10, 9, 0, 0, 0)
FDATE = '10/09/2022'
MLB = 'MLB'
NPB = 'NPB'
RECORD = '{} ({})'
RECORD1 = '76-86'
RECORD2 = '97-65'
RUNS1 = 4
RUNS2 = 2
TEAM1 = 'Arizona Diamondbacks'
TEAM2 = 'Los Angeles Dodgers'
TEAM3 = 'Los Angeles Angels'
TEAM4 = 'Yokohama DeNA BayStars'
TEAM5 = 'Tokyo Yakult Swallows'
NUMBER = 73
NAME = 'Dakota Donovan'
TEAM = '44'
TEAM_ENCODED = 'T44'
TEAM_DECODED = 'Los Angeles Angels'

GAME_BOX = '<html> ... <title>{0} Box Scores, {1} at {2}, {3}</title> ... ' + \
           '<tr style="background-color:#FFFFFE;">\n\t<td class="dl"><b>' + \
           '{4}</b></td>\n\t<td class="dc">0</td>\n<td class="dc">0</td>' + \
           '\n<td class="dc">0</td>\n<td class="dc">2</td>\n<td ' + \
           'class="dc">2</td>\n<td class="dc">0</td>\n<td class="dc">0' + \
           '</td>\n<td class="dc">0</td>\n<td class="dc">0</td>\n\t<td ' + \
           'class="dc"><b>{5}</b></td>\n\t<td class="dc"><b>10</b></td>\n' + \
           '\t<td class="dc"><b>0</b></td>\n\t</tr>\n\t<tr ' + \
           'style="background-color:#FFFFFE;">\n\t<td class="dl">{6}</td>' + \
           '\n\t<td class="dc">0</td>\n<td class="dc">1</td>\n<td class=' + \
           '"dc">0</td>\n<td class="dc">0</td>\n<td class="dc">0</td>\n' + \
           '<td class="dc">0</td>\n<td class="dc">1</td>\n<td class="dc">' + \
           '0</td>\n<td class="dc">0</td>\n\t<td class="dc"><b>{7}</b>' + \
           '</td>\n\t<td class="dc"><b>9</b></td>\n\t<td class="dc"><b>0' + \
           '</b></td>\n\t</tr>\n\t</table>\n\t</td>\n\t</tr> ... </html'
PLAYER = '<html> ... <title>Player Report for #{0}  {1}</title> ... <div ' + \
         'class="repsubtitle"><a class="boxlink" style="font-weight:bold; ' + \
         'font-size:18px; color:#FFFFFF;" href="../teams/team_{2}.html">' + \
         '{3}</a></div> ... </html'
PLAYER_EMPTY = '<html><title>Player Report for #{0}  {1}</title></html>'


def _box(arecord, aruns, ateam, date, hrecord, hruns, hteam):
    return {
        'away_record': arecord,
        'away_runs': aruns,
        'away_team': decoding_to_encoding(ateam),
        'date': date,
        'home_record': hrecord,
        'home_runs': hruns,
        'home_team': decoding_to_encoding(hteam),
        'ok': True
    }


def _play(name, team):
    return {'name': name, 'ok': True, 'team': team}


class StatslabTest(unittest.TestCase):
    @mock.patch('util.statslab.statslab.open', create=True)
    @mock.patch('util.statslab.statslab.os.path.isfile')
    def test_box_score__with_valid_file(self, mock_isfile, mock_open):
        mock_isfile.return_value = True
        content = GAME_BOX.format(MLB, TEAM1, TEAM2, FDATE,
                                  RECORD.format(TEAM1, RECORD1), RUNS1,
                                  RECORD.format(TEAM2, RECORD2), RUNS2)
        mo = mock.mock_open(read_data=content)
        mock_handle = mo()
        mock_open.side_effect = [mo.return_value]

        actual = box_score(GAME_BOX_FILE)
        expected = _box(RECORD1, RUNS1, TEAM1, DATE, RECORD2, RUNS2, TEAM2)
        self.assertEqual(actual, expected)

        mock_isfile.assert_called_once_with(GAME_BOX_FILE)
        mock_handle.assert_not_called()
        mock_open.assert_called_once_with(
            GAME_BOX_FILE, 'r', encoding='iso-8859-1')

    @mock.patch('util.statslab.statslab.urlopen')
    def test_box_score__with_valid_link(self, mock_urlopen):
        content = GAME_BOX.format(MLB, TEAM1, TEAM2, FDATE,
                                  RECORD.format(TEAM1, RECORD1), RUNS1,
                                  RECORD.format(TEAM2, RECORD2), RUNS2)
        mock_urlopen.return_value = bytes(content, 'utf-8')

        actual = box_score(GAME_BOX_LINK)
        expected = _box(RECORD1, RUNS1, TEAM1, DATE, RECORD2, RUNS2, TEAM2)
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(GAME_BOX_LINK)

    @mock.patch('util.statslab.statslab.urlopen')
    def test_box_score__with_invalid_title(self, mock_urlopen):
        content = GAME_BOX.format(NPB, TEAM4, TEAM5, FDATE,
                                  RECORD.format(TEAM4, RECORD1), RUNS1,
                                  RECORD.format(TEAM5, RECORD2), RUNS2)
        mock_urlopen.return_value = bytes(content, 'utf-8')

        actual = box_score(GAME_BOX_LINK)
        expected = INVALID_TITLE
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(GAME_BOX_LINK)

    @mock.patch('util.statslab.statslab.urlopen')
    def test_box_score__with_invalid_line(self, mock_urlopen):
        content = GAME_BOX.format(MLB, TEAM1, TEAM2, FDATE,
                                  RECORD.format(TEAM4, RECORD1), RUNS1,
                                  RECORD.format(TEAM5, RECORD2), RUNS2)
        mock_urlopen.return_value = bytes(content, 'utf-8')

        actual = box_score(GAME_BOX_LINK)
        expected = INVALID_LINE
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(GAME_BOX_LINK)

    @mock.patch('util.statslab.statslab.urlopen')
    def test_player__with_valid_link(self, mock_urlopen):
        content = PLAYER.format(NUMBER, NAME, TEAM, TEAM_DECODED)
        mock_urlopen.return_value = bytes(content, 'utf-8')

        actual = player(PLAYER_LINK)
        expected = _play(NAME, TEAM_ENCODED)
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(PLAYER_LINK)

    @mock.patch('util.statslab.statslab.urlopen')
    def test_player__with_invalid_team(self, mock_urlopen):
        content = PLAYER_EMPTY.format(NUMBER, NAME)
        mock_urlopen.return_value = bytes(content, 'utf-8')

        actual = player(PLAYER_LINK)
        expected = INVALID_TEAM
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(PLAYER_LINK)


if __name__ == '__main__':
    unittest.main()
