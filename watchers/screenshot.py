#! /usr/bin/python

import os
import subprocess
import sys
import time

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *


class Screenshot(QWebView):

  def __init__(self, app, path):
    self.app = app
    self._path = path
    QWebView.__init__(self)
    self._loaded = False
    self.loadFinished.connect(self._loadFinished)

  def capture(self, html, filename):
    cwd = os.getcwd()
    os.chdir(self._path)

    local = "temp.html"
    with open(local, "w") as f:
      f.write(html)

    self.load(QUrl.fromLocalFile(os.path.join(self._path, local)))
    self.wait_load()
    frame = self.page().mainFrame()
    self.page().setViewportSize(frame.contentsSize())
    qimage = QImage(self.page().viewportSize(), QImage.Format_ARGB32)
    qpainter = QPainter(qimage)
    frame.render(qpainter)
    qpainter.end()
    qimage.save(filename)

    subprocess.call(["rm", local])
    os.chdir(cwd)

  def wait_load(self, delay=0):
    while not self._loaded:
      self.app.processEvents()
      time.sleep(delay)
    self._loaded = False

  def _loadFinished(self, result):
    self._loaded = True