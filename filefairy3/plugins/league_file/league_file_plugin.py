#!/usr/bin/env python

import json
import os
import re
import subprocess
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from private.server import user, league_file_dir


path = '/orangeandblueleague/filefairy3/plugins/league_file/'


size_pattern = '(\d+)'
date_pattern = '(\w+\s\d+\s\d+:\d+)'
name_pattern = '(orange_and_blue_league_baseball.tar.gz(?:.filepart)?)'
line_pattern = '\s'.join([size_pattern, date_pattern, name_pattern])


class LeagueFilePlugin(object):

  def __init__(self, infile='data.txt'):
    self.infile = infile
    self.setup()

  def setup(self):
    if os.path.isfile(path + self.infile):
      with open

  def on_message(self, obj):
    pass

  def run(self):
    try:
      output = subprocess.check_output(['ssh', user, 'ls -l ' + league_file_dir])
    except:
      output = ''

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
        elif (not len(self.finished) or self.finished[0]['end'] != end) and self.filepart:
          self.filepart['size'] = size
          self.filepart['end'] = date
          self.finished.insert(0, self.filepart.copy())
          self.filepart = None
