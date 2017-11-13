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

injury = '03/21/2021 RP Drew Pomeranz was injured while pitching (Baltimore @ Seattle)'
finalScores = '03/21/2021 MAJOR LEAGUE BASEBALL Final Scores\n' + \
              '<game_box_24216.html|Atlanta 7, Colorado 6>\n' + \
              '<game_box_24018.html|Cleveland 5, Toronto 1>\n' + \
              '<game_box_24015.html|Houston 5, Tampa Bay 3>\n' + \
              '<game_box_24014.html|Kansas City 7, Detroit 2>\n' + \
              '<game_box_24212.html|Los Angeles 3, Cincinnati 2>\n' + \
              '<game_box_24013.html|Los Angeles 7, New York 6>\n' + \
              '<game_box_24214.html|Miami 4, Pittsburgh 1>\n' + \
              '<game_box_24215.html|Milwaukee 9, Washington 8>\n' + \
              '<game_box_24218.html|New York 6, San Diego 1>\n' + \
              '<game_box_24017.html|Oakland 5, Minnesota 2>\n' + \
              '<game_box_24213.html|Philadelphia 4, San Francisco 2>\n' + \
              '<game_box_24016.html|Seattle 3, Baltimore 2>\n' + \
              '<game_box_24217.html|St. Louis 2, Chicago 0>\n' + \
              '<game_box_24019.html|Texas 8, Chicago 2>'


class AppTest(App):
  '''Tests for App.'''

  def __init__(self, logger, slackApi, fileUrls, integration=False):
    self.logger = logger
    self.slackApi = slackApi

    self.fileUrls, self.fileIndex = fileUrls, 0
    self.filePage = self.getPage(self.fileUrls[0])
    self.fileDate = self.findFileDate(self.filePage)

    self.finalScores = []
    self.finalScoresLock = threading.Lock()
    self.lastFinalScoreTime = 0
    self.records = {t: [0, 0, 0] for t in range(31, 61)}
    self.ws = None
    self.integration = integration

  def getFileUrl(self):
    if len(self.fileUrls) > self.fileIndex + 1:
      self.fileIndex = self.fileIndex + 1

    if self.integration and self.fileIndex == 1:
      self.slackApi.chatPostMessage('testing', injury)
    elif self.integration and self.fileIndex == 2:
      self.slackApi.chatPostMessage('testing', finalScores)
    elif self.integration and self.fileIndex == 3:
      self.slackApi.chatPostMessage('testing', finalScores)

    return self.fileUrls[self.fileIndex]

  def getBoxScoreUrl(self, boxid):
    return 'game_box_{}.html'.format(boxid)

  def getChannelGeneral(self):
    return 'testing'

  def getChannelLiveSimDiscussion(self):
    return 'testing'

  def getChannelStatsplus(self):
    return 'testing'

  def getTimerValues(self):
    return [1, 2, 3, 8]

  def getPage(self, url):
    path = os.path.expanduser("~") + "/orangeandblueleague/filefairy/testing/"
    cwd = os.getcwd()
    os.chdir(path)

    page = ''
    with open(url, 'r') as f:
      page = f.read()

    os.chdir(cwd)
    return page

  def chatInjuryTest(self):
    self.slackApi.chatPostMessage('testing', injury)

  def chatFinalScoresTest(self):
    self.slackApi.chatPostMessage('testing', finalScores)

  def getListen(self):
    t1 = threading.Thread(target=self.listen)
    t1.start()
    time.sleep(6)

    t2 = threading.Thread(target=self.chatInjuryTest)
    t2.start()
    time.sleep(2)

    t3 = threading.Thread(target=self.chatFinalScoresTest)
    t3.start()
    time.sleep(2)

    self.handleClose()
    time.sleep(2)

    t1.join()
    t2.join()
    t3.join()

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
    'export_01172017_1.html',         # 3. League file date has changed.
]

fileDates = {
    'old': 'Saturday January 14, 2017 13:01:09 EST',
    'new': 'Tuesday January 17, 2017 09:03:12 EST',
}

records = {
    31: [0, 0, 0], 32: [1, 0, 0], 33: [0, 1, 0], 34: [0, 0, 0], 35: [0, 1, 0],
    36: [0, 1, 0], 37: [0, 1, 0], 38: [1, 0, 0], 39: [0, 1, 0], 40: [0, 1, 0],
    41: [1, 0, 0], 42: [1, 0, 0], 43: [1, 0, 0], 44: [1, 0, 0], 45: [1, 0, 0],
    46: [1, 0, 0], 47: [0, 1, 0], 48: [0, 1, 0], 49: [1, 0, 0], 50: [1, 0, 0],
    51: [1, 0, 0], 52: [0, 1, 0], 53: [0, 1, 0], 54: [1, 0, 0], 55: [0, 1, 0],
    56: [1, 0, 0], 57: [0, 1, 0], 58: [1, 0, 0], 59: [0, 1, 0], 60: [0, 1, 0]
}

formatRecords = 'AL East\n:redsox: 0-0 :separator: :orioles: 0-1 :separator: :yankees: 0-1 :separator: :rays: 0-1 :separator: :jays: 0-1\n\n' + \
    'AL Central\n:indians: 1-0 :separator: :monarchs: 1-0 :separator: :whitesox: 0-1 :separator: :crackeyes: 0-1 :separator: :twincities: 0-1\n\n' + \
    'AL West\n:stros: 1-0 :separator: :angels: 1-0 :separator: :athletics: 1-0 :separator: :mariners: 1-0 :separator: :rangers: 1-0\n\n' + \
    'NL East\n:braves: 1-0 :separator: :marlins: 1-0 :separator: :mets: 1-0 :separator: :phillies: 1-0 :separator: :nationals: 0-1\n\n' + \
    'NL Central\n:brewers: 1-0 :separator: :cardinals: 1-0 :separator: :cubbies: 0-1 :separator: :reds: 0-1 :separator: :pirates: 0-1\n\n' + \
    'NL West\n:dodgers: 1-0 :separator: :dbacks: 0-0 :separator: :rox: 0-1 :separator: :pads: 0-1 :separator: :giants: 0-1'

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
  appTest = AppTest(logger, slackApi, fileUrls[:])

  assertNotEquals(appTest.findFileDate(filePage), '')


def testFindFileDate():
  logger = TestLogger()
  slackApi = TestSlackApi(logger)
  appTest = AppTest(logger, slackApi, fileUrls[:])

  page = appTest.getPage(fileUrls[0])
  assertEquals(appTest.findFileDate(page), fileDates['old'])

  page = appTest.getPage(fileUrls[1])
  assertEquals(appTest.findFileDate(page), fileDates['old'])

  page = appTest.getPage(fileUrls[2])
  assertEquals(appTest.findFileDate(page), fileDates['old'])

  page = appTest.getPage(fileUrls[3])
  assertEquals(appTest.findFileDate(page), fileDates['new'])


def testUpdateLeagueFile():
  logger = TestLogger()
  slackApi = TestSlackApi(logger)
  appTest = AppTest(logger, slackApi, fileUrls[:])

  expected = {'ret': False, 'collected': [], 'index': 1,
              'date': fileDates['old']}
  assertEquals(appTest.getUpdateLeagueFile(), expected)

  expected = {'ret': False, 'collected': [], 'index': 2,
              'date': fileDates['old']}
  assertEquals(appTest.getUpdateLeagueFile(), expected)

  expected = {'ret': True, 'collected': logs[4:6], 'index': 3,
              'date': fileDates['new']}
  assertEquals(appTest.getUpdateLeagueFile(), expected)

  expected = {'ret': False, 'collected': logs[4:6], 'index': 3,
              'date': fileDates['new']}
  assertEquals(appTest.getUpdateLeagueFile(), expected)


def testWatch():
  logger = TestLogger()
  slackApi = TestSlackApi(logger)
  appTest = AppTest(logger, slackApi, fileUrls[:])

  expected = {'collected': logs[1:4] + logs[5:8]}
  assertEquals(appTest.getWatch(), expected)


def testFinalScores():
  logger = TestLogger()
  slackApi = TestSlackApi(logger)
  appTest = AppTest(logger, slackApi, fileUrls[:])

  appTest.handleFinalScores(finalScores)
  appTest.processFinalScores()
  assertEquals(appTest.records, records)
  assertEquals(appTest.formatRecords(), formatRecords)


def testListen():
  logger = TestLogger()
  slackApi = SlackApi(logger)
  appTest = AppTest(logger, slackApi, fileUrls[:])

  expected = {'collected': logs[:1] + logs[8:]}
  assertEquals(appTest.getListen(), expected)


def testIntegration():
  logger = TestLogger()
  slackApi = SlackApi(logger)
  appTest = AppTest(logger, slackApi, fileUrls[:], True)

  expected = {'collected': logs[:1] + logs[2:3] + logs[5:6] + logs[7:9]}
  assertEquals(appTest.getIntegration(), expected)


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--mode', dest='mode')
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

  if args.mode == 'listen' or args.mode == 'all':
    testListen()

  if args.mode == 'integration' or args.mode == 'all':
    testIntegration()

  print 'Passed.'
