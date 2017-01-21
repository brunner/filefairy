#!/usr/bin/env python

import argparse
import datetime
import os
import re
import subprocess
import slack
import sys
import threading
import time
import urllib2

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *


class SimWatcher(QWebView):
  """Watches the live sim page for any changes."""

  def __init__(self, app=None):
    """Does an initial parse of the live sim page."""
    self._page = self._getPage(self._getUrl())
    self._date = self._findDate(self._page)
    self._finals = self._findFinals(self._page)
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
          self._uploadToSlack(queued)
        elapsed = 0
        found = True
        posted = False
      elif found and not posted and elapsed > post:
        self._uploadToSlack(self._getFile(self._date))
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
    date = self._findDate(page)
    finals = self._findFinals(page)
    changed = page != self._page
    queued = ""

    if date != self._date:
      queued = self._getFile(self._date)

    if changed:
      if finals != self._finals:
        self.capture(url, self._getFile(date))
        self._finals = finals

      self._page, self._date = page, date

    return self._sendAlert("Updated live sim page.", changed, queued)

  def _findDate(self, page):
    match = re.findall(r"MAJOR LEAGUE BASEBALL<br(?: /)?>([^<]+)<", page)
    return match[0].replace("/", "").strip() if len(match) else ""

  def _findFinals(self, page):
    boxes = re.findall(r"FINAL</td>(.*?)</table>", page, re.DOTALL)
    games = set()
    for box in boxes:
      games.add("".join(re.findall(r"teams/team_([^\.]+)\.html", box)))

    return games

  def _findUpdates(self, page):
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
        updates.append(self._formatUpdates(teams, runs, inning, summary))

    return updates

  def _formatUpdates(self, teams, runs, inning, summary):
    if len(teams) != 2 or len(runs) != 2 or len(inning) != 2:
      self._sendAlert("Failed to format {0} teams, {1} runs, {2} inning.".format(
          len(teams), len(runs), len(innings)), False)
      return ""

    if inning[1] == "&nbsp;":
      time = "Top {0}".format(filter(str.isdigit, inning[0]))
    else:
      time = "Bot {0}".format(filter(str.isdigit, inning[1]))

    score = " ".join([j for i in zip(teams, runs) for j in i])
    return "{0}: {1}. {2}".format(time, score, summary)

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

  def _uploadToSlack(self, queued):
    """Posts the queued photo to the Slack team, from a background thread."""
    t = ThreadedUpload(queued)
    self._threads.append(t)
    t.start()


class ThreadedUpload(threading.Thread):
  """Posts a queued photo to the Slack team from a background thread."""

  def __init__(self, filename):
    """Stores a filename to be uploaded."""
    self.filename = filename

    threading.Thread.__init__(self)

  def run(self):
    slack.upload(self.filename)
    # subprocess.call(["rm", self.filename])


class SimWatcherTest(SimWatcher):
  """Tests for SimWatcher."""

  def __init__(self, app, urls):
    """Stores a few test sim urls."""
    self._urls = urls
    self._current = self._urls[0]
    self._captured = {}
    self._posted = []

    self._page = self._getPage(self._current)
    self._date = self._findDate(self._page)
    self._finals = self._findFinals(self._page)
    self._threads = []

    self._setUp(app)
    self._updateLiveSim(self._current)

  def capture(self, url, output_file):
    """Stores the captured file and url for asserting."""
    self._captured[output_file] = url

  def _getUrl(self):
    """Returns the next test sim page."""
    if len(self._urls) > 1:
      self._current = self._urls.pop(0)
    else:
      self._current = self._urls[0]

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
        "finals": self._finals,
        "captured": self._captured,
        "posted": self._posted,
    }

  def _uploadToSlack(self, queued):
    """Stores the queued photo for asserting."""
    self._posted.append(queued)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--test', dest='test', action='store_true')
  parser.set_defaults(test=False)
  args = parser.parse_args()

  if args.test:
    app = QApplication(sys.argv)

    # Real data.
    url = "http://orangeandblueleaguebaseball.com/league/OBL/reports/news/html/real_time_sim/index.html"
    page = urllib2.urlopen(url).read()
    simWatcherTest = SimWatcherTest(app, [url])
    assert simWatcherTest._findDate(page) != ""
    assert simWatcherTest._findFinals(page) != []

    # Test data.
    path = "http://brunnerj.com/orangeandblueleague/"
    files = [
        "sim_09052018_1.html",            # 0. Initial sim page.
        "sim_09052018_2.html",            # 1. Same date. No new final games.
        "sim_09052018_3.html",            # 2. Same date. One new final game.
        "sim_09092018_1.html",            # 3. Different date.
    ]
    urls = [os.path.join(path, fi) for fi in files]
    dates = {
        "old": "09052018",
        "new": "09092018",
    }
    files = {
        "old": "simwatcher_09052018.png",
        "new": "simwatcher_09092018.png",
    }
    finals = {
        "old1": set(["5933"]),
        "old2": set(["5933", "5345"]),
        "new": set(["3348", "4151", "3456", "3637", "5035",
                    "4254", "3955", "4645", "5847", "4038",
                    "4952", "6032", "4459", "4357"]),
    }
    updates = {
        "old1": "Top 4: PIT 10 SF 0. PIT: C.J. Hinojosa hits a 3-run HR.",
        "old2": "Bot 5: PIT 10 SF 2. SF: David Olmedo-Barrera hits a 2-run HR.",
    }

    # Test _findDate method.
    simWatcherTest = SimWatcherTest(app, urls[:])
    page = urllib2.urlopen(urls[0]).read()
    assert simWatcherTest._findDate(page) == dates["old"]
    page = urllib2.urlopen(urls[1]).read()
    assert simWatcherTest._findDate(page) == dates["old"]
    page = urllib2.urlopen(urls[2]).read()
    assert simWatcherTest._findDate(page) == dates["old"]
    page = urllib2.urlopen(urls[3]).read()
    assert simWatcherTest._findDate(page) == dates["new"]

    # Test _findFinalGames method.
    simWatcherTest = SimWatcherTest(app, urls[:])
    page = urllib2.urlopen(urls[0]).read()
    assert simWatcherTest._findFinals(page) == finals["old1"]
    simWatcherTest = SimWatcherTest(app, urls[:])
    page = urllib2.urlopen(urls[1]).read()
    assert simWatcherTest._findFinals(page) == finals["old1"]
    simWatcherTest = SimWatcherTest(app, urls[:])
    page = urllib2.urlopen(urls[2]).read()
    assert simWatcherTest._findFinals(page) == finals["old2"]
    simWatcherTest = SimWatcherTest(app, urls[:])
    page = urllib2.urlopen(urls[3]).read()
    assert simWatcherTest._findFinals(page) == finals["new"]

    # Test _findUpdates method.
    simWatcherTest = SimWatcherTest(app, urls[:])
    page = urllib2.urlopen(urls[0]).read()
    assert simWatcherTest._findUpdates(page) == [updates["old1"]]
    page = urllib2.urlopen(urls[1]).read()
    assert simWatcherTest._findUpdates(page) == []
    page = urllib2.urlopen(urls[2]).read()
    assert simWatcherTest._findUpdates(page) == [updates["old2"]]
    page = urllib2.urlopen(urls[3]).read()
    assert simWatcherTest._findUpdates(page) == []

    # Test _updateLiveSim method for changed case.
    simWatcherTest = SimWatcherTest(app, urls[:])
    assert simWatcherTest._updateLiveSim() == \
        {"value": False, "secondary_value": "", "current": urls[0],
         "date": dates["old"], "finals": finals["old1"], "captured": {},
         "posted": []}
    assert simWatcherTest._updateLiveSim() == \
        {"value": True, "secondary_value": "", "current": urls[1],
         "date": dates["old"], "finals": finals["old1"], "captured": {},
         "posted": []}
    assert simWatcherTest._updateLiveSim() == \
        {"value": True, "secondary_value": "", "current": urls[2],
         "date": dates["old"], "finals": finals["old2"],
         "captured": {files["old"]: urls[2]}, "posted": []}
    assert simWatcherTest._updateLiveSim() == \
        {"value": True, "secondary_value": files["old"], "current": urls[3],
         "date": dates["new"], "finals": finals["new"],
         "captured": {files["old"]: urls[2], files["new"]: urls[3]},
         "posted": []}
    assert simWatcherTest._updateLiveSim() == \
        {"value": False, "secondary_value": "", "current": urls[3],
         "date": dates["new"], "finals": finals["new"],
         "captured": {files["old"]: urls[2], files["new"]: urls[3]},
         "posted": []}

    # Test _updateLiveSim method for unchanged case.
    simWatcherTest = SimWatcherTest(app, urls[:1])
    assert simWatcherTest._updateLiveSim() == \
        {"value": False, "secondary_value": "", "current": urls[0],
         "date": dates["old"], "finals": finals["old1"], "captured": {},
         "posted": []}
    assert simWatcherTest._updateLiveSim() == \
        {"value": False, "secondary_value": "", "current": urls[0],
         "date": dates["old"], "finals": finals["old1"], "captured": {},
         "posted": []}

    # Test _watchLiveSimInternal method for changed case.
    simWatcherTest = SimWatcherTest(app, urls[:])
    assert simWatcherTest._watchLiveSimInternal() == \
        {"value": True, "secondary_value": "", "current": urls[3],
         "date": dates["new"], "finals": finals["new"],
         "captured": {files["old"]: urls[2], files["new"]: urls[3]},
         "posted": [files["old"], files["new"]]}

    # Test _watchLiveSimInternal method for unchanged case.
    simWatcherTest = SimWatcherTest(app, urls[:1])
    assert simWatcherTest._watchLiveSimInternal() == \
        {"value": False, "secondary_value": "", "current": urls[0],
         "date": dates["old"], "finals": finals["old1"], "captured": {},
         "posted": []}

    # Test _watchLiveSim method for changed case.
    simWatcherTest = SimWatcherTest(app, urls[:])
    assert simWatcherTest._watchLiveSim() == True

    # Test _watchLiveSim method for unchanged case.
    simWatcherTest = SimWatcherTest(app, urls[:1])
    assert simWatcherTest._watchLiveSim() == False

    print "Passed."
