#!/usr/bin/env python

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
import threading
import time
import urllib2

from logger import TestLogger
from app import App
from slack_api import SlackApi, TestSlackApi
from utils import assertEquals, assertNotEquals

injury1 = '03/21/2021 RP <https://player_33610.html|Drew Pomeranz> was injured ' + \
          'while pitching (Baltimore @ Seattle)'
injury2 = '03/21/2021 LF <https://player_37732.html|Alexis Rivera> was injured ' + \
          'on a defensive play (Cleveland @ Toronto)'
injury3 = '03/21/2021 Rain delay of 16 minutes in the 7th inning. ' + \
          'SS <https://player_39374.html|Amed Rosario> was injured ' + \
          'in a collision at a base (Kansas City @ Detroit)'
injury4 = '03/21/2021 SS <https://player_39374.html|Amed Rosario> was injured ' + \
          'during a surprise event (Kansas City @ Detroit)'
finalScores = '03/21/2021 MAJOR LEAGUE BASEBALL Final Scores\n' + \
              '*<https://game_box_24216.html|Atlanta 7, Colorado 6>*\n' + \
              '*<https://game_box_24018.html|Cleveland 5, Toronto 1>*\n' + \
              '*<https://game_box_24015.html|Houston 5, Tampa Bay 3>*\n' + \
              '*<https://game_box_24014.html|Kansas City 7, Detroit 2>*\n' + \
              '*<https://game_box_24212.html|Los Angeles 3, Cincinnati 2>*\n' + \
              '*<https://game_box_24013.html|Los Angeles 7, New York 6>*\n' + \
              '*<https://game_box_24214.html|Miami 4, Pittsburgh 1>*\n' + \
              '*<https://game_box_24215.html|Milwaukee 9, Washington 8>*\n' + \
              '*<https://game_box_24218.html|New York 6, San Diego 1>*\n' + \
              '*<https://game_box_24017.html|Oakland 5, Minnesota 2>*\n' + \
              '*<https://game_box_24213.html|Philadelphia 4, San Francisco 2>*\n' + \
              '*<https://game_box_24016.html|Seattle 3, Baltimore 2>*\n' + \
              '*<https://game_box_24217.html|St. Louis 2, Chicago 0>*\n' + \
              '*<https://game_box_24019.html|Texas 8, Chicago 2>*'

liveTable = '```MAJOR LEAGUE BASEBALL Live Table - 03/21/2021\n' + \
            'Cincinnati Reds                48\n' + \
            'Colorado Rockies               43\n' + \
            'Los Angeles Dodgers            43\n' + \
            'San Diego Padres               42\n' + \
            'Minnesota Twins                41\n' + \
            'St. Louis Cardinals            41\n' + \
            'Atlanta Braves                 40\n' + \
            'Kansas City Royals             40\n' + \
            'Seattle Mariners               40\n' + \
            'Toronto Blue Jays              40\n' + \
            'New York Mets                  38\n' + \
            'Philadelphia Phillies          38\n' + \
            'Baltimore Orioles              37\n' + \
            'Boston Red Sox                 36\n' + \
            'Tampa Bay Rays                 36\n' + \
            'Chicago Cubs                   35\n' + \
            'Cleveland Indians              34\n' + \
            'Detroit Tigers                 34\n' + \
            'New York Yankees               34\n' + \
            'Chicago White Sox              33\n' + \
            'Milwaukee Brewers              33\n' + \
            'Houston Astros                 31\n' + \
            'Los Angeles Angels             31\n' + \
            'Washington Nationals           31\n' + \
            'Oakland Athletics              30\n' + \
            'San Francisco Giants           30\n' + \
            'Arizona Diamondbacks           25\n' + \
            'Miami Marlins                  25\n' + \
            'Texas Rangers                  25\n' + \
            'Pittsburgh Pirates             21````'


class AppTest(App):
  '''Tests for App.'''

  def __init__(self, logger, slackApi, fileUrls, standingsInFile, integration=False):
    self.logger = logger
    self.slackApi = slackApi

    self.fileUrls, self.fileIndex = fileUrls, 0
    self.filePage = self.getPage(self.fileUrls[0])
    self.fileDate = self.findFileDate(self.filePage)

    self.standingsInFile = standingsInFile

    self.finalScores = []
    self.injuries = []
    self.liveTables = []
    self.lock = threading.Lock()
    self.tick = 0
    self.records = {t: [0, 0] for t in range(31, 61)}
    self.standings = self.getStandings()
    self.ws = None
    self.integration = integration

  def getFileUrl(self):
    if len(self.fileUrls) > self.fileIndex + 1:
      self.fileIndex = self.fileIndex + 1

    if self.integration and self.fileIndex == 1:
      self.chatInjuryTest()
      self.chatFinalScoresTest()
      self.chatFinalScoresTest()
      self.chatLiveTableTest()

    return self.fileUrls[self.fileIndex]

  def getBoxScoreUrl(self, boxid):
    return 'game_box_{}.html'.format(boxid)

  def getStandingsPath(self):
    return os.path.expanduser('~') + '/orangeandblueleague/filefairy/testing/'

  def getStandingsGoldFile(self):
    return self.getStandingsPath() + 'standingsgold.txt'

  def getStandingsInFile(self):
    return self.getStandingsPath() + self.standingsInFile

  def getStandingsOutFile(self):
    return self.getStandingsPath() + 'standingsout.txt'

  def getChannelGeneral(self):
    return 'testing'

  def getChannelLiveSimDiscussion(self):
    return 'testing'

  def getChannelStatsplus(self):
    return 'testing'

  def getTimerValues(self):
    return [1, 2, 10]

  def getPage(self, url):
    path = os.path.expanduser("~") + "/orangeandblueleague/filefairy/testing/"
    cwd = os.getcwd()
    os.chdir(path)

    if url.startswith('https://'):
      url = url.substring(8)

    page = ''
    with open(url, 'r') as f:
      page = f.read()

    os.chdir(cwd)
    return page

  def chatInjuryTest(self):
    self.slackApi.chatPostMessage('testing', injury1)
    self.slackApi.chatPostMessage('testing', injury2)
    self.slackApi.chatPostMessage('testing', injury3)
    self.slackApi.chatPostMessage('testing', injury4)

  def chatFinalScoresTest(self):
    self.slackApi.chatPostMessage('testing', finalScores)

  def chatLiveTableTest(self):
    self.slackApi.chatPostMessage('testing', liveTable)

  def getListen(self):
    t1 = threading.Thread(target=self.listen)
    t1.start()
    time.sleep(6)

    self.chatInjuryTest()
    self.chatFinalScoresTest()
    self.chatLiveTableTest()

    self.handleClose()
    time.sleep(1)
    t1.join()

    self.logger.collect()
    return {
        'collected': self.logger.collected
    }

  def getWatch(self):
    self.watch()
    self.logger.collect()
    return {
        'collected': self.logger.collected,
    }

  def getIntegration(self):
    t1 = threading.Thread(target=self.listen)
    t1.start()
    time.sleep(6)

    t2 = threading.Thread(target=self.watch)
    t2.start()

    t1.join()
    t2.join()

    self.logger.collect()
    return {
        'collected': self.logger.collected
    }

  def getUpdateLeagueFile(self):
    ret = self.updateLeagueFile()
    self.logger.collect()
    return {
        'ret': ret,
        'collected': self.logger.collected,
        'index': self.fileIndex,
        'date': self.fileDate,
    }

fileUrls = [
    'export_01142017_1.html',         # 0. Initial exports page.
    'export_01142017_2.html',         # 1. League file date has not changed.
    'export_01142017_2.html',         # 2. League file date has not changed.
    'export_01142017_2.html',         # 3. League file date has not changed.
    'export_01172017_1.html',         # 3. League file date has changed.
]

fileDates = {
    'old': 'Saturday January 14, 2017 13:01:09 EST',
    'new': 'Tuesday January 17, 2017 09:03:12 EST',
}

records = {
    31: [0, 0], 32: [1, 0], 33: [0, 1], 34: [0, 0], 35: [0, 1],
    36: [0, 1], 37: [0, 1], 38: [1, 0], 39: [0, 1], 40: [0, 1],
    41: [1, 0], 42: [1, 0], 43: [1, 0], 44: [1, 0], 45: [1, 0],
    46: [1, 0], 47: [0, 1], 48: [0, 1], 49: [1, 0], 50: [1, 0],
    51: [1, 0], 52: [0, 1], 53: [0, 1], 54: [1, 0], 55: [0, 1],
    56: [1, 0], 57: [0, 1], 58: [1, 0], 59: [0, 1], 60: [0, 1]
}

standings = {
    31: {'l': 44, 'w': 25}, 32: {'l': 30, 'w': 40}, 33: {'l': 35, 'w': 37},
    34: {'l': 33, 'w': 36}, 35: {'l': 38, 'w': 33}, 36: {'l': 36, 'w': 35},
    37: {'l': 21, 'w': 48}, 38: {'l': 36, 'w': 34}, 39: {'l': 26, 'w': 43},
    40: {'l': 36, 'w': 34}, 41: {'l': 45, 'w': 25}, 42: {'l': 39, 'w': 31},
    43: {'l': 33, 'w': 40}, 44: {'l': 39, 'w': 31}, 45: {'l': 26, 'w': 43},
    46: {'l': 38, 'w': 33}, 47: {'l': 30, 'w': 41}, 48: {'l': 37, 'w': 34},
    49: {'l': 33, 'w': 38}, 50: {'l': 40, 'w': 30}, 51: {'l': 32, 'w': 38},
    52: {'l': 50, 'w': 21}, 53: {'l': 29, 'w': 42}, 54: {'l': 28, 'w': 40},
    55: {'l': 41, 'w': 30}, 56: {'l': 28, 'w': 41}, 57: {'l': 35, 'w': 36},
    58: {'l': 46, 'w': 25}, 59: {'l': 29, 'w': 40}, 60: {'l': 40, 'w': 31},
}

formatRecords = 'AL East\n:redsox: 0-0 :separator: :orioles: 0-1 :separator: :yankees: 0-1 ' + \
                ':separator: :rays: 0-1 :separator: :jays: 0-1\n\n' + \
                'AL Central\n:indians: 1-0 :separator: :monarchs: 1-0 :separator: ' + \
                ':whitesox: 0-1 :separator: :crackeyes: 0-1 :separator: :twincities: 0-1\n\n' + \
                'AL West\n:stros: 1-0 :separator: :angels: 1-0 :separator: :athletics: 1-0 ' + \
                ':separator: :mariners: 1-0 :separator: :rangers: 1-0\n\n' + \
                'NL East\n:braves: 1-0 :separator: :marlins: 1-0 :separator: :mets: 1-0 ' + \
                ':separator: :phillies: 1-0 :separator: :nationals: 0-1\n\n' + \
                'NL Central\n:brewers: 1-0 :separator: :cardinals: 1-0 :separator: ' + \
                ':cubbies: 0-1 :separator: :reds: 0-1 :separator: :pirates: 0-1\n\n' + \
                'NL West\n:dodgers: 1-0 :separator: :dbacks: 0-0 :separator: :rox: 0-1 ' + \
                ':separator: :pads: 0-1 :separator: :giants: 0-1'

formatStandingsA = 'AL East         |   W |   L |    GB |  M#\n' + \
                   '----------------|-----|-----|-------|-----\n' + \
                   'Toronto         |  40 |  29 |     - |  90\n' + \
                   'Boston          |  36 |  33 |   4.0 |    \n' + \
                   'Baltimore       |  37 |  35 |   4.5 |    \n' + \
                   'Tampa Bay       |  36 |  35 |   5.0 |    \n' + \
                   'New York        |  34 |  37 |   7.0 |    \n\n' + \
                   'AL Central      |   W |   L |    GB |  M#\n' + \
                   '----------------|-----|-----|-------|-----\n' + \
                   'Minnesota       |  41 |  30 |     - |  89\n' + \
                   'Kansas City     |  40 |  33 |   2.0 |    \n' + \
                   'Cleveland       |  34 |  36 |   6.5 |    \n' + \
                   'Detroit         |  34 |  36 |   6.5 |    \n' + \
                   'Chicago         |  33 |  38 |   8.0 |    \n\n' + \
                   'AL West         |   W |   L |    GB |  M#\n' + \
                   '----------------|-----|-----|-------|-----\n' + \
                   'Seattle         |  40 |  28 |     - |  84\n' + \
                   'Houston         |  31 |  39 |  10.0 |    \n' + \
                   'Los Angeles     |  31 |  39 |  10.0 |    \n' + \
                   'Oakland         |  30 |  40 |  11.0 |    \n' + \
                   'Texas           |  25 |  46 |  16.5 |    \n\n' + \
                   'AL Wild Card    |   W |   L |    GB |  M#\n' + \
                   '----------------|-----|-----|-------|-----\n' + \
                   'Kansas City     |  40 |  33 |  +2.0 |  88\n' + \
                   'Boston          |  36 |  33 |     - |  92\n' + \
                   'Baltimore       |  37 |  35 |   0.5 |    \n' + \
                   'Tampa Bay       |  36 |  35 |   1.0 |    \n' + \
                   'Cleveland       |  34 |  36 |   2.5 |    \n' + \
                   'Detroit         |  34 |  36 |   2.5 |    \n' + \
                   'New York        |  34 |  37 |   3.0 |    \n' + \
                   'Chicago         |  33 |  38 |   4.0 |    \n' + \
                   'Houston         |  31 |  39 |   5.5 |    \n' + \
                   'Los Angeles     |  31 |  39 |   5.5 |    \n' + \
                   'Oakland         |  30 |  40 |   6.5 |    \n' + \
                   'Texas           |  25 |  46 |  12.0 |    '

formatStandingsN = 'NL East         |   W |   L |    GB |  M#\n' + \
                   '----------------|-----|-----|-------|-----\n' + \
                   'Atlanta         |  40 |  30 |     - |  91\n' + \
                   'Philadelphia    |  38 |  32 |   2.0 |    \n' + \
                   'New York        |  38 |  33 |   2.5 |    \n' + \
                   'Washington      |  31 |  40 |   9.5 |    \n' + \
                   'Miami           |  25 |  45 |  15.0 |    \n\n' + \
                   'NL Central      |   W |   L |    GB |  M#\n' + \
                   '----------------|-----|-----|-------|-----\n' + \
                   'Cincinnati      |  48 |  21 |     - |  87\n' + \
                   'St. Louis       |  41 |  28 |   7.0 |    \n' + \
                   'Chicago         |  35 |  36 |  14.0 |    \n' + \
                   'Milwaukee       |  33 |  38 |  16.0 |    \n' + \
                   'Pittsburgh      |  21 |  50 |  28.0 |    \n\n' + \
                   'NL West         |   W |   L |    GB |  M#\n' + \
                   '----------------|-----|-----|-------|-----\n' + \
                   'Colorado        |  43 |  26 |     - |  94\n' + \
                   'Los Angeles     |  43 |  26 |     - |  94\n' + \
                   'San Diego       |  42 |  29 |   2.0 |    \n' + \
                   'San Francisco   |  30 |  41 |  14.0 |    \n' + \
                   'Arizona         |  25 |  44 |  18.0 |    \n\n' + \
                   'NL Wild Card    |   W |   L |    GB |  M#\n' + \
                   '----------------|-----|-----|-------|-----\n' + \
                   'Colorado        |  43 |  26 |  +2.0 |  91\n' + \
                   'Los Angeles     |  43 |  26 |  +2.0 |  91\n' + \
                   'St. Louis       |  41 |  28 |     - |  93\n' + \
                   'San Diego       |  42 |  29 |     - |  93\n' + \
                   'Philadelphia    |  38 |  32 |   3.5 |    \n' + \
                   'New York        |  38 |  33 |   4.0 |    \n' + \
                   'Chicago         |  35 |  36 |   7.0 |    \n' + \
                   'Milwaukee       |  33 |  38 |   9.0 |    \n' + \
                   'Washington      |  31 |  40 |  11.0 |    \n' + \
                   'San Francisco   |  30 |  41 |  12.0 |    \n' + \
                   'Arizona         |  25 |  44 |  16.0 |    \n' + \
                   'Miami           |  25 |  45 |  16.5 |    \n' + \
                   'Pittsburgh      |  21 |  50 |  21.0 |    '

logs = [
    'Started listening.',             # 0
    'Test mocked chat.postMessage.',  # 1
    'Started watching.',              # 2
    'Test mocked chat.postMessage.',  # 3
    'Test mocked chat.postMessage.',  # 4
    'File is up.',                    # 5
    'Test mocked chat.postMessage.',  # 6
    'Done watching.',                 # 7
    'Done listening.',                # 8
]


def testReal():
  fileUrl = 'http://orangeandblueleaguebaseball.com/StatsLab/exports.php'
  filePage = urllib2.urlopen(fileUrl).read()

  logger = TestLogger()
  slackApi = TestSlackApi(logger)
  appTest = AppTest(logger, slackApi, fileUrls[:], 'standingsin.txt')

  assertNotEquals(appTest.findFileDate(filePage), '')


def testFindFileDate():
  logger = TestLogger()
  slackApi = TestSlackApi(logger)
  appTest = AppTest(logger, slackApi, fileUrls[:], 'standingsin.txt')

  page = appTest.getPage(fileUrls[0])
  assertEquals(appTest.findFileDate(page), fileDates['old'])

  page = appTest.getPage(fileUrls[1])
  assertEquals(appTest.findFileDate(page), fileDates['old'])

  page = appTest.getPage(fileUrls[2])
  assertEquals(appTest.findFileDate(page), fileDates['old'])

  page = appTest.getPage(fileUrls[3])
  assertEquals(appTest.findFileDate(page), fileDates['old'])

  page = appTest.getPage(fileUrls[4])
  assertEquals(appTest.findFileDate(page), fileDates['new'])


def testUpdateLeagueFile():
  logger = TestLogger()
  slackApi = TestSlackApi(logger)
  appTest = AppTest(logger, slackApi, fileUrls[:], 'standingsin.txt')

  expected = {'ret': False, 'collected': [], 'index': 1,
              'date': fileDates['old']}
  assertEquals(appTest.getUpdateLeagueFile(), expected)

  expected = {'ret': False, 'collected': [], 'index': 2,
              'date': fileDates['old']}
  assertEquals(appTest.getUpdateLeagueFile(), expected)

  expected = {'ret': False, 'collected': [], 'index': 3,
              'date': fileDates['old']}
  assertEquals(appTest.getUpdateLeagueFile(), expected)

  expected = {'ret': True, 'collected': logs[4:6], 'index': 4,
              'date': fileDates['new']}
  assertEquals(appTest.getUpdateLeagueFile(), expected)

  expected = {'ret': False, 'collected': logs[4:6], 'index': 4,
              'date': fileDates['new']}
  assertEquals(appTest.getUpdateLeagueFile(), expected)


def testWatch():
  logger = TestLogger()
  slackApi = TestSlackApi(logger)
  appTest = AppTest(logger, slackApi, fileUrls[:], 'standingsin.txt')

  expected = {'collected': logs[1:4] + logs[5:8]}
  assertEquals(appTest.getWatch(), expected)


def testFinalScores():
  logger = TestLogger()
  slackApi = TestSlackApi(logger)
  appTest = AppTest(logger, slackApi, fileUrls[:], 'standingsin.txt')

  appTest.handleFinalScores(finalScores)
  appTest.handleLiveTable(liveTable)
  appTest.processFinalScores()
  assertEquals(appTest.records, records)
  assertEquals(appTest.standings, standings)
  assertEquals(appTest.formatRecords(), formatRecords)
  assertEquals(appTest.formatStandingsAL(), formatStandingsA)
  assertEquals(appTest.formatStandingsNL(), formatStandingsN)


def testStandings():
  logger = TestLogger()
  slackApi = TestSlackApi(logger)

  appTest = AppTest(logger, slackApi, fileUrls[:], 'standings_openingday.txt')
  print appTest.formatStandingsAL()
  print appTest.formatStandingsNL()
  print '\n--------------------\n'

  appTest = AppTest(logger, slackApi, fileUrls[:], 'standings_linear.txt')
  print appTest.formatStandingsAL()
  print appTest.formatStandingsNL()
  print '\n--------------------\n'

  appTest = AppTest(logger, slackApi, fileUrls[:], 'standings_final.txt')
  print appTest.formatStandingsAL()
  print appTest.formatStandingsNL()
  print '\n--------------------\n'

  appTest = AppTest(logger, slackApi, fileUrls[:], 'standings_baddivision.txt')
  print appTest.formatStandingsAL()
  print appTest.formatStandingsNL()
  print '\n--------------------\n'

  appTest = AppTest(logger, slackApi, fileUrls[:], 'standings_today.txt')
  print appTest.formatStandingsAL()
  print appTest.formatStandingsNL()


def testListen():
  logger = TestLogger()
  slackApi = SlackApi(logger)
  appTest = AppTest(logger, slackApi, fileUrls[:], 'standingsin.txt')

  expected = {'collected': logs[:1] + logs[8:]}
  assertEquals(appTest.getListen(), expected)


def testIntegration():
  logger = TestLogger()
  slackApi = SlackApi(logger)
  appTest = AppTest(logger, slackApi, fileUrls[:], 'standingsin.txt', True)

  with open(appTest.getStandingsOutFile(), 'w') as f:
    pass

  expected = {'collected': logs[:1] + logs[2:3] + logs[5:6] + logs[7:9]}
  assertEquals(appTest.getIntegration(), expected)

  out, gold = '', ''
  with open(appTest.getStandingsOutFile(), 'r') as f:
    out = f.read()
  with open(appTest.getStandingsGoldFile(), 'r') as f:
    gold = f.read()
  assertEquals(out, gold)


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--mode', dest='mode', default='all')
  args = parser.parse_args()

  if args.mode == 'real' or args.mode == 'all':
    testReal()

  if args.mode == 'filedate' or args.mode == 'all':
    testFindFileDate()

  if args.mode == 'leaguefile' or args.mode == 'all':
    testUpdateLeagueFile()

  if args.mode == 'watch' or args.mode == 'all':
    testWatch()

  if args.mode == 'finalscores' or args.mode == 'all':
    testFinalScores()

  # if args.mode == 'standings' or args.mode == 'all':
  #   testStandings()

  if args.mode == 'listen' or args.mode == 'all':
    testListen()

  if args.mode == 'integration' or args.mode == 'all':
    testIntegration()

  print 'Passed.'
