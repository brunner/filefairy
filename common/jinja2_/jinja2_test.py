#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for jinja2_.py."""

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/common/jinja2_', '', _path))

from common.jinja2_.jinja2_ import env  # noqa


class Jinja2Test(unittest.TestCase):
    def test_env(self):
        environment = env()

        root = re.sub(r'/common/jinja2_', '', _path)
        templates = os.path.join(root, 'resources/templates')
        self.assertEqual(environment.loader.searchpath, [templates])
        self.assertEqual(environment.trim_blocks, True)
        self.assertEqual(environment.lstrip_blocks, True)


if __name__ == '__main__':
    unittest.main()
