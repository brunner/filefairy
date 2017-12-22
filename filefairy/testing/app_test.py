#!/usr/bin/env python

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import App


class AppTest(App):

  def __init__(self, file_url='', playoffs_in='', standings_in=''):
    self.file_url = file_url
    self.playoffs_in = playoffs_in
    self.standings_in = standings_in

  def get_path(self):
    return os.path.expanduser('~') + '/orangeandblueleague/filefairy/testing/'

  def get_playoffs_out(self):
    return self.get_path() + 'data/playoffs_out.txt'

  def get_standings_out(self):
    return self.get_path() + 'data/standings_out.txt'

  def get_general_name(self):
    return 'testing'

  def get_live_sim_discussion_name(self):
    return 'testing'

  def get_statsplus_id(self):
    return 'G3SUFLMK4'

  def get_timer_values(self):
    return [2, 10]

  def get_page(self, url):
    path = self.get_path()
    cwd = os.getcwd()
    os.chdir(path)
    page = ''
    if url:
      with open(url, 'r') as f:
        page = f.read()
    os.chdir(cwd)
    return page
