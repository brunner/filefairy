#!/usr/bin/env python

import argparse
import export_watcher
import os
import re
import sim_watcher
import threading
import time
import urllib2


class Scheduler(object):
  """Schedules the export and sim watching."""

  def __init__(self):
    self.exportWatcher = export_watcher.ExportWatcher()
    self.simWatcher = sim_watcher.SimWatcher()

  def start(self):
    up = threading.Event()

    p1 = threading.Thread(target=self.exportWatcher.watchLeagueFile, args=(up,))
    p2 = threading.Thread(target=self.simWatcher.watchLiveSim, args=(up,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

if __name__ == "__main__":
  scheduler = Scheduler()
  scheduler.start()
