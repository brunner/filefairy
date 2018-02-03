#!/usr/bin/env python

import os
import re
import sys

import logging
logging.basicConfig()

sys.path.append(re.sub(r'/plugins/league_file', '', os.path.dirname(__file__)))
from apis.base_plugin.base_plugin_api import BasePluginApi
from utils.slack.slack_util import chat_post_message, testing_name
from utils.subprocess.subprocess_util import check_output


class GitPlugin(BasePluginApi):

  def _on_message_internal(self, obj):
    pass

  def _run_internal(self):
    pass

  def _call(self, cmd):
    out = check_output(cmd)
    chat_post_message(testing_name, out.strip('\n'))

  def add(self):
    self._call(['git', 'add' '.'])

  def commit(self):
    self._call(['git', 'commit', '-m', 'Automated data push.'])

  def pull(self):
    self._call(['git', 'pull'])

  def push(self):
    self._call(['git', 'push', 'origin', 'master'])

  def reset(self):
    self._call(['git', 'reset', '--hard'])

  def status(self):
    self._call(['git', 'status'])
