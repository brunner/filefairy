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
from logger import Logger


class SimWatcher(object):
  """Watches the live sim page for any changes."""

  def __init__(self, logger=None, app=None):
    """Does an initial parse of the live sim page."""
    self.logger = logger or Logger()
    self.screenshot = screenshot.Screenshot(
        app or QApplication(sys.argv), self.getImagesPath())

    self.filePage = self.getPage(self.getFileUrl())
    self.fileDate = self.findFileDate(self.filePage)

    self.simPage = self.getPage(self.getSimUrl())
    self.simDate = self.findSimDate(self.simPage)
    self.finals = self.findFinals(self.simPage)
    self.updates = self.findUpdates(self.simPage)

    self.pages = {}
    self.records = {t: [0, 0, 0] for t in range(31, 61)}

    self.updateLiveSim()

  def capture(self, html, filename):
    self.screenshot.capture(html, filename)

  def postMessage(self, message, channel):
    slack.postMessage(message, channel)

  def upload(self, filename, channel):
    slack.upload(self.getImagesPath(), filename, channel)

  def getFileUrl(self):
    """Returns the exports page url that should be checked for date changes."""
    return "http://orangeandblueleaguebaseball.com/StatsLab/exports.php"

  def getSimUrl(self):
    """Returns the live sim page url that should be checked for date changes."""
    return "http://orangeandblueleaguebaseball.com/league/OBL/reports/news/html/real_time_sim/index.html"

  def getTimerValues(self):
    """Returns a tuple of values, in seconds, for the watchLiveSim timer."""
    return [
        2,      # 2 seconds, to sleep between consecutive sim page checks.
        60,     # 1 minute, after which the watcher pauses to upload any sim
                #     page screenshots to Slack and check if the file is up.
        82800,  # 23 hours, to wait for a page change, before timing out and
                #     exiting the program.
    ]

  def getPage(self, url):
    try:
      page = urllib2.urlopen(url).read()
    except Exception as e:
      self.logger.log("Exception opening {0}: {1}.".format(url, e))
      page = ""

    return page

  def getImagesPath(self):
    return os.path.expanduser("~") + "/orangeandblueleague/watchers/screenshots/"

  def watch(self):
    """Itermittently checks the page urls for any changes.

    If any changes are found, wait for a certain amount of time before checking
    if there are any page snapshots to upload. Abandon watching after a timeout.
    """
    sleep, pause, timeout = self.getTimerValues()
    elapsed = 0

    self.logger.log("Started watching.")

    while elapsed < timeout:
      if self.updateLiveSim():
        elapsed = 0
      else:
        time.sleep(sleep)
        elapsed = elapsed + sleep

      if elapsed and elapsed % pause == 0:
        self.digest()
        if self.updateLeagueFile():
          elapsed = timeout

    self.logger.log("Done watching.")
    self.digest()

  def updateLeagueFile(self, url=""):
    """Opens the exports page and checks the league file.

    Returns true if the file has changed since the previous check.
    """
    url = url or self.getFileUrl()

    page, date = "", ""
    while not date:
      page = self.getPage(url)
      date = self.findFileDate(page)

    if date != self.fileDate:
      self.fileDate = date
      self.postMessage("File is up.", "general")
      self.logger.log("File is up.")
      return True

    return False

  def updateLiveSim(self, url=""):
    """Opens the live sim page and checks the page content.

    Returns true if a page snapshot was saved.
    """
    url = url or self.getSimUrl()

    page, date = "", ""
    while not date:
      page = self.getPage(url)
      date = self.findSimDate(page)

    finals = self.findFinals(page)

    ret = False
    if date != self.simDate:
      self.updates = []

      if finals:
        self.pages[date] = page
        ret = True

        self.logger.log("Saved {0} finals on {1}.".format(len(finals), date))

      self.simDate = date
      self.finals = finals

    elif page != self.simPage:
      updates = self.findUpdates(page)
      for update in updates:
        if update not in self.updates:
          self.postMessage(update, "live-sim-discussion")
          self.updates.append(update)

      if finals and finals > self.finals:
        self.pages[date] = page
        ret = True

        self.logger.log("Saved {0} finals on {1}.".format(len(finals), date))
        self.finals = finals

      elif finals and finals < self.finals:
        self.logger.log("Ignored {0} finals on {1}.".format(len(finals), date))

    self.simPage = page

    return ret

  def digest(self):
    for date in sorted(self.pages):
      filename = "sim{0}.png".format(date)
      self.findRecords(self.pages[date])
      self.capture(self.pages[date], filename)
      self.upload(filename, "live-sim-discussion")
      self.logger.log("Uploaded {0}.".format(filename))

    if self.pages:
      lines = self.formatRecords()
      self.postMessage("\n\n".join(lines), "live-sim-discussion")
      self.logger.log("Posted records.")

    self.pages = {}
    self.logger.dump()

  def findFileDate(self, page):
    match = re.findall(r"League File Updated: ([^<]+)<", page)
    return match[0] if len(match) else ""

  def findSimDate(self, page):
    match = re.findall(r"MAJOR LEAGUE BASEBALL<br(?: /)?>([^<]+)<", page)
    return match[0].replace("/", "").strip() if len(match) else ""

  def findFinals(self, page):
    boxes = re.findall(
        r"FINAL(?: \(\d+\))?</td>(.*?)</table>", page, re.DOTALL)
    games = set()
    for box in boxes:
      games.add("".join(re.findall(r"teams/team_([^\.]+)\.html", box)))

    return games

  def findRecords(self, page):
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
            self.records[team1][0] += 1
            self.records[team2][1] += 1
          elif runs1 < runs2:
            self.records[team1][1] += 1
            self.records[team2][0] += 1
          else:
            self.records[team1][2] += 1
            self.records[team2][2] += 1

  def formatRecords(self):
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
      pct = lambda x: (float(r[x][0] + 0.5 * r[x][2]) / (sum(r[x]) or 1),
                       r[x][0],
                       float(1) / r[x][1] if r[x][1] else 2,
                       r[x][2])
      ordered = sorted(division[1], key=pct, reverse=True)

      formatted = []
      for t in ordered:
        emoji = slack.teamidsToEmoji[t]
        record = r[t] if r[t][2] else r[t][:2]
        formatted.append("{0} {1}".format(
            emoji, "-".join([str(n) for n in record])))

      lines.append("{0}\n{1}".format(
          division[0], " :separator: ".join(formatted)))

    return lines

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

        if len(teams) == 2 and len(runs) == 2 or len(inning) == 2:
          if inning[1] == "&nbsp;":
            time = ":toparrow: {0}".format(filter(str.isdigit, inning[0]))
          else:
            time = ":bottomarrow: {0}".format(filter(str.isdigit, inning[1]))

          score = "{0} {1} {2} {3} {4}".format(
              teams[0], runs[0], ":separator:", teams[1], runs[1])
          formatted = "{0} {1} {2}\n{3}".format(
              time, ":separator:", score, summary.replace(":", ""))

          pattern = re.compile("|".join(slack.nicksToEmoji.keys()))
          updates.append(pattern.sub(
              lambda x: slack.nicksToEmoji[x.group()], formatted))

    return updates


if __name__ == "__main__":
  simWatcher = SimWatcher()
  simWatcher.watch()
