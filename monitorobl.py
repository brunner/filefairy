import datetime
import re
import sys
import time
import urllib2

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

HOST = "http://orangeandblueleaguebaseball.com"

class LiveSimScreenshotter(QWebView):
  def __init__(self):
    self.app = QApplication(sys.argv)
    QWebView.__init__(self)
    self._loaded = False
    self.loadFinished.connect(self._loadFinished)
    self._url = HOST + "/league/OBL/reports/news/html/real_time_sim/index.html"
    self._date = self._getLiveSimDate()

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

  def _getLiveSimDate(self):
    content = urllib2.urlopen(self._url).read()
    date = re.findall(r"MAJOR LEAGUE BASEBALL<br>([^\r]+)\r", content)
    return date[0].replace("/", "") if len(date) else ""

  def _monitor(self):
    elapsed, sleep, timeout = 0, 30, 300
    started = False
    while elapsed < timeout or not started:
      date = self._getLiveSimDate()
      if date != self._date:
        self.capture(self._url, "livesim{0}.png".format(date))
        self._date = date
        elapsed = 0
        started = True
      else:
        elapsed = elapsed + sleep
      time.sleep(sleep)
    return started

class LeagueFileChecker():
  def __init__(self):
    self._url = HOST + "/StatsLab/exports.php"
    self._date = self._getLeagueFileDate()

  def _getLeagueFileDate(self):
    content = urllib2.urlopen(self._url).read()
    date = re.findall(r"League File Updated: ([^<]+)<", content)
    return date[0] if len(date) else ""

  def _monitor(self):
    elapsed, sleep, timeout = 0, 120, 18000
    while elapsed < timeout:
      date = self._getLeagueFileDate()
      if date != self._date:
        self._date = date
        return True
      time.sleep(sleep)
      elapsed = elapsed + sleep
    return False

# class Scheduler():
#   def __init__(self):
#     self._tec = TwinsExportChecker()
#     self._lss = LiveSimScreenshotter()
#     self._lfc = LeagueFileChecker()

#   def _start(self):
#     if self._tec._monitor():
#       print "{0}: Twins export updated.".format(self._getCurrentTime())
#       if self._lss._monitor():
#         print "{0}: Live sim screenshots captured.".format(self._getCurrentTime())
#         if self._lfc._monitor():
#           print "{0}: File uploaded.".format(self._getCurrentTime())
#         else:
#           print "{0}: TIMEOUT. File not uploaded.".format(self._getCurrentTime())
#       else:
#         print "{0}: TIMEOUT. Live sim screenshots not captured.".format(self._getCurrentTime())
#     else:
#       print "{0}: TIMEOUT. Twins export not updated.".format(self._getCurrentTime())


#   def _getCurrentTime(self):
#     return datetime.datetime.now().strftime("%I:%M %p")

# if __name__ == "__main__":
#   s = Scheduler()
#   s._start()