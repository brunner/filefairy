#!/usr/bin/env python

import copy
import json
import os
import re
import subprocess
import sys

sys.path.append(re.sub(r'/plugins/league_file', '', os.path.dirname(__file__)))
from apis.plugin.plugin_api import PluginApi
from private.server import user, league_file_dir
from utils.subprocess.subprocess_util import check_output

size_pattern = '(\d+)'
date_pattern = '(\w+\s\d+\s\d+:\d+)'
name_pattern = '(orange_and_blue_league_baseball.tar.gz(?:.filepart)?)'
line_pattern = '\s'.join([size_pattern, date_pattern, name_pattern])


class LeagueFilePlugin(PluginApi):

  @staticmethod
  def __data__():
    return os.path.join(os.path.dirname(__file__), 'data.txt')

  def __on_message__(self, obj):
    pass

  def run(self):
    original_filepart = copy.deepcopy(self.filepart)
    original_finished = copy.deepcopy(self.finished)

    output = check_output(['ssh', user, 'ls -l ' + league_file_dir])
    for line in output.splitlines():
      line = re.sub(r'\s+', ' ', line)
      match = re.findall(line_pattern, line)
      if match:
        size, date, name = match[0]
        if '.filepart' in name:
          if not self.filepart:
            self.filepart = {'start': date}
          self.filepart['size'] = size
          self.filepart['end'] = date
        elif self.filepart and '.filepart' not in output:
          self.filepart['size'] = size
          self.filepart['date'] = date
          if not len(self.finished) or self.finished[0]['date'] != date:
            self.finished.insert(0, copy.deepcopy(self.filepart))
          self.filepart = None

    if self.filepart != original_filepart or self.finished != original_finished:
      self.write()

  def read(self):
    with open(self.data, 'r') as f:
      obj = json.loads(f.read())
      self.filepart = copy.deepcopy(obj['filepart'])
      self.finished = copy.deepcopy(obj['finished'])

  def write(self):
    with open(self.data, 'w') as f:
      obj = {'filepart': self.filepart, 'finished': self.finished}
      f.write(json.dumps(obj))
