#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/util/jinja2_', '', _path)
sys.path.append(_root)
from util.jinja2_.jinja2_ import env  # noqa


class Jinja2Test(unittest.TestCase):
    def test_env(self):
        environment = env()
        templates = os.path.join(_root, 'resource/templates')
        self.assertEqual(environment.loader.searchpath, [templates])
        self.assertEqual(environment.trim_blocks, True)
        self.assertEqual(environment.lstrip_blocks, True)


if __name__ == '__main__':
    unittest.main()
