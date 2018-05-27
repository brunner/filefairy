#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import abc
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/api/plugin', '', _path))
from api.messageable.messageable import Messageable  # noqa
from api.renderable.renderable import Renderable  # noqa
from api.runnable.runnable import Runnable  # noqa
from core.notify.notify import Notify  # noqa
from core.response.response import Response  # noqa


class Plugin(Messageable, Runnable):
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        super(Plugin, self).__init__(**kwargs)
        self.shadow = {}

    @abc.abstractproperty
    def enabled(self):
        pass

    @abc.abstractmethod
    def _notify_internal(self, **kwargs):
        pass

    @abc.abstractmethod
    def _setup_internal(self, **kwargs):
        pass

    @abc.abstractmethod
    def _shadow_internal(self, **kwargs):
        pass

    def _notify(self, **kwargs):
        response = self._notify_internal(**kwargs)
        if response.notify:
            response.notify = [Notify.BASE]
        return response

    def _setup(self, **kwargs):
        response = self._setup_internal(**kwargs)
        response.shadow = self._shadow_internal(**kwargs)
        return response

    def _shadow(self, **kwargs):
        shadow = kwargs['shadow']
        self.shadow[shadow.key] = shadow.data
        self._setup(**kwargs)
        return Response()
