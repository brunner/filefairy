#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/value/task', '', _path))
from value.task.task import Task  # noqa


class TaskTest(unittest.TestCase):
    def test_init__empty_target(self):
        with self.assertRaises(ValueError):
            Task()

    def test_init__empty_args(self):
        kwargs = {'key': 'value'}
        task = Task(target='foo', kwargs=kwargs)
        self.assertEqual(task.target, 'foo')
        self.assertEqual(task.args, tuple())
        self.assertEqual(task.kwargs, kwargs)

    def test_init__empty_kwargs(self):
        args = (True, False)
        task = Task(target='foo', args=args)
        self.assertEqual(task.target, 'foo')
        self.assertEqual(task.args, args)
        self.assertEqual(task.kwargs, dict())

    def test_init__task_invalid_target(self):
        args = (True, False)
        kwargs = {'key': 'value'}
        with self.assertRaises(ValueError):
            Task(target=[1], args=args, kwargs=kwargs)

    def test_init__task_invalid_args(self):
        kwargs = {'key': 'value'}
        with self.assertRaises(ValueError):
            Task(target='foo', args=[1], kwargs=kwargs)

    def test_init__task_invalid_kwargs(self):
        args = (True, False)
        with self.assertRaises(ValueError):
            Task(target='foo', args=args, kwargs=[1])

    def test_init__task_valid(self):
        args = (True, False)
        kwargs = {'key': 'value'}
        task = Task(target='foo', args=args, kwargs=kwargs)
        self.assertEqual(task.target, 'foo')
        self.assertEqual(task.args, args)
        self.assertEqual(task.kwargs, kwargs)


if __name__ == '__main__':
    unittest.main()
