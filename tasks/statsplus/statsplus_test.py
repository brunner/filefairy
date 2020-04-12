#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for statsplus.py."""

import json
import logging
import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.extend((_path, re.sub(r'/tasks/statsplus', '', _path)))

from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.datetime_.datetime_ import encode_datetime  # noqa
from common.jinja2_.jinja2_ import env  # noqa
from common.json_.json_ import dumps  # noqa
from common.test.test import Test  # noqa
from common.test.test import get_testdata  # noqa
from tasks.statsplus.statsplus import Statsplus  # noqa
from types_.notify.notify import Notify  # noqa
from types_.response.response import Response  # noqa
from types_.shadow.shadow import Shadow  # noqa
from types_.thread_.thread_ import Thread  # noqa

ENV = env()

DATE_08300000 = datetime_datetime_pst(2024, 8, 30)
DATE_08310000 = datetime_datetime_pst(2024, 8, 31)
DATE_10260602 = datetime_datetime_pst(1985, 10, 26, 6, 2, 30)

EXTRACT_DIR = re.sub(r'/tasks/statsplus', '/resources/extract', _path)
EXTRACT_BOX_SCORES = os.path.join(EXTRACT_DIR, 'box_scores')
EXTRACT_GAME_LOGS = os.path.join(EXTRACT_DIR, 'game_logs')
GAMES_DIR = re.sub(r'/tasks/statsplus', '/resources/games', _path)

STATSPLUS_LINK = 'https://statsplus.net/oblootp/reports/news/html'
STATSPLUS_BOX_SCORES = os.path.join(STATSPLUS_LINK, 'box_scores')
STATSPLUS_GAME_LOGS = os.path.join(STATSPLUS_LINK, 'game_logs')

TESTDATA = get_testdata()

FINAL_SCORES = '08/31/2024 MAJOR LEAGUE BASEBALL Final Scores\n'
SCORES = '*<game_box_2449.html|Minnesota 6, Detroit 5>*\n'


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
        patch_chat = mock.patch('tasks.statsplus.statsplus.chat_post_message')
        self.addCleanup(patch_chat.stop)
        self.mock_chat = patch_chat.start()

        patch_log = mock.patch('tasks.statsplus.statsplus._logger.log')
        self.addCleanup(patch_log.stop)
        self.mock_log = patch_log.start()

        patch_open = mock.patch(
            'api.serializable.serializable.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]

    def reset_mocks(self):
        self.mock_chat.reset_mock()
        self.mock_log.reset_mock()
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()

    def create_statsplus(self, data):
        self.init_mocks(data)
        statsplus = Statsplus(date=DATE_10260602, e=ENV)

        self.mock_open.assert_called_once_with(Statsplus._data(), 'r')
        self.assertNotCalled(self.mock_chat, self.mock_log,
                             self.mock_handle.write)
        self.assertEqual(statsplus.data, data)

        self.reset_mocks()
        self.init_mocks(data)

        return statsplus

    def test_shadow_data(self):
        date = encode_datetime(DATE_08310000)
        scores = {date: {'2449': 'T47 6, T40 5'}}
        table = {'T40': '0-1', 'T47': '1-0'}
        statsplus = self.create_statsplus(_data(scores=scores, table=table))
        actual = statsplus._shadow_data(date=DATE_10260602)
        shadow = statsplus._shadow_scores() + statsplus._shadow_table()
        self.assertEqual(actual, shadow)

        self.assertNotCalled(self.mock_chat, self.mock_log, self.mock_open,
                             self.mock_handle.write)

    def test_shadow_scores(self):
        date = encode_datetime(DATE_08310000)
        scores = {date: {'2449': 'T47 6, T40 5'}}
        table = {'T40': '0-1', 'T47': '1-0'}
        statsplus = self.create_statsplus(_data(scores=scores, table=table))
        actual = statsplus._shadow_scores()
        shadow = [
            Shadow(
                destination='gameday',
                key='statsplus.scores',
                info=scores,
            ),
            Shadow(
                destination='standings',
                key='statsplus.scores',
                info=scores,
            ),
        ]
        self.assertEqual(actual, shadow)

        self.assertNotCalled(self.mock_chat, self.mock_log, self.mock_open,
                             self.mock_handle.write)

    def test_shadow_table(self):
        date = encode_datetime(DATE_08310000)
        scores = {date: {'2449': 'T47 6, T40 5'}}
        table = {'T40': '0-1', 'T47': '1-0'}
        statsplus = self.create_statsplus(_data(scores=scores, table=table))
        actual = statsplus._shadow_table()
        shadow = [
            Shadow(
                destination='standings',
                key='statsplus.table',
                info=table,
            )
        ]
        self.assertEqual(actual, shadow)

        self.assertNotCalled(self.mock_chat, self.mock_log, self.mock_open,
                             self.mock_handle.write)

    def test_notify__download_finish(self):
        statsplus = self.create_statsplus(_data(started=True))
        response = statsplus._notify_internal(notify=Notify.DOWNLOAD_FINISH)
        expected = Response(thread_=[Thread(target='_parse_extracted_scores')])
        self.assertEqual(response, expected)

        self.assertNotCalled(self.mock_chat, self.mock_log, self.mock_open,
                             self.mock_handle.write)

    def test_notify__other(self):
        statsplus = self.create_statsplus(_data(started=True))
        response = statsplus._notify_internal(notify=Notify.OTHER)
        expected = Response()
        self.assertEqual(response, expected)

        self.assertNotCalled(self.mock_chat, self.mock_log, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Statsplus, '_valid')
    @mock.patch.object(Statsplus, '_start')
    @mock.patch.object(Statsplus, '_save_scores')
    def test_on_message__date(self, mock_scores, mock_start, mock_valid):
        mock_valid.return_value = True

        text = '08/30/2024 Final Scores'
        obj = {'bot_id': 'B7KJ3362Y', 'channel': 'C7JSGHW8G', 'text': text}

        statsplus = self.create_statsplus(_data())
        statsplus.shadow['download.end'] = encode_datetime(DATE_08310000)

        actual = statsplus._on_message_internal(obj=obj)
        self.assertEqual(actual, Response())

        mock_valid.assert_called_once_with(obj)
        self.assertNotCalled(mock_scores, mock_start, self.mock_chat,
                             self.mock_log, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Statsplus, '_valid')
    @mock.patch.object(Statsplus, '_start')
    @mock.patch.object(Statsplus, '_save_scores')
    def test_on_message__save_scores(self, mock_scores, mock_start,
                                     mock_valid):
        response = Response(notify=[Notify.OTHER])
        mock_scores.return_value = response
        mock_valid.return_value = True

        text = FINAL_SCORES + SCORES
        obj = {'bot_id': 'B7KJ3362Y', 'channel': 'C7JSGHW8G', 'text': text}

        statsplus = self.create_statsplus(_data(started=True))
        statsplus.shadow['download.end'] = encode_datetime(DATE_08300000)

        actual = statsplus._on_message_internal(obj=obj)
        self.assertEqual(actual, response)

        mock_scores.assert_called_once_with(
            encode_datetime(DATE_08310000), text)
        mock_valid.assert_called_once_with(obj)
        self.assertNotCalled(mock_start, self.mock_chat, self.mock_log,
                             self.mock_open, self.mock_handle.write)

    @mock.patch.object(Statsplus, '_valid')
    @mock.patch.object(Statsplus, '_start')
    @mock.patch.object(Statsplus, '_save_scores')
    def test_on_message__start(self, mock_scores, mock_start, mock_valid):
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
        self.assertNotCalled(mock_scores, self.mock_chat, self.mock_log,
                             self.mock_open, self.mock_handle.write)

    @mock.patch.object(Statsplus, '_on_message_internal')
    @mock.patch('tasks.statsplus.statsplus.time.time')
    @mock.patch('tasks.statsplus.statsplus.channels_history')
    def test_backfill(self, mock_history, mock_time, mock_on_message):
        message1 = {'bot_id': 'B7KJ3362Y', 'text': '08/31/2024 Final Scores'}
        message2 = {'bot_id': 'B7KJ3362Y', 'text': FINAL_SCORES}
        messages = [message2, message1]
        mock_history.return_value = {'ok': True, 'messages': messages}
        mock_time.return_value = 499132800.1234567

        statsplus = self.create_statsplus(_data())

        date = encode_datetime(DATE_08310000)
        thread_ = Thread(target='_parse_saved_scores', args=(date, ))
        mock_on_message.side_effect = [
            Response(notify=[Notify.STATSPLUS_START]),
            Response(shadow=statsplus._shadow_scores(), thread_=[thread_]),
        ]

        actual = statsplus.backfill('2')
        expected = Response(
            notify=[Notify.STATSPLUS_START],
            shadow=statsplus._shadow_data(),
            thread_=[thread_])
        self.assertEqual(actual, expected)

        mock_history.assert_called_once_with('C7JSGHW8G', '', 499125600)
        mock_time.assert_called_once_with()
        mock_on_message.assert_has_calls([
            mock.call(obj=message1),
            mock.call(obj=message2),
        ])

        self.assertNotCalled(self.mock_chat, self.mock_log, self.mock_open,
                             self.mock_handle.write)

    def test_extract(self):
        statsplus = self.create_statsplus(_data(started=True))
        response = statsplus.extract()
        expected = Response(thread_=[Thread(target='_parse_extracted_scores')])
        self.assertEqual(response, expected)

        write = _data()
        self.assertNotCalled(self.mock_chat, self.mock_log)
        self.mock_open.assert_called_with(Statsplus._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

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
            mock.call(EXTRACT_BOX_SCORES),
            mock.call(GAMES_DIR),
        ])
        mock_loads.assert_has_calls([
            mock.call(os.path.join(GAMES_DIR, '2449.json')),
            mock.call(os.path.join(GAMES_DIR, '2469.json'))
        ])
        mock_parse.assert_has_calls([
            mock.call('2449', None),
            mock.call('2469', None),
        ])
        mock_rm.assert_called_once_with()
        self.mock_chat.assert_called_once_with('fairylab',
                                               'Download complete.')
        self.mock_log.assert_called_once_with(logging.INFO,
                                              'Download complete.')
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
            mock.call(EXTRACT_BOX_SCORES),
            mock.call(GAMES_DIR),
        ])
        mock_loads.assert_has_calls([
            mock.call(os.path.join(GAMES_DIR, '2449.json')),
            mock.call(os.path.join(GAMES_DIR, '2469.json'))
        ])
        mock_parse.assert_has_calls([
            mock.call('2449', None),
            mock.call('2469', None),
        ])
        self.mock_chat.assert_called_once_with('fairylab',
                                               'Download complete.')
        self.mock_log.assert_called_once_with(logging.INFO,
                                              'Download complete.')
        self.mock_open.assert_called_with(Statsplus._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.assertNotCalled(mock_rm)

    @mock.patch.object(Statsplus, '_parse_score')
    def test_parse_saved_scores__none(self, mock_parse):
        mock_parse.return_value = None

        date = encode_datetime(DATE_08310000)
        scores = {date: {'2449': 'T47 6, T40 5'}}
        statsplus = self.create_statsplus(_data(scores=scores))
        actual = statsplus._parse_saved_scores(date)
        expected = Response(
            thread_=[Thread(target='_parse_saved_scores', args=(date, ))])
        self.assertEqual(actual, expected)

        mock_parse.assert_called_once_with('2449', date)
        self.assertNotCalled(self.mock_chat, self.mock_log, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Statsplus, '_parse_score')
    def test_parse_saved_scores__true(self, mock_parse):
        mock_parse.return_value = json.loads(TESTDATA['2449.json'])

        date = encode_datetime(DATE_08310000)
        scores = {date: {'2449': 'T47 6, T40 5'}}
        statsplus = self.create_statsplus(_data(scores=scores))
        actual = statsplus._parse_saved_scores(date)
        expected = Response(
            notify=[Notify.STATSPLUS_PARSE], shadow=statsplus._shadow_data())
        self.assertEqual(actual, expected)

        write = _data(table={'T40': '0-1', 'T47': '1-0'})
        mock_parse.assert_called_once_with('2449', date)
        self.assertNotCalled(self.mock_chat, self.mock_log)
        self.mock_open.assert_called_with(Statsplus._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch('tasks.statsplus.statsplus.os.path.isfile')
    @mock.patch('tasks.statsplus.statsplus.call_service')
    def test_parse_score__isfile(self, mock_call, mock_isfile):
        mock_isfile.return_value = True

        date = encode_datetime(DATE_08310000)
        statsplus = self.create_statsplus(_data())
        actual = statsplus._parse_score('2449', date)
        self.assertEqual(actual, True)

        mock_isfile.assert_called_once_with(
            os.path.join(GAMES_DIR, '2449.json'))
        self.assertNotCalled(mock_call, self.mock_chat, self.mock_log,
                             self.mock_open, self.mock_handle.write)

    @mock.patch('tasks.statsplus.statsplus.os.path.isfile')
    @mock.patch('tasks.statsplus.statsplus.call_service')
    def test_parse_score__none(self, mock_call, mock_isfile):
        mock_call.return_value = None
        mock_isfile.return_value = False

        date = encode_datetime(DATE_08310000)
        statsplus = self.create_statsplus(_data())
        actual = statsplus._parse_score('2449', date)
        self.assertEqual(actual, None)

        box = os.path.join(EXTRACT_BOX_SCORES, 'game_box_2449.html')
        log = os.path.join(EXTRACT_GAME_LOGS, 'log_2449.txt')
        out = os.path.join(GAMES_DIR, '2449.json')
        mock_call.assert_called_once_with('statslab', 'parse_game',
                                          (box, log, out, date))
        mock_isfile.assert_called_once_with(out)
        self.assertNotCalled(self.mock_chat, self.mock_log, self.mock_open,
                             self.mock_handle.write)

    @mock.patch('tasks.statsplus.statsplus.os.path.isfile')
    @mock.patch('tasks.statsplus.statsplus.call_service')
    def test_parse_score__started(self, mock_call, mock_isfile):
        mock_call.return_value = True
        mock_isfile.return_value = False

        date = encode_datetime(DATE_08310000)
        statsplus = self.create_statsplus(_data(started=True))
        actual = statsplus._parse_score('2449', date)
        self.assertEqual(actual, True)

        box = os.path.join(STATSPLUS_BOX_SCORES, 'game_box_2449.html')
        log = os.path.join(STATSPLUS_GAME_LOGS, 'log_2449.html')
        out = os.path.join(GAMES_DIR, '2449.json')
        mock_call.assert_called_once_with('statslab', 'parse_game',
                                          (box, log, out, date))
        mock_isfile.assert_called_once_with(out)
        self.assertNotCalled(self.mock_chat, self.mock_log, self.mock_open,
                             self.mock_handle.write)

    @mock.patch('tasks.statsplus.statsplus.os.path.isfile')
    @mock.patch('tasks.statsplus.statsplus.call_service')
    def test_parse_score__true(self, mock_call, mock_isfile):
        mock_call.return_value = True
        mock_isfile.return_value = False

        date = encode_datetime(DATE_08310000)
        statsplus = self.create_statsplus(_data())
        actual = statsplus._parse_score('2449', date)
        self.assertEqual(actual, True)

        box = os.path.join(EXTRACT_BOX_SCORES, 'game_box_2449.html')
        log = os.path.join(EXTRACT_GAME_LOGS, 'log_2449.txt')
        out = os.path.join(GAMES_DIR, '2449.json')
        mock_call.assert_called_once_with('statslab', 'parse_game',
                                          (box, log, out, date))
        mock_isfile.assert_called_once_with(out)
        self.assertNotCalled(self.mock_chat, self.mock_log, self.mock_open,
                             self.mock_handle.write)

    def test_save_scores(self):
        date = encode_datetime(DATE_08310000)
        text = '08/31/2024 MAJOR LEAGUE BASEBALL Final Scores\n' + SCORES

        statsplus = self.create_statsplus(_data())
        actual = statsplus._save_scores(date, text)
        expected = Response(
            shadow=statsplus._shadow_scores(),
            thread_=[Thread(target='_parse_saved_scores', args=(date, ))])
        self.assertEqual(actual, expected)

        scores = {date: {'2449': 'T47 6, T40 5'}}
        write = _data(scores=scores)
        self.assertNotCalled(self.mock_chat, self.mock_log)
        self.mock_open.assert_called_with(Statsplus._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch('tasks.statsplus.statsplus.check_output')
    def test_rm(self, mock_check):
        statsplus = self.create_statsplus(_data())
        statsplus._rm()

        # TODO: Remove after the World Series.
        # mock_check.assert_has_calls([
        #     mock.call(['rm', '-rf', GAMES_DIR]),
        #     mock.call(['mkdir', GAMES_DIR]),
        # ])
        # self.assertNotCalled(self.mock_chat, self.mock_log, self.mock_open,
        #                      self.mock_handle.write)

    @mock.patch.object(Statsplus, '_rm')
    def test_start(self, mock_rm):
        date = encode_datetime(DATE_08310000)
        scores = {date: {'2449': 'T47 6, T40 5'}}
        table = {'T40': '0-1', 'T47': '1-0'}
        statsplus = self.create_statsplus(_data(scores=scores, table=table))
        statsplus._start()

        write = _data(started=True)
        mock_rm.assert_called_once_with()
        self.mock_chat.assert_called_once_with('fairylab', 'Sim in progress.')
        self.mock_log.assert_called_once_with(logging.INFO, 'Sim in progress.')
        self.mock_open.assert_called_with(Statsplus._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    def test_valid__false(self):
        obj = {'bot_id': 'B123', 'channel': 'C123', 'text': 'foo'}

        statsplus = self.create_statsplus(_data())
        actual = statsplus._valid(obj)
        expected = False
        self.assertEqual(actual, expected)

        self.assertNotCalled(self.mock_chat, self.mock_log, self.mock_open,
                             self.mock_handle.write)

    def test_valid__true(self):
        obj = {'bot_id': 'B7KJ3362Y', 'channel': 'C7JSGHW8G', 'text': 'foo'}

        statsplus = self.create_statsplus(_data())
        actual = statsplus._valid(obj)
        expected = True
        self.assertEqual(actual, expected)

        self.assertNotCalled(self.mock_chat, self.mock_log, self.mock_open,
                             self.mock_handle.write)


if __name__ == '__main__':
    unittest.main()
