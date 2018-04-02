#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/plugins/git', '', _path))
from apis.plugin.plugin_api import PluginApi  # noqa
from enums.activity.activity_enum import ActivityEnum  # noqa
from utils.logger.logger_util import log  # noqa
from utils.subprocess.subprocess_util import check_output  # noqa


class GitPlugin(PluginApi):
    def __init__(self, **kwargs):
        super(GitPlugin, self).__init__(**kwargs)

    @property
    def enabled(self):
        return True

    @staticmethod
    def _info():
        return 'Exposes git commands to admins.'

    def _setup_internal(self, **kwargs):
        self.day = kwargs['date'].day

    def _on_message_internal(self, **kwargs):
        return ActivityEnum.NONE

    def _run_internal(self, **kwargs):
        day = kwargs['date'].day
        if self.day != day:
            self.add(**kwargs)
            self.commit(**kwargs)
            self.push(**kwargs)
            self.day = day

        return ActivityEnum.NONE

    def _call(self, cmd, kwargs):
        d = check_output(cmd).strip('\n')
        log(self._name(), **dict(kwargs, c=d, s='Call completed.'))
        return ActivityEnum.BASE

    def add(self, **kwargs):
        return self._call(['git', 'add', '.'], kwargs)

    def commit(self, **kwargs):
        return self._call(['git', 'commit', '-m', 'Automated data push.'],
                          kwargs)

    def pull(self, **kwargs):
        return self._call(['git', 'pull'], kwargs)

    def push(self, **kwargs):
        return self._call(['git', 'push'], kwargs)

    def reset(self, **kwargs):
        return self._call(['git', 'reset', '--hard'], kwargs)

    def status(self, **kwargs):
        return self._call(['git', 'status'], kwargs)
