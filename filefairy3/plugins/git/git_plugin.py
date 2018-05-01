#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import threading

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/plugins/git', '', _path))
from apis.plugin.plugin_api import PluginApi  # noqa
from utils.logger.logger_util import log  # noqa
from utils.subprocess.subprocess_util import check_output  # noqa
from values.notify.notify_value import NotifyValue  # noqa
from values.response.response_value import ResponseValue  # noqa


class GitPlugin(PluginApi):
    def __init__(self, **kwargs):
        super(GitPlugin, self).__init__(**kwargs)

    @property
    def enabled(self):
        return True

    @staticmethod
    def _info():
        return 'Exposes git commands to admins.'

    def _notify_internal(self, **kwargs):
        notify = kwargs['notify']
        if notify == NotifyValue.FAIRYLAB_DAY:
            t = threading.Thread(target=self.automate)
            t.daemon = True
            t.start()
        return False

    def _on_message_internal(self, **kwargs):
        return ResponseValue()

    def _run_internal(self, **kwargs):
        return ResponseValue()

    def _setup_internal(self, **kwargs):
        pass

    def _shadow_internal(self, **kwargs):
        return {}

    @staticmethod
    def _format(cmd):
        return ' '.join(['"{}"'.format(c) if ' ' in c else c for c in cmd])

    def _call(self, cmd, kwargs):
        d = check_output(cmd).strip('\n')
        s = 'Call completed: ' + self._format(cmd)
        log(self._name(), **dict(kwargs, c=d, s=s))
        return ResponseValue(notify=[NotifyValue.BASE])

    def add(self, **kwargs):
        return self._call(['git', 'add', '.'], kwargs)

    def automate(self, **kwargs):
        self.add(**kwargs)
        self.commit(**kwargs)
        self.push(**kwargs)
        return ResponseValue(notify=[NotifyValue.BASE])

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
