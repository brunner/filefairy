#!/usr/bin/env python

import abc
import os
import re
import sys

import logging
logging.basicConfig()

sys.path.append(re.sub(r'/apis/plugin', '', os.path.dirname(__file__)))
from apis.base_plugin.base_plugin_api import BasePluginApi
from utils.abc.abc_util import abstractstatic


class DataPluginApi(BasePluginApi):
  __metaclass__ = abc.ABCMeta

  def __init__(self):
    super(DataPluginApi, self).__init__()
    self.data = self._data()

    self.read()

  @abc.abstractmethod
  def _on_message_internal(self, obj):
    pass

  @abc.abstractmethod
  def _run_internal(self):
    pass

  @abstractstatic
  def _data():
    pass

  @abc.abstractmethod
  def read(self):
    pass

  @abc.abstractmethod
  def write(self):
    pass
