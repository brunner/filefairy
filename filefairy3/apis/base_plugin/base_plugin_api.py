#!/usr/bin/env python

import abc
import os
import re
import sys

import logging
logging.basicConfig()

sys.path.append(re.sub(r'/apis/plugin', '', os.path.dirname(__file__)))
from utils.slack.slack_util import contains_text, from_channel, testing_id


class BasePluginApi(object):
  __metaclass__ = abc.ABCMeta

  def __init__(self):
    self.name = self.__class__.__name__.lower()

  @abc.abstractmethod
  def _on_message_internal(self, obj):
    pass

  def _on_message(self, obj):
    if from_channel(obj, testing_id) and contains_text(obj, self.name):
      for method in dir(self):
        if method.startswith('_'):
          continue
        if contains_text(obj, self.name + '.' + method):
          item = getattr(self, method)
          if callable(item):
            return item()

    return self._on_message_internal(obj)

  @abc.abstractmethod
  def _run_internal(self):
    pass

  def _run(self):
    return self._run_internal()
