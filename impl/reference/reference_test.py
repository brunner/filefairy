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
from common.json_.json_ import dumps  # noqa
from common.test.test import Test  # noqa
from impl.reference.reference import Reference  # noqa
from types_.notify.notify import Notify  # noqa
from types_.response.response import Response  # noqa

DATE_10260602 = datetime_datetime_pst(1985, 10, 26, 6, 2, 30)
DATE_10260604 = datetime_datetime_pst(1985, 10, 26, 6, 4)

PLAYERS = {'P123': 'T31 1 L R Jim Alfa', 'P456': 'T32 42 R L Jim Beta'}

STATSPLUS_LINK = 'https://statsplus.net/oblootp/reports/news/html'
STATSPLUS_PLAYERS = os.path.join(STATSPLUS_LINK, 'players')


def create_statsplus_player_page(num):
    return os.path.join(STATSPLUS_PLAYERS, 'player_{}.html'.format(num))


class ReferenceTest(Test):
    def setUp(self):
        open_patch = mock.patch('common.io_.io_.open', create=True)
        self.addCleanup(open_patch.stop)
        self.open_ = open_patch.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.open_handle_ = mo()
        self.open_.side_effect = [mo.return_value]

    def reset_mocks(self):
        self.open_handle_.write.reset_mock()

    def create_reference(self, data, warnings=None):
        self.init_mocks(data)
        reference = Reference(date=DATE_10260602)

        self.assertEqual(reference.data, data)

        self.reset_mocks()
        self.init_mocks(data)

        if warnings:
            reference.warnings = warnings

        return reference

    @mock.patch.object(Reference, 'parse_players')
    def test_notify__fairylab_day(self, parse_players_):
        data = {'players': PLAYERS}
        reference = self.create_reference(data)
        response = reference._notify_internal(notify=Notify.FILEFAIRY_DAY)
        self.assertEqual(response, Response())

        parse_players_.assert_called_once_with(['P123', 'P456'])
        self.assertNotCalled(self.open_handle_.write)

    @mock.patch.object(Reference, 'parse_players')
    def test_notify__other(self, parse_players_):
        data = {'players': {}}
        reference = self.create_reference(data)
        response = reference._notify_internal(notify=Notify.OTHER)
        self.assertEqual(response, Response())

        self.assertNotCalled(parse_players_, self.open_handle_.write)

    def test_get_attribute__bats(self):
        data = {'players': PLAYERS}
        reference = self.create_reference(data)
        inputs = [('P123', 'L'), ('P456', 'R'), ('P789', 'R')]
        for num, expected in inputs:
            actual = reference.get_attribute(num, 2, 'R')
            self.assertEqual(actual, expected)

        self.assertNotCalled(self.open_handle_.write)

    def test_get_attribute__name(self):
        data = {'players': PLAYERS}
        reference = self.create_reference(data)
        inputs = [('P123', 'Jim Alfa'), ('P456', 'Jim Beta'),
                  ('P789', 'Jim Unknown')]
        for num, expected in inputs:
            actual = reference.get_attribute(num, 4, 'Jim Unknown')
            self.assertEqual(actual, expected)

        self.assertNotCalled(self.open_handle_.write)

    def test_get_attribute__number(self):
        data = {'players': PLAYERS}
        reference = self.create_reference(data)
        inputs = [('P123', '1'), ('P456', '42'), ('P789', '0')]
        for num, expected in inputs:
            actual = reference.get_attribute(num, 1, '0')
            self.assertEqual(actual, expected)

        self.assertNotCalled(self.open_handle_.write)

    def test_get_attribute__team(self):
        data = {'players': PLAYERS}
        reference = self.create_reference(data)
        inputs = [('P123', 'T31'), ('P456', 'T32'), ('P789', 'T30')]
        for num, expected in inputs:
            actual = reference.get_attribute(num, 0, 'T30')
            self.assertEqual(actual, expected)

        self.assertNotCalled(self.open_handle_.write)

    def test_get_attribute__throws(self):
        data = {'players': PLAYERS}
        reference = self.create_reference(data)
        inputs = [('P123', 'R'), ('P456', 'L'), ('P789', 'R')]
        for num, expected in inputs:
            actual = reference.get_attribute(num, 3, 'R')
            self.assertEqual(actual, expected)

        self.assertNotCalled(self.open_handle_.write)

    @mock.patch('impl.reference.reference.call_service')
    def test_parse_players__different(self, call_service_):
        call_service_.return_value = 'T32 1 L R Jim Alfa'

        players = {'P123': 'T31 1 L R Jim Alfa'}
        data = {'players': players}
        reference = self.create_reference(data)
        reference.parse_players(['P123'])

        link = create_statsplus_player_page('123')
        players = {'P123': 'T32 1 L R Jim Alfa'}
        write = {'players': players}
        call_service_.assert_called_once_with('statslab', 'parse_player',
                                              (link, ))
        self.open_handle_.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch('impl.reference.reference.call_service')
    def test_parse_players__none(self, call_service_):
        call_service_.return_value = None

        players = {'P123': 'T31 1 L R Jim Alfa'}
        data = {'players': players}
        reference = self.create_reference(data)
        reference.parse_players(['P123'])

        link = create_statsplus_player_page('123')
        write = {'players': {}}
        call_service_.assert_called_once_with('statslab', 'parse_player',
                                              (link, ))
        self.open_handle_.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch('impl.reference.reference.call_service')
    def test_parse_players__same(self, call_service_):
        call_service_.return_value = 'T31 1 L R Jim Alfa'

        players = {'P123': 'T31 1 L R Jim Alfa'}
        data = {'players': players}
        reference = self.create_reference(data)
        reference.parse_players(['P123'])

        link = create_statsplus_player_page('123')
        call_service_.assert_called_once_with('statslab', 'parse_player',
                                              (link, ))
        self.assertNotCalled(self.open_handle_.write)

    @mock.patch.object(Reference, 'parse_players')
    def test_put_players(self, parse_players_):
        data = {'players': PLAYERS}
        reference = self.create_reference(data)
        reference.put_players(['P123', 'P789'])

        parse_players_.assert_called_once_with(['P789'])
        self.assertNotCalled(self.open_handle_.write)

    def test_substitute(self):
        data = {'players': PLAYERS}
        reference = self.create_reference(data)

        def _repl(m):
            return reference.get_attribute(m.group(0), 4, 'Jim Unknown')

        actual = reference.substitute(_repl, 'P123 (1-0, 0.00 ERA)')
        expected = 'Jim Alfa (1-0, 0.00 ERA)'
        self.assertEqual(actual, expected)

        self.assertNotCalled(self.open_handle_.write)


if __name__ == '__main__':
    unittest.main()
