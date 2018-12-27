#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for statsplus.py."""

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

ENV = env()

DATE_08300000 = datetime_datetime_pst(2024, 8, 30)
DATE_08310000 = datetime_datetime_pst(2024, 8, 31)
DATE_10260602 = datetime_datetime_pst(1985, 10, 26, 6, 2, 30)

EXTRACT_DIR = re.sub(r'/tasks/statsplus', '/resource/extract', _path)
GAMES_DIR = re.sub(r'/tasks/statsplus', '/resource/games', _path)
RESOURCE_DIR = re.sub(r'/tasks/statsplus', '/resource', _path)

SCORES_MSG = ('*<game_box_2998.html|Arizona 4, Los Angeles 2>*\n'
              '*<game_box_3003.html|Atlanta 2, Baltimore 1>*\n'
              '*<game_box_2996.html|Cincinnati 7, Milwaukee 2>*\n'
              '*<game_box_3002.html|Detroit 11, Chicago 4>*\n'
              '*<game_box_2993.html|Houston 7, Seattle 2>*\n'
              '*<game_box_2991.html|Kansas City 8, Cleveland 2>*\n'
              '*<game_box_3004.html|Miami 6, Chicago 2>*\n'
              '*<game_box_3001.html|New York 1, San Francisco 0>*\n'
              '*<game_box_3000.html|New York 5, Los Angeles 3>*\n'
              '*<game_box_2992.html|Philadelphia 3, Washington 1>*\n'
              '*<game_box_2999.html|San Diego 8, Colorado 2>*\n'
              '*<game_box_2990.html|St. Louis 5, Pittsburgh 4>*\n'
              '*<game_box_2997.html|Tampa Bay 12, Boston 9>*\n'
              '*<game_box_2994.html|Texas 5, Oakland 3>*\n'
              '*<game_box_2995.html|Toronto 8, Minnesota 2>*')

TABLE_MSG = ('Cincinnati Reds 111\nSan Diego Padres 104\n'
             'Boston Red Sox 99\nSeattle Mariners 98\n'
             'Los Angeles Dodgers 97\nNew York Mets 95\n'
             'St. Louis Cardinals 89\nColorado Rockies 88\n'
             'Minnesota Twins 88\nNew York Yankees 88\n'
             'Detroit Tigers 86\nHouston Astros 85\n'
             'Miami Marlins 84\nChicago White Sox 82\n'
             'Atlanta Braves 77\nMilwaukee Brewers 77\n'
             'Cleveland Indians 76\nArizona Diamondbacks 76\n'
             'Kansas City Royals 76\nPhiladelphia Phillies 75\n'
             'Oakland Athletics 75\nWashington Nationals 73\n'
             'Toronto Blue Jays 73\nChicago Cubs 71\n'
             'Baltimore Orioles 70\nLos Angeles Angels 70\n'
             'Texas Rangers 67\nTampa Bay Rays 65\n'
             'San Francisco Giants 62\nPittsburgh Pirates 53```')


def _data(scores=None, started=False, table=None):
    if scores is None:
        scores = {}
    if table is None:
        table = {}

    return {
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

    def test_notify__download_finish(self):
        statsplus = self.create_statsplus(_data(started=True))
        response = statsplus._notify_internal(notify=Notify.DOWNLOAD_FINISH)
        self.assertEqual(response, Response())

        write = _data()
        self.mock_open.assert_called_with(Statsplus._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    def test_notify__other(self):
        statsplus = self.create_statsplus(_data(started=True))
        response = statsplus._notify_internal(notify=Notify.OTHER)
        self.assertEqual(response, Response())

        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    @mock.patch.object(Statsplus, '_valid')
    @mock.patch.object(Statsplus, '_save_table')
    @mock.patch.object(Statsplus, '_start')
    @mock.patch.object(Statsplus, '_save_scores')
    def test_on_message__scores_date(self, mock_scores, mock_start, mock_table,
                                     mock_valid):
        mock_valid.return_value = True

        text = '08/30/2024 MAJOR LEAGUE BASEBALL Final Scores\n' + SCORES_MSG
        obj = {'bot_id': 'B7KJ3362Y', 'channel': 'C7JSGHW8G', 'text': text}

        statsplus = self.create_statsplus(_data(started=True))
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
    def test_on_message__scores_start(self, mock_scores, mock_start,
                                      mock_table, mock_valid):
        response = Response(notify=[Notify.BASE])
        mock_scores.return_value = response
        mock_valid.return_value = True

        text = '08/31/2024 MAJOR LEAGUE BASEBALL Final Scores\n' + SCORES_MSG
        obj = {'bot_id': 'B7KJ3362Y', 'channel': 'C7JSGHW8G', 'text': text}

        statsplus = self.create_statsplus(_data())
        statsplus.shadow['download.end'] = encode_datetime(DATE_08300000)

        actual = statsplus._on_message_internal(obj=obj)
        self.assertEqual(actual, response)

        mock_scores.assert_called_once_with(
            encode_datetime(DATE_08310000), text)
        mock_start.assert_called_once_with()
        mock_valid.assert_called_once_with(obj)
        self.assertNotCalled(mock_table, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Statsplus, '_valid')
    @mock.patch.object(Statsplus, '_save_table')
    @mock.patch.object(Statsplus, '_start')
    @mock.patch.object(Statsplus, '_save_scores')
    def test_on_message__scores_valid(self, mock_scores, mock_start,
                                      mock_table, mock_valid):
        response = Response(notify=[Notify.BASE])
        mock_scores.return_value = response
        mock_valid.return_value = True

        text = '08/31/2024 MAJOR LEAGUE BASEBALL Final Scores\n' + SCORES_MSG
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
    def test_on_message__table_date(self, mock_scores, mock_start, mock_table,
                                    mock_valid):
        mock_valid.return_value = True

        text = '```MAJOR LEAGUE BASEBALL Live Table - 08/30/2024\n' + TABLE_MSG
        obj = {'bot_id': 'B7KJ3362Y', 'channel': 'C7JSGHW8G', 'text': text}

        statsplus = self.create_statsplus(_data(started=True))
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
    def test_on_message__table_start(self, mock_scores, mock_start, mock_table,
                                     mock_valid):
        response = Response(notify=[Notify.BASE])
        mock_table.return_value = response
        mock_valid.return_value = True

        text = '```MAJOR LEAGUE BASEBALL Live Table - 08/31/2024\n' + TABLE_MSG
        obj = {'bot_id': 'B7KJ3362Y', 'channel': 'C7JSGHW8G', 'text': text}

        statsplus = self.create_statsplus(_data())
        statsplus.shadow['download.end'] = encode_datetime(DATE_08300000)

        actual = statsplus._on_message_internal(obj=obj)
        self.assertEqual(actual, response)

        mock_start.assert_called_once_with()
        mock_table.assert_called_once_with(text)
        mock_valid.assert_called_once_with(obj)
        self.assertNotCalled(mock_scores, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Statsplus, '_valid')
    @mock.patch.object(Statsplus, '_save_table')
    @mock.patch.object(Statsplus, '_start')
    @mock.patch.object(Statsplus, '_save_scores')
    def test_on_message__table_valid(self, mock_scores, mock_start, mock_table,
                                     mock_valid):
        response = Response(notify=[Notify.BASE])
        mock_table.return_value = response
        mock_valid.return_value = True

        text = '```MAJOR LEAGUE BASEBALL Live Table - 08/31/2024\n' + TABLE_MSG
        obj = {'bot_id': 'B7KJ3362Y', 'channel': 'C7JSGHW8G', 'text': text}

        statsplus = self.create_statsplus(_data(started=True))
        statsplus.shadow['download.end'] = encode_datetime(DATE_08300000)

        actual = statsplus._on_message_internal(obj=obj)
        self.assertEqual(actual, response)

        mock_table.assert_called_once_with(text)
        mock_valid.assert_called_once_with(obj)
        self.assertNotCalled(mock_scores, mock_start, self.mock_open,
                             self.mock_handle.write)

    def test_reload(self):
        statsplus = self.create_statsplus(_data())
        actual = statsplus._reload_internal(date=DATE_10260602)
        expected = {'statslab': ['parse_score']}
        self.assertEqual(actual, expected)

        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    def test_shadow(self):
        table = {'T32': '1-0', 'T45': '0-1'}
        statsplus = self.create_statsplus(_data(table=table))
        actual = statsplus._shadow_internal(date=DATE_10260602)
        shadow = Shadow(
            destination='standings', key='statsplus.table', info=table)
        self.assertEqual(actual, [shadow])

        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    @mock.patch.object(Statsplus, '_call')
    def test_parse_scores__none(self, mock_call):
        mock_call.side_effect = [True, None]

        date = encode_datetime(DATE_08310000)
        read = _data(scores={date: ['2998', '3003']})
        statsplus = self.create_statsplus(read)
        actual = statsplus._parse_scores(date)
        expected = Response(
            thread_=[Thread(target='_parse_scores', args=(date, ))])
        self.assertEqual(actual, expected)

        write = _data(scores={date: ['3003']})
        mock_call.assert_has_calls([
            mock.call('parse_score', (date, '2998', False)),
            mock.call('parse_score', (date, '3003', False)),
        ])
        self.mock_open.assert_called_with(Statsplus._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch.object(Statsplus, '_call')
    def test_parse_scores__started(self, mock_call):
        mock_call.side_effect = [True, None]

        date = encode_datetime(DATE_08310000)
        read = _data(scores={date: ['2998', '3003']}, started=True)
        statsplus = self.create_statsplus(read)
        actual = statsplus._parse_scores(date)
        expected = Response(
            thread_=[Thread(target='_parse_scores', args=(date, ))])
        self.assertEqual(actual, expected)

        write = _data(scores={date: ['3003']}, started=True)
        mock_call.assert_has_calls([
            mock.call('parse_score', (date, '2998', True)),
            mock.call('parse_score', (date, '3003', True)),
        ])
        self.mock_open.assert_called_with(Statsplus._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch.object(Statsplus, '_call')
    def test_parse_scores__true(self, mock_call):
        mock_call.side_effect = [True, True]

        date = encode_datetime(DATE_08310000)
        read = _data(scores={date: ['2998', '3003']})
        statsplus = self.create_statsplus(read)
        actual = statsplus._parse_scores(date)
        expected = Response()
        self.assertEqual(actual, expected)

        write = _data()
        mock_call.assert_has_calls([
            mock.call('parse_score', (date, '2998', False)),
            mock.call('parse_score', (date, '3003', False)),
        ])
        self.mock_open.assert_called_with(Statsplus._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch('tasks.statsplus.statsplus.check_output')
    def test_start(self, mock_check):
        date = encode_datetime(DATE_08310000)
        table = {'T32': '1-0', 'T45': '0-1'}
        read = _data(scores={date: ['2998']}, table=table)
        statsplus = self.create_statsplus(read)
        statsplus._start()

        write = _data(started=True)
        mock_check.assert_has_calls([
            mock.call(['rm', '-rf', GAMES_DIR]),
            mock.call(['mkdir', GAMES_DIR]),
        ])
        self.mock_open.assert_called_with(Statsplus._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    def test_save_scores(self):
        date = encode_datetime(DATE_08310000)
        text = '08/31/2024 MAJOR LEAGUE BASEBALL Final Scores\n' + SCORES_MSG

        statsplus = self.create_statsplus(_data())
        actual = statsplus._save_scores(date, text)
        expected = Response(
            thread_=[Thread(target='_parse_scores', args=(date, ))])
        self.assertEqual(actual, expected)

        nums = [
            '2998', '3003', '2996', '3002', '2993', '2991', '3004', '3001',
            '3000', '2992', '2999', '2990', '2997', '2994', '2995'
        ]
        write = _data(scores={date: nums})
        self.mock_open.assert_called_with(Statsplus._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    def test_save_table(self):
        table = {
            'T31': '75-86', 'T32': '76-85', 'T33': '70-91', 'T34': '99-62',
            'T35': '82-79', 'T36': '71-90', 'T37': '110-51', 'T38': '76-85',
            'T39': '88-73', 'T40': '85-76', 'T41': '83-78', 'T42': '84-77',
            'T43': '75-86', 'T44': '70-91', 'T45': '97-64', 'T46': '77-84',
            'T47': '88-73', 'T48': '87-74', 'T49': '94-67', 'T50': '75-86',
            'T51': '74-87', 'T52': '53-108', 'T53': '103-58', 'T54': '98-63',
            'T55': '62-99', 'T56': '88-73', 'T57': '64-97', 'T58': '66-95',
            'T59': '72-89', 'T60': '73-88'
        }  # yapf: disable
        text = '```MAJOR LEAGUE BASEBALL Live Table - 08/31/2024\n' + TABLE_MSG

        statsplus = self.create_statsplus(_data())
        statsplus.shadow['standings.table'] = table
        actual = statsplus._save_table(text)
        expected = Response(shadow=statsplus._shadow_internal())
        self.assertEqual(actual, expected)

        table = {
            'T31': '1-0', 'T32': '1-0', 'T33': '0-1', 'T34': '0-1',
            'T35': '0-1', 'T36': '0-1', 'T37': '1-0', 'T38': '0-1',
            'T39': '0-1', 'T40': '1-0', 'T41': '1-0', 'T42': '1-0',
            'T43': '1-0', 'T44': '0-1', 'T45': '0-1', 'T46': '0-1',
            'T47': '0-1', 'T48': '1-0', 'T49': '1-0', 'T50': '0-1',
            'T51': '1-0', 'T52': '0-1', 'T53': '1-0', 'T54': '0-1',
            'T55': '0-1', 'T56': '1-0', 'T57': '1-0', 'T58': '1-0',
            'T59': '1-0', 'T60': '0-1'
        }  # yapf: disable
        write = _data(table=table)
        self.mock_open.assert_called_with(Statsplus._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    def test_decode_wl(self):
        statsplus = self.create_statsplus(_data())
        actual = statsplus._decode_wl('75-86')
        expected = (75, 86)
        self.assertEqual(actual, expected)

    def test_encode_wl(self):
        statsplus = self.create_statsplus(_data())
        actual = statsplus._encode_wl(75, 86)
        expected = '75-86'
        self.assertEqual(actual, expected)

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
