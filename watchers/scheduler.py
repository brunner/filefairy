#!/usr/bin/env python

import export_watcher
import logger
import sim_watcher
import threading


class Scheduler(object):
  """Schedules the export and sim watching."""

  def __init__(self, logger, fileIsUp, simIsInProgress):
    self.logger = logger

    self.fileIsUp = fileIsUp
    self.simIsInProgress = simIsInProgress

    self.exportWatcher = export_watcher.ExportWatcher()
    self.simWatcher = sim_watcher.SimWatcher()

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


if __name__ == "__main__":
  logger = logger.Logger()
  fileIsUp = threading.Event()
  simIsInProgress = threading.Event()

  scheduler = Scheduler(logger, fileIsUp, simIsInProgress)
  scheduler.start()
