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
    standings = {}
    with open(self.getStandingsInFile(), 'r') as f:
      for line in f.readlines():
        if line.count(' ') == 2:
          t, w, l = line.split()
          standings[int(t)] = {'w': int(w), 'l': int(l)}

    return standings

  def writeStandings(self):
    with open(self.getStandingsOutFile(), 'w') as f:
      for t in self.standings:
        w, l = self.standings[t]['w'], self.standings[t]['l']
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
              w = int(tw[0]) - self.standings[t]['w']
            elif tw and uw and w == 1 and l == 1:
              # If both teams played and one won and one lost, we calculate using the live table.
              # The number of wins for the current team is the diff between the table and standings.
              w = int(tw[0]) - self.standings[t]['w']
              l = 0 if w else 1

          self.records[t][0] += w
          self.records[t][1] += l

          self.standings[t]['w'] += w
          self.standings[t]['l'] += l

      # Save for now, this might be useful for the edge cases.
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

  def getStandingsKeys(self, k):
    return [k + ey for ey in ['gb', 'en', 'mn']]

  def getGamesBehind(self, s, u, t0):
    return (s[t0]['w'] - s[u]['w'] + s[u]['l'] - s[t0]['l']) / 2.0

  def getEliminationNumber(self, s, u, t):
    return max(163 - s[t]['w'] - s[u]['l'], 0)

  def getOrdered(self, s, group):
    pct = lambda t: (float(s[t]['w']) / ((s[t]['w'] + s[t]['l']) or 1),
                     s[t]['w'],
                     float(1) / s[t]['l'] if s[t]['l'] else 2,
                     float(1) / t)
    return sorted(group, key=pct, reverse=True)

  def processEliminationNumbers(self, s, ordered, i, k):
    kgb, ken, kmn = self.getStandingsKeys(k)
    ts = filter(lambda v: s[v][kgb] <= 0, ordered)
    if len(ts) == len(ordered):
      for t in ordered:
        u0 = sorted(filter(lambda v: v != t, ts), key=lambda v: s[v]['l'], reverse=True)[0]
        en = self.getEliminationNumber(s, u0, t)
        if kmn not in s[t] or en > s[t][kmn]:
          s[t][kmn] = en
    else:
      for t in ts:
        for u in ordered:
          if u == t or (u not in ts and 'dgb0' in s[u]):
            continue
          en = self.getEliminationNumber(s, u, t)
          s[u].setdefault(ken, []).append(en)
          s[t].setdefault(kmn, []).append(en)
      for v in ordered:
        if kmn in s[v]:
          s[v][kmn] = sorted(s[v][kmn], reverse=True)[i]
        elif ken in s[v]:
          s[v][ken] = sorted(s[v][ken])[i]
        if kmn in s[v] and ken in s[v]:
          del s[v][ken]

  def getStandingsOutput(self, s, kgroup, group, k):
    kgb, ken, kmn = self.getStandingsKeys(k)
    div = ' | '
    top = '{title:<15}{div}  W{div}  L{div}   GB{div} M#\n' + \
          '----------------|-----|-----|-------|-----'
    row = '{city:<15}{div}{w:>3}{div}{l:>3}{div}{gb:>5}{div}{mn:>3}'

    lines = [top.format(title=kgroup, div=div)]
    for v in self.getOrdered(s, group):
      city = slack_api.teamidsToCities[v]
      if 'p' in s[v]:
        city = s[v]['p'] + city
      w, l, dgb = s[v]['w'], s[v]['l'], s[v][kgb]
      gb = '{:0.1f}'.format(dgb) if dgb > 0 else '+{:0.1f}'.format(abs(dgb)) if dgb < 0 else '-'
      mn = '' if kmn not in s[v] else s[v][kmn] if s[v][kmn] > 0 else 'X'
      en = '' if ken not in s[v] else s[v][ken]
      lines.append(row.format(city=city, div=div, w=w, l=l, gb=gb, mn=mn))

    return '\n'.join(lines)

  def formatStandingsInternal(self, east, cent, west, k):
    s = self.standings.copy()
    keast, kcent, kwest, kwc = [k + ' ' + ey for ey in ['East', 'Central', 'West', 'Wild Card']]

    for group in [east, cent, west]:
      ordered = self.getOrdered(s, group)
      t0, s[t0]['dgb'], s[t0]['dgb0'] = ordered[0], 0.0, 1

      for u in ordered[1:]:
        gb = self.getGamesBehind(s, u, t0)
        s[u]['dgb'] = gb
        if gb == 0.0 and 'dgb0' in s[t0]:
          del s[t0]['dgb0']

      self.processEliminationNumbers(s, ordered, 0, 'd')

    lg = east + cent + west
    wc = filter(lambda v: 'dgb0' not in s[v], lg)
    ordered = self.getOrdered(s, lg)

    k, j = 0, 2
    for i, t0 in enumerate(ordered):
      if 'dgb0' not in s[t0]:
        k += 1
        if s[t0]['dgb'] == 0:
          j = 3
      if k == j:
        break

    s[t0]['wgb'] = 0.0
    for v in ordered:
      s[v]['wgb'] = self.getGamesBehind(s, v, t0)

    self.processEliminationNumbers(s, ordered, i, 'w')

    for v in ordered:
      if s[v].get('den', 1) == 0 and s[v].get('wen', 1) == 0:
        s[v]['p'] = 'e-'
      if s[v].get('dmn', 1) == 0:
        s[v]['p'] = 'x-'
      elif s[v].get('wmn', 1) == 0:
        s[v]['p'] = 'y-' if 'dgb0' in s[v] else 'z-'

    groups = zip([keast, kcent, kwest, kwc], [east, cent, west, wc], ['d', 'd', 'd', 'w'])
    ret = [self.getStandingsOutput(s, kgroup, group, k) for (kgroup, group, k) in groups]
    return '\n\n'.join(ret)

  def formatStandingsAL(self):
    aleast, alcent, alwest = [33, 34, 48, 57, 59], [35, 38, 40, 43, 47], [42, 44, 50, 54, 58]
    return self.formatStandingsInternal(aleast, alcent, alwest, 'AL')

  def formatStandingsNL(self):
    nleast, nlcent, nlwest = [32, 41, 49, 51, 60], [36, 37, 46, 52, 56], [31, 39, 45, 53, 55]
    return self.formatStandingsInternal(nleast, nlcent, nlwest, 'NL')


if __name__ == '__main__':
  logger = Logger()
  slackApi = SlackApi(logger)
  app = App(logger, slackApi)
  app.listen()
  app.watch()
