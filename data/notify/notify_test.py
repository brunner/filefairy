#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for notify.py."""

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/data/notify', '', _path))

from data.notify.notify import Notify  # noqa


class NotifyTest(unittest.TestCase):
    def test_enum(self):
        self.assertEqual(Notify.BASE, Notify(1))
        self.assertEqual(Notify.EXPORTS_EMAILS, Notify(2))
        self.assertEqual(Notify.FILEFAIRY_DAY, Notify(3))
        self.assertEqual(Notify.FILEFAIRY_DEPLOY, Notify(4))
        self.assertEqual(Notify.LEAGUEFILE_DOWNLOAD, Notify(5))
        self.assertEqual(Notify.LEAGUEFILE_FINISH, Notify(6))
        self.assertEqual(Notify.LEAGUEFILE_START, Notify(7))
        self.assertEqual(Notify.LEAGUEFILE_YEAR, Notify(8))
        self.assertEqual(Notify.STATSPLUS_SIM, Notify(9))
        self.assertEqual(Notify.OTHER, Notify(10))


if __name__ == '__main__':
    unittest.main()
