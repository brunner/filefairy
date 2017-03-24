#!/usr/bin/env python

import argparse
import os
import screenshot
import slack
import sys
import urllib2

from PyQt4.QtGui import QApplication
from sim_watcher import SimWatcher


class SimWatcherTest(SimWatcher):
  """Tests for SimWatcher."""

  def __init__(self, app, urls, slack=False):
    """Stores a few test sim urls.

    Pass slack=True to interface with the testing Slack channel."""
    self.urls = urls
    self.current = self.urls[0]
    self.captured = []
    self.posted = []
    self.slack = slack

    self.page = self.getPage(self.current)
    self.date = self.findDate(self.page)
    self.finals = self.findFinals(self.page)
    self.updates = self.findUpdates(self.page)
    self.started = False
    self.pages = {}
    self.threads = []
    self.logs = []

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
    return [1, 2, 3]

  def sendAlert(self, value):
    """Returns an easily assertable value."""
    return {"value": value, "current": self.current, "date": self.date, "finals": self.finals, "captured": self.captured
            }


app = QApplication(sys.argv)

path = "http://brunnerj.com/orangeandblueleague/"
files = [
    "sim_09052018_1.html",            # 0. Initial sim page.
    "sim_09052018_2.html",            # 1. Same date. No new final games.
    "sim_09052018_3.html",            # 2. Same date. One new final game.
    "sim_09092018_1.html",            # 3. Different date, partially loaded.
    "sim_09092018_2.html",            # 4. Fully loaded.
    "sim_09092018_3.html",            # 5. Partially loaded again.
]
urls = [os.path.join(path, fi) for fi in files]

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
    "new2": set(["5331", "3348", "4151", "3456", "3637", "5035", "4254", "3955", "4645", "5847", "4038", "4952", "6032", "4459", "4357"]),
}

updates = {
    "update1": ":toparrow: 4 :separator: :pirates: 10 " +
    ":separator: :giants: 0\n:pirates: C.J. Hinojosa " +
    "hits a 3-run HR.",
    "update2": ":bottomarrow: 5 :separator: :pirates: " +
    "10 :separator: :giants: 2\n:giants: David " +
    "Olmedo-Barrera hits a 2-run HR."
}


def testReal():
  url = "http://orangeandblueleaguebaseball.com/league/OBL/reports/news/html/real_time_sim/index.html"
  page = urllib2.urlopen(url).read()
  simWatcherTest = SimWatcherTest(app, [url])

  assertNotEquals(simWatcherTest.findDate(page), "")
  assertNotEquals(simWatcherTest.findFinals(page), [])


def testFindDate():
  simWatcherTest = SimWatcherTest(app, urls[:])

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


def testFindFinals():
  simWatcherTest = SimWatcherTest(app, urls[:])

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


def testFindUpdates():
  simWatcherTest = SimWatcherTest(app, urls[:])

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


def testUpdateLiveSim(slack):
  simWatcherTest = SimWatcherTest(app, urls[:], slack)

  expected = {"value": False, "current": urls[0], "date": dates["old"],
              "finals": finals["old1"], "captured": []}
  assertEquals(simWatcherTest.updateLiveSim(), expected)

  expected = {"value": False, "current": urls[1], "date": dates["old"],
              "finals": finals["old1"], "captured": []}
  assertEquals(simWatcherTest.updateLiveSim(), expected)

  expected = {"value": True, "current": urls[2], "date": dates["old"],
              "finals": finals["old2"], "captured": []}
  assertEquals(simWatcherTest.updateLiveSim(), expected)

  expected = {"value": True, "current": urls[3], "date": dates["new"],
              "finals": finals["new1"], "captured": []}
  assertEquals(simWatcherTest.updateLiveSim(), expected)

  expected = {"value": True, "current": urls[4], "date": dates["new"],
              "finals": finals["new2"], "captured": []}
  assertEquals(simWatcherTest.updateLiveSim(), expected)

  expected = {"value": False, "current": urls[5], "date": dates["new"],
              "finals": finals["new2"], "captured": []}
  assertEquals(simWatcherTest.updateLiveSim(), expected)

  expected = {"value": False, "current": urls[5], "date": dates["new"],
              "finals": finals["new2"], "captured": []}
  assertEquals(simWatcherTest.updateLiveSim(), expected)

  simWatcherTest = SimWatcherTest(app, urls[:1], slack)

  expected = {"value": False, "current": urls[0], "date": dates["old"],
              "finals": finals["old1"], "captured": []}
  assertEquals(simWatcherTest.updateLiveSim(), expected)

  expected = {"value": False, "current": urls[0], "date": dates["old"],
              "finals": finals["old1"], "captured": []}
  assertEquals(simWatcherTest.updateLiveSim(), expected)


def testWatchLiveSimInternal(slack):
  simWatcherTest = SimWatcherTest(app, urls[:], slack)

  expected = {"value": True, "current": urls[5], "date": dates["new"],
              "finals": finals["new2"],
              "captured": [files["old"], files["new"]]}
  assertEquals(simWatcherTest.watchLiveSimInternal(), expected)

  simWatcherTest = SimWatcherTest(app, urls[:1], slack)

  expected = {"value": False, "current": urls[0], "date": dates["old"],
              "finals": finals["old1"], "captured": []}
  assertEquals(simWatcherTest.watchLiveSimInternal(), expected)


def testWatchLiveSim(slack):
  simWatcherTest = SimWatcherTest(app, urls[:], slack)
  assertEquals(simWatcherTest.watchLiveSim(), True)

  simWatcherTest = SimWatcherTest(app, urls[:1], slack)
  assertEquals(simWatcherTest.watchLiveSim(), False)


def assertEquals(actual, expected):
  if actual != expected:
    raise AssertionError(
        "Expected {0} to match {1}, but it didn't.".format(expected, actual))


def assertNotEquals(actual, expected):
  if actual == expected:
    raise AssertionError(
        "Expected {0} to not match {1}, but it did.".format(expected, actual))


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--mode', dest='mode')
  parser.add_argument('--slack', dest='slack', action='store_true')
  parser.set_defaults(slack=False)
  args = parser.parse_args()

  if args.mode == "real" or args.mode == "all":
    testReal()

  if args.mode == "date" or args.mode == "all":
    testFindDate()

  if args.mode == "finals" or args.mode == "all":
    testFindFinals()

  if args.mode == "updates" or args.mode == "all":
    testFindUpdates()

  if args.mode == "livesim" or args.mode == "all":
    testUpdateLiveSim(args.slack)

  if args.mode == "internal" or args.mode == "all":
    testWatchLiveSimInternal(args.slack)

  if args.mode == "watch" or args.mode == "all":
    testWatchLiveSim(args.slack)

  print "Passed."
