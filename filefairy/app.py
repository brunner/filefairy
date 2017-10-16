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
    return 'https://orangeandblueleaguebaseball.com/StatsLab/exports.php'

  def getSimUrl(self):
    return 'https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/real_time_sim/index.html'

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

    cities = ['Chicago', 'Los Angeles', 'New York']
    for line in text.splitlines():
      match = re.findall(
          r'game_box_(\d+)\.html\|([^\d]+)(\d+),([^\d]+)(\d+)', line)
      if match:
        boxid, wteam, wruns, lteam, lruns = match[0]
        wteam, lteam = wteam.strip(), lteam.strip()

        if wteam in cities or lteam in cities:
          url = self.getBoxScoreUrl(boxid)
          page = self.getPage(url)
          score = r'([^<]+)</(?:.*?)<b>(\d+)</b>'
          wmatch = re.findall(r'<b>' + re.escape(wteam) + r'([^<]+)</b>', page)
          lmatch = re.findall(r'\">' + re.escape(lteam) + r'([^<]+)</td>', page)
          if wmatch and wteam in cities:
            wteam = wmatch[0].strip()
          if lmatch and lteam in cities:
            lteam = lmatch[0].strip()

        if wteam in slack_api.nicksToTeamids and lteam in slack_api.nicksToTeamids:
          wid = slack_api.nicksToTeamids[wteam]
          lid = slack_api.nicksToTeamids[lteam]
          self.records[wid][0] += 1
          self.records[lid][1] += 1

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

          pattern = re.compile('|'.join(slack_api.abbsToEmoji.keys()))
          updates.append(pattern.sub(
              lambda x: slack_api.abbsToEmoji[x.group()], formatted))

    return updates

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
