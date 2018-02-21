#!/usr/bin/env python

from plugin_api import PluginApi

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/apis/plugin', '', _path))
from apis.messageable.messageable_api import MessageableApi  # noqa
from apis.runnable.runnable_api import RunnableApi  # noqa


class FakePlugin(PluginApi):
    def __init__(self):
        super(FakePlugin, self).__init__()

    def _on_message_internal(self):
        pass

    def _run_internal(self):
        pass


class PluginApiTest(unittest.TestCase):
    def test_inheritance(self):
        plugin = FakePlugin()
        self.assertTrue(isinstance(plugin, MessageableApi))
        self.assertTrue(isinstance(plugin, RunnableApi))


if __name__ == '__main__':
    unittest.main()
