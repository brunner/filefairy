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
_game_box_sub = """<html> ...
<title>{0} Box Scores, {1} at {2}, {3}</title> ...
<tr style="background-color:#FFFFFE;">
\t<td class="dl"><b>{4}</b></td>
\t<td class="dc">0</td>
<td class="dc">0</td>
<td class="dc">0</td>
<td class="dc">2</td>
<td class="dc">2</td>
<td class="dc">0</td>
<td class="dc">0</td>
<td class="dc">0</td>
<td class="dc">0</td>
\t<td class="dc"><b>{5}</b></td>
\t<td class="dc"><b>10</b></td>
\t<td class="dc"><b>0</b></td>
\t</tr>\n\t<tr style="background-color:#FFFFFE;">
\t<td class="dl">{6}</td>
\t<td class="dc">0</td>
<td class="dc">1</td>
<td class="dc">0</td>
<td class="dc">0</td>
<td class="dc">0</td>
<td class="dc">0</td>
<td  class="dc">1</td>
<td class="dc">0</td>
<td class="dc">0</td>
\t<td class="dc"><b>{7}</b></td>
\t<td class="dc"><b>9</b></td>
\t<td class="dc"><b>0</b></td>
\t</tr>
\t</table>
\t</td>
\t</tr> ...
<th width="30" class="hsn dc">RBI</th></tr>
<tr><td class="dl"><a href="../players/player_102.html">J. Alpha</a> SS</td>
<td class="dl"><a href="../players/player_103.html">J. Beta</a> 1B</td>
<td class="dl"><a href="../players/player_104.html">J. Charlie</a> CF, LF</td>
<td class="dl"><a href="../players/player_105.html">J. Delta</a> C</td>
<td class="dl"><a href="../players/player_106.html">J. Echo</a> 2B</td>
<td class="dl">&#160;&#160; <a href="../players/player_107.html">J. Foxtrot</a> PH, 2B</td>
</table> ...
<th width="30" class="hsn dc">RBI</th></tr>
<tr><td class="dl"><a href="../players/player_110.html">J. Golf</a> RF</td>
<td class="dl"><a href="../players/player_111.html">J. Juliet</a> LF</td>
<td class="dl"><a href="../players/player_112.html">J. Kilo</a> SS</td>
</table> ...
<th width="30" class="hsn dc">ERA</th></tr>
<tr><td class="dl"><a href="../players/player_108.html">J. Whiskey</a></td>
<tr><td class="dl"><a href="../players/player_109.html">J. Victor</a></td>
</table> ...
<th width="30" class="hsn dc">ERA</th></tr>
<tr><td class="dl"><a href="../players/player_101.html">J. Unknown</a></td>
</table> ...
</html>"""
_game_log_file_sub = """[%T]\tTop of the 1st -  {0} batting - Pitching for {1} : RHP <a href="../players/player_101.html">Jim Unknown</a>
[%B]\tPitching: RHP <a href="../players/player_101.html">101</a>
[%B]\tBatting: RHB <a href="../players/player_102.html">Jim Alpha</a>
[%N]\t0-0: Ball
[%N]\t1-0: Fly out, F7  (Flyball, 7LSF)
[%B]\tBatting: LHB <a href="../players/player_103.html">Jim Beta</a>
[%N]\t0-0: SINGLE  (Groundball, 56)
[%B]\tBatting: RHB <a href="../players/player_104.html">Jim Charlie</a>
[%N]\t0-0: <b>SINGLE</b>  (Groundball, 6MS) (infield hit)
[%N]\t<a href="../players/player_103.html">Jim Beta</a> to second
[%B]\tBatting: SHB <a href="../players/player_105.html">Jim Delta</a>
[%N]\t0-0:  Fly out, F9  (Flyball, 9)
[%B]\tBatting: LHB <a href="../players/player_106.html">Jim Echo</a>
[%N]\t0-0: Swinging Strike
[%N]\t0-1: Foul Ball, location: 2F
[%N]\t0-2: Strikes out  swinging
[%F]\tTop of the 1st over -  0 run(s), 2 hit(s), 0 error(s), 2 left on base; {3} 0 - {4} 0"""
_game_log_link_sub = """<html> ...
<title>{0} @ {1}</title> ...
<div style="text-align:center; color:#000000; padding-top:4px;">{2}</div> ...
<table cellspacing="0" cellpadding="0" class="data" width="968px">\r
\t<tr><th colspan="2" class="boxtitle">TOP OF THE 1ST</th></tr>\r
\t<tr>\r
\t<th colspan="2" align="left" style="padding:4px 0px 4px 4px;">\r
\t{0} batting - Pitching for {1} : RHP <a href="../players/player_101.html">Jim Unknown</a>\r
\t</th>\r
\t</tr>\r
\t<tr>\r
\t<td valign="top" width="268px" class="dl">\r
\tPitching: RHP <a href="../players/player_101.html">101</a>\r
\t</td>\r
\t<td class="dl" width="700px">\r
\t</td>\r
\t</tr>\r
\t<tr>\r
\t<td valign="top" width="268px" class="dl">\r
\tBatting: RHB <a href="../players/player_102.html">Jim Alpha</a>\r
\t</td>\r
\t<td class="dl" width="700px">\r
\t0-0: Ball<br>1-0: Fly out, F7  (Flyball, 7LSF)\r
\t</td>\r
\t</tr>\r
\t<tr>\r
\t<td valign="top" width="268px" class="dl">\r
\tBatting: LHB <a href="../players/player_103.html">Jim Beta</a>\r
\t</td>\r
\t<td class="dl" width="700px">\r
\t0-0: SINGLE  (Groundball, 56)\r
\t</td>\r
\t</tr>\r
\t<tr>\r
\t<td valign="top" width="268px" class="dl">\r
\tBatting: RHB <a href="../players/player_104.html">Jim Charlie</a>\r
\t</td>\r
\t<td class="dl" width="700px">\r
\t0-0: <b>SINGLE</b>  (Groundball, 6MS) (infield hit)<br><a href="../players/player_103.html">Jim Beta</a> to second\r
\t</td>\r
\t</tr>\r
\t<tr>\r
\t<td valign="top" width="268px" class="dl">\r
\tBatting: SHB <a href="../players/player_105.html">Jim Delta</a>\r
\t</td>\r
\t<td class="dl" width="700px">\r
\t0-0:  Fly out, F9  (Flyball, 9)\r
\t</td>\r
\t</tr>\r
\t<tr>\r
\t<td valign="top" width="268px" class="dl">\r
\tBatting: LHB <a href="../players/player_106.html">Jim Echo</a>\r
\t</td>\r
\t<td class="dl" width="700px">\r
\t0-0: Swinging Strike<br>0-1: Foul Ball, location: 2F<br>0-2: Strikes out  swinging\r
\t</td>\r
\t</tr>\r
\t<tr>\r
\t<td class="datathbg" colspan="2">Top of the 1st over -  0 run(s), 2 hit(s), 0 error(s), 2 left on base; {3} 0 - {4} 0</td>\r
\t</tr>\r
\t</table> ...
</html>"""
_player_sub = """<html> ...
<title>Player Report for #{0}  {1}</title> ...
<div class="repsubtitle"><a class="boxlink" style="font-weight:bold; font-size:18px; color:#FFFFFF;" href="../teams/team_{2}.html">{3}</a></div>
<div style="text-align:center;font-weight:bold; font-size:18px; color:#FFFFFF;">\r
\tAge: 21 | \r
\tBats: R |\r
\tThrows: R |\r
\tMorale: Normal  \r
\t&nbsp;&nbsp;&nbsp;\r
\t</div> ...
</html>"""
_player_empty_sub = '<html><title>Player Report for #{0}  {1}</title></html>'

_html = 'https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/'
_game_box = 'box_scores/game_box_{}.html'
_game_log = 'game_logs/log_{}.html'
_player = 'players/player_{}.html'

_players = ['101', '102', '103', '104', '105', '106', '107', '108', '109', '110', '111', '112']
_plays = [[{
    'label':
    'Top 1st',
    'batting':
    'T31',
    'pitching':
    'P101',
    'footer':
    '0 run(s), 2 hit(s), 0 error(s), 2 left on base; T31 0 - T45 0',
    'play': [{
        'type': 'matchup',
        'pitcher': {
            'id': 'P101',
            'pos': 'SP',
            'stats': '0.0 IP, 0 H, 0 R, 0 BB, 0 K'
        },
        'batter': {
            'id': 'P102',
            'pos': 'SS',
            'stats': '0-0'
        }
    }, {
        'type': 'event',
        'outs': 1,
        'runs': 0,
        'sequence': ['1 1 0 Ball', '2 1 0 In play, out(s)'],
        'value': 'P102 flies out to left fielder P111 (zone 7LSF).',
    }, {
        'type': 'matchup',
        'pitcher': {
            'id': 'P101',
            'pos': 'SP',
            'stats': '0.1 IP, 0 H, 0 R, 0 BB, 0 K'
        },
        'batter': {
            'id': 'P103',
            'pos': '1B',
            'stats': '0-0'
        }
    }, {
        'type':
        'event',
        'outs':
        0,
        'runs':
        0,
        'sequence': ['1 0 0 In play, no out'],
        'value':
        'P103 singles on a ground ball to left fielder P111 (zone 56).'
    }, {
        'type': 'matchup',
        'pitcher': {
            'id': 'P101',
            'pos': 'SP',
            'stats': '0.1 IP, 1 H, 0 R, 0 BB, 0 K'
        },
        'batter': {
            'id': 'P104',
            'pos': 'CF',
            'stats': '0-0'
        }
    }, {
        'type':
        'event',
        'outs':
        0,
        'runs':
        0,
        'sequence': ['1 0 0 In play, no out'],
        'value':
        'P104 singles on a ground ball to shortstop P112 (infield hit) '
        '(zone 6MS). P103 to second.'
    }, {
        'type': 'matchup',
        'pitcher': {
            'id': 'P101',
            'pos': 'SP',
            'stats': '0.1 IP, 2 H, 0 R, 0 BB, 0 K'
        },
        'batter': {
            'id': 'P105',
            'pos': 'C',
            'stats': '0-0'
        }
    }, {
        'type': 'event',
        'outs': 1,
        'runs': 0,
        'sequence': ['1 0 0 In play, out(s)'],
        'value': 'P105 flies out to right fielder P110 (zone 9).'
    }, {
        'type': 'matchup',
        'pitcher': {
            'id': 'P101',
            'pos': 'SP',
            'stats': '0.2 IP, 2 H, 0 R, 0 BB, 0 K'
        },
        'batter': {
            'id': 'P106',
            'pos': '2B',
            'stats': '0-0'
        }
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
        mo_box = mock.mock_open(read_data=box_content)
        mock_handle_box = mo_box()
        log_content = _game_log_file_sub.format(
            'Arizona Diamondbacks', 'Los Angeles Dodgers', _now_displayed,
            'Arizona', 'Los Angeles')
        mo_log = mock.mock_open(read_data=log_content)
        mock_handle_log = mo_log()
        mock_open.side_effect = [mo_box.return_value, mo_log.return_value]

        box_link = _path + _game_box.format('2998')
        log_link = _path + _game_log.format('2998')
        actual = parse_game_data(box_link, log_link)
        expected = _data('2998', '76-86', 4, 'Arizona Diamondbacks',
                         _now_encoded, '97-65', 2, 'Los Angeles Dodgers',
                         _players, _plays)
        self.assertEqual(actual, expected)

        mock_isfile.assert_has_calls(
            [mock.call(box_link), mock.call(log_link)])
        mock_handle_box.assert_not_called()
        mock_handle_log.assert_not_called()
        mock_open.assert_has_calls([
            mock.call(box_link, 'r', encoding='iso-8859-1'),
            mock.call(log_link, 'r', encoding='iso-8859-1')
        ])
        mock_urlopen.assert_not_called()

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
        log_content = _game_log_link_sub.format(
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
        log_content = _game_log_link_sub.format(
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
        log_content = _game_log_link_sub.format(
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
