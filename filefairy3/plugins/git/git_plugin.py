#!/usr/bin/env python

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/plugins/git', '', _path))
from apis.plugin.plugin_api import PluginApi  # noqa
from utils.logger.logger_util import log  # noqa
from utils.subprocess.subprocess_util import check_output  # noqa


class GitPlugin(PluginApi):
    def __init__(self, **kwargs):
        super(GitPlugin, self).__init__(**kwargs)

    @staticmethod
    def _info():
        return 'Exposes git commands to admins.'

    def _setup(self, **kwargs):
        pass

    def _on_message_internal(self, **kwargs):
        pass

    def _run_internal(self, **kwargs):
        pass

    def _call(self, cmd, kwargs):
        d = check_output(cmd).strip('\n')
        log(self._name(), **dict(kwargs, c=d, s='Call completed.'))
        return True

    def add(self, **kwargs):
        return self._call(['git', 'add', '.'], kwargs)

    def commit(self, **kwargs):
        return self._call(['git', 'commit', '-m', 'Automated data push.'],
                          kwargs)

    def pull(self, **kwargs):
        return self._call(['git', 'pull'], kwargs)

    def push(self, **kwargs):
        return self._call(['git', 'push', 'origin', 'master'], kwargs)

    def reset(self, **kwargs):
        return self._call(['git', 'reset', '--hard'], kwargs)

    def status(self, **kwargs):
        return self._call(['git', 'status'], kwargs)
