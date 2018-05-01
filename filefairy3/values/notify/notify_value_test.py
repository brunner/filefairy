#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/values/notify', '', _path))
from values.notify.notify_value import NotifyValue  # noqa


class NotifyValueTest(unittest.TestCase):
    def test_enum(self):
        self.assertEqual(NotifyValue.BASE, NotifyValue(1))
        self.assertEqual(NotifyValue.DOWNLOAD_FINISH, NotifyValue(2))
        self.assertEqual(NotifyValue.EXPORTS_EMAILS, NotifyValue(3))
        self.assertEqual(NotifyValue.FAIRYLAB_DAY, NotifyValue(4))
        self.assertEqual(NotifyValue.LEAGUEFILE_FINISH, NotifyValue(5))
        self.assertEqual(NotifyValue.LEAGUEFILE_START, NotifyValue(6))
        self.assertEqual(NotifyValue.STATSPLUS_SIM, NotifyValue(7))
        self.assertEqual(NotifyValue.OTHER, NotifyValue(8))


if __name__ == '__main__':
    unittest.main()
