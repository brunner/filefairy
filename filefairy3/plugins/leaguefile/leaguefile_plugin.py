#!/usr/bin/env python

import copy
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/plugins/leaguefile', '', _path))
from apis.plugin.plugin_api import PluginApi  # noqa
from apis.serializable.serializable_api import SerializableApi  # noqa
from utils.secrets.secrets_util import server  # noqa
from utils.slack.slack_util import chat_post_message  # noqa
from utils.subprocess.subprocess_util import check_output  # noqa

_size_pattern = '(\d+)'
_date_pattern = '(\w+\s\d+\s\d+:\d+)'
_name_pattern = '(orange_and_blue_league_baseball.tar.gz(?:.filepart)?)'
_line_pattern = '\s'.join([_size_pattern, _date_pattern, _name_pattern])


class LeaguefilePlugin(PluginApi, SerializableApi):
    def __init__(self, **kwargs):
        super(LeaguefilePlugin, self).__init__(**kwargs)

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _info():
        return 'Reports the progress of the league file upload.'

    def _setup(self, **kwargs):
        data = self.data
        original = copy.deepcopy(data)

        data['fp'] = None
        for size, date, name, fp in self._check():
            if '.filepart' in name:
                data['fp'] = {'start': date, 'size': size, 'end': date}
            elif not len(data['up']) or data['up'][0]['date'] != date:
                data['up'].insert(0, {
                    'date': date,
                    'start': date,
                    'size': size,
                    'end': date
                })

        if data != original:
            self.write()

    def _on_message_internal(self, **kwargs):
        pass

    def _run_internal(self, **kwargs):
        data = self.data
        original = copy.deepcopy(data)

        for size, date, name, fp in self._check():
            if '.filepart' in name:
                if not data['fp']:
                    data['fp'] = {'start': date}
                data['fp']['size'] = size
                data['fp']['end'] = date
            elif data['fp'] and not fp:
                data['fp']['size'] = size
                data['fp']['date'] = date
                if not len(data['up']) or data['up'][0]['date'] != date:
                    data['up'].insert(0, copy.deepcopy(data['fp']))
                    chat_post_message('general', 'File is up.')
                data['fp'] = None

        if data != original:
            self.write()
            return True

    @staticmethod
    def _check():
        ls = 'ls -l /var/www/html/StatsLab/league_file'
        out = check_output(['ssh', 'brunnerj@' + server, ls])
        fp = '.filepart' in out
        for line in out.splitlines():
            line = re.sub(r'\s+', ' ', line)
            match = re.findall(_line_pattern, line)
            if match:
                yield match[0] + (fp,)
