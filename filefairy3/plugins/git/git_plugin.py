#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import threading

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/plugins/git', '', _path))
from api.plugin.plugin_api import PluginApi  # noqa
from utils.logger.logger_util import log  # noqa
from utils.subprocess.subprocess_util import check_output  # noqa
from value.notify.notify_value import NotifyValue  # noqa
from value.response.response_value import ResponseValue  # noqa


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
        output = check_output(cmd)
        if output.get('ok'):
            value = output.get('output', '').strip('\n')
            s = 'Call completed: \'{}\'.'.format(self._format(cmd))
            log(self._name(), **dict(kwargs, c=value, s=s))
        else:
            s = 'Call failed: \'{}\'.'.format(self._format(cmd))
            log(self._name(), **dict(kwargs, c=output, s=s))

    def add(self, **kwargs):
        return self._call(['git', 'add', '.'], kwargs)

    def automate(self, **kwargs):
        self.add(**kwargs)
        self.commit(**kwargs)
        self.push(**kwargs)

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
