#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/pluin/git', '', _path))
from api.plugin.plugin import Plugin  # noqa
from core.notify.notify import Notify  # noqa
from core.response.response import Response  # noqa
from util.logger.logger import log  # noqa
from util.subprocess_.subprocess_ import check_output  # noqa


class Git(Plugin):
    def __init__(self, **kwargs):
        super(Git, self).__init__(**kwargs)

    @property
    def enabled(self):
        return True

    @staticmethod
    def _info():
        return 'Exposes remote commands to admins.'

    def _notify_internal(self, **kwargs):
        notify = kwargs['notify']
        if notify == Notify.FAIRYLAB_DAY:
            self.automate(**kwargs)
        return Response()

    def _on_message_internal(self, **kwargs):
        return Response()

    def _run_internal(self, **kwargs):
        return Response()

    def _setup_internal(self, **kwargs):
        return Response()

    def _shadow_internal(self, **kwargs):
        return []

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
