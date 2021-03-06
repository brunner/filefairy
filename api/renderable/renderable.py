#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extend the renderable API to provide generated HTML from a class.

This base class abstracts the transformation from template input data to one or
more rendered templates. The rendered templates are deposited into a co-located
``fairylab`` repository, and are then deployed to live by a separate task.

Example:
    class Task(Renderable):
        def __init__(self, **kwargs):
            super(Task, self).__init__(**kwargs)

        @staticmethod
        def _href():
            return '/foo/'

        @staticmethod
        def _title():
            return 'foo'

        def _render_data(self, **kwargs):
            return [('foo/index.html', '', 'tmpl.html', {'a': 1, 'b': True}]

When the _render function is called, the template input data produced by
_render_data is passed to the corresponding template (in the above example,
this is ``tmpl.html``) and dumped to the given location (``foo/index.html``).

For golden tests, the rendered templates are dumped to a specified location
within the ``filefairy`` (current) repository.
"""

import abc
import errno
import logging
import os
import re
import sys

_logger = logging.getLogger('filefairy')
_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/api/renderable', '', _path)
sys.path.append(_root)

from common.abc_.abc_ import abstractstatic  # noqa
from common.datetime_.datetime_ import timestamp  # noqa
from common.elements.elements import menu  # noqa
from common.styles.styles import get_styles  # noqa
from types_.response.response import Response  # noqa

FAIRYLAB_DIR = _root + '/fairylab'
FILEFAIRY_DIR = _root


class Renderable():
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        e = kwargs.pop('e')
        super(Renderable, self).__init__(**kwargs)

        self.environment = e

    @abstractstatic
    def _href():
        pass

    @abstractstatic
    def _title():
        pass

    def _render_data(self, **kwargs):
        return []

    def _render(self, **kwargs):
        date = timestamp(kwargs['date'])
        test = kwargs.get('test')
        log = kwargs.get('log', True)

        data = self._render_data(**kwargs)
        if not data:
            return Response()

        for html, subtitle, tmpl, context in data:
            try:
                current = self._href() if test else self._get_current(html)
                m = None if current == '/fairylab/' else menu(current)

                subtitle = ' » ' + subtitle if subtitle else ''
                title = self._title() + subtitle

                styles = get_styles(context)
                tmpl = self.environment.get_template(tmpl)
                ts = tmpl.stream(
                    dict(context,
                         menu=m,
                         styles=styles,
                         title=title,
                         date=date))

                root = FILEFAIRY_DIR if test else FAIRYLAB_DIR
                path = os.path.join(root, html)
                self._mkdirs(path.rsplit('/', 1)[0])
                ts.dump(path)
            except Exception:
                if log:
                    _logger.log(logging.WARNING,
                                'Handled warning.',
                                exc_info=True)

        return Response()

    @staticmethod
    def _get_current(html):
        if html.endswith('index.html'):
            return '/fairylab/' + html[:-10]

        return '/fairylab/' + html

    @staticmethod
    def _mkdirs(path):
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise
