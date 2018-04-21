#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import datetime
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugins/statsplus', '', _path)
sys.path.append(_root)
from apis.plugin.plugin_api import PluginApi  # noqa
from apis.renderable.renderable_api import RenderableApi  # noqa
from enums.activity.activity_enum import ActivityEnum  # noqa
from utils.datetime.datetime_util import encode_datetime  # noqa


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
        activity = kwargs['activity']
        if activity == ActivityEnum.DOWNLOAD:
            self.data['finished'] = True
            self.write()
        return False

    def _on_message_internal(self, **kwargs):
        obj = kwargs['obj']
        bot_id = obj.get('bot_id')
        channel = obj.get('channel')
        if bot_id != 'B7KJ3362Y' or channel != 'C7JSGHW8G':
            return ActivityEnum.NONE

        data = self.data
        original = copy.deepcopy(data)

        if self.data['finished']:
            self.data['finished'] = False
            self._clear()

        text = obj.get('text', '')

        if 'MAJOR LEAGUE BASEBALL Final Scores' in text:
            self._scores(text)

        if data != original:
            self.write()

        return ActivityEnum.BASE

    def _run_internal(self, **kwargs):
        if self.data['updated']:
            self.data['updated'] = False
            self.write()

        return ActivityEnum.NONE

    def _render_internal(self, **kwargs):
        html = 'html/fairylab/statsplus/index.html'
        return [(html, '', 'statsplus.html', {})]

    def _setup_internal(self, **kwargs):
        pass

    def _clear(self):
        self.data['scores'] = {}

    def _scores(self, text):
        match = re.findall('\d{2}\/\d{2}\/\d{4}', text)
        if match:
            date = datetime.datetime.strptime(match[0], '%m/%d/%Y')
            self.data['scores'][encode_datetime(date)] = text
            self.data['updated'] = True
