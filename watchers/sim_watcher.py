#!/usr/bin/env python

import argparse
import datetime
import os
import re
import subprocess
import sys
import threading
import time
import tokens
import urllib2

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *


class SimWatcher(QWebView):
  """Watches the live sim page for any changes."""

  def __init__(self, app=None):
    """Does an initial parse of the live sim page."""
    self._page = self._getPage(self._getUrl())
    self._date = self._findSimDate(self._page)
    self._threads = []

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
    Returns true if any changes were found.
    """
    return self._checkAlert(self._watchLiveSimInternal())

  def _watchLiveSimInternal(self):
    """Itermittently checks the sim page url for any changes.

    If any changes are found, wait for a certain amount of time to capture any
    additional changes. If not, abandon watching after a timeout.
    Returns a true alert if any changes were found.
    """
    sleep, post, timeout = self._getWatchLiveSimValues()
    elapsed = 0
    previous = 1
    found = False
    posted = False

    while elapsed < timeout:
      alert = self._updateLiveSim()
      queued = self._checkSecondaryAlert(alert)

      if self._checkAlert(alert):
        if queued:
          self._postScreenshot(queued)
        elapsed = 0
        found = True
        posted = False
      elif found and not posted and elapsed > post:
        self._postScreenshot(self._getFile(self._date))
        posted = True

      time.sleep(sleep)
      elapsed = elapsed + sleep

    if found:
      alert = self._sendAlert("Live sim change detected.", True)
    else:
      alert = self._sendAlert("Timeout. Live sim change not detected.", False)

    for t in self._threads:
      t.join()

    return alert

  def _updateLiveSim(self, url=""):
    """Opens the live sim page and checks the page content.

    Returns a true alert if the content has changed since the previous check.
    """
    url = url or self._getUrl()
    page = self._getPage(url)
    date = self._findSimDate(page)
    changed = page != self._page
    queued = ""

    if date != self._date:
      queued = self._getFile(self._date)

    if changed:
      self.capture(url, self._getFile(date))
      self._page, self._date = page, date

    return self._sendAlert("Updated live sim page.", changed, queued)

  def _findSimDate(self, page):
    match = re.findall(r"MAJOR LEAGUE BASEBALL<br(?: /)?>([^<]+)<", page)
    return match[0].replace("/", "").strip() if len(match) else ""

  def _getPage(self, url):
    return urllib2.urlopen(url).read()

  def _getUrl(self):
    """Returns the live sim page url that should be checked for date changes."""
    return "http://orangeandblueleaguebaseball.com/league/OBL/reports/news/html/real_time_sim/index.html"

  def _getWatchLiveSimValues(self):
    """Returns a tuple of values, in seconds, for the watchLiveSim timer."""
    return [
        6,      # 6 seconds, to sleep between consecutive page checks.
        120,    # 2 minutes, to wait before posting a screenshot (during which
                #     the page has stopped changing and the sim is presumed
                #     to be over).
        3600,   # 1 hour, to wait before officially timing out (during which
                #     the page has not changed and the sim is presumed
                #     to be over).
    ]

  def _getFile(self, date):
    """Gets the file name to use for a given live sim date."""
    return "simwatcher_{0}.png".format(date)

  def _sendAlert(self, message, value, secondary_value=""):
    """Returns the specified value."""
    print "{0}: {1}".format(str(datetime.datetime.now()), message)
    return {
        "value": value,
        "secondary_value": secondary_value,
    }

  def _checkAlert(self, alert):
    """Returns the value of the alert."""
    return alert["value"]

  def _checkSecondaryAlert(self, alert):
    """Returns the secondary value of the alert."""
    return alert["secondary_value"]

  def _postScreenshot(self, queued):
    """Posts the queued photo to the Slack team, from a background thread."""
    t = ThreadedPostScreenshot(queued)
    self._threads.append(t)
    t.start()


class ThreadedPostScreenshot(threading.Thread):
  """Posts a queued photo to the Slack team from a background thread."""

  def __init__(self, queued):
    """Stores a reference to the queued photo file."""
    self.queued = queued

    threading.Thread.__init__(self)

  def run(self):
    fi = "file=@{0}".format(self.queued)
    token = "token={0}".format(tokens.filefairy)
    url = "https://slack.com/api/files.upload"
    with open(os.devnull, "wb") as f:
      subprocess.call(["curl", "-F", fi, "-F", "channels=#general",
                       "-F", token, url], stderr=f, stdout=f)
    subprocess.call(["rm", self.queued])


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
    self._threads = []

    self._setUp(app)
    self._updateLiveSim(self._current)

  def capture(self, url, output_file):
    """Stores the captured file and url for asserting."""
    self._captured[output_file] = url

  def _getUrl(self):
    """Returns the next test sim page."""
    if len(self._pages) > 1:
      self._current = self._pages.pop(0)
    else:
      self._current = self._pages[0]

    return self._current

  def _getWatchLiveSimValues(self):
    """Returns a tuple of test values, in seconds, for the watchLiveSim timer."""
    return [1, 2, 8]

  def _sendAlert(self, message, value, secondary_value=""):
    """Returns an easily assertable value."""
    return {
        "value": value,
        "secondary_value": secondary_value,
        "current": self._current,
        "date": self._date,
        "captured": self._captured,
        "posted": self._posted,
    }

  def _postScreenshot(self, queued):
    """Stores the queued photo for asserting."""
    self._posted.append(queued)


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
        "old": "simwatcher_09052018.png",
        "new": "simwatcher_09092018.png",
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
        {"value": False, "secondary_value": "", "current": pages[
            0], "date": dates["old"], "captured": {}, "posted": []}
    assert simWatcherTest._updateLiveSim() == \
        {"value": True, "secondary_value": "", "current": pages[1], "date": dates[
            "old"], "captured": {files["old"]: pages[1]}, "posted": []}
    assert simWatcherTest._updateLiveSim() == \
        {"value": True, "secondary_value": "", "current": pages[2], "date": dates[
            "old"], "captured": {files["old"]: pages[2]}, "posted": []}
    assert simWatcherTest._updateLiveSim() == \
        {"value": True, "secondary_value": files["old"], "current": pages[3], "date": dates[
            "new"], "captured": {files["old"]: pages[2], files["new"]: pages[3]}, "posted": []}
    assert simWatcherTest._updateLiveSim() == \
        {"value": False, "secondary_value": "", "current": pages[3], "date": dates[
            "new"], "captured": {files["old"]: pages[2], files["new"]: pages[3]}, "posted": []}

    # Test _updateLiveSim method for unchanged case.
    simWatcherTest = TestSimWatcher(app, pages[:1])
    assert simWatcherTest._updateLiveSim() == \
        {"value": False, "secondary_value": "", "current": pages[
            0], "date": dates["old"], "captured": {}, "posted": []}
    assert simWatcherTest._updateLiveSim() == \
        {"value": False, "secondary_value": "", "current": pages[
            0], "date": dates["old"], "captured": {}, "posted": []}

    # Test _watchLiveSimInternal method for changed case.
    simWatcherTest = TestSimWatcher(app, pages[:])
    assert simWatcherTest._watchLiveSimInternal() == \
        {"value": True, "secondary_value": "", "current": pages[3], "date": dates["new"], "captured": {
            files["old"]: pages[2], files["new"]: pages[3]}, "posted": [files["old"], files["new"]]}

    # Test _watchLiveSimInternal method for unchanged case.
    simWatcherTest = TestSimWatcher(app, pages[:1])
    assert simWatcherTest._watchLiveSimInternal() == \
        {"value": False, "secondary_value": "", "current": pages[
            0], "date": dates["old"], "captured": {}, "posted": []}

    # Test _watchLiveSim method for changed case.
    simWatcherTest = TestSimWatcher(app, pages[:])
    assert simWatcherTest._watchLiveSim() == True

    # Test _watchLiveSim method for unchanged case.
    simWatcherTest = TestSimWatcher(app, pages[:1])
    assert simWatcherTest._watchLiveSim() == False

    print "Passed."
