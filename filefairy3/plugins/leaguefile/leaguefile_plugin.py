#!/usr/bin/env python

import copy
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/plugins/leaguefile', '', _path))
from apis.plugin.plugin_api import PluginApi  # noqa
from apis.renderable.renderable_api import RenderableApi  # noqa
from utils.secrets.secrets_util import server  # noqa
from utils.slack.slack_util import chat_post_message  # noqa
from utils.subprocess.subprocess_util import check_output  # noqa

_size_pattern = '(\d+)'
_date_pattern = '(\w+\s\d+\s\d+:\d+)'
_name_pattern = '(orange_and_blue_league_baseball.tar.gz(?:.filepart)?)'
_line_pattern = '\s'.join([_size_pattern, _date_pattern, _name_pattern])


class LeaguefilePlugin(PluginApi, RenderableApi):
    def __init__(self, **kwargs):
        super(LeaguefilePlugin, self).__init__(**kwargs)

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _html():
        return 'leaguefile/index.html'

    @staticmethod
    def _info():
        return 'Reports the progress of the league file upload.'

    @staticmethod
    def _tmpl():
        return 'leaguefile.html'

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

        self._render()

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
                    if len(data['up']) > 7:
                        data['up'] = data['up'][:7]
                    chat_post_message('general', 'File is up.')
                data['fp'] = None

        if data != original:
            self.write()

        if data != original or data['fp']:
            self._render()
            return True

    def _render_internal(self, **kwargs):
        ret = copy.deepcopy(self.data)
        ret['title'] = 'leaguefile'
        ret['breadcrumbs'] = [{
            'href': '/fairylab/',
            'name': 'Home'
        }, {
            'href': '',
            'name': 'Leaguefile'
        }]

        if ret['fp']:
            fp = ret['fp']
            fp['size'] = self._commaify(fp['size'])
            fp['start'] = self._reverse(fp['start'])
            fp['end'] = self._reverse(fp['end'])

        for up in ret['up']:
            del up['date']
            up['size'] = self._commaify(up['size'])
            up['start'] = self._reverse(up['start'])
            up['end'] = self._reverse(up['end'])

        return ret

    @staticmethod
    def _commaify(s):
        return '{:,}'.format(int(s))

    @staticmethod
    def _reverse(s):
        return ' '.join(s.rsplit(' ', 1)[::-1])

    @staticmethod
    def _check():
        ls = 'ls -l /var/www/html/StatsLab/league_file'
        out = check_output(['ssh', 'brunnerj@' + server, ls])
        fp = '.filepart' in out
        for line in out.splitlines():
            line = re.sub(r'\s+', ' ', line)
            match = re.findall(_line_pattern, line)
            if match:
                yield match[0] + (fp, )
