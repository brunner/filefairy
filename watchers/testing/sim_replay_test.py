#!/usr/bin/env python

import json
import os
import re
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import slack
from functools import partial
from game_data import GameData

class SimReplay(object):
  """Replays a game log via Slack."""

  def __init__(self, number, path, away, home):
    self.gameData = GameData(away, home)
    self.innings = self.parseInnings(number, path)
    self.parseUpdates()

  def parseInnings(self, number, path):
    with open(os.path.join(path, "log_{0}.txt".format(number))) as f:
      log = f.read()
      sanitized = re.sub("\[%\w\]\t|</?b>", "", log).replace("  ", " ")
      match = re.split("(\w+ of the \w+ -)", sanitized)
      return [x[0] + x[1] for x in zip(match[1::2], match[2::2])]

  # begin deprecated methods
  def storeRunner(self):
    match = re.search("Pinch Runner at (\w+) (.+):", self.line)
    base = self.parseBase(match.groups()[0])
    self.runners[base] = match.groups()[1]

  def storeUnfinishedBatterToBase(self):
    if self.batterToBase != Base.NONE:
      while self.runners[self.batterToBase]:
        self.storeRunnersAdvance()
      self.runners[self.batterToBase] = self.batter

  def handleChangeRunner(self):
    return self.search(
        "Pinch Runner at \w+ .+:",
        "__Pinch runner.",
        self.storeRunner)

  def handleWildPitch(self):
    return self.search(
        "Wild Pitch!",
        "Wild pitch.")

  def handleSingleMissedBase(self):
    return self.search(
        "SINGLE, but batter called out on appeal for missing \w+ base",
        "{0} singles, out on appeal.".format(self.batter),
        self.storeOut)

  def handleDoubleMissedBase(self):
    return self.search(
        "DOUBLE, but batter called out on appeal for missing \w+ base",
        "{0} doubles, out on appeal.".format(self.batter),
        self.storeOut)

  def handleFoulBunt(self):
    return self.search(
        "Bunted foul",
        "__Foul bunt.",
        self.storeStrike)

  def handleSingleAdvancesToSecond(self):
    return self.search(
        "Single.*? batter to second",
        "{0} singles, advances to second".format(self.batter),
        partial(self.storeBatterToBase, Base.SECOND))

  def handleSingleStretchOutAtSecond(self):
    return self.search(
        "SINGLE.*?- OUT at second",
        "{0} singles, out at second".format(self.batter),
        self.storeOut)

  def handleDoubleAdvancesToThird(self):
    return self.search(
        "Double.*? batter to third",
        "{0} doubles, advances to third".format(self.batter),
        partial(self.storeBatterToBase, Base.THIRD))

  def handleDoubleStretchOutAtThird(self):
    return self.search(
        "DOUBLE.*?- OUT at third",
        "{0} doubles, out at third".format(self.batter),
        self.storeOut)

  def handleTripleStretchOutAtHome(self):
    return self.search(
        "TRIPLE.*?- OUT at home",
        "{0} triples, out at home".format(self.batter),
        self.storeOut)

  def handleFieldersChoiceAtHomeOut(self):
    return self.search(
        "fielders choice \d-2",
        "{0} hits into a fielders choice. {1} out at home.".format(
            self.batter, self.runners[Base.THIRD]),
        self.storeOut,
        partial(self.storeBatterToBase, Base.FIRST),
        partial(self.storeRunnerErased, Base.THIRD))

  def handleFieldersChoiceAtHomeSafe(self):
    return self.search(
        "Fielders Choice attempt at home, Runner SAFE",
        "{0} hits into a fielders choice. {1} scores.".format(
            self.batter, self.runners[Base.THIRD]),
        self.storeRun,
        partial(self.storeBatterToBase, Base.FIRST),
        partial(self.storeRunnerErased, Base.THIRD))

  def handleFieldersChoiceAtThird(self):
    return self.search(
        "Fielders Choice at 3rd",
        "{0} hits into a fielders choice. {1} out at third.".format(
            self.batter, self.runners[Base.SECOND]),
        self.storeOut,
        partial(self.storeBatterToBase, Base.FIRST),
        partial(self.storeRunnerErased, Base.SECOND))

  def handleFieldersChoiceAtSecond(self):
    return self.search(
        "Fielders Choice at 2nd",
        "{0} hits into a fielders choice. {1} out at second.".format(
            self.batter, self.runners[Base.FIRST]),
        self.storeOut,
        partial(self.storeBatterToBase, Base.FIRST),
        partial(self.storeRunnerErasedOrBatter, Base.FIRST))

  def handleGroundIntoDoublePlayHomeToFirst(self):
    return self.search(
        "Grounds into double play, \d-2-3 \(",
        "{0} grounds into a double play.".format(self.batter),
        self.storeOut,
        self.storeOut,
        partial(self.storeRunnerErased, Base.THIRD))

  def handleGroundIntoDoublePlaySecondToFirst(self):
    return self.search(
        "Grounds into double play, (?:U3-6|3-6-[14]|4-3-6|U[46]-3|\d-[46]-3) \(",
        "{0} grounds into a double play.".format(self.batter),
        self.storeOut,
        self.storeOut,
        partial(self.storeRunnerErased, Base.FIRST))

  def handleHitByPitch(self):
    return self.search(
        "Hit by Pitch",
        "{0} hit by the pitch.".format(self.batter),
        partial(self.storeBatterToBase, Base.FIRST))

  def handleReachOnError(self):
    return self.search(
        "Reached \w+ [eE]rror|Reaches on Catchers interference",
        "{0} reaches on an error.".format(self.batter),
        partial(self.storeBatterToBase, Base.FIRST))

  def handleBatterScores(self):
    return self.search(
        "{0} scores".format(self.batter),
        "{0} scores.".format(self.batter),
        self.storeRun,
        partial(self.storeRunnerErased, Base.THIRD))

  def handleBatterAdvancesToThird(self):
    return self.search(
        "{0} to third".format(self.batter),
        "{0} to third.".format(self.batter),
        self.storeBatterErased,
        partial(self.storeRunnerToBase, Base.THIRD, Base.SECOND))

  def handleBatterAdvancesToSecond(self):
    return self.search(
        "{0} to second".format(self.batter),
        "{0} to second.".format(self.batter),
        self.storeBatterErased,
        partial(self.storeRunnerToBase, Base.SECOND, Base.FIRST))

  def handleRunnerScoresFromThirdTrailingRunnerSafe(self):
    return self.search(
        "Runner from 3rd tries for Home, SAFE, throw made at trailing runner, SAFE at third",
        "{0} scores. {1} to third.".format(
            self.runners[Base.THIRD], self.runners[Base.SECOND]),
        self.storeRun,
        partial(self.storeRunnerErased, Base.THIRD),
        partial(self.storeRunnerToBase, Base.THIRD, Base.SECOND),
        condition=self.runners[Base.THIRD])

  def handleRunnerScoresFromThirdTrailingRunnerOut(self):
    return self.search(
        "Runner from 3rd tries for Home, SAFE, throw made at trailing runner, OUT at third",
        "{0} scores. {1} out at third.".format(
            self.runners[Base.THIRD], self.runners[Base.SECOND]),
        self.storeRun,
        partial(self.storeRunnerErased, Base.THIRD),
        partial(self.storeRunnerErasedOrBatter, Base.SECOND),
        condition=self.runners[Base.THIRD])

  def handleRunnerScoresFromThirdSafe(self):
    return self.search(
        "{0} scores|Runner from 3rd (?:tries for Home, SAFE|tags up, SCORES)".format(
            self.runners[Base.THIRD]),
        "{0} scores.".format(self.runners[Base.THIRD]),
        self.storeRun,
        partial(self.storeRunnerErasedOrBatter, Base.THIRD),
        condition=self.runners[Base.THIRD])

  def handleRunnerScoresFromThirdOut(self):
    return self.search(
        "Runner from 3rd (?:tries for Home, throw and OUT|tags up, OUT)".format(
            self.runners[Base.THIRD]),
        "{0} out at home.".format(self.runners[Base.THIRD]),
        self.storeOut,
        partial(self.storeRunnerErasedOrBatter, Base.THIRD),
        condition=self.runners[Base.THIRD])

  def handleRunnerScoresFromSecondSafe(self):
    return self.search(
        "{0} scores".format(self.runners[Base.SECOND]),
        "{0} scores.".format(self.runners[Base.SECOND]),
        self.storeRun,
        partial(self.storeRunnerErasedOrBatter, Base.SECOND),
        condition=self.runners[Base.SECOND])

  def handleRunnerScoresFromFirstSafe(self):
    return self.search(
        "{0} scores".format(self.runners[Base.FIRST]),
        "{0} scores.".format(self.runners[Base.FIRST]),
        self.storeRun,
        partial(self.storeRunnerErasedOrBatter, Base.FIRST),
        condition=self.runners[Base.FIRST])

  def handleRunnerAdvancesFromSecondToThirdError(self):
    return self.search(
        "Runner from 2nd tries for 3rd, throw and ERROR! Runner scores".format(
            self.runners[Base.SECOND]),
        "{0} scores on error.".format(self.runners[Base.SECOND]),
        self.storeRun,
        partial(self.storeRunnerErasedOrBatter, Base.SECOND),
        condition=self.runners[Base.SECOND])

  def handleRunnerAdvancesFromSecondToThirdSafe(self):
    return self.search(
        "{0} to third|Runner from 2nd (?:tries for 3rd|tags up), SAFE".format(
            self.runners[Base.SECOND]),
        "{0} to third.".format(self.runners[Base.SECOND]),
        partial(self.storeRunnerToBase, Base.THIRD, Base.SECOND),
        condition=self.runners[Base.SECOND])

  def handleRunnerAdvancesFromSecondToThirdOut(self):
    return self.search(
        "Runner from 2nd (?:tries for 3rd|tags up), OUT".format(
            self.runners[Base.SECOND]),
        "{0} out at third.".format(self.runners[Base.SECOND]),
        self.storeOut,
        partial(self.storeRunnerErasedOrBatter, Base.SECOND),
        condition=self.runners[Base.SECOND])

  def handleRunnerAdvancesFromFirstToThird(self):
    return self.search(
        "{0} to third".format(self.runners[Base.FIRST]),
        "{0} to third.".format(self.runners[Base.FIRST]),
        partial(self.storeRunnerToBase, Base.THIRD, Base.FIRST),
        condition=self.runners[Base.FIRST])

  def handleRunnerAdvancesFromFirstToSecondSafe(self):
    return self.search(
        "{0} to second|Runner from 1st (?:tries for 2nd|tags up), SAFE".format(
            self.runners[Base.FIRST]),
        "{0} to second.".format(self.runners[Base.FIRST]),
        partial(self.storeRunnerToBase, Base.SECOND, Base.FIRST),
        condition=self.runners[Base.FIRST])

  def handleRunnerAdvancesFromFirstToSecondOut(self):
    return self.search(
        "Runner from 1st (?:tries for 2nd|tags up), OUT".format(
            self.runners[Base.FIRST]),
        "{0} out at second.".format(self.runners[Base.FIRST]),
        self.storeOut,
        partial(self.storeRunnerErasedOrBatter, Base.FIRST),
        condition=self.runners[Base.FIRST])

  def handleRunnerStealsHomeSafe(self):
    return self.search(
        "Steal of home, {0} is safe".format(self.runners[Base.THIRD]),
        "{0} steals home.".format(self.runners[Base.THIRD]),
        self.storeRun,
        partial(self.storeRunnerErased, Base.THIRD),
        condition=self.runners[Base.THIRD])

  def handleRunnerStealsHomeOut(self):
    return self.search(
        "Steal of home, {0} is out".format(self.runners[Base.THIRD]),
        "{0} caught stealing home.".format(self.runners[Base.THIRD]),
        self.storeOut,
        partial(self.storeRunnerErased, Base.THIRD),
        condition=self.runners[Base.THIRD])

  def handleRunnerStealsThirdSafe(self):
    return self.search(
        "{0} steals 3rd base".format(self.runners[Base.SECOND]),
        "{0} steals third.".format(self.runners[Base.SECOND]),
        partial(self.storeRunnerToBase, Base.THIRD, Base.SECOND),
        condition=self.runners[Base.SECOND])

  def handleRunnerStealsThirdOut(self):
    return self.search(
        "{0} is caught stealing 3rd base".format(self.runners[Base.SECOND]),
        "{0} caught stealing third.".format(self.runners[Base.SECOND]),
        self.storeOut,
        partial(self.storeRunnerErased, Base.SECOND),
        condition=self.runners[Base.SECOND])

  def handleRunnerStealsSecondSafe(self):
    return self.search(
        "{0} steals 2nd base".format(self.runners[Base.FIRST]),
        "{0} steals second.".format(self.runners[Base.FIRST]),
        partial(self.storeRunnerToBase, Base.SECOND, Base.FIRST),
        condition=self.runners[Base.FIRST])

  def handleRunnerStealsSecondOut(self):
    return self.search(
        "{0} is caught stealing 2nd base".format(self.runners[Base.FIRST]),
        "{0} caught stealing second.".format(self.runners[Base.FIRST]),
        self.storeOut,
        partial(self.storeRunnerErased, Base.FIRST),
        condition=self.runners[Base.FIRST])

  def handleLineIntoDoublePlayThird(self):
    return self.search(
        "Lined into DP, (?:U5|\d-[5]) \(",
        "{0} lines into a double play. {1} out at third.".format(
            self.batter, self.runners[Base.THIRD]),
        self.storeOut,
        self.storeOut,
        partial(self.storeRunnerErased, Base.THIRD),
        condition=self.runners[Base.THIRD])

  def handleLineIntoDoublePlaySecond(self):
    return self.search(
        "Lined into DP, (U[46]|\d-[46]) \(",
        "{0} lines into a double play. {1} out at second.".format(
            self.batter, self.runners[Base.SECOND]),
        self.storeOut,
        self.storeOut,
        partial(self.storeRunnerErased, Base.SECOND),
        condition=self.runners[Base.SECOND])

  def handleLineIntoDoublePlayFirst(self):
    return self.search(
        "Lined into DP, (?:U3|\d-[3]) \(",
        "{0} lines into a double play. {1} out at first.".format(
            self.batter, self.runners[Base.FIRST]),
        self.storeOut,
        self.storeOut,
        partial(self.storeRunnerErased, Base.FIRST),
        condition=self.runners[Base.FIRST])

  def handlePickoffError(self):
    return self.search(
        "Pickoff Throw(?: by Catcher)? to \w+ - Error",
        "Throwing error.")

  def handlePickoffThird(self):
    return self.search(
        "Pickoff Throw(?: by Catcher)? to Third - Out",
        "{0} picked off third.".format(self.runners[Base.THIRD]),
        self.storeOut,
        partial(self.storeRunnerErased, Base.THIRD),
        condition=self.runners[Base.THIRD])

  def handlePickoffSecond(self):
    return self.search(
        "Pickoff Throw(?: by Catcher)? to Second - Out",
        "{0} picked off second.".format(self.runners[Base.SECOND]),
        self.storeOut,
        partial(self.storeRunnerErased, Base.SECOND),
        condition=self.runners[Base.SECOND])

  def handlePickoffFirst(self):
    return self.search(
        "Pickoff Throw(?: by Catcher)? to First - Out",
        "{0} picked off first.".format(self.runners[Base.FIRST]),
        self.storeOut,
        partial(self.storeRunnerErased, Base.FIRST),
        condition=self.runners[Base.FIRST])

  def handleChangeFielder(self):
    return self.search(
        "Now (?:at|in) \w+: (.+)",
        "__New fielder.")

  def handleBatterStrikesOut(self):
    return self.search(
        "Batter strikes out",
        "__Batter strikes out.")

  def handlePassedBall(self):
    return self.search(
        "Passed Ball",
        "__Passed ball.")

  def handleBalk(self):
    return self.search(
        "Balk",
        "__Balk.")

  def handleThrowingError(self):
    return self.search(
        "Throwing error",
        "__Throwing error.")

  def handleErrorOnFoulBall(self):
    return self.search(
        "Error on foul ball",
        "__Error on foul ball.")

  def handleBuntMissed(self):
    return self.search(
        "Bunt missed",
        "__Bunt missed.")

  def handleRainDelay(self):
    return self.search(
        "Rain delay",
        "__Rain delay.")

  def handleGameOver(self):
    return self.search(
        "Game Over",
        "__Game over.")

  def handleFodder(self):
    return self.handleChangeFielder() or \
        self.handleBatterStrikesOut() or \
        self.handlePassedBall() or \
        self.handleBalk() or \
        self.handleThrowingError() or \
        self.handleErrorOnFoulBall() or \
        self.handleBuntMissed() or \
        self.handleRainDelay() or \
        self.handleGameOver()

  def handleUnhandled(self):
    print "{0}: {1}".format(self.gameid, self.line)
    self.chunk.append("__Unhandled {1}".format(self.gameid, self.line))
  # end deprecated methods

  def search(self, pattern, text, *callbacks):
    match = re.search(pattern, text)
    if match:
      for callback in callbacks:
        callback()

    return match

  def storeInning(self, pattern, text):
    match = re.search(pattern, text)
    half, frame = match.groups()
    self.gameData.storeInning(half, frame)

  def storePlayer(self, text):
    pattern = "<a href=\"../players/player_(\d+).html\">([^<]+)</a>"
    match = re.search(pattern, text)

    if not match:
      return 0

    number, full = match.groups()
    first, last = full.rsplit(" ", 1) if full.count(" ") else ("", full)
    self.gameData.storePlayer(number, first, last)

    return number

  def storePitcher(self, pattern, text):
    player = self.storePlayer(text)
    match = re.search(pattern, text)
    self.gameData.storePitcher(player, match.groups()[0])

  def storeBatter(self, pattern, text):
    player = self.storePlayer(text)
    match = re.search(pattern, text)
    self.gameData.storeBatter(player, match.groups()[0])

  def storeStrikeOut(self, pattern, text):
    match = re.search(pattern, text)
    self.gameData.storeStrikeOut("{} strikes out " + match.groups()[0] + ".")

  def storeHomerun(self, pattern, text):
    match = re.search(pattern, text)
    self.gameData.storeHomerun(
        "{} hits a " + match.groups()[0].lower + "homerun.")

  def storeBunt(self, pattern, text):
    match = re.search(pattern, text)
    value, runner = match.groups()

    values = ["first", "second", "third", "home"]
    i = values.index(value) if value in values else -1

    bases = [Base.FIRST, Base.SECOND, Base.THIRD, Base.HOME, Base.NONE]
    base = bases[i] if runner == "safe" else Base.NONE
    previous = bases[i - 1] if i > 0 else Base.NONE
    ticker = "{} " + "{} at {}".format(runner.lower(), value)

    if runner == "safe" and base == Base.FIRST:
      self.gameData.storeBuntSafeAtFirst()
    elif base == Base.FIRST:
      self.gameData.storeBuntOutAtFirst()
    elif runner == "safe":
      self.gameData.storeBuntFieldersChoiceSafe()
      self.gameData.storeRunnerToBase(base, previous, ticker)
    else:
      self.gameData.storeBuntFieldersChoiceOut()
      self.gameData.storeRunnerToBase(base, previous, ticker)

  def storeRunnerScoresTrailing(self, pattern, text):
    match = re.search(pattern, text)
    runner = match.groups()[0]
    base = Base.THIRD if runner == "SAFE" else Base.NONE
    ticker = "{} " + "{} at third".format(runner.lower())
    self.gameData.storeRunnerToBase(Base.HOME, Base.THIRD, "{} scores.")
    self.gameData.storeRunnerToBase(base, Base.SECOND, ticker)

  def handleInningStart(self, text):
    pattern = "(\w+) of the (\d+)\w+ -"
    return self.search(
        pattern,
        text,
        partial(self.storeInning, pattern, text))

  def handleInningEnd(self, text):
    return self.search(
        "\w+ of the \d+\w+ over -",
        text,
        self.gameData.storeAllRunnersErased,
        self.gameData.storeBatterErased)

  def handleChangePitcher(self, text):
    pattern = "Pitching: (\w+) "
    return self.search(
        pattern,
        text,
        partial(self.storePitcher, pattern, text))

  def handleChangeBatter(self, text):
    pattern = "(?:Batting|Pinch Hitting): (\w+) "
    return self.search(
        pattern,
        text,
        partial(self.storeBatter, pattern, text))

  def handleStrike(self, text):
    return self.search(
        "Swinging Strike|Called Strike",
        text,
        self.gameData.storeStrike)

  def handleFoulBall(self, text):
    return self.search(
        "Foul Ball",
        text,
        self.gameData.storeFoul)

  def handleBall(self, text):
    return self.search(
        "Ball",
        text,
        self.gameData.storeBall)

  def handleGroundOut(self, text):
    return self.search(
        "Grounds? out",
        text,
        partial(self.gameData.storeSimpleOut, "{} grounds out."))

  def handleFlyOut(self, text):
    return self.search(
        "Fly out",
        text,
        partial(self.gameData.storeSimpleOut, "{} flies out."))

  def handleStrikeOut(self, text):
    pattern = "Strikes out (\w+)"
    return self.search(
        pattern,
        text,
        partial(self.storeStrikeOut, pattern, text))

  def handleStrikeOutReaches(self, text):
    return self.search(
        "Strikes out .*? reaches first",
        text,
        self.gameData.storeStrikeOutReachesFirst)

  def handleWalk(self, text):
    return self.search(
        "Base on Balls|Intentional Walk|3-\d: Ball",
        text,
        self.gameData.storeWalk)

  def handleSingle(self, text):
    return self.search(
        "SINGLE",
        text,
        self.gameData.storeSingle)

  def handleDouble(self, text):
    return self.search(
        "DOUBLE",
        text,
        self.gameData.storeDouble)

  def handleTriple(self, text):
    return self.search(
        "TRIPLE",
        text,
        self.gameData.storeTriple)

  def handleHomerun(self, text):
    pattern = "(SOLO|2-RUN|3-RUN|GRAND SLAM) HOME RUN"
    return self.search(
        pattern,
        text,
        partial(self.storeHomerun, pattern, text))

  def handleBunt(self, text):
    pattern = "Bunt.*?- play at (\w+), runner (\w+)"
    return self.search(
        pattern,
        text,
        partial(self.storeBunt, pattern, text))

  def handleBuntFlyOut(self, text):
    return self.search(
        "Bunt - Flyout",
        text,
        partial(self.gameData.storeSimpleOut, "{} pops out on a bunt."))

  def handleRunnerScoresTrailing_(self, text):
    pattern = "throw made at trailing runner, (\w+) at third"
    return self.search(
        pattern,
        text,
        partial(self.storeRunnerScoresTrailing, pattern, text))

  def parseUpdates(self):
    for inning in self.innings[0:1]:
      for text in inning.splitlines():
        match = re.match("\d-\d: (.+)", text)
        if match:
          self.handleStrike(text) or \
              self.handleFoulBall(text) or \
              self.handleBall(text) or \
              self.handleGroundOut(text) or \
              self.handleFlyOut(text) or \
              self.handleStrikeOut(text) or \
              self.handleStrikeOutReaches(text) or \
              self.handleWalk(text) or \
              self.handleSingle(text) or \
              self.handleDouble(text) or \
              self.handleTriple(text) or \
              self.handleHomerun(text) or \
              self.handleBunt(text) or \
              self.handleBuntFlyOut(text)

        else:
          self.handleInningStart(text) or \
              self.handleInningEnd(text) or \
              self.handleChangePitcher(text) or \
              self.handleChangeBatter(text)

        print self.gameData.printBox()


path = os.path.expanduser("~") + "/orangeandblueleague/watchers/testing/"
for filename in os.listdir(path):
  match = re.search("log_(1708).txt", filename)
  if match:
    simReplay = SimReplay(match.groups()[0], path, 51, 49)
