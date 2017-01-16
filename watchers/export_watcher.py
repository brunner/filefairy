#!/usr/bin/env python

import argparse
import os
import re
import time
import urllib2


class ExportWatcher(object):
  """Watches the exports page for export and league file date changes."""

  def __init__(self):
    """Does an initial parse of the exports page."""
    self.teams = ["Twins", "Rockies", "Athletics",
                  "Reds", "Cardinals", "Red Sox", "Mariners"]
    self.exports, self.file = {}, ""

    self.updateTeamExports()
    self.updateLeagueFile()

  def watchTeamExports(self):
    """Itermittently checks the exports page url for export date changes.

    Returns true once a change has been found, or false after a timeout limit
    has been exceeded.
    """
    return self.checkAlert(self.watchTeamExportsInternal())

  def watchLeagueFile(self):
    """Itermittently checks the exports page url for league file date changes.

    Returns true once a change has been found, or false after a timeout limit
    has been exceeded.
    """
    return self.checkAlert(self.watchLeagueFileInternal())

  def watchTeamExportsInternal(self):
    """Itermittently checks the exports page url for export date changes.

    Returns a true alert once a change has been found, or a false alert after a
    timeout limit has been exceeded.
    """
    sleep, timeout = self.getWatchTeamExportsValues()
    elapsed = 0

    while elapsed < timeout:
      if self.checkAlert(self.updateTeamExports()):
        return self.sendAlert("Team export date change detected.", True)

      time.sleep(sleep)
      elapsed = elapsed + sleep

    return self.sendAlert("Timeout. Team export date change not detected.", False)

  def watchLeagueFileInternal(self):
    """Itermittently checks the exports page url for league file date changes.

    Returns a true alert once a change has been found, or a false alert after a
    timeout limit has been exceeded.
    """
    sleep, timeout = self.getWatchTeamExportsValues()
    sleep, timeout = self.getWatchLeagueFileValues()
    elapsed = 0

    while elapsed < timeout:
      if self.checkAlert(self.updateLeagueFile()):
        return self.sendAlert("League file date change detected.", True)

      time.sleep(sleep)
      elapsed = elapsed + sleep

    return self.sendAlert("Timeout. League file date change not detected.", False)

  def updateTeamExports(self, url=""):
    """Opens the exports page and checks the export date for a list of teams.

    Returns a true alert if any dates have changed since the previous check.
    """
    page = urllib2.urlopen(url or self.getUrl()).read()
    changed = False
    for team in self.teams:
      export = self.findTeamExport(page, team)
      if export and (team not in self.exports or export != self.exports[team]):
        self.exports[team] = export
        changed = True

    return self.sendAlert("Updated team export dates.", changed)

  def updateLeagueFile(self, url=""):
    """Opens the exports page and checks the date of the league file.

    Returns a true alert if the date has changed since the previous check.
    """
    page = urllib2.urlopen(url or self.getUrl()).read()
    changed = False
    file = self.findLeagueFile(page)
    if file and file != self.file:
      self.file = file
      changed = True

    return self.sendAlert("Updated league file date.", changed)

  def findTeamExport(self, page, team):
    """Parses the exports page and returns the export date for a given team."""
    match = re.findall(re.escape(team) + r"</a><br><([^<]+)<", page)
    chunks = (match[0].split(">") if len(match) else "")
    return (chunks[1] if len(chunks) > 1 else "")

  def findLeagueFile(self, page):
    """Parses the exports page and returns the date of the league file."""
    match = re.findall(r"League File Updated: ([^<]+)<", page)
    return match[0] if len(match) else ""

  def getUrl(self):
    """Returns the exports page url that should be checked for date changes."""
    return "http://orangeandblueleaguebaseball.com/StatsLab/exports.php"

  def getWatchTeamExportsValues(self):
    """Returns a pair of values, in seconds, for the watchTeamExports timer.

    The first value is the amount of time to sleep between consecutive page
    checks. The second value is the amount of time after which the watcher can
    stop checking the page for changes."""
    return [
        600,    # 10 minutes
        36000,  # 10 hours
    ]

  def getWatchLeagueFileValues(self):
    """Returns a pair of values, in seconds, for the watchLeagueFile timer.

    The first value is the amount of time to sleep between consecutive page
    checks. The second value is the amount of time after which the watcher can
    stop checking the page for changes."""
    return [
        300,    # 5 minutes
        18000,  # 5 hours
    ]

  def sendAlert(self, message, value):
    """Returns the specified value.

    TODO: Either surface the message or remove it."""
    return value

  def checkAlert(self, alert):
    """Returns the value of the alert."""
    return alert


class ExportWatcherTest(ExportWatcher):
  """Tests for ExportWatcher."""

  def __init__(self, pages, teams):
    """Stores a few test export pages and teams."""
    self.pages = pages
    self.current = self.pages[0]

    self.teams = teams
    self.exports, self.file = {}, ""

    self.updateTeamExports(self.current)
    self.updateLeagueFile(self.current)

  def getUrl(self):
    """Returns the next test export page."""
    if len(self.pages) > 1:
      self.current = self.pages.pop(0)
    else:
      self.current = self.pages[0]

    return self.current

  def getWatchTeamExportsValues(self):
    """Returns a pair of test values, in seconds."""
    return [1, 4]

  def getWatchLeagueFileValues(self):
    """Returns a pair of test values, in seconds."""
    return [1, 4]

  def sendAlert(self, message, value):
    """Returns an easily assertable value."""
    return {
        "value": value,
        "current": self.current,
        "exports": self.exports,
        "file": self.file,
    }

  def checkAlert(self, alert):
    """Returns the value of the alert."""
    return alert["value"]


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--test', dest='test', action='store_true')
  parser.set_defaults(test=False)
  args = parser.parse_args()

  if args.test:
    path = "http://brunnerj.com/orangeandblueleague/"
    files = [
        "export_01142017_1.html",         # 0. Initial exports page.
        "export_01142017_2.html",         # 1. No watched teams have changed.
        "export_01142017_3.html",         # 2. Twins export date has changed.
        "export_01172017_1.html",         # 3. League file date has changed.
    ]
    pages = [os.path.join(path, fi) for fi in files]
    twins = {
        "old": "Saturday January 14, 2017 08:35:12 EST",
        "new": "Saturday January 14, 2017 22:15:32 EST",
    }
    league = {
        "old": "Saturday January 14, 2017 13:01:09 EST",
        "new": "Tuesday January 17, 2017 09:03:12 EST",
    }

    # Test findTeamExport method.
    exportWatcherTest = ExportWatcherTest(pages[:], ["Twins"])
    page = urllib2.urlopen(pages[0]).read()
    assert exportWatcherTest.findTeamExport(page, "Twins") == twins["old"]
    page = urllib2.urlopen(pages[1]).read()
    assert exportWatcherTest.findTeamExport(page, "Twins") == twins["old"]
    page = urllib2.urlopen(pages[2]).read()
    assert exportWatcherTest.findTeamExport(page, "Twins") == twins["new"]
    page = urllib2.urlopen(pages[3]).read()
    assert exportWatcherTest.findTeamExport(page, "Twins") == twins["new"]

    # Test findLeagueFile method
    exportWatcherTest = ExportWatcherTest(pages[:], ["Twins"])
    page = urllib2.urlopen(pages[0]).read()
    assert exportWatcherTest.findLeagueFile(page) == league["old"]
    page = urllib2.urlopen(pages[1]).read()
    assert exportWatcherTest.findLeagueFile(page) == league["old"]
    page = urllib2.urlopen(pages[2]).read()
    assert exportWatcherTest.findLeagueFile(page) == league["old"]
    page = urllib2.urlopen(pages[3]).read()
    assert exportWatcherTest.findLeagueFile(page) == league["new"]

    # Test updateTeamExports method for changed case.
    exportWatcherTest = ExportWatcherTest(pages[:], ["Twins"])
    assert exportWatcherTest.updateTeamExports() == \
        {"value": False, "current": pages[0], "exports": {
            "Twins": twins["old"]}, "file": league["old"]}
    assert exportWatcherTest.updateTeamExports() == \
        {"value": False, "current": pages[1], "exports": {
            "Twins": twins["old"]}, "file": league["old"]}
    assert exportWatcherTest.updateTeamExports() == \
        {"value": True, "current": pages[2], "exports": {
            "Twins": twins["new"]}, "file": league["old"]}
    assert exportWatcherTest.updateTeamExports() == \
        {"value": False, "current": pages[3], "exports": {
            "Twins": twins["new"]}, "file": league["old"]}
    assert exportWatcherTest.updateTeamExports() == \
        {"value": False, "current": pages[3], "exports": {
            "Twins": twins["new"]}, "file": league["old"]}

    # Test updateTeamExports method for unchanged case.
    exportWatcherTest = ExportWatcherTest(pages[:2], ["Twins"])
    assert exportWatcherTest.updateTeamExports() == \
        {"value": False, "current": pages[0], "exports": {
            "Twins": twins["old"]}, "file": league["old"]}
    assert exportWatcherTest.updateTeamExports() == \
        {"value": False, "current": pages[1], "exports": {
            "Twins": twins["old"]}, "file": league["old"]}
    assert exportWatcherTest.updateTeamExports() == \
        {"value": False, "current": pages[1], "exports": {
            "Twins": twins["old"]}, "file": league["old"]}

    # Test updateLeagueFile method for changed case.
    exportWatcherTest = ExportWatcherTest(pages[:], ["Twins"])
    assert exportWatcherTest.updateLeagueFile() == \
        {"value": False, "current": pages[0], "exports": {
            "Twins": twins["old"]}, "file": league["old"]}
    assert exportWatcherTest.updateLeagueFile() == \
        {"value": False, "current": pages[1], "exports": {
            "Twins": twins["old"]}, "file": league["old"]}
    assert exportWatcherTest.updateLeagueFile() == \
        {"value": False, "current": pages[2], "exports": {
            "Twins": twins["old"]}, "file": league["old"]}
    assert exportWatcherTest.updateLeagueFile() == \
        {"value": True, "current": pages[3], "exports": {
            "Twins": twins["old"]}, "file": league["new"]}
    assert exportWatcherTest.updateLeagueFile() == \
        {"value": False, "current": pages[3], "exports": {
            "Twins": twins["old"]}, "file": league["new"]}

    # Test updateLeagueFile method for unchanged case.
    exportWatcherTest = ExportWatcherTest(pages[:3], ["Twins"])
    assert exportWatcherTest.updateLeagueFile() == \
        {"value": False, "current": pages[0], "exports": {
            "Twins": twins["old"]}, "file": league["old"]}
    assert exportWatcherTest.updateLeagueFile() == \
        {"value": False, "current": pages[1], "exports": {
            "Twins": twins["old"]}, "file": league["old"]}
    assert exportWatcherTest.updateLeagueFile() == \
        {"value": False, "current": pages[2], "exports": {
            "Twins": twins["old"]}, "file": league["old"]}
    assert exportWatcherTest.updateLeagueFile() == \
        {"value": False, "current": pages[2], "exports": {
            "Twins": twins["old"]}, "file": league["old"]}

    # Test watchTeamExportsInternal method for changed case.
    exportWatcherTest = ExportWatcherTest(pages[:], ["Twins"])
    assert exportWatcherTest.watchTeamExportsInternal() == \
        {"value": True, "current": pages[2], "exports": {
            "Twins": twins["new"]}, "file": league["old"]}

    # Test watchTeamExportsInternal method for unchanged case.
    exportWatcherTest = ExportWatcherTest(pages[:2], ["Twins"])
    assert exportWatcherTest.watchTeamExportsInternal() == \
        {"value": False, "current": pages[1], "exports": {
            "Twins": twins["old"]}, "file": league["old"]}

    # Test watchLeagueFileInternal method for changed case.
    exportWatcherTest = ExportWatcherTest(pages[:], ["Twins"])
    assert exportWatcherTest.watchLeagueFileInternal() == \
        {"value": True, "current": pages[3], "exports": {
            "Twins": twins["old"]}, "file": league["new"]}

    # Test watchLeagueFileInternal method for unchanged case.
    exportWatcherTest = ExportWatcherTest(pages[:3], ["Twins"])
    assert exportWatcherTest.watchLeagueFileInternal() == \
        {"value": False, "current": pages[2], "exports": {
            "Twins": twins["old"]}, "file": league["old"]}

    # Test watchTeamExports method for changed case.
    exportWatcherTest = ExportWatcherTest(pages[:], ["Twins"])
    assert exportWatcherTest.watchTeamExports() == True

    # Test watchTeamExports method for unchanged case.
    exportWatcherTest = ExportWatcherTest(pages[:2], ["Twins"])
    assert exportWatcherTest.watchTeamExports() == False

    # Test watchLeagueFile method for changed case.
    exportWatcherTest = ExportWatcherTest(pages[:], ["Twins"])
    assert exportWatcherTest.watchLeagueFile() == True

    # Test watchLeagueFile method for unchanged case.
    exportWatcherTest = ExportWatcherTest(pages[:3], ["Twins"])
    assert exportWatcherTest.watchLeagueFile() == False

    print "Passed."
