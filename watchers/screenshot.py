#! /usr/bin/python

import os
import subprocess
import sys
import time

from PIL import Image
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

  def capture(self, url, output_file):
    cwd = os.getcwd()
    os.chdir(self._path)

    self.load(QUrl(url))
    self.wait_load()
    frame = self.page().mainFrame()
    self.page().setViewportSize(frame.contentsSize())
    qimage = QImage(self.page().viewportSize(), QImage.Format_ARGB32)
    qpainter = QPainter(qimage)
    frame.render(qpainter)
    qpainter.end()

    if os.path.exists(os.path.join(self._path, output_file)):
      tmp_output_file = "tmp" + output_file
      qimage.save(tmp_output_file)
      with Image.open(os.path.join(self._path, output_file)) as image:
        with Image.open(os.path.join(self._path, tmp_output_file)) as tmp_image:
          if tmp_image.size[1] < image.size[1]:
            subprocess.call(["rm", tmp_output_file])
          else:
            subprocess.call(["mv", tmp_output_file, output_file])
    else:
      qimage.save(output_file)

    os.chdir(cwd)

  def wait_load(self, delay=0):
    while not self._loaded:
      self.app.processEvents()
      time.sleep(delay)
    self._loaded = False

  def _loadFinished(self, result):
    self._loaded = True