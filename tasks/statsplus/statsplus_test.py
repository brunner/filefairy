#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for statsplus.py."""

import json
import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.extend((_path, re.sub(r'/tasks/statsplus', '', _path)))

from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa
from data.shadow.shadow import Shadow  # noqa
from data.thread_.thread_ import Thread  # noqa
from tasks.statsplus.statsplus import Statsplus  # noqa
from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.datetime_.datetime_ import encode_datetime  # noqa
from common.jinja2_.jinja2_ import env  # noqa
from common.json_.json_ import dumps  # noqa
from common.test.test import Test  # noqa
from common.test.test import get_testdata  # noqa

ENV = env()

DATE_08300000 = datetime_datetime_pst(2024, 8, 30)
DATE_08310000 = datetime_datetime_pst(2024, 8, 31)
DATE_10260602 = datetime_datetime_pst(1985, 10, 26, 6, 2, 30)

EXTRACT_DIR = re.sub(r'/tasks/statsplus', '/resource/extract', _path)
EXTRACT_BOX_SCORES = os.path.join(EXTRACT_DIR, 'box_scores')
GAMES_DIR = re.sub(r'/tasks/statsplus', '/resource/games', _path)

STATSPLUS_LINK = 'https://statsplus.net/oblootp/reports/news/html'
STATSPLUS_BOX_SCORES = os.path.join(STATSPLUS_LINK, 'box_scores')

TESTDATA = get_testdata()

SCORES_ONE = ('*<game_box_2998.html|Arizona 4, Los Angeles 2>*\n'
              '*<game_box_3003.html|Atlanta 2, Baltimore 1>*\n')
SCORES_TWO = ('*<game_box_2998.html|Arizona 4, Los Angeles 2>*\n'
              '*<game_box_3003.html|Arizona 2, Los Angeles 1>*\n')

TABLE_ONE = ('Los Angeles Dodgers 97\nAtlanta Braves 77\n'
             'Arizona Diamondbacks 76\nBaltimore Orioles 70```')
TABLE_TWO = ('Los Angeles Dodgers 97\nArizona Diamondbacks 76```')


def _data(games=None, scores=None, started=False, table=None):
    if games is None:
        games = {}
    if scores is None:
        scores = {}
    if table is None:
        table = {}

    return {
        'games': games,
        'scores': scores,
        'started': started,
        'table': table,
    }


class StatsplusTest(Test):
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

    def create_statsplus(self, data):
        self.init_mocks(data)
        statsplus = Statsplus(date=DATE_10260602, e=ENV)

        self.mock_open.assert_called_once_with(Statsplus._data(), 'r')
        self.mock_handle.write.assert_not_called()

        self.reset_mocks()
        self.init_mocks(data)

        return statsplus

    def test_reload_data(self):
        statsplus = self.create_statsplus(_data())
        actual = statsplus._reload_data(date=DATE_10260602)
        expected = {'statslab': ['parse_score']}
        self.assertEqual(actual, expected)

        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    def test_shadow_data(self):
        date = encode_datetime(DATE_08310000)
        scores = {date: {'2998': 'T31 4, TLA 2'}}
        table = {'T32': '1-0', 'T45': '0-1'}
        statsplus = self.create_statsplus(_data(scores=scores, table=table))
        actual = statsplus._shadow_data(date=DATE_10260602)
        shadow = statsplus._shadow_scores() + statsplus._shadow_table()
        self.assertEqual(actual, shadow)

        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    def test_shadow_scores(self):
        date = encode_datetime(DATE_08310000)
        scores = {date: {'2998': 'T31 4, TLA 2'}}
        table = {'T32': '1-0', 'T45': '0-1'}
        statsplus = self.create_statsplus(_data(scores=scores, table=table))
        actual = statsplus._shadow_scores()
        shadow = Shadow(
            destination='standings',
            key='statsplus.scores',
            info=scores,
        )
        self.assertEqual(actual, [shadow])

        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    def test_shadow_table(self):
        date = encode_datetime(DATE_08310000)
        scores = {date: {'2998': 'T31 4, TLA 2'}}
        table = {'T32': '1-0', 'T45': '0-1'}
        statsplus = self.create_statsplus(_data(scores=scores, table=table))
        actual = statsplus._shadow_table()
        shadow = Shadow(
            destination='standings',
            key='statsplus.table',
            info=table,
        )
        self.assertEqual(actual, [shadow])

        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    def test_notify__download_finish(self):
        statsplus = self.create_statsplus(_data(started=True))
        response = statsplus._notify_internal(notify=Notify.DOWNLOAD_FINISH)
        expected = Response(thread_=[Thread(target='_parse_extracted_scores')])
        self.assertEqual(response, expected)

        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    def test_notify__other(self):
        statsplus = self.create_statsplus(_data(started=True))
        response = statsplus._notify_internal(notify=Notify.OTHER)
        expected = Response()
        self.assertEqual(response, expected)

        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    @mock.patch.object(Statsplus, '_valid')
    @mock.patch.object(Statsplus, '_save_table')
    @mock.patch.object(Statsplus, '_start')
    @mock.patch.object(Statsplus, '_save_scores')
    def test_on_message__date(self, mock_scores, mock_start, mock_table,
                              mock_valid):
        mock_valid.return_value = True

        text = '08/30/2024 Final Scores'
        obj = {'bot_id': 'B7KJ3362Y', 'channel': 'C7JSGHW8G', 'text': text}

        statsplus = self.create_statsplus(_data())
        statsplus.shadow['download.end'] = encode_datetime(DATE_08310000)

        actual = statsplus._on_message_internal(obj=obj)
        self.assertEqual(actual, Response())

        mock_valid.assert_called_once_with(obj)
        self.assertNotCalled(mock_scores, mock_start, mock_table,
                             self.mock_open, self.mock_handle.write)

    @mock.patch.object(Statsplus, '_valid')
    @mock.patch.object(Statsplus, '_save_table')
    @mock.patch.object(Statsplus, '_start')
    @mock.patch.object(Statsplus, '_save_scores')
    def test_on_message__save_scores(self, mock_scores, mock_start, mock_table,
                                     mock_valid):
        response = Response(notify=[Notify.OTHER])
        mock_scores.return_value = response
        mock_valid.return_value = True

        text = '08/31/2024 MAJOR LEAGUE BASEBALL Final Scores\n' + SCORES_ONE
        obj = {'bot_id': 'B7KJ3362Y', 'channel': 'C7JSGHW8G', 'text': text}

        statsplus = self.create_statsplus(_data(started=True))
        statsplus.shadow['download.end'] = encode_datetime(DATE_08300000)

        actual = statsplus._on_message_internal(obj=obj)
        self.assertEqual(actual, response)

        mock_scores.assert_called_once_with(
            encode_datetime(DATE_08310000), text)
        mock_valid.assert_called_once_with(obj)
        self.assertNotCalled(mock_start, mock_table, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Statsplus, '_valid')
    @mock.patch.object(Statsplus, '_save_table')
    @mock.patch.object(Statsplus, '_start')
    @mock.patch.object(Statsplus, '_save_scores')
    def test_on_message__save_table(self, mock_scores, mock_start, mock_table,
                                    mock_valid):
        response = Response(notify=[Notify.OTHER])
        mock_table.return_value = response
        mock_valid.return_value = True

        text = '```MAJOR LEAGUE BASEBALL Live Table - 08/31/2024\n' + TABLE_ONE
        obj = {'bot_id': 'B7KJ3362Y', 'channel': 'C7JSGHW8G', 'text': text}

        statsplus = self.create_statsplus(_data(started=True))
        statsplus.shadow['download.end'] = encode_datetime(DATE_08300000)

        actual = statsplus._on_message_internal(obj=obj)
        self.assertEqual(actual, response)

        mock_table.assert_called_once_with(
            encode_datetime(DATE_08310000), text)
        mock_valid.assert_called_once_with(obj)
        self.assertNotCalled(mock_scores, mock_start, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Statsplus, '_valid')
    @mock.patch.object(Statsplus, '_save_table')
    @mock.patch.object(Statsplus, '_start')
    @mock.patch.object(Statsplus, '_save_scores')
    def test_on_message__start(self, mock_scores, mock_start, mock_table,
                               mock_valid):
        response = Response(notify=[Notify.OTHER])
        mock_start.return_value = response
        mock_valid.return_value = True

        text = '08/31/2024 Final Scores'
        obj = {'bot_id': 'B7KJ3362Y', 'channel': 'C7JSGHW8G', 'text': text}

        statsplus = self.create_statsplus(_data())
        statsplus.shadow['download.end'] = encode_datetime(DATE_08300000)

        actual = statsplus._on_message_internal(obj=obj)
        self.assertEqual(actual, response)

        mock_start.assert_called_once_with()
        mock_valid.assert_called_once_with(obj)
        self.assertNotCalled(mock_scores, mock_table, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Statsplus, '_rm')
    @mock.patch.object(Statsplus, '_parse_score')
    @mock.patch('tasks.statsplus.statsplus.loads')
    @mock.patch('tasks.statsplus.statsplus.os.listdir')
    def test_parse_extracted_scores__started_false(
            self, mock_listdir, mock_loads, mock_parse, mock_rm):
        mock_listdir.side_effect = [
            ['game_box_2449.html', 'game_box_2469.html'],
            ['2449.json', '2469.json'],
        ]
        mock_loads.side_effect = [
            json.loads(TESTDATA['2449.json']),
            json.loads(TESTDATA['2469.json'])
        ]

        statsplus = self.create_statsplus(_data())
        actual = statsplus._parse_extracted_scores()
        expected = Response(
            shadow=statsplus._shadow_data(), notify=[Notify.STATSPLUS_FINISH])
        self.assertEqual(actual, expected)

        write = _data(table={'T40': '0-2', 'T47': '2-0'})
        mock_listdir.assert_has_calls([
            mock.call(EXTRACT_BOX_SCORES), mock.call(GAMES_DIR)])
        mock_loads.assert_has_calls([
            mock.call(os.path.join(GAMES_DIR, '2449.json')),
            mock.call(os.path.join(GAMES_DIR, '2469.json'))
        ])
        mock_parse.assert_has_calls([
            mock.call('2449', None),
            mock.call('2469', None),
        ])
        mock_rm.assert_called_once_with()
        self.mock_open.assert_called_with(Statsplus._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch.object(Statsplus, '_rm')
    @mock.patch.object(Statsplus, '_parse_score')
    @mock.patch('tasks.statsplus.statsplus.loads')
    @mock.patch('tasks.statsplus.statsplus.os.listdir')
    def test_parse_extracted_scores__started_true(
            self, mock_listdir, mock_loads, mock_parse, mock_rm):
        mock_listdir.side_effect = [
            ['game_box_2449.html', 'game_box_2469.html'],
            ['2449.json', '2469.json'],
        ]
        mock_loads.side_effect = [
            json.loads(TESTDATA['2449.json']),
            json.loads(TESTDATA['2469.json'])
        ]

        statsplus = self.create_statsplus(_data(started=True))
        actual = statsplus._parse_extracted_scores()
        expected = Response(
            shadow=statsplus._shadow_data(), notify=[Notify.STATSPLUS_FINISH])
        self.assertEqual(actual, expected)

        write = _data(table={'T40': '0-2', 'T47': '2-0'})
        mock_listdir.assert_has_calls([
            mock.call(EXTRACT_BOX_SCORES), mock.call(GAMES_DIR)])
        mock_loads.assert_has_calls([
            mock.call(os.path.join(GAMES_DIR, '2449.json')),
            mock.call(os.path.join(GAMES_DIR, '2469.json'))
        ])
        mock_parse.assert_has_calls([
            mock.call('2449', None),
            mock.call('2469', None),
        ])
        self.mock_open.assert_called_with(Statsplus._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.assertNotCalled(mock_rm)

    @mock.patch.object(Statsplus, '_parse_score')
    def test_parse_saved_scores__none(self, mock_parse):
        mock_parse.return_value = None

        date = encode_datetime(DATE_08310000)
        scores = {date: {'2998': 'T31 4, TLA 2', '3003': 'T32 2, T33 1'}}
        statsplus = self.create_statsplus(_data(scores=scores))
        actual = statsplus._parse_saved_scores(date)
        expected = Response(
            thread_=[Thread(target='_parse_saved_scores', args=(date, ))])
        self.assertEqual(actual, expected)

        mock_parse.assert_has_calls([
            mock.call('2998', date),
            mock.call('3003', date),
        ])
        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    @mock.patch.object(Statsplus, '_parse_score')
    def test_parse_saved_scores__some(self, mock_parse):
        mock_parse.side_effect = [True, None]

        date = encode_datetime(DATE_08310000)
        scores = {date: {'2998': 'T31 4, TLA 2', '3003': 'T32 2, T33 1'}}
        statsplus = self.create_statsplus(_data(scores=scores))
        actual = statsplus._parse_saved_scores(date)
        thread_ = Thread(target='_parse_saved_scores', args=(date, ))
        expected = Response(
            notify=[Notify.STATSPLUS_PARSE],
            shadow=statsplus._shadow_scores(),
            thread_=[thread_])
        self.assertEqual(actual, expected)

        write = _data(scores={date: {'3003': 'T32 2, T33 1'}})
        mock_parse.assert_has_calls([
            mock.call('2998', date),
            mock.call('3003', date),
        ])
        self.mock_open.assert_called_with(Statsplus._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch.object(Statsplus, '_parse_score')
    def test_parse_saved_scores__true(self, mock_parse):
        mock_parse.return_value = True

        date = encode_datetime(DATE_08310000)
        scores = {date: {'2998': 'T31 4, TLA 2', '3003': 'T32 2, T33 1'}}
        statsplus = self.create_statsplus(_data(scores=scores))
        actual = statsplus._parse_saved_scores(date)
        expected = Response(
            notify=[Notify.STATSPLUS_PARSE], shadow=statsplus._shadow_scores())
        self.assertEqual(actual, expected)

        write = _data()
        mock_parse.assert_has_calls([
            mock.call('2998', date),
            mock.call('3003', date),
        ])
        self.mock_open.assert_called_with(Statsplus._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch('tasks.statsplus.statsplus.os.path.isfile')
    @mock.patch.object(Statsplus, '_call')
    def test_parse_score__isfile(self, mock_call, mock_isfile):
        mock_isfile.return_value = True

        date = encode_datetime(DATE_08310000)
        statsplus = self.create_statsplus(_data())
        actual = statsplus._parse_score('2998', date)
        self.assertEqual(actual, True)

        mock_isfile.assert_called_once_with(
            os.path.join(GAMES_DIR, '2998.json'))
        self.assertNotCalled(mock_call, self.mock_open, self.mock_handle.write)

    @mock.patch('tasks.statsplus.statsplus.os.path.isfile')
    @mock.patch.object(Statsplus, '_call')
    def test_parse_score__none(self, mock_call, mock_isfile):
        mock_call.return_value = None
        mock_isfile.return_value = False

        date = encode_datetime(DATE_08310000)
        statsplus = self.create_statsplus(_data())
        actual = statsplus._parse_score('2998', date)
        self.assertEqual(actual, None)

        in_ = os.path.join(EXTRACT_BOX_SCORES, 'game_box_2998.html')
        out = os.path.join(GAMES_DIR, '2998.json')
        mock_call.assert_called_once_with('parse_score', (in_, out, date))
        mock_isfile.assert_called_once_with(out)
        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    @mock.patch('tasks.statsplus.statsplus.os.path.isfile')
    @mock.patch.object(Statsplus, '_call')
    def test_parse_score__started(self, mock_call, mock_isfile):
        mock_call.return_value = True
        mock_isfile.return_value = False

        date = encode_datetime(DATE_08310000)
        statsplus = self.create_statsplus(_data(started=True))
        actual = statsplus._parse_score('2998', date)
        self.assertEqual(actual, True)

        in_ = os.path.join(STATSPLUS_BOX_SCORES, 'game_box_2998.html')
        out = os.path.join(GAMES_DIR, '2998.json')
        mock_call.assert_called_once_with('parse_score', (in_, out, date))
        mock_isfile.assert_called_once_with(out)
        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    @mock.patch('tasks.statsplus.statsplus.os.path.isfile')
    @mock.patch.object(Statsplus, '_call')
    def test_parse_score__true(self, mock_call, mock_isfile):
        mock_call.return_value = True
        mock_isfile.return_value = False

        date = encode_datetime(DATE_08310000)
        statsplus = self.create_statsplus(_data())
        actual = statsplus._parse_score('2998', date)
        self.assertEqual(actual, True)

        in_ = os.path.join(EXTRACT_BOX_SCORES, 'game_box_2998.html')
        out = os.path.join(GAMES_DIR, '2998.json')
        mock_call.assert_called_once_with('parse_score', (in_, out, date))
        mock_isfile.assert_called_once_with(out)
        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    def test_save_scores__one(self):
        date = encode_datetime(DATE_08310000)
        text = '08/31/2024 MAJOR LEAGUE BASEBALL Final Scores\n' + SCORES_ONE

        statsplus = self.create_statsplus(_data())
        actual = statsplus._save_scores(date, text)
        expected = Response(
            shadow=statsplus._shadow_scores(),
            thread_=[Thread(target='_parse_saved_scores', args=(date, ))])
        self.assertEqual(actual, expected)

        scores = {date: {'2998': 'T31 4, TLA 2', '3003': 'T32 2, T33 1'}}
        write = _data(scores=scores)
        self.mock_open.assert_called_with(Statsplus._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    def test_save_scores__two(self):
        date = encode_datetime(DATE_08310000)
        text = '08/31/2024 MAJOR LEAGUE BASEBALL Final Scores\n' + SCORES_TWO

        statsplus = self.create_statsplus(_data())
        actual = statsplus._save_scores(date, text)
        expected = Response(
            shadow=statsplus._shadow_scores(),
            thread_=[Thread(target='_parse_saved_scores', args=(date, ))])
        self.assertEqual(actual, expected)

        games = {date: {'T31': 2, 'TLA': 2}}
        scores = {date: {'2998': 'T31 4, TLA 2', '3003': 'T31 2, TLA 1'}}
        write = _data(games=games, scores=scores)
        self.mock_open.assert_called_with(Statsplus._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    def test_save_table__one(self):
        date = encode_datetime(DATE_08310000)
        text = '```MAJOR LEAGUE BASEBALL Live Table - 08/31/2024\n' + TABLE_ONE

        table = {'T31': '3-3', 'T32': '2-4', 'T33': '2-4', 'T45': '5-1'}
        standings = {
            'T31': '72-83',
            'T32': '74-81',
            'T33': '68-87',
            'T45': '92-63'
        }

        statsplus = self.create_statsplus(_data(table=table))
        statsplus.shadow['standings.table'] = standings
        actual = statsplus._save_table(date, text)
        expected = Response(shadow=statsplus._shadow_table())
        self.assertEqual(actual, expected)

        table = {'T31': '4-3', 'T32': '3-4', 'T33': '2-5', 'T45': '5-2'}
        write = _data(table=table)
        self.mock_open.assert_called_with(Statsplus._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    def test_save_table__two(self):
        date = encode_datetime(DATE_08310000)
        text = '```MAJOR LEAGUE BASEBALL Live Table - 08/31/2024\n' + TABLE_TWO

        games = {date: {'T31': 2, 'TLA': 2}}
        table = {'T31': '2-3', 'T45': '5-0'}
        standings = {'T31': '72-83', 'T45': '92-63'}

        statsplus = self.create_statsplus(_data(games=games, table=table))
        statsplus.shadow['standings.table'] = standings
        actual = statsplus._save_table(date, text)
        expected = Response(shadow=statsplus._shadow_table())
        self.assertEqual(actual, expected)

        table = {'T31': '4-3', 'T45': '5-1'}
        write = _data(table=table)
        self.mock_open.assert_called_with(Statsplus._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch('tasks.statsplus.statsplus.check_output')
    def test_rm(self, mock_check):
        statsplus = self.create_statsplus(_data())
        statsplus._rm()

        mock_check.assert_has_calls([
            mock.call(['rm', '-rf', GAMES_DIR]),
            mock.call(['mkdir', GAMES_DIR]),
        ])
        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    @mock.patch.object(Statsplus, '_rm')
    def test_start(self, mock_rm):
        date = encode_datetime(DATE_08310000)
        games = {date: {'T31': 2, 'TLA': 2}}
        scores = {date: {'2998': 'T31 4, TLA 2'}}
        table = {'T32': '1-0', 'T45': '0-1'}
        statsplus = self.create_statsplus(
            _data(games=games, scores=scores, table=table))
        statsplus._start()

        write = _data(started=True)
        mock_rm.assert_called_once_with()
        self.mock_open.assert_called_with(Statsplus._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    def test_valid__false(self):
        obj = {'bot_id': 'B123', 'channel': 'C123', 'text': 'foo'}

        statsplus = self.create_statsplus(_data())
        actual = statsplus._valid(obj)
        expected = False
        self.assertEqual(actual, expected)

    def test_valid__true(self):
        obj = {'bot_id': 'B7KJ3362Y', 'channel': 'C7JSGHW8G', 'text': 'foo'}

        statsplus = self.create_statsplus(_data())
        actual = statsplus._valid(obj)
        expected = True
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
