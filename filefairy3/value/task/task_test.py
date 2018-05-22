#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/value/task', '', _path))
from value.task.task import Task  # noqa


class TaskTest(unittest.TestCase):
    def test_init__empty(self):
        with self.assertRaises(ValueError):
            Task()

    def test_init__task_invalid(self):
        args = (True, False)
        kwargs = {'key': 'value'}
        with self.assertRaises(ValueError):
            Task(target=[1], args=args, kwargs=kwargs)

    def test_init__task_valid(self):
        mock_foo = mock.Mock()
        args = (True, False)
        kwargs = {'key': 'value'}
        task = Task(target=mock_foo, args=args, kwargs=kwargs)
        self.assertEqual(task.target, mock_foo)
        self.assertEqual(task.args, args)
        self.assertEqual(task.kwargs, kwargs)


if __name__ == '__main__':
    unittest.main()
