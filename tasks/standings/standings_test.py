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
from common.teams.teams import icon_absolute  # noqa
from common.test.test import RMock  # noqa
from common.test.test import Suite  # noqa
from common.test.test import Test  # noqa
from common.test.test import get_testdata  # noqa
from common.test.test import main  # noqa
from tasks.standings.standings import Standings  # noqa
from types_.notify.notify import Notify  # noqa
from types_.response.response import Response  # noqa

ENV = env()

DATE_08300000 = datetime_datetime_pst(2024, 8, 30)
DATE_08310000 = datetime_datetime_pst(2024, 8, 31)
DATE_10260602 = datetime_datetime_pst(1985, 10, 26, 6, 2, 30)

GAMES_DIR = re.sub(r'/tasks/standings', '/resources/games', _path)

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

ICON_31 = icon_absolute('T31', 'Arizona Diamondbacks')
ICON_40 = icon_absolute('T40', 'Detroit Tigers')
ICON_44 = icon_absolute('T44', 'Los Angeles Angels')
ICON_45 = icon_absolute('T45', 'Los Angeles Dodgers')
ICON_47 = icon_absolute('T47', 'Minnesota Twins')

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
        open_patch = mock.patch('common.io_.io_.open', create=True)
        self.addCleanup(open_patch.stop)
        self.open_ = open_patch.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.open_handle_ = mo()
        self.open_.side_effect = [mo.return_value]

    def reset_mocks(self):
        self.open_handle_.write.reset_mock()

    def create_standings(self, data):
        self.init_mocks(data)
        standings = Standings(date=DATE_10260602, e=ENV)

        self.reset_mocks()
        self.init_mocks(data)

        return standings

    @mock.patch.object(Standings, 'get_standings_html')
    def test_render_data(self, get_standings_html_):
        standings_html = {'dialogs': []}
        get_standings_html_.return_value = standings_html

        standings = self.create_standings(_data())
        actual = standings._render_data(date=DATE_10260602)
        expected = [('standings/index.html', '', 'standings.html',
                     standings_html)]
        self.assertEqual(actual, expected)

        get_standings_html_.assert_called_once_with(date=DATE_10260602)
        self.assertNotCalled(self.open_handle_.write)

    @mock.patch.object(Standings, '_render')
    @mock.patch.object(Standings, 'handle_start')
    @mock.patch.object(Standings, 'handle_finish')
    @mock.patch.object(Standings, 'clear_standings')
    def test_notify__download_year(self, clear_standings_, handle_finish_,
                                   handle_start_, _render_):
        standings = self.create_standings(_data())
        response = standings._notify_internal(notify=Notify.DOWNLOAD_YEAR)
        self.assertEqual(response, Response())

        clear_standings_.assert_called_once_with(notify=Notify.DOWNLOAD_YEAR)
        self.assertNotCalled(handle_finish_, handle_start_, _render_,
                             self.open_handle_.write)

    @mock.patch.object(Standings, '_render')
    @mock.patch.object(Standings, 'handle_start')
    @mock.patch.object(Standings, 'handle_finish')
    @mock.patch.object(Standings, 'clear_standings')
    def test_notify__statsplus_finish(self, clear_standings_, handle_finish_,
                                      handle_start_, _render_):
        standings = self.create_standings(_data())
        response = standings._notify_internal(notify=Notify.STATSPLUS_FINISH)
        self.assertEqual(response, Response())

        handle_finish_.assert_called_once_with(notify=Notify.STATSPLUS_FINISH)
        self.assertNotCalled(clear_standings_, handle_start_, _render_,
                             self.open_handle_.write)

    @mock.patch.object(Standings, '_render')
    @mock.patch.object(Standings, 'handle_start')
    @mock.patch.object(Standings, 'handle_finish')
    @mock.patch.object(Standings, 'clear_standings')
    def test_notify__statsplus_render(self, clear_standings_, handle_finish_,
                                      handle_start_, _render_):
        standings = self.create_standings(_data())
        response = standings._notify_internal(notify=Notify.STATSPLUS_PARSE)
        self.assertEqual(response, Response())

        _render_.assert_called_once_with(notify=Notify.STATSPLUS_PARSE)
        self.assertNotCalled(clear_standings_, handle_finish_, handle_start_,
                             self.open_handle_.write)

    @mock.patch.object(Standings, '_render')
    @mock.patch.object(Standings, 'handle_start')
    @mock.patch.object(Standings, 'handle_finish')
    @mock.patch.object(Standings, 'clear_standings')
    def test_notify__statsplus_save(self, clear_standings_, handle_finish_,
                                    handle_start_, _render_):
        standings = self.create_standings(_data())
        response = standings._notify_internal(notify=Notify.STATSPLUS_SAVE)
        self.assertEqual(response, Response())

        _render_.assert_called_once_with(notify=Notify.STATSPLUS_SAVE)
        self.assertNotCalled(clear_standings_, handle_finish_, handle_start_,
                             self.open_handle_.write)

    @mock.patch.object(Standings, '_render')
    @mock.patch.object(Standings, 'handle_start')
    @mock.patch.object(Standings, 'handle_finish')
    @mock.patch.object(Standings, 'clear_standings')
    def test_notify__statsplus_start(self, clear_standings_, handle_finish_,
                                     handle_start_, _render_):
        standings = self.create_standings(_data())
        response = standings._notify_internal(notify=Notify.STATSPLUS_START)
        self.assertEqual(response, Response())

        handle_start_.assert_called_once_with(notify=Notify.STATSPLUS_START)
        self.assertNotCalled(clear_standings_, handle_finish_, _render_,
                             self.open_handle_.write)

    @mock.patch.object(Standings, '_render')
    @mock.patch.object(Standings, 'handle_start')
    @mock.patch.object(Standings, 'handle_finish')
    @mock.patch.object(Standings, 'clear_standings')
    def test_notify__other(self, clear_standings_, handle_finish_,
                           handle_start_, _render_):
        standings = self.create_standings(_data())
        response = standings._notify_internal(notify=Notify.OTHER)
        self.assertEqual(response, Response())

        self.assertNotCalled(clear_standings_, handle_finish_, handle_start_,
                             _render_, self.open_handle_.write)

    @mock.patch.object(Standings, '_render')
    def test_clear_standings(self, _render_):
        table_ = {'T40': '87-75', 'T47': '91-71'}
        standings = self.create_standings(_data(table_=table_))
        standings.clear_standings(date=DATE_10260602)

        table_ = {'T40': '0-0', 'T47': '0-0'}
        write = _data(table_=table_)
        _render_.assert_called_once_with(date=DATE_10260602)
        self.open_handle_.write.assert_called_once_with(dumps(write) + '\n')

    def test_create_dialog_tables(self):
        date_0830 = encode_datetime(DATE_08300000)
        date_0831 = encode_datetime(DATE_08310000)
        body = table(head=[[cell(content='Pending')]])
        data = [
            (date_0830, BODY_2449, FOOT_2449),
            (date_0831, BODY_2469, FOOT_2469),
            (date_0831, body, None),
        ]

        head_0830 = topper('Friday, August 30th, 2024')
        head_0831 = topper('Saturday, August 31st, 2024')
        standings = self.create_standings(_data())
        actual = standings.create_dialog_tables(data)
        expected = [
            head_0830, BODY_2449, FOOT_2449,
            head_0831, BODY_2469, FOOT_2469,
            body
        ]  # yapf: disable
        self.assertEqual(actual, expected)

        self.assertNotCalled(self.open_handle_.write)

    @mock.patch.object(Standings, '_render')
    @mock.patch('common.json_.json_.open', create=True)
    @mock.patch('tasks.standings.standings.os.listdir')
    def test_handle_finish(self, listdir_, open_, _render_):
        listdir_.return_value = ['2449.json', '2469.json', '2476.json']
        suite = Suite(
            RMock(GAMES_DIR, '2449.json', TESTDATA),
            RMock(GAMES_DIR, '2469.json', TESTDATA),
            RMock(GAMES_DIR, '2476.json', TESTDATA),
        )
        open_.side_effect = suite.values()

        table_ = {'T40': '66-58', 'T47': '71-53'}
        standings = self.create_standings(_data(table_=table_))
        standings.handle_finish(date=DATE_10260602)

        table_ = {'T40': '66-61', 'T47': '74-53'}
        write = _data(finished=True, table_=table_)
        _render_.assert_called_once_with(date=DATE_10260602)
        self.open_handle_.write.assert_called_once_with(dumps(write) + '\n')

    def test_handle_start(self):
        standings = self.create_standings(_data(finished=True))

        standings.handle_start(date=DATE_10260602)

        write = _data()
        self.open_handle_.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch('tasks.standings.standings.os.listdir')
    @mock.patch.object(Standings, 'create_dialog_tables')
    @mock.patch('tasks.standings.standings.call_service')
    def test_get_standings_html__finished_false(self, call_service_,
                                                create_dialog_tables_,
                                                listdir_):
        date = encode_datetime(DATE_08310000)
        head = table(body=[[cell(content='Saturday')]])
        body = table(head=[[cell(content='Pending')]])
        data_2998 = (date, body, None)

        line = {'T40': [DATA_2449, DATA_2469], 'T47': [DATA_2449, DATA_2469]}
        pending = {'T31': [data_2998], 'T44': [data_2998], 'T45': [data_2998]}
        call_service_.side_effect = [
            {
                'dialogs': [],
                'scores': line
            },
            pending,
            [TABLE_ALE, TABLE_ALC, TABLE_ALW, TABLE_ALWC],
            TABLE_AL,
            [TABLE_NLE, TABLE_NLC, TABLE_NLW, TABLE_NLWC],
            TABLE_NL,
        ]

        ds = [HEAD_2449, BODY_2449, FOOT_2449, HEAD_2469, BODY_2469, FOOT_2469]
        create_dialog_tables_.side_effect = [
            [head, body],
            [HEAD_2449, BODY_2449, FOOT_2449, HEAD_2469, BODY_2469, FOOT_2469],
            [head, body],
            [head, body],
            [HEAD_2449, BODY_2449, FOOT_2449, HEAD_2469, BODY_2469, FOOT_2469],
        ]

        listdir_.return_value = ['2449.json', '2469.json', '2998.json']

        encodings = encoding_keys()
        table_ = _table(encodings, {})
        standings = self.create_standings(_data(table_=table_))

        date = encode_datetime(DATE_08310000)
        score = 'T31 4, TLA 2'
        statsplus_scores = {date: {'2998': score}}
        statsplus_table = {'T40': '0-2', 'T47': '2-0'}
        statsplus_data = {'scores': statsplus_scores, 'table': statsplus_table}
        self.init_mocks(statsplus_data)

        actual = standings.get_standings_html(date=DATE_10260602)
        expected = {
            'recent': [TABLE_AL, TABLE_NL],
            'expanded': [
                TABLE_ALE, TABLE_ALC, TABLE_ALW, TABLE_ALWC,
                TABLE_NLE, TABLE_NLC, TABLE_NLW, TABLE_NLWC
            ],
            'dialogs': [
                dialog(id_='diamondbacks', icon=ICON_31, tables=[head, body]),
                dialog(id_='tigers', icon=ICON_40, tables=ds),
                dialog(id_='angels', icon=ICON_44, tables=[head, body]),
                dialog(id_='dodgers', icon=ICON_45, tables=[head, body]),
                dialog(id_='twins', icon=ICON_47, tables=ds),
            ]
        }  # yapf: disable
        self.assertEqual(actual, expected)

        etable = {'T31': '1-0', 'T40': '0-2', 'T47': '2-0', 'TLA': '0-1'}
        rtable = {
            e: (etable.get(e, '0-0'), e in ['T31', 'T40', 'T44', 'T45', 'T47'])
            for e in ENCODINGS
        }
        call_service_.assert_has_calls([
            mock.call('scoreboard', 'line_scores',
                      (['2449', '2469', '2998'], )),
            mock.call('scoreboard', 'pending_dialog', (statsplus_scores, )),
            mock.call('division', 'expanded_league', ('American League', [
                ('East', _table(LEAGUE_ALE, etable)),
                ('Central', _table(LEAGUE_ALC, etable)),
                ('West', _table(LEAGUE_ALW, etable)),
            ])),
            mock.call('division', 'condensed_league', ('American League', [
                ('East', _table(LEAGUE_ALE, rtable)),
                ('Central', _table(LEAGUE_ALC, rtable)),
                ('West', _table(LEAGUE_ALW, rtable)),
            ])),
            mock.call('division', 'expanded_league', ('National League', [
                ('East', _table(LEAGUE_NLE, etable)),
                ('Central', _table(LEAGUE_NLC, etable)),
                ('West', _table(LEAGUE_NLW, etable)),
            ])),
            mock.call('division', 'condensed_league', ('National League', [
                ('East', _table(LEAGUE_NLE, rtable)),
                ('Central', _table(LEAGUE_NLC, rtable)),
                ('West', _table(LEAGUE_NLW, rtable)),
            ])),
        ])
        create_dialog_tables_.assert_has_calls([
            mock.call([data_2998]),
            mock.call([DATA_2449, DATA_2469]),
            mock.call([data_2998]),
            mock.call([data_2998]),
            mock.call([DATA_2449, DATA_2469]),
        ])
        self.assertNotCalled(self.open_handle_.write)

    @mock.patch('tasks.standings.standings.os.listdir')
    @mock.patch.object(Standings, 'create_dialog_tables')
    @mock.patch('tasks.standings.standings.call_service')
    def test_get_standings_html__finished_true(self, call_service_,
                                               create_dialog_tables_,
                                               listdir_):
        date = encode_datetime(DATE_08310000)
        head = table(body=[[cell(content='Saturday')]])
        body = table(head=[[cell(content='Final')]])
        foot = table(foot=[[cell(content='Diamondbacks')]])
        data_2998 = (date, body, foot)
        tables_2998 = [head, body, foot]

        line = {
            'T31': [data_2998],
            'T40': [DATA_2449, DATA_2469],
            'T45': [data_2998],
            'T47': [DATA_2449, DATA_2469]
        }
        call_service_.side_effect = [
            {
                'dialogs': [],
                'scores': line
            },
            {},
            [TABLE_ALE, TABLE_ALC, TABLE_ALW, TABLE_ALWC],
            TABLE_AL,
            [TABLE_NLE, TABLE_NLC, TABLE_NLW, TABLE_NLWC],
            TABLE_NL,
        ]

        ds = [HEAD_2449, BODY_2449, FOOT_2449, HEAD_2469, BODY_2469, FOOT_2469]
        create_dialog_tables_.side_effect = [tables_2998, ds, tables_2998, ds]

        listdir_.return_value = ['2449.json', '2469.json', '2998.json']

        encodings = encoding_keys()
        table_ = _table(encodings, {})
        standings = self.create_standings(_data(finished=True, table_=table_))

        statsplus_table = {
            'T31': '1-0',
            'T40': '0-2',
            'T45': '0-1',
            'T47': '2-0'
        }
        statsplus_data = {'scores': {}, 'table': statsplus_table}
        self.init_mocks(statsplus_data)

        actual = standings.get_standings_html(date=DATE_10260602)
        expected = {
            'recent': [TABLE_AL, TABLE_NL],
            'expanded': [
                TABLE_ALE, TABLE_ALC, TABLE_ALW, TABLE_ALWC,
                TABLE_NLE, TABLE_NLC, TABLE_NLW, TABLE_NLWC
            ],
            'dialogs': [
                dialog(id_='diamondbacks', icon=ICON_31, tables=tables_2998),
                dialog(id_='tigers', icon=ICON_40, tables=ds),
                dialog(id_='dodgers', icon=ICON_45, tables=tables_2998),
                dialog(id_='twins', icon=ICON_47, tables=ds),
            ]
        }  # yapf: disable
        self.assertEqual(actual, expected)

        etable = {'T31': '1-0', 'T40': '0-2', 'T45': '0-1', 'T47': '2-0'}
        rtable = {e: (etable.get(e, '0-0'), e in etable) for e in ENCODINGS}
        call_service_.assert_has_calls([
            mock.call('scoreboard', 'line_scores',
                      (['2449', '2469', '2998'], )),
            mock.call('scoreboard', 'pending_dialog', ({}, )),
            mock.call('division', 'expanded_league', ('American League', [
                ('East', _table(LEAGUE_ALE, table_)),
                ('Central', _table(LEAGUE_ALC, table_)),
                ('West', _table(LEAGUE_ALW, table_)),
            ])),
            mock.call('division', 'condensed_league', ('American League', [
                ('East', _table(LEAGUE_ALE, rtable)),
                ('Central', _table(LEAGUE_ALC, rtable)),
                ('West', _table(LEAGUE_ALW, rtable)),
            ])),
            mock.call('division', 'expanded_league', ('National League', [
                ('East', _table(LEAGUE_NLE, table_)),
                ('Central', _table(LEAGUE_NLC, table_)),
                ('West', _table(LEAGUE_NLW, table_)),
            ])),
            mock.call('division', 'condensed_league', ('National League', [
                ('East', _table(LEAGUE_NLE, rtable)),
                ('Central', _table(LEAGUE_NLC, rtable)),
                ('West', _table(LEAGUE_NLW, rtable)),
            ])),
        ])
        create_dialog_tables_.assert_has_calls([
            mock.call([data_2998]),
            mock.call([DATA_2449, DATA_2469]),
            mock.call([data_2998]),
            mock.call([DATA_2449, DATA_2469]),
        ])
        self.assertNotCalled(self.open_handle_.write)


if __name__ in ['__main__', 'tasks.standings.standings_test']:
    main(StandingsTest,
         Standings,
         'tasks.standings',
         'tasks/standings', {},
         __name__ == '__main__',
         date=DATE_10260602,
         e=ENV)
