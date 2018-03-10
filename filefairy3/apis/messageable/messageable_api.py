#!/usr/bin/env python

import abc
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/apis/messageable', '', _path))
from apis.nameable.nameable_api import NameableApi  # noqa


class MessageableApi(NameableApi):
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        super(MessageableApi, self).__init__(**kwargs)

    def _name(self):
        return self.__class__.__name__

    @abc.abstractmethod
    def _on_message_internal(self, **kwargs):
        pass

    def _on_message(self, **kwargs):
        obj = kwargs.get('obj', {})
        text = obj.get('text', '')
        if obj.get('channel', '') == 'G3SUFLMK4' and self._name() in text:
            for method in dir(self):
                if method not in text or method.startswith('_'):
                    continue

                item = getattr(self, method)
                if not callable(item):
                    continue

                pattern = r'^' + self._name() + '\.' + method + '\((.*)\)$'
                match = re.findall(pattern, text)
                if match:
                    for i, a in enumerate(match[0].split(',')):
                        kwargs['a{}'.format(i+1)] = a
                    return item(**dict(kwargs, v=True))

        return self._on_message_internal(**kwargs)
