#!/usr/bin/env python

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_data import GameData, Half, Qualifier
from utils import assertEquals, assertNotEquals


def testGameData():
  gameData = GameData(35, 34)

  inning = ":small_red_triangle: 1"
  away, home = ":whitesox: 0", ":redsox: 0"
  count = "0-0, 0 out"
  bases = ":greydiamond: :greydiamond: :greydiamond:"
  batting = "*Batting:* SHB Jacob May (0-0)"
  pitching = "*Pitching:* LHP Sean Newcomb (0.0 IP, 0 H, 0 R, 0 BB, 0 K)"
  ticker = ""

  expected = createBox(inning, away, home, count, bases)
  assertEquals(expected, gameData.printBox())

  gameData.addPlayer(1, "Sean", "Newcomb", Qualifier.PITCHING, "LHP")
  gameData.setPitcher(1)
  assertEquals(expected, gameData.printBox())

  gameData.addPlayer(2, "Jacob", "May", Qualifier.BATTING, "SHB")
  gameData.setBatter(2)
  expected = createBox(inning, away, home, count, bases, batting, pitching)
  assertEquals(expected, gameData.printBox())

  gameData.storeBall()
  gameData.storeStrike()
  gameData.storeStrike()
  gameData.storeFoul()
  count = "1-2, 0 out"
  expected = createBox(inning, away, home, count, bases, batting, pitching)
  assertEquals(expected, gameData.printBox())

  gameData.storeStrikeOut("{} strikes out looking.")
  count = "1-3, 1 out"
  batting = "*Batting:* SHB Jacob May (0-1)"
  pitching = "*Pitching:* LHP Sean Newcomb (0.1 IP, 0 H, 0 R, 0 BB, 1 K)"
  ticker = ":whitesox: _Jacob May strikes out looking._"
  expected = createBox(inning, away, home, count,
                       bases, batting, pitching, ticker)
  assertEquals(expected, gameData.printBox())

  gameData.addPlayer(3, "Jake", "Bauers", Qualifier.BATTING, "LHB")
  gameData.setBatter(3)
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
