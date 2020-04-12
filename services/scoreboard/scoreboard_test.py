#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for scoreboard.py."""

import json
import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/services/scoreboard', '', _path))

from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.datetime_.datetime_ import datetime_replace  # noqa
from common.datetime_.datetime_ import encode_datetime  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import dialog  # noqa
from common.elements.elements import row  # noqa
from common.elements.elements import table  # noqa
from common.test.test import get_testdata  # noqa
from services.scoreboard.scoreboard import line_score_show_body  # noqa
from services.scoreboard.scoreboard import line_score_show_foot  # noqa
from services.scoreboard.scoreboard import line_scores  # noqa
from services.scoreboard.scoreboard import pending_show_body  # noqa
from services.scoreboard.scoreboard import pending_carousel  # noqa
from services.scoreboard.scoreboard import pending_dialog  # noqa

DATE_08280000 = datetime_datetime_pst(2024, 8, 28)
DATE_08310000 = datetime_datetime_pst(2024, 8, 31)

GAMES_DIR = re.sub(r'/services/scoreboard', '/resources/games', _path)

TESTDATA = get_testdata()

DIALOG_2449 = dialog(id_='d0828g2449')
DIALOG_2469 = dialog(id_='d0829g2469')
DIALOG_0 = dialog(id_='d0828g0')

GAME_2449 = json.loads(TESTDATA['2449.json'])
GAME_2469 = json.loads(TESTDATA['2469.json'])

HEAD_2449 = table(body=[row(cells=[cell(content='Wednesday')])])
HIDE_BODY_2449 = table(head=[row(cells=[cell(content='Warmup')])])
HIDE_FOOT_2449 = table(
    foot=[row(cells=[cell(content='7:10 PM at Target Field')])])
SHOW_BODY_2449 = table(head=[row(cells=[cell(content='Final (10)')])])
SHOW_FOOT_2449 = table(
    foot=[row(cells=[cell(content='Twins Top Tigers in Extras')])])

HEAD_2469 = table(body=[row(cells=[cell(content='Thursday')])])
HIDE_BODY_2469 = table(head=[row(cells=[cell(content='Warmup')])])
HIDE_FOOT_2469 = table(
    foot=[row(cells=[cell(content='7:10 PM at Target Field')])])
SHOW_BODY_2469 = table(head=[row(cells=[cell(content='Final')])])
SHOW_FOOT_2469 = table(
    foot=[row(cells=[cell(content='Twins Shut Out Tigers')])])

HIDE_2449 = (GAME_2449['date'], HIDE_BODY_2449, HIDE_FOOT_2449)
HIDE_2469 = (GAME_2469['date'], HIDE_BODY_2469, HIDE_FOOT_2469)
SHOW_2449 = (GAME_2449['date'], SHOW_BODY_2449, SHOW_FOOT_2449)
SHOW_2469 = (GAME_2469['date'], SHOW_BODY_2469, SHOW_FOOT_2469)


class ScoreboardTest(unittest.TestCase):
    def test_line_score_show_body(self):
        for num in ['2449', '2469', '2476']:
            data = json.loads(TESTDATA[num + '.json'])
            actual = line_score_show_body(data)
            s = 'line_score_show_body_' + num + '.json'
            expected = json.loads(TESTDATA[s])
            self.assertEqual(actual, expected)

    def test_line_score_show_foot(self):
        for num in ['2449', '2469', '2476']:
            data = json.loads(TESTDATA[num + '.json'])
            actual = line_score_show_foot(data)
            s = 'line_score_show_foot_' + num + '.json'
            expected = json.loads(TESTDATA[s])
            self.assertEqual(actual, expected)

    @mock.patch('services.scoreboard.scoreboard.loads')
    @mock.patch('services.scoreboard.scoreboard.os.listdir')
    @mock.patch('services.scoreboard.scoreboard.line_score_show_foot')
    @mock.patch('services.scoreboard.scoreboard.line_score_show_body')
    @mock.patch('services.scoreboard.scoreboard.line_score_hide_foot')
    @mock.patch('services.scoreboard.scoreboard.line_score_hide_body')
    @mock.patch('services.scoreboard.scoreboard.create_dialog')
    def test_line_scores__hidden_false(
            self, mock_create_dialog, mock_hide_body, mock_hide_foot,
            mock_show_body, mock_show_foot, mock_listdir, mock_loads):
        mock_show_body.side_effect = [SHOW_BODY_2449, SHOW_BODY_2469]
        mock_show_foot.side_effect = [SHOW_FOOT_2449, SHOW_FOOT_2469]
        mock_listdir.return_value = ['2449.json', '2469.json']
        mock_loads.side_effect = [GAME_2449, GAME_2469]

        actual = line_scores()
        expected = {
            'dialogs': [],
            'scores': {
                'T40': [SHOW_2449, SHOW_2469],
                'T47': [SHOW_2449, SHOW_2469]
            }
        }
        self.assertEqual(actual, expected)

        mock_create_dialog.assert_not_called()
        mock_hide_body.assert_not_called()
        mock_hide_foot.assert_not_called()
        mock_show_body.assert_has_calls([
            mock.call(GAME_2449, hidden=False),
            mock.call(GAME_2469, hidden=False)
        ])
        mock_show_foot.assert_has_calls([
            mock.call(GAME_2449, hidden=False),
            mock.call(GAME_2469, hidden=False)
        ])
        mock_listdir.assert_called_once_with(GAMES_DIR)
        mock_loads.assert_has_calls([
            mock.call(os.path.join(GAMES_DIR, '2449.json')),
            mock.call(os.path.join(GAMES_DIR, '2469.json'))
        ])

    @mock.patch('services.scoreboard.scoreboard.loads')
    @mock.patch('services.scoreboard.scoreboard.os.listdir')
    @mock.patch('services.scoreboard.scoreboard.line_score_show_foot')
    @mock.patch('services.scoreboard.scoreboard.line_score_show_body')
    @mock.patch('services.scoreboard.scoreboard.line_score_hide_foot')
    @mock.patch('services.scoreboard.scoreboard.line_score_hide_body')
    @mock.patch('services.scoreboard.scoreboard.create_dialog')
    def test_line_scores__hidden_true(
            self, mock_create_dialog, mock_hide_body, mock_hide_foot,
            mock_show_body, mock_show_foot, mock_listdir, mock_loads):
        mock_create_dialog.side_effect = [DIALOG_2449, DIALOG_2469]
        mock_hide_body.side_effect = [HIDE_BODY_2449, HIDE_BODY_2469]
        mock_hide_foot.side_effect = [HIDE_FOOT_2449, HIDE_FOOT_2469]
        mock_show_body.side_effect = [SHOW_BODY_2449, SHOW_BODY_2469]
        mock_show_foot.side_effect = [SHOW_FOOT_2449, SHOW_FOOT_2469]
        mock_listdir.return_value = ['2449.json', '2469.json']
        mock_loads.side_effect = [GAME_2449, GAME_2469]

        actual = line_scores(hidden=True)
        expected = {
            'dialogs': [DIALOG_2449, DIALOG_2469],
            'scores': {
                'T40': [HIDE_2449, SHOW_2449, HIDE_2469, SHOW_2469],
                'T47': [HIDE_2449, SHOW_2449, HIDE_2469, SHOW_2469]
            }
        }
        self.assertEqual(actual, expected)

        mock_create_dialog.assert_has_calls(
            [mock.call('0828', '2449'),
             mock.call('0829', '2469')])
        mock_hide_body.assert_has_calls(
            [mock.call(GAME_2449), mock.call(GAME_2469)])
        mock_hide_foot.assert_has_calls(
            [mock.call(GAME_2449), mock.call(GAME_2469)])
        mock_show_body.assert_has_calls([
            mock.call(GAME_2449, hidden=True),
            mock.call(GAME_2469, hidden=True)
        ])
        mock_show_foot.assert_has_calls([
            mock.call(GAME_2449, hidden=True),
            mock.call(GAME_2469, hidden=True)
        ])
        mock_listdir.assert_called_once_with(GAMES_DIR)
        mock_loads.assert_has_calls([
            mock.call(os.path.join(GAMES_DIR, '2449.json')),
            mock.call(os.path.join(GAMES_DIR, '2469.json'))
        ])

    def test_pending_show_body(self):
        date = encode_datetime(DATE_08280000)
        actual = pending_show_body(date, ['T31 4, TLA 2', 'TNY 5, TLA 3'])
        expected = json.loads(TESTDATA['pending_show_body_la.json'])
        self.assertEqual(actual, expected)

    @mock.patch('services.scoreboard.scoreboard.pending_show_body')
    @mock.patch('services.scoreboard.scoreboard.pending_hide_body')
    @mock.patch('services.scoreboard.scoreboard.create_dialog')
    def test_pending_carousel__hidden_false(self, mock_create_dialog,
                                            mock_hide_body, mock_show_body):
        body = table(clazz='', head=[row(cells=[cell(content='Pending')])])
        mock_show_body.side_effect = [body, body]

        date = encode_datetime(DATE_08280000)
        score = 'T31 4, TLA 2'
        statsplus = {date: {'2998': score}}

        data_2998 = [(datetime_replace(date, hour=23, minute=59), body)]
        actual = pending_carousel(statsplus)
        expected = {'dialogs': [], 'scores': {date: data_2998}}
        self.assertEqual(actual, expected)

        mock_create_dialog.assert_not_called()
        mock_hide_body.assert_not_called()
        mock_show_body.assert_called_once_with(date, [score], hidden=False)

    @mock.patch('services.scoreboard.scoreboard.pending_show_body')
    @mock.patch('services.scoreboard.scoreboard.pending_hide_body')
    @mock.patch('services.scoreboard.scoreboard.create_dialog')
    def test_pending_carousel__hidden_true(self, mock_create_dialog,
                                           mock_hide_body, mock_show_body):
        mock_create_dialog.side_effect = [DIALOG_0]
        hide = table(
            clazz='', head=[row(cells=[cell(content='Pending (hidden)')])])
        show = table(
            clazz='', head=[row(cells=[cell(content='Pending (shown)')])])
        mock_hide_body.side_effect = [hide, hide]
        mock_show_body.side_effect = [show, show]

        date = encode_datetime(DATE_08280000)
        score = 'T31 4, TLA 2'
        statsplus_scores = {date: {'2998': score}}

        data_2998 = [(datetime_replace(date, hour=23, minute=59), hide),
                     (datetime_replace(date, hour=23, minute=59), show)]
        actual = pending_carousel(statsplus_scores, hidden=True)
        expected = {'dialogs': [DIALOG_0], 'scores': {date: data_2998}}
        self.assertEqual(actual, expected)

        mock_create_dialog.assert_called_once_with('0828', '0')
        mock_hide_body.assert_called_once_with(date, [score])
        mock_show_body.assert_called_once_with(date, [score], hidden=True)

    @mock.patch('services.scoreboard.scoreboard.pending_show_body')
    def test_pending_dialog(self, mock_show_body):
        body = table(clazz='', head=[row(cells=[cell(content='Pending')])])
        mock_show_body.side_effect = [body, body]

        date = encode_datetime(DATE_08310000)
        score = 'T31 4, TLA 2'
        statsplus = {date: {'2998': score}}

        data_2998 = (date, body, None)
        actual = pending_dialog(statsplus)
        expected = {'T31': [data_2998], 'T44': [data_2998], 'T45': [data_2998]}
        self.assertEqual(actual, expected)

        mock_show_body.assert_has_calls(
            [mock.call(date, [score]),
             mock.call(date, [score])])


if __name__ == '__main__':
    unittest.main()
