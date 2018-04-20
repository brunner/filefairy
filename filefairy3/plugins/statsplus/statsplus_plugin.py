#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugins/statsplus', '', _path)
sys.path.append(_root)
from apis.plugin.plugin_api import PluginApi  # noqa
from apis.renderable.renderable_api import RenderableApi  # noqa
from enums.activity.activity_enum import ActivityEnum  # noqa


class StatsplusPlugin(PluginApi, RenderableApi):
    def __init__(self, **kwargs):
        super(StatsplusPlugin, self).__init__(**kwargs)

    @property
    def enabled(self):
        return False

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _href():
        return '/fairylab/statsplus/'

    @staticmethod
    def _info():
        return 'Collects live sim results.'

    @staticmethod
    def _title():
        return 'statsplus'

    def _notify_internal(self, **kwargs):
        pass

    def _on_message_internal(self, **kwargs):
        return ActivityEnum.NONE

    def _run_internal(self, **kwargs):
        return ActivityEnum.NONE

    def _render_internal(self, **kwargs):
        html = 'html/fairylab/statsplus/index.html'
        return [(html, '', 'statsplus.html', {})]

    def _setup_internal(self, **kwargs):
        pass
