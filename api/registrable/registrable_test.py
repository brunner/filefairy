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
from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa
from data.shadow.shadow import Shadow  # noqa
from util.jinja2_.jinja2_ import env  # noqa
from util.json_.json_ import dumps  # noqa

_env = env()
_now = datetime.datetime(1985, 10, 27, 0, 0, 0)
_then = datetime.datetime(1985, 10, 26, 0, 2, 30)


def _data():
    return {'a': 1}


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

    def _render_internal(self, **kwargs):
        return [('html/fairylab/foo/index.html', '', 'foo.html', {})]

    def _run_internal(self, **kwargs):
        return Response()

    def _setup_internal(self, **kwargs):
        return Response()

    def _shadow_internal(self, **kwargs):
        return [Shadow(destination='bar', key='foo.a', data='b')]


class ResponseTest(unittest.TestCase):
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

    def create_registrable(self, data):
        self.init_mocks(data)
        registrable = FakeRegistrable(date=_then, e=_env)

        self.mock_open.assert_called_once_with(FakeRegistrable._data(), 'r')
        self.mock_handle.write.assert_not_called()
        self.assertEqual(registrable.data, data)

        self.reset_mocks()
        self.init_mocks(data)

        return registrable

    def test_init(self):
        registrable = self.create_registrable(_data())
        self.assertEqual(registrable.date, _then)
        self.assertEqual(registrable.ok, True)

    def test_set__valid(self):
        registrable = self.create_registrable(_data())
        registrable.date = _now
        registrable.ok = False
        self.assertEqual(registrable.date, _now)
        self.assertEqual(registrable.ok, False)

    def test_set__invalid_date(self):
        with self.assertRaises(ValueError):
            registrable = self.create_registrable(_data())
            registrable.date = [1]

    def test_set__invalid_ok(self):
        with self.assertRaises(ValueError):
            registrable = self.create_registrable(_data())
            registrable.ok = [1]

    def test_notify(self):
        registrable = self.create_registrable(_data())
        response = registrable._notify(notify=Notify.OTHER)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

    def test_run(self):
        registrable = self.create_registrable(_data())
        response = registrable._run()
        self.assertEqual(response, Response())

    def test_setup(self):
        registrable = self.create_registrable(_data())
        response = registrable._setup()
        self.assertEqual(
            response,
            Response(shadow=[
                Shadow(destination='bar', key='foo.a', data='b')
            ]))

    @mock.patch.object(FakeRegistrable, '_setup')
    def test_shadow(self, mock_setup):
        shadow = Shadow(destination='bar', key='foo.a', data='b')
        registrable = self.create_registrable(_data())
        self.assertEqual(registrable.shadow, {})

        response = registrable._shadow(shadow=shadow)
        self.assertEqual(response, Response())

        mock_setup.assert_called_once_with(shadow=shadow)
        self.assertEqual(registrable.shadow, {'foo.a': 'b'})


if __name__ == '__main__':
    unittest.main()
