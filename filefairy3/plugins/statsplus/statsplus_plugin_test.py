#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(_path)
_root = re.sub(r'/plugins/statsplus', '', _path)
sys.path.append(_root)
from enums.activity.activity_enum import ActivityEnum  # noqa
from plugins.statsplus.statsplus_plugin import StatsplusPlugin  # noqa
from utils.test.test_util import main, TestUtil  # noqa


class StatsplusPluginTest(TestUtil):
    def init_mocks(self, data):
        pass


if __name__ in ['__main__', 'plugins.statsplus.statsplus_plugin_test']:
    _main = __name__ == '__main__'
    _pkg = 'plugins.statsplus'
    _pth = 'plugins/statsplus'
    main(StatsplusPluginTest, StatsplusPlugin, _pkg, _pth, {}, _main)
