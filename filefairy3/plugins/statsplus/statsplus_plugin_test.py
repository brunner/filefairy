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
from utils.team.team_util import ilogo  # noqa
from utils.test.test_util import main, TestUtil  # noqa

_html = 'https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/'
_game_box = 'box_scores/game_box'

DATA = StatsplusPlugin._data()
NOW_ENCODED = '2022-10-10T00:00:00'
THEN_ENCODED = '2022-10-09T00:00:00'
HOME = {'breadcrumbs': [], 'live': []}
INDEX = 'html/fairylab/statsplus/index.html'
LIVE_TABLE_HEADER = table(head=['American League'])
LIVE_TABLE_SEASON = table(body=[['BAL 1-0', 'BOS 0-1']])
SCORES_TABLE_NOW = table(head='2022-10-10', body=[['Baltimore 1, Boston 0']])
SCORES_TABLE_THEN = table(head='2022-10-09', body=[['Baltimore 1, Boston 0']])
NOW = datetime.datetime(1985, 10, 26, 0, 2, 30)
AL = [('AL East', ['33']), ('AL Central', ['35']), ('AL West', ['42'])]
NL = [('NL East', ['32']), ('NL Central', ['36']), ('NL West', ['31'])]
FINAL_SCORES_THEN = '10/09/2022 MAJOR LEAGUE BASEBALL Final Scores\n'
FINAL_SCORES_NOW = '10/10/2022 MAJOR LEAGUE BASEBALL Final Scores\n'
SEASON_SCORES = '<{0}{1}_2998.html|Arizona 4, Los Angeles 2>\n' + \
                '<{0}{1}_3003.html|Atlanta 2, Los Angeles 1>\n' + \
                '<{0}{1}_2996.html|Cincinnati 7, Milwaukee 2>\n' + \
                '<{0}{1}_3002.html|Detroit 11, Chicago 4>\n' + \
                '<{0}{1}_2993.html|Houston 7, Seattle 2>\n' + \
                '<{0}{1}_2991.html|Kansas City 8, Cleveland 2>\n' + \
                '<{0}{1}_14721.html|Miami 6, Chicago 2>\n' + \
                '<{0}{1}_3001.html|New York 1, San Francisco 0>\n' + \
                '<{0}{1}_3000.html|New York 5, Baltimore 3>\n' + \
                '<{0}{1}_2992.html|Philadelphia 3, Washington 1>\n' + \
                '<{0}{1}_2999.html|San Diego 8, Colorado 2>\n' + \
                '<{0}{1}_2990.html|St. Louis 5, Pittsburgh 4>\n' + \
                '<{0}{1}_2997.html|Tampa Bay 12, Boston 9>\n' + \
                '<{0}{1}_2994.html|Texas 5, Oakland 3>\n' + \
                '<{0}{1}_2995.html|Toronto 8, Minnesota 2>'
SEASON_SCORES_TEXT = SEASON_SCORES.replace('<', '*<').replace('>', '>*')


def game_box(s):
    return s.format(_html, _game_box)


SCORES_TABLE_BODY = [[
    game_box('<a href="{0}{1}_2998.html">Arizona 4, Los Angeles 2</a>')
], [game_box('<a href="{0}{1}_3003.html">Atlanta 2, Los Angeles 1</a>')], [
    game_box('<a href="{0}{1}_2996.html">Cincinnati 7, Milwaukee 2</a>')
], [game_box('<a href="{0}{1}_3002.html">Detroit 11, Chicago 4</a>')], [
    game_box('<a href="{0}{1}_2993.html">Houston 7, Seattle 2</a>')
], [game_box('<a href="{0}{1}_2991.html">Kansas City 8, Cleveland 2</a>')], [
    game_box('<a href="{0}{1}_14721.html">Miami 6, Chicago 2</a>')
], [game_box('<a href="{0}{1}_3001.html">New York 1, San Francisco 0</a>')], [
    game_box('<a href="{0}{1}_3000.html">New York 5, Baltimore 3</a>')
], [game_box('<a href="{0}{1}_2992.html">Philadelphia 3, Washington 1</a>')], [
    game_box('<a href="{0}{1}_2999.html">San Diego 8, Colorado 2</a>')
], [game_box('<a href="{0}{1}_2990.html">St. Louis 5, Pittsburgh 4</a>')], [
    game_box('<a href="{0}{1}_2997.html">Tampa Bay 12, Boston 9</a>')
], [game_box('<a href="{0}{1}_2994.html">Texas 5, Oakland 3</a>')], [
    game_box('<a href="{0}{1}_2995.html">Toronto 8, Minnesota 2</a>')
]]
BREADCRUMBS = [{
    'href': '/fairylab/',
    'name': 'Home'
}, {
    'href': '',
    'name': 'Statsplus'
}]


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

        self.mock_open.assert_called_once_with(DATA, 'r')
        self.mock_handle.write.assert_not_called()

        self.reset_mocks()
        self.init_mocks(data)

        return plugin

    def test_notify__with_download(self):
        read = {
            'finished': False,
            'scores': {},
            'status': 'season',
            'updated': False
        }
        plugin = self.create_plugin(read)
        ret = plugin._notify_internal(activity=ActivityEnum.DOWNLOAD)
        self.assertFalse(ret)

        write = {
            'finished': True,
            'scores': {},
            'status': 'season',
            'updated': False
        }
        self.mock_open.assert_called_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    def test_notify__with_none(self):
        read = {
            'finished': False,
            'scores': {},
            'status': 'season',
            'updated': False
        }
        plugin = self.create_plugin(read)
        ret = plugin._notify_internal(activity=ActivityEnum.NONE)
        self.assertFalse(ret)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

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
            'scores': {},
            'status': 'season',
            'updated': False
        }
        plugin = self.create_plugin(read)
        ret = plugin._on_message_internal(obj=obj)
        self.assertEqual(ret, ActivityEnum.BASE)

        write = {
            'finished': False,
            'scores': {},
            'status': 'season',
            'updated': False
        }
        mock_clear.assert_called_once_with()
        self.mock_open.assert_called_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

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

    @mock.patch.object(StatsplusPlugin, '_render')
    def test_run__with_updated_true(self, mock_render):
        read = {
            'finished': False,
            'scores': {},
            'status': 'season',
            'updated': True
        }
        plugin = self.create_plugin(read)
        ret = plugin._run_internal(date=NOW)
        self.assertEqual(ret, ActivityEnum.BASE)

        write = {
            'finished': False,
            'scores': {},
            'status': 'season',
            'updated': False
        }
        mock_render.assert_called_once_with(date=NOW)
        self.mock_open.assert_called_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch.object(StatsplusPlugin, '_render')
    def test_run__with_updated_false(self, mock_render):
        read = {
            'finished': False,
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

    @mock.patch.object(StatsplusPlugin, '_home')
    def test_render(self, mock_home):
        mock_home.return_value = HOME

        read = {
            'finished': False,
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

    @mock.patch.object(StatsplusPlugin, '_render')
    def test_setup(self, mock_render):
        read = {
            'finished': False,
            'scores': {},
            'status': 'season',
            'updated': False
        }
        plugin = self.create_plugin(read)
        plugin._setup_internal(date=NOW)

        mock_render.assert_called_once_with(date=NOW)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    def test_clear(self):
        read = {
            'finished': False,
            'scores': {
                THEN_ENCODED: SEASON_SCORES
            },
            'status': 'season',
            'updated': False
        }
        plugin = self.create_plugin(read)
        plugin._clear()

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
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

    def test_final_scores(self):
        read = {
            'finished': False,
            'scores': {},
            'status': 'season',
            'updated': False
        }
        plugin = self.create_plugin(read)
        text = FINAL_SCORES_THEN + SEASON_SCORES_TEXT.format(_html, _game_box)
        plugin._final_scores(text)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.assertEqual(plugin.data['scores'], {THEN_ENCODED: SEASON_SCORES})
        self.assertTrue(plugin.data['updated'])

    @mock.patch.object(StatsplusPlugin, '_scores_table')
    @mock.patch.object(StatsplusPlugin, '_live_tables_season')
    def test_home__with_season(self, mock_live, mock_scores):
        mock_live.return_value = [LIVE_TABLE_SEASON]
        mock_scores.side_effect = [SCORES_TABLE_NOW, SCORES_TABLE_THEN]

        read = {
            'finished': False,
            'scores': {
                THEN_ENCODED: SEASON_SCORES,
                NOW_ENCODED: SEASON_SCORES
            },
            'status': 'season',
            'updated': False
        }
        plugin = self.create_plugin(read)
        ret = plugin._home(date=NOW)
        expected = {
            'breadcrumbs': BREADCRUMBS,
            'live': [LIVE_TABLE_SEASON],
            'scores': [SCORES_TABLE_NOW, SCORES_TABLE_THEN]
        }
        self.assertEqual(ret, expected)

        mock_live.assert_called_once_with()
        calls = [mock.call(NOW_ENCODED), mock.call(THEN_ENCODED)]
        mock_scores.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

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

    @mock.patch.object(StatsplusPlugin, '_scores_season')
    def test_live_tables_season_internal(self, mock_scores):
        score = 'BAL 1-0'
        mock_scores.return_value = score

        read = {
            'finished': False,
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
            body=[[score], [score], [score]])
        self.assertEqual(actual, expected)

        calls = [mock.call('33'), mock.call('35'), mock.call('42')]
        mock_scores.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    def test_scores_season(self):
        read = {
            'finished': False,
            'scores': {
                THEN_ENCODED: SEASON_SCORES
            },
            'status': 'season',
            'updated': False
        }
        plugin = self.create_plugin(read)

        actual = plugin._scores_season('33')
        expected = ilogo('33', '0-1')
        self.assertEqual(actual, expected)
        actual = plugin._scores_season('35')
        expected = ilogo('35', '0-2')
        self.assertEqual(actual, expected)
        actual = plugin._scores_season('42')
        expected = ilogo('42', '1-0')
        self.assertEqual(actual, expected)

    def test_scores_table(self):
        read = {
            'finished': False,
            'scores': {
                THEN_ENCODED: SEASON_SCORES
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


if __name__ in ['__main__', 'plugins.statsplus.statsplus_plugin_test']:
    _main = __name__ == '__main__'
    _pkg = 'plugins.statsplus'
    _pth = 'plugins/statsplus'
    main(StatsplusPluginTest, StatsplusPlugin, _pkg, _pth, {}, _main)
