#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for notify.py."""

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/types_/notify', '', _path))

from types_.notify.notify import Notify  # noqa


class NotifyTest(unittest.TestCase):
    def test_enum(self):
        self.assertEqual(Notify.BASE, Notify(1))
        self.assertEqual(Notify.DOWNLOAD_FINISH, Notify(2))
        self.assertEqual(Notify.DOWNLOAD_YEAR, Notify(3))
        self.assertEqual(Notify.EXPORTS_EMAILS, Notify(4))
        self.assertEqual(Notify.FILEFAIRY_DAY, Notify(5))
        self.assertEqual(Notify.FILEFAIRY_DEPLOY, Notify(6))
        self.assertEqual(Notify.STATSPLUS_FINISH, Notify(7))
        self.assertEqual(Notify.STATSPLUS_PARSE, Notify(8))
        self.assertEqual(Notify.STATSPLUS_SAVE, Notify(9))
        self.assertEqual(Notify.STATSPLUS_START, Notify(10))
        self.assertEqual(Notify.UPLOAD_FINISH, Notify(11))
        self.assertEqual(Notify.OTHER, Notify(12))


if __name__ == '__main__':
    unittest.main()
