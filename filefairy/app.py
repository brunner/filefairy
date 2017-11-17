#!/usr/bin/env python

import datetime
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

    self.finalScores = []
    self.injuries = []
    self.liveTables = []
    self.lock = threading.Lock()
    self.tick = 0
    self.records = {t: [0, 0] for t in range(31, 61)}
    self.standings = self.getStandings()
    self.ws = None

  def getFileUrl(self):
    return 'https://orangeandblueleaguebaseball.com/StatsLab/exports.php'

  def getBoxScoreUrl(self, boxid):
    return 'https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_{}.html'.format(boxid)

  def getStandingsPath(self):
    return os.path.expanduser('~') + '/orangeandblueleague/filefairy/data/'

  def getStandingsInFile(self):
    return self.getStandingsPath() + 'standings.txt'

  def getStandingsOutFile(self):
    return self.getStandingsInFile()

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

  def getStandings(self):
    table = {}
    with open(self.getStandingsInFile(), 'r') as f:
      for line in f.readlines():
        if line.count(' ') == 2:
          t, w, l = line.split()
          table[int(t)] = [int(w), int(l)]

    return table

  def writeStandings(self):
    with open(self.getStandingsOutFile(), 'w') as f:
      for t in self.standings:
        w, l = self.standings[t]
        f.write('{} {} {}\n'.format(t, w, l))

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
    elif 'MAJOR LEAGUE BASEBALL Live Table' in text:
      self.handleLiveTable(text)
    elif re.findall(r'\d{2}\/\d{2}\/\d{4}', text) and 'was injured' in text:
      self.handleInjuries(text)

  def handleFinalScores(self, text):
    self.lock.acquire()
    text = re.sub(r'(MAJOR LEAGUE BASEBALL Final Scores|\*)', '', text)
    if text not in self.finalScores:
      self.finalScores.append(text)
      self.tick = int(time.time())
    self.lock.release()

  def processFinalScores(self):
    if len(self.finalScores) == len(self.liveTables):
      for finalScore, liveTable in zip(self.finalScores, self.liveTables):
        self.slackApi.chatPostMessage(
            self.getChannelLiveSimDiscussion(), finalScore)

        for t in range(31, 61):
          # Look up the city of the team.
          # For example, city could be 'Red Sox' or 'Chicago'.
          city = slack_api.teamidsToCities[t]

          w = len(re.findall(r'\|' + re.escape(city), finalScore))
          l = len(re.findall(r', ' + re.escape(city), finalScore))

          if t in [35, 36, 44, 45, 48, 49]:
            # Look up the nickname of the team.
            # For example, tnick could be 'Cubs'.
            tnick = slack_api.teamidsToNicks[t]

            # Look up the id and nickname of the team in the same city.
            # For example, u could be 36 and unick could be 'White Sox'.
            u = slack_api.teamidsToNeighbors[t]
            unick = slack_api.teamidsToNicks[u]

            # Find the number of wins for both teams in the live table.
            # For example, tw (Cubs wins) could be 4 and tu (White Sox wins) could be 2.
            tw = re.findall(re.escape(tnick) + r'\s+(\d+)', liveTable)
            uw = re.findall(re.escape(unick) + r'\s+(\d+)', liveTable)

            if tw and not uw:
              # If the other team didn't play, their wins/losses are correct.
              pass
            elif not tw and uw:
              # If the current team didn't play, their wins/losses are zero.
              # This is because the recorded wins/losses belong to the other team.
              w, l = 0, 0
            elif tw and uw and w == 0:
              # If both teams played and neither won, we have limited information.
              l = 0 if l == 3 else l / 2
            elif tw and uw and l == 0:
              # If both teams played and neither lost, we calculate using the live table.
              # The number of wins for the current team is the diff between the table and standings.
              w = int(tw[0]) - self.standings[t][0]
            elif tw and uw and w == 1 and l == 1:
              # If both teams played and one won and one lost, we calculate using the live table.
              # The number of wins for the current team is the diff between the table and standings.
              w = int(tw[0]) - self.standings[t][0]
              l = 0 if w else 1

          self.records[t][0] += w
          self.records[t][1] += l

          self.standings[t][0] += w
          self.standings[t][1] += l

      ## Save for now, this might be useful for the edge cases.
      # cities = ['Chicago', 'Los Angeles', 'New York']
      # for line in finalScore.splitlines():
      #   match = re.findall(
      #       r'game_box_(\d+)\.html\|([^\d]+)(\d+),([^\d]+)(\d+)', line)
      #   if match:
      #     boxid, wteam, wruns, lteam, lruns = match[0]
      #     wteam, lteam = wteam.strip(), lteam.strip()

      #     if wteam in cities or lteam in cities:
      #       url = self.getBoxScoreUrl(boxid)
      #       page = self.getPage(url)
      #       wmatch = re.findall(r'<b>' + re.escape(wteam) + r'([^<(]+)', page)
      #       lmatch = re.findall(r'\">' + re.escape(lteam) + r'([^<(]+)', page)
      #       if wmatch and wteam in cities:
      #         wteam = wmatch[0].strip()
      #       if lmatch and lteam in cities:
      #         lteam = lmatch[0].strip()

      #     if wteam in slack_api.nicksToTeamids:
      #       wid = slack_api.nicksToTeamids[wteam]
      #       self.records[wid][0] += 1

      #     if lteam in slack_api.nicksToTeamids:
      #       lid = slack_api.nicksToTeamids[lteam]
      #       self.records[lid][1] += 1

    self.finalScores, self.liveTables = [], []

  def handleLiveTable(self, text):
    self.lock.acquire()
    self.liveTables.append(text)
    self.tick = int(time.time())
    self.lock.release()

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
        match = re.findall(r'(\<[^\(]+)\(', chunk)
        if match:
          line = re.sub(r'was injured (?:(?:in a|on a|while) )?',
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
        self.slackApi.filesUpload(self.formatStandingsAL(), 'AL.txt', 'testing')
        self.slackApi.filesUpload(self.formatStandingsNL(), 'NL.txt', 'testing')
        self.writeStandings()
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
      pct = lambda t: (float(r[t][0]) / (sum(r[t]) or 1),
                       r[t][0],
                       float(1) / r[t][1] if r[t][1] else 2)
      ordered = sorted(group[1], key=pct, reverse=True)

      formatted = []
      for t in ordered:
        emoji = slack_api.teamidsToEmoji[t]
        formatted.append('{0} {1}'.format(
            emoji, '-'.join([str(n) for n in r[t]])))

      lines.append('{0}\n{1}'.format(
          group[0], ' :separator: '.join(formatted)))

    return '\n\n'.join(lines)

  def formatStandingsAL(self):
    groups = [
        ('AL East', [33, 34, 48, 57, 59]),
        ('AL Central', [35, 38, 40, 43, 47]),
        ('AL West', [42, 44, 50, 54, 58]),
    ]

    return self.formatStandingsInternal(groups, 'AL Wild Card')

  def formatStandingsNL(self):
    groups = [
        ('NL East', [32, 41, 49, 51, 60]),
        ('NL Central', [36, 37, 46, 52, 56]),
        ('NL West', [31, 39, 45, 53, 55]),
    ]

    return self.formatStandingsInternal(groups, 'NL Wild Card')

  def formatStandingsInternal(self, groups, wildcard):
    div = ' | '
    top = '{division:<15}{div}  W{div}  L{div}  GB{div} M#\n' + \
          '----------------|-----|-----|------|-----'
    row = '{city:<15}{div}{w:>3}{div}{l:>3}{div}{gb:>4}{div}{mn:>3}'

    s = self.standings
    pct = lambda t: (float(s[t][0]) / (sum(s[t]) or 1),
                     s[t][0],
                     float(1) / s[t][1] if s[t][1] else 2)

    lines = []
    wc = []
    for group in groups:
      lines.append(top.format(division=group[0], div=div))
      ordered = sorted(group[1], key=pct, reverse=True)

      t = ordered[0]
      wc.extend(ordered[1:])

      leaders = 1
      for u in ordered[1:]:
        if (s[t][0] - s[u][0] + s[u][1] - s[t][1]) / 2.0 == 0:
          leaders += 1
        else:
          break

      for l in ordered[:leaders]:
        city = slack_api.teamidsToCities[l]
        wa = s[l][0]
        lb = min(s[v][1] for v in ordered if l != v)
        mn = 163 - wa - lb
        lines.append(row.format(city=city, div=div, w=s[l][0], l=s[l][1], gb='-', mn=mn))
      for f in ordered[leaders:]:
        city = slack_api.teamidsToCities[f]
        gb = '{:0.1f}'.format((s[t][0] - s[f][0] + s[f][1] - s[t][1]) / 2.0)
        lines.append(row.format(city=city, div=div, w=s[f][0], l=s[f][1], gb=gb, mn=''))

      lines.append('')

    lines.append(top.format(division=wildcard, div=div))
    ordered = sorted(wc, key=pct, reverse=True)

    t = ordered[0]
    u = ordered[1]
    leaders = 2
    for v in ordered[2:]:
      if (s[u][0] - s[v][0] + s[v][1] - s[u][1]) / 2.0 == 0:
        leaders += 1
      else:
        break

    l = ordered[leaders - 1]
    for m in ordered[:leaders]:
      city = slack_api.teamidsToCities[m]
      wa = s[m][0]
      lb = min(s[v][1] for v in ordered[leaders:])
      mn = 163 - wa - lb
      gb = (s[m][0] - s[l][0] + s[l][1] - s[m][1]) / 2.0
      gb = '-' if gb == 0 else '{:+0.1f}'.format(gb)
      lines.append(row.format(city=city, div=div, w=s[m][0], l=s[m][1], gb=gb, mn=mn))
    for f in ordered[leaders:leaders + 4]:
      city = slack_api.teamidsToCities[f]
      gb = '{:0.1f}'.format((s[l][0] - s[f][0] + s[f][1] - s[l][1]) / 2.0)
      lines.append(row.format(city=city, div=div, w=s[f][0], l=s[f][1], gb=gb, mn=''))

  
    return '\n'.join(lines)


if __name__ == '__main__':
  logger = Logger()
  slackApi = SlackApi(logger)
  app = App(logger, slackApi)
  app.listen()
  app.watch()
