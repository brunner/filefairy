#!/usr/bin/env python

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/plugins/exports', '', _path))
from apis.plugin.plugin_api import PluginApi  # noqa
from apis.serializable.serializable_api import SerializableApi  # noqa
from utils.urllib.urllib_util import urlopen  # noqa

_url = 'https://orangeandblueleaguebaseball.com/StatsLab/exports.php'


class ExportsPlugin(PluginApi, SerializableApi):
    def __init__(self, **kwargs):
        super(ExportsPlugin, self).__init__(**kwargs)

    @property
    def enabled(self):
        return True

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _info():
        return 'Tracks how often each manager exports.'

    def _setup(self, **kwargs):
        text = urlopen(_url)
        self.file_date = self._file_date(text)
        self.exports = self._exports(text)

    def _on_message_internal(self, **kwargs):
        pass

    def _run_internal(self, **kwargs):
        data = self.data

        text = urlopen(_url)
        file_date = self._file_date(text)

        if not file_date:
            pass
        elif not self.file_date:
            self.file_date = file_date
        elif file_date != self.file_date:
            for teamid, status in self.exports:
                if not data[teamid]['ai']:
                    s = status.lower()[0]
                    data[teamid][s] += 1
                    data[teamid]['form'] += s
                    while len(data[teamid]['form']) > 20:
                        data[teamid]['form'] = data[teamid]['form'][1:]
            self.file_date = file_date
            self.write()
            return True
        else:
            self.exports = self._exports(text)

    @staticmethod
    def _file_date(text):
        match = re.findall(r'League File Updated: ([^<]+)<', text)
        return match[0] if len(match) else ''

    @staticmethod
    def _exports(text):
        return re.findall(r"teams/team_(\d+)(?:[\s\S]+?)(New|Old) Export",
                          text)
