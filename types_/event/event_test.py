#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for event.py."""

import logging
import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/types_/event', '', _path))

from types_.event.event import Event  # noqa


class EventTest(unittest.TestCase):
    def setUp(self):
        patch_log = mock.patch('types_.event.event._logger.log')
        self.addCleanup(patch_log.stop)
        self.mock_log = patch_log.start()

    def test_decode__args(self):
        actual = Event.decode('change_batter P24322')
        expected = (Event.CHANGE_BATTER, ['P24322'])
        self.assertEqual(actual, expected)

        self.mock_log.assert_not_called()

    def test_decode__exception(self):
        actual = Event.decode('other')
        expected = (None, [])
        self.assertEqual(actual, expected)

        self.mock_log.assert_called_once_with(
            logging.WARNING, 'Handled warning.', exc_info=True)

    def test_decode__member(self):
        actual = Event.decode('change_inning')
        expected = (Event.CHANGE_INNING, [])
        self.assertEqual(actual, expected)

        self.mock_log.assert_not_called()

    def test_encode__args(self):
        actual = Event.CHANGE_BATTER.encode('P24322')
        expected = 'change_batter P24322'
        self.assertEqual(actual, expected)

        self.mock_log.assert_not_called()

    def test_encode__member(self):
        actual = Event.CHANGE_INNING.encode()
        expected = 'change_inning'
        self.assertEqual(actual, expected)

        self.mock_log.assert_not_called()


if __name__ == '__main__':
    unittest.main()
