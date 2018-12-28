#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for standings.py."""

import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.extend((_path, re.sub(r'/tasks/standings', '', _path)))

from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa
from tasks.standings.standings import Standings  # noqa
from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.jinja2_.jinja2_ import env  # noqa
from common.json_.json_ import dumps  # noqa
from common.test.test import RMock  # noqa
from common.test.test import Suite  # noqa
from common.test.test import Test  # noqa
from common.test.test import get_testdata  # noqa

ENV = env()

DATE_10260602 = datetime_datetime_pst(1985, 10, 26, 6, 2, 30)

GAMES_DIR = re.sub(r'/tasks/standings', '/resource/games', _path)

TESTDATA = get_testdata(os.path.join(_path, 'testdata'))


def _data(finished=False, games=None, table=None):
    if games is None:
        games = {}
    if table is None:
        table = {}

    return {'games': games, 'finished': finished, 'table': table}


def _game(away_runs, away_team, home_runs, home_team):
    return {
        'away_runs': away_runs,
        'away_team': away_team,
        'home_runs': home_runs,
        'home_team': home_team,
    }


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
    def test_clear(self, mock_render):
        table = {'T40': '87-75', 'T47': '91-71'}
        standings = self.create_standings(_data(table=table))
        standings._clear(date=DATE_10260602)

        table = {'T40': '0-0', 'T47': '0-0'}
        write = _data(table=table)
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

        table = {'T40': '66-58', 'T47': '71-53'}
        standings = self.create_standings(_data(table=table))
        standings._finish(date=DATE_10260602)

        table = {'T40': '66-61', 'T47': '74-53'}
        write = _data(finished=True, table=table)
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
        table = {'T40': '66-58', 'T47': '71-53'}
        standings = self.create_standings(_data(games=games, table=table))
        standings._parse(date=DATE_10260602)

        games = {
            '2449': _game('5', 'T40', '6', 'T47'),
            '2469': _game('0', 'T40', '7', 'T47'),
            '2476': _game('2', 'T40', '5', 'T47'),
        }
        write = _data(games=games, table=table)
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

    def test_index_html(self):
        standings = self.create_standings(_data())

        breadcrumbs = [{
            'href': '/',
            'name': 'Fairylab'
        }, {
            'href': '',
            'name': 'Standings'
        }]
        actual = standings._index_html(date=DATE_10260602)
        expected = {'breadcrumbs': breadcrumbs}
        self.assertEqual(actual, expected)
        self.assertNotCalled(self.mock_open, self.mock_handle.write)


if __name__ == '__main__':
    unittest.main()
