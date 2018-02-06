#!/usr/bin/env python

import copy
import os
import re
import sys

sys.path.append(
    re.sub(r'/plugins/league_file', '',
           os.path.dirname(os.path.abspath(__file__))))
from apis.plugin.plugin_api import PluginApi  # noqa
from apis.serializable.serializable_api import SerializableApi  # noqa
from private.server import user, league_file_dir  # noqa
from utils.subprocess.subprocess_util import check_output  # noqa

_size_pattern = '(\d+)'
_date_pattern = '(\w+\s\d+\s\d+:\d+)'
_name_pattern = '(orange_and_blue_league_baseball.tar.gz(?:.filepart)?)'
_line_pattern = '\s'.join([_size_pattern, _date_pattern, _name_pattern])


class LeagueFilePlugin(PluginApi, SerializableApi):
    def __init__(self):
        super(LeagueFilePlugin, self).__init__()

    def _on_message_internal(self, obj):
        pass

    def _run_internal(self):
        data = self.data
        original = copy.deepcopy(data)

        out = check_output(['ssh', user, 'ls -l ' + league_file_dir])
        for line in out.splitlines():
            line = re.sub(r'\s+', ' ', line)
            match = re.findall(_line_pattern, line)
            if match:
                size, date, name = match[0]
                if '.filepart' in name:
                    if not data['fp']:
                        data['fp'] = {'start': date}
                    data['fp']['size'] = size
                    data['fp']['end'] = date
                elif data['fp'] and '.filepart' not in out:
                    data['fp']['size'] = size
                    data['fp']['date'] = date
                    if not len(data['up']) or data['up'][0]['date'] != date:
                        data['up'].insert(0, copy.deepcopy(data['fp']))
                    data['fp'] = None

        if data != original:
            self.write()

    @staticmethod
    def _data():
        return os.path.join(os.path.dirname(__file__), 'data.json')
