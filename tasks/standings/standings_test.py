#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for standings.py."""

import json
import os
import re
import sys
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.extend((_path, re.sub(r'/tasks/standings', '', _path)))

from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.datetime_.datetime_ import encode_datetime  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import dialog  # noqa
from common.elements.elements import table  # noqa
from common.elements.elements import topper  # noqa
from common.jinja2_.jinja2_ import env  # noqa
from common.json_.json_ import dumps  # noqa
from common.teams.teams import encoding_keys  # noqa
from common.test.test import RMock  # noqa
from common.test.test import Suite  # noqa
from common.test.test import Test  # noqa
from common.test.test import get_testdata  # noqa
from common.test.test import main  # noqa
from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa
from data.shadow.shadow import Shadow  # noqa
from tasks.standings.standings import Standings  # noqa

ENV = env()

DATE_08300000 = datetime_datetime_pst(2024, 8, 30)
DATE_08310000 = datetime_datetime_pst(2024, 8, 31)
DATE_10260602 = datetime_datetime_pst(1985, 10, 26, 6, 2, 30)

GAMES_DIR = re.sub(r'/tasks/standings', '/resource/games', _path)

TESTDATA = get_testdata()

ENCODINGS = encoding_keys()

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

DIALOG_TABLES = [
    HEAD_2449, BODY_2449, FOOT_2449, HEAD_2469, BODY_2469, FOOT_2469
]
DIALOG_TEAMS = ['T31', 'T40', 'T44', 'T45', 'T47']

STATSPLUS_TABLE = {'T31': '1-0', 'T40': '0-2', 'T45': '0-1', 'T47': '2-0'}
CONDENSED_TABLE = {
    e: (STATSPLUS_TABLE.get(e, '0-0'), e in DIALOG_TEAMS)
    for e in ENCODINGS
}

BREADCRUMBS = [{
    'href': '/',
    'name': 'Fairylab'
}, {
    'href': '',
    'name': 'Standings'
}]

LEAGUE_ALE = ['T33', 'T34', 'T48', 'T57', 'T59']
LEAGUE_ALC = ['T35', 'T38', 'T40', 'T43', 'T47']
LEAGUE_ALW = ['T42', 'T44', 'T50', 'T54', 'T58']
LEAGUE_NLE = ['T32', 'T41', 'T49', 'T51', 'T60']
LEAGUE_NLC = ['T36', 'T37', 'T46', 'T52', 'T56']
LEAGUE_NLW = ['T31', 'T39', 'T45', 'T53', 'T55']

TABLE_AL = table(head=[[cell(content='American League')]])
TABLE_ALE = table(head=[[cell(content='AL East')]])
TABLE_ALC = table(head=[[cell(content='AL Central')]])
TABLE_ALW = table(head=[[cell(content='AL West')]])
TABLE_ALWC = table(head=[[cell(content='AL Wild Card')]])

TABLE_NL = table(head=[[cell(content='National League')]])
TABLE_NLE = table(head=[[cell(content='NL East')]])
TABLE_NLC = table(head=[[cell(content='NL Central')]])
TABLE_NLW = table(head=[[cell(content='NL West')]])
TABLE_NLWC = table(head=[[cell(content='NL Wild Card')]])


def _data(finished=False, table_=None):
    if table_ is None:
        table_ = {}

    return {'finished': finished, 'table': table_}


def _table(keys, table_):
    return {k: table_.get(k, '0-0') for k in keys}


class StandingsTest(Test):
    def setUp(self):
        patch_open = mock.patch(
            'api.serializable.serializable.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]

    def reset_mocks(self):
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()

    def create_standings(self, data):
        self.init_mocks(data)
        standings = Standings(date=DATE_10260602, e=ENV)

        self.mock_open.assert_called_once_with(Standings._data(), 'r')
        self.mock_handle.write.assert_not_called()

        self.reset_mocks()
        self.init_mocks(data)

        return standings

    @mock.patch.object(Standings, '_index_html')
    def test_render_data(self, mock_index):
        index_html = {'breadcrumbs': []}
        mock_index.return_value = index_html

        standings = self.create_standings(_data())
        actual = standings._render_data(date=DATE_10260602)
        expected = [('standings/index.html', '', 'standings.html', index_html)]
        self.assertEqual(actual, expected)

        mock_index.assert_called_once_with(date=DATE_10260602)
        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    def test_shadow_data(self):
        table_ = {'T40': '87-75', 'T47': '91-71'}
        standings = self.create_standings(_data(table_=table_))
        actual = standings._shadow_data(date=DATE_10260602)
        expected = [
            Shadow(
                destination='statsplus', key='standings.table', info=table_)
        ]
        self.assertEqual(actual, expected)

        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    @mock.patch.object(Standings, '_start')
    @mock.patch.object(Standings, '_render')
    @mock.patch.object(Standings, '_finish')
    @mock.patch.object(Standings, '_clear')
    def test_notify__download_year(self, mock_clear, mock_finish, mock_render,
                                   mock_start):
        standings = self.create_standings(_data())
        response = standings._notify_internal(notify=Notify.DOWNLOAD_YEAR)
        self.assertEqual(response, Response())

        mock_clear.assert_called_once_with(notify=Notify.DOWNLOAD_YEAR)
        self.assertNotCalled(mock_finish, mock_render, mock_start,
                             self.mock_open, self.mock_handle.write)

    @mock.patch.object(Standings, '_start')
    @mock.patch.object(Standings, '_render')
    @mock.patch.object(Standings, '_finish')
    @mock.patch.object(Standings, '_clear')
    def test_notify__statsplus_finish(self, mock_clear, mock_finish,
                                      mock_render, mock_start):
        standings = self.create_standings(_data())
        response = standings._notify_internal(notify=Notify.STATSPLUS_FINISH)
        self.assertEqual(response, Response())

        mock_finish.assert_called_once_with(notify=Notify.STATSPLUS_FINISH)
        self.assertNotCalled(mock_clear, mock_render, mock_start,
                             self.mock_open, self.mock_handle.write)

    @mock.patch.object(Standings, '_start')
    @mock.patch.object(Standings, '_render')
    @mock.patch.object(Standings, '_finish')
    @mock.patch.object(Standings, '_clear')
    def test_notify__statsplus_render(self, mock_clear, mock_finish,
                                      mock_render, mock_start):
        standings = self.create_standings(_data())
        response = standings._notify_internal(notify=Notify.STATSPLUS_PARSE)
        self.assertEqual(response, Response())

        mock_render.assert_called_once_with(notify=Notify.STATSPLUS_PARSE)
        self.assertNotCalled(mock_clear, mock_finish, mock_start,
                             self.mock_open, self.mock_handle.write)

    @mock.patch.object(Standings, '_start')
    @mock.patch.object(Standings, '_render')
    @mock.patch.object(Standings, '_finish')
    @mock.patch.object(Standings, '_clear')
    def test_notify__statsplus_start(self, mock_clear, mock_finish,
                                     mock_render, mock_start):
        standings = self.create_standings(_data())
        response = standings._notify_internal(notify=Notify.STATSPLUS_START)
        self.assertEqual(response, Response())

        mock_start.assert_called_once_with(notify=Notify.STATSPLUS_START)
        self.assertNotCalled(mock_clear, mock_finish, mock_render,
                             self.mock_open, self.mock_handle.write)

    @mock.patch.object(Standings, '_start')
    @mock.patch.object(Standings, '_render')
    @mock.patch.object(Standings, '_finish')
    @mock.patch.object(Standings, '_clear')
    def test_notify__other(self, mock_clear, mock_finish, mock_render,
                           mock_start):
        standings = self.create_standings(_data())
        response = standings._notify_internal(notify=Notify.OTHER)
        self.assertEqual(response, Response())

        self.assertNotCalled(mock_clear, mock_finish, mock_render, mock_start,
                             self.mock_open, self.mock_handle.write)

    @mock.patch.object(Standings, '_render')
    def test_shadow(self, mock_render):
        standings = self.create_standings(_data())
        response = standings._shadow_internal(date=DATE_10260602)
        self.assertEqual(response, Response())

        mock_render.assert_called_once_with(date=DATE_10260602)
        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    @mock.patch.object(Standings, '_render')
    def test_clear(self, mock_render):
        table_ = {'T40': '87-75', 'T47': '91-71'}
        standings = self.create_standings(_data(table_=table_))
        standings._clear(date=DATE_10260602)

        table_ = {'T40': '0-0', 'T47': '0-0'}
        write = _data(table_=table_)
        mock_render.assert_called_once_with(date=DATE_10260602)
        self.mock_open.assert_called_with(Standings._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    maxDiff = None
    def test_dialog_tables(self):
        date_0830 = encode_datetime(DATE_08300000)
        date_0831 = encode_datetime(DATE_08310000)
        body = table(clazz='', head=[[cell(content='Pending')]])
        data = [
            (date_0830, BODY_2449, FOOT_2449),
            (date_0831, BODY_2469, FOOT_2469),
            (date_0831, body, None),
        ]

        head_0830 = topper('Friday, August 30th, 2024')
        head_0831 = topper('Saturday, August 31st, 2024')
        standings = self.create_standings(_data())
        actual = standings._dialog_tables(data)
        expected = [
            head_0830, BODY_2449, FOOT_2449,
            head_0831, BODY_2469, FOOT_2469,
            body
        ]  # yapf: disable
        self.assertEqual(actual, expected)

        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    @mock.patch.object(Standings, '_render')
    @mock.patch('common.json_.json_.open', create=True)
    @mock.patch('tasks.standings.standings.os.listdir')
    def test_finish(self, mock_listdir, mock_open, mock_render):
        mock_listdir.return_value = [
            '2449.json', '2469.json', '2476.json'
        ]
        suite = Suite(
            RMock(GAMES_DIR, '2449.json', TESTDATA),
            RMock(GAMES_DIR, '2469.json', TESTDATA),
            RMock(GAMES_DIR, '2476.json', TESTDATA),
        )
        mock_open.side_effect = suite.values()

        table_ = {'T40': '66-58', 'T47': '71-53'}
        standings = self.create_standings(_data(table_=table_))
        standings._finish(date=DATE_10260602)

        table_ = {'T40': '66-61', 'T47': '74-53'}
        write = _data(finished=True, table_=table_)
        mock_render.assert_called_once_with(date=DATE_10260602)
        self.mock_open.assert_called_with(Standings._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch('tasks.standings.standings.loads')
    @mock.patch('tasks.standings.standings.os.listdir')
    @mock.patch('tasks.standings.standings.call_service')
    def test_line_scores(self, mock_call, mock_listdir, mock_loads):
        mock_call.side_effect = [BODY_2449, FOOT_2449, BODY_2469, FOOT_2469]
        mock_listdir.return_value = [
            '2449.json', '2469.json'
        ]
        mock_loads.side_effect = [GAME_2449, GAME_2469]

        standings = self.create_standings(_data())
        actual = standings._line_scores()
        expected = {
            'T40': [DATA_2449, DATA_2469],
            'T47': [DATA_2449, DATA_2469]
        }
        self.assertEqual(actual, expected)

        mock_call.assert_has_calls([
            mock.call('scoreboard', 'line_score_body', (GAME_2449, )),
            mock.call('scoreboard', 'line_score_foot', (GAME_2449, )),
            mock.call('scoreboard', 'line_score_body', (GAME_2469, )),
            mock.call('scoreboard', 'line_score_foot', (GAME_2469, ))
        ])
        mock_listdir.assert_called_once_with(GAMES_DIR)
        mock_loads.assert_has_calls([
            mock.call(os.path.join(GAMES_DIR, '2449.json')),
            mock.call(os.path.join(GAMES_DIR, '2469.json'))
        ])
        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    @mock.patch('tasks.standings.standings.call_service')
    def test_pending_scores(self, mock_call):
        body = table(clazz='', head=[[cell(content='Pending')]])
        mock_call.side_effect = [body, body]

        standings = self.create_standings(_data())

        date = encode_datetime(DATE_08310000)
        score = 'T31 4, TLA 2'
        statsplus_scores = {date: {'2998': score}}
        standings.shadow['statsplus.scores'] = statsplus_scores

        data_2998 = (date, body, None)
        actual = standings._pending_scores()
        expected = {'T31': [data_2998], 'T44': [data_2998], 'T45': [data_2998]}
        self.assertEqual(actual, expected)

        mock_call.assert_has_calls([
            mock.call('scoreboard', 'pending_score_body', ([score], )),
            mock.call('scoreboard', 'pending_score_body', ([score], ))
        ])
        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    def test_start(self):
        standings = self.create_standings(_data(finished=True))

        date = encode_datetime(DATE_08310000)
        statsplus_scores = {date: {'2998': 'T31 4, TLA 2'}}
        statsplus_table = {'T40': '0-3', 'T47': '3-0'}
        standings.shadow['statsplus.scores'] = statsplus_scores
        standings.shadow['statsplus.table'] = statsplus_table

        standings._start(date=DATE_10260602)

        write = _data()
        self.assertFalse(standings.shadow['statsplus.scores'])
        self.assertFalse(standings.shadow['statsplus.table'])
        self.mock_open.assert_called_with(Standings._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch.object(Standings, '_pending_scores')
    @mock.patch.object(Standings, '_line_scores')
    @mock.patch.object(Standings, '_dialog_tables')
    @mock.patch('tasks.standings.standings.call_service')
    def test_index_html__finished_false(self, mock_call, mock_dialog,
                                        mock_line, mock_pending):
        date = encode_datetime(DATE_08310000)
        head = table(body=[[cell(content='Saturday')]])
        body = table(clazz='', head=[[cell(content='Pending')]])
        data_2998 = (date, body, None)

        mock_call.side_effect = [
            [TABLE_ALE, TABLE_ALC, TABLE_ALW, TABLE_ALWC],
            TABLE_AL,
            [TABLE_NLE, TABLE_NLC, TABLE_NLW, TABLE_NLWC],
            TABLE_NL,
        ]
        mock_dialog.side_effect = [
            [head, body],
            DIALOG_TABLES,
            [head, body],
            [head, body],
            DIALOG_TABLES,
        ]
        mock_line.return_value = {
            'T40': [DATA_2449, DATA_2469],
            'T47': [DATA_2449, DATA_2469]
        }
        mock_pending.return_value = {
            'T31': [data_2998],
            'T44': [data_2998],
            'T45': [data_2998]
        }

        encodings = encoding_keys()
        table_ = _table(encodings, {})
        standings = self.create_standings(_data(table_=table_))
        standings.shadow['statsplus.table'] = STATSPLUS_TABLE
        actual = standings._index_html(date=DATE_10260602)
        expected = {
            'breadcrumbs': BREADCRUMBS,
            'recent': [TABLE_AL, TABLE_NL],
            'expanded': [
                TABLE_ALE, TABLE_ALC, TABLE_ALW, TABLE_ALWC,
                TABLE_NLE, TABLE_NLC, TABLE_NLW, TABLE_NLWC
            ],
            'dialogs': [
                dialog('31', 'Arizona Diamondbacks', [head, body]),
                dialog('40', 'Detroit Tigers', DIALOG_TABLES),
                dialog('44', 'Los Angeles Angels', [head, body]),
                dialog('45', 'Los Angeles Dodgers', [head, body]),
                dialog('47', 'Minnesota Twins', DIALOG_TABLES),
            ]
        }  # yapf: disable
        self.assertEqual(actual, expected)

        mock_call.assert_has_calls([
            mock.call('division', 'expanded_league', ('American League', [
                ('East', _table(LEAGUE_ALE, STATSPLUS_TABLE)),
                ('Central', _table(LEAGUE_ALC, STATSPLUS_TABLE)),
                ('West', _table(LEAGUE_ALW, STATSPLUS_TABLE)),
            ])),
            mock.call('division', 'condensed_league', ('American League', [
                ('East', _table(LEAGUE_ALE, CONDENSED_TABLE)),
                ('Central', _table(LEAGUE_ALC, CONDENSED_TABLE)),
                ('West', _table(LEAGUE_ALW, CONDENSED_TABLE)),
            ])),
            mock.call('division', 'expanded_league', ('National League', [
                ('East', _table(LEAGUE_NLE, STATSPLUS_TABLE)),
                ('Central', _table(LEAGUE_NLC, STATSPLUS_TABLE)),
                ('West', _table(LEAGUE_NLW, STATSPLUS_TABLE)),
            ])),
            mock.call('division', 'condensed_league', ('National League', [
                ('East', _table(LEAGUE_NLE, CONDENSED_TABLE)),
                ('Central', _table(LEAGUE_NLC, CONDENSED_TABLE)),
                ('West', _table(LEAGUE_NLW, CONDENSED_TABLE)),
            ])),
        ])
        mock_dialog.assert_has_calls([
            mock.call([data_2998]),
            mock.call([DATA_2449, DATA_2469]),
            mock.call([data_2998]),
            mock.call([data_2998]),
            mock.call([DATA_2449, DATA_2469]),
        ])
        mock_line.assert_called_once_with()
        mock_pending.assert_called_once_with()
        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    @mock.patch.object(Standings, '_pending_scores')
    @mock.patch.object(Standings, '_line_scores')
    @mock.patch.object(Standings, '_dialog_tables')
    @mock.patch('tasks.standings.standings.call_service')
    def test_index_html__finished_true(self, mock_call, mock_dialog, mock_line,
                                       mock_pending):
        date = encode_datetime(DATE_08310000)
        head = table(body=[[cell(content='Saturday')]])
        body = table(clazz='', head=[[cell(content='Pending')]])
        data_2998 = (date, body, None)

        mock_call.side_effect = [
            [TABLE_ALE, TABLE_ALC, TABLE_ALW, TABLE_ALWC],
            TABLE_AL,
            [TABLE_NLE, TABLE_NLC, TABLE_NLW, TABLE_NLWC],
            TABLE_NL,
        ]
        mock_dialog.side_effect = [
            [head, body],
            DIALOG_TABLES,
            [head, body],
            [head, body],
            DIALOG_TABLES,
        ]
        mock_line.return_value = {
            'T40': [DATA_2449, DATA_2469],
            'T47': [DATA_2449, DATA_2469]
        }
        mock_pending.return_value = {
            'T31': [data_2998],
            'T44': [data_2998],
            'T45': [data_2998]
        }

        encodings = encoding_keys()
        table_ = _table(encodings, {})
        standings = self.create_standings(_data(finished=True, table_=table_))
        standings.shadow['statsplus.table'] = STATSPLUS_TABLE
        actual = standings._index_html(date=DATE_10260602)
        expected = {
            'breadcrumbs': BREADCRUMBS,
            'recent': [TABLE_AL, TABLE_NL],
            'expanded': [
                TABLE_ALE, TABLE_ALC, TABLE_ALW, TABLE_ALWC,
                TABLE_NLE, TABLE_NLC, TABLE_NLW, TABLE_NLWC
            ],
            'dialogs': [
                dialog('31', 'Arizona Diamondbacks', [head, body]),
                dialog('40', 'Detroit Tigers', DIALOG_TABLES),
                dialog('44', 'Los Angeles Angels', [head, body]),
                dialog('45', 'Los Angeles Dodgers', [head, body]),
                dialog('47', 'Minnesota Twins', DIALOG_TABLES),
            ]
        }  # yapf: disable
        self.assertEqual(actual, expected)

        mock_call.assert_has_calls([
            mock.call('division', 'expanded_league', ('American League', [
                ('East', _table(LEAGUE_ALE, table_)),
                ('Central', _table(LEAGUE_ALC, table_)),
                ('West', _table(LEAGUE_ALW, table_)),
            ])),
            mock.call('division', 'condensed_league', ('American League', [
                ('East', _table(LEAGUE_ALE, CONDENSED_TABLE)),
                ('Central', _table(LEAGUE_ALC, CONDENSED_TABLE)),
                ('West', _table(LEAGUE_ALW, CONDENSED_TABLE)),
            ])),
            mock.call('division', 'expanded_league', ('National League', [
                ('East', _table(LEAGUE_NLE, table_)),
                ('Central', _table(LEAGUE_NLC, table_)),
                ('West', _table(LEAGUE_NLW, table_)),
            ])),
            mock.call('division', 'condensed_league', ('National League', [
                ('East', _table(LEAGUE_NLE, CONDENSED_TABLE)),
                ('Central', _table(LEAGUE_NLC, CONDENSED_TABLE)),
                ('West', _table(LEAGUE_NLW, CONDENSED_TABLE)),
            ])),
        ])
        mock_dialog.assert_has_calls([
            mock.call([data_2998]),
            mock.call([DATA_2449, DATA_2469]),
            mock.call([data_2998]),
            mock.call([data_2998]),
            mock.call([DATA_2449, DATA_2469]),
        ])
        mock_line.assert_called_once_with()
        mock_pending.assert_called_once_with()
        self.assertNotCalled(self.mock_open, self.mock_handle.write)


if __name__ in ['__main__', 'tasks.standings.standings_test']:
    main(
        StandingsTest,
        Standings,
        'tasks.standings',
        'tasks/standings', {},
        __name__ == '__main__',
        date=DATE_10260602,
        e=ENV)
