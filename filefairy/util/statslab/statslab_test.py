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
from util.team.team import decoding_to_encoding  # noqa

_html = 'https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/'
_game_box = 'box_scores/game_box_{}.html'

FILE = _path + _game_box.format('2998')
LINK = _html + _game_box.format('2998')
INVALID_TITLE = {'ok': False, 'error': 'invalid_title'}
INVALID_LINE = {'ok': False, 'error': 'invalid_line'}
DATE = datetime.datetime(2022, 10, 9, 0, 0, 0)
FDATE = '10/09/2022'
FDATE_INVALID = '10/26/1985'
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
VALID = '<html> ... <title>{0} Box Scores, {1} at {2}, {3}</title> ... ' + \
        '<tr style="background-color:#FFFFFE;">\n\t<td class="dl"><b>{4}' + \
        '</b></td>\n\t<td class="dc">0</td>\n<td class="dc">0</td>\n<td ' + \
        'class="dc">0</td>\n<td class="dc">2</td>\n<td class="dc">2</td>' + \
        '\n<td class="dc">0</td>\n<td class="dc">0</td>\n<td class="dc">0' + \
        '</td>\n<td class="dc">0</td>\n\t<td class="dc"><b>{5}</b></td>\n' + \
        '\t<td class="dc"><b>10</b></td>\n\t<td class="dc"><b>0</b></td>\n' + \
        '\t</tr>\n\t<tr style="background-color:#FFFFFE;">\n\t<td ' + \
        'class="dl">{6}</td>\n\t<td class="dc">0</td>\n<td class="dc">1' + \
        '</td>\n<td class="dc">0</td>\n<td class="dc">0</td>\n<td ' + \
        'class="dc">0</td>\n<td class="dc">0</td>\n<td class="dc">1</td>\n' + \
        '<td class="dc">0</td>\n<td class="dc">0</td>\n\t<td class="dc">' + \
        '<b>{7}</b></td>\n\t<td class="dc"><b>9</b></td>\n\t<td ' + \
        'class="dc"><b>0</b></td>\n\t</tr>\n\t</table>\n\t</td>\n\t</tr> ' + \
        '... </html'


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


class StatslabTest(unittest.TestCase):
    @mock.patch('util.statslab.statslab.open', create=True)
    @mock.patch('util.statslab.statslab.os.path.isfile')
    def test_box_score__with_valid_file(self, mock_isfile, mock_open):
        mock_isfile.return_value = True
        content = VALID.format(MLB, TEAM1, TEAM2, FDATE,
                               RECORD.format(TEAM1, RECORD1), RUNS1,
                               RECORD.format(TEAM2, RECORD2), RUNS2)
        mo = mock.mock_open(read_data=content)
        mock_handle = mo()
        mock_open.side_effect = [mo.return_value]

        actual = box_score(FILE)
        expected = _box(RECORD1, RUNS1, TEAM1, DATE, RECORD2, RUNS2, TEAM2)
        self.assertEqual(actual, expected)

        mock_isfile.assert_called_once_with(FILE)
        mock_handle.assert_not_called()
        mock_open.assert_called_once_with(FILE, 'r', encoding='iso-8859-1')

    @mock.patch('util.statslab.statslab.urlopen')
    def test_box_score__with_valid_link(self, mock_urlopen):
        content = VALID.format(MLB, TEAM1, TEAM2, FDATE,
                               RECORD.format(TEAM1, RECORD1), RUNS1,
                               RECORD.format(TEAM2, RECORD2), RUNS2)
        mock_urlopen.return_value = bytes(content, 'utf-8')

        actual = box_score(LINK)
        expected = _box(RECORD1, RUNS1, TEAM1, DATE, RECORD2, RUNS2, TEAM2)
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(LINK)

    @mock.patch('util.statslab.statslab.urlopen')
    def test_box_score__with_invalid_title(self, mock_urlopen):
        content = VALID.format(NPB, TEAM4, TEAM5, FDATE,
                               RECORD.format(TEAM4, RECORD1), RUNS1,
                               RECORD.format(TEAM5, RECORD2), RUNS2)
        mock_urlopen.return_value = bytes(content, 'utf-8')

        actual = box_score(LINK)
        expected = INVALID_TITLE
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(LINK)

    @mock.patch('util.statslab.statslab.urlopen')
    def test_box_score__with_invalid_line(self, mock_urlopen):
        content = VALID.format(MLB, TEAM1, TEAM2, FDATE,
                               RECORD.format(TEAM4, RECORD1), RUNS1,
                               RECORD.format(TEAM5, RECORD2), RUNS2)
        mock_urlopen.return_value = bytes(content, 'utf-8')

        actual = box_score(LINK)
        expected = INVALID_LINE
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(LINK)


if __name__ == '__main__':
    unittest.main()
