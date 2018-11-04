#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import abc
import errno
import logging
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/api/renderable', '', _path)
sys.path.append(_root)
from api.serializable.serializable import Serializable  # noqa
from util.abc_.abc_ import abstractstatic  # noqa
from util.ago.ago import timestamp  # noqa
from util.secrets.secrets import fairylab  # noqa
from util.slack.slack import chat_post_message  # noqa
from util.subprocess_.subprocess_ import check_output  # noqa

logger_ = logging.getLogger('fairylab')

_fairylab = fairylab()


class Renderable(Serializable):
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        e = kwargs.pop('e')
        super().__init__(**kwargs)

        self.environment = e

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
        attachments = self._attachments()
        return chat_post_message(channel, text, attachments=attachments)

    def _render(self, **kwargs):
        date = timestamp(kwargs['date'])
        test = kwargs.get('test')
        log = kwargs.get('log', True)

        _title = self._title()
        for html, subtitle, tmpl, context in self._render_internal(**kwargs):
            try:
                subtitle = ' » ' + subtitle if subtitle else ''
                title = _title + subtitle
                tmpl = self.environment.get_template(tmpl)
                ts = tmpl.stream(dict(context, title=title, date=date))
                root = _root if test else os.path.join(_root, 'resource/html')
                here = os.path.join(root, html)
                there = 'brunnerj@{}:/public_html/fairylab/{}'.format(
                    _fairylab, html)
                self._mkdir_p(here.rsplit('/', 1)[0])
                ts.dump(here)
                check_output(['scp', here, there], log=log, timeout=8)
            except:
                if log:
                    logger_.log(
                        logging.WARNING, 'Handled warning.', exc_info=True)

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
        link = 'http://fairylab.surge.sh' + self._href()
        return [{
            'fallback': info,
            'title': title,
            'title_link': link,
            'text': info
        }]
