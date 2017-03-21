#!/usr/bin/env python

import argparse
import export_watcher
import multiprocessing
import os
import re
import sim_watcher
import time
import urllib2


class Scheduler(object):
  """Schedules the export and sim watching."""

  def __init__(self):
    self.exportWatcher = export_watcher.ExportWatcher()
    self.simWatcher = sim_watcher.SimWatcher()

  def start(self):
    #p1 = multiprocessing.Process(target=self.simWatcher.watchLiveSim)
    p2 = multiprocessing.Process(target=self.exportWatcher.watchLeagueFile)

    #p1.start()
    p2.start()

    #p1.join()
    p2.join()

if __name__ == "__main__":
  scheduler = Scheduler()
  scheduler.start()
