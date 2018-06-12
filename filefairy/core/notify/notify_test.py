#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/core/notify', '', _path))
from core.notify.notify import Notify  # noqa


class NotifyTest(unittest.TestCase):
    def test_enum(self):
        self.assertEqual(Notify.BASE, Notify(1))
        self.assertEqual(Notify.EXPORTS_EMAILS, Notify(2))
        self.assertEqual(Notify.FAIRYLAB_DAY, Notify(3))
        self.assertEqual(Notify.LEAGUEFILE_DOWNLOAD, Notify(4))
        self.assertEqual(Notify.LEAGUEFILE_FINISH, Notify(5))
        self.assertEqual(Notify.LEAGUEFILE_START, Notify(6))
        self.assertEqual(Notify.LEAGUEFILE_YEAR, Notify(7))
        self.assertEqual(Notify.STATSPLUS_SIM, Notify(8))
        self.assertEqual(Notify.OTHER, Notify(9))


if __name__ == '__main__':
    unittest.main()
