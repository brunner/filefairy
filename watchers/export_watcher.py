#!/usr/bin/env python

import argparse
import datetime
import os
import re
import slack
import threading
import time
import urllib2

from logger import Logger


class ExportWatcher(object):
  """Watches the exports page for export and league file date changes."""

  def __init__(self, logger=None):
    """Does an initial parse of the exports page."""
    self.logger = logger or Logger()

    self.file = ""
    self.updateLeagueFile()

  def watchLeagueFile(self, fileIsUp, simIsInProgress):
    """Itermittently checks the exports page url for league file date changes.

    Returns true once a change has been found, or false after a timeout limit
    has been exceeded.
    """
    alert = self.checkAlert(self.watchLeagueFileInternal(simIsInProgress))
    fileIsUp.set()

    return alert

  def watchLeagueFileInternal(self, simIsInProgress):
    """Itermittently checks the exports page url for league file date changes.

    Returns a true alert once a change has been found, or a false alert after a
    timeout limit has been exceeded.
    """
    sleep, timeout = self.getWatchLeagueFileValues()
    elapsed = 0

    self.logger.log("Started watching file.")

    while elapsed < timeout:
      if not simIsInProgress.is_set():
        if self.checkAlert(self.updateLeagueFile()):
          self.postToSlack("File is up.", "general")
          self.logger.log("Done watching file: success.")
          return self.sendAlert(True)

      time.sleep(sleep)
      elapsed = elapsed + sleep

    self.logger.log("Done watching file: failure.")
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