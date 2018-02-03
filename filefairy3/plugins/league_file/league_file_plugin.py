#!/usr/bin/env python

import copy
import os
import re
import sys

sys.path.append(re.sub(r'/plugins/league_file', '', os.path.dirname(__file__)))
from apis.data_plugin.data_plugin_api import DataPluginApi  # noqa
from private.server import user, league_file_dir  # noqa
from utils.subprocess.subprocess_util import check_output  # noqa

size_pattern = '(\d+)'
date_pattern = '(\w+\s\d+\s\d+:\d+)'
name_pattern = '(orange_and_blue_league_baseball.tar.gz(?:.filepart)?)'
line_pattern = '\s'.join([size_pattern, date_pattern, name_pattern])


class LeagueFilePlugin(DataPluginApi):
    def _on_message_internal(self, obj):
        pass

    def _run_internal(self):
        data = self.data
        original = copy.deepcopy(data)

        out = check_output(['ssh', user, 'ls -l ' + league_file_dir])
        for line in out.splitlines():
            line = re.sub(r'\s+', ' ', line)
            match = re.findall(line_pattern, line)
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
