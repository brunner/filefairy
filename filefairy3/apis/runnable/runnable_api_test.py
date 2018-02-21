#!/usr/bin/env python

from runnable_api import RunnableApi

import unittest


class FakeRunnable(RunnableApi):
    def __init__(self):
        super(FakeRunnable, self).__init__()

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
