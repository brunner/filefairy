#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import re
import sys

_logger = logging.getLogger('filefairy')
_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/tasks/git', '', _path))

from api.registrable.registrable import Registrable  # noqa
from data.debug.debug import Debug  # noqa
from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa
from common.elements.elements import anchor  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import span  # noqa
from common.elements.elements import table  # noqa
from common.datetime_.datetime_ import decode_datetime  # noqa
from common.datetime_.datetime_ import encode_datetime  # noqa
from common.os_.os_ import chdir  # noqa
from common.subprocess_.subprocess_ import check_output  # noqa

CONTAINING_DIR = re.sub(r'/filefairy/tasks/git', '', _path)
FAIRYLAB_DIR = CONTAINING_DIR + '/fairylab/static'
FILEFAIRY_DIR = CONTAINING_DIR + '/filefairy'


class Git(Registrable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _href():
        return ''

    @staticmethod
    def _info():
        return 'Exposes remote commands to admins.'

    @staticmethod
    def _title():
        return 'git'

    def _notify_internal(self, **kwargs):
        notify = kwargs['notify']
        if notify == Notify.FILEFAIRY_DAY:
            self.automate('filefairy', **kwargs)
        elif notify == Notify.FILEFAIRY_DEPLOY:
            response = self.status('fairylab', **kwargs)
            stdout = self._stdout(response)
            if 'Changes not staged for commit' in stdout:
                self.automate('fairylab', **kwargs)
        return Response()

    def _on_message_internal(self, **kwargs):
        return Response()

    def _render_internal(self, **kwargs):
        return []

    def _run_internal(self, **kwargs):
        return Response()

    def _setup_internal(self, **kwargs):
        return Response()

    def _shadow_internal(self, **kwargs):
        return []

    @staticmethod
    def _format(cmd):
        return ' '.join(['"{}"'.format(c) if ' ' in c else c for c in cmd])

    @staticmethod
    def _stderr(response):
        stderr = response.debug[0].extra.get('stderr', '')
        return stderr

    @staticmethod
    def _stdout(response):
        return response.debug[0].extra.get('stdout', '')

    @staticmethod
    def _call(cmd, *args, **kwargs):
        if len(args) == 1 and args[0] == 'fairylab':
            with chdir(FAIRYLAB_DIR):
                output = check_output(cmd)
        else:
            output = check_output(cmd)

        response = Response()
        if output.get('ok'):
            response.append(notify=Notify.BASE)
            status = 'completed'
        else:
            status = 'failed'

        fcmd = '\'{}\''.format(Git._format(cmd))
        msg = 'Call {}: {}.'.format(status, fcmd)
        response.append(debug=Debug(msg=msg, extra=output))
        return response

    def add(self, *args, **kwargs):
        return self._call(['git', 'add', '.'], *args, **kwargs)

    def automate(self, *args, **kwargs):
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

    def commit(self, *args, **kwargs):
        s = 'Manual push.' if kwargs.get('v') else 'Automated push.'
        return self._call(['git', 'commit', '-m', s], *args, **kwargs)

    def pull(self, *args, **kwargs):
        return self._call(['git', 'pull'], *args, **kwargs)

    def push(self, *args, **kwargs):
        return self._call(['git', 'push'], *args, **kwargs)

    def reset(self, *args, **kwargs):
        return self._call(['git', 'reset', '--hard'], *args, **kwargs)

    def status(self, *args, **kwargs):
        return self._call(['git', 'status'], *args, **kwargs)
