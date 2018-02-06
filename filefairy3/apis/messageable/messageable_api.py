#!/usr/bin/env python

import abc
import os
import re
import sys

sys.path.append(
    re.sub(r'/apis/messageable', '', os.path.dirname(
        os.path.abspath(__file__))))
from apis.nameable.nameable_api import NameableApi  # noqa
from utils.slack.slack_util import chat_post_message, contains_text, from_channel, testing_id, testing_name  # noqa


class MessageableApi(NameableApi):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(MessageableApi, self).__init__()

    def _name(self):
        return self.__class__.__name__

    @abc.abstractmethod
    def _on_message_internal(self, obj):
        pass

    def _on_message(self, obj):
        if from_channel(obj, testing_id) and contains_text(obj, self._name()):
            for method in dir(self):
                if method.startswith('_'):
                    continue
                if contains_text(obj, self._name() + '.' + method + '()'):
                    item = getattr(self, method)
                    if callable(item):
                        return item(v='true')

        return self._on_message_internal(obj)
