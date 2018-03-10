#!/usr/bin/env python

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/apis/runnable', '', _path))
from apis.runnable.runnable_api import RunnableApi  # noqa


class FakeRunnable(RunnableApi):
    def __init__(self, **kwargs):
        super(FakeRunnable, self).__init__(**kwargs)

    def _run_internal(self, **kwargs):
        return dict(kwargs, m='internal')


class RunnableApiTest(unittest.TestCase):
    def test_run(self):
        runnable = FakeRunnable()
        actual = runnable._run_internal()
        expected = {'m': 'internal'}
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
