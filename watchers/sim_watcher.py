#!/usr/bin/env python

import argparse
import datetime
import os
import re
import screenshot
import subprocess
import slack
import sys
import threading
import time
import urllib2

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *


imagespath = os.path.expanduser("~") + "/orangeandblueleague/watchers/images/"


class SimWatcher(object):
  """Watches the live sim page for any changes."""

  def __init__(self, app=None):
    """Does an initial parse of the live sim page."""
    self.page = self.getPage(self.getUrl())
    self.date = self.findDate(self.page)
    self.finals = self.findFinals(self.page)
    self.updates = self.findUpdates(self.page)
    self.started = False
    self.threads = []
    self.logs = []

    self.screenshot = screenshot.Screenshot(
        app or QApplication(sys.argv), imagespath)

    self.updateLiveSim()

  def capture(self, url, output_file):
    self.screenshot.capture(url, output_file)

  def watchLiveSim(self):
    """Itermittently checks the sim page url for any changes.

    If any changes are found, wait for a certain amount of time to capture any
    additional changes. If not, abandon watching after a timeout.
    Returns true if any changes were found.
    """
    return self.checkAlert(self.watchLiveSimInternal())

  def watchLiveSimInternal(self):
    """Itermittently checks the sim page url for any changes.

    If any changes are found, wait for a certain amount of time before deciding
    that the sim is done. If not, abandon watching after a timeout.
    Returns a true alert if any changes were found.
    """
    sleep, done, timeout = self.getWatchLiveSimValues()
    elapsed = 0

    self.postMessageToSlack("Watching live sim.", "testing")

    while (not self.started and elapsed < timeout) or (self.started and elapsed < done):
      alert = self.updateLiveSim()
      updated = self.checkAlert(alert)
      queued = self.checkSecondaryAlert(alert)

      if updated:
        elapsed = 0

      if queued:
        self.uploadToSlack(queued, "live-sim-discussion")
        self.log("Uploaded {0} to live-sim-discussion.".format(queued))

      time.sleep(sleep)
      elapsed = elapsed + sleep

    if self.started:
      f = self.getFile(self.date)
      self.uploadToSlack(f, "live-sim-discussion")
      self.log("Uploaded {0} to live-sim-discussion.".format(f))
      alert = self.sendAlert(True)
    else:
      alert = self.sendAlert(False)

    self.postMessageToSlack("Done watching live sim.", "testing")
    self.postMessageToSlack("\n".join(self.logs), "testing")

    for t in self.threads:
      t.join()

    return alert

  def updateLiveSim(self, url=""):
    """Opens the live sim page and checks the page content.

    Returns a true alert if a screenshot was captured.
    """
    url = url or self.getUrl()
    page = self.getPage(url)
    date = self.findDate(page)
    finals = self.findFinals(page)
    updated = False
    queued = ""

    if date and date != self.date:
      self.log("Detected date change to {0}.".format(date))
      if self.date and self.started:
        queued = self.getFile(self.date)
        self.log("Queued {0} for upload.".format(queued))

      self.started = False
      self.updates = []

      if finals:
        self.log("Detected {0} finals.".format(len(finals)))
        self.finals = finals
        updated = True

      f = self.getFile(date)
      self.capture(url, f)
      self.log("Captured {0}.".format(f))

      self.date = date

    elif page and page != self.page:
      self.log("Detected page change.")
      updated = True

      updates = self.findUpdates(page)
      for update in updates:
        if update not in self.updates:
          self.postMessageToSlack(update, "live-sim-discussion")
          self.updates.append(update)

      if finals and finals > self.finals:
        self.log("Detected {0} finals.".format(len(finals)))

        f = self.getFile(date)
        self.capture(url, self.getFile(date))
        self.log("Captured {0}.".format(f))

        self.finals = finals
      elif finals and finals < self.finals:
        self.log("Ignored partially loaded page with {0} finals.".format(len(finals)))

    self.page = page

    if updated:
      self.started = True

    return self.sendAlert(updated, queued)

  def findDate(self, page):
    match = re.findall(r"MAJOR LEAGUE BASEBALL<br(?: /)?>([^<]+)<", page)
    return match[0].replace("/", "").strip() if len(match) else ""

  def findFinals(self, page):
    boxes = re.findall(
        r"FINAL(?: \(\d+\))?</td>(.*?)</table>", page, re.DOTALL)
    games = set()
    for box in boxes:
      games.add("".join(re.findall(r"teams/team_([^\.]+)\.html", box)))

    return games

  def findUpdates(self, page):
    match = re.findall(r"SCORING UPDATES(.*?)</table>", page, re.DOTALL)
    box = match[0] if len(match) == 1 else ""

    rows = re.findall(r"<tr>(.*?)</tr>", box, re.DOTALL)
    updates = []
    for row in rows:
      cols = re.findall(r"<td(.*?)</td>", row, re.DOTALL)
      if len(cols) == 5:
        teams = re.findall(r"teams/team_(?:\d+)\.html\">([^<]+)<", cols[1])
        runs = re.findall(r"<div(?:[^>]+)>([^<]+)<", cols[2])
        inning = re.findall(r"<div(?:[^>]+)>([^<]+)<", cols[3])
        chunks = cols[4].split(">")
        summary = chunks[1] if len(chunks) > 1 else ""
        updates.append(self.formatUpdates(teams, runs, inning, summary))

    return updates

  def formatUpdates(self, teams, runs, inning, summary):
    if len(teams) != 2 or len(runs) != 2 or len(inning) != 2:
      return ""

    if inning[1] == "&nbsp;":
      time = ":toparrow: {0}".format(filter(str.isdigit, inning[0]))
    else:
      time = ":bottomarrow: {0}".format(
          filter(str.isdigit, inning[1]))

    separator = ":separator:"
    score = "{0} {1} {2} {3} {4}".format(
        teams[0], runs[0], separator, teams[1], runs[1])
    formatted = "{0} {1} {2}\n{3}".format(
        time, separator, score, summary.replace(":", ""))

    pattern = re.compile("|".join(slack.icons.keys()))
    return pattern.sub(lambda x: slack.icons[x.group()], formatted)

  def getPage(self, url):
    try:
      page = urllib2.urlopen(url).read()
    except Exception as e:
      page = ""

    return page

  def getUrl(self):
    """Returns the live sim page url that should be checked for date changes."""
    return "http://orangeandblueleaguebaseball.com/league/OBL/reports/news/html/real_time_sim/index.html"

  def getWatchLiveSimValues(self):
    """Returns a tuple of values, in seconds, for the watchLiveSim timer."""
    return [
        5,      # 5 seconds, to sleep between consecutive page checks.
        360,    # 6 minutes, after which (if the page is currently static but
                #     had changed previously) the sim is presumed to be over
                #     and the last screenshot can be uploaded to Slack.
        18000,  # 12 hours, to wait for an initial page change, before timing
                #     out and exiting the program.
    ]

  def getFile(self, date):
    """Gets the file name to use for a given live sim date."""
    return "sim{0}.png".format(date)

  def sendAlert(self, value, secondary_value=""):
    """Returns the specified value."""
    return {
        "value": value,
        "secondary_value": secondary_value,
    }

  def checkAlert(self, alert):
    """Returns the value of the alert."""
    return alert["value"]

  def checkSecondaryAlert(self, alert):
    """Returns the secondary value of the alert."""
    return alert["secondary_value"]

  def log(self, message):
    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
    current = self.date
    self.logs.append("[{0}] ({1}) {2}".format(timestamp, current, message))

  def uploadToSlack(self, queued, channel):
    """Posts the queued photo to the Slack team, from a background thread."""
    t = SimWatcherThread(slack.upload, imagespath, queued, channel)
    self.threads.append(t)
    t.start()

  def postMessageToSlack(self, message, channel):
    """Posts the message to the Slack team, from a background thread."""
    t = SimWatcherThread(slack.postMessage, message, channel)
    self.threads.append(t)
    t.start()


class SimWatcherThread(threading.Thread):
  """Calls a method from a background thread."""

  def __init__(self, method, *args):
    self.method = method
    self.args = args
    threading.Thread.__init__(self)

  def run(self):
    self.method.__call__(*self.args)


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

    self.screenshot = screenshot.Screenshot(app, imagespath)

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
      slack.upload(imagespath, queued, "testing")

  def postMessageToSlack(self, message, channel):
    """Stores the message for asserting. Channel is overridden."""
    self.posted.append(message)
    if self.filefairy:
      slack.postMessage(message, "testing")


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--test', dest='test', action='store_true')
  parser.set_defaults(test=False)
  parser.add_argument('--filefairy', dest='filefairy', action='store_true')
  parser.set_defaults(filefairy=False)
  parser.add_argument('--real', dest='real', action='store_true')
  parser.set_defaults(real=False)
  args = parser.parse_args()

  if args.test:
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
