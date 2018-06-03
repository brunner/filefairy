#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/plugin/git', '', _path))
from api.messageable.messageable import Messageable  # noqa
from api.registrable.registrable import Registrable  # noqa
from api.runnable.runnable import Runnable  # noqa
from core.notify.notify import Notify  # noqa
from core.response.response import Response  # noqa
from util.subprocess_.subprocess_ import check_output  # noqa

import core.dashboard.dashboard  # noqa
logger_ = logging.getLogger('fairylab')


class Git(Messageable, Registrable, Runnable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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

    def _call(self, cmd, **kwargs):
        output = check_output(cmd)
        if kwargs.get('v') or not output.get('ok'):
            status = 'completed' if output.get('ok') else 'failed'
            fcmd = '\'{}\''.format(self._format(cmd))
            s = 'Call {}: {}.'.format(status, fcmd)
            logger_.log(
                logging.DEBUG, s, extra={
                    'output': output.get('output', '')
                })
        return output

    def add(self, **kwargs):
        return self._call(['git', 'add', '.'], **kwargs)

    def automate(self, **kwargs):
        output = self.add(**kwargs)
        if not output.get('ok'):
            return

        output = self.commit(**kwargs)
        if not output.get('ok'):
            return

        output = self.push(**kwargs)
        if output.get('ok'):
            logger_.log(logging.INFO, 'Automated data push.')

    def commit(self, **kwargs):
        return self._call(['git', 'commit', '-m', 'Automated data push.'],
                          **kwargs)

    def pull(self, **kwargs):
        output = self._call(['git', 'pull'], **kwargs)
        if output.get('ok'):
            logger_.log(logging.INFO, 'Fetched latest changes.')

    def push(self, **kwargs):
        return self._call(['git', 'push'], **kwargs)

    def reset(self, **kwargs):
        return self._call(['git', 'reset', '--hard'], **kwargs)

    def status(self, **kwargs):
        return self._call(['git', 'status'], **kwargs)
