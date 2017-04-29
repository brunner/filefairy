#!/usr/bin/env python

import slack
import threading

from export_watcher import ExportWatcher
from logger import Logger
from sim_watcher import SimWatcher


class Scheduler(object):
  """Schedules the export and sim watching."""

  def __init__(self, logger, fileIsUp, simIsInProgress):
    self.logger = logger

    self.fileIsUp = fileIsUp
    self.simIsInProgress = simIsInProgress

    self.exportWatcher = ExportWatcher()
    self.simWatcher = SimWatcher()

  def start(self):
    p1 = threading.Thread(target=self.exportWatcher.watchLeagueFile,
                          args=(self.fileIsUp, self.simIsInProgress,))
    self.logger.log("Starting export watcher.")
    p1.start()

    p2 = threading.Thread(target=self.simWatcher.watchLiveSim,
                          args=(self.fileIsUp, self.simIsInProgress,))
    self.logger.log("Starting sim watcher.")
    p2.start()

    p1.join()
    p2.join()
    self.logger.log("Joined watcher threads.")

  def postMessage(self, message, channel):
    slack.postMessage(message, channel)


if __name__ == "__main__":
  logger = Logger()
  fileIsUp = threading.Event()
  simIsInProgress = threading.Event()

  scheduler = Scheduler(logger, fileIsUp, simIsInProgress)
  scheduler.start()
