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
from core.debug.debug import Debug  # noqa
from core.notify.notify import Notify  # noqa
from core.response.response import Response  # noqa
from util.subprocess_.subprocess_ import check_output  # noqa

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
        response = Response()

        if output.get('ok'):
            response.append_notify(Notify.BASE)
            status = 'completed'
        else:
            status = 'failed'

        fcmd = '\'{}\''.format(self._format(cmd))
        msg = 'Call {}: {}.'.format(status, fcmd)
        extra = {'output': output.get('output', '')}
        response.append_debug(Debug(msg=msg, extra=extra))
        return response

    def add(self, **kwargs):
        return self._call(['git', 'add', '.'], **kwargs)

    def automate(self, **kwargs):
        response = Response(notify=[Notify.BASE])

        sub = self.add(**kwargs)
        if not sub.notify:
            return sub
        for debug in sub.debug:
            response.append_debug(debug)

        sub = self.commit(**kwargs)
        if not sub.notify:
            return sub
        for debug in sub.debug:
            response.append_debug(debug)

        sub = self.push(**kwargs)
        if not sub.notify:
            return sub
        for debug in sub.debug:
            response.append_debug(debug)

        logger_.log(logging.INFO, 'Automated data push.')
        return response

    def commit(self, **kwargs):
        return self._call(['git', 'commit', '-m', 'Automated data push.'],
                          **kwargs)

    def pull(self, **kwargs):
        response = self._call(['git', 'pull'], **kwargs)
        if response.notify:
            logger_.log(logging.INFO, 'Fetched latest changes.')
        return response

    def push(self, **kwargs):
        return self._call(['git', 'push'], **kwargs)

    def reset(self, **kwargs):
        return self._call(['git', 'reset', '--hard'], **kwargs)

    def status(self, **kwargs):
        return self._call(['git', 'status'], **kwargs)
