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


class Filefairy(object):
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

    self.exports = self.readExports() 

    self.pages, self.posts = {}, []
    self.records = {t: [0, 0, 0] for t in range(31, 61)}

  def capture(self, html, filename):
    self.screenshot.capture(html, filename)

  def postMessage(self, message, channel):
    try:
      slack.postMessage(message, channel)
    except urllib2.URLError as e:
      if hasattr(e, "reason"):
        self.logger.log("Failed to reach server. {0}.".format(e.reason))
      elif hasattr(e, "code"):
        self.logger.log("Server failed to handle request. {0}.".format(e.code))
    except:
      self.logger.log("Unspecified exception.")

  def upload(self, filename, channel):
    slack.upload(self.getImagesPath(), filename, channel)

  def getFileUrl(self):
    """Returns the exports page url that should be checked for date changes."""
    return "http://orangeandblueleaguebaseball.com/StatsLab/exports.php"

  def getSimUrl(self):
    """Returns the live sim page url that should be checked for date changes."""
    return "http://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/real_time_sim/index.html"

  def getExportsInputFile(self):
    """Returns the file that exports data is saved to."""
    return os.path.expanduser("~") + "/orangeandblueleague/filefairy/data/exports.txt"

  def getExportsOutputFile(self):
    """Returns the file that exports data is saved to."""
    return self.getExportsInputFile()

  def getTimerValues(self):
    """Returns a tuple of values, in seconds, for the watchLiveSim timer."""
    return [
        5,      # 5 seconds, to sleep between consecutive sim page checks.
        60,     # 1 minute, after which the watcher pauses to upload any sim
                #     page screenshots to Slack and check if the file is up.
        82800,  # 23 hours, to wait for a page change, before timing out and
                #     exiting the program.
    ]

  def getPage(self, url):
    page = ""
    try:
      page = urllib2.urlopen(url).read()
    except urllib2.URLError as e:
      if hasattr(e, "reason"):
        pass
        # self.logger.log("Failed to reach server. {0}.".format(e.reason))
      elif hasattr(e, "code"):
        self.logger.log("Server failed to handle request. {0}.".format(e.code))
    except:
      self.logger.log("Unspecified exception.")

    return page

  def getImagesPath(self):
    return os.path.expanduser("~") + "/orangeandblueleague/filefairy/screenshots/"

  def watch(self):
    """Itermittently checks the page urls for any changes.

    If any changes are found, wait for a certain amount of time before checking
    if there are any page snapshots to upload. Abandon watching after a timeout.
    """
    sleep, pause, timeout = self.getTimerValues()
    elapsed = 0

    self.logger.log("Started watching.")

    while elapsed < timeout:
      time.sleep(sleep)
      elapsed = elapsed + sleep

      if elapsed % pause == 0:
        self.digest()
        if self.updateLeagueFile():
          elapsed = timeout
      elif self.updateLiveSim():
        elapsed = 0

    self.logger.log("Done watching.")
    self.digest()

  def updateLeagueFile(self):
    """Opens the exports page and checks the league file.

    Returns true if the file has changed since the previous check.
    """
    url = self.getFileUrl()
    page = self.getPage(url)
    date = self.findFileDate(page)

    if not date:
      return False

    ret = False
    if date != self.fileDate:
      self.postMessage("File is up.", "general")
      self.logger.log("File is up.")

      teamids = self.findExports(self.filePage)
      self.writeExports(self.exports, teamids)
      self.logger.log("{0} teams exported.".format(len(teamids)))

      ret = True

    self.filePage = page
    self.fileDate = date

    return ret

  def updateLiveSim(self):
    """Opens the live sim page and checks the page content.

    Returns true if a page snapshot was saved.
    """
    url = self.getSimUrl()
    page = self.getPage(url)
    date = self.findSimDate(page)

    if not date:
      return False

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
          self.posts.append(update)
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
    for post in self.posts:
      self.postMessage(post, "live-sim-discussion")

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

    self.pages, self.posts = {}, []

    logs = "\n".join(self.logger.collect())
    if logs:
      self.postMessage(logs, "testing")

  def findFileDate(self, page):
    match = re.findall(r"League File Updated: ([^<]+)<", page)
    return match[0] if len(match) else ""

  def findExports(self, page):
    teams = re.findall(r"teams/team_(.*?) Export", page)
    exports = []
    for team in teams:
      if team[-3:] == "New":
        exports.append(int(team[:2]))

    return exports

  def readExports(self):
    exports = {}
    with open(self.getExportsInputFile(), "r") as f:
      for line in f.readlines():
        entries = line.split()
        if len(entries) > 2:
          teamid = int(entries[0])
          wins = int(entries[1])
          losses = int(entries[2])
          streak = int(entries[3]) if len(entries) > 3 else -1
          recent = [int(e) for e in entries[4:]] if len(entries) > 4 else []
          exports[teamid] = [wins, losses, streak, recent]

    return exports

  def writeExports(self, exports, teamids):
    with open(self.getExportsOutputFile(), "w") as f:
      for teamid in sorted(exports.keys()):
        wins, losses, streak, recent = exports[teamid]
        if teamid in teamids:
          wins = wins + 1
          streak = streak + 1 if len(recent) and recent[-1] == 1 else 1
          recent = (recent + [1])[-10:]
        elif not streak == -1:
          losses = losses + 1
          streak = streak + 1 if len(recent) and recent[-1] == 0 else 1
          recent = (recent + [0])[-10:]

        if not streak == -1:
          f.write("{0}  {1:<3} {2:<3} {3:<3} {4}\n".format(
              teamid, wins, losses, streak, " ".join([str(r) for r in recent])))
        else:
          f.write("{0}  {1:<3} {2:<3}\n".format(teamid, wins, losses))

        exports[teamid] = [wins, losses, streak, recent]

    return exports

  def formatExports(self):
    e = self.exports
    f = lambda x: (float(e[x][0]) / ((e[x][0] + e[x][1]) or 1),
                   e[x][0],
                   float(1) / e[x][1] if e[x][1] else 2,
                   float(e[x][3].count(1)) /
                   ((e[x][3].count(1) + e[x][3].count(0)) or 1),
                   0 if e[x][2] <= 0 else e[x][2] if e[x][3][-1] else -e[x][2])
    ordered = sorted(e, key=f, reverse=True)

    formatted = []
    formatted.append("{0:<12} {1:>3}-{2:<4} {3:>5} {4:>6}    {5:<3}".format(
        "team", "W", "L", "%", "L10", "*"))
    formatted.append("-"*44)
    for t in ordered:
      emoji = slack.teamidsToEmoji[t].replace(":", "")

      if e[t][2] > 0:
        streak = "{0}{1}".format("W" if e[t][3][-1] else "L", e[t][2])
      else:
        streak = "W0"

      pct = "{0:1.3f}".format(float(e[t][0]) / ((e[t][0] + e[t][1]) or 1))
      if pct[0] == "0":
        pct = " " + pct[1:]

      formatted.append("{0:<12} {1:>3}-{2:<4} {3:<7} {4:>2}-{5:<4} {6:<3}".format(
          emoji, e[t][0], e[t][1], pct, e[t][3].count(1), e[t][3].count(0), streak))

    print "\n".join(formatted)

  def findSimDate(self, page):
    match = re.findall(r"MAJOR LEAGUE BASEBALL<br(?: /)?>([^<]+)<", page)
    return match[0].replace("/", "").strip() if len(match) else ""

  def findBoxes(self, page):
    boxes = re.findall(
        r"FINAL(?: \(\d+\))?</td>(.*?)</table>", page, re.DOTALL)
    if len(boxes) == page.count("Box Score</a>"):
      return boxes

    return []

  def findFinals(self, page):
    finals = set()
    boxes = self.findBoxes(page)
    for box in boxes:
      finals.add("".join(re.findall(r"teams/team_([^\.]+)\.html", box)))

    return finals

  def findRecords(self, page):
    boxes = self.findBoxes(page)
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
    groups = [
        ("AL East", [33, 34, 48, 57, 59]),
        ("AL Central", [35, 38, 40, 43, 47]),
        ("AL West", [42, 44, 50, 54, 58]),
        ("NL East", [32, 41, 49, 51, 60]),
        ("NL Central", [36, 37, 46, 52, 56]),
        ("NL West", [31, 39, 45, 53, 55]),
    ]

    lines = []
    for group in groups:
      r = self.records
      pct = lambda x: (float(r[x][0] + 0.5 * r[x][2]) / (sum(r[x]) or 1),
                       r[x][0],
                       float(1) / r[x][1] if r[x][1] else 2,
                       r[x][2])
      ordered = sorted(group[1], key=pct, reverse=True)

      formatted = []
      for t in ordered:
        emoji = slack.teamidsToEmoji[t]
        record = r[t] if r[t][2] else r[t][:2]
        formatted.append("{0} {1}".format(
            emoji, "-".join([str(n) for n in record])))

      lines.append("{0}\n{1}".format(
          group[0], " :separator: ".join(formatted)))

    return lines

  def findUpdates(self, page):
    match = re.findall(r"SCORING UPDATES(.*?)</table>", page, re.DOTALL)
    box = match[0] if len(match) == 1 else ""

    rows = re.findall(r"<tr>(.*?)</tr>", box, re.DOTALL)
    updates = []
    for row in reversed(rows):
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
  filefairy = Filefairy()
  filefairy.watch()
