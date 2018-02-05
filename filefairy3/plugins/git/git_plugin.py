#!/usr/bin/env python

import os
import re
import sys

sys.path.append(re.sub(r'/plugins/league_file', '', os.path.dirname(__file__)))
from apis.base_plugin.base_plugin_api import BasePluginApi  # noqa
from utils.subprocess.subprocess_util import check_output  # noqa


class GitPlugin(BasePluginApi):
    def _on_message_internal(self, obj):
        pass

    def _run_internal(self):
        pass

    def _call(self, cmd, args):
        s = check_output(cmd).strip('\n')
        return self._chats(s, s, args)

    def add(self, *args):
        return self._call(['git', 'add' '.'], args)

    def commit(self, *args):
        return self._call(['git', 'commit', '-m', 'Automated data push.'],
                          args)

    def pull(self, *args):
        return self._call(['git', 'pull'], args)

    def push(self, *args):
        return self._call(['git', 'push', 'origin', 'master'], args)

    def reset(self, *args):
        return self._call(['git', 'reset', '--hard'], args)

    def status(self, *args):
        return self._call(['git', 'status'], args)
