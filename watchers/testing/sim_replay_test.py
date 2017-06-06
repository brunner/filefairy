#!/usr/bin/env python

import os
import re
from functools import partial


class Base:
  NONE = 0
  FIRST = 1
  SECOND = 2
  THIRD = 3


class Frame:
  TOP = 1
  BOTTOM = 2


class SimReplay(object):
  """Replays a game log via Slack."""

  def __init__(self, gameid, path):
    self.gameid = gameid
    self.path = path
    self.log = self.getLog()

    self.chunk, self.data = [], []
    self.line = ""

    self.awayruns, self.homeruns = 0, 0
    self.awaypitcher, self.homepitcher, self.batter, self.runner = "", "", "", ""
    self.frame, self.inning = Frame.TOP, 1

    self.balls, self.strikes, self.outs = 0, 0, 0
    self.runners = {Base.FIRST: "", Base.SECOND: "", Base.THIRD: ""}
    self.batterToBase, self.runnerToBase = Base.NONE, Base.NONE

  def getLog(self):
    """Returns the contents of the specified log file."""
    with open(os.path.join(self.path, "log_{0}.txt".format(self.gameid))) as f:
      return f.read()

  def sanitize(self, log):
    """Removes junk characters and HTML tags from log text."""
    return re.sub("\[%\w\]\t|<(?:a[^>]*>|/a>)|</?b>", "", log.replace("  ", " "))

  def parseInnings(self):
    """Splits log text by inning into a list."""
    match = re.split("(\w+ of the \w+ -)", self.sanitize(self.log))
    return [x[0] + x[1] for x in zip(match[1::2], match[2::2])]

  def search(self, regex, text, *args, **kwargs):
    if "condition" not in kwargs or kwargs["condition"]:
      match = re.search(regex, self.line)
      if match:
        if not text.startswith("__"):
          self.chunk.append(text.format(*match.groups()))
        for callback in args:
          callback()
        return match

  def parseBase(self, string):
    if string == "1st":
      return Base.FIRST
    elif string == "2nd":
      return Base.SECOND
    elif string == "3rd":
      return Base.THIRD
    else:
      return Base.NONE

  def parseFrame(self, string):
    if string == "Top":
      return Frame.TOP
    else:
      return Frame.BOTTOM

  def storeChunk(self):
    if self.chunk:
      self.data.append(self.chunk[:])
      del self.chunk[:]

  def storeInningStart(self):
    self.outs = 0
    match = re.search("(\w+) of the (\d+)\w+ -", self.line)
    self.frame = self.parseFrame(match.groups()[0])
    self.inning = int(match.groups()[1])

  def storePitcher(self):
    match = re.search("Pitching: \w+ (.+)", self.line)
    if self.frame == Frame.TOP:
      self.homepitcher = match.groups()[0]
    else:
      self.awaypitcher = match.groups()[0]

  def storeBatter(self):
    self.balls, self.strikes = 0, 0
    self.batterToBase, self.runnerToBase = Base.NONE, Base.NONE
    match = re.search("(?:Batting|Pinch Hitting): \w+ (.+)", self.line)
    self.batter = match.groups()[0]

  def storeBatterToBase(self, base):
    if self.runners[base]:
      self.batterToBase = base
    else:
      self.runners[base] = self.batter

  def storeBatterErased(self):
    self.batterToBase = Base.NONE

  def storeRunner(self):
    match = re.search("Pinch Runner at (\w+) (.+):", self.line)
    base = self.parseBase(match.groups()[0])
    self.runners[base] = match.groups()[1]

  def storeRunnerToBase(self, base, previous):
    if self.runners[base]:
      self.runnerToBase = base
      self.runner = self.runners[previous]
      self.runners[previous] = ""
    else:
      self.runners[base] = self.runners[previous]
      if self.batterToBase == previous:
        self.runners[previous] = self.batter
        self.batterToBase = Base.NONE
      elif self.runnerToBase == previous:
        self.runners[previous] = self.runner
        self.runner = ""
      else:
        self.runners[previous] = ""

  def storeRunnerErased(self, base):
    self.runners[base] = ""

  def storeRunnerErasedOrBatter(self, base):
    if self.batterToBase == base:
      self.runners[base] = self.batter
      self.batterToBase = Base.NONE
    else:
      self.runners[base] = ""

  def storeRunnersAllErased(self):
    self.runners[Base.FIRST] = ""
    self.runners[Base.SECOND] = ""
    self.runners[Base.THIRD] = ""

  def storeRunnersAdvance(self):
    if self.runners[Base.THIRD]:
      self.chunk.append("{0} scores.".format(self.runners[Base.THIRD]))
    self.runners[Base.THIRD] = self.runners[Base.SECOND]
    self.runners[Base.SECOND] = self.runners[Base.FIRST]
    self.runners[Base.FIRST] = ""

  def storeUnfinishedBatterToBase(self):
    if self.batterToBase != Base.NONE:
      while self.runners[self.batterToBase]:
        self.storeRunnersAdvance()
      self.runners[self.batterToBase] = self.batter


  def storeBall(self):
    self.balls = self.balls + 1

  def storeStrike(self):
    self.strikes = self.strikes + 1

  def storeFoul(self):
    self.strikes = max(2, self.strikes + 1)

  def storeOut(self):
    self.outs = self.outs + 1

  def storeRun(self):
    if self.frame == Frame.TOP:
      self.awayruns = self.awayruns + 1
    else:
      self.homeruns = self.homeruns + 1

  def handleInningStart(self):
    return self.search(
        "\w+ of the \d+\w+ -",
        "__Inning start.",
        self.storeInningStart)

  def handleInningEnd(self):
    return self.search(
        "\w+ of the \d+\w+ over -",
        "__Inning end.",
        self.storeRunnersAllErased,
        self.storeChunk)

  def handleChangePitcher(self):
    return self.search(
        "Pitching: \w+ .+",
        "__New pitcher.",
        self.storePitcher)

  def handleChangeBatter(self):
    return self.search(
        "(?:Batting|Pinch Hitting): \w+ .+",
        "__New batter. ({0},{1},{2})".format(self.runners[Base.FIRST], self.runners[Base.SECOND], self.runners[Base.THIRD]),
        self.storeUnfinishedBatterToBase,
        self.storeBatter)

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

  def handleStrike(self):
    return self.search(
        "Swinging Strike|Called Strike",
        "__Strike {0}-{1}.".format(self.balls, self.strikes + 1),
        self.storeStrike)

  def handleFoulBall(self):
    return self.search(
        "Foul Ball",
        "__Foul ball.",
        self.storeFoul)

  def handleFoulBunt(self):
    return self.search(
        "Bunted foul",
        "__Foul bunt.",
        self.storeStrike)

  def handleWalk(self):
    return self.search(
        "Base on Balls",
        "{0} walks.".format(self.batter),
        self.storeBall,
        partial(self.storeBatterToBase, Base.FIRST))

  def handleIntentionalWalk(self):
    return self.search(
        "Intentional Walk",
        "{0} walks intentionally.".format(self.batter),
        partial(self.storeBatterToBase, Base.FIRST))

  def handleRareWalk(self):
    return self.search(
        "Ball",
        "{0} walks.".format(self.batter),
        self.storeBall,
        partial(self.storeBatterToBase, Base.FIRST),
        condition=(self.balls == 3))

  def handleBall(self):
    return self.search(
        "Ball",
        "__Ball {0}-{1}.".format(self.balls + 1, self.strikes),
        self.storeBall)

  def handleGroundOut(self):
    return self.search(
        "Grounds? out",
        "{0} grounds out.".format(self.batter),
        self.storeOut)

  def handleFlyOut(self):
    return self.search(
        "Fly out",
        "{0} flies out.".format(self.batter),
        self.storeOut)

  def handleStrikeOutReachesFirst(self):
    return self.search(
        "Strikes out .*? reaches first",
        "{0} reaches first.".format(self.batter, self.line.lower()),
        self.storeStrike,
        partial(self.storeBatterToBase, Base.FIRST))

  def handleStrikeOut(self):
    return self.search(
        "Strikes out",
        "{0} {1}.".format(self.batter, self.line.lower()),
        self.storeStrike,
        self.storeOut)

  def handleBuntRunnerOutAtHome(self):
    return self.search(
        "Bunt.*?- play at home, runner OUT",
        "{0} bunts into a fielders choice. {1} out at home.".format(
            self.batter, self.runners[Base.THIRD]),
        self.storeOut,
        partial(self.storeRunnerErased, Base.THIRD),
        partial(self.storeBatterToBase, Base.FIRST))

  def handleBuntRunnerSafeAtHome(self):
    return self.search(
        "Bunt.*?- play at home, runner safe",
        "{0} bunts. {1} safe at home.".format(
            self.batter, self.runners[Base.THIRD]),
        self.storeRun,
        partial(self.storeBatterToBase, Base.FIRST))

  def handleBuntRunnerOutAtThird(self):
    return self.search(
        "Bunt.*?- play at third, runner OUT",
        "{0} bunts into a fielders choice. {1} out at third.".format(
            self.batter, self.runners[Base.SECOND]),
        self.storeOut,
        partial(self.storeRunnerErased, Base.SECOND),
        partial(self.storeBatterToBase, Base.FIRST))

  def handleBuntRunnerSafeAtThird(self):
    return self.search(
        "Bunt.*?- play at third, runner safe",
        "{0} bunts. {1} safe at third.".format(
            self.batter, self.runners[Base.SECOND]),
        partial(self.storeRunnerToBase, Base.THIRD, Base.SECOND),
        partial(self.storeBatterToBase, Base.FIRST))

  def handleBuntRunnerOutAtSecond(self):
    return self.search(
        "Bunt.*?- play at second, runner OUT",
        "{0} bunts into a fielders choice. {1} out at second.".format(
            self.batter, self.runners[Base.FIRST]),
        self.storeOut,
        partial(self.storeRunnerErased, Base.FIRST),
        partial(self.storeBatterToBase, Base.FIRST))

  def handleBuntRunnerSafeAtSecond(self):
    return self.search(
        "Bunt.*?- play at second, runner safe",
        "{0} bunts. {1} safe at second.".format(
            self.batter, self.runners[Base.FIRST]),
        partial(self.storeRunnerToBase, Base.SECOND, Base.FIRST),
        partial(self.storeBatterToBase, Base.FIRST))

  def handleBuntBatterPlayOut(self):
    return self.search(
        "Bunt.*?- play at first, batter OUT",
        "{0} bunts, out at first.".format(self.batter),
        self.storeOut)

  def handleBuntBatterFlyOut(self):
    return self.search(
        "Bunt - Flyout",
        "{0} pops out on a bunt.".format(self.batter),
        self.storeOut)

  def handleBuntBatterSafe(self):
    return self.search(
        "Bunt.*?- play at first, batter safe",
        "{0} bunts, safe at first.".format(self.batter),
        partial(self.storeBatterToBase, Base.FIRST))

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

  def handleSingle(self):
    return self.search(
        "SINGLE",
        "{0} singles.".format(self.batter),
        partial(self.storeBatterToBase, Base.FIRST))

  def handleDouble(self):
    return self.search(
        "DOUBLE",
        "{0} doubles.".format(self.batter),
        partial(self.storeBatterToBase, Base.SECOND))

  def handleTriple(self):
    return self.search(
        "TRIPLE",
        "{0} triples.".format(self.batter),
        partial(self.storeBatterToBase, Base.THIRD))

  def handleOneRunHomerun(self):
    return self.search(
        "SOLO HOME RUN",
        "{0} hits a solo homerun.".format(self.batter),
        self.storeRun)

  def handleTwoRunHomerun(self):
    return self.search(
        "2-RUN HOME RUN",
        "{0} hits a 2-run homerun.".format(self.batter),
        self.storeRun,
        self.storeRun,
        self.storeRunnersAdvance,
        self.storeRunnersAdvance,
        self.storeRunnersAdvance)

  def handleThreeRunHomerun(self):
    return self.search(
        "3-RUN HOME RUN",
        "{0} hits a 3-run homerun.".format(self.batter),
        self.storeRun,
        self.storeRun,
        self.storeRun,
        self.storeRunnersAdvance,
        self.storeRunnersAdvance,
        self.storeRunnersAdvance)

  def handleGrandSlamHomerun(self):
    return self.search(
        "GRAND SLAM HOME RUN",
        "{0} hits a grand slam.".format(self.batter),
        self.storeRun,
        self.storeRun,
        self.storeRun,
        self.storeRun,
        self.storeRunnersAdvance,
        self.storeRunnersAdvance,
        self.storeRunnersAdvance)

  def handlePitch(self):
    match = re.match("\d-\d: (.+)", self.line)
    if match:
      self.storeChunk()

      self.line = match.groups()[0]
      return self.handleStrike() or \
          self.handleFoulBall() or \
          self.handleFoulBunt() or \
          self.handleWalk() or \
          self.handleIntentionalWalk() or \
          self.handleRareWalk() or \
          self.handleBall() or \
          self.handleWildPitch() or \
          self.handleGroundOut() or \
          self.handleFlyOut() or \
          self.handleStrikeOutReachesFirst() or \
          self.handleStrikeOut() or \
          self.handleBuntRunnerOutAtHome() or \
          self.handleBuntRunnerSafeAtHome() or \
          self.handleBuntRunnerOutAtThird() or \
          self.handleBuntRunnerSafeAtThird() or \
          self.handleBuntRunnerOutAtSecond() or \
          self.handleBuntRunnerSafeAtSecond() or \
          self.handleBuntBatterPlayOut() or \
          self.handleBuntBatterFlyOut() or \
          self.handleBuntBatterSafe() or \
          self.handleSingleAdvancesToSecond() or \
          self.handleSingleMissedBase() or \
          self.handleSingleStretchOutAtSecond() or \
          self.handleDoubleAdvancesToThird() or \
          self.handleDoubleMissedBase() or \
          self.handleDoubleStretchOutAtThird() or \
          self.handleTripleStretchOutAtHome() or \
          self.handleFieldersChoiceAtHomeOut() or \
          self.handleFieldersChoiceAtHomeSafe() or \
          self.handleFieldersChoiceAtThird() or \
          self.handleFieldersChoiceAtSecond() or \
          self.handleGroundIntoDoublePlayHomeToFirst() or \
          self.handleGroundIntoDoublePlaySecondToFirst() or \
          self.handleHitByPitch() or \
          self.handleReachOnError() or \
          self.handleSingle() or \
          self.handleDouble() or \
          self.handleTriple() or \
          self.handleOneRunHomerun() or \
          self.handleTwoRunHomerun() or \
          self.handleThreeRunHomerun() or \
          self.handleGrandSlamHomerun()

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
        "{0} scores. {1} to third.".format(self.runners[Base.THIRD], self.runners[Base.SECOND]),
        self.storeRun,
        partial(self.storeRunnerErased, Base.THIRD),
        partial(self.storeRunnerToBase, Base.THIRD, Base.SECOND),
        condition=self.runners[Base.THIRD])

  def handleRunnerScoresFromThirdTrailingRunnerOut(self):
    return self.search(
        "Runner from 3rd tries for Home, SAFE, throw made at trailing runner, OUT at third",
        "{0} scores. {1} out at third.".format(self.runners[Base.THIRD], self.runners[Base.SECOND]),
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
        "{0} lines into a double play. {1} out at third.".format(self.batter, self.runners[Base.THIRD]),
        self.storeOut,
        self.storeOut,
        partial(self.storeRunnerErased, Base.THIRD),
        condition=self.runners[Base.THIRD])

  def handleLineIntoDoublePlaySecond(self):
    return self.search(
        "Lined into DP, (U[46]|\d-[46]) \(",
        "{0} lines into a double play. {1} out at second.".format(self.batter, self.runners[Base.SECOND]),
        self.storeOut,
        self.storeOut,
        partial(self.storeRunnerErased, Base.SECOND),
        condition=self.runners[Base.SECOND])

  def handleLineIntoDoublePlayFirst(self):
    return self.search(
        "Lined into DP, (?:U3|\d-[3]) \(",
        "{0} lines into a double play. {1} out at first.".format(self.batter, self.runners[Base.FIRST]),
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

  def start(self):
    innings = self.parseInnings()
    for inning in innings:
      for line in inning.splitlines():
        self.line = line
        self.handleInningStart() or \
            self.handleInningEnd() or \
            self.handleChangePitcher() or \
            self.handleChangeBatter() or \
            self.handleChangeRunner() or \
            self.handleWildPitch() or \
            self.handleSingleMissedBase() or \
            self.handleDoubleMissedBase() or \
            self.handlePitch() or \
            self.handleBatterScores() or \
            self.handleBatterAdvancesToThird() or \
            self.handleBatterAdvancesToSecond() or \
            self.handleRunnerScoresFromThirdTrailingRunnerSafe() or \
            self.handleRunnerScoresFromThirdTrailingRunnerOut() or \
            self.handleRunnerScoresFromThirdSafe() or \
            self.handleRunnerScoresFromThirdOut() or \
            self.handleRunnerScoresFromSecondSafe() or \
            self.handleRunnerScoresFromFirstSafe() or \
            self.handleRunnerAdvancesFromSecondToThirdError() or \
            self.handleRunnerAdvancesFromSecondToThirdSafe() or \
            self.handleRunnerAdvancesFromSecondToThirdOut() or \
            self.handleRunnerAdvancesFromFirstToThird() or \
            self.handleRunnerAdvancesFromFirstToSecondSafe() or \
            self.handleRunnerAdvancesFromFirstToSecondOut() or \
            self.handleRunnerStealsHomeSafe() or \
            self.handleRunnerStealsHomeOut() or \
            self.handleRunnerStealsThirdSafe() or \
            self.handleRunnerStealsThirdOut() or \
            self.handleRunnerStealsSecondSafe() or \
            self.handleRunnerStealsSecondOut() or \
            self.handleLineIntoDoublePlayThird() or \
            self.handleLineIntoDoublePlaySecond() or \
            self.handleLineIntoDoublePlayFirst() or \
            self.handlePickoffError() or \
            self.handlePickoffThird() or \
            self.handlePickoffSecond() or \
            self.handlePickoffFirst() or \
            self.handleFodder() or \
            self.handleUnhandled()

    # for d in self.data:
    #   print ", ".join(d)


path = os.path.expanduser("~") + "/.Out of the Park Developments/OOTP Baseball 17/custdata/saved_games/orangeandblue.lg/news/txt/leagues/"
for filename in os.listdir(path):
  match = re.search("log_(\d+).txt", filename)
  if match:
    simReplay = SimReplay(match.groups()[0], path)
    simReplay.start()