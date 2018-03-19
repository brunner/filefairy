#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/plugins/snacks', '', _path))
from plugins.snacks.snacks_plugin import SnacksPlugin  # noqa

_data = SnacksPlugin._data()


class SnacksPluginTest(unittest.TestCase):
    pass
