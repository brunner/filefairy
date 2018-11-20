#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extend the messageable API to process Slack messages from a class.

This base class enhances a task endpoint which can process messages in the
league Slack. If the message describes a function that the task can perform,
then the function is invoked, otherwise the message is passed through to the
task implementation for custom handling.

Example:
    class Task(Messageable):
        def __init__(self, **kwargs):
            super(Task, self).__init__(**kwargs)

        def _on_message_internal(self, **kwargs):
            self._bar()
            return Response()

        def foo(self, *args, **kwargs):
            pass

        def _bar(self):
            pass

If the message ``Task.foo(a,b)`` is sent in the Slack testing channel, then the
function foo is invoked with *args equal to ['a', 'b'].

Or, if any other message is sent in the entire Slack, then the function
_on_message_internal is invoked with **kwargs containing the message data.

Tasks are required to return Response data from _on_message_internal.

Functions named with a leading underscore cannot be invoked by messageable.
"""

import abc
import logging
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/api/messageable', '', _path))

from api.nameable.nameable import Nameable  # noqa
from common.re_.re_ import find  # noqa
from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa

ARGS_PATTERN = r'^{}\.{}\((.*)\)$'
TESTING_CHANNEL = 'G3SUFLMK4'

_logger = logging.getLogger('fairylab')


class Messageable(Nameable):
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _name(self):
        return self.__class__.__name__

    @abc.abstractmethod
    def _on_message_internal(self, **kwargs):
        pass

    def _on_message(self, **kwargs):
        obj = kwargs.get('obj', {})
        text = obj.get('text', '')

        if obj.get('channel', '') == TESTING_CHANNEL and self._name() in text:
            for method in dir(self):
                if method not in text or method.startswith('_'):
                    continue

                item = getattr(self, method)
                if not callable(item):
                    continue

                args = find(ARGS_PATTERN.format(self._name(), method), text)
                if args is not None:
                    args = [a.strip() for a in args.split(',') if a]
                    response = item(*args, **dict(kwargs, v=True))

                    if not isinstance(response, Response):
                        response = Response()

                    for debug in response.debug:
                        _logger.log(
                            logging.DEBUG, debug.msg, extra=debug.extra)

                    response.notify = [Notify.BASE]
                    return response

        return self._on_message_internal(**kwargs)
