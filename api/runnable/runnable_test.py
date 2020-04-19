#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for messageable.py."""

import datetime
import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/api/runnable', '', _path))

from api.runnable.runnable import Runnable  # noqa
from common.jinja2_.jinja2_ import env  # noqa
from common.json_.json_ import dumps  # noqa
from types_.notify.notify import Notify  # noqa
from types_.response.response import Response  # noqa
from types_.shadow.shadow import Shadow  # noqa

ENV = env()

DATE_10260602 = datetime.datetime(1985, 10, 26, 6, 2, 30)
DATE_10270000 = datetime.datetime(1985, 10, 27)


class FakeRunnable(Runnable):
    def __init__(self, **kwargs):
        super(FakeRunnable, self).__init__(**kwargs)

    def _notify_internal(self, **kwargs):
        return Response(notify=[Notify.BASE])

    def _run_internal(self, **kwargs):
        return Response()

    def _setup_internal(self, **kwargs):
        return Response()

    def _shadow_data(self, **kwargs):
        return [Shadow(destination='bar', key='foo.a', info='b')]


class RunnableTest(unittest.TestCase):
    def create_runnable(self):
        return FakeRunnable(date=DATE_10260602)

    def test_init(self):
        runnable = self.create_runnable()

        self.assertEqual(runnable.date, DATE_10260602)
        self.assertEqual(runnable.ok, True)

    def test_set__valid(self):
        runnable = self.create_runnable()
        runnable.date = DATE_10270000
        runnable.ok = False

        self.assertEqual(runnable.date, DATE_10270000)
        self.assertEqual(runnable.ok, False)

    def test_set__invalid_date(self):
        with self.assertRaises(ValueError):
            runnable = self.create_runnable()
            runnable.date = [1]

    def test_set__invalid_ok(self):
        with self.assertRaises(ValueError):
            runnable = self.create_runnable()
            runnable.ok = [1]

    def test_notify(self):
        runnable = self.create_runnable()

        response = runnable._notify(notify=Notify.OTHER)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

    def test_run(self):
        runnable = self.create_runnable()

        response = runnable._run()
        self.assertEqual(response, Response())

    def test_setup(self):
        runnable = self.create_runnable()

        response = runnable._setup()
        self.assertEqual(
            response,
            Response(
                shadow=[Shadow(destination='bar', key='foo.a', info='b')]))

    def test_shadow(self):
        runnable = self.create_runnable()

        shadow = Shadow(destination='bar', key='foo.a', info='b')
        response = runnable._shadow(shadow=shadow)
        self.assertEqual(response, Response())
        self.assertEqual(runnable.shadow, {'foo.a': 'b'})


if __name__ == '__main__':
    unittest.main()
