#!/usr/bin/env python

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
import datetime
import re
import slack
import threading
import time
import urllib2

from export_watcher import ExportWatcher
from utils import assertEquals, assertNotEquals

class ExportWatcherTest(ExportWatcher):
  """Tests for ExportWatcher."""

  def __init__(self, urls, slack=False):
    """Stores a few test export urls and teams.

    Pass slack=True to interface with the testing Slack channel."""
    self.urls = urls
    self.current = self.urls[0]
    self.posted = []
    self.slack = slack

    self.file = ""
    self.updateLeagueFile(self.current)

  def postToSlack(self, message, channel):
    """Stores the message for asserting. Channel is overridden."""
    self.posted.append(message)
    if self.slack:
      slack.postMessage(message, "testing")

  def getUrl(self):
    """Returns the next test export page."""
    if len(self.urls) > 1:
      self.current = self.urls.pop(0)
    else:
      self.current = self.urls[0]

    return self.current

  def getWatchLeagueFileValues(self):
    """Returns a pair of test values, in seconds."""
    return [1, 4]

  def sendAlert(self, value):
    """Returns an easily assertable value."""
    return {
        "value": value,
        "current": self.current,
        "file": self.file,
        "posted": self.posted,
    }

  def checkAlert(self, alert):
    """Returns the value of the alert."""
    return alert["value"]


fileIsUp = threading.Event()
simIsInProgress = threading.Event()

path = "http://brunnerj.com/orangeandblueleague/"
files = [
    "export_01142017_1.html",         # 0. Initial exports page.
    "export_01142017_2.html",         # 1. League file date has not changed.
    "export_01172017_1.html",         # 3. League file date has changed.
]
urls = [os.path.join(path, fi) for fi in files]

league = {
    "old": "Saturday January 14, 2017 13:01:09 EST",
    "new": "Tuesday January 17, 2017 09:03:12 EST",
}

updates = {
    "file1": "Watching file.",
    "file2": "File is up.",
    "file3": "File date change not detected.",
}


def testReal():
  url = "http://orangeandblueleaguebaseball.com/StatsLab/exports.php"
  page = urllib2.urlopen(url).read()
  exportWatcherTest = ExportWatcherTest([url])

  assertNotEquals(exportWatcherTest.findLeagueFile(page), "")


def testFindLeagueFile():
  exportWatcherTest = ExportWatcherTest(urls[:])

  page = urllib2.urlopen(urls[0]).read()
  assertEquals(exportWatcherTest.findLeagueFile(page), league["old"])

  page = urllib2.urlopen(urls[1]).read()
  assertEquals(exportWatcherTest.findLeagueFile(page), league["old"])

  page = urllib2.urlopen(urls[2]).read()
  assertEquals(exportWatcherTest.findLeagueFile(page), league["new"])


def testUpdateLeagueFile():
  exportWatcherTest = ExportWatcherTest(urls[:])

  expected = {"value": False, "current": urls[0], "file": league["old"],
              "posted": []}
  assertEquals(exportWatcherTest.updateLeagueFile(), expected)

  expected = {"value": False, "current": urls[1], "file": league["old"],
              "posted": []}
  assertEquals(exportWatcherTest.updateLeagueFile(), expected)

  expected = {"value": True, "current": urls[2], "file": league["new"],
              "posted": []}
  assertEquals(exportWatcherTest.updateLeagueFile(), expected)

  expected = {"value": False, "current": urls[2], "file": league["new"],
              "posted": []}
  assertEquals(exportWatcherTest.updateLeagueFile(), expected)

  exportWatcherTest = ExportWatcherTest(urls[:2])

  expected = {"value": False, "current": urls[0], "file": league["old"],
              "posted": []}
  assertEquals(exportWatcherTest.updateLeagueFile(), expected)

  expected = {"value": False, "current": urls[1], "file": league["old"],
              "posted": []}
  assertEquals(exportWatcherTest.updateLeagueFile(), expected)

  expected = {"value": False, "current": urls[1], "file": league["old"],
              "posted": []}
  assertEquals(exportWatcherTest.updateLeagueFile(), expected)


def testWatchLeagueFileInternal(slack):
  exportWatcherTest = ExportWatcherTest(urls[:], slack)

  expected = {"value": True, "current": urls[2], "file": league["new"],
              "posted": [updates["file1"], updates["file2"]]}
  assertEquals(exportWatcherTest.watchLeagueFileInternal(simIsInProgress),
               expected)

  exportWatcherTest = ExportWatcherTest(urls[:2], slack)

  expected = {"value": False, "current": urls[1], "file": league["old"],
              "posted": [updates["file1"], updates["file3"]]}
  assertEquals(exportWatcherTest.watchLeagueFileInternal(simIsInProgress),
               expected)


def testWatchLeagueFile(slack):
  exportWatcherTest = ExportWatcherTest(urls[:], slack)
  assertEquals(exportWatcherTest.watchLeagueFile(fileIsUp, simIsInProgress),
               True)

  exportWatcherTest = ExportWatcherTest(urls[:2], slack)
  assertEquals(exportWatcherTest.watchLeagueFile(fileIsUp, simIsInProgress),
               False)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--mode', dest='mode')
  parser.add_argument('--slack', dest='slack', action='store_true')
  parser.set_defaults(slack=False)
  args = parser.parse_args()

  if args.mode == "real" or args.mode == "all":
    testReal()

  if args.mode == "file" or args.mode == "all":
    testFindLeagueFile()

  if args.mode == "update" or args.mode == "all":
    testUpdateLeagueFile()

  if args.mode == "internal" or args.mode == "all":
    testWatchLeagueFileInternal(args.slack)

  if args.mode == "watch" or args.mode == "all":
    testWatchLeagueFile(args.slack)

  print "Passed."
