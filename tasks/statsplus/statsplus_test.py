#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import re
import sys
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.extend((_path, re.sub(r'/tasks/statsplus', '', _path)))

from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa
from data.shadow.shadow import Shadow  # noqa
from data.thread_.thread_ import Thread  # noqa
from tasks.statsplus.statsplus import Statsplus  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import table  # noqa
from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.jinja2_.jinja2_ import env  # noqa
from common.json_.json_ import dumps  # noqa
from util.team.team import logo_inline  # noqa
from common.test.test import Test  # noqa
from common.test.test import main  # noqa

EXTRACT_DIR = re.sub(r'/tasks/statsplus', '/resource/extract', _path)
GAMES_DIR = re.sub(r'/tasks/statsplus', '/resource/games', _path)
RESOURCE_DIR = re.sub(r'/tasks/statsplus', '/resource', _path)

_env = env()
_now = datetime_datetime_pst(2022, 10, 10)
_now_encoded = '2022-10-10T00:00:00-07:00'
_then = datetime_datetime_pst(2022, 10, 9)
_then_encoded = '2022-10-09T00:00:00-07:00'

_highlights_pattern = '<[^|]+\|[^<]+> (?:sets|ties) [^)]+\)'
_highlights_encoded = [
    '<{0}{1}38868.html|Connor Harrell> ties the BOS regular season game reco' +
    'rd for runs with 4 (T34 @ T57)'
]
_highlights_table = table(body=[[cell(content='Player set the record.')]])
_highlights_text = '<{0}{1}38868.html|Connor Harrell> ties the BOS regular' + \
                   ' season game record for runs with 4 (Boston @ Tampa Bay)'

_injuries_clarified = [
    'SP <{0}{1}37102.html|Jairo Labourt> was injured while pitching (T54 @ T' +
    '34)',
    'SS <{0}{1}29923.html|Jeremy Houston> was injured while running the base' +
    's (T54 @ T34)',
    'CF <{0}{1}1473.html|Jeren Kendall> was injured while running the bases ' +
    '(T31 @ T45)',
    'SP <{0}{1}29663.html|Dakota Donovan> was injured while pitching (T48 @ ' +
    'T44)'
]
_injuries_encoded = [
    'SP <{0}{1}37102.html|Jairo Labourt> was injured while pitching (T54 @ T' +
    '34)',
    'SS <{0}{1}29923.html|Jeremy Houston> was injured while running the base' +
    's (T54 @ T34)',
    'CF <{0}{1}1473.html|Jeren Kendall> was injured while running the bases ' +
    '(T31 @ TLA)',
    'SP <{0}{1}29663.html|Dakota Donovan> was injured while pitching (TNY @ ' +
    'TLA)'
]
_injuries_pattern = '\w+ <[^|]+\|[^<]+> was injured [^)]+\)'
_injuries_table = table(body=[[cell(content='Player was injured.')]])
_injuries_text = 'SP <{0}{1}37102.html|Jairo Labourt> was injured while pi' + \
                 'tching (Seattle @ Boston)'

_scores_pattern = '<[^|]+\|[^<]+>'
_scores_regular_clarified = [
    '<{0}{1}2998.html|T31 4, T45 2>', '<{0}{1}3003.html|T32 2, T33 1>',
    '<{0}{1}2996.html|T37 7, T46 2>', '<{0}{1}3002.html|T40 11, T35 4>',
    '<{0}{1}2993.html|T42 7, T54 2>', '<{0}{1}2991.html|T43 8, T38 2>',
    '<{0}{1}14721.html|T41 6, T36 2>', '<{0}{1}3001.html|T49 1, T55 0>',
    '<{0}{1}3000.html|T48 5, T44 3>', '<{0}{1}2992.html|T51 3, T60 1>',
    '<{0}{1}2999.html|T53 8, T39 2>', '<{0}{1}2990.html|T56 5, T52 4>',
    '<{0}{1}2997.html|T57 12, T34 9>', '<{0}{1}2994.html|T58 5, T50 3>',
    '<{0}{1}2995.html|T59 8, T47 2>'
]
_scores_postseason_encoded = [
    '<{0}{1}25051.html|T45 8, T53 3>', '<{0}{1}25043.html|T54 6, T34 3>'
]
_scores_regular_encoded = [
    '<{0}{1}2998.html|T31 4, TLA 2>', '<{0}{1}3003.html|T32 2, T33 1>',
    '<{0}{1}2996.html|T37 7, T46 2>', '<{0}{1}3002.html|T40 11, TCH 4>',
    '<{0}{1}2993.html|T42 7, T54 2>', '<{0}{1}2991.html|T43 8, T38 2>',
    '<{0}{1}14721.html|T41 6, TCH 2>', '<{0}{1}3001.html|TNY 1, T55 0>',
    '<{0}{1}3000.html|TNY 5, TLA 3>', '<{0}{1}2992.html|T51 3, T60 1>',
    '<{0}{1}2999.html|T53 8, T39 2>', '<{0}{1}2990.html|T56 5, T52 4>',
    '<{0}{1}2997.html|T57 12, T34 9>', '<{0}{1}2994.html|T58 5, T50 3>',
    '<{0}{1}2995.html|T59 8, T47 2>'
]
_scores_table = table(
    head=cell(content='2022-10-10'),
    body=[[cell(content='Baltimore 1, Boston 0')]])
_scores_regular_text = '*<{0}{1}2998.html|Arizona 4, Los Angeles 2>*\n' + \
                       '*<{0}{1}3003.html|Atlanta 2, Baltimore 1>*\n' + \
                       '*<{0}{1}2996.html|Cincinnati 7, Milwaukee 2>*\n' + \
                       '*<{0}{1}3002.html|Detroit 11, Chicago 4>*\n' + \
                       '*<{0}{1}2993.html|Houston 7, Seattle 2>*\n' + \
                       '*<{0}{1}2991.html|Kansas City 8, Cleveland 2>*\n' + \
                       '*<{0}{1}14721.html|Miami 6, Chicago 2>*\n' + \
                       '*<{0}{1}3001.html|New York 1, San Francisco 0>*\n' + \
                       '*<{0}{1}3000.html|New York 5, Los Angeles 3>*\n' + \
                       '*<{0}{1}2992.html|Philadelphia 3, Washington 1>*\n' + \
                       '*<{0}{1}2999.html|San Diego 8, Colorado 2>*\n' + \
                       '*<{0}{1}2990.html|St. Louis 5, Pittsburgh 4>*\n' + \
                       '*<{0}{1}2997.html|Tampa Bay 12, Boston 9>*\n' + \
                       '*<{0}{1}2994.html|Texas 5, Oakland 3>*\n' + \
                       '*<{0}{1}2995.html|Toronto 8, Minnesota 2>*'

_standings_new = {'31': '76-86', '32': '77-85', '44': '70-92', '45': '97-65'}
_standings_old = {'31': '75-85', '32': '76-85', '44': '70-91', '45': '96-64'}

_table_encoded_new = {
    'T35': 82,
    'T36': 71,
    'T44': 70,
    'T45': 97,
    'T48': 88,
    'T49': 95
}
_table_encoded_old = {
    'T35': 82,
    'T36': 71,
    'T44': 70,
    'T45': 97,
    'T48': 87,
    'T49': 94
}
_table_text = '```MAJOR LEAGUE BASEBALL Live Table - 10/10/2022\nCincinnat' + \
              'i Reds 111\nSan Diego Padres 104\nBoston Red Sox 99\nSeattl' + \
              'e Mariners 98\nLos Angeles Dodgers 97\nNew York Mets 95\nSt' + \
              '. Louis Cardinals 89\nColorado Rockies 88\nMinnesota Twins ' + \
              '88\nNew York Yankees 88\nDetroit Tigers 86\nHouston Astros ' + \
              '85\nMiami Marlins 84\nChicago White Sox 82\nAtlanta Braves ' + \
              '77\nMilwaukee Brewers 77\nCleveland Indians 76\nArizona Dia' + \
              'mondbacks 76\nKansas City Royals 76\nPhiladelphia Phillies ' + \
              '75\nOakland Athletics 75\nWashington Nationals 73\nToronto ' + \
              'Blue Jays 73\nChicago Cubs 71\nBaltimore Orioles 70\nLos An' + \
              'geles Angels 70\nTexas Rangers 67\nTampa Bay Rays 65\nSan F' + \
              'rancisco Giants 62\nPittsburgh Pirates 53```'

_html = 'https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/'
_game_box = 'box_scores/game_box_'
_game_game = 'games/game_'
_game_log = 'game_logs/log_'
_player = 'players/player_'


def _data(finished=False,
          highlights={},
          injuries={},
          offseason=False,
          postseason=False,
          scores={},
          started=False,
          table={},
          unchecked=[]):
    return {
        'finished': finished,
        'highlights': highlights,
        'injuries': injuries,
        'offseason': offseason,
        'postseason': postseason,
        'scores': scores,
        'started': started,
        'table': table,
        'unchecked': unchecked,
    }


def _game_box_sub(s):
    return s.format(_html, _game_box)


def _game_log_sub(s):
    return s.format(_html, _game_log)


def _player_sub(s):
    return s.format(_html, _player)


class StatsplusTest(Test):
    def setUp(self):
        patch_open = mock.patch(
            'api.serializable.serializable.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

        patch_chat = mock.patch.object(Statsplus, '_chat')
        self.addCleanup(patch_chat.stop)
        self.mock_chat = patch_chat.start()

        patch_log = mock.patch('tasks.statsplus.statsplus.logger_.log')
        self.addCleanup(patch_log.stop)
        self.mock_log = patch_log.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]

    def reset_mocks(self):
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()
        self.mock_chat.reset_mock()
        self.mock_log.reset_mock()

    def create_statsplus(self, data):
        self.init_mocks(data)
        statsplus = Statsplus(date=_now, e=_env)
        statsplus.shadow['leaguefile.end'] = _now_encoded

        self.mock_open.assert_called_once_with(Statsplus._data(), 'r')
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()

        self.reset_mocks()
        self.init_mocks(data)

        return statsplus

    def test_notify__with_finish(self):
        statsplus = self.create_statsplus(_data())
        response = statsplus._notify_internal(notify=Notify.LEAGUEFILE_DOWNLOAD)
        self.assertEqual(response, Response())

        write = _data(finished=True)
        self.mock_open.assert_called_with(Statsplus._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()

    def test_notify__with_year(self):
        statsplus = self.create_statsplus(_data())
        response = statsplus._notify_internal(notify=Notify.LEAGUEFILE_YEAR)
        self.assertEqual(response, Response())

        write = _data(offseason=True)
        self.mock_open.assert_called_with(Statsplus._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()

    def test_notify__with_other(self):
        statsplus = self.create_statsplus(_data())
        response = statsplus._notify_internal(notify=Notify.OTHER)
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()

    @mock.patch.object(Statsplus, '_handle_table')
    @mock.patch.object(Statsplus, '_render')
    @mock.patch.object(Statsplus, '_handle_key')
    @mock.patch.object(Statsplus, '_clear')
    def test_on_message__with_finished(self, mock_clear, mock_handle,
                                       mock_render, mock_table):
        date = '10/10/2022 MAJOR LEAGUE BASEBALL Final Scores\n'
        text = date + _game_box_sub(_scores_regular_text)
        obj = {
            'channel': 'C7JSGHW8G',
            'text': text,
            'ts': '1000.789',
            'user': 'U1234',
            'bot_id': 'B7KJ3362Y'
        }
        statsplus = self.create_statsplus(_data(finished=True))
        response = statsplus._on_message_internal(obj=obj)
        self.assertEqual(response, Response(notify=[Notify.STATSPLUS_SIM]))

        write = _data()
        mock_clear.assert_called_once_with()
        mock_handle.assert_called_once_with('scores', _now_encoded, text,
                                            _scores_pattern, False)
        mock_render.assert_not_called()
        mock_table.assert_not_called()
        self.mock_open.assert_called_with(Statsplus._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_called_once_with('fairylab', 'Sim in progress.')
        self.mock_log.assert_not_called()

    @mock.patch.object(Statsplus, '_handle_table')
    @mock.patch.object(Statsplus, '_render')
    @mock.patch.object(Statsplus, '_handle_key')
    @mock.patch.object(Statsplus, '_clear')
    def test_on_message__with_scores(self, mock_clear, mock_handle,
                                     mock_render, mock_table):
        date = '10/10/2022 MAJOR LEAGUE BASEBALL Final Scores\n'
        text = date + _game_box_sub(_scores_regular_text)
        obj = {
            'channel': 'C7JSGHW8G',
            'text': text,
            'ts': '1000.789',
            'user': 'U1234',
            'bot_id': 'B7KJ3362Y'
        }
        statsplus = self.create_statsplus(_data())
        response = statsplus._on_message_internal(obj=obj)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        mock_clear.assert_not_called()
        mock_handle.assert_called_once_with('scores', _now_encoded, text,
                                            _scores_pattern, False)
        mock_render.assert_not_called()
        mock_table.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()

    @mock.patch.object(Statsplus, '_handle_table')
    @mock.patch.object(Statsplus, '_render')
    @mock.patch.object(Statsplus, '_handle_key')
    @mock.patch.object(Statsplus, '_clear')
    def test_on_message__with_scores_and_postseason(
            self, mock_clear, mock_handle, mock_render, mock_table):
        date = '10/10/2022 MAJOR LEAGUE BASEBALL Final Scores\n'
        text = date + _game_box_sub(_scores_regular_text)
        obj = {
            'channel': 'C7JSGHW8G',
            'text': text,
            'ts': '1000.789',
            'user': 'U1234',
            'bot_id': 'B7KJ3362Y'
        }
        statsplus = self.create_statsplus(_data(offseason=True, postseason=True))
        response = statsplus._on_message_internal(obj=obj)
        self.assertEqual(
            response,
            Response(notify=[Notify.BASE], shadow=statsplus._shadow_internal()))

        write = _data(offseason=True)
        mock_clear.assert_not_called()
        mock_handle.assert_called_once_with('scores', _now_encoded, text,
                                            _scores_pattern, False)
        mock_render.assert_called_once_with(obj=obj)
        mock_table.assert_not_called()
        self.mock_open.assert_called_with(Statsplus._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()

    @mock.patch.object(Statsplus, '_handle_table')
    @mock.patch.object(Statsplus, '_render')
    @mock.patch.object(Statsplus, '_handle_key')
    @mock.patch.object(Statsplus, '_clear')
    def test_on_message__with_table(self, mock_clear, mock_handle, mock_render,
                                    mock_table):
        obj = {
            'channel': 'C7JSGHW8G',
            'text': _table_text,
            'ts': '1000.789',
            'user': 'U1234',
            'bot_id': 'B7KJ3362Y'
        }
        statsplus = self.create_statsplus(_data())
        response = statsplus._on_message_internal(obj=obj)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        mock_clear.assert_not_called()
        mock_handle.assert_not_called()
        mock_render.assert_called_once_with(obj=obj)
        mock_table.assert_called_once_with(_now_encoded, _table_text)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()

    @mock.patch.object(Statsplus, '_handle_table')
    @mock.patch.object(Statsplus, '_render')
    @mock.patch.object(Statsplus, '_handle_key')
    @mock.patch.object(Statsplus, '_clear')
    def test_on_message__with_table_and_postseason(
            self, mock_clear, mock_handle, mock_render, mock_table):
        obj = {
            'channel': 'C7JSGHW8G',
            'text': _table_text,
            'ts': '1000.789',
            'user': 'U1234',
            'bot_id': 'B7KJ3362Y'
        }
        statsplus = self.create_statsplus(_data(offseason=True))
        response = statsplus._on_message_internal(obj=obj)
        self.assertEqual(
            response,
            Response(notify=[Notify.BASE], shadow=statsplus._shadow_internal()))

        write = _data()
        mock_clear.assert_not_called()
        mock_handle.assert_not_called()
        mock_render.assert_not_called()
        mock_table.assert_called_once_with(_now_encoded, _table_text)
        self.mock_open.assert_called_with(Statsplus._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()

    @mock.patch.object(Statsplus, '_handle_table')
    @mock.patch.object(Statsplus, '_render')
    @mock.patch.object(Statsplus, '_handle_key')
    @mock.patch.object(Statsplus, '_clear')
    def test_on_message__with_delay(self, mock_clear, mock_handle, mock_render,
                                    mock_table):
        delay = '10/10/2022 Rain delay of 19 minutes in the 2nd inning. '
        text = delay + _player_sub(_injuries_text)
        obj = {
            'channel': 'C7JSGHW8G',
            'text': text,
            'ts': '1000.789',
            'user': 'U1234',
            'bot_id': 'B7KJ3362Y'
        }
        statsplus = self.create_statsplus(_data())
        response = statsplus._on_message_internal(obj=obj)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        mock_clear.assert_not_called()
        mock_handle.assert_called_once_with('injuries', _now_encoded, text,
                                            _injuries_pattern, True)
        mock_render.assert_not_called()
        mock_table.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()

    @mock.patch.object(Statsplus, '_handle_table')
    @mock.patch.object(Statsplus, '_render')
    @mock.patch.object(Statsplus, '_handle_key')
    @mock.patch.object(Statsplus, '_clear')
    def test_on_message__with_injuries(self, mock_clear, mock_handle,
                                       mock_render, mock_table):
        text = '10/10/2022 ' + _player_sub(_injuries_text)
        obj = {
            'channel': 'C7JSGHW8G',
            'text': text,
            'ts': '1000.789',
            'user': 'U1234',
            'bot_id': 'B7KJ3362Y'
        }
        statsplus = self.create_statsplus(_data())
        response = statsplus._on_message_internal(obj=obj)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        mock_clear.assert_not_called()
        mock_handle.assert_called_once_with('injuries', _now_encoded, text,
                                            _injuries_pattern, True)
        mock_render.assert_not_called()
        mock_table.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()

    @mock.patch.object(Statsplus, '_handle_table')
    @mock.patch.object(Statsplus, '_render')
    @mock.patch.object(Statsplus, '_handle_key')
    @mock.patch.object(Statsplus, '_clear')
    def test_on_message__with_highlights(self, mock_clear, mock_handle,
                                         mock_render, mock_table):
        text = '10/10/2022 ' + _player_sub(_highlights_text)
        obj = {
            'channel': 'C7JSGHW8G',
            'text': text,
            'ts': '1000.789',
            'user': 'U1234',
            'bot_id': 'B7KJ3362Y'
        }
        statsplus = self.create_statsplus(_data())
        response = statsplus._on_message_internal(obj=obj)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        mock_clear.assert_not_called()
        mock_handle.assert_called_once_with('highlights', _now_encoded, text,
                                            _highlights_pattern, True)
        mock_render.assert_not_called()
        mock_table.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()

    @mock.patch.object(Statsplus, '_handle_table')
    @mock.patch.object(Statsplus, '_render')
    @mock.patch.object(Statsplus, '_handle_key')
    @mock.patch.object(Statsplus, '_clear')
    def test_on_message__with_invalid_bot_id(self, mock_clear, mock_handle,
                                             mock_render, mock_table):
        date = '10/09/2022 MAJOR LEAGUE BASEBALL Final Scores\n'
        text = date + _game_box_sub(_scores_regular_text)
        obj = {
            'channel': 'G3SUFLMK4',
            'text': text,
            'ts': '1000.789',
            'user': 'U1234',
        }
        statsplus = self.create_statsplus(_data())
        response = statsplus._on_message_internal(obj=obj)
        self.assertEqual(response, Response())

        mock_clear.assert_not_called()
        mock_handle.assert_not_called()
        mock_render.assert_not_called()
        mock_table.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()

    @mock.patch.object(Statsplus, '_handle_table')
    @mock.patch.object(Statsplus, '_render')
    @mock.patch.object(Statsplus, '_handle_key')
    @mock.patch.object(Statsplus, '_clear')
    def test_on_message__with_invalid_date(self, mock_clear, mock_handle,
                                           mock_render, mock_table):
        date = '10/09/2022 MAJOR LEAGUE BASEBALL Final Scores\n'
        text = date + _game_box_sub(_scores_regular_text)
        obj = {
            'channel': 'C7JSGHW8G',
            'text': text,
            'ts': '1000.789',
            'user': 'U1234',
            'bot_id': 'B7KJ3362Y'
        }
        statsplus = self.create_statsplus(_data())
        response = statsplus._on_message_internal(obj=obj)
        self.assertEqual(response, Response())

        mock_clear.assert_not_called()
        mock_handle.assert_not_called()
        mock_render.assert_not_called()
        mock_table.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()

    @mock.patch.object(Statsplus, '_handle_table')
    @mock.patch.object(Statsplus, '_render')
    @mock.patch.object(Statsplus, '_handle_key')
    @mock.patch.object(Statsplus, '_clear')
    def test_on_message__with_invalid_channel(self, mock_clear, mock_handle,
                                              mock_render, mock_table):
        date = '10/10/2022 MAJOR LEAGUE BASEBALL Final Scores\n'
        text = date + _game_box_sub(_scores_regular_text)
        obj = {
            'channel': 'G3SUFLMK4',
            'text': text,
            'ts': '1000.789',
            'user': 'U1234',
            'bot_id': 'B7KJ3362Y'
        }
        statsplus = self.create_statsplus(_data())
        response = statsplus._on_message_internal(obj=obj)
        self.assertEqual(response, Response())

        mock_clear.assert_not_called()
        mock_handle.assert_not_called()
        mock_render.assert_not_called()
        mock_table.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()

    @mock.patch.object(Statsplus, '_render')
    def test_run__with_extractd(self, mock_render):
        statsplus = self.create_statsplus(_data())
        response = statsplus._run_internal(date=_now)
        self.assertEqual(response, Response())

        mock_render.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()

    @mock.patch.object(Statsplus, '_render')
    def test_run__with_unchecked(self, mock_render):
        statsplus = self.create_statsplus(_data(unchecked=[_then_encoded]))
        response = statsplus._run_internal(date=_now)
        thread_ = Thread(target='_extract_all', args=([_then_encoded], ))
        self.assertEqual(response, Response(thread_=[thread_]))

        mock_render.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()

    @mock.patch.object(Statsplus, '_home')
    def test_render(self, mock_home):
        home = {'breadcrumbs': [], 'live': []}
        mock_home.return_value = home

        statsplus = self.create_statsplus(_data())
        value = statsplus._render_internal(date=_now)
        index = 'statsplus/index.html'
        self.assertEqual(value, [(index, '', 'statsplus.html', home)])

        mock_home.assert_called_once_with(date=_now)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()

    @mock.patch.object(Statsplus, '_render')
    def test_setup(self, mock_render):
        statsplus = self.create_statsplus(_data())
        response = statsplus._setup_internal(date=_now)
        self.assertEqual(response, Response())

        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()

    def test_shadow(self):
        statsplus = self.create_statsplus(_data())
        value = statsplus._shadow_internal()
        self.assertEqual(value, [
            Shadow(destination='recap', key='statsplus.offseason', info=False),
            Shadow(
                destination='recap', key='statsplus.postseason', info=False)
        ])

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()

    @mock.patch('tasks.statsplus.statsplus.check_output')
    def test_clear(self, mock_check):
        read = _data(
            highlights={_then_encoded: _highlights_encoded},
            injuries={_then_encoded: _injuries_encoded},
            scores={_then_encoded: _scores_regular_encoded})
        statsplus = self.create_statsplus(read)
        statsplus._clear()

        mock_check.assert_has_calls([
            mock.call(['rm', '-rf', GAMES_DIR]),
            mock.call(['mkdir', GAMES_DIR]),
        ])
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(statsplus.data['highlights'], {})
        self.assertEqual(statsplus.data['injuries'], {})
        self.assertEqual(statsplus.data['scores'], {})

    def test_handle_key__delay(self):
        statsplus = self.create_statsplus(_data())
        delay = '10/10/2022 Rain delay of 19 minutes in the 2nd inning. '
        text = delay + _player_sub(_injuries_text)
        statsplus._handle_key('injuries', _then_encoded, text, _injuries_pattern,
                           True)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(statsplus.data['injuries'],
                         {_then_encoded: _injuries_encoded[:1]})
        self.assertEqual(statsplus.data['unchecked'], [])

    def test_handle_key__highlights(self):
        statsplus = self.create_statsplus(_data())
        text = '10/10/2022 ' + _player_sub(_highlights_text)
        statsplus._handle_key('highlights', _then_encoded, text,
                           _highlights_pattern, True)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(statsplus.data['highlights'],
                         {_then_encoded: _highlights_encoded[:1]})
        self.assertEqual(statsplus.data['unchecked'], [])

    def test_handle_key__injuries(self):
        statsplus = self.create_statsplus(_data())
        text = '10/10/2022 ' + _player_sub(_injuries_text)
        statsplus._handle_key('injuries', _then_encoded, text, _injuries_pattern,
                           True)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(statsplus.data['injuries'],
                         {_then_encoded: _injuries_encoded[:1]})
        self.assertEqual(statsplus.data['unchecked'], [])

    def test_handle_key__scores(self):
        statsplus = self.create_statsplus(_data())
        date = '10/10/2022 MAJOR LEAGUE BASEBALL Final Scores\n'
        text = date + _game_box_sub(_scores_regular_text)
        statsplus._handle_key('scores', _then_encoded, text, _scores_pattern,
                           False)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(statsplus.data['scores'],
                         {_then_encoded: _scores_regular_encoded})
        self.assertEqual(
            statsplus.data['unchecked'], [[_then_encoded, id_] for id_ in [
                '2998', '3003', '2996', '3002', '2993', '2991', '14721',
                '3001', '3000', '2992', '2999', '2990', '2997', '2994', '2995'
            ]])

    def test_handle_table(self):
        statsplus = self.create_statsplus(_data())
        statsplus._handle_table(_then_encoded, _table_text)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.assertEqual(statsplus.data['table'],
                         {_then_encoded: _table_encoded_new})
        self.assertEqual(statsplus.data['unchecked'], [])

    @mock.patch.object(Statsplus, '_table')
    @mock.patch('tasks.statsplus.statsplus.standings_table')
    @mock.patch.object(Statsplus, '_live_postseason')
    @mock.patch.object(Statsplus, '_forecast')
    def test_home__with_postseason(self, mock_forecast, mock_live,
                                   mock_standings, mock_table):
        live_postseason = table(body=[[
            cell(content='Baltimore'),
            cell(content='1'),
            cell(content='0'),
            cell(content='Boston')
        ]])
        mock_live.return_value = [live_postseason]
        mock_table.side_effect = [
            _highlights_table,
            _injuries_table,
            _scores_table,
            _scores_table,
        ]

        read = _data(
            highlights={_then_encoded: _highlights_encoded},
            injuries={_then_encoded: _injuries_encoded},
            postseason=True,
            scores={
                _then_encoded: _scores_regular_encoded,
                _now_encoded: _scores_regular_encoded
            })
        statsplus = self.create_statsplus(read)
        actual = statsplus._home(date=_now)
        breadcrumbs = [{
            'href': '/',
            'name': 'Fairylab'
        }, {
            'href': '',
            'name': 'Statsplus'
        }]
        expected = {
            'breadcrumbs': breadcrumbs,
            'live': [live_postseason],
            'highlights': [_highlights_table],
            'injuries': [_injuries_table],
            'scores': [_scores_table, _scores_table],
            'forecast': {}
        }
        self.assertEqual(actual, expected)

        mock_forecast.assert_not_called()
        mock_live.assert_called_once_with()
        calls = [
            mock.call('highlights', _then_encoded, _player),
            mock.call('injuries', _then_encoded, _player),
            mock.call('scores', _then_encoded, _game_box),
            mock.call('scores', _now_encoded, _game_box),
        ]
        mock_standings.assert_not_called()
        mock_table.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()

    @mock.patch.object(Statsplus, '_table')
    @mock.patch('tasks.statsplus.statsplus.standings_table')
    @mock.patch.object(Statsplus, '_live_regular')
    @mock.patch.object(Statsplus, '_forecast')
    def test_home__with_regular(self, mock_forecast, mock_live, mock_standings,
                                mock_table):
        cols = [
            col(clazz='position-relative text-truncate'),
            col(clazz='text-right w-55p'),
            col(clazz='text-right w-55p')
        ]
        standings_table = [
            table(
                hcols=cols,
                bcols=cols,
                head=[
                    cell(content='AL East'),
                    cell(content='W'),
                    cell(content='L')
                ],
                body=[[
                    cell(content='33'),
                    cell(content='0'),
                    cell(content='0')
                ], [cell(content='34'),
                    cell(content='0'),
                    cell(content='0')], [
                        cell(content='48'),
                        cell(content='0'),
                        cell(content='0')
                    ], [
                        cell(content='57'),
                        cell(content='0'),
                        cell(content='0')
                    ], [
                        cell(content='59'),
                        cell(content='0'),
                        cell(content='0')
                    ]])
        ]
        mock_forecast.return_value = _standings_new
        live_regular = table(
            body=[[cell(content='BAL 1-0'),
                   cell(content='BOS 0-1')]])
        mock_live.return_value = [live_regular]
        mock_standings.return_value = [standings_table]
        mock_table.side_effect = [
            _highlights_table,
            _injuries_table,
            _scores_table,
            _scores_table,
        ]

        read = _data(
            highlights={_then_encoded: _highlights_encoded},
            injuries={_then_encoded: _injuries_encoded},
            scores={
                _then_encoded: _scores_regular_encoded,
                _now_encoded: _scores_regular_encoded
            })
        statsplus = self.create_statsplus(read)
        actual = statsplus._home(date=_now)
        breadcrumbs = [{
            'href': '/',
            'name': 'Fairylab'
        }, {
            'href': '',
            'name': 'Statsplus'
        }]
        expected = {
            'breadcrumbs': breadcrumbs,
            'live': [live_regular],
            'highlights': [_highlights_table],
            'injuries': [_injuries_table],
            'scores': [_scores_table, _scores_table],
            'forecast': [standings_table]
        }
        self.assertEqual(actual, expected)

        mock_forecast.assert_called_once_with()
        mock_live.assert_called_once_with()
        calls = [
            mock.call('highlights', _then_encoded, _player),
            mock.call('injuries', _then_encoded, _player),
            mock.call('scores', _then_encoded, _game_box),
            mock.call('scores', _now_encoded, _game_box),
        ]
        mock_standings.assert_called_once_with(_standings_new)
        mock_table.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()

    @mock.patch.object(Statsplus, '_table')
    @mock.patch('tasks.statsplus.statsplus.standings_table')
    @mock.patch.object(Statsplus, '_live_regular')
    @mock.patch.object(Statsplus, '_forecast')
    def test_home__with_finished(self, mock_forecast, mock_live,
                                 mock_standings, mock_table):
        live_regular = table(
            body=[[cell(content='BAL 1-0'),
                   cell(content='BOS 0-1')]])
        mock_live.return_value = [live_regular]
        mock_table.side_effect = [
            _highlights_table,
            _injuries_table,
            _scores_table,
            _scores_table,
        ]

        read = _data(
            finished=True,
            highlights={_then_encoded: _highlights_encoded},
            injuries={_then_encoded: _injuries_encoded},
            scores={
                _then_encoded: _scores_regular_encoded,
                _now_encoded: _scores_regular_encoded
            })
        statsplus = self.create_statsplus(read)
        actual = statsplus._home(date=_now)
        breadcrumbs = [{
            'href': '/',
            'name': 'Fairylab'
        }, {
            'href': '',
            'name': 'Statsplus'
        }]
        expected = {
            'breadcrumbs': breadcrumbs,
            'live': [live_regular],
            'highlights': [_highlights_table],
            'injuries': [_injuries_table],
            'scores': [_scores_table, _scores_table],
            'forecast': {}
        }
        self.assertEqual(actual, expected)

        mock_forecast.assert_not_called()
        mock_live.assert_called_once_with()
        calls = [
            mock.call('highlights', _then_encoded, _player),
            mock.call('injuries', _then_encoded, _player),
            mock.call('scores', _then_encoded, _game_box),
            mock.call('scores', _now_encoded, _game_box),
        ]
        mock_standings.assert_not_called()
        mock_table.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()

    @mock.patch('tasks.statsplus.statsplus.teamids')
    @mock.patch.object(Statsplus, '_record')
    def test_forecast__with_empty(self, mock_record, mock_teamids):
        teamids = ['31', '32', '44', '45']
        mock_record.side_effect = ['1-1', '1-0', '0-1', '1-1']
        mock_teamids.return_value = teamids

        new = [
            '<{0}{1}2998.html|T31 4, T45 2>', '<{0}{1}3003.html|T32 2, T33 1>'
        ]
        old = ['<{0}{1}2998.html|T45 5, T31 3>']
        read = _data(
            finished=True, scores={
                _then_encoded: old,
                _now_encoded: new
            })
        statsplus = self.create_statsplus(read)
        statsplus.shadow['recap.standings'] = {}
        actual = statsplus._forecast()
        expected = {'31': '1-1', '32': '1-0', '44': '0-1', '45': '1-1'}
        self.assertEqual(actual, expected)

        mock_record.assert_has_calls([mock.call(t) for t in teamids])
        mock_teamids.assert_called_once_with()

    @mock.patch('tasks.statsplus.statsplus.teamids')
    @mock.patch.object(Statsplus, '_record')
    def test_forecast__with_valid_input(self, mock_record, mock_teamids):
        teamids = ['31', '32', '44', '45']
        mock_record.side_effect = ['1-1', '1-0', '0-1', '1-1']
        mock_teamids.return_value = teamids

        new = [
            '<{0}{1}2998.html|T31 4, T45 2>', '<{0}{1}3003.html|T32 2, T33 1>'
        ]
        old = ['<{0}{1}2998.html|T45 5, T31 3>']
        read = _data(
            finished=True, scores={
                _then_encoded: old,
                _now_encoded: new
            })
        statsplus = self.create_statsplus(read)
        statsplus.shadow['recap.standings'] = _standings_old
        actual = statsplus._forecast()
        expected = _standings_new
        self.assertEqual(actual, expected)

        mock_record.assert_has_calls([mock.call(t) for t in teamids])
        mock_teamids.assert_called_once_with()

    @mock.patch.object(Statsplus, '_live_postseason_body')
    def test_live_postseason(self, mock_body):
        body = [[
            cell(content='Baltimore'),
            cell(content='1'),
            cell(content='0'),
            cell(content='Boston')
        ]]
        mock_body.return_value = body

        read = _data(
            postseason=True,
            scores={_then_encoded: _scores_postseason_encoded})
        statsplus = self.create_statsplus(read)
        actual = statsplus._live_postseason()
        ps_header = table(
            clazz='table-fixed border border-bottom-0 mt-3',
            hcols=[col(clazz='text-center')],
            head=[cell(content='Postseason')])
        live_postseason = table(
            clazz='table-fixed border',
            bcols=[
                col(clazz='position-relative w-40'),
                col(clazz='text-center w-10'),
                col(clazz='text-center w-10'),
                col(clazz='position-relative text-right w-40')
            ],
            body=body)
        expected = [ps_header, live_postseason]
        self.assertEqual(actual, expected)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()

    @mock.patch.object(Statsplus, '_live_postseason_series')
    @mock.patch.object(Statsplus, '_record')
    @mock.patch('tasks.statsplus.statsplus.logo_absolute')
    def test_live_postseason_body(self, mock_logo, mock_record, mock_series):
        mock_logo.return_value = 'logo'
        mock_record.side_effect = ['1-0', '0-1', '0-1', '1-0']
        mock_series.return_value = [['T45', 'T53'], ['T34', 'T54']]

        statsplus = self.create_statsplus(_data())
        actual = statsplus._live_postseason_body()
        expected = [[
            cell(content='logo'),
            cell(content='1'),
            cell(content='0'),
            cell(content='logo')
        ], [
            cell(content='logo'),
            cell(content='1'),
            cell(content='0'),
            cell(content='logo')
        ]]
        self.assertEqual(actual, expected)

        homes = ['Los Angeles', 'San Diego', 'Seattle', 'Boston']
        sides = ['left', 'right'] * 2
        teamids = ['45', '53', '54', '34']
        calls = [mock.call(t, h, s) for t, h, s in zip(teamids, homes, sides)]
        mock_logo.assert_has_calls(calls)
        teamids = ['45', '53', '34', '54']
        calls = [mock.call(t) for t in teamids]
        mock_record.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()

    def test_live_postseason_series(self):
        read = _data(
            postseason=True,
            scores={_then_encoded: _scores_postseason_encoded})
        statsplus = self.create_statsplus(read)
        actual = statsplus._live_postseason_series()
        expected = [['T45', 'T53'], ['T34', 'T54']]
        self.assertEqual(actual, expected)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()

    @mock.patch.object(Statsplus, '_live_regular_body')
    @mock.patch('tasks.statsplus.statsplus.divisions')
    def test_live_regular(self, mock_divisions, mock_body):
        al = [('AL East', ['33', '34', '48']),
              ('AL Central', ['35', '38', '40']), ('AL West',
                                                   ['42', '44', '50'])]
        nl = [('NL East', ['32', '41', '49']),
              ('NL Central', ['36', '37', '46']), ('NL West',
                                                   ['31', '39', '45'])]
        mock_divisions.return_value = al + nl
        body = [[cell(content='BAL 1-0'), cell(content='BOS 0-1')]]
        mock_body.return_value = body

        statsplus = self.create_statsplus(_data())
        actual = statsplus._live_regular()
        al_header = table(
            clazz='table-fixed border border-bottom-0 mt-3',
            hcols=[col(clazz='text-center')],
            head=[cell(content='American League')])
        nl_header = table(
            clazz='table-fixed border border-bottom-0 mt-3',
            hcols=[col(clazz='text-center')],
            head=[cell(content='National League')])
        live_regular = table(
            clazz='table-fixed border',
            bcols=[col(clazz='td-sm position-relative text-center w-20')] * 5,
            body=body)
        expected = [al_header, live_regular, nl_header, live_regular]
        self.assertEqual(actual, expected)

        mock_divisions.assert_called_once_with()
        mock_body.assert_has_calls([mock.call(al), mock.call(nl)])
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()

    @mock.patch.object(Statsplus, '_record')
    @mock.patch('tasks.statsplus.statsplus.logo_inline')
    def test_live_regular_body(self, mock_logo, mock_record):
        mock_logo.return_value = 'logo'
        mock_record.side_effect = ['2-0', '0-2', '1-1'] * 3

        statsplus = self.create_statsplus(_data())
        al = [('AL East', ['33', '34', '48']),
              ('AL Central', ['35', '38', '40']), ('AL West',
                                                   ['42', '44', '50'])]
        actual = statsplus._live_regular_body(al)
        expected = [[cell(content='logo')] * 3, [cell(content='logo')] * 3,
                    [cell(content='logo')] * 3]
        self.assertEqual(actual, expected)

        records = ['2-0', '1-1', '0-2'] * 3
        teamids = ['33', '48', '34', '35', '40', '38', '42', '50', '44']
        calls = [mock.call(t, r) for t, r in zip(teamids, records)]
        mock_logo.assert_has_calls(calls)
        teamids = ['33', '34', '48', '35', '38', '40', '42', '44', '50']
        calls = [mock.call(t) for t in teamids]
        mock_record.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()

    def test_record__with_encoded(self):
        read = _data(
            scores={_now_encoded: _scores_regular_encoded},
            table={
                _then_encoded: _table_encoded_old,
                _now_encoded: _table_encoded_new
            })
        statsplus = self.create_statsplus(read)
        self.assertEqual(statsplus._record('31'), '1-0')
        self.assertEqual(statsplus._record('32'), '1-0')
        self.assertEqual(statsplus._record('33'), '0-1')
        self.assertEqual(statsplus._record('34'), '0-1')
        self.assertEqual(statsplus._record('35'), '0-1')
        self.assertEqual(statsplus._record('36'), '0-1')
        self.assertEqual(statsplus._record('37'), '1-0')
        self.assertEqual(statsplus._record('38'), '0-1')
        self.assertEqual(statsplus._record('39'), '0-1')
        self.assertEqual(statsplus._record('40'), '1-0')
        self.assertEqual(statsplus._record('41'), '1-0')
        self.assertEqual(statsplus._record('42'), '1-0')
        self.assertEqual(statsplus._record('43'), '1-0')
        self.assertEqual(statsplus._record('44'), '0-1')
        self.assertEqual(statsplus._record('45'), '0-1')
        self.assertEqual(statsplus._record('46'), '0-1')
        self.assertEqual(statsplus._record('47'), '0-1')
        self.assertEqual(statsplus._record('48'), '1-0')
        self.assertEqual(statsplus._record('49'), '1-0')
        self.assertEqual(statsplus._record('50'), '0-1')
        self.assertEqual(statsplus._record('51'), '1-0')
        self.assertEqual(statsplus._record('52'), '0-1')
        self.assertEqual(statsplus._record('53'), '1-0')
        self.assertEqual(statsplus._record('54'), '0-1')
        self.assertEqual(statsplus._record('55'), '0-1')
        self.assertEqual(statsplus._record('56'), '1-0')
        self.assertEqual(statsplus._record('57'), '1-0')
        self.assertEqual(statsplus._record('58'), '1-0')
        self.assertEqual(statsplus._record('59'), '1-0')
        self.assertEqual(statsplus._record('60'), '0-1')

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()

    def test_record__with_clarified(self):
        read = _data(scores={_now_encoded: _scores_regular_clarified})
        statsplus = self.create_statsplus(read)
        self.assertEqual(statsplus._record('31'), '1-0')
        self.assertEqual(statsplus._record('32'), '1-0')
        self.assertEqual(statsplus._record('33'), '0-1')
        self.assertEqual(statsplus._record('34'), '0-1')
        self.assertEqual(statsplus._record('35'), '0-1')
        self.assertEqual(statsplus._record('36'), '0-1')
        self.assertEqual(statsplus._record('37'), '1-0')
        self.assertEqual(statsplus._record('38'), '0-1')
        self.assertEqual(statsplus._record('39'), '0-1')
        self.assertEqual(statsplus._record('40'), '1-0')
        self.assertEqual(statsplus._record('41'), '1-0')
        self.assertEqual(statsplus._record('42'), '1-0')
        self.assertEqual(statsplus._record('43'), '1-0')
        self.assertEqual(statsplus._record('44'), '0-1')
        self.assertEqual(statsplus._record('45'), '0-1')
        self.assertEqual(statsplus._record('46'), '0-1')
        self.assertEqual(statsplus._record('47'), '0-1')
        self.assertEqual(statsplus._record('48'), '1-0')
        self.assertEqual(statsplus._record('49'), '1-0')
        self.assertEqual(statsplus._record('50'), '0-1')
        self.assertEqual(statsplus._record('51'), '1-0')
        self.assertEqual(statsplus._record('52'), '0-1')
        self.assertEqual(statsplus._record('53'), '1-0')
        self.assertEqual(statsplus._record('54'), '0-1')
        self.assertEqual(statsplus._record('55'), '0-1')
        self.assertEqual(statsplus._record('56'), '1-0')
        self.assertEqual(statsplus._record('57'), '1-0')
        self.assertEqual(statsplus._record('58'), '1-0')
        self.assertEqual(statsplus._record('59'), '1-0')
        self.assertEqual(statsplus._record('60'), '0-1')

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()

    @mock.patch.object(Statsplus, '_render')
    @mock.patch('tasks.statsplus.statsplus.parse_player')
    @mock.patch('tasks.statsplus.statsplus.open')
    @mock.patch('tasks.statsplus.statsplus.parse_game_data')
    def test_extract_all__with_valid_box_finished_false(
            self, mock_data, mock_open, mock_player, mock_render):
        _game_data = [{
            'away_runs': 4,
            'away_team': 'T31',
            'date': _then_encoded,
            'home_runs': 2,
            'home_team': 'T45',
            'ok': True
        }, {
            'away_runs': 11,
            'away_team': 'T40',
            'date': _then_encoded,
            'home_runs': 4,
            'home_team': 'T35',
            'ok': True
        }, {
            'away_runs': 2,
            'away_team': 'T36',
            'date': _then_encoded,
            'home_runs': 6,
            'home_team': 'T41',
            'ok': True
        }, {
            'away_runs': 1,
            'away_team': 'T49',
            'date': _then_encoded,
            'home_runs': 0,
            'home_team': 'T55',
            'ok': True
        }, {
            'away_runs': 5,
            'away_team': 'T48',
            'date': _then_encoded,
            'home_runs': 3,
            'home_team': 'T44',
            'ok': True
        }]
        mock_data.side_effect = _game_data
        mock_player.return_value = {
            'name': 'Dakota Donovan',
            'ok': True,
            'team': 'T44'
        }
        mo = mock.mock_open(read_data=dumps({}))
        mock_handle = mo()
        mock_open.side_effect = [mo.return_value] * 5
        unchecked = [[_then_encoded, id_]
                     for id_ in ['2998', '3002', '14721', '3001', '3000']]
        read = _data(
            highlights={_then_encoded: _highlights_encoded},
            injuries={_then_encoded: _injuries_encoded},
            scores={_then_encoded: _scores_regular_encoded},
            unchecked=unchecked)
        statsplus = self.create_statsplus(read)
        response = statsplus._extract_all(unchecked, date=_then)
        self.assertEqual(response, Response())

        write = _data(
            highlights={_then_encoded: _highlights_encoded},
            injuries={_then_encoded: _injuries_clarified},
            scores={_then_encoded: _scores_regular_clarified},
            unchecked=[])
        ids = [
            '{0}{1}2998{2}', '{0}{1}3002{2}', '{0}{1}14721{2}',
            '{0}{1}3001{2}', '{0}{1}3000{2}'
        ]
        mock_data.assert_has_calls([
            mock.call(
                id_.format(_html, _game_box, '.html'),
                id_.format(_html, _game_log, '.html')) for id_ in ids
        ])
        link = '{0}{1}29663.html'.format(_html, _player)
        mock_player.assert_called_once_with(link)
        mock_open.assert_has_calls([
            mock.call(
                id_.format(RESOURCE_DIR + '/', _game_game, '.json'), 'w')
            for id_ in ids
        ])
        mock_handle.write.assert_has_calls(
            [mock.call(dumps(gd) + '\n') for gd in _game_data])
        mock_render.assert_called_once_with(date=_then)
        self.mock_open.assert_called_once_with(Statsplus._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()

    @mock.patch.object(Statsplus, '_render')
    @mock.patch('tasks.statsplus.statsplus.parse_player')
    @mock.patch('tasks.statsplus.statsplus.open')
    @mock.patch('tasks.statsplus.statsplus.parse_game_data')
    def test_extract_all__with_valid_box_finished_true(
            self, mock_data, mock_open, mock_player, mock_render):
        _game_data = [{
            'away_runs': 4,
            'away_team': 'T31',
            'date': _then_encoded,
            'home_runs': 2,
            'home_team': 'T45',
            'ok': True
        }, {
            'away_runs': 11,
            'away_team': 'T40',
            'date': _then_encoded,
            'home_runs': 4,
            'home_team': 'T35',
            'ok': True
        }, {
            'away_runs': 2,
            'away_team': 'T36',
            'date': _then_encoded,
            'home_runs': 6,
            'home_team': 'T41',
            'ok': True
        }, {
            'away_runs': 1,
            'away_team': 'T49',
            'date': _then_encoded,
            'home_runs': 0,
            'home_team': 'T55',
            'ok': True
        }, {
            'away_runs': 5,
            'away_team': 'T48',
            'date': _then_encoded,
            'home_runs': 3,
            'home_team': 'T44',
            'ok': True
        }]
        mock_data.side_effect = _game_data
        mock_player.return_value = {
            'name': 'Dakota Donovan',
            'ok': True,
            'team': 'T44'
        }
        mo = mock.mock_open(read_data=dumps({}))
        mock_handle = mo()
        mock_open.side_effect = [mo.return_value] * 5
        unchecked = [[_then_encoded, id_]
                     for id_ in ['2998', '3002', '14721', '3001', '3000']]
        read = _data(
            finished=True,
            highlights={_then_encoded: _highlights_encoded},
            injuries={_then_encoded: _injuries_encoded},
            scores={_then_encoded: _scores_regular_encoded},
            unchecked=unchecked)
        statsplus = self.create_statsplus(read)
        response = statsplus._extract_all(unchecked, date=_then)
        self.assertEqual(response, Response())

        write = _data(
            finished=True,
            highlights={_then_encoded: _highlights_encoded},
            injuries={_then_encoded: _injuries_clarified},
            scores={_then_encoded: _scores_regular_clarified},
            unchecked=[])
        ids = [
            '{0}{1}2998{2}', '{0}{1}3002{2}', '{0}{1}14721{2}',
            '{0}{1}3001{2}', '{0}{1}3000{2}'
        ]
        mock_data.assert_has_calls([
            mock.call(
                id_.format(EXTRACT_DIR, _game_box, '.html'),
                id_.format(EXTRACT_DIR, _game_log, '.txt')) for id_ in ids
        ])
        link = '{0}{1}29663.html'.format(_html, _player)
        mock_player.assert_called_once_with(link)
        mock_open.assert_has_calls([
            mock.call(
                id_.format(RESOURCE_DIR + '/', _game_game, '.json'), 'w')
            for id_ in ids
        ])
        mock_handle.write.assert_has_calls(
            [mock.call(dumps(gd) + '\n') for gd in _game_data])
        mock_render.assert_called_once_with(date=_then)
        self.mock_open.assert_called_once_with(Statsplus._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()

    @mock.patch.object(Statsplus, '_render')
    @mock.patch('tasks.statsplus.statsplus.parse_player')
    @mock.patch('tasks.statsplus.statsplus.open')
    @mock.patch('tasks.statsplus.statsplus.parse_game_data')
    def test_extract_all__with_invalid_date(self, mock_data, mock_open,
                                            mock_player, mock_render):
        mock_data.return_value = {
            'away_runs': 4,
            'away_team': 'T31',
            'date': _now,
            'home_runs': 2,
            'home_team': 'T45',
            'ok': True
        }
        scores = ['<{0}{1}2998.html|T31 4, TLA 2>']
        unchecked = [[_then_encoded, '2998']]
        read = _data(scores={_then_encoded: scores}, unchecked=unchecked)
        statsplus = self.create_statsplus(read)
        response = statsplus._extract_all(unchecked, date=_then)
        self.assertEqual(response, Response())

        mock_data.assert_called_once_with(
            _game_box_sub('{0}{1}2998.html'), _game_log_sub('{0}{1}2998.html'))
        mock_player.assert_not_called()
        mock_open.assert_not_called()
        mock_render.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()

    def test_table__highlights(self):
        read = _data(highlights={_then_encoded: _highlights_encoded})
        statsplus = self.create_statsplus(read)

        actual = statsplus._table('highlights', _then_encoded, _player)
        body = [[
            cell(
                content=_player_sub(
                    '<a href="{0}{1}38868.html">Connor Harrell</a> ties the BO'
                    'S regular season game record for runs with 4 (Boston Red '
                    'Sox @ Tampa Bay Rays)'))
        ]]
        expected = table(
            head=[cell(content='Sunday, October 9th, 2022')], body=body)
        self.assertEqual(actual, expected)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()

    def test_table__injuries(self):
        read = _data(injuries={_then_encoded: _injuries_encoded})
        statsplus = self.create_statsplus(read)

        actual = statsplus._table('injuries', _then_encoded, _player)
        body = [[
            cell(
                content=_player_sub(
                    'SP <a href="{0}{1}37102.html">Jairo Labourt</a> was injur'
                    'ed while pitching (Seattle Mariners @ Boston Red Sox)'))
        ], [
            cell(
                content=_player_sub(
                    'SS <a href="{0}{1}29923.html">Jeremy Houston</a> was inju'
                    'red while running the bases (Seattle Mariners @ Boston Re'
                    'd Sox)'))
        ], [
            cell(
                content=_player_sub(
                    'CF <a href="{0}{1}1473.html">Jeren Kendall</a> was injure'
                    'd while running the bases (Arizona Diamondbacks @ Los Ang'
                    'eles)'))
        ], [
            cell(
                content=_player_sub(
                    'SP <a href="{0}{1}29663.html">Dakota Donovan</a> was inju'
                    'red while pitching (New York @ Los Angeles)'))
        ]]
        expected = table(
            head=[cell(content='Sunday, October 9th, 2022')], body=body)
        self.assertEqual(actual, expected)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()

    def test_table__scores(self):
        read = _data(scores={_then_encoded: _scores_regular_encoded})
        statsplus = self.create_statsplus(read)

        actual = statsplus._table('scores', _then_encoded, _game_box)
        body = [[
            cell(
                content=_game_box_sub(
                    '<a href="{0}{1}2998.html">Arizona Diamondbacks 4, Los Ang'
                    'eles 2</a>'))
        ], [
            cell(
                content=_game_box_sub(
                    '<a href="{0}{1}3003.html">Atlanta Braves 2, Baltimore Ori'
                    'oles 1</a>'))
        ], [
            cell(
                content=_game_box_sub(
                    '<a href="{0}{1}2996.html">Cincinnati Reds 7, Milwaukee Br'
                    'ewers 2</a>'))
        ], [
            cell(
                content=_game_box_sub(
                    '<a href="{0}{1}3002.html">Detroit Tigers 11, Chicago 4</a'
                    '>'))
        ], [
            cell(
                content=_game_box_sub(
                    '<a href="{0}{1}2993.html">Houston Astros 7, Seattle Marin'
                    'ers 2</a>'))
        ], [
            cell(
                content=_game_box_sub(
                    '<a href="{0}{1}2991.html">Kansas City Royals 8, Cleveland'
                    ' Indians 2</a>'))
        ], [
            cell(
                content=_game_box_sub(
                    '<a href="{0}{1}14721.html">Miami Marlins 6, Chicago 2</a>'
                ))
        ], [
            cell(
                content=_game_box_sub(
                    '<a href="{0}{1}3001.html">New York 1, San Francisco Giant'
                    's 0</a>'))
        ], [
            cell(
                content=_game_box_sub(
                    '<a href="{0}{1}3000.html">New York 5, Los Angeles 3</a>'))
        ], [
            cell(
                content=_game_box_sub(
                    '<a href="{0}{1}2992.html">Philadelphia Phillies 3, Washin'
                    'gton Nationals 1</a>'))
        ], [
            cell(
                content=_game_box_sub(
                    '<a href="{0}{1}2999.html">San Diego Padres 8, Colorado Ro'
                    'ckies 2</a>'))
        ], [
            cell(
                content=_game_box_sub(
                    '<a href="{0}{1}2990.html">St. Louis Cardinals 5, Pittsbur'
                    'gh Pirates 4</a>'))
        ], [
            cell(
                content=_game_box_sub(
                    '<a href="{0}{1}2997.html">Tampa Bay Rays 12, Boston Red S'
                    'ox 9</a>'))
        ], [
            cell(
                content=_game_box_sub(
                    '<a href="{0}{1}2994.html">Texas Rangers 5, Oakland Athlet'
                    'ics 3</a>'))
        ], [
            cell(
                content=_game_box_sub(
                    '<a href="{0}{1}2995.html">Toronto Blue Jays 8, Minnesota '
                    'Twins 2</a>'))
        ]]
        expected = table(
            head=[cell(content='Sunday, October 9th, 2022')], body=body)
        self.assertEqual(actual, expected)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()


if __name__ in ['__main__', 'tasks.statsplus.statsplus_test']:
    _main = __name__ == '__main__'
    _pkg = 'tasks.statsplus'
    _pth = 'tasks/statsplus'
    main(StatsplusTest, Statsplus, _pkg, _pth, {}, _main, date=_now, e=_env)
