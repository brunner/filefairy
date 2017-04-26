#!/usr/bin/env python

import datetime
import os
import re
import screenshot
import subprocess
import slack
import sys
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
    self.records = self.initializeRecords()
    self.updates = self.findUpdates(self.page)
    self.started = False
    self.pages = {}
    self.logs = []
    self.inProgress = False

    self.screenshot = screenshot.Screenshot(
        app or QApplication(sys.argv), self.getImagesPath())

    self.updateLiveSim()

  def dequeue(self):
    for filename in sorted(self.pages):
      self.capture(self.pages[filename], filename)
      self.upload(filename, "live-sim-discussion")
      self.updateRecords(self.pages[filename])
      self.log("Uploaded {0} to live-sim-discussion.".format(filename))
      time.sleep(2)

    if self.pages:
      self.postRecords()
      self.log("Posted records to live-sim-discussion.")

    self.pages = {}

  def capture(self, html, filename):
    self.screenshot.capture(html, filename)

  def postMessage(self, message, channel):
    slack.postMessage(message, channel)

  def upload(self, filename, channel):
    slack.upload(self.getImagesPath(), filename, channel)

  def getUrl(self):
    """Returns the live sim page url that should be checked for date changes."""
    return "http://orangeandblueleaguebaseball.com/league/OBL/reports/news/html/real_time_sim/index.html"

  def getWatchLiveSimValues(self):
    """Returns a tuple of values, in seconds, for the watchLiveSim timer."""
    return [
        2,      # 2 seconds, to sleep between consecutive page checks.
        120,    # 2 minutes, after which (if the page is currently static but
                #     had changed previously) the sim is presumed to be over
                #     and the last screenshot can be uploaded to Slack.
        54000,  # 15 hours, to wait for an initial page change, before timing
                #     out and exiting the program.
    ]

  def sendAlert(self, value):
    """Returns the specified value."""
    return {"value": value}

  def checkAlert(self, alert):
    """Returns the value of the alert."""
    return alert["value"]

  def getPage(self, url):
    try:
      page = urllib2.urlopen(url).read()
    except Exception as e:
      page = ""

    return page

  def getFile(self, date):
    """Gets the file name to use for a given live sim date."""
    return "sim{0}.png".format(date)

  def getImagesPath(self):
    return os.path.expanduser("~") + "/orangeandblueleague/watchers/screenshots/"

  def log(self, message):
    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
    current = self.date
    self.logs.append("[{0}] ({1}) {2}".format(timestamp, current, message))

  def watchLiveSim(self, fileIsUp, simIsInProgress):
    """Itermittently checks the sim page url for any changes.

    If any changes are found, wait for a certain amount of time to capture any
    additional changes. If not, abandon watching after a timeout.
    Returns true if any changes were found.
    """
    return self.checkAlert(self.watchLiveSimInternal(fileIsUp, simIsInProgress))

  def watchLiveSimInternal(self, fileIsUp, simIsInProgress):
    """Itermittently checks the sim page url for any changes.

    If any changes are found, wait for a certain amount of time before checking
    if there are any page snapshots to upload. Abandon watching after a timeout.
    Returns a true alert if any changes were found.
    """
    sleep, check, timeout = self.getWatchLiveSimValues()
    elapsed = 0

    self.postMessage("Watching live sim.", "testing")

    while elapsed < timeout:
      alert = self.updateLiveSim()
      updated = self.checkAlert(alert)

      if updated:
        elapsed = 0

        if not self.inProgress:
          self.inProgress = True
          simIsInProgress.set()
      else:
        time.sleep(sleep)
        elapsed = elapsed + sleep

      if elapsed and elapsed % check == 0:
        self.dequeue()

        if self.inProgress:
          self.inProgress = False
          simIsInProgress.clear()

        if fileIsUp.is_set():
          elapsed = timeout

    if self.started:
      self.dequeue()
      alert = self.sendAlert(True)
    else:
      alert = self.sendAlert(False)

    self.postMessage("Done watching live sim.", "testing")
    self.postMessage("\n".join(self.logs), "testing")

    return alert

  def updateLiveSim(self, url=""):
    """Opens the live sim page and checks the page content.

    Returns a true alert if a screenshot was captured.
    """
    url = url or self.getUrl()

    page, date = "", ""
    while not date:
      page = self.getPage(url)
      date = self.findDate(page)

    finals = self.findFinals(page)
    updated = False

    if date != self.date:
      self.log("Detected date change to {0}.".format(date))
      self.started = False
      self.updates = []

      if finals:
        filename = self.getFile(date)
        self.pages[filename] = page
        self.log(
            "Detected {0} finals and saved page snapshot.".format(len(finals)))
        updated = True

      self.date = date
      self.finals = finals

    elif page != self.page:
      self.log("Detected page change.")

      updates = self.findUpdates(page)
      for update in updates:
        if update not in self.updates:
          self.postMessage(update, "testing")
          self.updates.append(update)

      if finals and finals > self.finals:
        filename = self.getFile(date)
        self.pages[filename] = page
        self.log(
            "Detected {0} finals and saved page snapshot.".format(len(finals)))

        self.finals = finals
        updated = True

      elif finals and finals < self.finals:
        self.log(
            "Ignored partially loaded page with {0} finals.".format(len(finals)))

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

  def initializeRecords(self):
    records = {}
    for teamid in range(31, 61):
      records[teamid] = {"W": 0, "L": 0, "T": 0}

    return records

  def formatRecord(self, record):
    if record["T"]:
      return "{0}-{1}-{2}".format(record["W"], record["L"], record["T"])
    else:
      return "{0}-{1}".format(record["W"], record["L"])

  def updateRecords(self, page):
    boxes = re.findall(
        r"FINAL(?: \(\d+\))?</td>(.*?)</table>", page, re.DOTALL)

    for box in boxes:
      teamids = re.findall(r"teams/team_([^\.]+)\.html", box)
      lines = re.findall(r"<span style=\"color:#F6EF7D;\">([^<]+)<", box)
      if len(teamids) == 2 and len(lines) == 6:
        team1, team2 = int(teamids[0]), int(teamids[1])
        runs1, runs2 = int(lines[0]), int(lines[3])
        if team1 in self.records and team2 in self.records:
          if runs1 > runs2:
            self.records[team1]["W"] += 1
            self.records[team2]["L"] += 1
          elif runs1 < runs2:
            self.records[team1]["L"] += 1
            self.records[team2]["W"] += 1
          else:
            self.records[team1]["T"] += 1
            self.records[team2]["T"] += 1

  def postRecords(self):
    divisions = [
        ("AL East", [33, 34, 48, 57, 59]),
        ("AL Central", [35, 38, 40, 43, 47]),
        ("AL West", [42, 44, 50, 54, 58]),
        ("NL East", [32, 41, 49, 51, 60]),
        ("NL Central", [36, 37, 46, 52, 56]),
        ("NL West", [31, 39, 45, 53, 55]),
    ]

    lines = []
    for division in divisions:
      r = self.records
      pct = lambda x: (float(r[x]["W"] + 0.5 * r[x]["T"]) /
                       (r[x]["W"] + r[x]["L"] + r[x]["T"] if r[x]
                        ["W"] + r[x]["L"] + r[x]["T"] else 1),    # Winning pct.
                       r[x]["W"],                                 # Most wins.
                       float(1) / r[x]["L"] if r[x]["L"] else 2,  # Few. losses.
                       r[x]["T"])                                 # Most ties.
      ordered = sorted(division[1], key=pct, reverse=True)

      formatted = " :separator: ".join(["{0} {1}".format(
          slack.teamidsToEmoji[teamid],
          self.formatRecord(r[teamid])) for teamid in ordered])
      lines.append("{0}\n{1}".format(division[0], formatted))

    self.postMessage("\n\n".join(lines), "live-sim-discussion")

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

    pattern = re.compile("|".join(slack.nicksToEmoji.keys()))
    return pattern.sub(lambda x: slack.nicksToEmoji[x.group()], formatted)
