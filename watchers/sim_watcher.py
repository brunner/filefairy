#!/usr/bin/env python

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

from PyQt4.QtGui import QApplication


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
        app or QApplication(sys.argv), self.getImagesPath())

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

      if updated:
        elapsed = 0

      time.sleep(sleep)
      elapsed = elapsed + sleep

    if self.started:
      for f in sorted(os.listdir(self.getImagesPath())):
        self.uploadToSlack(f, "testing")
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

    if date and date != self.date:
      self.log("Detected date change to {0}.".format(date))
      self.started = False
      self.updates = []

      if finals:
        f = self.getFile(date)
        self.capture(url, f)
        self.log("Detected {0} finals and captured screenshot.".format(len(finals)))
        updated = True

      self.date = date
      self.finals = finals

    elif page and page != self.page:
      self.log("Detected page change.")
      updated = True

      updates = self.findUpdates(page)
      for update in updates:
        if update not in self.updates:
          self.postMessageToSlack(update, "testing")
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

    return self.sendAlert(updated)

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

  def sendAlert(self, value):
    """Returns the specified value."""
    return {
        "value": value,
    }

  def checkAlert(self, alert):
    """Returns the value of the alert."""
    return alert["value"]

  def log(self, message):
    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
    current = self.date
    self.logs.append("[{0}] ({1}) {2}".format(timestamp, current, message))

  def uploadToSlack(self, filename, channel):
    """Posts a PNG screenshot to the Slack team, from a background thread."""
    t = SimWatcherThread(slack.upload, self.getImagesPath(), filename, channel)
    self.threads.append(t)
    t.start()

  def postMessageToSlack(self, message, channel):
    """Posts the message to the Slack team, from a background thread."""
    t = SimWatcherThread(slack.postMessage, message, channel)
    self.threads.append(t)
    t.start()

  def getImagesPath(self):
    return os.path.expanduser("~") + "/orangeandblueleague/watchers/images/"


class SimWatcherThread(threading.Thread):
  """Calls a method from a background thread."""

  def __init__(self, method, *args):
    self.method = method
    self.args = args
    threading.Thread.__init__(self)

  def run(self):
    self.method.__call__(*self.args)
