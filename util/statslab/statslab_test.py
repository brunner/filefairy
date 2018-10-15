#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/util/statslab', '', _path))
from util.datetime_.datetime_ import datetime_datetime_pst  # noqa
from util.statslab.statslab import parse_box_score  # noqa
from util.statslab.statslab import parse_game_log  # noqa
from util.statslab.statslab import parse_player  # noqa
from util.team.team import decoding_to_encoding  # noqa

_now = datetime_datetime_pst(2022, 10, 9, 0, 0, 0)
_now_displayed = '10/09/2022'
_now_encoded = '2022-10-09T00:00:00-07:00'

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
                'td>\n\t</tr> ... </html>'
_game_log_sub = '<html> ... <title>{0} @ {1}</title> ... <div style="text-' + \
                'align:center; color:#000000; padding-top:4px;">{2}</div> ' + \
                ' ... <table cellspacing="0" cellpadding="0" class="data" ' + \
                'width="968px">\r\n\t<tr><th colspan="2" class="boxtitle">' + \
                'TOP OF THE 1ST</th></tr>\r\n\t<tr>\r\n\t<th colspan="2" a' + \
                'lign="left" style="padding:4px 0px 4px 4px;">\r\n\t{0} ba' + \
                'tting - Pitching for {1} : RHP <a href="../players/player' + \
                '_101.html">101</a>\r\n\t</th>\r\n\t</tr>\r\n\t<tr>\r\n\t<' + \
                'td valign="top" width="268px" class="dl">\r\n\tPitching: ' + \
                'RHP <a href="../players/player_101.html">101</a>\r\n\t</t' + \
                'd>\r\n\t<td class="dl" width="700px">\r\n\t</td>\r\n\t</t' + \
                'r>\r\n\t<tr>\r\n\t<td valign="top" width="268px" class="d' + \
                'l">\r\n\tBatting: RHB <a href="../players/player_102.html' + \
                '">102</a>\r\n\t</td>\r\n\t<td class="dl" width="700px">\r' + \
                '\n\t0-0: Ball<br>1-0: Fly out, F7  (Flyball, 7LSF)\r\n\t<' + \
                '/td>\r\n\t</tr>\r\n\t<tr>\r\n\t<td valign="top" width="26' + \
                '8px" class="dl">\r\n\tBatting: LHB <a href="../players/pl' + \
                'ayer_103.html">103</a>\r\n\t</td>\r\n\t<td class="dl" wid' + \
                'th="700px">\r\n\t0-0: SINGLE  (Groundball, 56)\r\n\t</td>' + \
                '\r\n\t</tr>\r\n\t<tr>\r\n\t<td valign="top" width="268px"' + \
                ' class="dl">\r\n\tBatting: RHB <a href="../players/player' + \
                '_104.html">104</a>\r\n\t</td>\r\n\t<td class="dl" width="' + \
                '700px">\r\n\t0-0: <b>SINGLE</b>  (Groundball, 6MS) (infie' + \
                'ld hit)<br><a href="../players/player_103.html">103</a> t' + \
                'o second\r\n\t</td>\r\n\t</tr>\r\n\t<tr>\r\n\t<td valign=' + \
                '"top" width="268px" class="dl">\r\n\tBatting: SHB <a href' + \
                '="../players/player_105.html">105</a>\r\n\t</td>\r\n\t<td' + \
                ' class="dl" width="700px">\r\n\t0-0:  Fly out, F9  (Flyba' + \
                'll, 9)\r\n\t</td>\r\n\t</tr>\r\n\t<tr>\r\n\t<td valign="t' + \
                'op" width="268px" class="dl">\r\n\tBatting: LHB <a href="' + \
                '../players/player_106.html">106</a>\r\n\t</td>\r\n\t<td c' + \
                'lass="dl" width="700px">\r\n\t0-0: Swinging Strike<br>0-1' + \
                ': Foul Ball, location: 2F<br>0-2: Strikes out  swinging\r' + \
                '\n\t</td>\r\n\t</tr>\r\n\t<tr>\r\n\t<td class="datathbg" ' + \
                'colspan="2">Top of the 1st over -  0 run(s), 1 hit(s), 0 ' + \
                'error(s), 2 left on base; {3} 0 - {4} 0</td>\r\n\t</tr>\r' + \
                '\n\t</table> ... </html>'
_player_sub = '<html> ... <title>Player Report for #{0}  {1}</title> ... <' + \
              'div class="repsubtitle"><a class="boxlink" style="font-weig' + \
              'ht:bold; font-size:18px; color:#FFFFFF;" href="../teams/tea' + \
              'm_{2}.html">{3}</a></div> ... </html>'
_player_empty_sub = '<html><title>Player Report for #{0}  {1}</title></html>'

_html = 'https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/'
_game_box = 'box_scores/game_box_{}.html'
_game_log = 'game_logs/log_{}.html'
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


def _log(id_, ateam, date, hteam, player, plays):
    return {
        'id': id_,
        'away_team': decoding_to_encoding(ateam),
        'home_team': decoding_to_encoding(hteam),
        'date': date,
        'player': player,
        'plays': plays,
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
            'MLB', 'Arizona Diamondbacks',
            'Los Angeles Dodgers', _now_displayed,
            _record_sub.format('Arizona Diamondbacks', '76-86'), 4,
            _record_sub.format('Los Angeles Dodgers', '97-65'), 2)
        mo = mock.mock_open(read_data=content)
        mock_handle = mo()
        mock_open.side_effect = [mo.return_value]

        link = _path + _game_box.format('2998')
        actual = parse_box_score(link)
        expected = _box('76-86', 4, 'Arizona Diamondbacks', _now, '97-65', 2,
                        'Los Angeles Dodgers')
        self.assertEqual(actual, expected)

        mock_isfile.assert_called_once_with(link)
        mock_handle.assert_not_called()
        mock_open.assert_called_once_with(link, 'r', encoding='iso-8859-1')

    @mock.patch('util.statslab.statslab.urlopen')
    def test_box_score__with_valid_link(self, mock_urlopen):
        content = _game_box_sub.format(
            'MLB', 'Arizona Diamondbacks',
            'Los Angeles Dodgers', _now_displayed,
            _record_sub.format('Arizona Diamondbacks', '76-86'), 4,
            _record_sub.format('Los Angeles Dodgers', '97-65'), 2)
        mock_urlopen.return_value = bytes(content, 'utf-8')

        link = _html + _game_box.format('2998')
        actual = parse_box_score(link)
        expected = _box('76-86', 4, 'Arizona Diamondbacks', _now, '97-65', 2,
                        'Los Angeles Dodgers')
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(link)

    @mock.patch('util.statslab.statslab.urlopen')
    def test_box_score__with_invalid_title(self, mock_urlopen):
        content = _game_box_sub.format(
            'NPB', 'Yokohama DeNA BayStars', 'Tokyo Yakult Swallows',
            _now_displayed,
            _record_sub.format('Yokohama DeNA BayStars', '76-86'), 4,
            _record_sub.format('Tokyo Yakult Swallows', '97-65'), 2)
        mock_urlopen.return_value = bytes(content, 'utf-8')

        link = _html + _game_box.format('2998')
        actual = parse_box_score(link)
        expected = {'ok': False, 'error': 'invalid_title'}
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(link)

    @mock.patch('util.statslab.statslab.urlopen')
    def test_box_score__with_invalid_line(self, mock_urlopen):
        content = _game_box_sub.format(
            'MLB', 'Arizona Diamondbacks', 'Los Angeles Dodgers',
            _now_displayed,
            _record_sub.format('Yokohama DeNA BayStars', '76-86'), 4,
            _record_sub.format('Tokyo Yakult Swallows', '97-65'), 2)
        mock_urlopen.return_value = bytes(content, 'utf-8')

        link = _html + _game_box.format('2998')
        actual = parse_box_score(link)
        expected = {'ok': False, 'error': 'invalid_line'}
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(link)

    maxDiff = None

    @mock.patch('util.statslab.statslab.urlopen')
    def test_game_log__with_valid_link(self, mock_urlopen):
        content = _game_log_sub.format('Arizona Diamondbacks',
                                       'Los Angeles Dodgers', _now_displayed,
                                       'Arizona', 'Los Angeles')
        mock_urlopen.return_value = bytes(content, 'utf-8')

        link = _html + _game_log.format('2998')
        actual = parse_game_log(link)
        player = {
            'P101': '101',
            'P102': '102',
            'P103': '103',
            'P104': '104',
            'P105': '105',
            'P106': '106'
        }
        plays = [[{
            'label':
            'Top 1st',
            'batting':
            'T31',
            'pitching':
            'RHP P101',
            'footer':
            '0 run(s), 1 hit(s), 0 error(s), 2 left on base; T31 0 - T45 0',
            'play': [{
                'type': 'sub',
                'subtype': 'pitching',
                'value': 'P101'
            }, {
                'type': 'sub',
                'subtype': 'batting',
                'value': 'P102'
            }, {
                'type': 'event',
                'sequence': ['0-0: Ball', '1-0: In play'],
                'value': 'P102 fly out, F7 (Flyball, 7LSF).'
            }, {
                'type': 'sub',
                'subtype': 'batting',
                'value': 'P103'
            }, {
                'type': 'event',
                'sequence': ['0-0: In play'],
                'value': 'P103 single (Groundball, 56).'
            }, {
                'type': 'sub',
                'subtype': 'batting',
                'value': 'P104'
            }, {
                'type':
                'event',
                'sequence': ['0-0: In play'],
                'value':
                'P104 single (Groundball, 6MS) (infield hit). P103 '
                'to second.'
            }, {
                'type': 'sub',
                'subtype': 'batting',
                'value': 'P105'
            }, {
                'type': 'event',
                'sequence': ['0-0: In play'],
                'value': 'P105 fly out, F9 (Flyball, 9).'
            }, {
                'type': 'sub',
                'subtype': 'batting',
                'value': 'P106'
            }, {
                'type':
                'event',
                'sequence': [
                    '0-0: Swinging Strike', '0-1: Foul',
                    '0-2: Swinging Strike'
                ],
                'value':
                'P106 strikes out swinging.'
            }]
        }]]
        expected = _log('2998', 'Arizona Diamondbacks', _now_encoded,
                        'Los Angeles Dodgers', player, plays)
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(link)

    @mock.patch('util.statslab.statslab.urlopen')
    def test_player__with_valid_link(self, mock_urlopen):
        content = _player_sub.format(73, 'Dakota Donovan', '44',
                                     'Los Angeles Angels')
        mock_urlopen.return_value = bytes(content, 'utf-8')

        link = _html + _player.format('29663')
        actual = parse_player(link)
        expected = _play('Dakota Donovan', 'T44')
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(link)

    @mock.patch('util.statslab.statslab.urlopen')
    def test_player__with_invalid_team(self, mock_urlopen):
        content = _player_empty_sub.format(73, 'Dakota Donovan')
        mock_urlopen.return_value = bytes(content, 'utf-8')

        link = _html + _player.format('29663')
        actual = parse_player(link)
        expected = {'ok': False, 'error': 'invalid_team'}
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(link)


if __name__ == '__main__':
    unittest.main()
