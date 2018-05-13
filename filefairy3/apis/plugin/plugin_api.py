#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc
import copy
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/apis/plugin', '', _path))
from apis.messageable.messageable_api import MessageableApi  # noqa
from apis.renderable.renderable_api import RenderableApi  # noqa
from apis.runnable.runnable_api import RunnableApi  # noqa
from utils.abc.abc_util import abstractstatic  # noqa
from value.notify.notify_value import NotifyValue  # noqa
from value.response.response_value import ResponseValue  # noqa


class PluginApi(MessageableApi, RunnableApi):
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        super(PluginApi, self).__init__(**kwargs)
        self.shadow = {}

    @abc.abstractproperty
    def enabled(self):
        pass

    @abstractstatic
    def _info():
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

    def _attachments(self):
        if not isinstance(self, RenderableApi):
            return []

        info = self._info()
        title = 'Fairylab | ' + self._title()
        link = 'http://orangeandblueleaguebaseball.com' + self._href()
        return [{
            'fallback': info,
            'title': title,
            'title_link': link,
            'text': info
        }]

    def _notify(self, **kwargs):
        if self._notify_internal(**kwargs):
            return ResponseValue(notify=[NotifyValue.BASE])
        return ResponseValue()

    def _setup(self, **kwargs):
        self._setup_internal(**kwargs)
        return ResponseValue(shadow=self._shadow_internal(**kwargs))

    def _shadow(self, **kwargs):
        self.shadow.update(copy.deepcopy(kwargs['shadow']))
        return ResponseValue()
