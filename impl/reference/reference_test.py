#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for reference.py."""

import os
import re
import sys
import unittest.mock as mock
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.extend((_path, re.sub(r'/impl/reference', '', _path)))

from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.jinja2_.jinja2_ import env  # noqa
from common.json_.json_ import dumps  # noqa
from common.test.test import Test  # noqa
from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa
from impl.reference.reference import Reference  # noqa

ENV = env()

DATE_10260602 = datetime_datetime_pst(1985, 10, 26, 6, 2, 30)
DATE_10260604 = datetime_datetime_pst(1985, 10, 26, 6, 4)

PLAYERS = {'P123': 'T31 1 L R Jim Alfa', 'P456': 'T32 42 R L Jim Beta'}

STATSPLUS_LINK = 'https://statsplus.net/oblootp/reports/news/html'
STATSPLUS_PLAYERS = os.path.join(STATSPLUS_LINK, 'players')


def _data(players=None):
    if players is None:
        players = {}
    return {'players': players}


def _statsplus_player_page(num):
    return os.path.join(STATSPLUS_PLAYERS, 'player_{}.html'.format(num))


class ReferenceTest(Test):
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

    def create_reference(self, data, warnings=None):
        self.init_mocks(data)
        reference = Reference(date=DATE_10260602, e=ENV)

        self.mock_open.assert_called_once_with(Reference._data(), 'r')
        self.assertNotCalled(self.mock_handle.write)
        self.assertEqual(reference.data, data)

        self.reset_mocks()
        self.init_mocks(data)

        if warnings:
            reference.warnings = warnings

        return reference

    def test_reload_data(self):
        reference = self.create_reference(_data())
        actual = reference._reload_data(date=DATE_10260602)
        expected = {'statslab': ['parse_player']}
        self.assertEqual(actual, expected)

        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    @mock.patch.object(Reference, '_refresh')
    def test_notify__fairylab_day(self, mock_refresh):
        reference = self.create_reference(_data())
        response = reference._notify_internal(notify=Notify.FILEFAIRY_DAY)
        self.assertEqual(response, Response())

        mock_refresh.assert_called_once_with()
        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    @mock.patch.object(Reference, '_refresh')
    def test_notify__other(self, mock_refresh):
        reference = self.create_reference(_data())
        response = reference._notify_internal(notify=Notify.OTHER)
        self.assertEqual(response, Response())

        self.assertNotCalled(mock_refresh, self.mock_open,
                             self.mock_handle.write)

    def test_get_bats(self):
        reference = self.create_reference(_data(players=PLAYERS))
        inputs = [('123', 'L'), ('456', 'R'), ('789', 'R')]
        for num, expected in inputs:
            actual = reference._get_bats(num)
            self.assertEqual(actual, expected)

        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    def test_get_name(self):
        reference = self.create_reference(_data(players=PLAYERS))
        inputs = [('123', 'Jim Alfa'), ('456', 'Jim Beta'),
                  ('789', 'Jim Unknown')]
        for num, expected in inputs:
            actual = reference._get_name(num)
            self.assertEqual(actual, expected)

        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    def test_get_number(self):
        reference = self.create_reference(_data(players=PLAYERS))
        inputs = [('123', '1'), ('456', '42'), ('789', '0')]
        for num, expected in inputs:
            actual = reference._get_number(num)
            self.assertEqual(actual, expected)

        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    def test_get_team(self):
        reference = self.create_reference(_data(players=PLAYERS))
        inputs = [('123', 'T31'), ('456', 'T32'), ('789', 'T??')]
        for num, expected in inputs:
            actual = reference._get_team(num)
            self.assertEqual(actual, expected)

        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    def test_get_throws(self):
        reference = self.create_reference(_data(players=PLAYERS))
        inputs = [('123', 'R'), ('456', 'L'), ('789', 'R')]
        for num, expected in inputs:
            actual = reference._get_throws(num)
            self.assertEqual(actual, expected)

        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    @mock.patch.object(Reference, '_call')
    def test_parse__different(self, mock_call):
        mock_call.return_value = 'T32 1 L R Jim Alfa'

        players = {'P123': 'T31 1 L R Jim Alfa'}
        reference = self.create_reference(_data(players=players))
        reference._parse('P123')

        link = _statsplus_player_page('123')
        players = {'P123': 'T32 1 L R Jim Alfa'}
        write = _data(players=players)
        mock_call.assert_called_once_with('parse_player', (link, ))
        self.mock_open.assert_called_once_with(Reference._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch.object(Reference, '_call')
    def test_parse__none(self, mock_call):
        mock_call.return_value = None

        players = {'P123': 'T31 1 L R Jim Alfa'}
        reference = self.create_reference(_data(players=players))
        reference._parse('P123')

        link = _statsplus_player_page('123')
        mock_call.assert_called_once_with('parse_player', (link, ))
        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    @mock.patch.object(Reference, '_call')
    def test_parse__same(self, mock_call):
        mock_call.return_value = 'T31 1 L R Jim Alfa'

        players = {'P123': 'T31 1 L R Jim Alfa'}
        reference = self.create_reference(_data(players=players))
        reference._parse('P123')

        link = _statsplus_player_page('123')
        mock_call.assert_called_once_with('parse_player', (link, ))
        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    @mock.patch.object(Reference, '_parse')
    def test_put(self, mock_parse):
        reference = self.create_reference(_data(players=PLAYERS))
        reference._put(['123', '789'])

        mock_parse.assert_called_once_with('P789')
        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    @mock.patch.object(Reference, '_parse')
    def test_refresh(self, mock_parse):
        reference = self.create_reference(_data(players=PLAYERS))
        reference._refresh()

        mock_parse.assert_has_calls([mock.call('P123'), mock.call('P456')])
        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    def test_sub(self):
        reference = self.create_reference(_data(players=PLAYERS))
        actual = reference._sub('P123 (1-0, 0.00 ERA)')
        expected = 'Jim Alfa (1-0, 0.00 ERA)'
        self.assertEqual(actual, expected)

        self.assertNotCalled(self.mock_open, self.mock_handle.write)


if __name__ == '__main__':
    unittest.main()
