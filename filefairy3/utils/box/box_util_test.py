#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import mock
import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/utils/box', '', _path))
from utils.box.box_util import clarify  # noqa

_html = 'https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/'
_game_box = 'box_scores/game_box_{}.html'

DATE = datetime.datetime(2022, 10, 9, 0, 0, 0)
FDATE = '10/09/2022'
FDATE_INVALID = '10/26/1985'
TEAM1 = 'Arizona Diamondbacks'
TEAM2 = 'Los Angeles Dodgers'
TEAM3 = 'Los Angeles Angels'
VALID = '<html> ... <title>MLB Box Scores, {0} at {1}, {2}</title> ... ' + \
        '<tr style="background-color:#FFFFFE;">\n\t<td class="dl"><b>{3}' + \
        '</b></td>\n\t<td class="dc">0</td>\n<td class="dc">0</td>\n<td ' + \
        'class="dc">0</td>\n<td class="dc">2</td>\n<td class="dc">2</td>' + \
        '\n<td class="dc">0</td>\n<td class="dc">0</td>\n<td class="dc">0' + \
        '</td>\n<td class="dc">0</td>\n\t<td class="dc"><b>4</b></td>\n\t' + \
        '<td class="dc"><b>10</b></td>\n\t<td class="dc"><b>0</b></td>\n\t' + \
        '</tr>\n\t<tr style="background-color:#FFFFFE;">\n\t<td ' + \
        'class="dl">{4}</td>\n\t<td class="dc">0</td>\n<td class="dc">1' + \
        '</td>\n<td class="dc">0</td>\n<td class="dc">0</td>\n<td ' + \
        'class="dc">0</td>\n<td class="dc">0</td>\n<td class="dc">1</td>\n' + \
        '<td class="dc">0</td>\n<td class="dc">0</td>\n\t<td class="dc">' + \
        '<b>2</b></td>\n\t<td class="dc"><b>9</b></td>\n\t<td class="dc">' + \
        '<b>0</b></td>\n\t</tr>\n\t</table>\n\t</td>\n\t</tr> ... </html'


class BoxUtilTest(unittest.TestCase):
    @mock.patch('utils.box.box_util.urlopen')
    def test_clarify__with_one_valid_content(self, mock_urlopen):
        content = VALID.format(TEAM1, TEAM2, FDATE, TEAM1, TEAM2)
        mock_urlopen.return_value = content

        link = _html + _game_box.format('2998')
        actual = clarify(DATE, link, 'T31 4, TLA 2')
        expected = 'T31 4, T45 2'
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(link)

    @mock.patch('utils.box.box_util.urlopen')
    def test_clarify__with_one_swap_both(self, mock_urlopen):
        content = VALID.format(TEAM2, TEAM1, FDATE, TEAM2, TEAM1)
        mock_urlopen.return_value = content

        link = _html + _game_box.format('2998')
        actual = clarify(DATE, link, 'TLA 4, T31 2')
        expected = 'T45 4, T31 2'
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(link)

    @mock.patch('utils.box.box_util.urlopen')
    def test_clarify__with_one_swap_row(self, mock_urlopen):
        content = VALID.format(TEAM1, TEAM2, FDATE, TEAM2, TEAM1)
        mock_urlopen.return_value = content

        link = _html + _game_box.format('2998')
        actual = clarify(DATE, link, 'TLA 4, T31 2')
        expected = 'T45 4, T31 2'
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(link)

    @mock.patch('utils.box.box_util.urlopen')
    def test_clarify__with_one_swap_title(self, mock_urlopen):
        content = VALID.format(TEAM2, TEAM1, FDATE, TEAM1, TEAM2)
        mock_urlopen.return_value = content

        link = _html + _game_box.format('2998')
        actual = clarify(DATE, link, 'T31 4, TLA 2')
        expected = 'T31 4, T45 2'
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(link)

    @mock.patch('utils.box.box_util.urlopen')
    def test_clarify__with_two_valid_content(self, mock_urlopen):
        content = VALID.format(TEAM2, TEAM3, FDATE, TEAM2, TEAM3)
        mock_urlopen.return_value = content

        link = _html + _game_box.format('2998')
        actual = clarify(DATE, link, 'TLA 4, TLA 2')
        expected = 'T45 4, T44 2'
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(link)

    @mock.patch('utils.box.box_util.urlopen')
    def test_clarify__with_two_swap_both(self, mock_urlopen):
        content = VALID.format(TEAM3, TEAM2, FDATE, TEAM3, TEAM2)
        mock_urlopen.return_value = content

        link = _html + _game_box.format('2998')
        actual = clarify(DATE, link, 'TLA 4, TLA 2')
        expected = 'T44 4, T45 2'
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(link)

    @mock.patch('utils.box.box_util.urlopen')
    def test_clarify__with_two_swap_row(self, mock_urlopen):
        content = VALID.format(TEAM2, TEAM3, FDATE, TEAM3, TEAM2)
        mock_urlopen.return_value = content

        link = _html + _game_box.format('2998')
        actual = clarify(DATE, link, 'TLA 4, TLA 2')
        expected = 'T44 4, T45 2'
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(link)

    @mock.patch('utils.box.box_util.urlopen')
    def test_clarify__with_two_swap_title(self, mock_urlopen):
        content = VALID.format(TEAM3, TEAM2, FDATE, TEAM2, TEAM3)
        mock_urlopen.return_value = content

        link = _html + _game_box.format('2998')
        actual = clarify(DATE, link, 'TLA 4, TLA 2')
        expected = 'T45 4, T44 2'
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(link)

    @mock.patch('utils.box.box_util.urlopen')
    def test_clarify__with_invalid_date(self, mock_urlopen):
        content = VALID.format(TEAM1, TEAM2, FDATE_INVALID, TEAM1, TEAM2)
        mock_urlopen.return_value = content

        link = _html + _game_box.format('2998')
        actual = clarify(DATE, link, 'T31 4, TLA 2')
        expected = 'T31 4, TLA 2'
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(link)

    @mock.patch('utils.box.box_util.urlopen')
    def test_clarify__with_invalid_title(self, mock_urlopen):
        content = VALID.format(TEAM2, TEAM3, FDATE, TEAM2, TEAM3)
        mock_urlopen.return_value = content

        link = _html + _game_box.format('2998')
        actual = clarify(DATE, link, 'T31 4, TLA 2')
        expected = 'T31 4, TLA 2'
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(link)

    @mock.patch('utils.box.box_util.urlopen')
    def test_clarify__with_invalid_runs(self, mock_urlopen):
        content = VALID.format(TEAM1, TEAM2, FDATE, TEAM1, TEAM2)
        mock_urlopen.return_value = content

        link = _html + _game_box.format('2998')
        actual = clarify(DATE, link, 'T31 4, TLA 3')
        expected = 'T31 4, TLA 3'
        self.assertEqual(actual, expected)

        mock_urlopen.assert_called_once_with(link)


if __name__ == '__main__':
    unittest.main()
