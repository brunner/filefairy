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

    @mock.patch.object(Reference, '_parse')
    def test_notify__fairylab_day(self, mock_parse):
        reference = self.create_reference(_data(players=PLAYERS))
        response = reference._notify_internal(notify=Notify.FILEFAIRY_DAY)
        self.assertEqual(response, Response())

        mock_parse.assert_called_once_with(['P123', 'P456'])
        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    @mock.patch.object(Reference, '_parse')
    def test_notify__other(self, mock_parse):
        reference = self.create_reference(_data())
        response = reference._notify_internal(notify=Notify.OTHER)
        self.assertEqual(response, Response())

        self.assertNotCalled(mock_parse, self.mock_open,
                             self.mock_handle.write)

    def test_get_bats(self):
        reference = self.create_reference(_data(players=PLAYERS))
        inputs = [('P123', 'L'), ('P456', 'R'), ('P789', 'R')]
        for num, expected in inputs:
            actual = reference._get(num, 2, 'R')
            self.assertEqual(actual, expected)

        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    def test_get_name(self):
        reference = self.create_reference(_data(players=PLAYERS))
        inputs = [('P123', 'Jim Alfa'), ('P456', 'Jim Beta'),
                  ('P789', 'Jim Unknown')]
        for num, expected in inputs:
            actual = reference._get(num, 4, 'Jim Unknown')
            self.assertEqual(actual, expected)

        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    def test_get_number(self):
        reference = self.create_reference(_data(players=PLAYERS))
        inputs = [('P123', '1'), ('P456', '42'), ('P789', '0')]
        for num, expected in inputs:
            actual = reference._get(num, 1, '0')
            self.assertEqual(actual, expected)

        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    def test_get_team(self):
        reference = self.create_reference(_data(players=PLAYERS))
        inputs = [('P123', 'T31'), ('P456', 'T32'), ('P789', 'T??')]
        for num, expected in inputs:
            actual = reference._get(num, 0, 'T??')
            self.assertEqual(actual, expected)

        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    def test_get_throws(self):
        reference = self.create_reference(_data(players=PLAYERS))
        inputs = [('P123', 'R'), ('P456', 'L'), ('P789', 'R')]
        for num, expected in inputs:
            actual = reference._get(num, 3, 'R')
            self.assertEqual(actual, expected)

        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    @mock.patch.object(Reference, '_call')
    def test_parse__different(self, mock_call):
        mock_call.return_value = 'T32 1 L R Jim Alfa'

        players = {'P123': 'T31 1 L R Jim Alfa'}
        reference = self.create_reference(_data(players=players))
        reference._parse(['P123'])

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
        reference._parse(['P123'])

        link = _statsplus_player_page('123')
        write = _data()
        mock_call.assert_called_once_with('parse_player', (link, ))
        self.mock_open.assert_called_once_with(Reference._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch.object(Reference, '_call')
    def test_parse__same(self, mock_call):
        mock_call.return_value = 'T31 1 L R Jim Alfa'

        players = {'P123': 'T31 1 L R Jim Alfa'}
        reference = self.create_reference(_data(players=players))
        reference._parse(['P123'])

        link = _statsplus_player_page('123')
        mock_call.assert_called_once_with('parse_player', (link, ))
        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    @mock.patch.object(Reference, '_parse')
    def test_put(self, mock_parse):
        reference = self.create_reference(_data(players=PLAYERS))
        reference._put(['P123', 'P789'])

        mock_parse.assert_called_once_with(['P789'])
        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    def test_sub(self):
        reference = self.create_reference(_data(players=PLAYERS))

        def _repl(m):
            return reference._get(m.group(0), 4, 'Jim Unknown')

        actual = reference._sub(_repl, 'P123 (1-0, 0.00 ERA)')
        expected = 'Jim Alfa (1-0, 0.00 ERA)'
        self.assertEqual(actual, expected)

        self.assertNotCalled(self.mock_open, self.mock_handle.write)


if __name__ == '__main__':
    unittest.main()
