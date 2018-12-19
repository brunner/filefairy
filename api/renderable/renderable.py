#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extend the renderable API to provide generated HTML from a class.

This base class abstracts the transformation from template input data to one or
more rendered templates. The rendered templates are deposited into a colocated
``fairylab`` repository, and are then deployed to live by a separate task.

Example:
    class Task(Renderable):
        def __init__(self, **kwargs):
            super(Task, self).__init__(**kwargs)

        @staticmethod
        def _data():
            return os.path.join(_path, 'data.json')

        @staticmethod
        def _href():
            return '/foo/'

        @staticmethod
        def _info():
            return 'Description.'

        @staticmethod
        def _title():
            return 'foo'

        def _render_internal(self, **kwargs):
            return [('foo/index.html', '', 'tmpl.html', {'a': 1, 'b': True}]

When the _render function is called, the template input data produced by
_render_internal is passed to the corresponding template (in the above example,
this is ``tmpl.html``) and dumped to the given location (``foo/index.html``).

For golden tests, the rendered templates are dumped to a specified location
within the ``filefairy`` (current) repository.

The base class also has a helper function for generating attachment data for
alerts posted to Slack. The attachment describes the link and behavior of the
particular rendered template which is related to the alert.
"""

import abc
import errno
import logging
import os
import re
import sys

_logger = logging.getLogger('filefairy')
_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/api/renderable', '', _path))

from api.serializable.serializable import Serializable  # noqa
from common.abc_.abc_ import abstractstatic  # noqa
from common.datetime_.datetime_ import timestamp  # noqa
from common.slack.slack import chat_post_message  # noqa

CONTAINING_DIR = re.sub(r'/filefairy/api/renderable', '', _path)
FAIRYLAB_DIR = CONTAINING_DIR + '/fairylab/static'
FILEFAIRY_DIR = CONTAINING_DIR + '/filefairy'
GITHUB_LINK = 'https://github.com/brunner/filefairy/'


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
        _logger.log(logging.INFO, text)
        attachments = self._attachments() if self._href() else []
        return chat_post_message(channel, text, attachments=attachments)

    def _render(self, **kwargs):
        date = timestamp(kwargs['date'])
        test = kwargs.get('test')
        log = kwargs.get('log', True)

        value = self._render_internal(**kwargs)
        if not value:
            return

        for html, subtitle, tmpl, context in value:
            try:
                subtitle = ' » ' + subtitle if subtitle else ''
                title = self._title() + subtitle

                tmpl = self.environment.get_template(tmpl)
                ts = tmpl.stream(
                    dict(
                        context,
                        documentation=GITHUB_LINK,
                        title=title,
                        date=date))

                root = FILEFAIRY_DIR if test else FAIRYLAB_DIR
                path = os.path.join(root, html)
                self._mkdir_p(path.rsplit('/', 1)[0])
                ts.dump(path)
            except Exception:
                if log:
                    _logger.log(
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
