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
              '<https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_24216.html|Atlanta 7, Colorado 6>\n' + \
              '<https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_24018.html|Cleveland 5, Toronto 1>\n' + \
              '<https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_24015.html|Houston 5, Tampa Bay 3>\n' + \
              '<https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_24014.html|Kansas City 7, Detroit 2>\n' + \
              '<https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_24212.html|Los Angeles 3, Cincinnati 2>\n' + \
              '<https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_24013.html|Los Angeles 7, New York 6>\n' + \
              '<https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_24214.html|Miami 4, Pittsburgh 1>\n' + \
              '<https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_24215.html|Milwaukee 9, Washington 8>\n' + \
              '<https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_24218.html|New York 6, San Diego 1>\n' + \
              '<https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_24017.html|Oakland 5, Minnesota 2>\n' + \
              '<https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_24213.html|Philadelphia 4, San Francisco 2>\n' + \
              '<https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_24016.html|Seattle 3, Baltimore 2>\n' + \
              '<https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_24217.html|St. Louis 2, Chicago 0>\n' + \
              '<https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_24019.html|Texas 8, Chicago 2>'


class AppTest(App):
  '''Tests for App.'''

  def __init__(self, logger, slackApi, fileUrls, simUrls, integration=False):
    self.logger = logger
    self.slackApi = slackApi

    self.fileUrls, self.fileIndex = fileUrls, 0
    self.filePage = self.getPage(self.fileUrls[0])
    self.fileDate = self.findFileDate(self.filePage)

    self.simUrls, self.simIndex = simUrls, 0
    self.simPage = self.getPage(self.simUrls[0])
    self.simDate = self.findSimDate(self.simPage)
    self.updates = self.findUpdates(self.simPage)

    self.records = {t: [0, 0, 0] for t in range(31, 61)}
    self.ws = None
    self.integration = integration

  def getFileUrl(self):
    if len(self.fileUrls) > self.fileIndex + 1:
      self.fileIndex = self.fileIndex + 1

    return self.fileUrls[self.fileIndex]

  def getSimUrl(self):
    if len(self.simUrls) > self.simIndex + 1:
      self.simIndex = self.simIndex + 1

    if self.integration and self.simIndex == 1:
      self.slackApi.chatPostMessage('testing', injury)
    elif self.integration and self.simIndex == 2:
      self.slackApi.chatPostMessage('testing', finalScores)

    return self.simUrls[self.simIndex]

  def getChannelGeneral(self):
    return 'testing'

  def getChannelLiveSimDiscussion(self):
    return 'testing'

  def getChannelStatsplus(self):
    return 'testing'

  def getTimerValues(self):
    return [1, 2, 8]

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

  def getUpdateLiveSim(self):
    ret = self.updateLiveSim()
    self.logger.collect()
    return {
        'ret': ret,
        'collected': self.logger.collected,
        'index': self.simIndex,
        'date': self.simDate,
        'updates': self.updates,
    }


path = 'http://brunnerj.com/orangeandblueleague/'

filePages = [
    'export_01142017_1.html',         # 0. Initial exports page.
    'export_01142017_2.html',         # 1. League file date has not changed.
    'export_01142017_2.html',         # 2. League file date has not changed.
    'export_01172017_1.html',         # 3. League file date has changed.
]
fileUrls = [os.path.join(path, fi) for fi in filePages]

fileDates = {
    'old': 'Saturday January 14, 2017 13:01:09 EST',
    'new': 'Tuesday January 17, 2017 09:03:12 EST',
}

simPages = [
    'sim_09052018_1.html',            # 0. Initial sim page.
    'sim_09052018_2.html',            # 1. Same date. No new final games.
    'sim_09052018_3.html',            # 2. Same date. One new final game.
    'sim_09092018_1.html',            # 3. Different date, partially loaded.
    'sim_09092018_2.html',            # 4. Fully loaded.
    'sim_09092018_3.html',            # 5. Partially loaded again.
]
simUrls = [os.path.join(path, fi) for fi in simPages]

simDates = {
    'old': '09052018',
    'new': '09092018',
}

updates = {
    'update1': ':toparrow: 4 :separator: :pirates: 10 ' +
    ':separator: :giants: 0\n:pirates: C.J. Hinojosa ' +
    'hits a 3-run HR.',
    'update2': ':bottomarrow: 5 :separator: :pirates: ' +
    '10 :separator: :giants: 2\n:giants: David ' +
    'Olmedo-Barrera hits a 2-run HR.'
}

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

  simUrl = 'http://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/real_time_sim/index.html'
  simPage = urllib2.urlopen(simUrl).read()

  logger = TestLogger()
  slackApi = TestSlackApi(logger)
  appTest = AppTest(logger, slackApi, [fileUrl], [simUrl])

  assertNotEquals(appTest.findFileDate(filePage), '')
  assertNotEquals(appTest.findSimDate(simPage), '')


def testFindFileDate():
  logger = TestLogger()
  slackApi = TestSlackApi(logger)
  appTest = AppTest(logger, slackApi, fileUrls[:], simUrls[:])

  page = urllib2.urlopen(fileUrls[0]).read()
  assertEquals(appTest.findFileDate(page), fileDates['old'])

  page = urllib2.urlopen(fileUrls[1]).read()
  assertEquals(appTest.findFileDate(page), fileDates['old'])

  page = urllib2.urlopen(fileUrls[2]).read()
  assertEquals(appTest.findFileDate(page), fileDates['old'])

  page = urllib2.urlopen(fileUrls[3]).read()
  assertEquals(appTest.findFileDate(page), fileDates['new'])


def testFindSimDate():
  logger = TestLogger()
  slackApi = TestSlackApi(logger)
  appTest = AppTest(logger, slackApi, fileUrls[:], simUrls[:])

  page = urllib2.urlopen(simUrls[0]).read()
  assertEquals(appTest.findSimDate(page), simDates['old'])

  page = urllib2.urlopen(simUrls[1]).read()
  assertEquals(appTest.findSimDate(page), simDates['old'])

  page = urllib2.urlopen(simUrls[2]).read()
  assertEquals(appTest.findSimDate(page), simDates['old'])

  page = urllib2.urlopen(simUrls[3]).read()
  assertEquals(appTest.findSimDate(page), simDates['new'])

  page = urllib2.urlopen(simUrls[4]).read()
  assertEquals(appTest.findSimDate(page), simDates['new'])

  page = urllib2.urlopen(simUrls[5]).read()
  assertEquals(appTest.findSimDate(page), simDates['new'])


def testFindUpdates():
  logger = TestLogger()
  slackApi = TestSlackApi(logger)
  appTest = AppTest(logger, slackApi, fileUrls[:], simUrls[:])

  page = urllib2.urlopen(simUrls[0]).read()
  assertEquals(appTest.findUpdates(page), [updates['update1']])

  page = urllib2.urlopen(simUrls[1]).read()
  assertEquals(appTest.findUpdates(page), [])

  page = urllib2.urlopen(simUrls[2]).read()
  assertEquals(appTest.findUpdates(page), [updates['update2']])

  page = urllib2.urlopen(simUrls[3]).read()
  assertEquals(appTest.findUpdates(page), [])

  page = urllib2.urlopen(simUrls[4]).read()
  assertEquals(appTest.findUpdates(page), [])

  page = urllib2.urlopen(simUrls[5]).read()
  assertEquals(appTest.findUpdates(page), [])


def testUpdateLeagueFile():
  logger = TestLogger()
  slackApi = TestSlackApi(logger)
  appTest = AppTest(logger, slackApi, fileUrls[:], simUrls[:])

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


def testUpdateLiveSim():
  logger = TestLogger()
  slackApi = TestSlackApi(logger)
  appTest = AppTest(logger, slackApi, fileUrls[:], simUrls[:])

  expected = {'ret': True, 'collected': [], 'index': 1,
              'date': simDates['old'],
              'updates': [updates['update1']]}
  assertEquals(appTest.getUpdateLiveSim(), expected)

  expected = {'ret': True, 'collected': logs[1:2], 'index': 2,
              'date': simDates['old'],
              'updates': [updates['update1'], updates['update2']]}
  assertEquals(appTest.getUpdateLiveSim(), expected)

  expected = {'ret': True, 'collected': logs[1:2], 'index': 3,
              'date': simDates['new'], 'updates': []}
  assertEquals(appTest.getUpdateLiveSim(), expected)

  expected = {'ret': True, 'collected': logs[1:2], 'index': 4,
              'date': simDates['new'], 'updates': []}
  assertEquals(appTest.getUpdateLiveSim(), expected)

  expected = {'ret': True, 'collected': logs[1:2], 'index': 5,
              'date': simDates['new'], 'updates': []}
  assertEquals(appTest.getUpdateLiveSim(), expected)

  expected = {'ret': True, 'collected': logs[1:2], 'index': 5,
              'date': simDates['new'], 'updates': []}
  assertEquals(appTest.getUpdateLiveSim(), expected)


def testWatch():
  logger = TestLogger()
  slackApi = TestSlackApi(logger)
  appTest = AppTest(logger, slackApi, fileUrls[:], simUrls[:])

  expected = {'collected': logs[1:5] + logs[5:8]}
  assertEquals(appTest.getWatch(), expected)


def testListen():
  logger = TestLogger()
  slackApi = SlackApi(logger)
  appTest = AppTest(logger, slackApi, fileUrls[:], simUrls[:])

  expected = {'collected': logs[:1] + logs[8:]}
  assertEquals(appTest.getListen(), expected)


def testIntegration():
  logger = TestLogger()
  slackApi = SlackApi(logger)
  appTest = AppTest(logger, slackApi, fileUrls[:], simUrls[:], True)

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

  if args.mode == 'updates' or args.mode == 'all':
    testFindUpdates()

  if args.mode == 'leaguefile' or args.mode == 'all':
    testUpdateLeagueFile()

  if args.mode == 'livesim' or args.mode == 'all':
    testUpdateLiveSim()

  if args.mode == 'watch' or args.mode == 'all':
    testWatch()

  if args.mode == 'listen' or args.mode == 'all':
    testListen()

  if args.mode == 'integration' or args.mode == 'all':
    testIntegration()

  print 'Passed.'
