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


import logging
logging.basicConfig()


class App(object):

  def __init__(self, logger, slackApi, app=None):
    self.logger = logger
    self.slackApi = slackApi

    page = self.getPage(self.getFileUrl())
    self.fileDate = self.findFileDate(page)

    self.finalScores = []
    self.injuries = []
    self.lock = threading.Lock()
    self.tick = 0
    self.records = {t: [0, 0, 0] for t in range(31, 61)}
    self.ws = None

  def getFileUrl(self):
    return 'https://orangeandblueleaguebaseball.com/StatsLab/exports.php'

  def getBoxScoreUrl(self, boxid):
    return 'https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_{}.html'.format(boxid)

  def getChannelGeneral(self):
    return 'general'

  def getChannelLiveSimDiscussion(self):
    return 'live-sim-discussion'

  def getChannelStatsplus(self):
    return 'statsplus'

  def getTimerValues(self):
    return [
        30,     # Sleep between consecutive file page checks.
        120,    # Pause and post records/injuries.
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

      t = threading.Thread(target=self.ws.run_forever)
      t.daemon = True
      t.start()

  def handleStatsplus(self, text):
    if 'MAJOR LEAGUE BASEBALL Final Scores' in text:
      self.handleFinalScores(text)
    elif re.findall(r'\d{2}\/\d{2}\/\d{4}', text) and 'was injured' in text:
      self.handleInjuries(text)

  def handleFinalScores(self, text):
    self.lock.acquire()
    text = text.replace('MAJOR LEAGUE BASEBALL Final Scores', '')
    if text not in self.finalScores:
      self.finalScores.append(text)
      self.tick = int(time.time())
    self.lock.release()

  def processFinalScores(self):
    for finalScore in self.finalScores:
      self.slackApi.chatPostMessage(
          self.getChannelLiveSimDiscussion(), finalScore)

      cities = ['Chicago', 'Los Angeles', 'New York']
      for line in finalScore.splitlines():
        match = re.findall(
            r'game_box_(\d+)\.html\|([^\d]+)(\d+),([^\d]+)(\d+)', line)
        if match:
          boxid, wteam, wruns, lteam, lruns = match[0]
          wteam, lteam = wteam.strip(), lteam.strip()

          if wteam in cities or lteam in cities:
            url = self.getBoxScoreUrl(boxid)
            page = self.getPage(url)
            score = r'([^<]+)</(?:.*?)<b>(\d+)</b>'
            wmatch = re.findall(r'<b>' + re.escape(wteam) + r'([^<(]+)', page)
            lmatch = re.findall(r'\">' + re.escape(lteam) + r'([^<(]+)', page)
            if wmatch and wteam in cities:
              wteam = wmatch[0].strip()
            if lmatch and lteam in cities:
              lteam = lmatch[0].strip()

          if wteam in slack_api.nicksToTeamids:
            wid = slack_api.nicksToTeamids[wteam]
            self.records[wid][0] += 1

          if lteam in slack_api.nicksToTeamids:
            lid = slack_api.nicksToTeamids[lteam]
            self.records[lid][1] += 1

    self.finalScores = []

  def handleInjuries(self, text):
    self.lock.acquire()
    if text not in self.injuries:
      self.injuries.append(text)
      self.tick = int(time.time())
    self.lock.release()

  def processInjuries(self):
    lines = ['Injuries']
    for injury in self.injuries:
      for chunk in injury.split('. '):
        print 'chunk: ' + chunk
        match = re.findall(r'(\<[^\(]+)\(', chunk)
        if match:
          print 'match: ' + match[0]
          line = re.sub('was injured (?:(?:in a|on a|while) )?',
                        '(', match[0].strip())
          if not line == match[0]:
            line += ')'
          lines.append(line)

    self.slackApi.chatPostMessage(
        self.getChannelLiveSimDiscussion(), '\n'.join(lines))
    self.injuries = []

  def handleClose(self):
    if self.ws:
      self.ws.close()
      self.slackApi.chatPostMessage('testing', 'Done listening.')
      self.logger.log('Done listening.')

  def watch(self):
    sleep, records, timeout = self.getTimerValues()
    elapsed = 0

    self.slackApi.chatPostMessage('testing', 'Started watching.')
    self.logger.log('Started watching.')

    while elapsed < timeout:
      time.sleep(sleep)
      elapsed = elapsed + sleep

      if self.updateLeagueFile():
        elapsed = timeout

      self.lock.acquire()
      if self.finalScores and int(time.time()) - self.tick > records:
        self.processFinalScores()
        self.processInjuries()
        self.slackApi.chatPostMessage(
            self.getChannelLiveSimDiscussion(), self.formatRecords())
      self.lock.release()

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

  def findFileDate(self, page):
    match = re.findall(r'League File Updated: ([^<]+)<', page)
    return match[0] if len(match) else ''

  def formatRecords(self):
    groups = [
        ('AL East', [33, 34, 48, 57, 59]),
        ('AL Central', [35, 38, 40, 43, 47]),
        ('AL West', [42, 44, 50, 54, 58]),
        ('NL East', [32, 41, 49, 51, 60]),
        ('NL Central', [36, 37, 46, 52, 56]),
        ('NL West', [31, 39, 45, 53, 55]),
    ]

    lines = []
    for group in groups:
      r = self.records
      pct = lambda x: (float(r[x][0] + 0.5 * r[x][2]) / (sum(r[x]) or 1),
                       r[x][0],
                       float(1) / r[x][1] if r[x][1] else 2,
                       r[x][2])
      ordered = sorted(group[1], key=pct, reverse=True)

      formatted = []
      for t in ordered:
        emoji = slack_api.teamidsToEmoji[t]
        record = r[t] if r[t][2] else r[t][:2]
        formatted.append('{0} {1}'.format(
            emoji, '-'.join([str(n) for n in record])))

      lines.append('{0}\n{1}'.format(
          group[0], ' :separator: '.join(formatted)))

    return '\n\n'.join(lines)


if __name__ == '__main__':
  logger = Logger()
  slackApi = SlackApi(logger)
  app = App(logger, slackApi)
  app.listen()
  app.watch()
