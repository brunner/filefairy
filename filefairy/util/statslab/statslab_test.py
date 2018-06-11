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

_now = datetime.datetime(2022, 10, 9, 0, 0, 0)
_now_encoded = '10/09/2022'

_record_sub = '{} ({})'
_game_box_sub = '<html> ... <title>{0} Box Scores, {1} at {2}, {3}</title>' + \
                ' ... <tr style="background-color:#FFFFFE;">\n\t<td class=' + \
                '"dl"><b>{4}</b></td>\n\t<td class="dc">0</td>\n<td class=' + \
                '"dc">0</td>\n<td class="dc">0</td>\n<td class="dc">2</td>' + \
                '\n<td class="dc">2</td>\n<td class="dc">0</td>\n<td class' + \
                '="dc">0</td>\n<td class="dc">0</td>\n<td class="dc">0</td' + \
                '>\n\t<td class="dc"><b>{5}</b></td>\n\t<td class="dc"><b>' + \
                '10</b></td>\n\t<td class="dc"><b>0</b></td>\n\t</tr>\n\t<' + \
                'tr style="background-color:#FFFFFE;">\n\t<td class="dl">{' + \
                '6}</td>\n\t<td class="dc">0</td>\n<td class="dc">1</td>\n' + \
                '<td class="dc">0</td>\n<td class="dc">0</td>\n<td class="' + \
                'dc">0</td>\n<td class="dc">0</td>\n<td  class="dc">1</td>' + \
                '\n<td class="dc">0</td>\n<td class="dc">0</td>\n\t<td cla' + \
                'ss="dc"><b>{7}</b></td>\n\t<td class="dc"><b>9</b></td>\n' + \
                '\t<td class="dc"><b>0</b></td>\n\t</tr>\n\t</table>\n\t</' + \
                'td>\n\t</tr> ... </html'
_player_sub = '<html> ... <title>Player Report for #{0}  {1}</title> ... <' + \
              'div class="repsubtitle"><a class="boxlink" style="font-weig' + \
              'ht:bold; font-size:18px; color:#FFFFFF;" href="../teams/tea' + \
              'm_{2}.html">{3}</a></div> ... </html'
_player_empty_sub = '<html><title>Player Report for #{0}  {1}</title></html>'

_html = 'https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/'
_game_box = 'box_scores/game_box_{}.html'
_player = 'players/player_{}.html'


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
        content = _game_box_sub.format(
            'MLB', 'Arizona Diamondbacks', 'Los Angeles Dodgers', _now_encoded,
            _record_sub.format('Arizona Diamondbacks', '76-86'), 4,
            _record_sub.format('Los Angeles Dodgers', '97-65'), 2)
        mo = mock.mock_open(read_data=content)
        mock_handle = mo()
        mock_open.side_effect = [mo.return_value]

        link = _path + _game_box.format('2998')
        actual = box_score(link)
        expected = _box('76-86', 4, 'Arizona Diamondbacks', _now, '97-65', 2,
                        'Los Angeles Dodgers')
        self.assertEqual(actual, expected)

        mock_isfile.assert_called_once_with(link)
        mock_handle.assert_not_called()
        mock_open.assert_called_once_with(link, 'r', encoding='iso-8859-1')

    @mock.patch('util.statslab.statslab.urlopen')
    def test_box_score__with_valid_link(self, mock_urlopen):
        content = _game_box_sub.format(
            'MLB', 'Arizona Diamondbacks', 'Los Angeles Dodgers', _now_encoded,
            _record_sub.format('Arizona Diamondbacks', '76-86'), 4,
            _record_sub.format('Los Angeles Dodgers', '97-65'), 2)
        mock_urlopen.return_value = bytes(content, 'utf-8')

        link = _html + _game_box.format('2998')
        actual = box_score(link)
        expected = _box('76-86', 4, 'Arizona Diamondbacks', _now, '97-65', 2,
                        'Los Angeles Dodgers')
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(link)

    @mock.patch('util.statslab.statslab.urlopen')
    def test_box_score__with_invalid_title(self, mock_urlopen):
        content = _game_box_sub.format(
            'NPB', 'Yokohama DeNA BayStars',
            'Tokyo Yakult Swallows', _now_encoded,
            _record_sub.format('Yokohama DeNA BayStars', '76-86'), 4,
            _record_sub.format('Tokyo Yakult Swallows', '97-65'), 2)
        mock_urlopen.return_value = bytes(content, 'utf-8')

        link = _html + _game_box.format('2998')
        actual = box_score(link)
        expected = {'ok': False, 'error': 'invalid_title'}
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(link)

    @mock.patch('util.statslab.statslab.urlopen')
    def test_box_score__with_invalid_line(self, mock_urlopen):
        content = _game_box_sub.format(
            'MLB', 'Arizona Diamondbacks', 'Los Angeles Dodgers', _now_encoded,
            _record_sub.format('Yokohama DeNA BayStars', '76-86'), 4,
            _record_sub.format('Tokyo Yakult Swallows', '97-65'), 2)
        mock_urlopen.return_value = bytes(content, 'utf-8')

        link = _html + _game_box.format('2998')
        actual = box_score(link)
        expected = {'ok': False, 'error': 'invalid_line'}
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(link)

    @mock.patch('util.statslab.statslab.urlopen')
    def test_player__with_valid_link(self, mock_urlopen):
        content = _player_sub.format(73, 'Dakota Donovan',
                                     '44', 'Los Angeles Angels')
        mock_urlopen.return_value = bytes(content, 'utf-8')

        link = _html + _player.format('29663')
        actual = player(link)
        expected = _play('Dakota Donovan', 'T44')
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(link)

    @mock.patch('util.statslab.statslab.urlopen')
    def test_player__with_invalid_team(self, mock_urlopen):
        content = _player_empty_sub.format(73, 'Dakota Donovan')
        mock_urlopen.return_value = bytes(content, 'utf-8')

        link = _html + _player.format('29663')
        actual = player(link)
        expected = {'ok': False, 'error': 'invalid_team'}
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(link)


if __name__ == '__main__':
    unittest.main()
