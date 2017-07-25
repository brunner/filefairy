#!/usr/bin/env python

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
import filecmp
import screenshot
import slack
import urllib2

from PyQt4.QtGui import QApplication
from logger import TestLogger
from sim_watcher import SimWatcher
from utils import assertEquals, assertNotEquals


class SimWatcherTest(SimWatcher):
  """Tests for SimWatcher."""

  def __init__(self, logger, app, fileUrls, simUrls, slack=False):
    self.logger = logger
    self.screenshot = screenshot.Screenshot(app, self.getImagesPath())

    self.fileUrls, self.fileIndex = fileUrls, 0
    self.filePage = self.getPage(self.fileUrls[0])
    self.fileDate = self.findFileDate(self.filePage)

    self.simUrls, self.simIndex = simUrls, 0
    self.simPage = self.getPage(self.simUrls[0])
    self.simDate = self.findSimDate(self.simPage)
    self.finals = self.findFinals(self.simPage)
    self.updates = self.findUpdates(self.simPage)

    self.exports = self.readExports()

    self.pages, self.posts = {}, []
    self.records = {t: [0, 0, 0] for t in range(31, 61)}

    self.captured = []
    self.posted = []

    self.slack = slack

  def capture(self, html, filename):
    self.captured.append(filename)
    self.slack and self.screenshot.capture(html, filename)

  def postMessage(self, message, channel):
    self.posted.append(message)
    self.slack and super(SimWatcherTest, self).postMessage(message, "testing")

  def upload(self, filename, channel):
    self.posted.append(filename)
    self.slack and super(SimWatcherTest, self).upload(filename, "testing")

  def getFileUrl(self):
    if len(self.fileUrls) > self.fileIndex + 1:
      self.fileIndex = self.fileIndex + 1

    return self.fileUrls[self.fileIndex]

  def getSimUrl(self):
    if len(self.simUrls) > self.simIndex + 1:
      self.simIndex = self.simIndex + 1

    return self.simUrls[self.simIndex]

  def getExportsInputFile(self):
    return os.path.expanduser("~") + "/orangeandblueleague/watchers/testing/exportsin.txt"

  def getExportsOutputFile(self):
    return os.path.expanduser("~") + "/orangeandblueleague/watchers/testing/exportsout.txt"

  def getTimerValues(self):
    return [1, 2, 8]

  def getFindRecords(self, page):
    self.findRecords(page)
    return {k: v for k, v in self.records.iteritems() if sum(v)}

  def getWatch(self):
    self.watch()
    return {
        "collected": self.logger.collected,
        "captured": self.captured,
        "posted": self.posted
    }

  def getUpdateLeagueFile(self):
    ret = self.updateLeagueFile()
    self.logger.collect()
    return {
        "ret": ret,
        "collected": self.logger.collected,
        "index": self.fileIndex,
        "date": self.fileDate,
        "posted": self.posted,
    }

  def getUpdateLiveSim(self):
    ret = self.updateLiveSim()
    self.logger.collect()
    return {
        "ret": ret,
        "collected": self.logger.collected,
        "index": self.simIndex,
        "date": self.simDate,
        "finals": self.finals,
        "updates": self.updates,
        "posted": self.posted,
    }


path = "http://brunnerj.com/orangeandblueleague/"

filePages = [
    "export_01142017_1.html",         # 0. Initial exports page.
    "export_01142017_2.html",         # 1. League file date has not changed.
    "export_01142017_2.html",         # 2. League file date has not changed.
    "export_01172017_1.html",         # 3. League file date has changed.
]
fileUrls = [os.path.join(path, fi) for fi in filePages]

new1a = [0, 0, -1, []]
new1b = [0, 0, 0, []]
new2 = [1, 0, 1, [1]]
zero1 = [0, 1, 1, [0]]
zero2a = [1, 1, 1, [0, 1]]
zero2b = [0, 2, 2, [0, 0]]
five1 = [5, 1, 3, [1, 0, 1, 1, 1]]
five2 = [5, 2, 1, [1, 0, 1, 1, 1, 0]]
seven1 = [7, 2, 4, [1, 0, 1, 1, 0, 1, 1, 1, 1]]
seven2a = [8, 2, 5, [1, 0, 1, 1, 0, 1, 1, 1, 1, 1]]
seven2b = [7, 3, 1, [1, 0, 1, 1, 0, 1, 1, 1, 1, 0]]
nine1 = [9, 4, 5, [1, 0, 0, 1, 0, 1, 1, 1, 1, 1]]
nine2 = [9, 5, 1, [0, 0, 1, 0, 1, 1, 1, 1, 1, 0]]
ten1 = [10, 3, 6, [1, 1, 0, 0, 1, 1, 1, 1, 1, 1]]
ten2 = [10, 4, 1, [1, 0, 0, 1, 1, 1, 1, 1, 1, 0]]
eleven1 = [11, 2, 1, [1, 1, 0, 1, 1, 1, 1, 1, 0, 1]]
eleven2 = [11, 3, 1, [1, 0, 1, 1, 1, 1, 1, 0, 1, 0]]
twelve1 = [12, 1, 7, [1, 1, 0, 1, 1, 1, 1, 1, 1, 1]]
twelve2 = [12, 2, 1, [1, 0, 1, 1, 1, 1, 1, 1, 1, 0]]
thirteen1 = [13, 0, 13, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
thirteen2a = [14, 0, 14, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
thirteen2b = [13, 1, 1, [1, 1, 1, 1, 1, 1, 1, 1, 1, 0]]
exports1 = {
  31: zero1, 32: eleven1, 33: nine1, 34: nine1, 35: twelve1, 36: thirteen1,
  37: thirteen1, 38: ten1, 39: nine1, 40: thirteen1, 41: seven1, 42: twelve1,
  43: new1b, 44: ten1, 45: twelve1, 46: eleven1, 47: thirteen1, 48: nine1,
  49: seven1, 50: twelve1, 51: five1, 52: thirteen1, 53: nine1, 54: ten1,
  55: eleven1, 56: five1, 57: twelve1, 58: zero1, 59: ten1, 60: new1a,
}
exports2 = {
  31: zero2b, 32: eleven2, 33: nine2, 34: nine2, 35: twelve2, 36: thirteen2b,
  37: thirteen2b, 38: ten2, 39: nine2, 40: thirteen2a, 41: seven2b, 42: twelve2,
  43: new2, 44: ten2, 45: twelve2, 46: eleven2, 47: thirteen2b, 48: nine2,
  49: seven2a, 50: twelve2, 51: five2, 52: thirteen2b, 53: nine2, 54: ten2,
  55: eleven2, 56: five2, 57: twelve2, 58: zero2a, 59: ten2, 60: new1a,
}
teamids = [40, 43, 58, 49]

fileDates = {
    "old": "Saturday January 14, 2017 13:01:09 EST",
    "new": "Tuesday January 17, 2017 09:03:12 EST",
}

simPages = [
    "sim_09052018_1.html",            # 0. Initial sim page.
    "sim_09052018_2.html",            # 1. Same date. No new final games.
    "sim_09052018_3.html",            # 2. Same date. One new final game.
    "sim_09092018_1.html",            # 3. Different date, partially loaded.
    "sim_09092018_2.html",            # 4. Fully loaded.
    "sim_09092018_3.html",            # 5. Partially loaded again.
]
simUrls = [os.path.join(path, fi) for fi in simPages]

simDates = {
    "old": "09052018",
    "new": "09092018",
}

filenames = {
    "new": "sim09092018.png",
}

finals = {
    "new1": set(["4254", "4952", "5035"]),
    "new2": set(["3348", "3456", "3637", "3955", "4038", "4151", "4254",
                 "4357", "4459", "4645", "4952", "5035", "5331", "5847",
                 "6032"]),
}

win, loss = [1, 0, 0], [0, 1, 0]
findRecords = {
    "old1": {33: loss, 59: win},
    "old2": {33: loss, 45: win, 53: loss, 59: win},
    "new1": {35: win, 42: loss, 49: win, 50: loss, 52: loss, 54: win},
    "new2": {
        31: win, 32: win, 33: win, 34: win, 35: win, 36: loss,
        37: win, 38: win, 39: win, 40: loss, 41: loss, 42: loss,
        43: win, 44: win, 45: loss, 46: win, 47: loss, 48: loss,
        49: win, 50: loss, 51: win, 52: loss, 53: loss, 54: win,
        55: loss, 56: loss, 57: loss, 58: win, 59: loss, 60: loss,
    }
}
formatRecords = [
    "AL East\n"
    + ":orioles: 1-0 :separator: :redsox: 1-0 :separator: :yankees: 0-1 "
    + ":separator: :rays: 0-1 :separator: :jays: 0-1",
    "AL Central\n"
    + ":whitesox: 1-0 :separator: :indians: 1-0 :separator: :royals: 1-0 "
    + ":separator: :tigers: 0-1 :separator: :twins: 0-1",
    "AL West\n"
    + ":angels: 1-0 :separator: :mariners: 1-0 :separator: :rangers: 1-0 "
    + ":separator: :astros: 0-1 :separator: :athletics: 0-1",
    "NL East\n"
    + ":braves: 1-0 :separator: :mets: 1-0 :separator: :phillies: 1-0 "
    + ":separator: :marlins: 0-1 :separator: :nationals: 0-1",
    "NL Central\n"
    + ":reds: 1-0 :separator: :brewers: 1-0 :separator: :cubs: 0-1 "
    + ":separator: :pirates: 0-1 :separator: :cardinals: 0-1",
    "NL West\n"
    + ":dbacks: 1-0 :separator: :rockies: 1-0 :separator: :dodgers: 0-1 "
    + ":separator: :padres: 0-1 :separator: :giants: 0-1"]
postedRecords = "\n\n".join(formatRecords)

updates = {
    "update1": ":toparrow: 4 :separator: :pirates: 10 " +
    ":separator: :giants: 0\n:pirates: C.J. Hinojosa " +
    "hits a 3-run HR.",
    "update2": ":bottomarrow: 5 :separator: :pirates: " +
    "10 :separator: :giants: 2\n:giants: David " +
    "Olmedo-Barrera hits a 2-run HR."
}

logs = [
    "[00:00:00] Started watching.",             # 0
    "[00:00:00] Saved 3 finals on 09092018.",   # 1
    "[00:00:00] Saved 15 finals on 09092018.",  # 2
    "[00:00:00] Ignored 3 finals on 09092018.", # 3
    "[00:00:00] Uploaded sim09092018.png.",     # 4
    "[00:00:00] Posted records.",               # 5
    "[00:00:00] File is up.",                   # 6
    "[00:00:00] 4 teams exported.",             # 7
    "[00:00:00] Done watching.",                # 8
]


def testReal(app):
  fileUrl = "http://orangeandblueleaguebaseball.com/StatsLab/exports.php"
  filePage = urllib2.urlopen(fileUrl).read()

  simUrl = "http://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/real_time_sim/index.html"
  simPage = urllib2.urlopen(simUrl).read()

  simWatcherTest = SimWatcherTest(TestLogger(), app, [fileUrl], [simUrl])

  assertNotEquals(simWatcherTest.findFileDate(filePage), "")
  assertNotEquals(simWatcherTest.findSimDate(simPage), "")
  assertNotEquals(simWatcherTest.findFinals(simPage), [])


def testFindFileDate(app):
  simWatcherTest = SimWatcherTest(TestLogger(), app, fileUrls[:], simUrls[:])

  page = urllib2.urlopen(fileUrls[0]).read()
  assertEquals(simWatcherTest.findFileDate(page), fileDates["old"])

  page = urllib2.urlopen(fileUrls[1]).read()
  assertEquals(simWatcherTest.findFileDate(page), fileDates["old"])

  page = urllib2.urlopen(fileUrls[2]).read()
  assertEquals(simWatcherTest.findFileDate(page), fileDates["old"])

  page = urllib2.urlopen(fileUrls[3]).read()
  assertEquals(simWatcherTest.findFileDate(page), fileDates["new"])


def testFindExports(app):
  simWatcherTest = SimWatcherTest(TestLogger(), app, fileUrls[:], simUrls[:])

  page = urllib2.urlopen(fileUrls[0]).read()
  assertEquals(simWatcherTest.findExports(page), [])

  page = urllib2.urlopen(fileUrls[1]).read()
  assertEquals(simWatcherTest.findExports(page), teamids)

  page = urllib2.urlopen(fileUrls[2]).read()
  assertEquals(simWatcherTest.findExports(page), teamids)

  page = urllib2.urlopen(fileUrls[3]).read()
  assertEquals(simWatcherTest.findExports(page), [])


def testReadExports(app):
  simWatcherTest = SimWatcherTest(TestLogger(), app, fileUrls[:], simUrls[:])
  assertEquals(simWatcherTest.readExports(), exports1)


def testWriteExports(app):
  simWatcherTest = SimWatcherTest(TestLogger(), app, fileUrls[:], simUrls[:])
  assertEquals(simWatcherTest.writeExports(exports1, teamids), exports2)


def testFindSimDate(app):
  simWatcherTest = SimWatcherTest(TestLogger(), app, fileUrls[:], simUrls[:])

  page = urllib2.urlopen(simUrls[0]).read()
  assertEquals(simWatcherTest.findSimDate(page), simDates["old"])

  page = urllib2.urlopen(simUrls[1]).read()
  assertEquals(simWatcherTest.findSimDate(page), simDates["old"])

  page = urllib2.urlopen(simUrls[2]).read()
  assertEquals(simWatcherTest.findSimDate(page), simDates["old"])

  page = urllib2.urlopen(simUrls[3]).read()
  assertEquals(simWatcherTest.findSimDate(page), simDates["new"])

  page = urllib2.urlopen(simUrls[4]).read()
  assertEquals(simWatcherTest.findSimDate(page), simDates["new"])

  page = urllib2.urlopen(simUrls[5]).read()
  assertEquals(simWatcherTest.findSimDate(page), simDates["new"])


def testFindBoxes(app):
  simWatcherTest = SimWatcherTest(TestLogger(), app, fileUrls[:], simUrls[:])

  page = urllib2.urlopen(simUrls[0]).read()
  assertEquals(len(simWatcherTest.findBoxes(page)), 0)

  page = urllib2.urlopen(simUrls[1]).read()
  assertEquals(len(simWatcherTest.findBoxes(page)), 0)

  page = urllib2.urlopen(simUrls[2]).read()
  assertEquals(len(simWatcherTest.findBoxes(page)), 0)

  page = urllib2.urlopen(simUrls[3]).read()
  assertEquals(len(simWatcherTest.findBoxes(page)), 3)

  page = urllib2.urlopen(simUrls[4]).read()
  assertEquals(len(simWatcherTest.findBoxes(page)), 15)

  page = urllib2.urlopen(simUrls[5]).read()
  assertEquals(len(simWatcherTest.findBoxes(page)), 3)


def testFindFinals(app):
  simWatcherTest = SimWatcherTest(TestLogger(), app, fileUrls[:], simUrls[:])

  page = urllib2.urlopen(simUrls[0]).read()
  assertEquals(simWatcherTest.findFinals(page), set())

  page = urllib2.urlopen(simUrls[1]).read()
  assertEquals(simWatcherTest.findFinals(page), set())

  page = urllib2.urlopen(simUrls[2]).read()
  assertEquals(simWatcherTest.findFinals(page), set())

  page = urllib2.urlopen(simUrls[3]).read()
  assertEquals(simWatcherTest.findFinals(page), finals["new1"])

  page = urllib2.urlopen(simUrls[4]).read()
  assertEquals(simWatcherTest.findFinals(page), finals["new2"])

  page = urllib2.urlopen(simUrls[5]).read()
  assertEquals(simWatcherTest.findFinals(page), finals["new1"])


def testFindRecords(app):
  simWatcherTest = SimWatcherTest(TestLogger(), app, fileUrls[:], simUrls[:])

  page = urllib2.urlopen(simUrls[0]).read()
  assertEquals(simWatcherTest.getFindRecords(page), {})
  
  simWatcherTest = SimWatcherTest(TestLogger(), app, fileUrls[:], simUrls[:])

  page = urllib2.urlopen(simUrls[1]).read()
  assertEquals(simWatcherTest.getFindRecords(page), {})

  simWatcherTest = SimWatcherTest(TestLogger(), app, fileUrls[:], simUrls[:])

  page = urllib2.urlopen(simUrls[2]).read()
  assertEquals(simWatcherTest.getFindRecords(page), {})

  simWatcherTest = SimWatcherTest(TestLogger(), app, fileUrls[:], simUrls[:])

  page = urllib2.urlopen(simUrls[3]).read()
  assertEquals(simWatcherTest.getFindRecords(page), findRecords["new1"])

  simWatcherTest = SimWatcherTest(TestLogger(), app, fileUrls[:], simUrls[:])

  page = urllib2.urlopen(simUrls[4]).read()
  assertEquals(simWatcherTest.getFindRecords(page), findRecords["new2"])

  assertEquals(simWatcherTest.formatRecords(), formatRecords)


def testFindUpdates(app):
  simWatcherTest = SimWatcherTest(TestLogger(), app, fileUrls[:], simUrls[:])

  page = urllib2.urlopen(simUrls[0]).read()
  assertEquals(simWatcherTest.findUpdates(page), [updates["update1"]])

  page = urllib2.urlopen(simUrls[1]).read()
  assertEquals(simWatcherTest.findUpdates(page), [])

  page = urllib2.urlopen(simUrls[2]).read()
  assertEquals(simWatcherTest.findUpdates(page), [updates["update2"]])

  page = urllib2.urlopen(simUrls[3]).read()
  assertEquals(simWatcherTest.findUpdates(page), [])

  page = urllib2.urlopen(simUrls[4]).read()
  assertEquals(simWatcherTest.findUpdates(page), [])

  page = urllib2.urlopen(simUrls[5]).read()
  assertEquals(simWatcherTest.findUpdates(page), [])


def testUpdateLeagueFile(app, slack):
  simWatcherTest = SimWatcherTest(
      TestLogger(slack), app, fileUrls[:], simUrls[:], slack)

  expected = {"ret": False, "collected": [], "index": 1,
              "date": fileDates["old"], "posted": []}
  assertEquals(simWatcherTest.getUpdateLeagueFile(), expected)

  expected = {"ret": False, "collected": [], "index": 2,
              "date": fileDates["old"], "posted": []}
  assertEquals(simWatcherTest.getUpdateLeagueFile(), expected)

  expected = {"ret": True, "collected": logs[6:8], "index": 3,
              "date": fileDates["new"], "posted": ["File is up."]}
  assertEquals(simWatcherTest.getUpdateLeagueFile(), expected)

  expected = {"ret": False, "collected": logs[6:8], "index": 3,
              "date": fileDates["new"], "posted": ["File is up."]}
  assertEquals(simWatcherTest.getUpdateLeagueFile(), expected)


def testUpdateLiveSim(app, slack):
  simWatcherTest = SimWatcherTest(
      TestLogger(slack), app, fileUrls[:], simUrls[:], slack)

  expected = {"ret": False, "collected": [], "index": 1,
              "date": simDates["old"], "finals": set(),
              "updates": [updates["update1"]], "posted": []}
  assertEquals(simWatcherTest.getUpdateLiveSim(), expected)

  expected = {"ret": False, "collected": [], "index": 2,
              "date": simDates["old"], "finals": set(),
              "updates": [updates["update1"], updates["update2"]],
              "posted": []}
  assertEquals(simWatcherTest.getUpdateLiveSim(), expected)

  expected = {"ret": True, "collected": logs[1:2], "index": 3,
              "date": simDates["new"], "finals": finals["new1"], "updates": [],
              "posted": []}
  assertEquals(simWatcherTest.getUpdateLiveSim(), expected)

  expected = {"ret": True, "collected": logs[1:3], "index": 4,
              "date": simDates["new"], "finals": finals["new2"], "updates": [],
              "posted": []}
  assertEquals(simWatcherTest.getUpdateLiveSim(), expected)

  expected = {"ret": False, "collected": logs[1:4], "index": 5,
              "date": simDates["new"], "finals": finals["new2"], "updates": [],
              "posted": []}
  assertEquals(simWatcherTest.getUpdateLiveSim(), expected)

  expected = {"ret": False, "collected": logs[1:4], "index": 5,
              "date": simDates["new"], "finals": finals["new2"], "updates": [],
              "posted": []}
  assertEquals(simWatcherTest.getUpdateLiveSim(), expected)


def testWatch(app, slack):
  simWatcherTest = SimWatcherTest(
      TestLogger(slack), app, fileUrls[:], simUrls[:], slack)

  expected = {"collected": logs,
              "captured": [filenames["new"]],
              "posted": [logs[0], updates["update2"], filenames["new"],
                         postedRecords, "\n".join(logs[1:6]),
                         "File is up.", "\n".join(logs[6:9])]}
  assertEquals(simWatcherTest.getWatch(), expected)


if __name__ == "__main__":
  app = QApplication(sys.argv)

  parser = argparse.ArgumentParser()
  parser.add_argument('--mode', dest='mode')
  parser.add_argument('--slack', dest='slack', action='store_true')
  parser.set_defaults(slack=False)
  args = parser.parse_args()

  # if args.mode == "real" or args.mode == "all":
  #   testReal(app)

  if args.mode == "filedate" or args.mode == "all":
    testFindFileDate(app)

  if args.mode == "findexports" or args.mode == "all":
    testFindExports(app)

  if args.mode == "readexports" or args.mode == "all":
    testReadExports(app)

  if args.mode == "writeexports" or args.mode == "all":
    testWriteExports(app)

  if args.mode == "simdate" or args.mode == "all":
    testFindSimDate(app)

  if args.mode == "boxes" or args.mode == "all":
    testFindBoxes(app)

  if args.mode == "finals" or args.mode == "all":
    testFindFinals(app)

  if args.mode == "records" or args.mode == "all":
    testFindRecords(app)

  if args.mode == "updates" or args.mode == "all":
    testFindUpdates(app)

  if args.mode == "leaguefile" or args.mode == "all":
    testUpdateLeagueFile(app, args.slack)

  if args.mode == "livesim" or args.mode == "all":
    testUpdateLiveSim(app, args.slack)

  if args.mode == "watch" or args.mode == "all":
    testWatch(app, args.slack)

  print "Passed."
