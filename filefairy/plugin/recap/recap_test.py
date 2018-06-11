#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import logging
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

_channel = 'C1234'
_env = env()
_now = datetime.datetime(1985, 10, 26, 0, 2, 30)
_standings = {'31': '75-85', '32': '76-85', '44': '70-91', '45': '96-64'}
_ts = '123456789'

_injuries_encoded_new = '20220817\tT47: 1B P34032 was injured while runnin' + \
                        'g the bases.  The Diagnosis: sprained ankle. This' + \
                        ' is a day-to-day injury expected to last 5 days.'
_injuries_encoded_old = '20220815\tT44: CF P0 was injured while running th' + \
                        'e bases.  The Diagnosis: knee inflammation. He\'s' + \
                        ' expected to miss about 3 weeks.'
_news_encoded_new = '20220818\tT41: P131 got suspended 3 games after eject' + \
                    'ion following a brawl.'
_news_encoded_old = '20220815\tT57: P27 got suspended 4 games after ejecti' + \
                    'on following arguing a strike call.'
_transactions_encoded_old = '20220815\tT33: Placed 2B P292 on the 7-day di' + \
                            'sabled list, retroactive to 08/12/2022.'
_transactions_encoded_new = '20220815\tT43: Signed C P29806 to a 7-year co' + \
                            'ntract extension worth a total of $119,640,000.'
_encoded_new = {
    'injuries': _injuries_encoded_new,
    'news': _news_encoded_new,
    'transactions': _transactions_encoded_new
}
_encoded_old = {
    'injuries': _injuries_encoded_old,
    'news': _news_encoded_old,
    'transactions': _transactions_encoded_old
}

_injuries_table_new = [
    table(
        clazz='border mt-3',
        head=['Wednesday, August 17th, 2022'],
        body=[[
            'Colorado Rockies: RF <a href=\"/StatsLab/reports/news/html/play' +
            'ers/player_24198.html\">Eddie Hoffman</a> was injured being hit' +
            ' by a pitch.  The Diagnosis: bruised knee. This is a day-to-day' +
            ' injury expected to last 5 days.'
        ], [
            'Minnesota Twins: 1B <a href=\"/StatsLab/reports/news/html/playe' +
            'rs/player_34032.html\">Nick Castellanos</a> was injured while r' +
            'unning the bases.  The Diagnosis: sprained ankle. This is a day' +
            '-to-day injury expected to last 5 days.'
        ]]),
    table(
        clazz='border mt-3',
        head=['Monday, August 15th, 2022'],
        body=[[
            'Tampa Bay Rays: <a href=\"/StatsLab/reports/news/html/players/p' +
            'layer_1.html\">Zack Weiss</a> diagnosed with a strained hamstri' +
            'ng, will miss 8 months.'
        ]])
]
_injuries_table_old = [
    table(
        clazz='border mt-3',
        head=['Monday, August 15th, 2022'],
        body=[[
            'Los Angeles Angels: CF <a href=\"/StatsLab/reports/news/html/pl' +
            'ayers/player_0.html\">Alex Aristy</a> was injured while running' +
            ' the bases.  The Diagnosis: knee inflammation. He\'s expected t' +
            'o miss about 3 weeks.'
        ]])
]
_news_table_new = [
    table(
        clazz='border mt-3',
        head=['Thursday, August 18th, 2022'],
        body=[[
            'Colorado Rockies: <a href=\"/StatsLab/reports/news/html/players' +
            '/player_30965.html\">Spencer Taylorr</a> got suspended 3 games ' +
            'after ejection following a brawl.'
        ], [
            'Miami Marlins: <a href=\"/StatsLab/reports/news/html/players/pl' +
            'ayer_131.html\">Jake Ehret</a> got suspended 3 games after ejec' +
            'tion following a brawl.'
        ]]),
    table(
        clazz='border mt-3',
        head=['Monday, August 15th, 2022'],
        body=[[
            'Houston Astros: <a href=\"/StatsLab/reports/news/html/players/p' +
            'layer_39044.html\">Mark Appel</a> pitches a 2-hit shutout again' +
            'st the Los Angeles Angels with 8 strikeouts and 0 BB allowed!'
        ]])
]
_news_table_old = [
    table(
        clazz='border mt-3',
        head=['Monday, August 15th, 2022'],
        body=[[
            'Tampa Bay Rays: <a href=\"/StatsLab/reports/news/html/players/p' +
            'layer_27.html\">A.J. Reed</a> got suspended 4 games after eject' +
            'ion following arguing a strike call.'
        ]])
]
_transactions_table_new = [
    table(
        clazz='border mt-3',
        head=['Monday, August 15th, 2022'],
        body=[[
            'Baltimore Orioles: Placed C <a href=\"/StatsLab/reports/news/ht' +
            'ml/players/player_1439.html\">Evan Skoug</a> on the active rost' +
            'er.'
        ], [
            'Baltimore Orioles: Activated C <a href=\"/StatsLab/reports/news' +
            '/html/players/player_1439.html\">Evan Skoug</a> from the disabl' +
            'ed list.'
        ], [
            'Baltimore Orioles: Placed C <a href=\"/StatsLab/reports/news/ht' +
            'ml/players/player_31093.html\">Salvador Perez</a> on waivers.'
        ], [
            'Kansas City Royals: Signed C <a href=\"/StatsLab/reports/news/h' +
            'tml/players/player_29806.html\">Thomas Dillard</a> to a 7-year ' +
            'contract extension worth a total of $119,640,000.'
        ]])
]
_transactions_table_old = [
    table(
        clazz='border mt-3',
        head=['Monday, August 15th, 2022'],
        body=[[
            'Baltimore Orioles: Placed 2B <a href=\"/StatsLab/reports/news/h' +
            'tml/players/player_292.html\">Austin Slater</a> on the 7-day di' +
            'sabled list, retroactive to 08/12/2022.'
        ]])
]
_table_new = {
    'injuries': _injuries_table_new,
    'news': _news_table_new,
    'transactions': _transactions_table_new
}
_table_old = {
    'injuries': _injuries_table_old,
    'news': _news_table_old,
    'transactions': _transactions_table_old
}


def _data(now=_encoded_new, standings=_standings, then=_encoded_old):
    return {'now': now, 'standings': standings, 'then': then}


class RecapTest(Test):
    def setUp(self):
        patch_open = mock.patch(
            'api.serializable.serializable.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

        patch_chat = mock.patch.object(Recap, '_chat')
        self.addCleanup(patch_chat.stop)
        self.mock_chat = patch_chat.start()

        patch_log = mock.patch('plugin.recap.recap.logger_.log')
        self.addCleanup(patch_log.stop)
        self.mock_log = patch_log.start()

        patch_reactions = mock.patch('plugin.recap.recap.reactions_add')
        self.addCleanup(patch_reactions.stop)
        self.mock_reactions = patch_reactions.start()

    def init_mocks(self, read):
        mo = mock.mock_open(read_data=dumps(read))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]
        self.mock_chat.return_value = {
            'ok': True,
            'channel': _channel,
            'ts': _ts
        }

    def reset_mocks(self):
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()
        self.mock_chat.reset_mock()
        self.mock_log.reset_mock()
        self.mock_reactions.reset_mock()

    def create_plugin(self, read):
        self.init_mocks(read)
        plugin = Recap(date=_now, e=_env)

        self.mock_open.assert_called_once_with(Recap._data(), 'r')
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
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
        mock_tables.return_value = _table_new

        plugin = self.create_plugin(_data())
        plugin.tables = _table_old
        response = plugin._notify_internal(notify=Notify.DOWNLOAD_FINISH)
        self.assertEqual(response,
                         Response(
                             notify=[Notify.BASE],
                             shadow=plugin._shadow_internal()))

        write = _data(then=_encoded_new)
        mock_death.assert_called_once_with()
        mock_money.assert_called_once_with()
        mock_render.assert_called_once_with(notify=Notify.DOWNLOAD_FINISH)
        mock_standings.assert_called_once_with()
        mock_tables.assert_called_once_with()
        self.mock_open.assert_called_once_with(Recap._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_called_once_with('fairylab', 'News updated.')
        self.mock_log.assert_called_once_with(logging.INFO, 'News updated.')
        self.mock_reactions.assert_called_once_with('skull', _channel, _ts)
        self.assertEqual(plugin.tables, _table_new)

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
        mock_tables.return_value = _table_new

        plugin = self.create_plugin(_data())
        plugin.tables = _table_old
        response = plugin._notify_internal(notify=Notify.DOWNLOAD_FINISH)
        self.assertEqual(response,
                         Response(
                             notify=[Notify.BASE],
                             shadow=plugin._shadow_internal()))

        write = _data(then=_encoded_new)
        mock_death.assert_called_once_with()
        mock_money.assert_called_once_with()
        mock_render.assert_called_once_with(notify=Notify.DOWNLOAD_FINISH)
        mock_standings.assert_called_once_with()
        mock_tables.assert_called_once_with()
        self.mock_open.assert_called_once_with(Recap._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_called_once_with('fairylab', 'News updated.')
        self.mock_log.assert_called_once_with(logging.INFO, 'News updated.')
        self.mock_reactions.assert_called_once_with('moneybag', _channel, _ts)
        self.assertEqual(plugin.tables, _table_new)

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
        mock_tables.return_value = _table_new

        plugin = self.create_plugin(_data())
        plugin.tables = _table_old
        response = plugin._notify_internal(notify=Notify.DOWNLOAD_FINISH)
        self.assertEqual(response,
                         Response(
                             notify=[Notify.BASE],
                             shadow=plugin._shadow_internal()))

        write = _data(then=_encoded_new)
        mock_death.assert_called_once_with()
        mock_money.assert_called_once_with()
        mock_render.assert_called_once_with(notify=Notify.DOWNLOAD_FINISH)
        mock_standings.assert_called_once_with()
        mock_tables.assert_called_once_with()
        self.mock_open.assert_called_once_with(Recap._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_called_once_with('fairylab', 'News updated.')
        self.mock_log.assert_called_once_with(logging.INFO, 'News updated.')
        self.mock_reactions.assert_not_called()
        self.assertEqual(plugin.tables, _table_new)

    @mock.patch.object(Recap, '_tables')
    @mock.patch.object(Recap, '_standings')
    @mock.patch.object(Recap, '_render')
    @mock.patch.object(Recap, '_money')
    @mock.patch.object(Recap, '_death')
    def test_notify__with_other(self, mock_death, mock_money, mock_render,
                                mock_standings, mock_tables):
        plugin = self.create_plugin(_data())
        plugin.tables = _table_old
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
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_on_message(self):
        plugin = self.create_plugin(_data())
        response = plugin._on_message_internal()
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_run(self):
        plugin = self.create_plugin(_data())
        response = plugin._run_internal()
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Recap, '_home')
    def test_render(self, mock_home):
        home = {
            'breadcrumbs': [],
            'injuries': [],
            'news': [],
            'transactions': []
        }
        mock_home.return_value = home

        plugin = self.create_plugin(_data())
        value = plugin._render_internal(date=_now)
        index = 'html/fairylab/recap/index.html'
        self.assertEqual(value, [(index, '', 'recap.html', home)])

        mock_home.assert_called_once_with(date=_now)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Recap, '_tables')
    @mock.patch.object(Recap, '_render')
    def test_setup(self, mock_render, mock_tables):
        plugin = self.create_plugin(_data())
        response = plugin._setup_internal(date=_now)
        self.assertEqual(response, Response())

        mock_render.assert_called_once_with(date=_now)
        mock_tables.assert_called_once_with()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_shadow(self):
        plugin = self.create_plugin(_data())
        value = plugin._shadow_internal()
        self.assertEqual(value, [
            Shadow(
                destination='statsplus',
                key='recap.standings',
                data=_standings)
        ])

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_encode(self):
        date = '20220817'
        line = '<a href=\"../teams/team_47.html\">Minnesota Twins</a>: 1B ' + \
               '<a href=\"../players/player_34032.html\">Nick Castellanos<' + \
               '/a> was injured while running the bases.  The Diagnosis: s' + \
               'prained ankle. This is a day-to-day injury expected to las' + \
               't 5 days.'
        actual = Recap._encode(date, line)
        expected = '20220817\tT47: 1B P34032 was injured while running the' + \
                   ' bases.  The Diagnosis: sprained ankle. This is a day-' + \
                   'to-day injury expected to last 5 days.'
        self.assertEqual(actual, expected)

    def test_strip_teams(self):
        line = '<a href=\"../teams/team_47.html\">Minnesota Twins</a>: 1B ' + \
               '<a href=\"../players/player_34032.html\">Nick Castellanos<' + \
               '/a> was injured while running the bases.  The Diagnosis: s' + \
               'prained ankle. This is a day-to-day injury expected to las' + \
               't 5 days.'
        actual = Recap._strip_teams(line)
        expected = 'Minnesota Twins: 1B <a href=\"../players/player_34032.' + \
                   'html\">Nick Castellanos</a> was injured while running ' + \
                   'the bases.  The Diagnosis: sprained ankle. This is a d' + \
                   'ay-to-day injury expected to last 5 days.'
        self.assertEqual(actual, expected)

    def test_rewrite_players(self):
        line = '<a href=\"../teams/team_47.html\">Minnesota Twins</a>: 1B ' + \
               '<a href=\"../players/player_34032.html\">Nick Castellanos<' + \
               '/a> was injured while running the bases.  The Diagnosis: s' + \
               'prained ankle. This is a day-to-day injury expected to las' + \
               't 5 days.'
        actual = Recap._rewrite_players(line)
        expected = '<a href=\"../teams/team_47.html\">Minnesota Twins</a>:' + \
                   ' 1B <a href=\"/StatsLab/reports/news/html/players/play' + \
                   'er_34032.html\">Nick Castellanos</a> was injured while' + \
                   ' running the bases.  The Diagnosis: sprained ankle. Th' + \
                   'is is a day-to-day injury expected to last 5 days.'
        self.assertEqual(actual, expected)

    def test_death__with_true(self):
        plugin = self.create_plugin(_data())
        plugin.tables = _table_new
        value = plugin._death()
        self.assertTrue(value)

    def test_death__with_false(self):
        plugin = self.create_plugin(_data())
        plugin.tables = _table_old
        value = plugin._death()
        self.assertFalse(value)

    @mock.patch('plugin.recap.recap.standings_table')
    def test_home(self, mock_standings):
        cols = [
            'class="position-relative text-truncate"',
            ' class="text-right w-55p"', ' class="text-right w-55p"',
            ' class="text-right w-55p"', ' class="text-right w-55p"'
        ]
        body = [['33', '0', '0', '-', '163'], ['34', '0', '0', '-', '163'],
                ['48', '0', '0', '-', '163'], ['57', '0', '0', '-', '163'],
                ['59', '0', '0', '-', '163']]
        standings_table = [
            table(
                hcols=cols,
                bcols=cols,
                head=['AL East', 'W', 'L', 'GB', 'M#'],
                body=body)
        ]
        mock_standings.return_value = standings_table

        plugin = self.create_plugin(_data())
        plugin.shadow['statsplus.offseason'] = False
        plugin.shadow['statsplus.postseason'] = False
        plugin.tables = _table_new

        value = plugin._home(date=_now)
        breadcrumbs = [{
            'href': '/fairylab/',
            'name': 'Home'
        }, {
            'href': '',
            'name': 'Recap'
        }]
        expected = {
            'breadcrumbs': breadcrumbs,
            'injuries': _injuries_table_new,
            'news': _news_table_new,
            'transactions': _transactions_table_new,
            'standings': standings_table
        }
        self.assertEqual(value, expected)

        mock_standings.assert_called_once_with(_standings)
        self.mock_open.assert_not_called()
        self.mock_handle.write.not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_money__with_true(self):
        plugin = self.create_plugin(_data())
        plugin.tables = _table_new
        value = plugin._money()
        self.assertTrue(value)

    def test_money__with_false(self):
        plugin = self.create_plugin(_data())
        plugin.tables = _table_old
        value = plugin._money()
        self.assertFalse(value)

    @mock.patch('plugin.recap.recap.os.listdir')
    @mock.patch('plugin.recap.recap.box_score')
    def test_standings(self, mock_box, mock_listdir):
        boxes = ['123', '456', '789']
        mock_listdir.return_value = [
            'game_box_{}.html'.format(b) for b in boxes
        ]
        box1 = {
            'away_record': '76-86',
            'away_team': 'T31',
            'home_record': '97-65',
            'home_team': 'T45',
            'ok': True
        }
        box2 = {
            'away_record': '77-85',
            'away_team': 'T32',
            'home_record': '70-92',
            'home_team': 'T44',
            'ok': True
        }
        box3 = {
            'away_record': '75-86',
            'away_team': 'T31',
            'home_record': '97-64',
            'home_team': 'T45',
            'ok': True
        }
        mock_box.side_effect = [box1, box2, box3]

        plugin = self.create_plugin(_data())
        plugin._standings()
        expected = {'31': '76-86', '32': '77-85', '44': '70-92', '45': '97-65'}
        self.assertEqual(plugin.data['standings'], expected)

        new = {'31': '76-86', '32': '77-85', '44': '70-92', '45': '97-65'}
        write = _data(standings=new)
        dpath = os.path.join(_root, 'resource/extract/box_scores')
        mock_listdir.assert_called_once_with(dpath)
        calls = [
            mock.call(os.path.join(dpath, 'game_box_{}.html'.format(b)))
            for b in boxes
        ]
        mock_box.assert_has_calls(calls)
        self.mock_open.assert_called_once_with(Recap._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch('plugin.recap.recap.open', create=True)
    def test_tables_internal__injuries(self, mock_open):
        injuries_new = '20220815\t<a href=\"../teams/team_57.html\">Tampa ' + \
                       'Bay Rays</a>: <a href=\"../players/player_1.html\"' + \
                       '>Zack Weiss</a> diagnosed with a strained hamstrin' + \
                       'g, will miss 8 months.\n20220817\t<a href=\"../tea' + \
                       'ms/team_39.html\">Colorado Rockies</a>: RF <a href' + \
                       '=\"../players/player_24198.html\">Eddie Hoffman</a' + \
                       '> was injured being hit by a pitch.  The Diagnosis' + \
                       ': bruised knee. This is a day-to-day injury expect' + \
                       'ed to last 5 days.\n20220817\t<a href=\"../teams/t' + \
                       'eam_47.html\">Minnesota Twins</a>: 1B <a href=\"..' + \
                       '/players/player_34032.html\">Nick Castellanos</a> ' + \
                       'was injured while running the bases.  The Diagnosi' + \
                       's: sprained ankle. This is a day-to-day injury exp' + \
                       'ected to last 5 days.'
        injuries_old = '20220815\t<a href=\"../teams/team_44.html\">Los An' + \
                       'geles Angels</a>: CF <a href=\"../players/player_0' + \
                       '.html\">Alex Aristy</a> was injured while running ' + \
                       'the bases.  The Diagnosis: knee inflammation. He\'' + \
                       's expected to miss about 3 weeks.'
        injuries = '\n'.join([injuries_old, injuries_new])
        mo = mock.mock_open(read_data=injuries)
        mock_open.side_effect = [mo.return_value]

        now = {'injuries': ''}
        then = {'injuries': _injuries_encoded_old}
        plugin = self.create_plugin(_data(now=now, then=then))
        actual = plugin._tables_internal('injuries')
        expected = _injuries_table_new
        self.assertEqual(actual, expected)

        dpath = os.path.join(_root, 'resource/extract/leagues/{}.txt')
        mock_open.assert_called_once_with(dpath.format('injuries'), 'r')
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()
        self.assertEqual(plugin.data['now']['injuries'], _injuries_encoded_new)

    @mock.patch('plugin.recap.recap.open', create=True)
    def test_tables_internal__news(self, mock_open):
        news_new = '20220815\t<a href=\"../teams/team_42.html\">Houston As' + \
                   'tros</a>: <a href=\"../players/player_39044.html\">Mar' + \
                   'k Appel</a> pitches a 2-hit shutout against the <a hre' + \
                   'f=\"../teams/team_44.html\">Los Angeles Angels</a> wit' + \
                   'h 8 strikeouts and 0 BB allowed!\n20220818\t<a href=\"' + \
                   '../teams/team_39.html\">Colorado Rockies</a>: <a href=' + \
                   '\"../players/player_30965.html\">Spencer Taylorr</a> g' + \
                   'ot suspended 3 games after ejection following a brawl.' + \
                   '\n20220818\t<a href=\"../teams/team_41.html\">Miami Ma' + \
                   'rlins</a>: <a href=\"../players/player_131.html\">Jake' + \
                   ' Ehret</a> got suspended 3 games after ejection follow' + \
                   'ing a brawl.'
        news_old = '20220815\t<a href=\"../teams/team_57.html\">Tampa Bay ' + \
                   'Rays</a>: <a href=\"../players/player_27.html\">A.J. R' + \
                   'eed</a> got suspended 4 games after ejection following' + \
                   ' arguing a strike call.'
        news = '\n'.join([news_old, news_new])
        mo = mock.mock_open(read_data=news)
        mock_open.side_effect = [mo.return_value]

        now = {'news': ''}
        then = {'news': _news_encoded_old}
        plugin = self.create_plugin(_data(now=now, then=then))
        actual = plugin._tables_internal('news')
        expected = _news_table_new
        self.assertEqual(actual, expected)

        dpath = os.path.join(_root, 'resource/extract/leagues/{}.txt')
        mock_open.assert_called_once_with(dpath.format('news'), 'r')
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()
        self.assertEqual(plugin.data['now']['news'], _news_encoded_new)

    @mock.patch('plugin.recap.recap.open', create=True)
    def test_tables_internal__transactions(self, mock_open):
        _transactions_new = '20220815\t<a href=\"../teams/team_33.html\">B' + \
                            'altimore Orioles</a>: Placed C <a href=\"../p' + \
                            'layers/player_1439.html\">Evan Skoug</a> on t' + \
                            'he active roster.\n\n20220815\t<a href=\"../t' + \
                            'eams/team_33.html\">Baltimore Orioles</a>: Ac' + \
                            'tivated C <a href=\"../players/player_1439.ht' + \
                            'ml\">Evan Skoug</a> from the disabled list.\n' + \
                            '\n20220815\t<a href=\"../teams/team_33.html\"' + \
                            '>Baltimore Orioles</a>: Placed C <a href=\"..' + \
                            '/players/player_31093.html\">Salvador Perez</' + \
                            'a> on waivers.\n\n20220815\t<a href="../teams' + \
                            '/team_43.html">Kansas City Royals</a>: Signed' + \
                            ' C <a href="../players/player_29806.html">Tho' + \
                            'mas Dillard</a> to a 7-year contract extensio' + \
                            'n worth a total of $119,640,000.\n'
        _transactions_old = '20220815\t<a href=\"../teams/team_33.html\">B' + \
                            'altimore Orioles</a>: Placed 2B <a href=\"../' + \
                            'players/player_292.html\">Austin Slater</a> o' + \
                            'n the 7-day disabled list, retroactive to 08/' + \
                            '12/2022.\n'
        trans = '\n'.join([_transactions_old, _transactions_new])
        mo = mock.mock_open(read_data=trans)
        mock_open.side_effect = [mo.return_value]

        now = {'transactions': ''}
        then = {'transactions': _transactions_encoded_old}
        plugin = self.create_plugin(_data(now=now, then=then))
        actual = plugin._tables_internal('transactions')
        expected = _transactions_table_new
        self.assertEqual(actual, expected)

        dpath = os.path.join(_root, 'resource/extract/leagues/{}.txt')
        mock_open.assert_called_once_with(dpath.format('transactions'), 'r')
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()
        self.assertEqual(plugin.data['now']['transactions'],
                         _transactions_encoded_new)


if __name__ in ['__main__', 'plugin.recap.recap_test']:
    _main = __name__ == '__main__'
    _pkg = 'plugin.recap'
    _pth = 'plugin/recap'
    main(RecapTest, Recap, _pkg, _pth, {}, _main, date=_now, e=_env)
