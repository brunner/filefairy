#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import abc
import errno
import os
import re
import sys
import traceback

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/api/renderable', '', _path)
sys.path.append(_root)
from api.serializable.serializable import Serializable  # noqa
from util.abc_.abc_ import abstractstatic  # noqa
from util.logger.logger import log  # noqa
from util.secrets.secrets import server  # noqa
from util.slack.slack import chat_post_message  # noqa
from util.subprocess_.subprocess_ import check_output  # noqa

_server = server()


class Renderable(Serializable):
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        super(Renderable, self).__init__(**kwargs)
        self.environment = kwargs['e']

    @abstractstatic
    def _href():
        pass

    @abstractstatic
    def _title():
        pass

    @abstractstatic
    def _render_internal():
        pass

    def _chat(self, channel, text):
        chat_post_message(channel, text, attachments=self._attachments())

    def _render(self, **kwargs):
        date = kwargs['date'].strftime('%Y-%m-%d %H:%M:%S') + ' PST'
        test = kwargs.get('test')

        _title = self._title()
        for html, subtitle, tmpl, context in self._render_internal(**kwargs):
            try:
                subtitle = ' » ' + subtitle if subtitle else ''
                title = _title + subtitle
                tmpl = self.environment.get_template(tmpl)
                ts = tmpl.stream(dict(context, title=title, date=date))
                hroot = _root if test else os.path.join(_root, 'resource')
                here = os.path.join(hroot, html)
                there = 'brunnerj@' + _server + ':/var/www/' + html
                self._mkdir_p(here.rsplit('/', 1)[0])
                ts.dump(here)
                check_output(['scp', here, there], timeout=8)
            except Exception:
                exc = traceback.format_exc()
                log(self._name(), s='Exception.', c=exc, v=True)

    @staticmethod
    def _mkdir_p(path):
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def _attachments(self):
        info = self._info()
        title = 'Fairylab | ' + self._title()
        link = 'http://orangeandblueleaguebaseball.com' + self._href()
        return [{
            'fallback': info,
            'title': title,
            'title_link': link,
            'text': info
        }]
