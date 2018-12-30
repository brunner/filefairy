#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for standings.py."""

import os
import re
import sys
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.extend((_path, re.sub(r'/tasks/standings', '', _path)))

from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa
from tasks.standings.standings import Standings  # noqa
from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import table  # noqa
from common.jinja2_.jinja2_ import env  # noqa
from common.json_.json_ import dumps  # noqa
from common.test.test import RMock  # noqa
from common.test.test import Suite  # noqa
from common.test.test import Test  # noqa
from common.test.test import get_testdata  # noqa
from common.test.test import main  # noqa

ENV = env()

DATE_10260602 = datetime_datetime_pst(1985, 10, 26, 6, 2, 30)

GAMES_DIR = re.sub(r'/tasks/standings', '/resource/games', _path)

TESTDATA = get_testdata(os.path.join(_path, 'testdata'))


def _data(finished=False, games=None, table_=None):
    if games is None:
        games = {}
    if table_ is None:
        table_ = {}

    return {'games': games, 'finished': finished, 'table': table_}


def _game(away_runs, away_team, home_runs, home_team):
    return {
        'away_runs': away_runs,
        'away_team': away_team,
        'home_runs': home_runs,
        'home_team': home_team,
    }


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

    def test_reload_data(self):
        standings = self.create_standings(_data())
        actual = standings._reload_data(date=DATE_10260602)
        expected = {'division': ['condensed_league']}
        self.assertEqual(actual, expected)

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

    @mock.patch.object(Standings, '_start')
    @mock.patch.object(Standings, '_parse')
    @mock.patch.object(Standings, '_finish')
    @mock.patch.object(Standings, '_clear')
    def test_notify__download_year(self, mock_clear, mock_finish, mock_parse,
                                   mock_start):
        standings = self.create_standings(_data())
        response = standings._notify_internal(notify=Notify.DOWNLOAD_YEAR)
        self.assertEqual(response, Response())

        mock_clear.assert_called_once_with(notify=Notify.DOWNLOAD_YEAR)
        self.assertNotCalled(mock_finish, mock_parse, mock_start,
                             self.mock_open, self.mock_handle.write)

    @mock.patch.object(Standings, '_start')
    @mock.patch.object(Standings, '_parse')
    @mock.patch.object(Standings, '_finish')
    @mock.patch.object(Standings, '_clear')
    def test_notify__statsplus_finish(self, mock_clear, mock_finish,
                                      mock_parse, mock_start):
        standings = self.create_standings(_data())
        response = standings._notify_internal(notify=Notify.STATSPLUS_FINISH)
        self.assertEqual(response, Response())

        mock_finish.assert_called_once_with(notify=Notify.STATSPLUS_FINISH)
        self.assertNotCalled(mock_clear, mock_parse, mock_start,
                             self.mock_open, self.mock_handle.write)

    @mock.patch.object(Standings, '_start')
    @mock.patch.object(Standings, '_parse')
    @mock.patch.object(Standings, '_finish')
    @mock.patch.object(Standings, '_clear')
    def test_notify__statsplus_parse(self, mock_clear, mock_finish, mock_parse,
                                     mock_start):
        standings = self.create_standings(_data())
        response = standings._notify_internal(notify=Notify.STATSPLUS_PARSE)
        self.assertEqual(response, Response())

        mock_parse.assert_called_once_with(notify=Notify.STATSPLUS_PARSE)
        self.assertNotCalled(mock_clear, mock_finish, mock_start,
                             self.mock_open, self.mock_handle.write)

    @mock.patch.object(Standings, '_start')
    @mock.patch.object(Standings, '_parse')
    @mock.patch.object(Standings, '_finish')
    @mock.patch.object(Standings, '_clear')
    def test_notify__statsplus_start(self, mock_clear, mock_finish, mock_parse,
                                     mock_start):
        standings = self.create_standings(_data())
        response = standings._notify_internal(notify=Notify.STATSPLUS_START)
        self.assertEqual(response, Response())

        mock_start.assert_called_once_with(notify=Notify.STATSPLUS_START)
        self.assertNotCalled(mock_clear, mock_finish, mock_parse,
                             self.mock_open, self.mock_handle.write)

    @mock.patch.object(Standings, '_finish')
    @mock.patch.object(Standings, '_clear')
    def test_notify__other(self, mock_clear, mock_finish):
        standings = self.create_standings(_data())
        response = standings._notify_internal(notify=Notify.OTHER)
        self.assertEqual(response, Response())

        self.assertNotCalled(mock_clear, mock_finish, self.mock_open,
                             self.mock_handle.write)

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

    @mock.patch.object(Standings, '_render')
    @mock.patch('common.json_.json_.open', create=True)
    @mock.patch('tasks.standings.standings.os.listdir')
    def test_finish(self, mock_listdir, mock_open, mock_render):
        mock_listdir.return_value = ['2449.json', '2469.json', '2476.json']
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

    @mock.patch.object(Standings, '_render')
    @mock.patch('common.json_.json_.open', create=True)
    @mock.patch('tasks.standings.standings.os.listdir')
    def test_parse(self, mock_listdir, mock_open, mock_render):
        mock_listdir.return_value = ['2449.json', '2469.json', '2476.json']
        suite = Suite(
            RMock(GAMES_DIR, '2469.json', TESTDATA),
            RMock(GAMES_DIR, '2476.json', TESTDATA),
        )
        mock_open.side_effect = suite.values()

        games = {'2449': _game('5', 'T40', '6', 'T47')}
        table_ = {'T40': '66-58', 'T47': '71-53'}
        standings = self.create_standings(_data(games=games, table_=table_))
        standings._parse(date=DATE_10260602)

        games = {
            '2449': _game('5', 'T40', '6', 'T47'),
            '2469': _game('0', 'T40', '7', 'T47'),
            '2476': _game('2', 'T40', '5', 'T47'),
        }
        write = _data(games=games, table_=table_)
        mock_render.assert_called_once_with(date=DATE_10260602)
        self.mock_open.assert_called_with(Standings._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    def test_start(self):
        games = {'2449': _game('5', 'T40', '6', 'T47')}
        statsplus = {'T40': '0-3', 'T47': '3-0'}
        standings = self.create_standings(_data(finished=True, games=games))
        standings.shadow['statsplus.table'] = statsplus
        standings._start(date=DATE_10260602)

        write = _data()
        self.mock_open.assert_called_with(Standings._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    maxDiff = None
    @mock.patch.object(Standings, '_call')
    def test_index_html(self, mock_call):
        condensed_al = table(
            clazz='table-fixed border mt-3',
            head=[cell(content='American League')],
            body=[[cell(content='0-0')]],
        )
        condensed_nl = table(
            clazz='table-fixed border mt-3',
            head=[cell(content='National League')],
            body=[[cell(content='0-0')]],
        )
        expanded_al_east = table(
            head=[cell(content='AL East')],
            body=[[cell(content='Baltimore')]],
        )
        expanded_al_central = table(
            head=[cell(content='AL Central')],
            body=[[cell(content='Cleveland')]])
        expanded_al_west = table(
            head=[cell(content='AL West')],
            body=[[cell(content='Houston')]],
        )
        expanded_al_wc = table(
            head=[cell(content='AL Wild Card')],
            body=[[cell(content='Boston')]],
        )
        expanded_nl_east = table(
            head=[cell(content='NL East')],
            body=[[cell(content='Atlanta')]],
        )
        expanded_nl_central = table(
            head=[cell(content='NL Central')],
            body=[[cell(content='Chicago')]])
        expanded_nl_west = table(
            head=[cell(content='NL West')],
            body=[[cell(content='Arizona')]],
        )
        expanded_nl_wc = table(
            head=[cell(content='NL Wild Card')],
            body=[[cell(content='Miami')]],
        )
        mock_call.side_effect = [
            condensed_al,
            [
                expanded_al_east,
                expanded_al_central,
                expanded_al_west,
                expanded_al_wc,
            ],
            condensed_nl,
            [
                expanded_nl_east,
                expanded_nl_central,
                expanded_nl_west,
                expanded_nl_wc,
            ],
        ]

        statsplus = {'T40': '0-3', 'T47': '3-0'}
        standings = self.create_standings(_data())
        standings.shadow['statsplus.table'] = statsplus
        standings._reload()

        breadcrumbs = [{
            'href': '/',
            'name': 'Fairylab'
        }, {
            'href': '',
            'name': 'Standings'
        }]
        actual = standings._index_html(date=DATE_10260602)
        expected = {
            'breadcrumbs':
            breadcrumbs,
            'recent': [
                condensed_al,
                condensed_nl,
            ],
            'expanded': [
                expanded_al_east,
                expanded_nl_east,
                expanded_al_central,
                expanded_nl_central,
                expanded_al_west,
                expanded_nl_west,
                expanded_al_wc,
                expanded_nl_wc,
            ],
        }
        self.assertEqual(actual, expected)

        al_east = _table(['T33', 'T34', 'T48', 'T57', 'T59'], statsplus)
        al_central = _table(['T35', 'T38', 'T40', 'T43', 'T47'], statsplus)
        al_west = _table(['T42', 'T44', 'T50', 'T54', 'T58'], statsplus)
        nl_east = _table(['T32', 'T41', 'T49', 'T51', 'T60'], statsplus)
        nl_central = _table(['T36', 'T37', 'T46', 'T52', 'T56'], statsplus)
        nl_west = _table(['T31', 'T39', 'T45', 'T53', 'T55'], statsplus)

        mock_call.assert_has_calls([
            mock.call('condensed_league', ('American League', [
                ('East', al_east),
                ('Central', al_central),
                ('West', al_west),
            ])),
            mock.call('expanded_league', ('American League', [
                ('East', al_east),
                ('Central', al_central),
                ('West', al_west),
            ])),
            mock.call('condensed_league', ('National League', [
                ('East', nl_east),
                ('Central', nl_central),
                ('West', nl_west),
            ])),
            mock.call('expanded_league', ('National League', [
                ('East', nl_east),
                ('Central', nl_central),
                ('West', nl_west),
            ])),
        ])
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
