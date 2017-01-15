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

  def watchTeamExports(self):
    """Itermittently checks the exports page url for export date changes.

    Returns true once a change has been found, or false after a timeout limit
    has been exceeded.
    """
    sleep, timeout = self.getWatchValues()
    elapsed = 0

    while elapsed < timeout:
      if self.checkAlert(self.updateTeamExports()):
        return self.sendAlert("Export date change detected.", True)

      time.sleep(sleep)
      elapsed = elapsed + sleep

    return self.sendAlert("Timeout. Export date change not detected.", False)

  def updateTeamExports(self):
    """Opens the exports page and checks the export date for a list of teams.

    Returns true if any dates have changed since the previous check.
    """
    url = self.getUrl()
    page = urllib2.urlopen(url).read()
    changed = False
    for team in self.teams:
      export = self.findTeamExport(page, team)
      if export and (team not in self.exports or export != self.exports[team]):
        self.exports[team] = export
        changed = True

    return self.sendAlert("Updated export dates.", changed)

  def findTeamExport(self, page, team):
    """Parses the exports page and returns the export date for a given team."""
    match = re.findall(re.escape(team) + r"</a><br><([^<]+)<", page)
    chunks = (match[0].split(">") if len(match) else "")
    return (chunks[1] if len(chunks) > 1 else "")

  def getUrl(self):
    """Returns the exports page url that should be checked for date changes."""
    return "http://orangeandblueleaguebaseball.com/StatsLab/exports.php"

  def getWatchValues(self):
    """Returns a pair of values, in seconds, corresponding to the watch timer.

    The first value is the amount of time to sleep between consecutive page
    checks. The second value is the amount of time after which the watcher can
    stop checking the page for changes."""
    return [600, 36000]

  def sendAlert(self, message, ret):
    """Returns the specified value.

    TODO: Either surface the message or remove it."""
    return ret

  def checkAlert(self, alert):
    """Returns the value of the alert."""
    return alert


class ExportWatcherTest(ExportWatcher):
  """Tests for ExportWatcher."""

  def __init__(self, pages, teams):
    """Stores a few test export pages and teams."""
    self.pages = pages
    self.teams = teams
    self.exports, self.file = {}, ""

    self.updateTeamExports()

  def getUrl(self):
    """Returns the next test export page."""
    if len(self.pages) > 1:
      return self.pages.pop(0)

    return self.pages[0] if len(self.pages) else ""

  def getWatchValues(self):
    """Returns a pair of test values, in seconds."""
    return [1, 4]

  def sendAlert(self, message, ret):
    """Returns an easily assertable value."""
    return {"value": ret, "pages": self.pages, "exports": self.exports}

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
        "export_01142017_1.html",  # 1. Initial exports page.
        "export_01142017_2.html",  # 2. No exports date change.
        "export_01142017_3.html",  # 3. Twins export date has changed.
    ]
    pages = [os.path.join(path, fi) for fi in files]
    old = "Saturday January 14, 2017 08:35:12 EST"
    new = "Saturday January 14, 2017 22:15:32 EST"

    # Test findTeamExport method.
    exportWatcherTest = ExportWatcherTest(pages[:], ["Twins"])
    page = urllib2.urlopen(pages[0]).read()
    assert exportWatcherTest.findTeamExport(page, "Twins") == \
        "Saturday January 14, 2017 08:35:12 EST"

    # Test updateTeamExports method for changed case.
    exportWatcherTest = ExportWatcherTest(pages[:], ["Twins"])
    assert exportWatcherTest.updateTeamExports() == \
        {"value": False, "pages": pages[2:], "exports": {"Twins": old}}
    assert exportWatcherTest.updateTeamExports() == \
        {"value": True, "pages": pages[2:], "exports": {"Twins": new}}
    assert exportWatcherTest.updateTeamExports() == \
        {"value": False, "pages": pages[2:], "exports": {"Twins": new}}

    # Test watchTeamExports method for changed case.
    exportWatcherTest = ExportWatcherTest(pages[:], ["Twins"])
    assert exportWatcherTest.watchTeamExports() == \
        {"value": True, "pages": pages[2:], "exports": {"Twins": new}}

    # Test updateTeamExports method for unchanged case.
    exportWatcherTest = ExportWatcherTest(pages[:2], ["Twins"])
    assert exportWatcherTest.updateTeamExports() == \
        {"value": False, "pages": pages[1:2], "exports": {"Twins": old}}
    assert exportWatcherTest.updateTeamExports() == \
        {"value": False, "pages": pages[1:2], "exports": {"Twins": old}}

    # Test watchTeamExports method for unchanged case.
    exportWatcherTest = ExportWatcherTest(pages[:2], ["Twins"])
    assert exportWatcherTest.watchTeamExports() == \
        {"value": False, "pages": pages[1:2], "exports": {"Twins": old}}

    print "Passed."
