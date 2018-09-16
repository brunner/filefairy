#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugin/gameday', '', _path)
sys.path.append(_root)
from core.notify.notify import Notify  # noqa
from core.response.response import Response  # noqa
from plugin.gameday.gameday import Gameday  # noqa
from util.component.component import table  # noqa
from util.datetime_.datetime_ import datetime_datetime_pst  # noqa
from util.jinja2_.jinja2_ import env  # noqa
from util.json_.json_ import dumps  # noqa
from util.test.test import Test  # noqa
from util.test.test import main  # noqa

_env = env()
_fairylab_root = re.sub(r'/filefairy', '/fairylab/static', _root)
_game = {
    'breadcrumbs': [{
        'href': '/',
        'name': 'Fairylab'
    }, {
        'href': '/gameday/',
        'name': 'Gameday'
    }, {
        'href': '',
        'name': 'Diamondbacks at Dodgers, 10/09/2022'
    }],
    'inning': [
        table(
            clazz='border mt-3',
            head=['t1'],
            body=[['T31 batting - Pitching for T45 : LHP P101'],
                  ['Batting: SHB P102'], ['0-0: Ball'], ['P103 to second'],
                  ['0 run(s), 0 hit(s), 0 error(s), 0 left on base']])
    ]
}
_game_data = {
    'away_team':
    'T31',
    'date':
    '2022-10-09T00:00:00-07:00',
    'home_team':
    'T45',
    'inning': [{
        'id':
        't1',
        'intro':
        'T31 batting - Pitching for T45 : LHP P101',
        'outro':
        '0 run(s), 0 hit(s), 0 error(s), 0 left on base',
        'pitch': [{
            'before': ['Batting: SHB P102'],
            'result': '0-0: Ball',
            'after': ['P103 to second']
        }]
    }]
}
_now = datetime_datetime_pst(1985, 10, 27, 0, 0, 0)
_then = datetime_datetime_pst(1985, 10, 26, 0, 2, 30)


def _data(games=None):
    if games is None:
        games = []
    return {'games': games}


class GamedayTest(unittest.TestCase):
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

    def create_plugin(self, data):
        self.init_mocks(data)
        plugin = Gameday(date=_now, e=_env)

        self.mock_open.assert_called_once_with(Gameday._data(), 'r')
        self.mock_handle.write.assert_not_called()

        self.reset_mocks()
        self.init_mocks(data)

        return plugin

    def test_notify(self):
        plugin = self.create_plugin(_data())
        response = plugin._notify_internal(notify=Notify.OTHER)
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    def test_on_message(self):
        plugin = self.create_plugin(_data())
        response = plugin._on_message_internal()
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    maxDiff = None

    @mock.patch('plugin.gameday.gameday.recreate')
    @mock.patch('plugin.gameday.gameday.open')
    def test_render(self, mock_open, mock_recreate):
        mo = mock.mock_open(read_data=dumps(_game_data))
        mock_open.side_effect = [mo.return_value]

        plugin = self.create_plugin(_data(games=['2998']))
        response = plugin._render_internal(date=_now)
        index = 'gameday/2998/index.html'
        subtitle = 'Diamondbacks at Dodgers, 10/09/2022'
        self.assertEqual(response, [(index, subtitle, 'game.html', _game)])

        mock_open.assert_called_once_with(
            _root + '/resource/games/game_2998.json', 'r')
        mock_recreate.assert_called_once_with(_fairylab_root + '/gameday/')
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(Gameday, '_check_games')
    def test_run__with_check_false(self, mock_check):
        mock_check.return_value = False

        plugin = self.create_plugin(_data())
        response = plugin._run_internal(date=_then)
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(Gameday, '_check_games')
    def test_run__with_check_true(self, mock_check):
        mock_check.return_value = True

        plugin = self.create_plugin(_data())
        response = plugin._run_internal(date=_then)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(Gameday, '_check_games')
    def test_setup(self, mock_check):
        plugin = self.create_plugin(_data())
        response = plugin._setup_internal(date=_then)
        self.assertEqual(response, Response())

        mock_check.assert_called_once_with(date=_then)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    def test_shadow(self):
        plugin = self.create_plugin(_data())
        value = plugin._shadow_internal()
        self.assertEqual(value, [])

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()


if __name__ in ['__main__', 'plugin.gameday.gameday_test']:
    _main = __name__ == '__main__'
    _pkg = 'plugin.gameday'
    _pth = 'plugin/gameday'
    main(GamedayTest, Gameday, _pkg, _pth, {}, _main, date=_now, e=_env)
