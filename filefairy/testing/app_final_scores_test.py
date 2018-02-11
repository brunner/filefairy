#!/usr/bin/env python

import threading
import time

from app_test import AppTest
from slack_api import chat_post_message
from utils import assert_equals


inpt = ['03/21/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_24216.html|Atlanta 7, Colorado 6>*\n' +
        '*<https://game_box_24018.html|Cleveland 5, Toronto 1>*\n' +
        '*<https://game_box_24015.html|Houston 5, Tampa Bay 3>*\n' +
        '*<https://game_box_24014.html|Kansas City 7, Detroit 2>*\n' +
        '*<https://game_box_24212.html|Los Angeles 3, Cincinnati 2>*\n' +
        '*<https://game_box_24013.html|Los Angeles 7, New York 6>*\n' +
        '*<https://game_box_24214.html|Miami 4, Pittsburgh 1>*\n' +
        '*<https://game_box_24215.html|Milwaukee 9, Washington 8>*\n' +
        '*<https://game_box_24218.html|New York 6, San Diego 1>*\n' +
        '*<https://game_box_24017.html|Oakland 5, Minnesota 2>*\n' +
        '*<https://game_box_24213.html|Philadelphia 4, San Francisco 2>*\n' +
        '*<https://game_box_24016.html|Seattle 3, Baltimore 2>*\n' +
        '*<https://game_box_24217.html|St. Louis 2, Chicago 0>*\n' +
        '*<https://game_box_24019.html|Texas 8, Chicago 2>*',
        '```MAJOR LEAGUE BASEBALL Live Table - 03/21/2021\n' +
        'Cincinnati Reds                48\nColorado Rockies               43\n' +
        'Los Angeles Dodgers            43\nSan Diego Padres               42\n' +
        'Minnesota Twins                41\nSt. Louis Cardinals            41\n' +
        'Atlanta Braves                 40\nKansas City Royals             40\n' +
        'Seattle Mariners               40\nToronto Blue Jays              40\n' +
        'New York Mets                  38\nPhiladelphia Phillies          38\n' +
        'Baltimore Orioles              37\nBoston Red Sox                 36\n' +
        'Tampa Bay Rays                 36\nChicago Cubs                   35\n' +
        'Cleveland Indians              34\nDetroit Tigers                 34\n' +
        'New York Yankees               34\nChicago White Sox              33\n' +
        'Milwaukee Brewers              33\nHouston Astros                 31\n' +
        'Los Angeles Angels             31\nWashington Nationals           31\n' +
        'Oakland Athletics              30\nSan Francisco Giants           30\n' +
        'Arizona Diamondbacks           25\nMiami Marlins                  25\n' +
        'Texas Rangers                  25\nPittsburgh Pirates             21````',
        '03/22/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_1791.html|Arizona 7, Philadelphia 5>*\n' +
        '*<https://game_box_1792.html|Atlanta 4, Miami 3>*\n' +
        '*<https://game_box_1802.html|Baltimore 2, Chicago 1>*\n' +
        '*<https://game_box_1801.html|Boston 10, Pittsburgh 9>*\n' +
        '*<https://game_box_1794.html|Cincinnati 6, Milwaukee 4>*\n' +
        '*<https://game_box_1796.html|Cleveland 6, Kansas City 1>*\n' +
        '*<https://game_box_1804.html|Colorado 5, San Diego 1>*\n' +
        '*<https://game_box_1797.html|Detroit 2, Seattle 1>*\n' +
        '*<https://game_box_1800.html|Los Angeles 5, Oakland 4>*\n' +
        '*<https://game_box_1805.html|Los Angeles 6, New York 5>*\n' +
        '*<https://game_box_1795.html|Minnesota 2, Chicago 1>*\n' +
        '*<https://game_box_1798.html|New York 7, Tampa Bay 6>*\n' +
        '*<https://game_box_1793.html|San Francisco 2, Washington 1>*\n' +
        '*<https://game_box_1799.html|Texas 6, Houston 3>*\n' +
        '*<https://game_box_1803.html|Toronto 5, St. Louis 4>*',
        '```MAJOR LEAGUE BASEBALL Live Table - 03/22/2021\n' +
        'Cincinnati Reds                49\nColorado Rockies               44\n' +
        'Los Angeles Dodgers            44\nSan Diego Padres               42\n' +
        'Minnesota Twins                42\nSt. Louis Cardinals            41\n' +
        'Atlanta Braves                 41\nToronto Blue Jays              41\n' +
        'Kansas City Royals             40\nSeattle Mariners               40\n' +
        'New York Mets                  38\nPhiladelphia Phillies          38\n' +
        'Baltimore Orioles              38\nBoston Red Sox                 37\n' +
        'Tampa Bay Rays                 36\nChicago Cubs                   35\n' +
        'Cleveland Indians              35\nDetroit Tigers                 35\n' +
        'New York Yankees               35\nChicago White Sox              33\n' +
        'Milwaukee Brewers              33\nLos Angeles Angels             32\n' +
        'Houston Astros                 31\nWashington Nationals           31\n' +
        'San Francisco Giants           31\nOakland Athletics              30\n' +
        'Arizona Diamondbacks           26\nTexas Rangers                  26\n' +
        'Miami Marlins                  25\nPittsburgh Pirates             21````']

outp = ['03/21/2021\n' +
        '<https://game_box_24216.html|Atlanta 7, Colorado 6>\n' +
        '<https://game_box_24018.html|Cleveland 5, Toronto 1>\n' +
        '<https://game_box_24015.html|Houston 5, Tampa Bay 3>\n' +
        '<https://game_box_24014.html|Kansas City 7, Detroit 2>\n' +
        '<https://game_box_24212.html|Los Angeles 3, Cincinnati 2>\n' +
        '<https://game_box_24013.html|Los Angeles 7, New York 6>\n' +
        '<https://game_box_24214.html|Miami 4, Pittsburgh 1>\n' +
        '<https://game_box_24215.html|Milwaukee 9, Washington 8>\n' +
        '<https://game_box_24218.html|New York 6, San Diego 1>\n' +
        '<https://game_box_24017.html|Oakland 5, Minnesota 2>\n' +
        '<https://game_box_24213.html|Philadelphia 4, San Francisco 2>\n' +
        '<https://game_box_24016.html|Seattle 3, Baltimore 2>\n' +
        '<https://game_box_24217.html|St. Louis 2, Chicago 0>\n' +
        '<https://game_box_24019.html|Texas 8, Chicago 2>',
        '03/22/2021\n' +
        '<https://game_box_1791.html|Arizona 7, Philadelphia 5>\n' +
        '<https://game_box_1792.html|Atlanta 4, Miami 3>\n' +
        '<https://game_box_1802.html|Baltimore 2, Chicago 1>\n' +
        '<https://game_box_1801.html|Boston 10, Pittsburgh 9>\n' +
        '<https://game_box_1794.html|Cincinnati 6, Milwaukee 4>\n' +
        '<https://game_box_1796.html|Cleveland 6, Kansas City 1>\n' +
        '<https://game_box_1804.html|Colorado 5, San Diego 1>\n' +
        '<https://game_box_1797.html|Detroit 2, Seattle 1>\n' +
        '<https://game_box_1800.html|Los Angeles 5, Oakland 4>\n' +
        '<https://game_box_1805.html|Los Angeles 6, New York 5>\n' +
        '<https://game_box_1795.html|Minnesota 2, Chicago 1>\n' +
        '<https://game_box_1798.html|New York 7, Tampa Bay 6>\n' +
        '<https://game_box_1793.html|San Francisco 2, Washington 1>\n' +
        '<https://game_box_1799.html|Texas 6, Houston 3>\n' +
        '<https://game_box_1803.html|Toronto 5, St. Louis 4>']

rcrd = ['AL East\n' +
        ':orioles: 0-1 :separator: :yankees: 0-1 :separator: :rays: 0-1 ' +
        ':separator: :jays: 0-1\n\n' +
        'AL Central\n' +
        ':indians: 1-0 :separator: :monarchs: 1-0 :separator: :whitesox: 0-1 ' +
        ':separator: :crackeyes: 0-1 :separator: :twincities: 0-1\n\n' +
        'AL West\n' +
        ':stros: 1-0 :separator: :angels: 1-0 :separator: :athletics: 1-0 ' +
        ':separator: :mariners: 1-0 :separator: :rangers: 1-0\n\n' +
        'NL East\n' +
        ':braves: 1-0 :separator: :marlins: 1-0 :separator: :mets: 1-0 ' +
        ':separator: :phillies: 1-0 :separator: :nationals: 0-1\n\n' +
        'NL Central\n' +
        ':brewers: 1-0 :separator: :cardinals: 1-0 :separator: :cubbies: 0-1 ' +
        ':separator: :reds: 0-1 :separator: :pirates: 0-1\n\n' +
        'NL West\n' +
        ':dodgers: 1-0 :separator: :rox: 0-1 :separator: :pads: 0-1 ' +
        ':separator: :giants: 0-1',
        'AL East\n' +
        ':redsox: 1-0 :separator: :orioles: 1-1 :separator: :yankees: 1-1 ' +
        ':separator: :jays: 1-1 :separator: :rays: 0-2\n\n' +
        'AL Central\n' +
        ':indians: 2-0 :separator: :crackeyes: 1-1 :separator: :monarchs: 1-1 ' +
        ':separator: :twincities: 1-1 :separator: :whitesox: 0-2\n\n' +
        'AL West\n' +
        ':angels: 2-0 :separator: :rangers: 2-0 :separator: :stros: 1-1 ' +
        ':separator: :athletics: 1-1 :separator: :mariners: 1-1\n\n' +
        'NL East\n' +
        ':braves: 2-0 :separator: :marlins: 1-1 :separator: :mets: 1-1 ' +
        ':separator: :phillies: 1-1 :separator: :nationals: 0-2\n\n' +
        'NL Central\n' +
        ':reds: 1-1 :separator: :brewers: 1-1 :separator: :cardinals: 1-1 ' +
        ':separator: :cubbies: 0-2 :separator: :pirates: 0-2\n\n' +
        'NL West\n' +
        ':dodgers: 2-0 :separator: :dbacks: 1-0 :separator: :rox: 1-1 ' +
        ':separator: :giants: 1-1 :separator: :pads: 0-2']

stnd = ['AL East         |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Toronto         |  40 |  29 |     - |  90\n' +
        'Boston          |  36 |  33 |   4.0 |    \n' +
        'Baltimore       |  37 |  35 |   4.5 |    \n' +
        'Tampa Bay       |  36 |  35 |   5.0 |    \n' +
        'New York        |  34 |  37 |   7.0 |    \n\n' +
        'AL Central      |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Minnesota       |  41 |  30 |     - |  89\n' +
        'Kansas City     |  40 |  33 |   2.0 |    \n' +
        'Cleveland       |  34 |  36 |   6.5 |    \n' +
        'Detroit         |  34 |  36 |   6.5 |    \n' +
        'Chicago         |  33 |  38 |   8.0 |    \n\n' +
        'AL West         |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Seattle         |  40 |  28 |     - |  84\n' +
        'Houston         |  31 |  39 |  10.0 |    \n' +
        'Los Angeles     |  31 |  39 |  10.0 |    \n' +
        'Oakland         |  30 |  40 |  11.0 |    \n' +
        'Texas           |  25 |  46 |  16.5 |    \n\n' +
        'AL Wild Card    |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Kansas City     |  40 |  33 |  +2.0 |  88\n' +
        'Boston          |  36 |  33 |     - |  92\n' +
        'Baltimore       |  37 |  35 |   0.5 |    \n' +
        'Tampa Bay       |  36 |  35 |   1.0 |    \n' +
        'Cleveland       |  34 |  36 |   2.5 |    \n' +
        'Detroit         |  34 |  36 |   2.5 |    \n' +
        'New York        |  34 |  37 |   3.0 |    \n' +
        'Chicago         |  33 |  38 |   4.0 |    \n' +
        'Houston         |  31 |  39 |   5.5 |    \n' +
        'Los Angeles     |  31 |  39 |   5.5 |    \n' +
        'Oakland         |  30 |  40 |   6.5 |    \n' +
        'Texas           |  25 |  46 |  12.0 |    \n' +
        'NL East         |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Atlanta         |  40 |  30 |     - |  91\n' +
        'Philadelphia    |  38 |  32 |   2.0 |    \n' +
        'New York        |  38 |  33 |   2.5 |    \n' +
        'Washington      |  31 |  40 |   9.5 |    \n' +
        'Miami           |  25 |  45 |  15.0 |    \n\n' +
        'NL Central      |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Cincinnati      |  48 |  21 |     - |  87\n' +
        'St. Louis       |  41 |  28 |   7.0 |    \n' +
        'Chicago         |  35 |  36 |  14.0 |    \n' +
        'Milwaukee       |  33 |  38 |  16.0 |    \n' +
        'Pittsburgh      |  21 |  50 |  28.0 |    \n\n' +
        'NL West         |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Colorado        |  43 |  26 |     - |  94\n' +
        'Los Angeles     |  43 |  26 |     - |  94\n' +
        'San Diego       |  42 |  29 |   2.0 |    \n' +
        'San Francisco   |  30 |  41 |  14.0 |    \n' +
        'Arizona         |  25 |  44 |  18.0 |    \n\n' +
        'NL Wild Card    |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Colorado        |  43 |  26 |  +2.0 |  91\n' +
        'Los Angeles     |  43 |  26 |  +2.0 |  91\n' +
        'St. Louis       |  41 |  28 |     - |  93\n' +
        'San Diego       |  42 |  29 |     - |  93\n' +
        'Philadelphia    |  38 |  32 |   3.5 |    \n' +
        'New York        |  38 |  33 |   4.0 |    \n' +
        'Chicago         |  35 |  36 |   7.0 |    \n' +
        'Milwaukee       |  33 |  38 |   9.0 |    \n' +
        'Washington      |  31 |  40 |  11.0 |    \n' +
        'San Francisco   |  30 |  41 |  12.0 |    \n' +
        'Arizona         |  25 |  44 |  16.0 |    \n' +
        'Miami           |  25 |  45 |  16.5 |    \n' +
        'Pittsburgh      |  21 |  50 |  21.0 |    ',
        'AL East         |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Toronto         |  41 |  29 |     - |  89\n' +
        'Boston          |  37 |  33 |   4.0 |    \n' +
        'Baltimore       |  38 |  35 |   4.5 |    \n' +
        'Tampa Bay       |  36 |  36 |   6.0 |    \n' +
        'New York        |  35 |  37 |   7.0 |    \n\n' +
        'AL Central      |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Minnesota       |  42 |  30 |     - |  87\n' +
        'Kansas City     |  40 |  34 |   3.0 |    \n' +
        'Cleveland       |  35 |  36 |   6.5 |    \n' +
        'Detroit         |  35 |  36 |   6.5 |    \n' +
        'Chicago         |  33 |  39 |   9.0 |    \n\n' +
        'AL West         |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Seattle         |  40 |  29 |     - |  84\n' +
        'Los Angeles     |  32 |  39 |   9.0 |    \n' +
        'Houston         |  31 |  40 |  10.0 |    \n' +
        'Oakland         |  30 |  41 |  11.0 |    \n' +
        'Texas           |  26 |  46 |  15.5 |    \n\n' +
        'AL Wild Card    |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Kansas City     |  40 |  34 |  +1.0 |  88\n' +
        'Boston          |  37 |  33 |     - |  91\n' +
        'Baltimore       |  38 |  35 |   0.5 |    \n' +
        'Tampa Bay       |  36 |  36 |   2.0 |    \n' +
        'Cleveland       |  35 |  36 |   2.5 |    \n' +
        'Detroit         |  35 |  36 |   2.5 |    \n' +
        'New York        |  35 |  37 |   3.0 |    \n' +
        'Chicago         |  33 |  39 |   5.0 |    \n' +
        'Los Angeles     |  32 |  39 |   5.5 |    \n' +
        'Houston         |  31 |  40 |   6.5 |    \n' +
        'Oakland         |  30 |  41 |   7.5 |    \n' +
        'Texas           |  26 |  46 |  12.0 |    \n' +
        'NL East         |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Atlanta         |  41 |  30 |     - |  89\n' +
        'Philadelphia    |  38 |  33 |   3.0 |    \n' +
        'New York        |  38 |  34 |   3.5 |    \n' +
        'Washington      |  31 |  41 |  10.5 |    \n' +
        'Miami           |  25 |  46 |  16.0 |    \n\n' +
        'NL Central      |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Cincinnati      |  49 |  21 |     - |  85\n' +
        'St. Louis       |  41 |  29 |   8.0 |    \n' +
        'Chicago         |  35 |  37 |  15.0 |    \n' +
        'Milwaukee       |  33 |  39 |  17.0 |    \n' +
        'Pittsburgh      |  21 |  51 |  29.0 |    \n\n' +
        'NL West         |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Colorado        |  44 |  26 |     - |  93\n' +
        'Los Angeles     |  44 |  26 |     - |  93\n' +
        'San Diego       |  42 |  30 |   3.0 |    \n' +
        'San Francisco   |  31 |  41 |  14.0 |    \n' +
        'Arizona         |  26 |  44 |  18.0 |    \n\n' +
        'NL Wild Card    |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Colorado        |  44 |  26 |  +3.0 |  89\n' +
        'Los Angeles     |  44 |  26 |  +3.0 |  89\n' +
        'St. Louis       |  41 |  29 |     - |  92\n' +
        'San Diego       |  42 |  30 |     - |  92\n' +
        'Philadelphia    |  38 |  33 |   3.5 |    \n' +
        'New York        |  38 |  34 |   4.0 |    \n' +
        'Chicago         |  35 |  37 |   7.0 |    \n' +
        'Milwaukee       |  33 |  39 |   9.0 |    \n' +
        'San Francisco   |  31 |  41 |  11.0 |    \n' +
        'Washington      |  31 |  41 |  11.0 |    \n' +
        'Arizona         |  26 |  44 |  15.0 |    \n' +
        'Miami           |  25 |  46 |  16.5 |    \n' +
        'Pittsburgh      |  21 |  51 |  21.0 |    ']


def test():
  appTest = AppTest(settings_in='data/settings_in.txt', standings_in='data/standings_in.txt')
  appTest.setup()

  t1 = threading.Thread(target=appTest.listen)
  t1.start()
  time.sleep(6)

  chat_post_message('testing', inpt[0])
  chat_post_message('testing', inpt[1])
  time.sleep(2)
  assert_equals(appTest.process_final_scores(), outp[0])
  assert_equals(appTest.process_records(), rcrd[0])
  assert_equals(appTest.process_standings(), stnd[0])

  chat_post_message('testing', inpt[2])
  chat_post_message('testing', inpt[3])
  time.sleep(2)
  assert_equals(appTest.process_final_scores(), outp[1])
  assert_equals(appTest.process_records(), rcrd[1])
  assert_equals(appTest.process_standings(), stnd[1])

  appTest.handle_close()
  t1.join()

  with open(appTest.get_standings_out(), 'r') as fo:
    with open(appTest.get_path() + 'data/standings_final_scores_gold.txt', 'r') as fg:
      assert_equals(fo.read(), fg.read())


if __name__ == '__main__':
  test()
