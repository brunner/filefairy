#!/usr/bin/env python

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_data import GameData, Base, Half, Qualifier
from utils import assertEquals, assertNotEquals


def testGameData():
  gameData = GameData(35, 34)

  gameData.storePlayer(1, "Sean", "Newcomb")
  gameData.storePitcher(1, "LHP")

  gameData.storePlayer(2, "Jacob", "May")
  gameData.storeBatter(2, "SHB")
  
  inning = ":small_red_triangle: 1"
  away, home = ":whitesox: 0", ":redsox: 0"
  count = "0-0, 0 out"
  bases = ":greydiamond: :greydiamond: :greydiamond:"
  batting = "*Batting:* SHB Jacob May (0-0)"
  pitching = "*Pitching:* LHP Sean Newcomb (0.0 IP, 0 H, 0 R, 0 BB, 0 K)"
  ticker = ""

  expected = createBox(inning, away, home, count,
                       bases, batting, pitching, ticker)
  assertEquals(expected, gameData.printBox())

  gameData.storeBall()
  gameData.storeStrike()
  gameData.storeStrike()
  gameData.storeFoul()
  count = "1-2, 0 out"
  expected = createBox(inning, away, home, count,
                       bases, batting, pitching, ticker)
  assertEquals(expected, gameData.printBox())

  gameData.storeStrikeOut("{} strikes out looking.")
  count = "1-3, 1 out"
  batting = "*Batting:* SHB Jacob May (0-1)"
  pitching = "*Pitching:* LHP Sean Newcomb (0.1 IP, 0 H, 0 R, 0 BB, 1 K)"
  ticker = ":whitesox: _Jacob May strikes out looking._"
  expected = createBox(inning, away, home, count,
                       bases, batting, pitching, ticker)
  assertEquals(expected, gameData.printBox())

  gameData.storePlayer(3, "Jake", "Bauers")
  gameData.storeBatter(3, "LHB")
  count = "0-0, 1 out"
  batting = "*Batting:* LHB Jake Bauers (0-0)"
  expected = createBox(inning, away, home, count,
                       bases, batting, pitching, ticker)
  assertEquals(expected, gameData.printBox())

  gameData.storeSimpleOut("{} grounds out.")
  count = "0-0, 2 out"
  batting = "*Batting:* LHB Jake Bauers (0-1)"
  pitching = "*Pitching:* LHP Sean Newcomb (0.2 IP, 0 H, 0 R, 0 BB, 1 K)"
  ticker = ":whitesox: _Jake Bauers grounds out._"
  expected = createBox(inning, away, home, count,
                       bases, batting, pitching, ticker)
  assertEquals(expected, gameData.printBox())

  gameData.storePlayer(4, "Adam", "Eaton")
  gameData.storeBatter(4, "LHB")
  gameData.storeStrike()
  gameData.storeStrike()
  gameData.storeStrikeOutReachesFirst()
  count = "0-3, 2 out"
  bases = ":greydiamond: :greydiamond: :reddiamond:"
  batting = "*Batting:* LHB Adam Eaton (0-1)"
  pitching = "*Pitching:* LHP Sean Newcomb (0.2 IP, 0 H, 0 R, 0 BB, 2 K)"
  ticker = ":whitesox: _Adam Eaton reaches first._"
  expected = createBox(inning, away, home, count,
                       bases, batting, pitching, ticker)
  assertEquals(expected, gameData.printBox())

  gameData.storePlayer(5, "Matt", "Davidson")
  gameData.storeBatter(5, "RHB")
  gameData.storeBall()
  gameData.storeBall()
  gameData.storeBall()
  gameData.storeWalk()
  gameData.storeRunnerToBase(Base.SECOND, Base.FIRST, "{} to second.")
  count = "4-0, 2 out"
  bases = ":greydiamond: :reddiamond: :reddiamond:"
  batting = "*Batting:* RHB Matt Davidson (0-0)"
  pitching = "*Pitching:* LHP Sean Newcomb (0.2 IP, 0 H, 0 R, 1 BB, 2 K)"
  ticker = ":whitesox: _Matt Davidson walks. Adam Eaton to second._"
  expected = createBox(inning, away, home, count,
                       bases, batting, pitching, ticker)
  assertEquals(expected, gameData.printBox())

  gameData.storePlayer(6, "Viosergy", "Rosa")
  gameData.storeBatter(6, "LHB")
  gameData.storeSingle()
  gameData.storeRunnerToBase(Base.THIRD, Base.SECOND, "{} to third.")
  gameData.storeRunnerToBase(Base.SECOND, Base.FIRST, "{} to second.")
  count = "0-0, 2 out"
  bases = ":reddiamond: :reddiamond: :reddiamond:"
  batting = "*Batting:* LHB Viosergy Rosa (1-1)"
  pitching = "*Pitching:* LHP Sean Newcomb (0.2 IP, 1 H, 0 R, 1 BB, 2 K)"
  ticker = ":whitesox: _Viosergy Rosa singles. Adam Eaton to third. Matt Davidson to second._"
  expected = createBox(inning, away, home, count,
                       bases, batting, pitching, ticker)
  assertEquals(expected, gameData.printBox())

  gameData.storePlayer(7, "Brett", "Austin")
  gameData.storeBatter(7, "SHB")
  gameData.storeDouble()
  gameData.storeRunnerToBase(Base.HOME, Base.THIRD, "{} scores.")
  gameData.storeRunnerToBase(Base.HOME, Base.SECOND, "{} scores.")
  gameData.storeRunnerToBase(Base.THIRD, Base.FIRST, "{} to third.")
  away = ":whitesox: 2"
  count = "0-0, 2 out"
  bases = ":reddiamond: :reddiamond: :greydiamond:"
  batting = "*Batting:* SHB Brett Austin (1-1, 2B, 2 RBI)"
  pitching = "*Pitching:* LHP Sean Newcomb (0.2 IP, 2 H, 2 R, 1 BB, 2 K)"
  ticker = ":whitesox: _Brett Austin doubles. Adam Eaton scores. Matt Davidson scores. Viosergy Rosa to third._"
  expected = createBox(inning, away, home, count,
                       bases, batting, pitching, ticker)
  assertEquals(expected, gameData.printBox())

  gameData.storePlayer(8, "Micah", "Johnson")
  gameData.storeBatter(8, "SHB")
  gameData.storeTriple()
  gameData.storeRunnerToBase(Base.HOME, Base.THIRD, "{} scores.")
  gameData.storeRunnerToBase(Base.HOME, Base.SECOND, "{} scores.")
  away = ":whitesox: 4"
  count = "0-0, 2 out"
  bases = ":reddiamond: :greydiamond: :greydiamond:"
  batting = "*Batting:* SHB Micah Johnson (1-1, 3B, 2 RBI)"
  pitching = "*Pitching:* LHP Sean Newcomb (0.2 IP, 3 H, 4 R, 1 BB, 2 K)"
  ticker = ":whitesox: _Micah Johnson triples. Viosergy Rosa scores. Brett Austin scores._"
  expected = createBox(inning, away, home, count,
                       bases, batting, pitching, ticker)
  assertEquals(expected, gameData.printBox())

  gameData.storePlayer(10, "Carlos", "Sanchez")
  gameData.storeBatter(10, "SHB")
  gameData.storeHomerun("{} hits a 2-run homerun.")
  away = ":whitesox: 6"
  count = "0-0, 2 out"
  bases = ":greydiamond: :greydiamond: :greydiamond:"
  batting = "*Batting:* SHB Carlos Sanchez (1-1, HR, 2 RBI, R)"
  pitching = "*Pitching:* LHP Sean Newcomb (0.2 IP, 4 H, 6 R, 1 BB, 2 K)"
  ticker = ":whitesox: _Carlos Sanchez hits a 2-run homerun. Micah Johnson scores._"
  expected = createBox(inning, away, home, count,
                       bases, batting, pitching, ticker)
  assertEquals(expected, gameData.printBox())

  gameData.storePlayer(11, "Luigi", "Rodriguez")
  gameData.storeBatter(11, "SHB")
  gameData.storeSimpleOut("{} flies out.")
  away = ":whitesox: 6"
  count = "0-0, 3 out"
  bases = ":greydiamond: :greydiamond: :greydiamond:"
  batting = "*Batting:* SHB Luigi Rodriguez (0-1)"
  pitching = "*Pitching:* LHP Sean Newcomb (1.0 IP, 4 H, 6 R, 1 BB, 2 K)"
  ticker = ":whitesox: _Luigi Rodriguez flies out._"
  expected = createBox(inning, away, home, count,
                       bases, batting, pitching, ticker)
  assertEquals(expected, gameData.printBox())

  gameData.storeInning("Bottom", 1)

  gameData.storePlayer(12, "Junior", "Reyes")
  gameData.storePitcher(12, "LHP")

  gameData.storePlayer(13, "Xander", "Bogaerts")
  gameData.storeBatter(13, "RHB")
  
  inning = ":small_red_triangle_down: 1"
  count = "0-0, 0 out"
  batting = "*Batting:* RHB Xander Bogaerts (0-0)"
  pitching = "*Pitching:* LHP Junior Reyes (0.0 IP, 0 H, 0 R, 0 BB, 0 K)"
  ticker = ""

  expected = createBox(inning, away, home, count,
                       bases, batting, pitching, ticker)
  assertEquals(expected, gameData.printBox())

  gameData.storeBuntOutAtFirst()
  count = "0-0, 1 out"
  bases = ":greydiamond: :greydiamond: :greydiamond:"
  batting = "*Batting:* RHB Xander Bogaerts (0-1)"
  pitching = "*Pitching:* LHP Junior Reyes (0.1 IP, 0 H, 0 R, 0 BB, 0 K)"
  ticker = ":redsox: _Xander Bogaerts bunts, out at first._"
  expected = createBox(inning, away, home, count,
                       bases, batting, pitching, ticker)
  assertEquals(expected, gameData.printBox())

  gameData.storePlayer(14, "Blake", "Swihart")
  gameData.storeBatter(14, "SHB")
  gameData.storeBuntSafeAtFirst()
  bases = ":greydiamond: :greydiamond: :reddiamond:"
  batting = "*Batting:* SHB Blake Swihart (1-1)"
  pitching = "*Pitching:* LHP Junior Reyes (0.1 IP, 1 H, 0 R, 0 BB, 0 K)"
  ticker = ":redsox: _Blake Swihart bunts, safe at first._"

  gameData.storePlayer(15, "Connor", "Harrell")
  gameData.storeBatter(15, "RHB")
  gameData.storeBuntOutAtFirst()
  gameData.storeRunnerToBase(Base.SECOND, Base.FIRST, "{} to second.")
  count = "0-0, 2 out"
  bases = ":greydiamond: :reddiamond: :greydiamond:"
  batting = "*Batting:* RHB Connor Harrell (0-0)"
  pitching = "*Pitching:* LHP Junior Reyes (0.2 IP, 1 H, 0 R, 0 BB, 0 K)"
  ticker = ":redsox: _Connor Harrell bunts, out at first. Blake Swihart to second._"

  gameData.storePlayer(16, "Joey", "Gallo")
  gameData.storeBatter(16, "LHB")
  gameData.storeBuntFieldersChoiceSafe()
  gameData.storeRunnerToBase(Base.THIRD, Base.SECOND, "{} to third.")
  bases = ":reddiamond: :greydiamond: :reddiamond:"
  batting = "*Batting:* LHB Joey Gallo (1-1)"
  pitching = "*Pitching:* LHP Junior Reyes (0.2 IP, 2 H, 0 R, 0 BB, 0 K)"
  ticker = ":redsox: _Joey Gallo bunts. Blake Swihart to third._"

  gameData.storePlayer(17, "Javier", "Baez")
  gameData.storeBatter(17, "RHB")
  gameData.storeBuntFieldersChoiceOut()
  gameData.storeRunnerToBase(Base.NONE, Base.FIRST, "{} out at second.")
  gameData.storeAllRunnersErased()
  gameData.storeBatterErased()
  count = "0-0, 3 out"
  bases = ":greydiamond: :greydiamond: :greydiamond:"
  batting = ""
  ticker = ":redsox: _Javier Baez bunts. Joey Gallo out at second._"


def createBox(inning, away, home, count, bases, batting="", pitching="", ticker=""):
  lines = [" :separator: ".join([inning, away, home, count, bases])]

  if batting and pitching:
    lines.append(batting + "\n" + pitching)

  if ticker:
    lines.append(ticker)

  return "\n\n".join(lines)


if __name__ == "__main__":
  testGameData()

  print "Passed."
