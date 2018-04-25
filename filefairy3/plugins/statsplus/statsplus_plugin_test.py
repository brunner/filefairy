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
from enums.activity.activity_enum import ActivityEnum  # noqa
from plugins.statsplus.statsplus_plugin import StatsplusPlugin  # noqa
from utils.component.component_util import table  # noqa
from utils.jinja2.jinja2_util import env  # noqa
from utils.json.json_util import dumps  # noqa
from utils.team.team_util import logo_inline  # noqa
from utils.test.test_util import TestUtil  # noqa
from utils.test.test_util import main  # noqa

_html = 'https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/'
_game_box = 'box_scores/game_box_'
_player = 'players/player_'

DATA = StatsplusPlugin._data()
NOW_ENCODED = '2022-10-10T00:00:00'
THEN_ENCODED = '2022-10-09T00:00:00'
HOME = {'breadcrumbs': [], 'live': []}
INDEX = 'html/fairylab/statsplus/index.html'
HIGHLIGHTS_TABLE_SEASON = table(body=[['Player set the record.']])
INJURIES_TABLE_SEASON = table(body=[['Player was injured.']])
LIVE_TABLE_HEADER = table(head=['American League'])
LIVE_TABLE_SEASON = table(body=[['BAL 1-0', 'BOS 0-1']])
SCORES_TABLE_NOW = table(head='2022-10-10', body=[['Baltimore 1, Boston 0']])
SCORES_TABLE_THEN = table(head='2022-10-09', body=[['Baltimore 1, Boston 0']])
NOW = datetime.datetime(2022, 10, 10)
THEN = datetime.datetime(2022, 10, 9)
AL = [('AL East', ['33', '34', '48']), ('AL Central', ['35', '38', '40']),
      ('AL West', ['42', '44', '50'])]
NL = [('NL East', ['32', '41', '49']), ('NL Central', ['36', '37', '46']),
      ('NL West', ['31', '39', '45'])]
FINAL_SCORES_THEN = '10/09/2022 MAJOR LEAGUE BASEBALL Final Scores\n'
FINAL_SCORES_NOW = '10/10/2022 MAJOR LEAGUE BASEBALL Final Scores\n'
SEASON_SCORES = '<{0}{1}2998.html|Arizona 4, Los Angeles 2>\n' + \
                '<{0}{1}3003.html|Atlanta 2, Los Angeles 1>\n' + \
                '<{0}{1}2996.html|Cincinnati 7, Milwaukee 2>\n' + \
                '<{0}{1}3002.html|Detroit 11, Chicago 4>\n' + \
                '<{0}{1}2993.html|Houston 7, Seattle 2>\n' + \
                '<{0}{1}2991.html|Kansas City 8, Cleveland 2>\n' + \
                '<{0}{1}14721.html|Miami 6, Chicago 2>\n' + \
                '<{0}{1}3001.html|New York 1, San Francisco 0>\n' + \
                '<{0}{1}3000.html|New York 5, Baltimore 3>\n' + \
                '<{0}{1}2992.html|Philadelphia 3, Washington 1>\n' + \
                '<{0}{1}2999.html|San Diego 8, Colorado 2>\n' + \
                '<{0}{1}2990.html|St. Louis 5, Pittsburgh 4>\n' + \
                '<{0}{1}2997.html|Tampa Bay 12, Boston 9>\n' + \
                '<{0}{1}2994.html|Texas 5, Oakland 3>\n' + \
                '<{0}{1}2995.html|Toronto 8, Minnesota 2>'
SEASON_SCORES_ENCODED = '<{0}{1}2998.html|T31 4, TLA 2>\n' + \
                        '<{0}{1}3003.html|T32 2, TLA 1>\n' + \
                        '<{0}{1}2996.html|T37 7, T46 2>\n' + \
                        '<{0}{1}3002.html|T40 11, TCH 4>\n' + \
                        '<{0}{1}2993.html|T42 7, T54 2>\n' + \
                        '<{0}{1}2991.html|T43 8, T38 2>\n' + \
                        '<{0}{1}14721.html|T41 6, TCH 2>\n' + \
                        '<{0}{1}3001.html|TNY 1, T55 0>\n' + \
                        '<{0}{1}3000.html|TNY 5, T33 3>\n' + \
                        '<{0}{1}2992.html|T51 3, T60 1>\n' + \
                        '<{0}{1}2999.html|T53 8, T39 2>\n' + \
                        '<{0}{1}2990.html|T56 5, T52 4>\n' + \
                        '<{0}{1}2997.html|T57 12, T34 9>\n' + \
                        '<{0}{1}2994.html|T58 5, T50 3>\n' + \
                        '<{0}{1}2995.html|T59 8, T47 2>'
HOMETOWNS = [
    'Arizona', 'Los Angeles', 'Atlanta', 'Los Angeles', 'Cincinnati',
    'Milwaukee', 'Detroit', 'Chicago', 'Houston', 'Seattle', 'Kansas City',
    'Cleveland', 'Miami', 'Chicago', 'New York', 'San Francisco', 'New York',
    'Baltimore', 'Philadelphia', 'Washington', 'San Diego', 'Colorado',
    'St. Louis', 'Pittsburgh', 'Tampa Bay', 'Boston', 'Texas', 'Oakland',
    'Toronto', 'Minnesota'
]
SEASON_SCORES_TEXT = SEASON_SCORES.replace('<', '*<').replace('>', '>*')
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


def player(s):
    return s.format(_html, _player)


INJURIES_TABLE_BODY = [[
    player('SP <a href="{0}{1}37102.html">Jairo Labourt</a> was injured while '
           'pitching (Seattle Mariners @ Boston Red Sox)')
]]
HIGHLIGHTS_TABLE_BODY = [[
    player('<a href="{0}{1}38868.html">Connor Harrell</a> ties the BOS '
           'regular season game record for runs with 4 (Boston Red Sox @ ' + \
           'Tampa Bay Rays)')
]]


class StatsplusPluginTest(TestUtil):
    def setUp(self):
        patch_open = mock.patch(
            'apis.serializable.serializable_api.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

        patch_clarify = mock.patch(
            'plugins.statsplus.statsplus_plugin.clarify')
        self.addCleanup(patch_clarify.stop)
        self.mock_clarify = patch_clarify.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]

        def fake_clarify(*args, **kwargs):
            return args[2]

        self.mock_clarify.side_effect = fake_clarify

    def reset_mocks(self):
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()
        self.mock_clarify.reset_mock()

    def create_plugin(self, data):
        self.init_mocks(data)
        plugin = StatsplusPlugin(e=env())

        self.mock_open.assert_called_once_with(DATA, 'r')
        self.mock_handle.write.assert_not_called()
        self.mock_clarify.assert_not_called()

        self.reset_mocks()
        self.init_mocks(data)

        return plugin

    def test_notify__with_download(self):
        read = {
            'finished': False,
            'highlights': {},
            'injuries': {},
            'scores': {},
            'status': 'season',
            'updated': False
        }
        plugin = self.create_plugin(read)
        ret = plugin._notify_internal(activity=ActivityEnum.DOWNLOAD)
        self.assertFalse(ret)

        write = {
            'finished': True,
            'highlights': {},
            'injuries': {},
            'scores': {},
            'status': 'season',
            'updated': False
        }
        self.mock_open.assert_called_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_clarify.assert_not_called()

    def test_notify__with_none(self):
        read = {
            'finished': False,
            'highlights': {},
            'injuries': {},
            'scores': {},
            'status': 'season',
            'updated': False
        }
        plugin = self.create_plugin(read)
        ret = plugin._notify_internal(activity=ActivityEnum.NONE)
        self.assertFalse(ret)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_clarify.assert_not_called()

    @mock.patch.object(StatsplusPlugin, '_clear')
    def test_on_message__with_finished_true(self, mock_clear):
        obj = {
            'channel': 'C7JSGHW8G',
            'text': 'text',
            'ts': '1000.789',
            'user': 'U1234',
            'bot_id': 'B7KJ3362Y'
        }
        read = {
            'finished': True,
            'highlights': {},
            'injuries': {},
            'scores': {},
            'status': 'season',
            'updated': False
        }
        plugin = self.create_plugin(read)
        ret = plugin._on_message_internal(obj=obj)
        self.assertEqual(ret, ActivityEnum.BASE)

        write = {
            'finished': False,
            'highlights': {},
            'injuries': {},
            'scores': {},
            'status': 'season',
            'updated': False
        }
        mock_clear.assert_called_once_with()
        self.mock_open.assert_called_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_clarify.assert_not_called()

    @mock.patch.object(StatsplusPlugin, '_clear')
    def test_on_message__with_finished_false(self, mock_clear):
        obj = {
            'channel': 'C7JSGHW8G',
            'text': 'text',
            'ts': '1000.789',
            'user': 'U1234',
            'bot_id': 'B7KJ3362Y'
        }
        read = {
            'finished': False,
            'highlights': {},
            'injuries': {},
            'scores': {},
            'status': 'season',
            'updated': False
        }
        plugin = self.create_plugin(read)
        ret = plugin._on_message_internal(obj=obj)
        self.assertEqual(ret, ActivityEnum.BASE)

        mock_clear.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_clarify.assert_not_called()

    @mock.patch.object(StatsplusPlugin, '_final_scores')
    def test_on_message__with_final_scores(self, mock_final_scores):
        scores = SEASON_SCORES_TEXT.format(_html, _game_box)
        obj = {
            'channel': 'C7JSGHW8G',
            'text': FINAL_SCORES_THEN + scores,
            'ts': '1000.789',
            'user': 'U1234',
            'bot_id': 'B7KJ3362Y'
        }
        read = {
            'finished': False,
            'highlights': {},
            'injuries': {},
            'scores': {},
            'status': 'season',
            'updated': False
        }
        plugin = self.create_plugin(read)
        ret = plugin._on_message_internal(obj=obj)
        self.assertEqual(ret, ActivityEnum.BASE)

        mock_final_scores.assert_called_once_with(FINAL_SCORES_THEN + scores)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_clarify.assert_not_called()

    @mock.patch.object(StatsplusPlugin, '_injuries')
    def test_on_message__with_delay(self, mock_injuries):
        injuries = INJURIES_TEXT.format(_html, _player)
        obj = {
            'channel': 'C7JSGHW8G',
            'text': INJURIES_DELAY + injuries,
            'ts': '1000.789',
            'user': 'U1234',
            'bot_id': 'B7KJ3362Y'
        }
        read = {
            'finished': False,
            'highlights': {},
            'injuries': {},
            'scores': {},
            'status': 'season',
            'updated': False
        }
        plugin = self.create_plugin(read)
        ret = plugin._on_message_internal(obj=obj)
        self.assertEqual(ret, ActivityEnum.BASE)

        mock_injuries.assert_called_once_with(INJURIES_DELAY + injuries)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_clarify.assert_not_called()

    @mock.patch.object(StatsplusPlugin, '_injuries')
    def test_on_message__with_injuries(self, mock_injuries):
        injuries = INJURIES_TEXT.format(_html, _player)
        obj = {
            'channel': 'C7JSGHW8G',
            'text': INJURIES_DATE + injuries,
            'ts': '1000.789',
            'user': 'U1234',
            'bot_id': 'B7KJ3362Y'
        }
        read = {
            'finished': False,
            'highlights': {},
            'injuries': {},
            'scores': {},
            'status': 'season',
            'updated': False
        }
        plugin = self.create_plugin(read)
        ret = plugin._on_message_internal(obj=obj)
        self.assertEqual(ret, ActivityEnum.BASE)

        mock_injuries.assert_called_once_with(INJURIES_DATE + injuries)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_clarify.assert_not_called()

    @mock.patch.object(StatsplusPlugin, '_highlights')
    def test_on_message__with_highlights(self, mock_highlights):
        highlights = HIGHLIGHTS_TEXT.format(_html, _player)
        obj = {
            'channel': 'C7JSGHW8G',
            'text': HIGHLIGHTS_DATE + highlights,
            'ts': '1000.789',
            'user': 'U1234',
            'bot_id': 'B7KJ3362Y'
        }
        read = {
            'finished': False,
            'highlights': {},
            'injuries': {},
            'scores': {},
            'status': 'season',
            'updated': False
        }
        plugin = self.create_plugin(read)
        ret = plugin._on_message_internal(obj=obj)
        self.assertEqual(ret, ActivityEnum.BASE)

        mock_highlights.assert_called_once_with(HIGHLIGHTS_DATE + highlights)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_clarify.assert_not_called()

    @mock.patch.object(StatsplusPlugin, '_clear')
    def test_on_message__with_invalid_bot_id(self, mock_clear):
        obj = {
            'channel': 'G3SUFLMK4',
            'text': 'text',
            'ts': '1000.789',
            'user': 'U1234',
        }
        read = {
            'finished': True,
            'highlights': {},
            'injuries': {},
            'scores': {},
            'status': 'season',
            'updated': False
        }
        plugin = self.create_plugin(read)
        ret = plugin._on_message_internal(obj=obj)
        self.assertEqual(ret, ActivityEnum.NONE)

        mock_clear.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_clarify.assert_not_called()

    @mock.patch.object(StatsplusPlugin, '_clear')
    def test_on_message__with_invalid_channel(self, mock_clear):
        obj = {
            'channel': 'G3SUFLMK4',
            'text': 'text',
            'ts': '1000.789',
            'user': 'U1234',
            'bot_id': 'B7KJ3362Y'
        }
        read = {
            'finished': True,
            'highlights': {},
            'injuries': {},
            'scores': {},
            'status': 'season',
            'updated': False
        }
        plugin = self.create_plugin(read)
        ret = plugin._on_message_internal(obj=obj)
        self.assertEqual(ret, ActivityEnum.NONE)

        mock_clear.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_clarify.assert_not_called()

    @mock.patch.object(StatsplusPlugin, '_render')
    def test_run__with_updated_true(self, mock_render):
        read = {
            'finished': False,
            'highlights': {},
            'injuries': {},
            'scores': {},
            'status': 'season',
            'updated': True
        }
        plugin = self.create_plugin(read)
        ret = plugin._run_internal(date=NOW)
        self.assertEqual(ret, ActivityEnum.BASE)

        write = {
            'finished': False,
            'highlights': {},
            'injuries': {},
            'scores': {},
            'status': 'season',
            'updated': False
        }
        mock_render.assert_called_once_with(date=NOW)
        self.mock_open.assert_called_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_clarify.assert_not_called()

    @mock.patch.object(StatsplusPlugin, '_render')
    def test_run__with_updated_false(self, mock_render):
        read = {
            'finished': False,
            'highlights': {},
            'injuries': {},
            'scores': {},
            'status': 'season',
            'updated': False
        }
        plugin = self.create_plugin(read)
        ret = plugin._run_internal(date=NOW)
        self.assertEqual(ret, ActivityEnum.NONE)

        mock_render.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_clarify.assert_not_called()

    @mock.patch.object(StatsplusPlugin, '_home')
    def test_render(self, mock_home):
        mock_home.return_value = HOME

        read = {
            'finished': False,
            'highlights': {},
            'injuries': {},
            'scores': {},
            'status': 'season',
            'updated': False
        }
        plugin = self.create_plugin(read)
        ret = plugin._render_internal(date=NOW)
        self.assertEqual(ret, [(INDEX, '', 'statsplus.html', HOME)])

        mock_home.assert_called_once_with(date=NOW)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_clarify.assert_not_called()

    @mock.patch.object(StatsplusPlugin, '_render')
    def test_setup(self, mock_render):
        read = {
            'finished': False,
            'highlights': {},
            'injuries': {},
            'scores': {},
            'status': 'season',
            'updated': False
        }
        plugin = self.create_plugin(read)
        plugin._setup_internal(date=NOW)

        mock_render.assert_called_once_with(date=NOW)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_clarify.assert_not_called()

    def test_clear(self):
        read = {
            'finished': False,
            'highlights': {},
            'injuries': {},
            'scores': {
                THEN_ENCODED: SEASON_SCORES_ENCODED
            },
            'status': 'season',
            'updated': False
        }
        plugin = self.create_plugin(read)
        plugin._clear()

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_clarify.assert_not_called()
        self.assertEqual(plugin.data['scores'], {})

    def test_live_tables_header(self):
        actual = StatsplusPlugin._live_tables_header('American League')
        expected = table(
            clazz='table-fixed border border-bottom-0 mt-3',
            hcols=[' class="text-center"'],
            bcols=[],
            head=['American League'],
            body=[])
        self.assertEqual(actual, expected)

    @mock.patch('plugins.statsplus.statsplus_plugin.logo_inline')
    def test_logo(self, mock_logo):
        mock_logo.return_value = 'logo'
        self.assertEqual(StatsplusPlugin._logo(('31', '0-1')), 'logo')

        mock_logo.assert_called_once_with('31', '0-1')

    def test_rewrite(self):
        self.init_mocks({})

        content = 'Arizona 4, Los Angeles 2'
        text = '<link|{}>'.format(content)
        actual = StatsplusPlugin._rewrite(THEN_ENCODED, text)
        expected = '<a href="link">{}</a>'.format(content)
        self.assertEqual(actual, expected)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_clarify.assert_called_once_with(THEN, 'link', content)

    def test_final_scores(self):
        read = {
            'finished': False,
            'highlights': {},
            'injuries': {},
            'scores': {},
            'status': 'season',
            'updated': False
        }
        plugin = self.create_plugin(read)
        text = FINAL_SCORES_THEN + SEASON_SCORES_TEXT.format(_html, _game_box)
        plugin._final_scores(text)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_clarify.assert_not_called()
        self.assertEqual(plugin.data['scores'], {
            THEN_ENCODED: SEASON_SCORES_ENCODED
        })
        self.assertTrue(plugin.data['updated'])

    def test_injuries__with_delay(self):
        read = {
            'finished': False,
            'highlights': {},
            'injuries': {},
            'scores': {},
            'status': 'season',
            'updated': False
        }
        plugin = self.create_plugin(read)
        text = INJURIES_DELAY + INJURIES_TEXT.format(_html, _player)
        plugin._injuries(text)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_clarify.assert_not_called()
        self.assertEqual(plugin.data['injuries'], {
            THEN_ENCODED: [INJURIES_TEXT_ENCODED]
        })
        self.assertTrue(plugin.data['updated'])

    def test_injuries__with_injuries(self):
        read = {
            'finished': False,
            'highlights': {},
            'injuries': {},
            'scores': {},
            'status': 'season',
            'updated': False
        }
        plugin = self.create_plugin(read)
        text = INJURIES_DATE + INJURIES_TEXT.format(_html, _player)
        plugin._injuries(text)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_clarify.assert_not_called()
        self.assertEqual(plugin.data['injuries'], {
            THEN_ENCODED: [INJURIES_TEXT_ENCODED]
        })
        self.assertTrue(plugin.data['updated'])

    def test_highlights__with_record(self):
        read = {
            'finished': False,
            'highlights': {},
            'injuries': {},
            'scores': {},
            'status': 'season',
            'updated': False
        }
        plugin = self.create_plugin(read)
        text = HIGHLIGHTS_DATE + HIGHLIGHTS_TEXT.format(_html, _player)
        plugin._highlights(text)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_clarify.assert_not_called()
        self.assertEqual(plugin.data['highlights'], {
            THEN_ENCODED: [HIGHLIGHTS_TEXT_ENCODED]
        })
        self.assertTrue(plugin.data['updated'])

    @mock.patch.object(StatsplusPlugin, '_scores_table')
    @mock.patch.object(StatsplusPlugin, '_live_tables_season')
    @mock.patch.object(StatsplusPlugin, '_injuries_table')
    @mock.patch.object(StatsplusPlugin, '_highlights_table')
    def test_home__with_season(self, mock_highlights, mock_injuries, mock_live,
                               mock_scores):
        mock_highlights.return_value = HIGHLIGHTS_TABLE_SEASON
        mock_injuries.return_value = INJURIES_TABLE_SEASON
        mock_live.return_value = [LIVE_TABLE_SEASON]
        mock_scores.side_effect = [SCORES_TABLE_NOW, SCORES_TABLE_THEN]

        read = {
            'finished': False,
            'highlights': {
                THEN_ENCODED: [HIGHLIGHTS_TEXT_ENCODED]
            },
            'injuries': {
                THEN_ENCODED: [INJURIES_TEXT_ENCODED]
            },
            'scores': {
                THEN_ENCODED: SEASON_SCORES_ENCODED,
                NOW_ENCODED: SEASON_SCORES_ENCODED
            },
            'status': 'season',
            'updated': False
        }
        plugin = self.create_plugin(read)
        ret = plugin._home(date=NOW)
        expected = {
            'breadcrumbs': BREADCRUMBS,
            'live': [LIVE_TABLE_SEASON],
            'scores': [SCORES_TABLE_NOW, SCORES_TABLE_THEN],
            'injuries': [INJURIES_TABLE_SEASON],
            'highlights': [HIGHLIGHTS_TABLE_SEASON]
        }
        self.assertEqual(ret, expected)

        mock_highlights.assert_called_once_with(THEN_ENCODED)
        mock_injuries.assert_called_once_with(THEN_ENCODED)
        mock_live.assert_called_once_with()
        calls = [mock.call(NOW_ENCODED), mock.call(THEN_ENCODED)]
        mock_scores.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_clarify.assert_not_called()

    @mock.patch.object(StatsplusPlugin, '_live_tables_season_internal')
    @mock.patch.object(StatsplusPlugin, '_live_tables_header')
    @mock.patch('plugins.statsplus.statsplus_plugin.divisions')
    def test_live_tables_season(self, mock_divisions, mock_header,
                                mock_internal):
        mock_divisions.return_value = AL + NL
        mock_header.return_value = [LIVE_TABLE_HEADER]
        mock_internal.return_value = [LIVE_TABLE_SEASON]

        read = {
            'finished': False,
            'highlights': {},
            'injuries': {},
            'scores': {},
            'status': 'season',
            'updated': False
        }
        plugin = self.create_plugin(read)
        actual = plugin._live_tables_season()
        expected = [[LIVE_TABLE_HEADER], [LIVE_TABLE_SEASON]] * 2
        self.assertEqual(actual, expected)

        mock_divisions.assert_called_once_with()
        calls = [mock.call('American League'), mock.call('National League')]
        mock_header.assert_has_calls(calls)
        mock_internal.assert_has_calls([mock.call(AL), mock.call(NL)])
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_clarify.assert_not_called()

    @mock.patch.object(StatsplusPlugin, '_record')
    @mock.patch.object(StatsplusPlugin, '_logo')
    def test_live_tables_season_internal(self, mock_logo, mock_record):
        mock_logo.return_value = 'logo'
        mock_record.side_effect = ['2-0', '0-2', '1-1'] * 3

        read = {
            'finished': False,
            'highlights': {},
            'injuries': {},
            'scores': {},
            'status': 'season',
            'updated': False
        }
        plugin = self.create_plugin(read)
        actual = plugin._live_tables_season_internal(AL)
        expected = table(
            clazz='table-fixed border',
            hcols=[],
            bcols=[' class="td-sm position-relative text-center w-20"'] * 5,
            head=[],
            body=[['logo', 'logo', 'logo'], ['logo', 'logo', 'logo'],
                  ['logo', 'logo', 'logo']])
        self.assertEqual(actual, expected)
        calls = [
            mock.call(('33', '2-0')),
            mock.call(('48', '1-1')),
            mock.call(('34', '0-2')),
            mock.call(('35', '2-0')),
            mock.call(('40', '1-1')),
            mock.call(('38', '0-2')),
            mock.call(('42', '2-0')),
            mock.call(('50', '1-1')),
            mock.call(('44', '0-2'))
        ]
        mock_logo.assert_has_calls(calls)
        calls = [
            mock.call('33'),
            mock.call('34'),
            mock.call('48'),
            mock.call('35'),
            mock.call('38'),
            mock.call('40'),
            mock.call('42'),
            mock.call('44'),
            mock.call('50')
        ]
        mock_record.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_clarify.assert_not_called()

    def test_record(self):
        read = {
            'finished': False,
            'highlights': {},
            'injuries': {},
            'scores': {
                THEN_ENCODED: SEASON_SCORES_ENCODED
            },
            'status': 'season',
            'updated': False
        }
        plugin = self.create_plugin(read)
        self.assertEqual(plugin._record('33'), '0-1')
        self.assertEqual(plugin._record('35'), '0-0')
        self.assertEqual(plugin._record('42'), '1-0')

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_clarify.assert_not_called()

    def test_scores_table(self):
        read = {
            'finished': False,
            'highlights': {},
            'injuries': {},
            'scores': {
                THEN_ENCODED: SEASON_SCORES_ENCODED
            },
            'status': 'season',
            'updated': False
        }
        plugin = self.create_plugin(read)

        actual = plugin._scores_table(THEN_ENCODED)
        expected = table(
            hcols=[''],
            bcols=[''],
            head=['Sunday, October 9th, 2022'],
            body=SCORES_TABLE_BODY)
        self.assertEqual(actual, expected)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        calls = [
            mock.call(THEN, game_box('{0}{1}2998.html'),
                      'Arizona Diamondbacks 4, Los Angeles 2'),
            mock.call(THEN, game_box('{0}{1}3003.html'),
                      'Atlanta Braves 2, Los Angeles 1'),
            mock.call(THEN, game_box('{0}{1}3002.html'),
                      'Detroit Tigers 11, Chicago 4'),
            mock.call(THEN, game_box('{0}{1}14721.html'),
                      'Miami Marlins 6, Chicago 2'),
            mock.call(THEN, game_box('{0}{1}3001.html'),
                      'New York 1, San Francisco Giants 0'),
            mock.call(THEN, game_box('{0}{1}3000.html'),
                      'New York 5, Baltimore Orioles 3')
        ]
        self.mock_clarify.assert_has_calls(calls)

    def test_injuries_table(self):
        read = {
            'finished': False,
            'highlights': {},
            'injuries': {
                THEN_ENCODED: [INJURIES_TEXT_ENCODED]
            },
            'scores': {},
            'status': 'season',
            'updated': False
        }
        plugin = self.create_plugin(read)

        actual = plugin._injuries_table(THEN_ENCODED)
        expected = table(
            hcols=[''],
            bcols=[''],
            head=['Sunday, October 9th, 2022'],
            body=INJURIES_TABLE_BODY)
        self.assertEqual(actual, expected)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_clarify.assert_not_called()

    def test_highlights_table(self):
        read = {
            'finished': False,
            'highlights': {
                THEN_ENCODED: [HIGHLIGHTS_TEXT_ENCODED]
            },
            'injuries': {},
            'scores': {},
            'status': 'season',
            'updated': False
        }
        plugin = self.create_plugin(read)

        actual = plugin._highlights_table(THEN_ENCODED)
        expected = table(
            hcols=[''],
            bcols=[''],
            head=['Sunday, October 9th, 2022'],
            body=HIGHLIGHTS_TABLE_BODY)
        self.assertEqual(actual, expected)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_clarify.assert_not_called()


if __name__ in ['__main__', 'plugins.statsplus.statsplus_plugin_test']:
    _main = __name__ == '__main__'
    _pkg = 'plugins.statsplus'
    _pth = 'plugins/statsplus'
    main(StatsplusPluginTest, StatsplusPlugin, _pkg, _pth, {}, _main)
