#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/values/response', '', _path))
from values.notification.notification_value import NotificationValue  # noqa
from values.response.response_value import ResponseValue  # noqa


class ResponseValueTest(unittest.TestCase):
    def test_init__empty(self):
        response = ResponseValue()
        self.assertEqual(response.notification, [])
        self.assertEqual(response.shadow, {})

    def test_init__notification_invalid_type(self):
        with self.assertRaises(TypeError):
            ResponseValue(notification=NotificationValue.BASE)

    def test_init__notification_invalid_element_value(self):
        with self.assertRaises(ValueError):
            ResponseValue(notification=[1])

    def test_init__notification_valid(self):
        response = ResponseValue(notification=[NotificationValue.BASE])
        self.assertEqual(response.notification, [NotificationValue.BASE])
        self.assertEqual(response.shadow, {})

    def test_init__shadow_invalid_type(self):
        with self.assertRaises(TypeError):
            ResponseValue(shadow='value')

    def test_init__shadow_invalid_key_value(self):
        with self.assertRaises(ValueError):
            ResponseValue(shadow={0: {'key': 'value'}})

    def test_init__shadow_invalid_value_value(self):
        with self.assertRaises(ValueError):
            ResponseValue(shadow={'plugin': 0})

    def test_init__shadow_valid(self):
        response = ResponseValue(shadow={'plugin': {'key': 'value'}})
        self.assertEqual(response.notification, [])
        self.assertEqual(response.shadow, {'plugin': {'key': 'value'}})


if __name__ == '__main__':
    unittest.main()
