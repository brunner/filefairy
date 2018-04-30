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
        self.assertEqual(NotifyValue.NONE, NotifyValue(0))
        self.assertEqual(NotifyValue.BASE, NotifyValue(1))
        self.assertEqual(NotifyValue.EXPORT, NotifyValue(2))
        self.assertEqual(NotifyValue.SIM, NotifyValue(3))
        self.assertEqual(NotifyValue.UPLOAD, NotifyValue(4))
        self.assertEqual(NotifyValue.FILE, NotifyValue(5))
        self.assertEqual(NotifyValue.DOWNLOAD, NotifyValue(6))


if __name__ == '__main__':
    unittest.main()
