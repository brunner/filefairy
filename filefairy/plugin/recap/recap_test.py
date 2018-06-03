#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
import re
import sys
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(_path)
_root = re.sub(r'/plugin/recap', '', _path)
sys.path.append(_root)
from core.notify.notify import Notify  # noqa
from core.response.response import Response  # noqa
from core.shadow.shadow import Shadow  # noqa
from plugin.recap.recap import Recap  # noqa
from util.component.component import table  # noqa
from util.jinja2_.jinja2_ import env  # noqa
from util.json_.json_ import dumps  # noqa
from util.test.test import Test  # noqa
from util.test.test import main  # noqa

_leagues = os.path.join(_root, 'file/news/txt/leagues')
_injuries = os.path.join(_leagues, 'league_100_injuries.txt')
_news = os.path.join(_leagues, 'league_100_news.txt')
_transactions = os.path.join(_leagues, 'league_100_transactions.txt')

DATA = Recap._data()
ENV = env()
NOW = datetime.datetime(1985, 10, 26, 0, 2, 30)

INJ_THEN = '20220815\t<a href=\"../teams/team_44.html\">Los Angeles Angels' + \
           '</a>: CF <a href=\"../players/player_0.html\">Alex Aristy</a> ' + \
           'was injured while running the bases.  The Diagnosis: knee ' + \
           'inflammation. He\'s expected to miss about 3 weeks.'
INJ_NOW = '20220815\t<a href=\"../teams/team_57.html\">Tampa Bay Rays' + \
          '</a>: <a href=\"../players/player_1.html\">Zack Weiss</a> ' + \
          'diagnosed with a strained hamstring, will miss 8 months.\n' + \
          '20220817\t<a href=\"../teams/team_39.html\">Colorado Rockies' + \
          '</a>: RF <a href=\"../players/player_24198.html\">Eddie ' + \
          'Hoffman</a> was injured being hit by a pitch.  The Diagnosis: ' + \
          'bruised knee. This is a day-to-day injury expected to last 5 ' + \
          'days.\n20220817\t<a href=\"../teams/team_47.html\">Minnesota ' + \
          'Twins</a>: 1B <a href=\"../players/player_34032.html\">Nick ' + \
          'Castellanos</a> was injured while running the bases.  The ' + \
          'Diagnosis: sprained ankle. This is a day-to-day injury ' + \
          'expected to last 5 days.'
INJ_TABLE_NOW = [
    table(
        clazz='border mt-3',
        head=['Wednesday, August 17th, 2022'],
        body=[[
            'Colorado Rockies: RF <a href=\"/StatsLab/reports/news/html/' +
            'players/player_24198.html\">Eddie Hoffman</a> was injured ' +
            'being hit by a pitch.  The Diagnosis: bruised knee. This is ' +
            'a day-to-day injury expected to last 5 days.'
        ], [
            'Minnesota Twins: 1B <a href=\"/StatsLab/reports/news/html/' +
            'players/player_34032.html\">Nick Castellanos</a> was injured ' +
            'while running the bases.  The Diagnosis: sprained ankle. ' +
            'This is a day-to-day injury expected to last 5 days.'
        ]]),
    table(
        clazz='border mt-3',
        head=['Monday, August 15th, 2022'],
        body=[[
            'Tampa Bay Rays: <a href=\"/StatsLab/reports/news/html/' +
            'players/player_1.html\">Zack Weiss</a> diagnosed with a ' +
            'strained hamstring, will miss 8 months.'
        ]])
]
INJ_TABLE_THEN = [
    table(
        clazz='border mt-3',
        head=['Monday, August 15th, 2022'],
        body=[[
            'Los Angeles Angels: CF <a href=\"/StatsLab/reports/news/html/' +
            'players/player_0.html\">Alex Aristy</a> was injured while ' +
            'running the bases.  The Diagnosis: knee inflammation. He\'s ' +
            'expected to miss about 3 weeks.'
        ]])
]
INJ_ENCODED_THEN = '20220815\tT44: CF P0 was injured while running the ' + \
                   'bases.  The Diagnosis: knee inflammation. He\'s ' + \
                   'expected to miss about 3 weeks.'
INJ_ENCODED_NOW = '20220817\tT47: 1B P34032 was injured while running the ' + \
                  'bases.  The Diagnosis: sprained ankle. This is a ' + \
                  'day-to-day injury expected to last 5 days.'

NEWS_THEN = '20220815\t<a href=\"../teams/team_57.html\">Tampa Bay Rays' + \
            '</a>: <a href=\"../players/player_27.html\">A.J. Reed</a> ' + \
            'got suspended 4 games after ejection following arguing a ' + \
            'strike call.'
NEWS_NOW = '20220815\t<a href=\"../teams/team_42.html\">Houston Astros' + \
           '</a>: <a href=\"../players/player_39044.html\">Mark Appel</a> ' + \
           'pitches a 2-hit shutout against the <a href=\"../teams/team_44' + \
           '.html\">Los Angeles Angels</a> with 8 strikeouts and 0 BB ' + \
           'allowed!\n20220818\t<a href=\"../teams/team_39.html\">' + \
           'Colorado Rockies</a>: <a href=\"../players/player_30965' + \
           '.html\">Spencer Taylor</a> got suspended 3 games after ' + \
           'ejection following a brawl.\n20220818\t<a href=\"../teams/' + \
           'team_41.html\">Miami Marlins</a>: <a href=\"../players/' + \
           'player_131.html\">Jake Ehret</a> got suspended 3 games after ' + \
           'ejection following a brawl.'
NEWS_TABLE_NOW = [
    table(
        clazz='border mt-3',
        head=['Thursday, August 18th, 2022'],
        body=[[
            'Colorado Rockies: <a href=\"/StatsLab/reports/news/html/' +
            'players/player_30965.html\">Spencer Taylor</a> got suspended ' +
            '3 games after ejection following a brawl.'
        ], [
            'Miami Marlins: <a href=\"/StatsLab/reports/news/html/players/' +
            'player_131.html\">Jake Ehret</a> got suspended 3 games after ' +
            'ejection following a brawl.'
        ]]),
    table(
        clazz='border mt-3',
        head=['Monday, August 15th, 2022'],
        body=[[
            'Houston Astros: <a href=\"/StatsLab/reports/news/html/' +
            'players/player_39044.html\">Mark Appel</a> pitches a 2-hit ' +
            'shutout against the Los Angeles Angels with 8 strikeouts and ' +
            '0 BB allowed!'
        ]])
]
NEWS_TABLE_THEN = [
    table(
        clazz='border mt-3',
        head=['Monday, August 15th, 2022'],
        body=[[
            'Tampa Bay Rays: <a href=\"/StatsLab/reports/news/html/players/' +
            'player_27.html\">A.J. Reed</a> got suspended 4 games after ' +
            'ejection following arguing a strike call.'
        ]])
]
NEWS_ENCODED_THEN = '20220815\tT57: P27 got suspended 4 games after ' + \
                    'ejection following arguing a strike call.'
NEWS_ENCODED_NOW = '20220818\tT41: P131 got suspended 3 games after ' + \
                   'ejection following a brawl.'

TRANS_THEN = '20220815\t<a href=\"../teams/team_33.html\">Baltimore ' + \
             'Orioles</a>: Placed 2B <a href=\"../players/player_292' + \
             '.html\">Austin Slater</a> on the 7-day disabled list, ' + \
             'retroactive to 08/12/2022.\n'
TRANS_NOW = '20220815\t<a href=\"../teams/team_33.html\">Baltimore Orioles' + \
            '</a>: Placed C <a href=\"../players/player_1439.html\">Evan ' + \
            'Skoug</a> on the active roster.\n\n20220815\t<a href=\"../' + \
            'teams/team_33.html\">Baltimore Orioles</a>: Activated C <a ' + \
            'href=\"../players/player_1439.html\">Evan Skoug</a> from the ' + \
            'disabled list.\n\n20220815\t<a href=\"../teams/team_33' + \
            '.html\">Baltimore Orioles</a>: Placed C <a href=\"../players/' + \
            'player_31093.html\">Salvador Perez</a> on waivers.\n\n' + \
            '20220815\t<a href="../teams/team_43.html">Kansas City Royals' + \
            '</a>: Signed C <a href="../players/player_29806.html">Thomas ' + \
            'Dillard</a> to a 7-year contract extension worth a total of ' + \
            '$119,640,000.\n'
TRANS_TABLE_NOW = [
    table(
        clazz='border mt-3',
        head=['Monday, August 15th, 2022'],
        body=[[
            'Baltimore Orioles: Placed C <a href=\"/StatsLab/reports/news/' +
            'html/players/player_1439.html\">Evan Skoug</a> on the active ' +
            'roster.'
        ], [
            'Baltimore Orioles: Activated C <a href=\"/StatsLab/reports/' +
            'news/html/players/player_1439.html\">Evan Skoug</a> from the ' +
            'disabled list.'
        ], [
            'Baltimore Orioles: Placed C <a href=\"/StatsLab/reports/news/' +
            'html/players/player_31093.html\">Salvador Perez</a> on waivers.'
        ], [
            'Kansas City Royals: Signed C <a href=\"/StatsLab/reports/news/' +
            'html/players/player_29806.html\">Thomas Dillard</a> to a ' +
            '7-year contract extension worth a total of $119,640,000.'
        ]])
]
TRANS_TABLE_THEN = [
    table(
        clazz='border mt-3',
        head=['Monday, August 15th, 2022'],
        body=[[
            'Baltimore Orioles: Placed 2B <a href=\"/StatsLab/reports/news/' +
            'html/players/player_292.html\">Austin Slater</a> on the 7-day ' +
            'disabled list, retroactive to 08/12/2022.'
        ]])
]
TRANS_ENCODED_THEN = '20220815\tT33: Placed 2B P292 on the 7-day disabled ' + \
                     'list, retroactive to 08/12/2022.'
TRANS_ENCODED_NOW = '20220815\tT43: Signed C P29806 to a 7-year contract ' + \
                    'extension worth a total of $119,640,000.'

TABLE_NOW_MAP = {
    'injuries': INJ_TABLE_NOW,
    'news': NEWS_TABLE_NOW,
    'transactions': TRANS_TABLE_NOW
}
TABLE_THEN_MAP = {
    'injuries': INJ_TABLE_THEN,
    'news': NEWS_TABLE_THEN,
    'transactions': TRANS_TABLE_THEN
}
ENCODED_NOW_MAP = {
    'injuries': INJ_ENCODED_NOW,
    'news': NEWS_ENCODED_NOW,
    'transactions': TRANS_ENCODED_NOW
}
ENCODED_THEN_MAP = {
    'injuries': INJ_ENCODED_THEN,
    'news': NEWS_ENCODED_THEN,
    'transactions': TRANS_ENCODED_THEN
}

COLS = [
    'class="position-relative text-truncate"', ' class="text-right w-55p"',
    ' class="text-right w-55p"', ' class="text-right w-55p"',
    ' class="text-right w-55p"'
]
STANDINGS_TABLE = [
    table(
        hcols=COLS,
        bcols=COLS,
        head=['AL East', 'W', 'L', 'GB', 'M#'],
        body=[['33', '0', '0', '-', '163'], ['34', '0', '0', '-', '163'],
              ['48', '0', '0', '-', '163'], ['57', '0', '0', '-', '163'],
              ['59', '0', '0', '-', '163']])
]

DATE = '20220817'
LINE = '<a href=\"../teams/team_47.html\">Minnesota Twins</a>: 1B <a href=\"../players/player_34032.html\">Nick Castellanos</a> was injured while running the bases.  The Diagnosis: sprained ankle. This is a day-to-day injury expected to last 5 days.'
LINE_ENCODED = '20220817\tT47: 1B P34032 was injured while running the bases.  The Diagnosis: sprained ankle. This is a day-to-day injury expected to last 5 days.'
LINE_STRIPPED = 'Minnesota Twins: 1B <a href=\"../players/player_34032.html\">Nick Castellanos</a> was injured while running the bases.  The Diagnosis: sprained ankle. This is a day-to-day injury expected to last 5 days.'
LINE_REWRITTEN = '<a href=\"../teams/team_47.html\">Minnesota Twins</a>: 1B <a href=\"/StatsLab/reports/news/html/players/player_34032.html\">Nick Castellanos</a> was injured while running the bases.  The Diagnosis: sprained ankle. This is a day-to-day injury expected to last 5 days.'

HOME = {'breadcrumbs': [], 'injuries': [], 'news': [], 'transactions': []}
INDEX = 'html/fairylab/recap/index.html'
BREADCRUMBS = [{
    'href': '/fairylab/',
    'name': 'Home'
}, {
    'href': '',
    'name': 'Recap'
}]
STANDINGS_NOW = {'31': '76-86', '32': '77-85', '44': '70-92', '45': '97-65'}
STANDINGS_THEN = {'31': '75-85', '32': '76-85', '44': '70-91', '45': '96-64'}
BOX_SCORE1 = {
    'away_record': '76-86',
    'away_team': 'T31',
    'home_record': '97-65',
    'home_team': 'T45',
    'ok': True
}
BOX_SCORE2 = {
    'away_record': '77-85',
    'away_team': 'T32',
    'home_record': '70-92',
    'home_team': 'T44',
    'ok': True
}
BOX_SCORE3 = {
    'away_record': '75-86',
    'away_team': 'T31',
    'home_record': '97-64',
    'home_team': 'T45',
    'ok': True
}
RECORDS1 = {'31': '76-86', '45': '97-65'}
RECORDS2 = {'32': '77-85', '44': '70-92'}
RECORDS3 = {'31': '75-86', '45': '97-64'}
TS = '123456789'


class RecapTest(Test):
    def setUp(self):
        patch_open = mock.patch(
            'api.serializable.serializable.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

        patch_chat = mock.patch.object(Recap, '_chat')
        self.addCleanup(patch_chat.stop)
        self.mock_chat = patch_chat.start()

        patch_reactions = mock.patch('plugin.recap.recap.reactions_add')
        self.addCleanup(patch_reactions.stop)
        self.mock_reactions = patch_reactions.start()

    def init_mocks(self, read):
        mo = mock.mock_open(read_data=dumps(read))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]
        self.mock_chat.return_value = {'ok': True, 'ts': TS}

    def reset_mocks(self):
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()
        self.mock_chat.reset_mock()
        self.mock_reactions.reset_mock()

    def create_plugin(self, read):
        self.init_mocks(read)
        plugin = Recap(date=NOW, e=ENV)

        self.mock_open.assert_called_once_with(DATA, 'r')
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_reactions.assert_not_called()
        self.assertEqual(plugin.data, read)

        self.reset_mocks()
        self.init_mocks({})

        return plugin

    @mock.patch.object(Recap, '_tables')
    @mock.patch.object(Recap, '_standings')
    @mock.patch.object(Recap, '_render')
    @mock.patch.object(Recap, '_money')
    @mock.patch.object(Recap, '_death')
    def test_notify__with_death_download(self, mock_death, mock_money,
                                         mock_render, mock_standings,
                                         mock_tables):
        mock_death.return_value = True
        mock_money.return_value = False
        mock_tables.return_value = TABLE_NOW_MAP

        plugin = self.create_plugin({
            'now': ENCODED_NOW_MAP,
            'standings': STANDINGS_THEN,
            'then': ENCODED_THEN_MAP
        })
        plugin.tables = TABLE_THEN_MAP
        response = plugin._notify_internal(notify=Notify.DOWNLOAD_FINISH)
        self.assertEqual(response,
                         Response(
                             notify=[Notify.BASE],
                             shadow=plugin._shadow_internal()))
        write = {
            'now': ENCODED_NOW_MAP,
            'standings': STANDINGS_THEN,
            'then': ENCODED_NOW_MAP
        }
        mock_death.assert_called_once_with()
        mock_money.assert_called_once_with()
        mock_render.assert_called_once_with(notify=Notify.DOWNLOAD_FINISH)
        mock_standings.assert_called_once_with()
        mock_tables.assert_called_once_with()
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_called_once_with('fairylab', 'News updated.')
        self.mock_reactions.assert_called_once_with('skull', 'fairylab', TS)
        self.assertEqual(plugin.tables, TABLE_NOW_MAP)

    @mock.patch.object(Recap, '_tables')
    @mock.patch.object(Recap, '_standings')
    @mock.patch.object(Recap, '_render')
    @mock.patch.object(Recap, '_money')
    @mock.patch.object(Recap, '_death')
    def test_notify__with_money_download(self, mock_death, mock_money,
                                         mock_render, mock_standings,
                                         mock_tables):
        mock_death.return_value = False
        mock_money.return_value = True
        mock_tables.return_value = TABLE_NOW_MAP

        plugin = self.create_plugin({
            'now': ENCODED_NOW_MAP,
            'standings': STANDINGS_THEN,
            'then': ENCODED_THEN_MAP
        })
        plugin.tables = TABLE_THEN_MAP
        response = plugin._notify_internal(notify=Notify.DOWNLOAD_FINISH)
        self.assertEqual(response,
                         Response(
                             notify=[Notify.BASE],
                             shadow=plugin._shadow_internal()))
        write = {
            'now': ENCODED_NOW_MAP,
            'standings': STANDINGS_THEN,
            'then': ENCODED_NOW_MAP
        }
        mock_death.assert_called_once_with()
        mock_money.assert_called_once_with()
        mock_render.assert_called_once_with(notify=Notify.DOWNLOAD_FINISH)
        mock_standings.assert_called_once_with()
        mock_tables.assert_called_once_with()
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_called_once_with('fairylab', 'News updated.')
        self.mock_reactions.assert_called_once_with('moneybag', 'fairylab', TS)
        self.assertEqual(plugin.tables, TABLE_NOW_MAP)

    @mock.patch.object(Recap, '_tables')
    @mock.patch.object(Recap, '_standings')
    @mock.patch.object(Recap, '_render')
    @mock.patch.object(Recap, '_money')
    @mock.patch.object(Recap, '_death')
    def test_notify__with_quiet_download(self, mock_death, mock_money,
                                         mock_render, mock_standings,
                                         mock_tables):
        mock_death.return_value = False
        mock_money.return_value = False
        mock_tables.return_value = TABLE_NOW_MAP

        plugin = self.create_plugin({
            'now': ENCODED_NOW_MAP,
            'standings': STANDINGS_THEN,
            'then': ENCODED_THEN_MAP
        })
        plugin.tables = TABLE_THEN_MAP
        response = plugin._notify_internal(notify=Notify.DOWNLOAD_FINISH)
        self.assertEqual(response,
                         Response(
                             notify=[Notify.BASE],
                             shadow=plugin._shadow_internal()))
        write = {
            'now': ENCODED_NOW_MAP,
            'standings': STANDINGS_THEN,
            'then': ENCODED_NOW_MAP
        }
        mock_death.assert_called_once_with()
        mock_money.assert_called_once_with()
        mock_render.assert_called_once_with(notify=Notify.DOWNLOAD_FINISH)
        mock_standings.assert_called_once_with()
        mock_tables.assert_called_once_with()
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_called_once_with('fairylab', 'News updated.')
        self.mock_reactions.assert_not_called()
        self.assertEqual(plugin.tables, TABLE_NOW_MAP)

    @mock.patch.object(Recap, '_tables')
    @mock.patch.object(Recap, '_standings')
    @mock.patch.object(Recap, '_render')
    @mock.patch.object(Recap, '_money')
    @mock.patch.object(Recap, '_death')
    def test_notify__with_other(self, mock_death, mock_money, mock_render,
                                mock_standings, mock_tables):
        plugin = self.create_plugin({
            'now': ENCODED_NOW_MAP,
            'standings': STANDINGS_THEN,
            'then': ENCODED_THEN_MAP
        })
        plugin.tables = TABLE_THEN_MAP
        response = plugin._notify_internal(notify=Notify.OTHER)
        self.assertEqual(response, Response())

        mock_death.assert_not_called()
        mock_money.assert_not_called()
        mock_render.assert_not_called()
        mock_standings.assert_not_called()
        mock_tables.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_on_message(self):
        plugin = self.create_plugin({
            'now': ENCODED_NOW_MAP,
            'standings': STANDINGS_THEN,
            'then': ENCODED_THEN_MAP
        })
        response = plugin._on_message_internal()
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_run(self):
        plugin = self.create_plugin({
            'now': ENCODED_NOW_MAP,
            'standings': STANDINGS_THEN,
            'then': ENCODED_THEN_MAP
        })
        response = plugin._run_internal()
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Recap, '_home')
    def test_render(self, mock_home):
        mock_home.return_value = HOME

        plugin = self.create_plugin({
            'now': ENCODED_NOW_MAP,
            'standings': STANDINGS_THEN,
            'then': ENCODED_THEN_MAP
        })
        value = plugin._render_internal(date=NOW)
        self.assertEqual(value, [(INDEX, '', 'recap.html', HOME)])

        mock_home.assert_called_once_with(date=NOW)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Recap, '_tables')
    @mock.patch.object(Recap, '_render')
    def test_setup(self, mock_render, mock_tables):
        plugin = self.create_plugin({
            'now': ENCODED_NOW_MAP,
            'standings': STANDINGS_THEN,
            'then': ENCODED_THEN_MAP
        })
        response = plugin._setup_internal(date=NOW)
        self.assertEqual(response, Response())

        mock_render.assert_called_once_with(date=NOW)
        mock_tables.assert_called_once_with()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_shadow(self):
        plugin = self.create_plugin({
            'now': ENCODED_NOW_MAP,
            'standings': STANDINGS_THEN,
            'then': ENCODED_THEN_MAP
        })
        value = plugin._shadow_internal()
        self.assertEqual(value, [
            Shadow(
                destination='statsplus',
                key='recap.standings',
                data=STANDINGS_THEN)
        ])

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_encode(self):
        actual = Recap._encode(DATE, LINE)
        expected = LINE_ENCODED
        self.assertEqual(actual, expected)

    def test_strip_teams(self):
        actual = Recap._strip_teams(LINE)
        expected = LINE_STRIPPED
        self.assertEqual(actual, expected)

    def test_rewrite_players(self):
        actual = Recap._rewrite_players(LINE)
        expected = LINE_REWRITTEN
        self.assertEqual(actual, expected)

    def test_death__with_true(self):
        plugin = self.create_plugin({
            'now': ENCODED_NOW_MAP,
            'standings': STANDINGS_THEN,
            'then': ENCODED_THEN_MAP
        })
        plugin.tables = TABLE_NOW_MAP
        value = plugin._death()
        self.assertTrue(value)

    def test_death__with_false(self):
        plugin = self.create_plugin({
            'now': ENCODED_NOW_MAP,
            'standings': STANDINGS_THEN,
            'then': ENCODED_THEN_MAP
        })
        plugin.tables = TABLE_THEN_MAP
        value = plugin._death()
        self.assertFalse(value)

    @mock.patch('plugin.recap.recap.standings_table')
    def test_home(self, mock_standings):
        mock_standings.return_value = STANDINGS_TABLE

        plugin = self.create_plugin({
            'now': ENCODED_NOW_MAP,
            'standings': STANDINGS_THEN,
            'then': ENCODED_THEN_MAP
        })
        plugin.shadow['statsplus.offseason'] = False
        plugin.shadow['statsplus.postseason'] = False
        plugin.tables = TABLE_NOW_MAP

        value = plugin._home(date=NOW)
        expected = {
            'breadcrumbs': BREADCRUMBS,
            'injuries': INJ_TABLE_NOW,
            'news': NEWS_TABLE_NOW,
            'transactions': TRANS_TABLE_NOW,
            'standings': STANDINGS_TABLE
        }
        self.assertEqual(value, expected)

        mock_standings.assert_called_once_with(STANDINGS_THEN)
        self.mock_open.assert_not_called()
        self.mock_handle.write.not_called()
        self.mock_chat.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_money__with_true(self):
        plugin = self.create_plugin({
            'now': ENCODED_NOW_MAP,
            'standings': STANDINGS_THEN,
            'then': ENCODED_THEN_MAP
        })
        plugin.tables = TABLE_NOW_MAP
        value = plugin._money()
        self.assertTrue(value)

    def test_money__with_false(self):
        plugin = self.create_plugin({
            'now': ENCODED_NOW_MAP,
            'standings': STANDINGS_THEN,
            'then': ENCODED_THEN_MAP
        })
        plugin.tables = TABLE_THEN_MAP
        value = plugin._money()
        self.assertFalse(value)

    @mock.patch('plugin.recap.recap.os.listdir')
    @mock.patch('plugin.recap.recap.box_score')
    def test_standings(self, mock_box, mock_listdir):
        boxes = ['123', '456', '789']
        mock_listdir.return_value = [
            'game_box_{}.html'.format(b) for b in boxes
        ]
        mock_box.side_effect = [BOX_SCORE1, BOX_SCORE2, BOX_SCORE3]

        plugin = self.create_plugin({'standings': STANDINGS_THEN})
        plugin._standings()
        expected = RECORDS1.copy()
        expected.update(RECORDS2)
        self.assertEqual(plugin.data['standings'], expected)

        write = {'standings': STANDINGS_NOW}
        dpath = os.path.join(_root, 'resource/extract/box_scores')
        mock_listdir.assert_called_once_with(dpath)
        calls = [
            mock.call(os.path.join(dpath, 'game_box_{}.html'.format(b)))
            for b in boxes
        ]
        mock_box.assert_has_calls(calls)
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch('plugin.recap.recap.open', create=True)
    def test_tables_internal__injuries(self, mock_open):
        injuries = '\n'.join([INJ_THEN, INJ_NOW])
        mo = mock.mock_open(read_data=injuries)
        mock_open.side_effect = [mo.return_value]

        plugin = self.create_plugin({
            'now': {
                'injuries': ''
            },
            'standings': STANDINGS_THEN,
            'then': {
                'injuries': INJ_ENCODED_THEN
            }
        })
        actual = plugin._tables_internal('injuries')
        expected = INJ_TABLE_NOW
        self.assertEqual(actual, expected)

        dpath = os.path.join(_root, 'resource/extract/leagues/{}.txt')
        mock_open.assert_called_once_with(dpath.format('injuries'), 'r')
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_reactions.assert_not_called()
        self.assertEqual(plugin.data['now']['injuries'], INJ_ENCODED_NOW)

    @mock.patch('plugin.recap.recap.open', create=True)
    def test_tables_internal__news(self, mock_open):
        news = '\n'.join([NEWS_THEN, NEWS_NOW])
        mo = mock.mock_open(read_data=news)
        mock_open.side_effect = [mo.return_value]

        plugin = self.create_plugin({
            'now': {
                'news': ''
            },
            'standings': STANDINGS_THEN,
            'then': {
                'news': NEWS_ENCODED_THEN
            }
        })
        actual = plugin._tables_internal('news')
        expected = NEWS_TABLE_NOW
        self.assertEqual(actual, expected)

        dpath = os.path.join(_root, 'resource/extract/leagues/{}.txt')
        mock_open.assert_called_once_with(dpath.format('news'), 'r')
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_reactions.assert_not_called()
        self.assertEqual(plugin.data['now']['news'], NEWS_ENCODED_NOW)

    @mock.patch('plugin.recap.recap.open', create=True)
    def test_tables_internal__transactions(self, mock_open):
        trans = '\n'.join([TRANS_THEN, TRANS_NOW])
        mo = mock.mock_open(read_data=trans)
        mock_open.side_effect = [mo.return_value]

        plugin = self.create_plugin({
            'now': {
                'transactions': ''
            },
            'standings': STANDINGS_THEN,
            'then': {
                'transactions': TRANS_ENCODED_THEN
            }
        })
        actual = plugin._tables_internal('transactions')
        expected = TRANS_TABLE_NOW
        self.assertEqual(actual, expected)

        dpath = os.path.join(_root, 'resource/extract/leagues/{}.txt')
        mock_open.assert_called_once_with(dpath.format('transactions'), 'r')
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_reactions.assert_not_called()
        self.assertEqual(plugin.data['now']['transactions'], TRANS_ENCODED_NOW)


if __name__ in ['__main__', 'plugin.recap.recap_test']:
    _main = __name__ == '__main__'
    _pkg = 'plugin.recap'
    _pth = 'plugin/recap'
    main(RecapTest, Recap, _pkg, _pth, {}, _main, date=NOW, e=ENV)
