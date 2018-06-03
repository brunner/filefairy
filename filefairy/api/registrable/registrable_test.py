#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/api/registrable', '', _path))
from api.registrable.registrable import Registrable  # noqa
from core.notify.notify import Notify  # noqa
from core.response.response import Response  # noqa
from core.shadow.shadow import Shadow  # noqa

NOW = datetime.datetime(1985, 10, 27, 0, 0, 0)
THEN = datetime.datetime(1985, 10, 26, 0, 2, 30)


class FakeRegistrable(Registrable):
    def __init__(self, **kwargs):
        super(FakeRegistrable, self).__init__(**kwargs)

    def _notify_internal(self, **kwargs):
        return Response(notify=[Notify.BASE])

    def _setup_internal(self, **kwargs):
        return Response()

    def _shadow_internal(self, **kwargs):
        return [Shadow(destination='foo', key='registrable.bar', data='baz')]


class ResponseTest(unittest.TestCase):
    def test_init__valid_date(self):
        registrable = FakeRegistrable(date=THEN)
        self.assertEqual(registrable.date, THEN)
        self.assertEqual(registrable.ok, True)

    def test_init__invalid_date(self):
        with self.assertRaises(ValueError):
            FakeRegistrable(date=[1])

    def test_set__valid(self):
        registrable = FakeRegistrable(date=THEN)
        registrable.date = NOW
        registrable.ok = False
        self.assertEqual(registrable.date, NOW)
        self.assertEqual(registrable.ok, False)

    def test_set__invalid_date(self):
        with self.assertRaises(ValueError):
            registrable = FakeRegistrable(date=THEN)
            registrable.date = [1]

    def test_set__invalid_ok(self):
        with self.assertRaises(ValueError):
            registrable = FakeRegistrable(date=THEN)
            registrable.ok = [1]

    def test_notify(self):
        registrable = FakeRegistrable(date=NOW)
        response = registrable._notify(notify=Notify.OTHER)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

    def test_setup(self):
        registrable = FakeRegistrable(date=NOW)
        response = registrable._setup()
        self.assertEqual(
            response,
            Response(shadow=[
                Shadow(destination='foo', key='registrable.bar', data='baz')
            ]))

    @mock.patch.object(FakeRegistrable, '_setup')
    def test_shadow(self, mock_setup):
        shadow = Shadow(destination='foo', key='registrable.bar', data='baz')
        registrable = FakeRegistrable(date=NOW)
        self.assertEqual(registrable.shadow, {})

        response = registrable._shadow(shadow=shadow)
        self.assertEqual(response, Response())

        mock_setup.assert_called_once_with(shadow=shadow)
        self.assertEqual(registrable.shadow, {'registrable.bar': 'baz'})


if __name__ == '__main__':
    unittest.main()
