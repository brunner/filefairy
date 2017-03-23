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

  def __init__(self, app, urls, filefairy=False):
    """Stores a few test sim urls.

    Pass filefairy=True to interface with the testing Slack channel."""
    self.urls = urls
    self.current = self.urls[0]
    self.captured = {}
    self.posted = []
    self.filefairy = filefairy

    self.page = self.getPage(self.current)
    self.date = self.findDate(self.page)
    self.finals = self.findFinals(self.page)
    self.updates = self.findUpdates(self.page)
    self.started = False
    self.threads = []
    self.logs = []

    self.screenshot = screenshot.Screenshot(app, self.getImagesPath())

    self.updateLiveSim(self.current)

  def capture(self, url, output_file):
    """Stores the captured file and url for asserting."""
    self.captured[output_file] = url
    if self.filefairy:
      super(SimWatcherTest, self).capture(url, output_file)
    else:
      self.log("Captured {0}.".format(output_file))

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

  def sendAlert(self, value, secondary_value=""):
    """Returns an easily assertable value."""
    return {
        "value": value,
        "secondary_value": secondary_value,
        "current": self.current,
        "date": self.date,
        "finals": self.finals,
        "captured": self.captured
    }

  def uploadToSlack(self, queued, channel):
    """Stores the queued photo for asserting. Channel is overridden."""
    self.posted.append(queued)
    if self.filefairy:
      slack.upload(self.getImagesPath(), queued, "testing")

  def postMessageToSlack(self, message, channel):
    """Stores the message for asserting. Channel is overridden."""
    self.posted.append(message)
    if self.filefairy:
      slack.postMessage(message, "testing")


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--filefairy', dest='filefairy', action='store_true')
  parser.set_defaults(filefairy=False)
  parser.add_argument('--real', dest='real', action='store_true')
  parser.set_defaults(real=False)
  args = parser.parse_args()

  app = QApplication(sys.argv)

  if args.real:
    # Real data.
    url = "http://orangeandblueleaguebaseball.com/league/OBL/reports/news/html/real_time_sim/index.html"
    page = urllib2.urlopen(url).read()
    simWatcherTest = SimWatcherTest(app, [url])
    assert simWatcherTest.findDate(page) != ""
    assert simWatcherTest.findFinals(page) != []

  # Test data.
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
      "new2": set(["5331", "3348", "4151", "3456", "3637",
                   "5035", "4254", "3955", "4645", "5847",
                   "4038", "4952", "6032", "4459", "4357"]),
  }
  updates = {
      "update1": ":toparrow: 4 :separator: :pirates: 10 " +
      ":separator: :giants: 0\n:pirates: C.J. Hinojosa " +
      "hits a 3-run HR.",
      "update2": ":bottomarrow: 5 :separator: :pirates: " +
      "10 :separator: :giants: 2\n:giants: David " +
      "Olmedo-Barrera hits a 2-run HR."
  }

  # Test findDate method.
  simWatcherTest = SimWatcherTest(app, urls[:])
  page = urllib2.urlopen(urls[0]).read()
  assert simWatcherTest.findDate(page) == dates["old"]
  page = urllib2.urlopen(urls[1]).read()
  assert simWatcherTest.findDate(page) == dates["old"]
  page = urllib2.urlopen(urls[2]).read()
  assert simWatcherTest.findDate(page) == dates["old"]
  page = urllib2.urlopen(urls[3]).read()
  assert simWatcherTest.findDate(page) == dates["new"]
  page = urllib2.urlopen(urls[4]).read()
  assert simWatcherTest.findDate(page) == dates["new"]
  page = urllib2.urlopen(urls[5]).read()
  assert simWatcherTest.findDate(page) == dates["new"]

  # Test findFinals method.
  simWatcherTest = SimWatcherTest(app, urls[:])
  page = urllib2.urlopen(urls[0]).read()
  assert simWatcherTest.findFinals(page) == finals["old1"]
  page = urllib2.urlopen(urls[1]).read()
  assert simWatcherTest.findFinals(page) == finals["old1"]
  page = urllib2.urlopen(urls[2]).read()
  assert simWatcherTest.findFinals(page) == finals["old2"]
  page = urllib2.urlopen(urls[3]).read()
  assert simWatcherTest.findFinals(page) == finals["new1"]
  page = urllib2.urlopen(urls[4]).read()
  assert simWatcherTest.findFinals(page) == finals["new2"]
  page = urllib2.urlopen(urls[5]).read()
  assert simWatcherTest.findFinals(page) == finals["new1"]

  # Test findUpdates method.
  simWatcherTest = SimWatcherTest(app, urls[:])
  page = urllib2.urlopen(urls[0]).read()
  assert simWatcherTest.findUpdates(page) == [updates["update1"]]
  page = urllib2.urlopen(urls[1]).read()
  assert simWatcherTest.findUpdates(page) == []
  page = urllib2.urlopen(urls[2]).read()
  assert simWatcherTest.findUpdates(page) == [updates["update2"]]
  page = urllib2.urlopen(urls[3]).read()
  assert simWatcherTest.findUpdates(page) == []
  page = urllib2.urlopen(urls[4]).read()
  assert simWatcherTest.findUpdates(page) == []
  page = urllib2.urlopen(urls[5]).read()
  assert simWatcherTest.findUpdates(page) == []

  # Test updateLiveSim method for changed case.
  simWatcherTest = SimWatcherTest(app, urls[:])
  assert simWatcherTest.updateLiveSim() == \
      {"value": False, "secondary_value": "", "current": urls[0],
       "date": dates["old"], "finals": finals["old1"], "captured": {}}
  assert simWatcherTest.updateLiveSim() == \
      {"value": True, "secondary_value": "", "current": urls[1],
       "date": dates["old"], "finals": finals["old1"], "captured": {}}
  assert simWatcherTest.updateLiveSim() == \
      {"value": True, "secondary_value": "", "current": urls[2],
       "date": dates["old"], "finals": finals["old2"],
       "captured": {files["old"]: urls[2]}}
  assert simWatcherTest.updateLiveSim() == \
      {"value": True, "secondary_value": files["old"], "current": urls[3],
       "date": dates["new"], "finals": finals["new1"],
       "captured": {files["old"]: urls[2], files["new"]: urls[3]}}
  assert simWatcherTest.updateLiveSim() == \
      {"value": True, "secondary_value": "", "current": urls[4],
       "date": dates["new"], "finals": finals["new2"],
       "captured": {files["old"]: urls[2], files["new"]: urls[4]}}
  assert simWatcherTest.updateLiveSim() == \
      {"value": True, "secondary_value": "", "current": urls[5],
       "date": dates["new"], "finals": finals["new2"],
       "captured": {files["old"]: urls[2], files["new"]: urls[4]}}
  assert simWatcherTest.updateLiveSim() == \
      {"value": False, "secondary_value": "", "current": urls[5],
       "date": dates["new"], "finals": finals["new2"],
       "captured": {files["old"]: urls[2], files["new"]: urls[4]}}

  # Test updateLiveSim method for unchanged case.
  simWatcherTest = SimWatcherTest(app, urls[:1])
  assert simWatcherTest.updateLiveSim() == \
      {"value": False, "secondary_value": "", "current": urls[0],
       "date": dates["old"], "finals": finals["old1"], "captured": {}}
  assert simWatcherTest.updateLiveSim() == \
      {"value": False, "secondary_value": "", "current": urls[0],
       "date": dates["old"], "finals": finals["old1"], "captured": {}}

  # Test watchLiveSimInternal method for changed case.
  simWatcherTest = SimWatcherTest(app, urls[:])
  assert simWatcherTest.watchLiveSimInternal() == \
      {"value": True, "secondary_value": "", "current": urls[5],
       "date": dates["new"], "finals": finals["new2"],
       "captured": {files["old"]: urls[2], files["new"]: urls[4]}}

  # Test watchLiveSimInternal method for unchanged case.
  simWatcherTest = SimWatcherTest(app, urls[:1])
  assert simWatcherTest.watchLiveSimInternal() == \
      {"value": False, "secondary_value": "", "current": urls[0],
       "date": dates["old"], "finals": finals["old1"], "captured": {}}

  # Test watchLiveSim method for changed case.
  simWatcherTest = SimWatcherTest(app, urls[:], args.filefairy)
  assert simWatcherTest.watchLiveSim() == True

  # Test watchLiveSim method for unchanged case.
  simWatcherTest = SimWatcherTest(app, urls[:1], args.filefairy)
  assert simWatcherTest.watchLiveSim() == False

  print "Passed."