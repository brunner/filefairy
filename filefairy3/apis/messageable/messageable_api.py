#!/usr/bin/env python

import abc
import os
import re
import sys

sys.path.append(re.sub(r'/apis/plugin', '', os.path.dirname(os.path.abspath(__file__))))
from utils.slack.slack_util import chat_post_message, contains_text, from_channel, testing_id, testing_name  # noqa


class MessageableApi(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(MessageableApi, self).__init__()
        self.name = self.__class__.__name__

    def _chats(self, s, d, args):
        if '-v' in args:
            ds = '\n' + d if d else ''
            chat_post_message(testing_name, '(' + self.name + ') ' + s + ds)

        return d

    @abc.abstractmethod
    def _on_message_internal(self, obj):
        pass

    def _on_message(self, obj):
        if from_channel(obj, testing_id) and contains_text(obj, self.name):
            for method in dir(self):
                if method.startswith('_'):
                    continue
                if contains_text(obj, self.name + '.' + method + '()'):
                    item = getattr(self, method)
                    if callable(item):
                        return item('-v')

        return self._on_message_internal(obj)
