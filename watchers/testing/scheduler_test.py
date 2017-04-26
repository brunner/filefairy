#!/usr/bin/env python

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import threading

from PyQt4.QtGui import QApplication
from export_watcher_test import ExportWatcherTest
from logger import TestLogger
from scheduler import Scheduler
from sim_watcher_test import SimWatcherTest
from utils import assertEquals, getExportUrls, getSimUrls


class SchedulerTest(Scheduler):
  """Tests for Scheduler."""

  def __init__(
          self, logger, fileIsUp, simIsInProgress, app, exportUrls, simUrls):
    """Initializes test watchers."""
    self.logger = logger

    self.fileIsUp = fileIsUp
    self.simIsInProgress = simIsInProgress

    self.exportWatcher = ExportSchedulerTest(exportUrls)
    self.simWatcher = SimSchedulerTest(app, simUrls)


class ExportSchedulerTest(ExportWatcherTest):
  """ExportWatcherTest with a more realistic sleep duration."""

  def getWatchLeagueFileValues(self):
    """Returns a pair of test values, in seconds."""
    return [4, 24]


class SimSchedulerTest(SimWatcherTest):
  """SimWatcherTest with a more realistic sleep duration."""

  def getWatchLiveSimValues(self):
    """Returns a pair of test values, in seconds."""
    return [1, 3, 20]


class EventTest(threading._Event):
  """Logs Event information."""

  def __init__(self, logger, tag):
    self.logger = logger
    self.tag = tag
    threading._Event.__init__(self)

  def set(self):
    self.logger.log("Set event for {0}".format(self.tag))
    super(EventTest, self).set()

  def clear(self):
    self.logger.log("Cleared event for {0}".format(self.tag))
    super(EventTest, self).clear()

  def is_set(self):
    self.logger.log("Checked event for {0}".format(self.tag))
    return super(EventTest, self).is_set()


exportUrls = getExportUrls()
simUrls = getSimUrls()


def testStart(app):
  logger = TestLogger()

  fileIsUp = EventTest(logger, "fileIsUp")
  simIsInProgress = EventTest(logger, "simIsInProgress")

  schedulerTest = SchedulerTest(
      logger, fileIsUp, simIsInProgress, app, exportUrls, simUrls)

  schedulerTest.start()
  logs = schedulerTest.logger.dump()

  # t = 0. Logged by Scheduler.start().
  # Scheduler starts an ExportWatcher object.
  assertEquals(logs[0], "[0:0:0] Starting export watcher.")

  # t = 0. Logged by ExportWatcher.watchLeagueFileInternal().
  # ExportWatcher immediately checks if the sim is in progress.
  assertEquals(logs[1], "[0:0:0] Checked event for simIsInProgress")

  # t = 0. Logged by Scheduler.start().
  # Scheduler starts a SimWatcher object.
  assertEquals(logs[2], "[0:0:0] Starting sim watcher.")

  # t ~= 2. Logged by SimWatcher.watchLiveSimInternal().
  # SimWatcher finds the first page with finals after two refreshes.
  assertEquals(logs[3], "[0:0:0] Set event for simIsInProgress")

  # t ~= 4. Logged by ExportWatcher.watchLeagueFileInternal().
  # ExportWatcher checks a second time if the sim is in progress.
  # It is, so the ExportWatcher should not be checking if the file is up.
  assertEquals(logs[4], "[0:0:0] Checked event for simIsInProgress")

  # t ~= 8. Logged by ExportWatcher.watchLeagueFileInternal().
  # ExportWatcher checks a third time if the sim is in progress.
  # Meanwhile, SimWatcher should be capturing and uploading sim pages.
  assertEquals(logs[5], "[0:0:0] Checked event for simIsInProgress")

  # t ~= 10. Logged by SimWatcher.watchLiveSimInternal().
  # SimWatcher pauses to upload two images after t ~= 6. Each upload takes
  #   t ~= 2 extra.
  assertEquals(logs[6], "[0:0:0] Cleared event for simIsInProgress")

  # t ~= 10. Logged by SimWatcher.watchLiveSimInternal().
  # After uploading, SimWatcher checks if the file is up. It is not.
  assertEquals(logs[7], "[0:0:0] Checked event for fileIsUp")

  # t ~= 12. Logged by ExportWatcher.watchLeagueFileInternal().
  # ExportWatcher checks a fourth time if the sim is in progress. It is not,
  #   which means ExportWatcher can resume checking if the file is up.
  assertEquals(logs[8], "[0:0:0] Checked event for simIsInProgress")

  # t ~= 13. Logged by SimWatcher.watchLiveSimInternal().
  # SimWatcher pauses again to check if the file is up. It is not.
  assertEquals(logs[9], "[0:0:0] Checked event for fileIsUp")

  # t ~= 16. Logged by ExportWatcher.watchLeagueFileInternal().
  # ExportWatcher checks a fifth time if the sim is in progress. It is not,
  #   which means ExportWatcher can check again if the file is up. This time,
  #   it is.
  assertEquals(logs[10], "[0:0:0] Checked event for simIsInProgress")

  # t ~= 16. Logged by ExportWatcher.watchLeagueFileInternal().
  # ExportWatcher determines that the file is up and sets the event.
  assertEquals(logs[11], "[0:0:0] Set event for fileIsUp")

  # t ~= 16. Logged by SimWatcher.watchLiveSimInternal().
  # After another pause, SimWatcher checks if the file is up. It is.
  assertEquals(logs[12], "[0:0:0] Checked event for fileIsUp")

  # t ~= 16. Logged by Scheduler.start().
  # Both ExportWatcher and SimWatcher terminate now that the file is up.
  assertEquals(logs[13], "[0:0:0] Joined watcher threads.")


if __name__ == "__main__":
  app = QApplication(sys.argv)

  testStart(app)

  print "Passed."
