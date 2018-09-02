#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/plugin/gameday', '', _path))
from core.notify.notify import Notify  # noqa
from core.response.response import Response  # noqa
from plugin.gameday.gameday import Gameday  # noqa
from util.jinja2_.jinja2_ import env  # noqa
from util.json_.json_ import dumps  # noqa
from util.test.test import Test  # noqa
from util.test.test import main  # noqa

_env = env()
_now = datetime.datetime(1985, 10, 27, 0, 0, 0)
_then = datetime.datetime(1985, 10, 26, 0, 2, 30)


def _data():
    return {}


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

    @mock.patch.object(Gameday, '_game')
    def test_render(self, mock_game):
        game = {'breadcrumbs': []}
        mock_game.return_value = game

        plugin = self.create_plugin(_data())
        response = plugin._render_internal(date=_now)
        index = 'gameday/diamondbacks/index.html'
        self.assertEqual(response,
                         [(index, 'diamondbacks', 'game.html', game)])

        mock_game.assert_called_once_with('Diamondbacks', date=_now)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    def test_run(self):
        plugin = self.create_plugin(_data())
        response = plugin._run_internal(date=_then)
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    @mock.patch.object(Gameday, '_render')
    def test_setup(self, mock_render):
        plugin = self.create_plugin(_data())
        response = plugin._setup_internal(date=_then)
        self.assertEqual(response, Response())

        mock_render.assert_called_once_with(date=_then)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    def test_shadow(self):
        plugin = self.create_plugin(_data())
        value = plugin._shadow_internal()
        self.assertEqual(value, [])

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()

    def test_game__with_empty(self):
        plugin = self.create_plugin(_data())
        actual = plugin._game('Diamondbacks', date=_now)
        breadcrumbs = [{
            'href': '/',
            'name': 'Home'
        }, {
            'href': '/gameday/',
            'name': 'Gameday'
        }, {
            'href': '',
            'name': 'Diamondbacks'
        }]
        expected = {'breadcrumbs': breadcrumbs}
        self.assertEqual(actual, expected)


if __name__ in ['__main__', 'plugin.gameday.gameday_test']:
    _main = __name__ == '__main__'
    _pkg = 'plugin.gameday'
    _pth = 'plugin/gameday'
    main(GamedayTest, Gameday, _pkg, _pth, {}, _main, date=_now, e=_env)
