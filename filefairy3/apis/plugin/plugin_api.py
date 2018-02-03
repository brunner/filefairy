#!/usr/bin/env python

import abc
import os
import re
import sys
import time

import logging
logging.basicConfig()

sys.path.append(re.sub(r'/apis/plugin', '', os.path.dirname(__file__)))
from utils.abc.abc_util import abstractstatic
from utils.slack.slack_util import contains_text, from_channel, testing_id
from utils.subprocess.subprocess_util import check_output


class PluginApi(object):
  __metaclass__ = abc.ABCMeta

  def __init__(self):
    self.data = self.__data__()
    self.name = self.__class__.__name__.lower()

    self.read()

  @abstractstatic
  def __data__():
    pass

  def push(self):
    check_output(['git', 'add', self.data])
    check_output(['git', 'commit', '-m', 'Automated data push for ' + self.name + '.'])
    check_output(['git', 'push', 'origin', 'master'])

  def on_message(self, obj):
    if from_channel(obj, testing_id) and contains_text(obj, self.name):
      for method in dir(self):
        if contains_text(obj, self.name + '.' + method):
          item = getattr(self, method)
          if callable(item):
            return item()

    return self.__on_message__(obj)


  @abc.abstractmethod
  def __on_message__(self, obj):
    pass

  @abc.abstractmethod
  def run(self):
    pass

  @abc.abstractmethod
  def read(self):
    pass

  @abc.abstractmethod
  def write(self):
    pass
