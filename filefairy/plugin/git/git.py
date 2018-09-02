#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import logging
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugin/git', '', _path)
sys.path.append(_root)
from api.registrable.registrable import Registrable  # noqa
from core.debug.debug import Debug  # noqa
from core.notify.notify import Notify  # noqa
from core.response.response import Response  # noqa
from util.component.component import anchor  # noqa
from util.component.component import span  # noqa
from util.component.component import table  # noqa
from util.datetime_.datetime_ import decode_datetime  # noqa
from util.datetime_.datetime_ import encode_datetime  # noqa
from util.subprocess_.subprocess_ import check_output  # noqa

logger_ = logging.getLogger('fairylab')

_commit = 'https://github.com/brunner/orangeandblueleague/commit/'
_l = ['d-inline-block', 'w-65p']
_r = ['d-inline-block', 'text-right', 'w-65p']

_fairylab_root = re.sub(r'/orangeandblueleague/filefairy', '/fairylab/static',
                        _root)


class Git(Registrable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _href():
        return '/git/'

    @staticmethod
    def _info():
        return 'Exposes remote commands to admins.'

    @staticmethod
    def _title():
        return 'git'

    def _notify_internal(self, **kwargs):
        notify = kwargs['notify']
        if notify == Notify.FAIRYLAB_DAY:
            self.automate('filefairy', **kwargs)
        elif notify == Notify.FAIRYLAB_DEPLOY:
            response = self.status('fairylab', **kwargs)
            stdout = self._stdout(response)
            if 'Changes not staged for commit' in stdout:
                self.automate('fairylab', **kwargs)
        return Response()

    def _on_message_internal(self, **kwargs):
        return Response()

    def _render_internal(self, **kwargs):
        html = 'git/index.html'
        _home = self._home(**kwargs)
        return [(html, '', 'git.html', _home)]

    def _run_internal(self, **kwargs):
        return Response()

    def _setup_internal(self, **kwargs):
        self._render(**kwargs)
        return Response()

    def _shadow_internal(self, **kwargs):
        return []

    @staticmethod
    def _firstlast(text):
        match = re.findall('(\w+)\.\.(\w+)', text)
        if match:
            first, last = match[0]
        else:
            return '???????', '???????'

        response = Git._call(['git', 'log', '-20', '--format="%H"'])
        stdout = Git._stdout(response)
        for line in stdout.splitlines():
            line = line.replace('"', '')
            if line.startswith(first):
                first = line
            if line.startswith(last):
                last = line

        return first, last

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
        cwd = os.getcwd()
        if len(args) == 1 and args[0] == 'fairylab':
            os.chdir(_fairylab_root)

        output = check_output(cmd)
        os.chdir(cwd)

        response = Response()
        if output.get('ok'):
            response.append_notify(Notify.BASE)
            status = 'completed'
        else:
            status = 'failed'

        fcmd = '\'{}\''.format(Git._format(cmd))
        msg = 'Call {}: {}.'.format(status, fcmd)
        response.append_debug(Debug(msg=msg, extra=output))
        return response

    def add(self, *args, **kwargs):
        return self._call(['git', 'add', '.'], *args, **kwargs)

    def automate(self, *args, **kwargs):
        response = Response(notify=[Notify.BASE])

        sub = self.add(*args, **kwargs)
        if not sub.notify:
            return sub
        for debug in sub.debug:
            response.append_debug(debug)

        sub = self.commit(*args, **kwargs)
        if not sub.notify:
            return sub
        for debug in sub.debug:
            response.append_debug(debug)

        sub = self.push(*args, **kwargs)
        if not sub.notify:
            return sub
        for debug in sub.debug:
            response.append_debug(debug)

        return response

    def commit(self, *args, **kwargs):
        s = 'Manual' if kwargs.get('v') else 'Automated'
        return self._call(['git', 'commit', '-m', s + ' push.'], *args,
                          **kwargs)

    def pull(self, *args, **kwargs):
        response = self._call(['git', 'pull'], *args, **kwargs)

        if len(args) == 1 and args[0] == 'fairylab':
            pass
        elif response.notify:
            logger_.log(logging.INFO, 'Fetched latest changes.')
            self._save(response, 'pull', self._stdout, **kwargs)

        return response

    def push(self, *args, **kwargs):
        response = self._call(['git', 'push'], *args, **kwargs)

        if len(args) == 1 and args[0] == 'fairylab':
            pass
        elif response.notify:
            s = 'Manual' if kwargs.get('v') else 'Automated'
            logger_.log(logging.INFO, s + ' push.')
            self._save(response, 'push', self._stderr, **kwargs)

        return response

    def reset(self, *args, **kwargs):
        return self._call(['git', 'reset', '--hard'], *args, **kwargs)

    def status(self, *args, **kwargs):
        return self._call(['git', 'status'], *args, **kwargs)

    def _body(self, key):
        body = []
        for value in self.data[key]:
            first = anchor(_commit + value['first'], value['first'][:7])
            last = anchor(_commit + value['last'], value['last'][:7])
            range_ = span(_l, first) + ' ... ' + span(_r, last)
            ddate = decode_datetime(value['date'])
            date = ddate.strftime('%b %d')
            time = ddate.strftime('%H:%M')
            body.append([range_, date + ' ' + time])
        return body

    def _home(self, **kwargs):
        data = self.data
        ret = {
            'breadcrumbs': [{
                'href': '/',
                'name': 'Fairylab'
            }, {
                'href': '',
                'name': 'Git'
            }]
        }

        if data['pull']:
            ret['pull'] = table(
                clazz='border mt-3',
                head=['Range'],
                hcols=[' colspan="2"'],
                bcols=['', ' class="text-right"'],
                body=self._body('pull'))

        if data['push']:
            ret['push'] = table(
                clazz='border mt-3',
                head=['Range'],
                hcols=[' colspan="2"'],
                bcols=['', ' class="text-right"'],
                body=self._body('push'))

        return ret

    def _save(self, response, key, extractor, **kwargs):
        data = self.data
        original = copy.deepcopy(data)

        date = encode_datetime(kwargs['date'])
        text = extractor(response)
        first, last = self._firstlast(text)
        value = {'date': date, 'first': first, 'last': last}
        data[key].insert(0, value)
        if len(data[key]) > 10:
            data[key] = data[key][:10]

        if data != original:
            self.write()
            self._render(**kwargs)
