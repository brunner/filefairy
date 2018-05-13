#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import mock
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(_path)
_root = re.sub(r'/plugins/statsplus', '', _path)
sys.path.append(_root)
from plugins.statsplus.statsplus_plugin import StatsplusPlugin  # noqa
from utils.component.component_util import table  # noqa
from utils.jinja2.jinja2_util import env  # noqa
from utils.json.json_util import dumps  # noqa
from utils.team.team_util import logo_inline  # noqa
from utils.test.test_util import TestUtil  # noqa
from utils.test.test_util import main  # noqa
from value.notify.notify_value import NotifyValue  # noqa
from value.response.response_value import ResponseValue  # noqa

_html = 'https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/'
_game_box = 'box_scores/game_box_'
_player = 'players/player_'
_lhclazz = 'table-fixed border border-bottom-0 mt-3'
_lhcols = [' class="text-center"']
_lbclazz = 'table-fixed border'
_lbpcols = [
    ' class="position-relative w-40"', ' class="text-center w-10"',
    ' class="text-center w-10"', ' class="position-relative text-right w-40"'
]
_lbrcols = [' class="td-sm position-relative text-center w-20"'] * 5

DATA = StatsplusPlugin._data()
NOW_ENCODED = '2022-10-10T00:00:00'
THEN_ENCODED = '2022-10-09T00:00:00'
HOME = {'breadcrumbs': [], 'live': []}
INDEX = 'html/fairylab/statsplus/index.html'
HIGHLIGHTS_TABLE = table(body=[['Player set the record.']])
INJURIES_TABLE = table(body=[['Player was injured.']])
LIVE_HEADER_AL = table(clazz=_lhclazz, hcols=_lhcols, head=['American League'])
LIVE_HEADER_POSTSEASON = table(
    clazz=_lhclazz, hcols=_lhcols, head=['Postseason'])
LIVE_HEADER_NL = table(clazz=_lhclazz, hcols=_lhcols, head=['National League'])
LIVE_POSTSEASON_BODY = [['Baltimore', '1', '0', 'Boston']]
LIVE_POSTSEASON = table(
    clazz=_lbclazz, bcols=_lbpcols, body=LIVE_POSTSEASON_BODY)
LIVE_REGULAR_BODY = [['BAL 1-0', 'BOS 0-1']]
LIVE_REGULAR = table(clazz=_lbclazz, bcols=_lbrcols, body=LIVE_REGULAR_BODY)
SCORES_TABLE_NOW = table(head='2022-10-10', body=[['Baltimore 1, Boston 0']])
SCORES_TABLE_THEN = table(head='2022-10-09', body=[['Baltimore 1, Boston 0']])
NOW = datetime.datetime(2022, 10, 10)
THEN = datetime.datetime(2022, 10, 9)
AL = [('AL East', ['33', '34', '48']), ('AL Central', ['35', '38', '40']),
      ('AL West', ['42', '44', '50'])]
NL = [('NL East', ['32', '41', '49']), ('NL Central', ['36', '37', '46']),
      ('NL West', ['31', '39', '45'])]
SCORES_THEN = '10/09/2022 MAJOR LEAGUE BASEBALL Final Scores\n'
SCORES_NOW = '10/10/2022 MAJOR LEAGUE BASEBALL Final Scores\n'
SCORES_POSTSEASON_ENCODED = [
    '<{0}{1}25051.html|T45 8, T53 3>', '<{0}{1}25043.html|T54 6, T34 3>'
]
SCORES_REGULAR_TEXT = '*<{0}{1}2998.html|Arizona 4, Los Angeles 2>*\n' + \
                '*<{0}{1}3003.html|Atlanta 2, Los Angeles 1>*\n' + \
                '*<{0}{1}2996.html|Cincinnati 7, Milwaukee 2>*\n' + \
                '*<{0}{1}3002.html|Detroit 11, Chicago 4>*\n' + \
                '*<{0}{1}2993.html|Houston 7, Seattle 2>*\n' + \
                '*<{0}{1}2991.html|Kansas City 8, Cleveland 2>*\n' + \
                '*<{0}{1}14721.html|Miami 6, Chicago 2>*\n' + \
                '*<{0}{1}3001.html|New York 1, San Francisco 0>*\n' + \
                '*<{0}{1}3000.html|New York 5, Baltimore 3>*\n' + \
                '*<{0}{1}2992.html|Philadelphia 3, Washington 1>*\n' + \
                '*<{0}{1}2999.html|San Diego 8, Colorado 2>*\n' + \
                '*<{0}{1}2990.html|St. Louis 5, Pittsburgh 4>*\n' + \
                '*<{0}{1}2997.html|Tampa Bay 12, Boston 9>*\n' + \
                '*<{0}{1}2994.html|Texas 5, Oakland 3>*\n' + \
                '*<{0}{1}2995.html|Toronto 8, Minnesota 2>*'
SCORES_REGULAR_ENCODED = [
    '<{0}{1}2998.html|T31 4, TLA 2>', '<{0}{1}3003.html|T32 2, TLA 1>',
    '<{0}{1}2996.html|T37 7, T46 2>', '<{0}{1}3002.html|T40 11, TCH 4>',
    '<{0}{1}2993.html|T42 7, T54 2>', '<{0}{1}2991.html|T43 8, T38 2>',
    '<{0}{1}14721.html|T41 6, TCH 2>', '<{0}{1}3001.html|TNY 1, T55 0>',
    '<{0}{1}3000.html|TNY 5, T33 3>', '<{0}{1}2992.html|T51 3, T60 1>',
    '<{0}{1}2999.html|T53 8, T39 2>', '<{0}{1}2990.html|T56 5, T52 4>',
    '<{0}{1}2997.html|T57 12, T34 9>', '<{0}{1}2994.html|T58 5, T50 3>',
    '<{0}{1}2995.html|T59 8, T47 2>'
]
TABLE_THEN = '```MAJOR LEAGUE BASEBALL Live Table - 10/09/2022\n'
TABLE_TEXT = 'Cincinnati Reds 111\nSan Diego Padres 104\nBoston Red Sox ' + \
             '99\nSeattle Mariners 98\nLos Angeles Dodgers 97\nNew York ' + \
             'Mets 95\nSt. Louis Cardinals 89\nColorado Rockies 88\n' + \
             'Minnesota Twins 88\nNew York Yankees 88\nDetroit Tigers 86\n' + \
             'Houston Astros 85\nMiami Marlins 84\nChicago White Sox 82\n' + \
             'Atlanta Braves 77\nMilwaukee Brewers 77\nCleveland Indians ' + \
             '76\nArizona Diamondbacks 76\nKansas City Royals 76\n' + \
             'Philadelphia Phillies 75\nOakland Athletics 75\nWashington ' + \
             'Nationals 73\nToronto Blue Jays 73\nChicago Cubs 71\n' + \
             'Baltimore Orioles 70\nLos Angeles Angels 70\nTexas Rangers ' + \
             '67\nTampa Bay Rays 65\nSan Francisco Giants 62\nPittsburgh ' + \
             'Pirates 53```'
TABLE_ENCODED = {
    'T45': '97',
    'T49': '95',
    'T48': '88',
    'T35': '82',
    'T36': '71',
    'T44': '70'
}
HOMETOWNS = [
    'Arizona', 'Los Angeles', 'Atlanta', 'Los Angeles', 'Cincinnati',
    'Milwaukee', 'Detroit', 'Chicago', 'Houston', 'Seattle', 'Kansas City',
    'Cleveland', 'Miami', 'Chicago', 'New York', 'San Francisco', 'New York',
    'Baltimore', 'Philadelphia', 'Washington', 'San Diego', 'Colorado',
    'St. Louis', 'Pittsburgh', 'Tampa Bay', 'Boston', 'Texas', 'Oakland',
    'Toronto', 'Minnesota'
]
INJURIES_DATE = '10/09/2022 '
INJURIES_DELAY = '10/09/2022 Rain delay of 19 minutes in the 2nd inning. '
INJURIES_TEXT = 'SP <{0}{1}37102.html|Jairo Labourt> was injured while ' + \
                'pitching (Seattle @ Boston)'
INJURIES_TEXT_ENCODED = 'SP <{0}{1}37102.html|Jairo Labourt> was injured ' + \
                'while pitching (T54 @ T34)'
HIGHLIGHTS_DATE = '10/09/2022 '
HIGHLIGHTS_TEXT = '<{0}{1}38868.html|Connor Harrell> ties the ' + \
                  'BOS regular season game record for runs with 4 (Boston ' + \
                  '@ Tampa Bay)'
HIGHLIGHTS_TEXT_ENCODED = '<{0}{1}38868.html|Connor Harrell> ties the ' + \
                  'BOS regular season game record for runs with 4 (T34 @ T57)'
BREADCRUMBS = [{
    'href': '/fairylab/',
    'name': 'Home'
}, {
    'href': '',
    'name': 'Statsplus'
}]


def game_box(s):
    return s.format(_html, _game_box)


SCORES_TABLE_BODY = [[
    game_box(
        '<a href="{0}{1}2998.html">Arizona Diamondbacks 4, Los Angeles 2</a>')
], [
    game_box('<a href="{0}{1}3003.html">Atlanta Braves 2, Los Angeles 1</a>')
], [
    game_box(
        '<a href="{0}{1}2996.html">Cincinnati Reds 7, Milwaukee Brewers 2</a>')
], [game_box('<a href="{0}{1}3002.html">Detroit Tigers 11, Chicago 4</a>')], [
    game_box(
        '<a href="{0}{1}2993.html">Houston Astros 7, Seattle Mariners 2</a>')
], [
    game_box(
        '<a href="{0}{1}2991.html">Kansas City Royals 8, Cleveland Indians 2</a>'
    )
], [game_box('<a href="{0}{1}14721.html">Miami Marlins 6, Chicago 2</a>')], [
    game_box(
        '<a href="{0}{1}3001.html">New York 1, San Francisco Giants 0</a>')
], [
    game_box('<a href="{0}{1}3000.html">New York 5, Baltimore Orioles 3</a>')
], [
    game_box(
        '<a href="{0}{1}2992.html">Philadelphia Phillies 3, Washington Nationals 1</a>'
    )
], [
    game_box(
        '<a href="{0}{1}2999.html">San Diego Padres 8, Colorado Rockies 2</a>')
], [
    game_box(
        '<a href="{0}{1}2990.html">St. Louis Cardinals 5, Pittsburgh Pirates 4</a>'
    )
], [
    game_box(
        '<a href="{0}{1}2997.html">Tampa Bay Rays 12, Boston Red Sox 9</a>')
], [
    game_box(
        '<a href="{0}{1}2994.html">Texas Rangers 5, Oakland Athletics 3</a>')
], [
    game_box(
        '<a href="{0}{1}2995.html">Toronto Blue Jays 8, Minnesota Twins 2</a>')
]]
SCORES_PATTERN = '<[^|]+\|[^<]+>'
INJURIES_PATTERN = '\w+ <[^|]+\|[^<]+> was injured [^)]+\)'
HIGHLIGHTS_PATTERN = '<[^|]+\|[^<]+> (?:sets|ties) [^)]+\)'


def player(s):
    return s.format(_html, _player)


INJURIES_TABLE_BODY = [[
    player('SP <a href="{0}{1}37102.html">Jairo Labourt</a> was injured while '
           'pitching (Seattle Mariners @ Boston Red Sox)')
]]
HIGHLIGHTS_TABLE_BODY = [[
    player('<a href="{0}{1}38868.html">Connor Harrell</a> ties the BOS '
           'regular season game record for runs with 4 (Boston Red Sox @ '
           'Tampa Bay Rays)')
]]


def _data(finished=False,
          highlights={},
          injuries={},
          offseason=False,
          postseason=False,
          scores={},
          table={},
          unresolved=[],
          updated=False):
    return {
        'finished': finished,
        'highlights': highlights,
        'injuries': injuries,
        'offseason': offseason,
        'postseason': postseason,
        'scores': scores,
        'table': table,
        'unresolved': unresolved,
        'updated': updated
    }


DATA_CANONICAL = _data()


class StatsplusPluginTest(TestUtil):
    def setUp(self):
        patch_open = mock.patch(
            'apis.serializable.serializable_api.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]

    def reset_mocks(self):
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()

    def create_plugin(self, data):
        self.init_mocks(data)
        plugin = StatsplusPlugin(e=env())
        plugin.shadow['download.now'] = THEN_ENCODED

        self.mock_open.assert_called_once_with(DATA, 'r')
        self.mock_handle.write.assert_not_called()

        self.reset_mocks()
        self.init_mocks(data)

        return plugin

    def test_notify__with_finish(self):
        read = DATA_CANONICAL
        plugin = self.create_plugin(read)
        value = plugin._notify_internal(notify=NotifyValue.DOWNLOAD_FINISH)
        self.assertFalse(value)

        write = _data(finished=True)
        self.mock_open.assert_called_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    def test_notify__with_year(self):
        read = DATA_CANONICAL
        plugin = self.create_plugin(read)
        value = plugin._notify_internal(notify=NotifyValue.DOWNLOAD_YEAR)
        self.assertFalse(value)

        write = _data(offseason=True)
        self.mock_open.assert_called_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    def test_notify__with_other(self):
        read = DATA_CANONICAL
        plugin = self.create_plugin(read)
        value = plugin._notify_internal(notify=NotifyValue.OTHER)
        self.assertFalse(value)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(StatsplusPlugin, '_handle_table')
    @mock.patch.object(StatsplusPlugin, '_handle_key')
    @mock.patch.object(StatsplusPlugin, '_clear')
    def test_on_message__with_finished(self, mock_clear, mock_handle,
                                       mock_table):
        scores = SCORES_REGULAR_TEXT.format(_html, _game_box)
        obj = {
            'channel': 'C7JSGHW8G',
            'text': SCORES_THEN + scores,
            'ts': '1000.789',
            'user': 'U1234',
            'bot_id': 'B7KJ3362Y'
        }
        read = _data(finished=True)
        plugin = self.create_plugin(read)
        response = plugin._on_message_internal(obj=obj)
        self.assertEqual(response, ResponseValue(notify=[NotifyValue.BASE]))

        write = DATA_CANONICAL
        mock_clear.assert_called_once_with()
        mock_handle.assert_called_once_with('scores', THEN_ENCODED,
                                            SCORES_THEN + scores,
                                            SCORES_PATTERN, False)
        mock_table.assert_not_called()
        self.mock_open.assert_called_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch.object(StatsplusPlugin, '_handle_table')
    @mock.patch.object(StatsplusPlugin, '_handle_key')
    @mock.patch.object(StatsplusPlugin, '_clear')
    def test_on_message__with_scores(self, mock_clear, mock_handle,
                                     mock_table):
        scores = SCORES_REGULAR_TEXT.format(_html, _game_box)
        obj = {
            'channel': 'C7JSGHW8G',
            'text': SCORES_THEN + scores,
            'ts': '1000.789',
            'user': 'U1234',
            'bot_id': 'B7KJ3362Y'
        }
        read = DATA_CANONICAL
        plugin = self.create_plugin(read)
        response = plugin._on_message_internal(obj=obj)
        self.assertEqual(response, ResponseValue(notify=[NotifyValue.BASE]))

        mock_clear.assert_not_called()
        mock_handle.assert_called_once_with('scores', THEN_ENCODED,
                                            SCORES_THEN + scores,
                                            SCORES_PATTERN, False)
        mock_table.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(StatsplusPlugin, '_handle_table')
    @mock.patch.object(StatsplusPlugin, '_handle_key')
    @mock.patch.object(StatsplusPlugin, '_clear')
    def test_on_message__with_scores_and_postseason(self, mock_clear,
                                                    mock_handle, mock_table):
        scores = SCORES_REGULAR_TEXT.format(_html, _game_box)
        obj = {
            'channel': 'C7JSGHW8G',
            'text': SCORES_THEN + scores,
            'ts': '1000.789',
            'user': 'U1234',
            'bot_id': 'B7KJ3362Y'
        }
        read = _data(offseason=True, postseason=True)
        plugin = self.create_plugin(read)
        response = plugin._on_message_internal(obj=obj)
        self.assertEqual(response, ResponseValue(notify=[NotifyValue.BASE]))

        write = _data(offseason=True)
        mock_clear.assert_not_called()
        mock_handle.assert_called_once_with('scores', THEN_ENCODED,
                                            SCORES_THEN + scores,
                                            SCORES_PATTERN, False)
        mock_table.assert_not_called()
        self.mock_open.assert_called_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch.object(StatsplusPlugin, '_handle_table')
    @mock.patch.object(StatsplusPlugin, '_handle_key')
    @mock.patch.object(StatsplusPlugin, '_clear')
    def test_on_message__with_table_and_postseason(self, mock_clear,
                                                   mock_handle, mock_table):
        obj = {
            'channel': 'C7JSGHW8G',
            'text': TABLE_THEN + TABLE_TEXT,
            'ts': '1000.789',
            'user': 'U1234',
            'bot_id': 'B7KJ3362Y'
        }
        read = _data(offseason=True)
        plugin = self.create_plugin(read)
        response = plugin._on_message_internal(obj=obj)
        self.assertEqual(response, ResponseValue(notify=[NotifyValue.BASE]))

        write = DATA_CANONICAL
        mock_clear.assert_not_called()
        mock_handle.assert_not_called()
        mock_table.assert_called_once_with(THEN_ENCODED,
                                           TABLE_THEN + TABLE_TEXT)
        self.mock_open.assert_called_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch.object(StatsplusPlugin, '_handle_table')
    @mock.patch.object(StatsplusPlugin, '_handle_key')
    @mock.patch.object(StatsplusPlugin, '_clear')
    def test_on_message__with_delay(self, mock_clear, mock_handle, mock_table):
        injuries = INJURIES_TEXT.format(_html, _player)
        obj = {
            'channel': 'C7JSGHW8G',
            'text': INJURIES_DELAY + injuries,
            'ts': '1000.789',
            'user': 'U1234',
            'bot_id': 'B7KJ3362Y'
        }
        read = DATA_CANONICAL
        plugin = self.create_plugin(read)
        response = plugin._on_message_internal(obj=obj)
        self.assertEqual(response, ResponseValue(notify=[NotifyValue.BASE]))

        mock_clear.assert_not_called()
        mock_handle.assert_called_once_with('injuries', THEN_ENCODED,
                                            INJURIES_DELAY + injuries,
                                            INJURIES_PATTERN, True)
        mock_table.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(StatsplusPlugin, '_handle_table')
    @mock.patch.object(StatsplusPlugin, '_handle_key')
    @mock.patch.object(StatsplusPlugin, '_clear')
    def test_on_message__with_injuries(self, mock_clear, mock_handle,
                                       mock_table):
        injuries = INJURIES_TEXT.format(_html, _player)
        obj = {
            'channel': 'C7JSGHW8G',
            'text': INJURIES_DATE + injuries,
            'ts': '1000.789',
            'user': 'U1234',
            'bot_id': 'B7KJ3362Y'
        }
        read = DATA_CANONICAL
        plugin = self.create_plugin(read)
        response = plugin._on_message_internal(obj=obj)
        self.assertEqual(response, ResponseValue(notify=[NotifyValue.BASE]))

        mock_clear.assert_not_called()
        mock_handle.assert_called_once_with('injuries', THEN_ENCODED,
                                            INJURIES_DATE + injuries,
                                            INJURIES_PATTERN, True)
        mock_table.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(StatsplusPlugin, '_handle_table')
    @mock.patch.object(StatsplusPlugin, '_handle_key')
    @mock.patch.object(StatsplusPlugin, '_clear')
    def test_on_message__with_highlights(self, mock_clear, mock_handle,
                                         mock_table):
        highlights = HIGHLIGHTS_TEXT.format(_html, _player)
        obj = {
            'channel': 'C7JSGHW8G',
            'text': HIGHLIGHTS_DATE + highlights,
            'ts': '1000.789',
            'user': 'U1234',
            'bot_id': 'B7KJ3362Y'
        }
        read = DATA_CANONICAL
        plugin = self.create_plugin(read)
        response = plugin._on_message_internal(obj=obj)
        self.assertEqual(response, ResponseValue(notify=[NotifyValue.BASE]))

        mock_clear.assert_not_called()
        mock_handle.assert_called_once_with('highlights', THEN_ENCODED,
                                            HIGHLIGHTS_DATE + highlights,
                                            HIGHLIGHTS_PATTERN, True)
        mock_table.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(StatsplusPlugin, '_handle_table')
    @mock.patch.object(StatsplusPlugin, '_handle_key')
    @mock.patch.object(StatsplusPlugin, '_clear')
    def test_on_message__with_invalid_bot_id(self, mock_clear, mock_handle,
                                             mock_table):
        scores = SCORES_REGULAR_TEXT.format(_html, _game_box)
        obj = {
            'channel': 'G3SUFLMK4',
            'text': SCORES_THEN + scores,
            'ts': '1000.789',
            'user': 'U1234',
        }
        read = DATA_CANONICAL
        plugin = self.create_plugin(read)
        response = plugin._on_message_internal(obj=obj)
        self.assertEqual(response, ResponseValue())

        mock_clear.assert_not_called()
        mock_handle.assert_not_called()
        mock_table.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(StatsplusPlugin, '_handle_table')
    @mock.patch.object(StatsplusPlugin, '_handle_key')
    @mock.patch.object(StatsplusPlugin, '_clear')
    def test_on_message__with_invalid_date(self, mock_clear, mock_handle,
                                           mock_table):
        scores = SCORES_REGULAR_TEXT.format(_html, _game_box)
        obj = {
            'channel': 'C7JSGHW8G',
            'text': SCORES_NOW + scores,
            'ts': '1000.789',
            'user': 'U1234',
            'bot_id': 'B7KJ3362Y'
        }
        read = DATA_CANONICAL
        plugin = self.create_plugin(read)
        response = plugin._on_message_internal(obj=obj)
        self.assertEqual(response, ResponseValue())

        mock_clear.assert_not_called()
        mock_handle.assert_not_called()
        mock_table.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(StatsplusPlugin, '_handle_table')
    @mock.patch.object(StatsplusPlugin, '_handle_key')
    @mock.patch.object(StatsplusPlugin, '_clear')
    def test_on_message__with_invalid_channel(self, mock_clear, mock_handle,
                                              mock_table):
        scores = SCORES_REGULAR_TEXT.format(_html, _game_box)
        obj = {
            'channel': 'G3SUFLMK4',
            'text': SCORES_THEN + scores,
            'ts': '1000.789',
            'user': 'U1234',
            'bot_id': 'B7KJ3362Y'
        }
        read = DATA_CANONICAL
        plugin = self.create_plugin(read)
        response = plugin._on_message_internal(obj=obj)
        self.assertEqual(response, ResponseValue())

        mock_clear.assert_not_called()
        mock_handle.assert_not_called()
        mock_table.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(StatsplusPlugin, '_resolve_all')
    @mock.patch.object(StatsplusPlugin, '_render')
    def test_run__with_resolved(self, mock_render, mock_resolve):
        read = DATA_CANONICAL
        plugin = self.create_plugin(read)
        response = plugin._run_internal(date=NOW)
        self.assertEqual(response, ResponseValue())

        mock_render.assert_not_called()
        mock_resolve.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(StatsplusPlugin, '_resolve_all')
    @mock.patch.object(StatsplusPlugin, '_render')
    def test_run__with_unresolved(self, mock_render, mock_resolve):
        read = _data(unresolved=[THEN_ENCODED])
        plugin = self.create_plugin(read)

        def fake_resolve_all(*args, **kwargs):
            for date in args[0]:
                plugin.data['unresolved'].remove(date)

        mock_resolve.side_effect = fake_resolve_all

        response = plugin._run_internal(date=NOW)
        self.assertEqual(response, ResponseValue())

        mock_render.assert_not_called()
        mock_resolve.assert_called_once_with([THEN_ENCODED])
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(StatsplusPlugin, '_resolve_all')
    @mock.patch.object(StatsplusPlugin, '_render')
    def test_run__with_updated(self, mock_render, mock_resolve):
        read = _data(updated=True)
        plugin = self.create_plugin(read)

        response = plugin._run_internal(date=NOW)
        self.assertEqual(response, ResponseValue(notify=[NotifyValue.BASE]))

        write = DATA_CANONICAL
        mock_render.assert_called_once_with(date=NOW)
        mock_resolve.assert_not_called()
        self.mock_open.assert_called_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch.object(StatsplusPlugin, '_home')
    def test_render(self, mock_home):
        mock_home.return_value = HOME

        read = DATA_CANONICAL
        plugin = self.create_plugin(read)
        value = plugin._render_internal(date=NOW)
        self.assertEqual(value, [(INDEX, '', 'statsplus.html', HOME)])

        mock_home.assert_called_once_with(date=NOW)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(StatsplusPlugin, '_render')
    def test_setup(self, mock_render):
        read = DATA_CANONICAL
        plugin = self.create_plugin(read)
        plugin._setup_internal(date=NOW)

        mock_render.assert_called_once_with(date=NOW)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    def test_shadow(self):
        read = DATA_CANONICAL
        plugin = self.create_plugin(read)
        value = plugin._shadow_internal()
        self.assertEqual(value, {})

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    def test_clear(self):
        read = _data(
            highlights={THEN_ENCODED: [HIGHLIGHTS_TEXT_ENCODED]},
            injuries={THEN_ENCODED: [INJURIES_TEXT_ENCODED]},
            scores={
                THEN_ENCODED: SCORES_REGULAR_ENCODED
            })
        plugin = self.create_plugin(read)
        plugin._clear()

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.assertEqual(plugin.data['highlights'], {})
        self.assertEqual(plugin.data['injuries'], {})
        self.assertEqual(plugin.data['scores'], {})

    def test_handle_key__delay(self):
        read = DATA_CANONICAL
        plugin = self.create_plugin(read)
        text = INJURIES_DELAY + INJURIES_TEXT.format(_html, _player)
        plugin._handle_key('injuries', THEN_ENCODED, text, INJURIES_PATTERN,
                           True)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.assertEqual(plugin.data['injuries'], {
            THEN_ENCODED: [INJURIES_TEXT_ENCODED]
        })
        self.assertFalse(plugin.data['unresolved'])

    def test_handle_key__highlights(self):
        read = DATA_CANONICAL
        plugin = self.create_plugin(read)
        text = HIGHLIGHTS_DATE + HIGHLIGHTS_TEXT.format(_html, _player)
        plugin._handle_key('highlights', THEN_ENCODED, text,
                           HIGHLIGHTS_PATTERN, True)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.assertEqual(plugin.data['highlights'], {
            THEN_ENCODED: [HIGHLIGHTS_TEXT_ENCODED]
        })
        self.assertFalse(plugin.data['unresolved'])

    def test_handle_key__injuries(self):
        read = DATA_CANONICAL
        plugin = self.create_plugin(read)
        text = INJURIES_DATE + INJURIES_TEXT.format(_html, _player)
        plugin._handle_key('injuries', THEN_ENCODED, text, INJURIES_PATTERN,
                           True)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.assertEqual(plugin.data['injuries'], {
            THEN_ENCODED: [INJURIES_TEXT_ENCODED]
        })
        self.assertFalse(plugin.data['unresolved'])

    def test_handle_key__scores(self):
        read = DATA_CANONICAL
        plugin = self.create_plugin(read)
        text = SCORES_THEN + SCORES_REGULAR_TEXT.format(_html, _game_box)
        plugin._handle_key('scores', THEN_ENCODED, text, SCORES_PATTERN, False)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.assertEqual(plugin.data['scores'], {
            THEN_ENCODED: SCORES_REGULAR_ENCODED
        })
        self.assertTrue(plugin.data['unresolved'])

    def test_handle_table(self):
        read = DATA_CANONICAL
        plugin = self.create_plugin(read)
        text = TABLE_THEN + TABLE_TEXT
        plugin._handle_table(THEN_ENCODED, text)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.assertEqual(plugin.data['table'], {THEN_ENCODED: TABLE_ENCODED})
        self.assertFalse(plugin.data['unresolved'])

    @mock.patch.object(StatsplusPlugin, '_table')
    @mock.patch.object(StatsplusPlugin, '_live_postseason')
    def test_home__with_postseason(self, mock_live, mock_table):
        mock_live.return_value = [LIVE_POSTSEASON]
        mock_table.side_effect = [
            HIGHLIGHTS_TABLE,
            INJURIES_TABLE,
            SCORES_TABLE_NOW,
            SCORES_TABLE_THEN,
        ]

        read = _data(
            highlights={THEN_ENCODED: [HIGHLIGHTS_TEXT_ENCODED]},
            injuries={THEN_ENCODED: [INJURIES_TEXT_ENCODED]},
            postseason=True,
            scores={
                THEN_ENCODED: SCORES_REGULAR_ENCODED,
                NOW_ENCODED: SCORES_REGULAR_ENCODED
            })
        plugin = self.create_plugin(read)
        actual = plugin._home(date=NOW)
        expected = {
            'breadcrumbs': BREADCRUMBS,
            'live': [LIVE_POSTSEASON],
            'highlights': [HIGHLIGHTS_TABLE],
            'injuries': [INJURIES_TABLE],
            'scores': [SCORES_TABLE_NOW, SCORES_TABLE_THEN],
        }
        self.assertEqual(actual, expected)

        mock_live.assert_called_once_with()
        calls = [
            mock.call('highlights', THEN_ENCODED, _player),
            mock.call('injuries', THEN_ENCODED, _player),
            mock.call('scores', NOW_ENCODED, _game_box),
            mock.call('scores', THEN_ENCODED, _game_box),
        ]
        mock_table.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(StatsplusPlugin, '_table')
    @mock.patch.object(StatsplusPlugin, '_live_regular')
    def test_home__with_regular(self, mock_live, mock_table):
        mock_live.return_value = [LIVE_REGULAR]
        mock_table.side_effect = [
            HIGHLIGHTS_TABLE,
            INJURIES_TABLE,
            SCORES_TABLE_NOW,
            SCORES_TABLE_THEN,
        ]

        read = _data(
            highlights={THEN_ENCODED: [HIGHLIGHTS_TEXT_ENCODED]},
            injuries={THEN_ENCODED: [INJURIES_TEXT_ENCODED]},
            scores={
                THEN_ENCODED: SCORES_REGULAR_ENCODED,
                NOW_ENCODED: SCORES_REGULAR_ENCODED
            })
        plugin = self.create_plugin(read)
        actual = plugin._home(date=NOW)
        expected = {
            'breadcrumbs': BREADCRUMBS,
            'live': [LIVE_REGULAR],
            'highlights': [HIGHLIGHTS_TABLE],
            'injuries': [INJURIES_TABLE],
            'scores': [SCORES_TABLE_NOW, SCORES_TABLE_THEN],
        }
        self.assertEqual(actual, expected)

        mock_live.assert_called_once_with()
        calls = [
            mock.call('highlights', THEN_ENCODED, _player),
            mock.call('injuries', THEN_ENCODED, _player),
            mock.call('scores', NOW_ENCODED, _game_box),
            mock.call('scores', THEN_ENCODED, _game_box),
        ]
        mock_table.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(StatsplusPlugin, '_live_postseason_body')
    def test_live_postseason(self, mock_body):
        mock_body.return_value = LIVE_POSTSEASON_BODY

        read = _data(
            postseason=True, scores={
                THEN_ENCODED: SCORES_POSTSEASON_ENCODED
            })
        plugin = self.create_plugin(read)
        actual = plugin._live_postseason()
        expected = [LIVE_HEADER_POSTSEASON, LIVE_POSTSEASON]
        self.assertEqual(actual, expected)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(StatsplusPlugin, '_live_postseason_series')
    @mock.patch.object(StatsplusPlugin, '_record')
    @mock.patch('plugins.statsplus.statsplus_plugin.logo_absolute')
    def test_live_postseason_body(self, mock_logo, mock_record, mock_series):
        mock_logo.return_value = 'logo'
        mock_record.side_effect = ['1-0', '0-1', '0-1', '1-0']
        mock_series.return_value = [['T45', 'T53'], ['T34', 'T54']]

        read = DATA_CANONICAL
        plugin = self.create_plugin(read)
        actual = plugin._live_postseason_body()
        expected = [['logo', '1', '0', 'logo'], ['logo', '1', '0', 'logo']]
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

    def test_live_postseason_series(self):
        read = _data(
            postseason=True, scores={
                THEN_ENCODED: SCORES_POSTSEASON_ENCODED
            })
        plugin = self.create_plugin(read)
        actual = plugin._live_postseason_series()
        expected = [['T45', 'T53'], ['T34', 'T54']]
        self.assertEqual(actual, expected)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(StatsplusPlugin, '_live_regular_body')
    @mock.patch('plugins.statsplus.statsplus_plugin.divisions')
    def test_live_regular(self, mock_divisions, mock_body):
        mock_divisions.return_value = AL + NL
        mock_body.return_value = LIVE_REGULAR_BODY

        read = DATA_CANONICAL
        plugin = self.create_plugin(read)
        actual = plugin._live_regular()
        expected = [LIVE_HEADER_AL, LIVE_REGULAR, LIVE_HEADER_NL, LIVE_REGULAR]
        self.assertEqual(actual, expected)

        mock_divisions.assert_called_once_with()
        mock_body.assert_has_calls([mock.call(AL), mock.call(NL)])
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(StatsplusPlugin, '_record')
    @mock.patch('plugins.statsplus.statsplus_plugin.logo_inline')
    def test_live_regular_body(self, mock_logo, mock_record):
        mock_logo.return_value = 'logo'
        mock_record.side_effect = ['2-0', '0-2', '1-1'] * 3

        read = DATA_CANONICAL
        plugin = self.create_plugin(read)
        actual = plugin._live_regular_body(AL)
        expected = [['logo'] * 3, ['logo'] * 3, ['logo'] * 3]
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

    def test_record(self):
        read = _data(scores={THEN_ENCODED: SCORES_REGULAR_ENCODED})
        plugin = self.create_plugin(read)
        self.assertEqual(plugin._record('33'), '0-1')
        self.assertEqual(plugin._record('35'), '0-0')
        self.assertEqual(plugin._record('42'), '1-0')

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch('plugins.statsplus.statsplus_plugin.clarify')
    def test_resolve_all(self, mock_clarify):
        mock_clarify.side_effect = [{
            'encoding': 'T31 4 T45 2',
            'away': 'T31',
            'home': 'T45'
        }, {
            'encoding': 'T32 2 T44 1',
            'away': 'T44',
            'home': 'T32'
        }, {
            'encoding': 'T40 11 T35 4',
            'away': 'T40',
            'home': 'T35'
        }, {
            'encoding': 'T41 6 T36 2',
            'away': 'T36',
            'home': 'T41'
        }, {
            'encoding': 'T49 1 T55 0',
            'away': 'T49',
            'home': 'T55'
        }, {
            'encoding': 'T48 5 T33 3',
            'away': 'T48',
            'home': 'T33'
        }]
        read = _data(
            scores={THEN_ENCODED: SCORES_REGULAR_ENCODED},
            unresolved=[THEN_ENCODED])
        plugin = self.create_plugin(read)
        plugin._resolve_all([THEN_ENCODED])

        calls = [
            mock.call(THEN_ENCODED, '{0}{1}2998.html'.format(_html, _game_box),
                      'T31 4, TLA 2'),
            mock.call(THEN_ENCODED, '{0}{1}3003.html'.format(_html, _game_box),
                      'T32 2, TLA 1'),
            mock.call(THEN_ENCODED, '{0}{1}3002.html'.format(_html, _game_box),
                      'T40 11, TCH 4'),
            mock.call(THEN_ENCODED, '{0}{1}14721.html'.format(
                _html, _game_box), 'T41 6, TCH 2'),
            mock.call(THEN_ENCODED, '{0}{1}3001.html'.format(_html, _game_box),
                      'TNY 1, T55 0'),
            mock.call(THEN_ENCODED, '{0}{1}3000.html'.format(_html, _game_box),
                      'TNY 5, T33 3')
        ]
        mock_clarify.assert_has_calls(calls)
        self.assertFalse(plugin.data['unresolved'])
        self.assertTrue(plugin.data['updated'])

    def test_table__highlights(self):
        read = _data(highlights={THEN_ENCODED: [HIGHLIGHTS_TEXT_ENCODED]})
        plugin = self.create_plugin(read)

        actual = plugin._table('highlights', THEN_ENCODED, _player)
        expected = table(
            hcols=[''],
            bcols=[''],
            head=['Sunday, October 9th, 2022'],
            body=HIGHLIGHTS_TABLE_BODY)
        self.assertEqual(actual, expected)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    def test_table__injuries(self):
        read = _data(injuries={THEN_ENCODED: [INJURIES_TEXT_ENCODED]})
        plugin = self.create_plugin(read)

        actual = plugin._table('injuries', THEN_ENCODED, _player)
        expected = table(
            hcols=[''],
            bcols=[''],
            head=['Sunday, October 9th, 2022'],
            body=INJURIES_TABLE_BODY)
        self.assertEqual(actual, expected)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    def test_table__scores(self):
        read = _data(scores={THEN_ENCODED: SCORES_REGULAR_ENCODED})
        plugin = self.create_plugin(read)

        actual = plugin._table('scores', THEN_ENCODED, _game_box)
        expected = table(
            hcols=[''],
            bcols=[''],
            head=['Sunday, October 9th, 2022'],
            body=SCORES_TABLE_BODY)
        self.assertEqual(actual, expected)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()


if __name__ in ['__main__', 'plugins.statsplus.statsplus_plugin_test']:
    _main = __name__ == '__main__'
    _pkg = 'plugins.statsplus'
    _pth = 'plugins/statsplus'
    main(StatsplusPluginTest, StatsplusPlugin, _pkg, _pth, {}, _main)
