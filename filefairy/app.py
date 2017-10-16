#!/usr/bin/env python

import json
import os
import re
import subprocess
import slack_api
import sys
import threading
import time
import urllib2
import websocket

from logger import Logger
from slack_api import SlackApi


class App(object):

  def __init__(self, logger, slackApi, app=None):
    self.logger = logger
    self.slackApi = slackApi

    page = self.getPage(self.getFileUrl())
    self.fileDate = self.findFileDate(page)

    self.simPage = self.getPage(self.getSimUrl())
    self.simDate = self.findSimDate(self.simPage)
    self.updates = self.findUpdates(self.simPage)

    self.records = {t: [0, 0, 0] for t in range(31, 61)}
    self.ws = None

    self.launch()

  def launch(self):
    t1 = threading.Thread(target=self.listen)
    t1.start()

    t2 = threading.Thread(target=self.watch)
    t2.start()

    t1.join()
    t2.join()

  def getFileUrl(self):
    return 'http://orangeandblueleaguebaseball.com/StatsLab/exports.php'

  def getSimUrl(self):
    return 'http://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/real_time_sim/index.html'

  def getChannelGeneral(self):
    return 'general'

  def getChannelLiveSimDiscussion(self):
    return 'live-sim-discussion'

  def getChannelStatsplus(self):
    return 'statsplus'

  def getTimerValues(self):
    return [
        15,     # Sleep between consecutive sim page checks.
        60,     # Pause and check if the file is up.
        82800,  # Time out and exiting the program.
    ]

  def getPage(self, url):
    page = ''
    try:
      page = urllib2.urlopen(url).read()
    except urllib2.URLError as e:
      if hasattr(e, 'reason'):
        pass  # Failed to reach server.
      elif hasattr(e, 'code'):
        self.logger.log('Server failed to handle request. {0}.'.format(e.code))
    except:
      self.logger.log('Unspecified exception.')

    return page

  def listen(self):
    def on_message_(ws, message):
      obj = json.loads(message)
      if 'type' not in obj or 'channel' not in obj or 'text' not in obj:
        return

      channel = self.slackApi.getChannel(obj['channel'])
      if obj['type'] == 'message' and channel == self.getChannelStatsplus():
        self.handleStatsplus(obj['text'])

    obj = self.slackApi.rtmConnect()
    if obj['ok'] and 'url' in obj:
      self.slackApi.chatPostMessage('testing', 'Started listening.')
      self.logger.log('Started listening.')

      self.ws = websocket.WebSocketApp(obj['url'], on_message=on_message_)
      self.ws.run_forever()

      self.slackApi.chatPostMessage('testing', 'Done listening.')
      self.logger.log('Done listening.')

  def handleStatsplus(self, text):
    if 'MAJOR LEAGUE BASEBALL Final Scores' in text:
      self.handleFinalScores(text)

  def handleFinalScores(self, text):
    text = text.replace('MAJOR LEAGUE BASEBALL Final Scores', '')
    self.slackApi.chatPostMessage(self.getChannelLiveSimDiscussion(), text)

  def handleClose(self):
    if self.ws:
      self.ws.close()

  def watch(self):
    sleep, pause, timeout = self.getTimerValues()
    elapsed = 0

    self.slackApi.chatPostMessage('testing', 'Started watching.')
    self.logger.log('Started watching.')

    while elapsed < timeout:
      time.sleep(sleep)
      elapsed = elapsed + sleep

      if elapsed % pause == 0 and self.updateLeagueFile():
        elapsed = timeout
      else:
        self.updateLiveSim()

    self.slackApi.chatPostMessage('testing', 'Done watching.')
    self.logger.log('Done watching.')
    self.handleClose()

  def updateLeagueFile(self):
    url = self.getFileUrl()
    page = self.getPage(url)
    date = self.findFileDate(page)

    if not date:
      return False

    if date != self.fileDate:
      self.slackApi.chatPostMessage(self.getChannelGeneral(), 'File is up.')
      self.logger.log('File is up.')
      self.fileDate = date
      return True

    return False

  def updateLiveSim(self):
    url = self.getSimUrl()
    page = self.getPage(url)
    date = self.findSimDate(page)

    if not date:
      return False

    if date != self.simDate:
      self.updates = []
      self.simDate = date
    elif page != self.simPage:
      updates = self.findUpdates(page)
      for update in updates:
        if update not in self.updates:
          self.slackApi.chatPostMessage(
              self.getChannelLiveSimDiscussion(), update)
          self.updates.append(update)

    self.simPage = page
    return True

  def findFileDate(self, page):
    match = re.findall(r'League File Updated: ([^<]+)<', page)
    return match[0] if len(match) else ''

  def findSimDate(self, page):
    match = re.findall(r'MAJOR LEAGUE BASEBALL<br(?: /)?>([^<]+)<', page)
    return match[0].replace('/', '').strip() if len(match) else ''

  def findUpdates(self, page):
    match = re.findall(r'SCORING UPDATES(.*?)</table>', page, re.DOTALL)
    box = match[0] if len(match) == 1 else ''

    rows = re.findall(r'<tr>(.*?)</tr>', box, re.DOTALL)
    updates = []
    for row in reversed(rows):
      cols = re.findall(r'<td(.*?)</td>', row, re.DOTALL)
      if len(cols) == 5:
        teams = re.findall(r'teams/team_(?:\d+)\.html\">([^<]+)<', cols[1])
        runs = re.findall(r'<div(?:[^>]+)>([^<]+)<', cols[2])
        inning = re.findall(r'<div(?:[^>]+)>([^<]+)<', cols[3])
        chunks = cols[4].split('>')
        summary = chunks[1] if len(chunks) > 1 else ''

        if len(teams) == 2 and len(runs) == 2 or len(inning) == 2:
          if inning[1] == '&nbsp;':
            time = ':toparrow: {0}'.format(filter(str.isdigit, inning[0]))
          else:
            time = ':bottomarrow: {0}'.format(filter(str.isdigit, inning[1]))

          score = '{0} {1} {2} {3} {4}'.format(
              teams[0], runs[0], ':separator:', teams[1], runs[1])
          formatted = '{0} {1} {2}\n{3}'.format(
              time, ':separator:', score, summary.replace(':', ''))

          pattern = re.compile('|'.join(slack_api.nicksToEmoji.keys()))
          updates.append(pattern.sub(
              lambda x: slack_api.nicksToEmoji[x.group()], formatted))

    return updates


if __name__ == '__main__':
  logger = Logger()
  slackApi = SlackApi(logger)
  app = App(logger, slackApi)
