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

    @staticmethod
    def _href():
        return '/fairylab/foo/'

    @staticmethod
    def _title():
        return 'foo'

    def _on_message_internal(self, **kwargs):
        return Response()

    def _notify_internal(self, **kwargs):
        return Response(notify=[Notify.BASE])

    def _run_internal(self, **kwargs):
        return Response()

    def _setup_internal(self, **kwargs):
        return Response()

    def _shadow_internal(self, **kwargs):
        return Response()

    def _render_data(self, **kwargs):
        return [('html/fairylab/foo/index.html', '', 'foo.html', {})]

    def _shadow_data(self, **kwargs):
        return [Shadow(destination='bar', key='foo.a', info='b')]


class RunnableTest(unittest.TestCase):
    def setUp(self):
        patch_open = mock.patch(
            'api.serializable.serializable.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]

    def reset_mocks(self):
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()

    def create_runnable(self):
        self.init_mocks({})
        runnable = FakeRunnable(date=DATE_10260602, e=ENV)

        self.assertEqual(runnable.data, {})

        self.reset_mocks()
        self.init_mocks({})

        return runnable

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

    @mock.patch.object(FakeRunnable, '_render')
    def test_setup(self, mock_render):
        runnable = self.create_runnable()

        response = runnable._setup()
        self.assertEqual(
            response,
            Response(
                shadow=[Shadow(destination='bar', key='foo.a', info='b')]))

        mock_render.assert_called_once_with()

    def test_shadow(self):
        runnable = self.create_runnable()

        shadow = Shadow(destination='bar', key='foo.a', info='b')
        response = runnable._shadow(shadow=shadow)
        self.assertEqual(response, Response())
        self.assertEqual(runnable.shadow, {'foo.a': 'b'})


if __name__ == '__main__':
    unittest.main()
