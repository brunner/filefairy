#!/usr/bin/env python

import argparse
import datetime
import slack
import os
import re
import time
import urllib2


class ExportWatcher(object):
  """Watches the exports page for export and league file date changes."""

  def __init__(self):
    """Does an initial parse of the exports page."""
    self.file = ""
    self.updateLeagueFile()

  def watchLeagueFile(self):
    """Itermittently checks the exports page url for league file date changes.

    Returns true once a change has been found, or false after a timeout limit
    has been exceeded.
    """
    return self.checkAlert(self.watchLeagueFileInternal())

  def watchLeagueFileInternal(self):
    """Itermittently checks the exports page url for league file date changes.

    Returns a true alert once a change has been found, or a false alert after a
    timeout limit has been exceeded.
    """
    sleep, timeout = self.getWatchLeagueFileValues()
    elapsed = 0

    self.postToSlack("Watching file.", "testing")

    while elapsed < timeout:
      if self.checkAlert(self.updateLeagueFile()):
        self.postToSlack("File is up.", "general")
        return self.sendAlert(True)

      time.sleep(sleep)
      elapsed = elapsed + sleep

    self.postToSlack("File date change not detected.", "testing")
    return self.sendAlert(False)

  def updateLeagueFile(self, url=""):
    """Opens the exports page and checks the date of the league file.

    Returns a true alert if the date has changed since the previous check.
    """
    url = url or self.getUrl()
    page = self.getPage(url)
    changed = False
    file = self.findLeagueFile(page)
    if file and file != self.file:
      self.file = file
      changed = True

    return self.sendAlert(changed)

  def findLeagueFile(self, page):
    """Parses the exports page and returns the date of the league file."""
    match = re.findall(r"League File Updated: ([^<]+)<", page)
    return match[0] if len(match) else ""

  def postToSlack(self, message, channel):
    """Posts the message to the Slack team."""
    slack.postMessage(message, channel)

  def getPage(self, url):
    try:
      page = urllib2.urlopen(url).read()
    except Exception as e:
      page = ""

    return page

  def getUrl(self):
    """Returns the exports page url that should be checked for date changes."""
    return "http://orangeandblueleaguebaseball.com/StatsLab/exports.php"

  def getWatchLeagueFileValues(self):
    """Returns a pair of values, in seconds, for the watchLeagueFile timer.

    The first value is the amount of time to sleep between consecutive page
    checks. The second value is the amount of time after which the watcher can
    stop checking the page for changes."""
    return [
        30,     # 30 seconds
        82800,  # 23 hours
    ]

  def sendAlert(self, value):
    """Returns the specified value."""
    return value

  def checkAlert(self, alert):
    """Returns the value of the alert."""
    return alert


class ExportWatcherTest(ExportWatcher):
  """Tests for ExportWatcher."""

  def __init__(self, urls, filefairy=False):
    """Stores a few test export urls and teams.

    Pass filefairy=True to interface with the testing Slack channel."""
    self.urls = urls
    self.current = self.urls[0]
    self.posted = []
    self.filefairy = filefairy

    self.file = ""
    self.updateLeagueFile(self.current)

  def postToSlack(self, message, channel):
    """Stores the message for asserting. Channel is overridden."""
    self.posted.append(message)
    if self.filefairy:
      slack.postMessage(message, "testing")

  def getUrl(self):
    """Returns the next test export page."""
    if len(self.urls) > 1:
      self.current = self.urls.pop(0)
    else:
      self.current = self.urls[0]

    return self.current

  def getWatchLeagueFileValues(self):
    """Returns a pair of test values, in seconds."""
    return [1, 4]

  def sendAlert(self, value):
    """Returns an easily assertable value."""
    return {
        "value": value,
        "current": self.current,
        "file": self.file,
        "posted": self.posted,
    }

  def checkAlert(self, alert):
    """Returns the value of the alert."""
    return alert["value"]


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
    if args.real:
      # Real data.
      url = "http://orangeandblueleaguebaseball.com/StatsLab/exports.php"
      page = urllib2.urlopen(url).read()
      exportWatcherTest = ExportWatcherTest([url], args.filefairy)
      assert exportWatcherTest.findLeagueFile(page) != ""

    # Test data.
    path = "http://brunnerj.com/orangeandblueleague/"
    files = [
        "export_01142017_1.html",         # 0. Initial exports page.
        "export_01142017_2.html",         # 1. League file date has not changed.
        "export_01172017_1.html",         # 3. League file date has changed.
    ]
    urls = [os.path.join(path, fi) for fi in files]
    league = {
        "old": "Saturday January 14, 2017 13:01:09 EST",
        "new": "Tuesday January 17, 2017 09:03:12 EST",
    }
    updates = {
        "file1": "Watching file.",
        "file2": "File is up.",
        "file3": "File date change not detected.",
    }

    # Test findLeagueFile method
    exportWatcherTest = ExportWatcherTest(urls[:])
    page = urllib2.urlopen(urls[0]).read()
    assert exportWatcherTest.findLeagueFile(page) == league["old"]
    page = urllib2.urlopen(urls[1]).read()
    assert exportWatcherTest.findLeagueFile(page) == league["old"]
    page = urllib2.urlopen(urls[2]).read()
    assert exportWatcherTest.findLeagueFile(page) == league["new"]

    # Test updateLeagueFile method for changed case.
    exportWatcherTest = ExportWatcherTest(urls[:])
    assert exportWatcherTest.updateLeagueFile() == \
        {"value": False, "current": urls[0], "file": league["old"], "posted": []}
    assert exportWatcherTest.updateLeagueFile() == \
        {"value": False, "current": urls[1], "file": league["old"], "posted": []}
    assert exportWatcherTest.updateLeagueFile() == \
        {"value": True, "current": urls[2], "file": league["new"], "posted": []}
    assert exportWatcherTest.updateLeagueFile() == \
        {"value": False, "current": urls[2], "file": league["new"], "posted": []}

    # Test updateLeagueFile method for unchanged case.
    exportWatcherTest = ExportWatcherTest(urls[:2])
    assert exportWatcherTest.updateLeagueFile() == \
        {"value": False, "current": urls[0], "file": league["old"], "posted": []}
    assert exportWatcherTest.updateLeagueFile() == \
        {"value": False, "current": urls[1], "file": league["old"], "posted": []}
    assert exportWatcherTest.updateLeagueFile() == \
        {"value": False, "current": urls[1], "file": league["old"], "posted": []}

    # Test watchLeagueFileInternal method for changed case.
    exportWatcherTest = ExportWatcherTest(urls[:])
    assert exportWatcherTest.watchLeagueFileInternal() == \
        {"value": True, "current": urls[2], "file": league["new"],
         "posted": [updates["file1"], updates["file2"]]}

    # Test watchLeagueFileInternal method for unchanged case.
    exportWatcherTest = ExportWatcherTest(urls[:2])
    assert exportWatcherTest.watchLeagueFileInternal() == \
        {"value": False, "current": urls[1], "file": league["old"],
         "posted": [updates["file1"], updates["file3"]]}

    # Test watchLeagueFile method for changed case.
    exportWatcherTest = ExportWatcherTest(urls[:], args.filefairy)
    assert exportWatcherTest.watchLeagueFile() == True

    # Test watchLeagueFile method for unchanged case.
    exportWatcherTest = ExportWatcherTest(urls[:2], args.filefairy)
    assert exportWatcherTest.watchLeagueFile() == False

    print "Passed."
