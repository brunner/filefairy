#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for sandbox.py."""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.extend((_path, re.sub(r'/impl/sandbox', '', _path)))

from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.jinja2_.jinja2_ import env  # noqa
from common.json_.json_ import dumps  # noqa
from common.test.test import Test  # noqa
from common.test.test import main  # noqa
from impl.sandbox.sandbox import Sandbox  # noqa

ENV = env()

DATE_10260602 = datetime_datetime_pst(1985, 10, 26, 6, 2, 30)


class SandboxTest(Test):
    def init_mocks(self, data):
        pass

    def create_sandbox(self):
        return Sandbox(e=ENV)

    def test_render_data(self):
        sandbox = self.create_sandbox()
        actual = sandbox._render_data(date=DATE_10260602)
        expected = None
        self.assertEqual(actual, expected)


if __name__ in ['__main__', 'impl.sandbox.sandbox_test']:
    main(SandboxTest,
         Sandbox,
         'impl.sandbox',
         'impl/sandbox', {},
         __name__ == '__main__',
         e=ENV)
