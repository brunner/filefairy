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
sys.path.append(re.sub(r'/api/registrable', '', _path))

from api.registrable.registrable import Registrable  # noqa
from common.jinja2_.jinja2_ import env  # noqa
from common.json_.json_ import dumps  # noqa
from types_.notify.notify import Notify  # noqa
from types_.response.response import Response  # noqa
from types_.shadow.shadow import Shadow  # noqa

ENV = env()

DATE_10260602 = datetime.datetime(1985, 10, 26, 6, 2, 30)
DATE_10270000 = datetime.datetime(1985, 10, 27)


class FakeRegistrable(Registrable):
    def __init__(self, **kwargs):
        super(FakeRegistrable, self).__init__(**kwargs)

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _href():
        return '/fairylab/foo/'

    @staticmethod
    def _info():
        return 'Description of foo.'

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


class RegistrableTest(unittest.TestCase):
    def setUp(self):
        patch_open = mock.patch(
            'api.serializable.serializable.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

    def init_mocks(self):
        mo = mock.mock_open(read_data=dumps({}))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]

    def reset_mocks(self):
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()

    def create_registrable(self):
        self.init_mocks()
        registrable = FakeRegistrable(date=DATE_10260602, e=ENV)

        self.mock_open.assert_called_once_with(FakeRegistrable._data(), 'r')
        self.mock_handle.write.assert_not_called()
        self.reset_mocks()
        self.init_mocks()

        return registrable

    def test_init(self):
        registrable = self.create_registrable()

        self.assertEqual(registrable.date, DATE_10260602)
        self.assertEqual(registrable.ok, True)

    def test_set__valid(self):
        registrable = self.create_registrable()
        registrable.date = DATE_10270000
        registrable.ok = False

        self.assertEqual(registrable.date, DATE_10270000)
        self.assertEqual(registrable.ok, False)

    def test_set__invalid_date(self):
        with self.assertRaises(ValueError):
            registrable = self.create_registrable()
            registrable.date = [1]

    def test_set__invalid_ok(self):
        with self.assertRaises(ValueError):
            registrable = self.create_registrable()
            registrable.ok = [1]

    def test_notify(self):
        registrable = self.create_registrable()

        response = registrable._notify(notify=Notify.OTHER)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

    def test_run(self):
        registrable = self.create_registrable()

        response = registrable._run()
        self.assertEqual(response, Response())

    @mock.patch.object(FakeRegistrable, '_render')
    def test_setup(self, mock_render):
        registrable = self.create_registrable()

        response = registrable._setup()
        self.assertEqual(
            response,
            Response(
                shadow=[Shadow(destination='bar', key='foo.a', info='b')]))

        mock_render.assert_called_once_with()

    def test_shadow(self):
        registrable = self.create_registrable()

        shadow = Shadow(destination='bar', key='foo.a', info='b')
        response = registrable._shadow(shadow=shadow)
        self.assertEqual(response, Response())
        self.assertEqual(registrable.shadow, {'foo.a': 'b'})


if __name__ == '__main__':
    unittest.main()
