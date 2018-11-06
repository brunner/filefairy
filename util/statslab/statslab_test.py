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
from util.statslab.statslab import parse_game_data  # noqa
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
                'td>\n\t</tr> ... <th width="30" class="hsn dc">RBI</th></' + \
                'tr> ... <tr><td class="dl"><a href="../players/player_102' + \
                '.html">J. Alpha</a> SS</td> ... <td class="dl"><a href=".' + \
                './players/player_103.html">J. Beta</a> 1B</td> ... <td cl' + \
                'ass="dl"><a href="../players/player_104.html">J. Charlie<' + \
                '/a> CF, LF</td> ... <td class="dl"><a href="../players/pl' + \
                'ayer_105.html">J. Delta</a> C</td> ... <td class="dl"><a ' + \
                'href="../players/player_106.html">J. Echo</a> 2B</td> ...' + \
                ' <td class="dl">&#160;&#160; <a href="../players/player_1' + \
                '07.html">J. Foxtrot</a> PH, 2B</td> ... </table> ... <th ' + \
                'width="30" class="hsn dc">ERA</th></tr> ... <tr><td class' + \
                '="dl"><a href="../players/player_108.html">J. Whiskey</a>' + \
                '</td> ... <tr><td class="dl"><a href="../players/player_1' + \
                '09.html">J. Victor</a></td> ... </table> ... <th width="3' + \
                '0" class="hsn dc">ERA</th></tr> ... <tr><td class="dl"><a' + \
                ' href="../players/player_101.html">J. Unknown</a></td> ..' + \
                '. </table> ... </html>'
_game_log_sub = '<html> ... <title>{0} @ {1}</title> ... <div style="text-' + \
                'align:center; color:#000000; padding-top:4px;">{2}</div> ' + \
                ' ... <table cellspacing="0" cellpadding="0" class="data" ' + \
                'width="968px">\r\n\t<tr><th colspan="2" class="boxtitle">' + \
                'TOP OF THE 1ST</th></tr>\r\n\t<tr>\r\n\t<th colspan="2" a' + \
                'lign="left" style="padding:4px 0px 4px 4px;">\r\n\t{0} ba' + \
                'tting - Pitching for {1} : RHP <a href="../players/player' + \
                '_101.html">Jim Unknown</a>\r\n\t</th>\r\n\t</tr>\r\n\t<tr' + \
                '>\r\n\t<td valign="top" width="268px" class="dl">\r\n\tPi' + \
                'tching: RHP <a href="../players/player_101.html">101</a>' + \
                '\r\n\t</td>\r\n\t<td class="dl" width="700px">\r\n\t</td>' + \
                '\r\n\t</tr>\r\n\t<tr>\r\n\t<td valign="top" width="268px"' + \
                ' class="dl">\r\n\tBatting: RHB <a href="../players/player' + \
                '_102.html">Jim Alpha</a>\r\n\t</td>\r\n\t<td class="dl" w' + \
                'idth="700px">\r\n\t0-0: Ball<br>1-0: Fly out, F7  (Flybal' + \
                'l, 7LSF)\r\n\t</td>\r\n\t</tr>\r\n\t<tr>\r\n\t<td valign=' + \
                '"top" width="268px" class="dl">\r\n\tBatting: LHB <a href' + \
                '="../players/player_103.html">Jim Beta</a>\r\n\t</td>\r\n' + \
                '\t<td class="dl" width="700px">\r\n\t0-0: SINGLE  (Ground' + \
                'ball, 56)\r\n\t</td>\r\n\t</tr>\r\n\t<tr>\r\n\t<td valign' + \
                '="top" width="268px" class="dl">\r\n\tBatting: RHB <a hre' + \
                'f="../players/player_104.html">Jim Charlie</a>\r\n\t</td>' + \
                '\r\n\t<td class="dl" width="700px">\r\n\t0-0: <b>SINGLE</' + \
                'b>  (Groundball, 6MS) (infield hit)<br><a href="../player' + \
                's/player_103.html">Jim Beta</a> to second\r\n\t</td>\r\n' + \
                '\t</tr>\r\n\t<tr>\r\n\t<td valign="top" width="268px" cla' + \
                'ss="dl">\r\n\tBatting: SHB <a href="../players/player_105' + \
                '.html">Jim Delta</a>\r\n\t</td>\r\n\t<td class="dl" width' + \
                '="700px">\r\n\t0-0:  Fly out, F9  (Flyball, 9)\r\n\t</td>' + \
                '\r\n\t</tr>\r\n\t<tr>\r\n\t<td valign="top" width="268px"' + \
                ' class="dl">\r\n\tBatting: LHB <a href="../players/player' + \
                '_106.html">Jim Echo</a>\r\n\t</td>\r\n\t<td class="dl" wi' + \
                'dth="700px">\r\n\t0-0: Swinging Strike<br>0-1: Foul Ball,' + \
                ' location: 2F<br>0-2: Strikes out  swinging\r\n\t</td>\r' + \
                '\n\t</tr>\r\n\t<tr>\r\n\t<td class="datathbg" colspan="2"' + \
                '>Top of the 1st over -  0 run(s), 1 hit(s), 0 error(s), 2' + \
                ' left on base; {3} 0 - {4} 0</td>\r\n\t</tr>\r\n\t</table' + \
                '> ... </html>'
_player_sub = '<html> ... <title>Player Report for #{0}  {1}</title> ... <' + \
              'div class="repsubtitle"><a class="boxlink" style="font-weig' + \
              'ht:bold; font-size:18px; color:#FFFFFF;" href="../teams/tea' + \
              'm_{2}.html">{3}</a></div><div style="text-align:center;font' + \
              '-weight:bold; font-size:18px; color:#FFFFFF;">\r\n\tAge: 21' + \
              ' | \r\n\tBats: R |\r\n\tThrows: R |\r\n\tMorale: Normal  \r' + \
              '\n\t&nbsp;&nbsp;&nbsp;\r\n\t</div> ... </html>'
_player_empty_sub = '<html><title>Player Report for #{0}  {1}</title></html>'

_html = 'https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/'
_game_box = 'box_scores/game_box_{}.html'
_game_log = 'game_logs/log_{}.html'
_player = 'players/player_{}.html'

_players = ['101', '102', '103', '104', '105', '106', '107', '108', '109']
_plays = [[{
    'label':
    'Top 1st',
    'batting':
    'T31',
    'pitching':
    'P101',
    'footer':
    '0 run(s), 1 hit(s), 0 error(s), 2 left on base; T31 0 - T45 0',
    'play': [{
        'type': 'sub',
        'subtype': 'P',
        'value': 'P101'
    }, {
        'type': 'sub',
        'subtype': 'B',
        'value': 'P102'
    }, {
        'type': 'event',
        'outs': 1,
        'runs': 0,
        'sequence': ['1 1 0 Ball', '2 1 0 In play, out(s)'],
        'value': 'P102 flies out to left fielder  (zone 7LSF).',
    }, {
        'type': 'sub',
        'subtype': 'B',
        'value': 'P103'
    }, {
        'type': 'event',
        'outs': 0,
        'runs': 0,
        'sequence': ['1 0 0 In play, no out'],
        'value': 'P103 singles on a ground ball to left fielder  (zone 56).'
    }, {
        'type': 'sub',
        'subtype': 'B',
        'value': 'P104'
    }, {
        'type':
        'event',
        'outs':
        0,
        'runs':
        0,
        'sequence': ['1 0 0 In play, no out'],
        'value':
        'P104 singles on a ground ball to shortstop  (infield hit) '
        '(zone 6MS). P103 to second.'
    }, {
        'type': 'sub',
        'subtype': 'B',
        'value': 'P105'
    }, {
        'type': 'event',
        'outs': 1,
        'runs': 0,
        'sequence': ['1 0 0 In play, out(s)'],
        'value': 'P105 flies out to right fielder  (zone 9).'
    }, {
        'type': 'sub',
        'subtype': 'B',
        'value': 'P106'
    }, {
        'type':
        'event',
        'outs':
        1,
        'runs':
        0,
        'sequence':
        ['1 0 1 Swinging Strike', '2 0 2 Foul', '3 0 3 Swinging Strike'],
        'value':
        'P106 strikes out swinging.'
    }]
}]]


def _data(id_, arecord, aruns, ateam, date, hrecord, hruns, hteam, players,
          plays):
    return {
        'id': id_,
        'away_record': arecord,
        'away_runs': aruns,
        'away_team': decoding_to_encoding(ateam),
        'date': date,
        'home_record': hrecord,
        'home_runs': hruns,
        'home_team': decoding_to_encoding(hteam),
        'players': players,
        'plays': plays,
        'ok': True
    }


def _play(bats, name, number, team, throws):
    return {
        'ok': True,
        'bats': bats,
        'name': name,
        'number': number,
        'team': team,
        'throws': throws
    }


class StatslabTest(unittest.TestCase):
    maxDiff = None

    @mock.patch('util.statslab.statslab.urlopen')
    @mock.patch('util.statslab.statslab.open', create=True)
    @mock.patch('util.statslab.statslab.os.path.isfile')
    def test_game_data__with_valid_box_file(self, mock_isfile, mock_open,
                                            mock_urlopen):
        mock_isfile.return_value = True
        box_content = _game_box_sub.format(
            'MLB', 'Arizona Diamondbacks',
            'Los Angeles Dodgers', _now_displayed,
            _record_sub.format('Arizona Diamondbacks', '76-86'), 4,
            _record_sub.format('Los Angeles Dodgers', '97-65'), 2)
        mo = mock.mock_open(read_data=box_content)
        mock_handle = mo()
        mock_open.side_effect = [mo.return_value]
        log_content = _game_log_sub.format(
            'Arizona Diamondbacks', 'Los Angeles Dodgers', _now_displayed,
            'Arizona', 'Los Angeles')
        mock_urlopen.return_value = bytes(log_content, 'utf-8')

        box_link = _path + _game_box.format('2998')
        log_link = _html + _game_log.format('2998')
        actual = parse_game_data(box_link, log_link)
        expected = _data('2998', '76-86', 4, 'Arizona Diamondbacks',
                         _now_encoded, '97-65', 2, 'Los Angeles Dodgers',
                         _players, _plays)
        self.assertEqual(actual, expected)

        mock_isfile.assert_called_once_with(box_link)
        mock_handle.assert_not_called()
        mock_open.assert_called_once_with(box_link, 'r', encoding='iso-8859-1')
        mock_urlopen.assert_called_once_with(log_link)

    @mock.patch('util.statslab.statslab.urlopen')
    @mock.patch('util.statslab.statslab.open', create=True)
    @mock.patch('util.statslab.statslab.os.path.isfile')
    def test_game_data__with_valid_box_link(self, mock_isfile, mock_open,
                                            mock_urlopen):
        box_content = _game_box_sub.format(
            'MLB', 'Arizona Diamondbacks',
            'Los Angeles Dodgers', _now_displayed,
            _record_sub.format('Arizona Diamondbacks', '76-86'), 4,
            _record_sub.format('Los Angeles Dodgers', '97-65'), 2)
        log_content = _game_log_sub.format(
            'Arizona Diamondbacks', 'Los Angeles Dodgers', _now_displayed,
            'Arizona', 'Los Angeles')
        mock_urlopen.side_effect = [
            bytes(box_content, 'utf-8'),
            bytes(log_content, 'utf-8')
        ]

        box_link = _html + _game_box.format('2998')
        log_link = _html + _game_log.format('2998')
        actual = parse_game_data(box_link, log_link)
        expected = _data('2998', '76-86', 4, 'Arizona Diamondbacks',
                         _now_encoded, '97-65', 2, 'Los Angeles Dodgers',
                         _players, _plays)
        self.assertEqual(actual, expected)

        mock_isfile.assert_not_called()
        mock_open.assert_not_called()
        mock_urlopen.assert_has_calls(
            [mock.call(box_link), mock.call(log_link)])

    @mock.patch('util.statslab.statslab.urlopen')
    @mock.patch('util.statslab.statslab.open', create=True)
    @mock.patch('util.statslab.statslab.os.path.isfile')
    def test_game_data__with_invalid_title(self, mock_isfile, mock_open,
                                           mock_urlopen):
        box_content = _game_box_sub.format(
            'NPB', 'Yokohama DeNA BayStars', 'Tokyo Yakult Swallows',
            _now_displayed,
            _record_sub.format('Yokohama DeNA BayStars', '76-86'), 4,
            _record_sub.format('Tokyo Yakult Swallows', '97-65'), 2)
        log_content = _game_log_sub.format(
            'Arizona Diamondbacks', 'Los Angeles Dodgers', _now_displayed,
            'Arizona', 'Los Angeles')
        mock_urlopen.side_effect = [
            bytes(box_content, 'utf-8'),
            bytes(log_content, 'utf-8')
        ]

        box_link = _html + _game_box.format('2998')
        log_link = _html + _game_log.format('2998')
        actual = parse_game_data(box_link, log_link)
        expected = {'ok': False, 'id': '2998', 'error': 'invalid_title'}
        self.assertEqual(actual, expected)

        mock_isfile.assert_not_called()
        mock_open.assert_not_called()
        mock_urlopen.assert_called_once_with(box_link)

    @mock.patch('util.statslab.statslab.urlopen')
    @mock.patch('util.statslab.statslab.open', create=True)
    @mock.patch('util.statslab.statslab.os.path.isfile')
    def test_game_data__with_invalid_line(self, mock_isfile, mock_open,
                                          mock_urlopen):
        box_content = _game_box_sub.format(
            'MLB', 'Arizona Diamondbacks', 'Los Angeles Dodgers',
            _now_displayed,
            _record_sub.format('Yokohama DeNA BayStars', '76-86'), 4,
            _record_sub.format('Tokyo Yakult Swallows', '97-65'), 2)
        log_content = _game_log_sub.format(
            'Arizona Diamondbacks', 'Los Angeles Dodgers', _now_displayed,
            'Arizona', 'Los Angeles')
        mock_urlopen.side_effect = [
            bytes(box_content, 'utf-8'),
            bytes(log_content, 'utf-8')
        ]

        box_link = _html + _game_box.format('2998')
        log_link = _html + _game_log.format('2998')
        actual = parse_game_data(box_link, log_link)
        expected = {'ok': False, 'id': '2998', 'error': 'invalid_line'}
        self.assertEqual(actual, expected)

        mock_isfile.assert_not_called()
        mock_open.assert_not_called()
        mock_urlopen.assert_called_once_with(box_link)

    @mock.patch('util.statslab.statslab.urlopen')
    def test_player__with_valid_link(self, mock_urlopen):
        player_content = _player_sub.format(73, 'Dakota Donovan', '44',
                                            'Los Angeles Angels')
        mock_urlopen.return_value = bytes(player_content, 'utf-8')

        link = _html + _player.format('29663')
        actual = parse_player(link)
        expected = _play('R', 'Dakota Donovan', '73', 'T44', 'R')
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(link)


if __name__ == '__main__':
    unittest.main()
