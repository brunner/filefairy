#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/value/response', '', _path))
from value.notify.notify import Notify  # noqa
from value.response.response import Response  # noqa


class ResponseTest(unittest.TestCase):
    def test_init__empty(self):
        response = Response()
        self.assertEqual(response.notify, [])
        self.assertEqual(response.shadow, {})

    def test_init__notify_invalid_type(self):
        with self.assertRaises(TypeError):
            Response(notify=Notify.BASE)

    def test_init__notify_invalid_element_value(self):
        with self.assertRaises(ValueError):
            Response(notify=[1])

    def test_init__notify_valid(self):
        response = Response(notify=[Notify.BASE])
        self.assertEqual(response.notify, [Notify.BASE])
        self.assertEqual(response.shadow, {})

    def test_init__shadow_invalid_type(self):
        with self.assertRaises(TypeError):
            Response(shadow='value')

    def test_init__shadow_invalid_key_value(self):
        with self.assertRaises(ValueError):
            Response(shadow={0: {'key': 'value'}})

    def test_init__shadow_invalid_value_value(self):
        with self.assertRaises(ValueError):
            Response(shadow={'plugin': 0})

    def test_init__shadow_valid(self):
        response = Response(shadow={'plugin': {'key': 'value'}})
        self.assertEqual(response.notify, [])
        self.assertEqual(response.shadow, {'plugin': {'key': 'value'}})

    def test_append_notify__invalid_element_value(self):
        response = Response()
        with self.assertRaises(ValueError):
            response.append_notify(1)

    def test_append_notify__valid(self):
        response = Response()
        response.append_notify(Notify.BASE)
        self.assertEqual(response.notify, [Notify.BASE])
        self.assertEqual(response.shadow, {})


if __name__ == '__main__':
    unittest.main()
