#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/values/notification', '', _path))
from values.notification.notification_value import NotificationValue  # noqa


class NotificationValueTest(unittest.TestCase):
    def test_enum(self):
        self.assertEqual(NotificationValue.NONE, NotificationValue(0))
        self.assertEqual(NotificationValue.BASE, NotificationValue(1))
        self.assertEqual(NotificationValue.EXPORT, NotificationValue(2))
        self.assertEqual(NotificationValue.SIM, NotificationValue(3))
        self.assertEqual(NotificationValue.UPLOAD, NotificationValue(4))
        self.assertEqual(NotificationValue.FILE, NotificationValue(5))
        self.assertEqual(NotificationValue.DOWNLOAD, NotificationValue(6))


if __name__ == '__main__':
    unittest.main()
