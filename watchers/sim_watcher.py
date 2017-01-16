#!/usr/bin/env python

import argparse
import os
import re
import subprocess
import sys
import time
import tokens
import urllib2

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *


class SimWatcher(QWebView):
  """Watches the live sim page for any changes."""

  def __init__(self, app):
    """Does an initial parse of the live sim page."""
    self._page = self._getPage(self._getUrl())
    self._date = self._findSimDate(self._page)

    self._setUp(app or QApplication(sys.argv))
    self._updateLiveSim()

  def _setUp(self, app):
    self.app = app
    QWebView.__init__(self)

    self._loaded = False
    self.loadFinished.connect(self._loadFinished)

  def capture(self, url, output_file):
    self.load(QUrl(url))
    self.wait_load()
    frame = self.page().mainFrame()
    self.page().setViewportSize(frame.contentsSize())
    image = QImage(self.page().viewportSize(), QImage.Format_ARGB32)
    painter = QPainter(image)
    frame.render(painter)
    painter.end()
    image.save(output_file)

  def wait_load(self, delay=0):
    while not self._loaded:
      self.app.processEvents()
      time.sleep(delay)
    self._loaded = False

  def _loadFinished(self, result):
    self._loaded = True

  def _watchLiveSim(self):
    """Itermittently checks the sim page url for any changes.

    If any changes are found, wait for a certain amount of time to capture any
    additional changes. If not, abandon watching after a timeout.
    Returns a true alert if any changes were found.
    """
    sleep, wait, timeout = self._getWatchLiveSimValues()
    elapsed = 0
    previous = 1
    found = False

    while (found and elapsed < wait) or (not found and elapsed < timeout):
      if self._checkAlert(self._updateLiveSim()):
        elapsed = 0
        found = True
      elif found:
        time.sleep(previous)
        temp = elapsed
        elapsed = elapsed + previous
        previous = temp
      else:
        time.sleep(sleep)
        elapsed = elapsed + sleep

    if found:
      self._postScreenshot()
      return self._sendAlert("Live sim change detected.", True)
    else:
      return self._sendAlert("Timeout. Live sim change not detected.", False)

  def _updateLiveSim(self, url=""):
    """Opens the live sim page and checks the page content.

    Returns a true alert if the content has changed since the previous check.
    """
    url = url or self._getUrl()
    page = self._getPage(url)
    date = self._findSimDate(page)
    if date != self._date:
      self._postScreenshot()

    changed = False
    if page != self._page:
      self.capture(url, "sim_{0}.png".format(date))
      self._page, self._date = page, date
      changed = True

    return self._sendAlert("Updated live sim page.", changed)

  def _findSimDate(self, page):
    match = re.findall(r"MAJOR LEAGUE BASEBALL<br>([^<]+)<", page)
    return match[0].replace("/", "").strip() if len(match) else ""

  def _getPage(self, url):
    return urllib2.urlopen(url).read()

  def _getUrl(self):
    """Returns the live sim page url that should be checked for date changes."""
    return "http://orangeandblueleaguebaseball.com/league/OBL/reports/news/html/real_time_sim/index.html"

  def _getWatchLiveSimValues(self):
    """Returns a tuple of values, in seconds, for the watchLiveSim timer.

    The first value is the amount of time to sleep between consecutive page
    checks, before any page changes have been detected. The second value is the
    amount of time to wait before the watcher can stop checking the page for
    changes, once the first change has been detected. The third value is the
    amount of time after which the watcher times out, if a first change was
    never found."""
    return [
        8,      # 8 seconds
        3600,   # 1 hour
        7200,   # 2 hours
    ]

  def _sendAlert(self, message, value):
    """Returns the specified value.

    TODO: Either surface the message or remove it."""
    return value

  def _checkAlert(self, alert):
    """Returns the value of the alert."""
    return alert

  def _postScreenshot(self):
    """Posts the captured photo to the Slack team before deleting the file."""
    screenshot = "sim_{0}.png".format(self._date)
    fi = "file=@{0}".format(screenshot)
    token = "token={0}".format(tokens.filefairy)
    url = "https://slack.com/api/files.upload"
    with open(os.devnull, "wb") as f:
      subprocess.call(["curl", "-F", fi, "-F", "channels=#general",
                       "-F", token, url], stderr=f, stdout=f)
    subprocess.call(["rm", screenshot])


class TestSimWatcher(SimWatcher):
  """Tests for SimWatcher."""

  def __init__(self, app, pages):
    """Stores a few test sim pages."""
    self._pages = pages
    self._current = self._pages[0]
    self._captured = {}
    self._posted = []

    self._page = self._getPage(self._current)
    self._date = self._findSimDate(self._page)

    self._setUp(app)
    self._updateLiveSim(self._current)

  def capture(self, url, output_file):
    self._captured[output_file] = url

  def _getUrl(self):
    """Returns the next test sim page."""
    if len(self._pages) > 1:
      self._current = self._pages.pop(0)
    else:
      self._current = self._pages[0]

    return self._current

  def _getWatchLiveSimValues(self):
    """Returns a tuple of test values, in seconds."""
    return [1, 3, 5]

  def _sendAlert(self, message, value):
    """Returns an easily assertable value."""
    return {
        "value": value,
        "current": self._current,
        "date": self._date,
        "captured": self._captured,
        "posted": self._posted,
    }

  def _checkAlert(self, alert):
    """Returns the value of the alert."""
    return alert["value"]

  def _postScreenshot(self):
    """Stores the captured photo for asserting."""
    screenshot = "sim_{0}.png".format(self._date)
    self._posted.append(screenshot)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--test', dest='test', action='store_true')
  parser.set_defaults(test=False)
  args = parser.parse_args()

  if args.test:
    path = "http://brunnerj.com/orangeandblueleague/"
    files = [
        "sim_09052018_1.html",            # 0. Initial sim page.
        "sim_09052018_2.html",            # 1. Same date, but data changed.
        "sim_09052018_3.html",            # 2. Same date, but data changed.
        "sim_09092018_1.html",            # 3. Different date.
    ]
    pages = [os.path.join(path, fi) for fi in files]
    dates = {
        "old": "09052018",
        "new": "09092018",
    }
    files = {
        "old": "sim_09052018.png",
        "new": "sim_09092018.png",
    }

    app = QApplication(sys.argv)

    # Test _findSimDate method.
    simWatcherTest = TestSimWatcher(app, pages[:])
    page = urllib2.urlopen(pages[0]).read()
    assert simWatcherTest._findSimDate(page) == dates["old"]
    page = urllib2.urlopen(pages[1]).read()
    assert simWatcherTest._findSimDate(page) == dates["old"]
    page = urllib2.urlopen(pages[2]).read()
    assert simWatcherTest._findSimDate(page) == dates["old"]
    page = urllib2.urlopen(pages[3]).read()
    assert simWatcherTest._findSimDate(page) == dates["new"]

    # Test _updateLiveSim method for changed case.
    simWatcherTest = TestSimWatcher(app, pages[:])
    assert simWatcherTest._updateLiveSim() == \
        {"value": False, "current": pages[0], "date": dates[
            "old"], "captured": {}, "posted": []}
    assert simWatcherTest._updateLiveSim() == \
        {"value": True, "current": pages[1], "date": dates[
            "old"], "captured": {files["old"]: pages[1]}, "posted": []}
    assert simWatcherTest._updateLiveSim() == \
        {"value": True, "current": pages[2], "date": dates[
            "old"], "captured": {files["old"]: pages[2]}, "posted": []}
    assert simWatcherTest._updateLiveSim() == \
        {"value": True, "current": pages[3], "date": dates["new"], "captured": {
            files["old"]: pages[2], files["new"]: pages[3]}, "posted": [files["old"]]}
    assert simWatcherTest._updateLiveSim() == \
        {"value": False, "current": pages[3], "date": dates["new"], "captured": {
            files["old"]: pages[2], files["new"]: pages[3]}, "posted":
         [files["old"]]}

    # Test _updateLiveSim method for unchanged case.
    simWatcherTest = TestSimWatcher(app, pages[:1])
    assert simWatcherTest._updateLiveSim() == \
        {"value": False, "current": pages[0], "date": dates[
            "old"], "captured": {}, "posted": []}
    assert simWatcherTest._updateLiveSim() == \
        {"value": False, "current": pages[0], "date": dates[
            "old"], "captured": {}, "posted": []}

    # Test _watchLiveSim method for changed case.
    simWatcherTest = TestSimWatcher(app, pages[:])
    assert simWatcherTest._watchLiveSim() == \
        {"value": True, "current": pages[3], "date": dates["new"], "captured": {files[
            "old"]: pages[2], files["new"]: pages[3]}, "posted": [files["old"], files["new"]]}

    # Test _watchLiveSim method for unchanged case.
    simWatcherTest = TestSimWatcher(app, pages[:1])
    assert simWatcherTest._watchLiveSim() == \
        {"value": False, "current": pages[0], "date": dates[
            "old"], "captured": {}, "posted": []}

    print "Passed."
