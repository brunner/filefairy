#!/usr/bin/env python

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
import threading
import time
import urllib2

from app import App
from slack_api import chat_post_message
from utils import assert_equals

injury = '03/21/2021 RP <https://player_33610.html|Drew Pomeranz> was injured ' + \
         'while pitching (Baltimore @ Seattle)'

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

overstandings = '31 36 46\n32 43 38\n33 45 38\n34 43 39\n35 41 41\n36 42 40\n' + \
                '37 57 24\n38 38 44\n39 48 33\n40 39 43\n41 29 53\n42 36 46\n' + \
                '43 43 41\n44 39 42\n45 48 33\n46 38 44\n47 48 35\n48 38 44\n' + \
                '49 45 38\n50 34 47\n51 42 39\n52 25 57\n53 49 33\n54 49 31\n' + \
                '55 36 46\n56 44 37\n57 43 40\n58 28 54\n59 47 35\n60 35 47\n'


class AppTest(App):

  def __init__(self, file_url='', standings_in='data/standings_in.txt'):
    self.file_url = file_url
    self.standings_in = standings_in

  def get_path(self):
    return os.path.expanduser('~') + '/orangeandblueleague/filefairy/testing/'

  def get_standings_out(self):
    return self.get_path() + 'data/standings_out.txt'

  def get_general_name(self):
    return 'testing'

  def get_live_sim_discussion_name(self):
    return 'testing'

  def get_statsplus_id(self):
    return 'G3SUFLMK4'

  def get_timer_values(self):
    return [2, 10]

  def get_page(self, url):
    path = self.get_path()
    cwd = os.getcwd()
    os.chdir(path)
    page = ''
    if url:
      with open(url, 'r') as f:
        page = f.read()
    os.chdir(cwd)
    return page


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


def testFinalScores():
  appTest = AppTest()
  appTest.setup()

  appTest.handleFinalScores(finalScores)
  appTest.handleLiveTable(liveTable)
  appTest.process_final_scores()
  assert_equals(appTest.records, records)
  assert_equals(appTest.standings, standings)
  assert_equals(appTest.formatRecords(), formatRecords)
  assert_equals(appTest.formatStandingsAL(), formatStandingsA)
  assert_equals(appTest.formatStandingsNL(), formatStandingsN)


def testStandings():
  # appTest = AppTest(fileUrls[:], 'data/standings_openingday.txt')
  # print appTest.formatStandingsAL()
  # print appTest.formatStandingsNL()
  # print '\n--------------------\n'

  # appTest = AppTest(fileUrls[:], 'data/standings_linear.txt')
  # print appTest.formatStandingsAL()
  # print appTest.formatStandingsNL()
  # print '\n--------------------\n'

  # appTest = AppTest(fileUrls[:], 'data/standings_final.txt')
  # print appTest.formatStandingsAL()
  # print appTest.formatStandingsNL()
  # print '\n--------------------\n'

  # appTest = AppTest(fileUrls[:], 'data/standings_baddivision.txt')
  # print appTest.formatStandingsAL()
  # print appTest.formatStandingsNL()
  # print '\n--------------------\n'

  # appTest = AppTest(fileUrls[:], 'data/standings_today.txt')
  # print appTest.formatStandingsAL()
  # print appTest.formatStandingsNL()

  path = os.path.expanduser('~') + '/orangeandblueleague/filefairy/testing/data/standings_over.txt'
  with open(path, 'w') as f:
    f.write(overstandings)
  appTest = AppTest()
  appTest.setup()

  print appTest.formatStandingsAL()
  print appTest.formatStandingsNL()
  os.remove(path)


def testListen():
  appTest = AppTest()
  appTest.setup()

  t1 = threading.Thread(target=appTest.listen)
  t1.start()
  time.sleep(6)

  chat_post_message('testing', injury)
  chat_post_message('testing', finalScores)
  chat_post_message('testing', liveTable)
  time.sleep(2)

  appTest.handle_close()
  t1.join()


def testIntegration():
  appTest = AppTest(file_url='data/exports1.html')
  appTest.setup()

  with open(appTest.get_standings_out(), 'w') as f:
    pass

  t1 = threading.Thread(target=appTest.listen)
  t1.start()
  time.sleep(6)

  t2 = threading.Thread(target=appTest.watch)
  t2.start()
  time.sleep(2)

  chat_post_message('testing', injury)
  chat_post_message('testing', finalScores)
  chat_post_message('testing', liveTable)
  time.sleep(2)

  appTest.file_url = 'data/exports2.html'
  time.sleep(2)

  appTest.handle_close()
  t1.join()
  t2.join()

  out, gold = '', ''
  with open(appTest.get_standings_out(), 'r') as f:
    out = f.read()
  with open(appTest.get_path() + 'data/standings_gold.txt', 'r') as f:
    gold = f.read()
  assert_equals(out, gold)


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--mode', dest='mode', default='all')
  args = parser.parse_args()

  if args.mode == 'finalscores' or args.mode == 'all':
    testFinalScores()

  if args.mode == 'standings':
    testStandings()

  if args.mode == 'listen' or args.mode == 'all':
    testListen()

  if args.mode == 'integration' or args.mode == 'all':
    testIntegration()

  print 'Passed.'
