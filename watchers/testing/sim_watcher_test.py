#!/usr/bin/env python

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
import screenshot
import slack
import threading
import urllib2

from PyQt4.QtGui import QApplication
from logger import TestLogger
from sim_watcher import SimWatcher
from utils import assertEquals, assertNotEquals, getSimUrls

class SimWatcherTest(SimWatcher):
  """Tests for SimWatcher."""

  def __init__(self, logger, app, urls, slack=False):
    """Stores a few test sim urls.

    Pass slack=True to interface with the testing Slack channel."""
    self.logger = logger

    self.urls = urls
    self.current = self.urls[0]
    self.captured = []
    self.posted = []
    self.slack = slack

    self.page = self.getPage(self.current)
    self.date = self.findDate(self.page)
    self.finals = self.findFinals(self.page)
    self.records = self.initializeRecords()
    self.updates = self.findUpdates(self.page)
    self.started = False
    self.pages = {}
    self.inProgress = False

    self.screenshot = screenshot.Screenshot(app, self.getImagesPath())

    self.updateLiveSim(self.current)

  def capture(self, html, filename):
    """Stores the captured file for asserting."""
    self.captured.append(filename)
    if self.slack:
      super(SimWatcherTest, self).capture(html, filename)

  def postMessage(self, message, channel):
    """Stores the message for asserting. Channel is overridden."""
    self.posted.append(message)
    if self.slack:
      slack.postMessage(message, "testing")

  def upload(self, filename, channel):
    """Stores the PNG screenshot for asserting. Channel is overridden."""
    self.posted.append(filename)
    if self.slack:
      slack.upload(self.getImagesPath(), filename, "testing")

  def getUrl(self):
    """Returns the next test sim page."""
    if len(self.urls) > 1:
      self.current = self.urls.pop(0)
    else:
      self.current = self.urls[0]

    return self.current

  def getWatchLiveSimValues(self):
    """Returns a tuple of test values, in seconds, for the watchLiveSim timer."""
    return [1, 2, 4]

  def sendAlert(self, value):
    """Returns an easily assertable value."""
    records = {k: v for k, v in self.records.iteritems() if
               v["W"] or v["L"] or v["T"]}
    return {
        "value": value,
        "current": self.current,
        "date": self.date,
        "finals": self.finals,
        "records": records,
        "captured": self.captured,
    }


fileIsUp = threading.Event()
simIsInProgress = threading.Event()

urls = getSimUrls()

dates = {
    "old": "09052018",
    "new": "09092018",
}

files = {
    "old": "sim09052018.png",
    "new": "sim09092018.png",
}

finals = {
    "old1": set(["5933"]),
    "old2": set(["5933", "5345"]),
    "new1": set(["4952", "5035", "4254"]),
    "new2": set(["5331", "3348", "4151", "3456", "3637", "5035", "4254",
                 "3955", "4645", "5847", "4038", "4952", "6032", "4459",
                 "4357"]),
}

win1 = {"W": 1, "L": 0, "T": 0}
loss1 = {"W": 0, "L": 1, "T": 0}
loss2 = {"W": 0, "L": 2, "T": 0}
split = {"W": 1, "L": 1, "T": 0}
records = {
    54: win1, 42: loss1, 50: loss1, 35: win1, 49: win1, 52: loss1,
    32: win1, 60: loss1, 58: win1, 47: loss1, 44: win1, 59: split,
    46: win1, 45: split, 51: win1, 41: loss1, 33: split, 48: loss1,
    38: win1, 40: loss1, 39: win1, 55: loss1, 31: win1, 53: loss2,
    43: win1, 57: loss1, 34: win1, 56: loss1, 37: win1, 36: loss1
}

updates = {
    "update1": ":toparrow: 4 :separator: :pirates: 10 " +
    ":separator: :giants: 0\n:pirates: C.J. Hinojosa " +
    "hits a 3-run HR.",
    "update2": ":bottomarrow: 5 :separator: :pirates: " +
    "10 :separator: :giants: 2\n:giants: David " +
    "Olmedo-Barrera hits a 2-run HR."
}

logs = [
    "[0:0:0] Started watching live sim.",
    "[0:0:0] Saved 2 finals on 09052018.",
    "[0:0:0] Saved 3 finals on 09092018.",
    "[0:0:0] Saved 15 finals on 09092018.",
    "[0:0:0] Ignored 3 finals on 09092018.",
    "[0:0:0] Uploaded sim09052018.png.",
    "[0:0:0] Uploaded sim09092018.png.",
    "[0:0:0] Posted records.",
    "[0:0:0] Done watching live sim: success.",
    "[0:0:0] Done watching live sim: failure.",
]


def testReal(app):
  url = "http://orangeandblueleaguebaseball.com/league/OBL/reports/news/html/real_time_sim/index.html"
  page = urllib2.urlopen(url).read()
  simWatcherTest = SimWatcherTest(TestLogger(), app, [url])

  assertNotEquals(simWatcherTest.findDate(page), "")
  assertNotEquals(simWatcherTest.findFinals(page), [])


def testFindDate(app):
  simWatcherTest = SimWatcherTest(TestLogger(), app, urls[:])

  page = urllib2.urlopen(urls[0]).read()
  assertEquals(simWatcherTest.findDate(page), dates["old"])

  page = urllib2.urlopen(urls[1]).read()
  assertEquals(simWatcherTest.findDate(page), dates["old"])

  page = urllib2.urlopen(urls[2]).read()
  assertEquals(simWatcherTest.findDate(page), dates["old"])

  page = urllib2.urlopen(urls[3]).read()
  assertEquals(simWatcherTest.findDate(page), dates["new"])

  page = urllib2.urlopen(urls[4]).read()
  assertEquals(simWatcherTest.findDate(page), dates["new"])

  page = urllib2.urlopen(urls[5]).read()
  assertEquals(simWatcherTest.findDate(page), dates["new"])


def testFindFinals(app):
  simWatcherTest = SimWatcherTest(TestLogger(), app, urls[:])

  page = urllib2.urlopen(urls[0]).read()
  assertEquals(simWatcherTest.findFinals(page), finals["old1"])

  page = urllib2.urlopen(urls[1]).read()
  assertEquals(simWatcherTest.findFinals(page), finals["old1"])

  page = urllib2.urlopen(urls[2]).read()
  assertEquals(simWatcherTest.findFinals(page), finals["old2"])

  page = urllib2.urlopen(urls[3]).read()
  assertEquals(simWatcherTest.findFinals(page), finals["new1"])

  page = urllib2.urlopen(urls[4]).read()
  assertEquals(simWatcherTest.findFinals(page), finals["new2"])

  page = urllib2.urlopen(urls[5]).read()
  assertEquals(simWatcherTest.findFinals(page), finals["new1"])


def testFindUpdates(app):
  simWatcherTest = SimWatcherTest(TestLogger(), app, urls[:])

  page = urllib2.urlopen(urls[0]).read()
  assertEquals(simWatcherTest.findUpdates(page), [updates["update1"]])

  page = urllib2.urlopen(urls[1]).read()
  assertEquals(simWatcherTest.findUpdates(page), [])

  page = urllib2.urlopen(urls[2]).read()
  assertEquals(simWatcherTest.findUpdates(page), [updates["update2"]])

  page = urllib2.urlopen(urls[3]).read()
  assertEquals(simWatcherTest.findUpdates(page), [])

  page = urllib2.urlopen(urls[4]).read()
  assertEquals(simWatcherTest.findUpdates(page), [])

  page = urllib2.urlopen(urls[5]).read()
  assertEquals(simWatcherTest.findUpdates(page), [])


def testUpdateLiveSim(app, slack):
  simWatcherTest = SimWatcherTest(TestLogger(), app, urls[:], slack)

  expected = {"value": False, "current": urls[0], "date": dates["old"],
              "finals": finals["old1"], "records": {}, "captured": []}
  assertEquals(simWatcherTest.updateLiveSim(), expected)

  expected = {"value": False, "current": urls[1], "date": dates["old"],
              "finals": finals["old1"], "records": {}, "captured": []}
  assertEquals(simWatcherTest.updateLiveSim(), expected)

  expected = {"value": True, "current": urls[2], "date": dates["old"],
              "finals": finals["old2"], "records": {}, "captured": []}
  assertEquals(simWatcherTest.updateLiveSim(), expected)

  expected = {"value": True, "current": urls[3], "date": dates["new"],
              "finals": finals["new1"], "records": {}, "captured": []}
  assertEquals(simWatcherTest.updateLiveSim(), expected)

  expected = {"value": True, "current": urls[4], "date": dates["new"],
              "finals": finals["new2"], "records": {}, "captured": []}
  assertEquals(simWatcherTest.updateLiveSim(), expected)

  expected = {"value": False, "current": urls[5], "date": dates["new"],
              "finals": finals["new2"], "records": {}, "captured": []}
  assertEquals(simWatcherTest.updateLiveSim(), expected)

  expected = {"value": False, "current": urls[5], "date": dates["new"],
              "finals": finals["new2"], "records": {}, "captured": []}
  assertEquals(simWatcherTest.updateLiveSim(), expected)

  assertEquals(simWatcherTest.logger.dump(), logs[1:5])

  simWatcherTest = SimWatcherTest(TestLogger(), app, urls[:1], slack)

  expected = {"value": False, "current": urls[0], "date": dates["old"],
              "finals": finals["old1"], "records": {}, "captured": []}
  assertEquals(simWatcherTest.updateLiveSim(), expected)

  expected = {"value": False, "current": urls[0], "date": dates["old"],
              "finals": finals["old1"], "records": {}, "captured": []}
  assertEquals(simWatcherTest.updateLiveSim(), expected)

  assertEquals(simWatcherTest.logger.dump(), [])


def testWatchLiveSimInternal(app, slack):
  simWatcherTest = SimWatcherTest(TestLogger(slack), app, urls[:], slack)

  expected = {"value": True, "current": urls[5], "date": dates["new"],
              "finals": finals["new2"], "records": records,
              "captured": [files["old"], files["new"]]}
  assertEquals(
      simWatcherTest.watchLiveSimInternal(fileIsUp, simIsInProgress),
      expected)
  assertEquals(simWatcherTest.logger.dump(), logs[:-1])

  simWatcherTest = SimWatcherTest(TestLogger(slack), app, urls[:1], slack)

  expected = {"value": False, "current": urls[0], "date": dates["old"],
              "finals": finals["old1"], "records": {}, "captured": []}
  assertEquals(
      simWatcherTest.watchLiveSimInternal(fileIsUp, simIsInProgress),
      expected)
  assertEquals(simWatcherTest.logger.dump(), [logs[0], logs[-1]])


def testWatchLiveSim(app, slack):
  simWatcherTest = SimWatcherTest(TestLogger(slack), app, urls[:], slack)
  assertEquals(simWatcherTest.watchLiveSim(fileIsUp, simIsInProgress), True)
  assertEquals(simWatcherTest.logger.dump(), logs[:-1])

  simWatcherTest = SimWatcherTest(TestLogger(slack), app, urls[:1], slack)
  assertEquals(simWatcherTest.watchLiveSim(fileIsUp, simIsInProgress), False)
  assertEquals(simWatcherTest.logger.dump(), [logs[0], logs[-1]])


if __name__ == "__main__":
  app = QApplication(sys.argv)

  parser = argparse.ArgumentParser()
  parser.add_argument('--mode', dest='mode')
  parser.add_argument('--slack', dest='slack', action='store_true')
  parser.set_defaults(slack=False)
  args = parser.parse_args()

  if args.mode == "real" or args.mode == "all":
    testReal(app)

  if args.mode == "date" or args.mode == "all":
    testFindDate(app)

  if args.mode == "finals" or args.mode == "all":
    testFindFinals(app)

  if args.mode == "updates" or args.mode == "all":
    testFindUpdates(app)

  if args.mode == "livesim" or args.mode == "all":
    testUpdateLiveSim(app, args.slack)

  if args.mode == "internal" or args.mode == "all":
    testWatchLiveSimInternal(app, args.slack)

  if args.mode == "watch" or args.mode == "all":
    testWatchLiveSim(app, args.slack)

  print "Passed."