#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import logging
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/plugin/git', '', _path))
from api.messageable.messageable import Messageable  # noqa
from api.registrable.registrable import Registrable  # noqa
from api.renderable.renderable import Renderable  # noqa
from api.runnable.runnable import Runnable  # noqa
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


class Git(Messageable, Registrable, Renderable, Runnable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _href():
        return '/fairylab/git/'

    @staticmethod
    def _info():
        return 'Exposes remote commands to admins.'

    @staticmethod
    def _title():
        return 'git'

    def _notify_internal(self, **kwargs):
        notify = kwargs['notify']
        if notify == Notify.FAIRYLAB_DAY:
            self.automate(**kwargs)
        return Response()

    def _on_message_internal(self, **kwargs):
        return Response()

    def _render_internal(self, **kwargs):
        html = 'html/fairylab/git/index.html'
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
        match = re.findall('(\w{7})\.\.(\w{7})', text)
        if match:
            first, last = match[0]
        else:
            return '???????', '???????'

        response = Git._call(['git', 'log', '-20', '--format="%H"'])
        stdout = Git._stdout(response)
        for line in stdout.splitlines():
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
        print(stderr)
        return stderr

    @staticmethod
    def _stdout(response):
        return response.debug[0].extra.get('output', '')

    @staticmethod
    def _call(cmd, **kwargs):
        output = check_output(cmd)
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

        return response

    def commit(self, **kwargs):
        s = 'Manual' if kwargs.get('v') else 'Automated'
        return self._call(['git', 'commit', '-m', s + ' data push.'], **kwargs)

    def pull(self, **kwargs):
        response = self._call(['git', 'pull'], **kwargs)
        if response.notify:
            logger_.log(logging.INFO, 'Fetched latest changes.')
            self._save(response, 'pull', self._stdout, **kwargs)

        return response

    def push(self, **kwargs):
        response = self._call(['git', 'push'], **kwargs)
        if response.notify:
            s = 'Manual' if kwargs.get('v') else 'Automated'
            logger_.log(logging.INFO, s + ' data push.')
            self._save(response, 'push', self._stderr, **kwargs)

        return response

    def reset(self, **kwargs):
        return self._call(['git', 'reset', '--hard'], **kwargs)

    def status(self, **kwargs):
        return self._call(['git', 'status'], **kwargs)

    def _body(self, key):
        body = []
        for value in self.data[key]:
            first = anchor(_commit + value['first'], value['first'][:7])
            last = anchor(_commit + value['last'], value['last'][:7])
            range_ = span(_l, first) + ' ... ' + span(_r, last)
            ddate = decode_datetime(value['date'])
            date = ddate.strftime('%b %d')
            time = ddate.strftime('%H:%M')
            body.append([range_, date, time])
        return body

    def _home(self, **kwargs):
        data = self.data
        ret = {
            'breadcrumbs': [{
                'href': '/fairylab/',
                'name': 'Home'
            }, {
                'href': '',
                'name': 'Git'
            }]
        }

        if data['pull']:
            ret['pull'] = table(
                clazz='border mt-3',
                head=['Range', 'Date', 'Time'],
                body=self._body('pull'))

        if data['push']:
            ret['push'] = table(
                clazz='border mt-3',
                head=['Range', 'Date', 'Time'],
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
