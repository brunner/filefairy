#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for event.py."""

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/data/event', '', _path))

from data.event.event import Event  # noqa


class EventTest(unittest.TestCase):
    def test_enum(self):
        pass


if __name__ == '__main__':
    unittest.main()
