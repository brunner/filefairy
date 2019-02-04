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
from common.elements.elements import table  # noqa
from common.test.test import get_testdata  # noqa
from services.scoreboard.scoreboard import line_score_body  # noqa
from services.scoreboard.scoreboard import line_score_foot  # noqa
from services.scoreboard.scoreboard import line_scores  # noqa
from services.scoreboard.scoreboard import pending_body  # noqa
from services.scoreboard.scoreboard import pending_carousel  # noqa
from services.scoreboard.scoreboard import pending_dialog  # noqa

DATE_08310000 = datetime_datetime_pst(2024, 8, 31)

GAMES_DIR = re.sub(r'/services/scoreboard', '/resource/games', _path)

TESTDATA = get_testdata()

GAME_2449 = json.loads(TESTDATA['2449.json'])
GAME_2469 = json.loads(TESTDATA['2469.json'])

HEAD_2449 = table(body=[[cell(content='Wednesday')]])
BODY_2449 = table(head=[[cell(content='Final (10)')]])
FOOT_2449 = table(foot=[[cell(content='Twins Top Tigers in Extras')]])

HEAD_2469 = table(body=[[cell(content='Thursday')]])
BODY_2469 = table(head=[[cell(content='Final')]])
FOOT_2469 = table(foot=[[cell(content='Twins Shut Out Tigers')]])

DATA_2449 = (GAME_2449['date'], BODY_2449, FOOT_2449)
DATA_2469 = (GAME_2469['date'], BODY_2469, FOOT_2469)


class ScoreboardTest(unittest.TestCase):
    def test_line_score_body(self):
        for num in ['2449', '2469', '2476']:
            data = json.loads(TESTDATA[num + '.json'])
            actual = line_score_body(data)
            expected = json.loads(TESTDATA['line_score_body_' + num + '.json'])
            self.assertEqual(actual, expected)

    def test_line_score_foot(self):
        for num in ['2449', '2469', '2476']:
            data = json.loads(TESTDATA[num + '.json'])
            actual = line_score_foot(data)
            expected = json.loads(TESTDATA['line_score_foot_' + num + '.json'])
            self.assertEqual(actual, expected)

    @mock.patch('services.scoreboard.scoreboard.loads')
    @mock.patch('services.scoreboard.scoreboard.os.listdir')
    @mock.patch('services.scoreboard.scoreboard.line_score_foot')
    @mock.patch('services.scoreboard.scoreboard.line_score_body')
    def test_line_scores(self, mock_body, mock_foot, mock_listdir, mock_loads):
        mock_body.side_effect = [BODY_2449, BODY_2469]
        mock_foot.side_effect = [FOOT_2449, FOOT_2469]
        mock_listdir.return_value = ['2449.json', '2469.json']
        mock_loads.side_effect = [GAME_2449, GAME_2469]

        actual = line_scores()
        expected = {
            'T40': [DATA_2449, DATA_2469],
            'T47': [DATA_2449, DATA_2469]
        }
        self.assertEqual(actual, expected)

        mock_body.assert_has_calls(
            [mock.call(GAME_2449), mock.call(GAME_2469)])
        mock_foot.assert_has_calls(
            [mock.call(GAME_2449), mock.call(GAME_2469)])
        mock_listdir.assert_called_once_with(GAMES_DIR)
        mock_loads.assert_has_calls([
            mock.call(os.path.join(GAMES_DIR, '2449.json')),
            mock.call(os.path.join(GAMES_DIR, '2469.json'))
        ])

    def test_pending_body(self):
        actual = pending_body(['T31 4, TLA 2', 'TNY 5, TLA 3'])
        expected = json.loads(TESTDATA['pending_body_la.json'])
        self.assertEqual(actual, expected)

    @mock.patch('services.scoreboard.scoreboard.pending_body')
    def test_pending_carousel(self, mock_body):
        body = table(clazz='', head=[[cell(content='Pending')]])
        mock_body.side_effect = [body, body]

        date = encode_datetime(DATE_08310000)
        score = 'T31 4, TLA 2'
        statsplus = {date: {'2998': score}}

        data_2998 = (datetime_replace(date, hour=23, minute=59), body)
        actual = pending_carousel(statsplus)
        expected = {date: data_2998}
        self.assertEqual(actual, expected)

        mock_body.assert_has_calls([mock.call([score])])

    @mock.patch('services.scoreboard.scoreboard.pending_body')
    def test_pending_dialog(self, mock_body):
        body = table(clazz='', head=[[cell(content='Pending')]])
        mock_body.side_effect = [body, body]

        date = encode_datetime(DATE_08310000)
        score = 'T31 4, TLA 2'
        statsplus = {date: {'2998': score}}

        data_2998 = (date, body, None)
        actual = pending_dialog(statsplus)
        expected = {'T31': [data_2998], 'T44': [data_2998], 'T45': [data_2998]}
        self.assertEqual(actual, expected)

        mock_body.assert_has_calls([mock.call([score]), mock.call([score])])


if __name__ == '__main__':
    unittest.main()
