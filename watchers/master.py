#!/usr/bin/env python

import argparse
import export_watcher
import os
import re
import sim_watcher
import time
import urllib2


class Master(object):
  """Schedules the export and sim watching."""

  def __init__(self):
    """Does an initial parse of the exports page."""
    self.exportWatcher = export_watcher.ExportWatcher()
    self.simWatcher = sim_watcher.SimWatcher()

  def start(self):
    value = self.exportWatcher.watchTeamExports()
    if not value:
      return

    value = self.simWatcher._watchLiveSim()
    if not value:
      return

    self.exportWatcher.watchLeagueFile()

if __name__ == "__main__":
  master = Master()
  master.start()