#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/values/response', '', _path))
from values.notify.notify_value import NotifyValue  # noqa
from values.response.response_value import ResponseValue  # noqa


class ResponseValueTest(unittest.TestCase):
    def test_init__empty(self):
        response = ResponseValue()
        self.assertEqual(response.notify, [])
        self.assertEqual(response.shadow, {})

    def test_init__notify_invalid_type(self):
        with self.assertRaises(TypeError):
            ResponseValue(notify=NotifyValue.BASE)

    def test_init__notify_invalid_element_value(self):
        with self.assertRaises(ValueError):
            ResponseValue(notify=[1])

    def test_init__notify_valid(self):
        response = ResponseValue(notify=[NotifyValue.BASE])
        self.assertEqual(response.notify, [NotifyValue.BASE])
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
        self.assertEqual(response.notify, [])
        self.assertEqual(response.shadow, {'plugin': {'key': 'value'}})

    def test_append_notify__invalid_element_value(self):
        response = ResponseValue()
        with self.assertRaises(ValueError):
            response.append_notify(1)

    def test_append_notify__valid(self):
        response = ResponseValue()
        response.append_notify(NotifyValue.BASE)
        self.assertEqual(response.notify, [NotifyValue.BASE])
        self.assertEqual(response.shadow, {})


if __name__ == '__main__':
    unittest.main()
