#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/core/response', '', _path))
from core.notify.notify import Notify  # noqa
from core.response.response import Response  # noqa
from core.shadow.shadow import Shadow  # noqa
from core.task.task import Task  # noqa


class ResponseTest(unittest.TestCase):
    def test_init__empty(self):
        response = Response()
        self.assertEqual(response.notify, [])
        self.assertEqual(response.shadow, [])
        self.assertEqual(response.task, [])

    def test_init__notify_invalid_type(self):
        with self.assertRaises(TypeError):
            Response(notify=Notify.BASE)

    def test_init__notify_invalid_element_value(self):
        with self.assertRaises(ValueError):
            Response(notify=[1])

    def test_init__notify_valid(self):
        notify = Notify.BASE
        response = Response(notify=[notify])
        self.assertEqual(response.notify, [notify])
        self.assertEqual(response.shadow, [])
        self.assertEqual(response.task, [])

    def test_init__shadow_invalid_type(self):
        with self.assertRaises(TypeError):
            Response(shadow=Shadow(destination='foo', key='plugin.bar'))

    def test_init__shadow_invalid_element_value(self):
        with self.assertRaises(ValueError):
            Response(shadow=[1])

    def test_init__shadow_valid(self):
        shadow = Shadow(destination='foo', key='plugin.bar')
        response = Response(shadow=[shadow])
        self.assertEqual(response.notify, [])
        self.assertEqual(response.shadow, [shadow])
        self.assertEqual(response.task, [])

    def test_init__task_invalid_type(self):
        with self.assertRaises(TypeError):
            Response(task=Task(target='foo'))

    def test_init__task_invalid_element_value(self):
        with self.assertRaises(ValueError):
            Response(task=[1])

    def test_init__task_valid(self):
        task = Task(target='foo')
        response = Response(task=[task])
        self.assertEqual(response.notify, [])
        self.assertEqual(response.shadow, [])
        self.assertEqual(response.task, [task])

    def test_append_notify__invalid_element_value(self):
        response = Response()
        with self.assertRaises(ValueError):
            response.append_notify(1)

    def test_append_notify__valid(self):
        notify = Notify.BASE
        response = Response()
        response.append_notify(notify)
        self.assertEqual(response.notify, [notify])
        self.assertEqual(response.shadow, [])
        self.assertEqual(response.task, [])

    def test_append_shadow__invalid_element_value(self):
        response = Response()
        with self.assertRaises(ValueError):
            response.append_shadow(1)

    def test_append_shadow__valid(self):
        shadow = Shadow(destination='foo', key='plugin.bar')
        response = Response()
        response.append_shadow(shadow)
        self.assertEqual(response.notify, [])
        self.assertEqual(response.shadow, [shadow])
        self.assertEqual(response.task, [])

    def test_append_task__invalid_element_value(self):
        response = Response()
        with self.assertRaises(ValueError):
            response.append_task(1)

    def test_append_task__valid(self):
        task = Task(target='foo')
        response = Response()
        response.append_task(task)
        self.assertEqual(response.notify, [])
        self.assertEqual(response.shadow, [])
        self.assertEqual(response.task, [task])


if __name__ == '__main__':
    unittest.main()
