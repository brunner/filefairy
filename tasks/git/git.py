#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Allows admin to interact with filefairy git repository."""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/tasks/git', '', _path)
sys.path.append(_root)

from api.messageable.messageable import Messageable  # noqa
from api.runnable.runnable import Runnable  # noqa
from common.messageable.messageable import messageable  # noqa
from common.os_.os_ import chdir  # noqa
from common.subprocess_.subprocess_ import check_output  # noqa
from types_.debug.debug import Debug  # noqa
from types_.notify.notify import Notify  # noqa
from types_.response.response import Response  # noqa

FAIRYLAB_DIR = _root + '/fairylab'


class Git(Messageable, Runnable):
    def __init__(self, **kwargs):
        super(Git, self).__init__(**kwargs)

    def _notify_internal(self, **kwargs):
        if kwargs['notify'] == Notify.FILEFAIRY_DAY:
            self.acp(**kwargs)
        elif kwargs['notify'] == Notify.FILEFAIRY_DEPLOY:
            with chdir(FAIRYLAB_DIR):
                self.acp(**kwargs)

        return Response()

    @messageable
    def acp(self, *args, **kwargs):
        response = Response(notify=[Notify.BASE])

        sub = self.add(*args, **kwargs)
        if not sub.notify:
            return sub
        for debug in sub.debug:
            response.append(debug=debug)

        sub = self.commit(*args, **kwargs)
        if not sub.notify:
            return sub
        for debug in sub.debug:
            response.append(debug=debug)

        sub = self.push(*args, **kwargs)
        if not sub.notify:
            return sub
        for debug in sub.debug:
            response.append(debug=debug)

        return response

    @messageable
    def add(self, *args, **kwargs):
        return self.check(['git', 'add', '.'], **kwargs)

    @messageable
    def commit(self, *args, **kwargs):
        return self.check(['git', 'commit', '-m', 'Automated push.'], **kwargs)

    @messageable
    def pull(self, *args, **kwargs):
        return self.check(['git', 'pull'], **kwargs)

    @messageable
    def push(self, *args, **kwargs):
        return self.check(['git', 'push'], **kwargs)

    @messageable
    def reset(self, *args, **kwargs):
        return self.check(['git', 'reset', '--hard'], **kwargs)

    @messageable
    def status(self, *args, **kwargs):
        return self.check(['git', 'status'], **kwargs)

    @staticmethod
    def check(cmd, **kwargs):
        response = Response()
        output = check_output(cmd)

        if output.get('ok'):
            response.append(notify=Notify.BASE)
            status = 'completed'
        else:
            status = 'failed'

        fcmd = ' '.join(['"{}"'.format(c) if ' ' in c else c for c in cmd])
        msg = 'Call {}: \'{}\'.'.format(status, fcmd)
        response.append(debug=Debug(msg=msg, extra=output))

        return response
