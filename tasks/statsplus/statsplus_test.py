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
from common.json_.json_ import dumps  # noqa
from common.test.test import Test  # noqa
from common.test.test import get_testdata  # noqa
from tasks.statsplus.statsplus import Statsplus  # noqa
from types_.notify.notify import Notify  # noqa
from types_.response.response import Response  # noqa
from types_.shadow.shadow import Shadow  # noqa
from types_.thread_.thread_ import Thread  # noqa

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


class StatsplusTest(Test):
    def setUp(self):
        chat_post_message_patch = mock.patch(
            'tasks.statsplus.statsplus.chat_post_message')
        self.addCleanup(chat_post_message_patch.stop)
        self.chat_post_message_ = chat_post_message_patch.start()

        log_patch = mock.patch('tasks.statsplus.statsplus._logger.log')
        self.addCleanup(log_patch.stop)
        self.log_ = log_patch.start()

        open_patch = mock.patch('api.serializable.serializable.open',
                                create=True)
        self.addCleanup(open_patch.stop)
        self.open_ = open_patch.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.open_handle_ = mo()
        self.open_.side_effect = [mo.return_value]

    def reset_mocks(self):
        self.chat_post_message_.reset_mock()
        self.log_.reset_mock()
        self.open_handle_.write.reset_mock()

    def create_statsplus(self, data):
        self.init_mocks(data)
        statsplus = Statsplus(date=DATE_10260602)

        self.assertNotCalled(self.chat_post_message_, self.log_,
                             self.open_handle_.write)
        self.assertEqual(statsplus.data, data)

        self.reset_mocks()
        self.init_mocks(data)

        return statsplus

    def test_shadow_data(self):
        date = encode_datetime(DATE_08310000)
        scores = {date: {'2449': 'T47 6, T40 5'}}
        table = {'T40': '0-1', 'T47': '1-0'}
        data = {'scores': scores, 'started': False, 'table': table}
        statsplus = self.create_statsplus(data)
        actual = statsplus._shadow_data(date=DATE_10260602)
        shadow = statsplus.get_shadow_scores() + statsplus.get_shadow_table()
        self.assertEqual(actual, shadow)

        self.assertNotCalled(self.chat_post_message_, self.log_,
                             self.open_handle_.write)

    def test_notify__download_finish(self):
        data = {'scores': {}, 'started': True, 'table': {}}
        statsplus = self.create_statsplus(data)
        response = statsplus._notify_internal(notify=Notify.DOWNLOAD_FINISH)
        expected = Response(thread_=[Thread(target='parse_extracted_scores')])
        self.assertEqual(response, expected)

        self.assertNotCalled(self.chat_post_message_, self.log_,
                             self.open_handle_.write)

    def test_notify__other(self):
        data = {'scores': {}, 'started': True, 'table': {}}
        statsplus = self.create_statsplus(data)
        response = statsplus._notify_internal(notify=Notify.OTHER)
        expected = Response()
        self.assertEqual(response, expected)

        self.assertNotCalled(self.chat_post_message_, self.log_,
                             self.open_handle_.write)

    @mock.patch.object(Statsplus, 'start')
    @mock.patch.object(Statsplus, 'save_scores')
    @mock.patch.object(Statsplus, 'is_valid_message')
    def test_on_message__date(self, is_valid_message_, save_scores_, start_):
        is_valid_message_.return_value = True

        text = '08/30/2024 Final Scores'
        obj = {'bot_id': 'B7KJ3362Y', 'channel': 'C7JSGHW8G', 'text': text}

        data = {'scores': {}, 'started': False, 'table': {}}
        statsplus = self.create_statsplus(data)
        statsplus.shadow['download.end'] = encode_datetime(DATE_08310000)

        actual = statsplus._on_message_internal(obj=obj)
        self.assertEqual(actual, Response())

        is_valid_message_.assert_called_once_with(obj)
        self.assertNotCalled(save_scores_, start_, self.chat_post_message_,
                             self.log_, self.open_handle_.write)

    @mock.patch.object(Statsplus, 'start')
    @mock.patch.object(Statsplus, 'save_scores')
    @mock.patch.object(Statsplus, 'is_valid_message')
    def test_on_message__save_scores(self, is_valid_message_, save_scores_,
                                     start_):
        response = Response(notify=[Notify.OTHER])
        save_scores_.return_value = response
        is_valid_message_.return_value = True

        text = FINAL_SCORES + SCORES
        obj = {'bot_id': 'B7KJ3362Y', 'channel': 'C7JSGHW8G', 'text': text}

        data = {'scores': {}, 'started': True, 'table': {}}
        statsplus = self.create_statsplus(data)
        statsplus.shadow['download.end'] = encode_datetime(DATE_08300000)

        actual = statsplus._on_message_internal(obj=obj)
        self.assertEqual(actual, response)

        is_valid_message_.assert_called_once_with(obj)
        save_scores_.assert_called_once_with(encode_datetime(DATE_08310000),
                                             text)
        self.assertNotCalled(start_, self.chat_post_message_, self.log_,
                             self.open_handle_.write)

    @mock.patch.object(Statsplus, 'start')
    @mock.patch.object(Statsplus, 'save_scores')
    @mock.patch.object(Statsplus, 'is_valid_message')
    def test_on_message__start(self, is_valid_message_, save_scores_, start_):
        response = Response(notify=[Notify.OTHER])
        start_.return_value = response
        is_valid_message_.return_value = True

        text = '08/31/2024 Final Scores'
        obj = {'bot_id': 'B7KJ3362Y', 'channel': 'C7JSGHW8G', 'text': text}

        data = {'scores': {}, 'started': False, 'table': {}}
        statsplus = self.create_statsplus(data)
        statsplus.shadow['download.end'] = encode_datetime(DATE_08300000)

        actual = statsplus._on_message_internal(obj=obj)
        self.assertEqual(actual, response)

        is_valid_message_.assert_called_once_with(obj)
        start_.assert_called_once_with()
        self.assertNotCalled(save_scores_, self.chat_post_message_, self.log_,
                             self.open_handle_.write)

    @mock.patch('tasks.statsplus.statsplus.time.time')
    @mock.patch.object(Statsplus, '_on_message_internal')
    @mock.patch('tasks.statsplus.statsplus.channels_history')
    def test_backfill(self, channels_history_, _on_message_internal_, time_):
        message1 = {'bot_id': 'B7KJ3362Y', 'text': '08/31/2024 Final Scores'}
        message2 = {'bot_id': 'B7KJ3362Y', 'text': FINAL_SCORES}
        messages = [message2, message1]
        channels_history_.return_value = {'ok': True, 'messages': messages}
        time_.return_value = 499132800.1234567

        data = {'scores': {}, 'started': False, 'table': {}}
        statsplus = self.create_statsplus(data)

        date = encode_datetime(DATE_08310000)
        thread_ = Thread(target='_parse_saved_scores', args=(date, ))
        _on_message_internal_.side_effect = [
            Response(notify=[Notify.STATSPLUS_START]),
            Response(shadow=statsplus.get_shadow_scores(), thread_=[thread_]),
        ]

        actual = statsplus.backfill('2')
        expected = Response(notify=[Notify.STATSPLUS_START],
                            shadow=statsplus._shadow_data(),
                            thread_=[thread_])
        self.assertEqual(actual, expected)

        channels_history_.assert_called_once_with('C7JSGHW8G', '', 499125600)
        time_.assert_called_once_with()
        _on_message_internal_.assert_has_calls([
            mock.call(obj=message1),
            mock.call(obj=message2),
        ])
        self.assertNotCalled(self.chat_post_message_, self.log_,
                             self.open_handle_.write)

    def test_extract(self):
        data = {'scores': {}, 'started': True, 'table': {}}
        statsplus = self.create_statsplus(data)
        response = statsplus.extract()
        expected = Response(thread_=[Thread(target='parse_extracted_scores')])
        self.assertEqual(response, expected)

        write = {'scores': {}, 'started': False, 'table': {}}
        self.open_handle_.write.assert_called_once_with(dumps(write) + '\n')
        self.assertNotCalled(self.chat_post_message_, self.log_)

    @mock.patch('tasks.statsplus.statsplus.check_output')
    def test_cleanup(self, check_output_):
        data = {'scores': {}, 'started': False, 'table': {}}
        statsplus = self.create_statsplus(data)
        statsplus.cleanup()

        check_output_.assert_has_calls([
            mock.call(['rm', '-rf', GAMES_DIR]),
            mock.call(['mkdir', GAMES_DIR]),
        ])
        self.assertNotCalled(self.chat_post_message_, self.log_,
                             self.open_handle_.write)

    def test_get_shadow_scores(self):
        date = encode_datetime(DATE_08310000)
        scores = {date: {'2449': 'T47 6, T40 5'}}
        table = {'T40': '0-1', 'T47': '1-0'}
        data = {'scores': scores, 'started': False, 'table': table}
        statsplus = self.create_statsplus(data)
        actual = statsplus.get_shadow_scores()
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

        self.assertNotCalled(self.chat_post_message_, self.log_,
                             self.open_handle_.write)

    def test_get_shadow_table(self):
        date = encode_datetime(DATE_08310000)
        scores = {date: {'2449': 'T47 6, T40 5'}}
        table = {'T40': '0-1', 'T47': '1-0'}
        data = {'scores': scores, 'started': False, 'table': table}
        statsplus = self.create_statsplus(data)
        actual = statsplus.get_shadow_table()
        shadow = [
            Shadow(
                destination='standings',
                key='statsplus.table',
                info=table,
            )
        ]
        self.assertEqual(actual, shadow)

        self.assertNotCalled(self.chat_post_message_, self.log_,
                             self.open_handle_.write)

    @mock.patch.object(Statsplus, 'parse_score')
    @mock.patch('tasks.statsplus.statsplus.loads')
    @mock.patch('tasks.statsplus.statsplus.os.listdir')
    @mock.patch.object(Statsplus, 'cleanup')
    def test_parse_extracted_scores__started_false(self, cleanup_, listdir_,
                                                   loads_, parse_score_):
        listdir_.side_effect = [
            ['game_box_2449.html', 'game_box_2469.html'],
            ['2449.json', '2469.json'],
        ]
        loads_.side_effect = [
            json.loads(TESTDATA['2449.json']),
            json.loads(TESTDATA['2469.json'])
        ]

        data = {'scores': {}, 'started': False, 'table': {}}
        statsplus = self.create_statsplus(data)
        actual = statsplus.parse_extracted_scores()
        expected = Response(shadow=statsplus._shadow_data(),
                            notify=[Notify.STATSPLUS_FINISH])
        self.assertEqual(actual, expected)

        write = {
            'scores': {},
            'started': False,
            'table': {
                'T40': '0-2',
                'T47': '2-0'
            }
        }
        cleanup_.assert_called_once_with()
        listdir_.assert_has_calls([
            mock.call(EXTRACT_BOX_SCORES),
            mock.call(GAMES_DIR),
        ])
        loads_.assert_has_calls([
            mock.call(os.path.join(GAMES_DIR, '2449.json')),
            mock.call(os.path.join(GAMES_DIR, '2469.json'))
        ])
        parse_score_.assert_has_calls([
            mock.call('2449', None),
            mock.call('2469', None),
        ])
        self.chat_post_message_.assert_called_once_with(
            'fairylab', 'Download complete.')
        self.log_.assert_called_once_with(logging.INFO, 'Download complete.')
        self.open_handle_.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch.object(Statsplus, 'parse_score')
    @mock.patch('tasks.statsplus.statsplus.loads')
    @mock.patch('tasks.statsplus.statsplus.os.listdir')
    @mock.patch.object(Statsplus, 'cleanup')
    def test_parse_extracted_scores__started_true(self, cleanup_, listdir_,
                                                  loads_, parse_score_):
        listdir_.side_effect = [
            ['game_box_2449.html', 'game_box_2469.html'],
            ['2449.json', '2469.json'],
        ]
        loads_.side_effect = [
            json.loads(TESTDATA['2449.json']),
            json.loads(TESTDATA['2469.json'])
        ]

        data = {'scores': {}, 'started': True, 'table': {}}
        statsplus = self.create_statsplus(data)
        actual = statsplus.parse_extracted_scores()
        expected = Response(shadow=statsplus._shadow_data(),
                            notify=[Notify.STATSPLUS_FINISH])
        self.assertEqual(actual, expected)

        write = {
            'scores': {},
            'started': False,
            'table': {
                'T40': '0-2',
                'T47': '2-0'
            }
        }
        listdir_.assert_has_calls([
            mock.call(EXTRACT_BOX_SCORES),
            mock.call(GAMES_DIR),
        ])
        loads_.assert_has_calls([
            mock.call(os.path.join(GAMES_DIR, '2449.json')),
            mock.call(os.path.join(GAMES_DIR, '2469.json'))
        ])
        parse_score_.assert_has_calls([
            mock.call('2449', None),
            mock.call('2469', None),
        ])
        self.chat_post_message_.assert_called_once_with(
            'fairylab', 'Download complete.')
        self.log_.assert_called_once_with(logging.INFO, 'Download complete.')
        self.open_handle_.write.assert_called_once_with(dumps(write) + '\n')
        self.assertNotCalled(cleanup_)

    @mock.patch.object(Statsplus, 'parse_score')
    def test_parse_saved_scores__none(self, parse_score_):
        parse_score_.return_value = None

        date = encode_datetime(DATE_08310000)
        scores = {date: {'2449': 'T47 6, T40 5'}}
        data = {'scores': scores, 'started': False, 'table': {}}
        statsplus = self.create_statsplus(data)
        actual = statsplus.parse_saved_scores(date)
        expected = Response(
            thread_=[Thread(target='parse_saved_scores', args=(date, ))])
        self.assertEqual(actual, expected)

        parse_score_.assert_called_once_with('2449', date)
        self.assertNotCalled(self.chat_post_message_, self.log_,
                             self.open_handle_.write)

    @mock.patch.object(Statsplus, 'parse_score')
    def test_parse_saved_scores__true(self, parse_score_):
        parse_score_.return_value = json.loads(TESTDATA['2449.json'])

        date = encode_datetime(DATE_08310000)
        scores = {date: {'2449': 'T47 6, T40 5'}}
        data = {'scores': scores, 'started': False, 'table': {}}
        statsplus = self.create_statsplus(data)
        actual = statsplus.parse_saved_scores(date)
        expected = Response(notify=[Notify.STATSPLUS_PARSE],
                            shadow=statsplus._shadow_data())
        self.assertEqual(actual, expected)

        write = {
            'scores': {},
            'started': False,
            'table': {
                'T40': '0-1',
                'T47': '1-0'
            }
        }
        parse_score_.assert_called_once_with('2449', date)
        self.assertNotCalled(self.chat_post_message_, self.log_)
        self.open_handle_.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch('tasks.statsplus.statsplus.os.path.isfile')
    @mock.patch('tasks.statsplus.statsplus.call_service')
    def test_parse_score__isfile(self, call_service_, isfile_):
        isfile_.return_value = True

        date = encode_datetime(DATE_08310000)
        data = {'scores': {}, 'started': False, 'table': {}}
        statsplus = self.create_statsplus(data)
        actual = statsplus.parse_score('2449', date)
        self.assertEqual(actual, True)

        isfile_.assert_called_once_with(os.path.join(GAMES_DIR, '2449.json'))
        self.assertNotCalled(call_service_, self.chat_post_message_, self.log_,
                             self.open_handle_.write)

    @mock.patch('tasks.statsplus.statsplus.os.path.isfile')
    @mock.patch('tasks.statsplus.statsplus.call_service')
    def test_parse_score__none(self, call_service_, isfile_):
        call_service_.return_value = None
        isfile_.return_value = False

        date = encode_datetime(DATE_08310000)
        data = {'scores': {}, 'started': False, 'table': {}}
        statsplus = self.create_statsplus(data)
        actual = statsplus.parse_score('2449', date)
        self.assertEqual(actual, None)

        box = os.path.join(EXTRACT_BOX_SCORES, 'game_box_2449.html')
        log = os.path.join(EXTRACT_GAME_LOGS, 'log_2449.txt')
        out = os.path.join(GAMES_DIR, '2449.json')
        call_service_.assert_called_once_with('statslab', 'parse_game',
                                              (box, log, out, date))
        isfile_.assert_called_once_with(out)
        self.assertNotCalled(self.chat_post_message_, self.log_,
                             self.open_handle_.write)

    @mock.patch('tasks.statsplus.statsplus.os.path.isfile')
    @mock.patch('tasks.statsplus.statsplus.call_service')
    def test_parse_score__started(self, call_service_, isfile_):
        call_service_.return_value = True
        isfile_.return_value = False

        date = encode_datetime(DATE_08310000)
        data = {'scores': {}, 'started': True, 'table': {}}
        statsplus = self.create_statsplus(data)
        actual = statsplus.parse_score('2449', date)
        self.assertEqual(actual, True)

        box = os.path.join(STATSPLUS_BOX_SCORES, 'game_box_2449.html')
        log = os.path.join(STATSPLUS_GAME_LOGS, 'log_2449.html')
        out = os.path.join(GAMES_DIR, '2449.json')
        call_service_.assert_called_once_with('statslab', 'parse_game',
                                              (box, log, out, date))
        isfile_.assert_called_once_with(out)
        self.assertNotCalled(self.chat_post_message_, self.log_,
                             self.open_handle_.write)

    @mock.patch('tasks.statsplus.statsplus.os.path.isfile')
    @mock.patch('tasks.statsplus.statsplus.call_service')
    def test_parse_score__true(self, call_service_, isfile_):
        call_service_.return_value = True
        isfile_.return_value = False

        date = encode_datetime(DATE_08310000)
        data = {'scores': {}, 'started': False, 'table': {}}
        statsplus = self.create_statsplus(data)
        actual = statsplus.parse_score('2449', date)
        self.assertEqual(actual, True)

        box = os.path.join(EXTRACT_BOX_SCORES, 'game_box_2449.html')
        log = os.path.join(EXTRACT_GAME_LOGS, 'log_2449.txt')
        out = os.path.join(GAMES_DIR, '2449.json')
        call_service_.assert_called_once_with('statslab', 'parse_game',
                                              (box, log, out, date))
        isfile_.assert_called_once_with(out)
        self.assertNotCalled(self.chat_post_message_, self.log_,
                             self.open_handle_.write)

    def test_save_scores(self):
        date = encode_datetime(DATE_08310000)
        text = '08/31/2024 MAJOR LEAGUE BASEBALL Final Scores\n' + SCORES

        data = {'scores': {}, 'started': False, 'table': {}}
        statsplus = self.create_statsplus(data)
        actual = statsplus.save_scores(date, text)
        expected = Response(
            notify=[Notify.STATSPLUS_SAVE],
            shadow=statsplus.get_shadow_scores(),
            thread_=[Thread(target='parse_saved_scores', args=(date, ))])
        self.assertEqual(actual, expected)

        scores = {date: {'2449': 'T47 6, T40 5'}}
        write = {'scores': scores, 'started': False, 'table': {}}
        self.assertNotCalled(self.chat_post_message_, self.log_)
        self.open_handle_.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch.object(Statsplus, 'cleanup')
    def test_start(self, cleanup_):
        date = encode_datetime(DATE_08310000)
        scores = {date: {'2449': 'T47 6, T40 5'}}
        table = {'T40': '0-1', 'T47': '1-0'}
        data = {'scores': scores, 'started': False, 'table': table}
        statsplus = self.create_statsplus(data)
        statsplus.start()

        write = {'scores': {}, 'started': True, 'table': {}}
        cleanup_.assert_called_once_with()
        self.chat_post_message_.assert_called_once_with(
            'fairylab', 'Sim in progress.')
        self.log_.assert_called_once_with(logging.INFO, 'Sim in progress.')
        self.open_handle_.write.assert_called_once_with(dumps(write) + '\n')

    def test_is_valid_message__false(self):
        obj = {'bot_id': 'B123', 'channel': 'C123', 'text': 'foo'}

        data = {'scores': {}, 'started': False, 'table': {}}
        statsplus = self.create_statsplus(data)
        actual = statsplus.is_valid_message(obj)
        expected = False
        self.assertEqual(actual, expected)

        self.assertNotCalled(self.chat_post_message_, self.log_,
                             self.open_handle_.write)

    def test_is_valid_message__true(self):
        obj = {'bot_id': 'B7KJ3362Y', 'channel': 'C7JSGHW8G', 'text': 'foo'}

        data = {'scores': {}, 'started': False, 'table': {}}
        statsplus = self.create_statsplus(data)
        actual = statsplus.is_valid_message(obj)
        expected = True
        self.assertEqual(actual, expected)

        self.assertNotCalled(self.chat_post_message_, self.log_,
                             self.open_handle_.write)


if __name__ == '__main__':
    unittest.main()
