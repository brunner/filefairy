#!/usr/bin/env python

import re
from functools import partial

# TODO:
# play at home in case of a sacrifice bunt or fielders choice
# double play with 0 outs and an out made at home or third
# line into double play with 0 outs and more than one player on base
# triple play

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

  def __init__(self, gameid):
    self.gameid = gameid
    self.log = self.getLog()

    self.chunk, self.data = [], []
    self.line = ""

    self.awayruns, self.homeruns = 0, 0
    self.awaypitcher, self.homepitcher, self.batter = "", "", ""
    self.frame, self.inning = Frame.TOP, 1

    self.clearLine()
    self.parseLog()

  def getLog(self):
    """Returns the contents of the specified log file."""
    with open("log_{0}.txt".format(self.gameid)) as f:
      return f.read()

  def clearLine(self):
    self.balls, self.strikes, self.outs = 0, 0, 0
    self.runners = {Base.FIRST: "", Base.SECOND: "", Base.THIRD: ""}
    self.toBase = Base.NONE

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

  def basesCleared(self):
    return " ".join([
        "{0} scores.".format(self.runners[base]) for base in [
            Base.THIRD, Base.SECOND, Base.FIRST]
        if self.runners[base]])

  def storeChunk(self):
    if self.chunk:
      frame = "Top" if self.frame == Frame.TOP else "Bot"
      self.chunk.insert(0, "{0} {1} - Home {2} - Away {3} - {4} out".format(
        frame, self.inning, self.homeruns, self.awayruns, self.outs))
      self.data.append(self.chunk[:])
      del self.chunk[:]

  def storeInningStart(self):
    match = re.search("(\w+) of the (\d+)\w+ -", self.line)
    self.frame = self.parseFrame(match.groups()[0])
    self.inning = int(match.groups()[1])

  def storePitcher(self):
    match = re.search("Pitching: \w+ (.+)", self.line)
    self.pitcher = match.groups()[0]
    self.chunk.append("Pitching: {0}".format(match.groups()[0]))

  def storeBatter(self):
    self.balls, self.strikes = 0, 0
    match = re.search("(?:Batting|Pinch Hitting): \w+ (.+)", self.line)
    self.batter = match.groups()[0]

  def storeBatterToBase(self, base):
    if self.runners[base]:
      self.toBase = base
    else:
      self.runners[base] = self.batter

  def storeRunner(self):
    match = re.search("Pinch Runner at (\w+) (.+):", self.line)
    base = self.parseBase(match.groups()[0])
    self.runners[base] = match.groups()[1]

  def storeRunnerToBase(self, base, previous):
    self.runners[base] = self.runners[previous]
    if self.toBase == previous:
      self.runners[previous] = self.batter
    else:
      self.runners[previous] = ""

  def storeRunnerErased(self, base):
    self.runners[base] = ""

  def storeRunnerErasedOrBatter(self, base):
    if self.toBase == base:
      self.runners[base] = self.batter
      self.toBase = Base.NONE
    else:
      self.runners[base] = ""

  def storeRunnersAllErased(self):
    self.runners[Base.FIRST] = ""
    self.runners[Base.SECOND] = ""
    self.runners[Base.THIRD] = ""

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
        self.storeInningStart,
        self.clearLine)

  def handleInningEnd(self):
    return self.search(
        "\w+ of the \d+\w+ over -",
        "__Inning end.",
        self.storeChunk)

  def handleChangePitcher(self):
    return self.search(
        "Pitching: \w+ .+",
        "__New pitcher.",
        self.storePitcher)

  def handleChangeBatter(self):
    return self.search(
        "(?:Batting|Pinch Hitting): \w+ .+",
        "__New batter.",
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

  def handleStrike(self):
    return self.search(
        "Swinging Strike|Called Strike",
        "__Strike.",
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
        "__Ball.",
        self.storeBall)

  def handleGroundOut(self):
    return self.search(
        "Ground out",
        "{0} grounds out.".format(self.batter),
        self.storeOut)

  def handleFlyOut(self):
    return self.search(
        "Fly out",
        "{0} flies out.".format(self.batter),
        self.storeOut)

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
        partial(self.storeBatterToBase, Base.FIRST),
        partial(self.storeRunnerErased, Base.THIRD))

  def handleBuntRunnerSafeAtHome(self):
    return self.search(
        "Bunt.*?- play at home, runner safe",
        "{0} bunts. {1} safe at home.".format(
            self.batter, self.runners[Base.THIRD]),
        partial(self.storeBatterToBase, Base.FIRST),
        self.storeRun)

  def handleBuntRunnerOutAtThird(self):
    return self.search(
        "Bunt.*?- play at third, runner OUT",
        "{0} bunts into a fielders choice. {1} out at third.".format(
            self.batter, self.runners[Base.SECOND]),
        self.storeOut,
        partial(self.storeBatterToBase, Base.FIRST),
        partial(self.storeRunnerErased, Base.SECOND))

  def handleBuntRunnerSafeAtThird(self):
    return self.search(
        "Bunt.*?- play at third, runner safe",
        "{0} bunts. {1} safe at third.".format(
            self.batter, self.runners[Base.SECOND]),
        partial(self.storeBatterToBase, Base.FIRST),
        partial(self.storeRunnerToBase, Base.THIRD, Base.SECOND))

  def handleBuntRunnerOutAtSecond(self):
    return self.search(
        "Bunt.*?- play at second, runner OUT",
        "{0} bunts into a fielders choice. {1} out at second.".format(
            self.batter, self.runners[Base.FIRST]),
        self.storeOut,
        partial(self.storeBatterToBase, Base.FIRST),
        partial(self.storeRunnerErased, Base.FIRST))

  def handleBuntRunnerSafeAtSecond(self):
    return self.search(
        "Bunt.*?- play at second, runner safe",
        "{0} bunts. {1} safe at second.".format(
            self.batter, self.runners[Base.FIRST]),
        partial(self.storeBatterToBase, Base.FIRST),
        partial(self.storeRunnerToBase, Base.SECOND, Base.FIRST))

  def handleBuntBatterOut(self):
    return self.search(
        "Bunt.*?- play at first, batter OUT",
        "{0} bunts, out at first.".format(self.batter),
        self.storeOut)

  def handleBuntBatterSafe(self):
    return self.search(
        "Bunt.*?- play at first, batter safe",
        "{0} bunts, safe at first.".format(self.batter),
        partial(self.storeBatterToBase, Base.FIRST))

  def handleSingleStretchOutAtSecond(self):
    return self.search(
        "SINGLE.*?- OUT at second",
        "{0} singles, out at second".format(self.batter),
        self.storeOut)

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

  def handleFieldersChoiceAtHome(self):
    return self.search(
        "Fielders Choice at home",
        "{0} hits into a fielders choice. {1} out at home.".format(
            self.batter, self.runners[Base.THIRD]),
        self.storeOut,
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

  def handleTriplePlay(self):
    return self.search(
        "triple play",
        "{0} hits into a triple play.",
        self.storeOut,
        self.storeOut,
        self.storeOut,
        self.storeRunnersAllErased)

  def handleGroundIntoDoublePlay(self):
    return self.search(
        "Grounds into double play",
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
        "Reached on error|Reaches on Catchers interference",
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
        "{0} hits a 2-run homerun. {1}".format(self.batter,
                                               self.basesCleared()),
        self.storeRun,
        self.storeRun,
        self.storeRunnersAllErased)

  def handleThreeRunHomerun(self):
    return self.search(
        "3-RUN HOME RUN",
        "{0} hits a 3-run homerun. {1}".format(self.batter,
                                               self.basesCleared()),
        self.storeRun,
        self.storeRun,
        self.storeRun,
        self.storeRunnersAllErased)

  def handleGrandSlamHomerun(self):
    return self.search(
        "GRAND SLAM HOME RUN",
        "{0} hits a grand slam. {1}".format(self.batter, self.basesCleared()),
        self.storeRun,
        self.storeRun,
        self.storeRun,
        self.storeRunnersAllErased)

  def handlePitch(self):
    match = re.match("\d-\d: (.+)", self.line)
    if match:
      self.storeChunk()

      self.line = match.groups()[0]
      return self.handleStrike() or \
          self.handleFoulBall() or \
          self.handleFoulBunt() or \
          self.handleWalk() or \
          self.handleRareWalk() or \
          self.handleBall() or \
          self.handleWildPitch() or \
          self.handleGroundOut() or \
          self.handleFlyOut() or \
          self.handleStrikeOut() or \
          self.handleBuntRunnerOutAtHome() or \
          self.handleBuntRunnerSafeAtHome() or \
          self.handleBuntRunnerOutAtThird() or \
          self.handleBuntRunnerSafeAtThird() or \
          self.handleBuntRunnerOutAtSecond() or \
          self.handleBuntRunnerSafeAtSecond() or \
          self.handleBuntBatterOut() or \
          self.handleBuntBatterSafe() or \
          self.handleSingleStretchOutAtSecond() or \
          self.handleDoubleStretchOutAtThird() or \
          self.handleTripleStretchOutAtHome() or \
          self.handleFieldersChoiceAtHome() or \
          self.handleFieldersChoiceAtThird() or \
          self.handleFieldersChoiceAtSecond() or \
          self.handleTriplePlay() or \
          self.handleGroundIntoDoublePlay() or \
          self.handleHitByPitch() or \
          self.handleReachOnError() or \
          self.handleSingle() or \
          self.handleDouble() or \
          self.handleTriple() or \
          self.handleOneRunHomerun() or \
          self.handleTwoRunHomerun() or \
          self.handleThreeRunHomerun() or \
          self.handleGrandSlamHomerun()

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
        "Runner from 3rd (?:tries for Hometags up), OUT".format(
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

  def handleLineIntoDoublePlay(self):
    return self.search(
        "Lined into DP",
        "{0} lines into a double play.".format(self.batter),
        self.storeOut,
        self.storeRunnersAllErased)

  def handlePickoffError(self):
    return self.search(
        "Pickoff Throw to \w+ - Error",
        "Throwing error.")

  def handlePickoffThird(self):
    return self.search(
        "Pickoff Throw to Third - Out",
        "{0} picked off third.".format(self.runners[Base.THIRD]),
        self.storeOut,
        partial(self.storeRunnerErased, Base.THIRD),
        condition=self.runners[Base.THIRD])

  def handlePickoffSecond(self):
    return self.search(
        "Pickoff Throw to Second - Out",
        "{0} picked off second.".format(self.runners[Base.SECOND]),
        self.storeOut,
        partial(self.storeRunnerErased, Base.SECOND),
        condition=self.runners[Base.SECOND])

  def handlePickoffFirst(self):
    return self.search(
        "Pickoff Throw to First - Out",
        "{0} picked off first.".format(self.runners[Base.FIRST]),
        self.storeOut,
        partial(self.storeRunnerErased, Base.FIRST),
        condition=self.runners[Base.FIRST])

  def handleChangeFielder(self):
    return self.search(
        "Now (?:at|in) \w+: (.+)",
        "__New fielder.")

  def handleBatterStrikesOut(self):
    return self.search("Batter strikes out", "EVENT_BATTER_STRIKES_OUT")

  def handleFodder(self):
    return self.handleChangeFielder() or \
        self.handleBatterStrikesOut()

  def handleUnhandled(self):
    print self.line
    self.chunk.append("UNHANDLED: {0}".format(self.line))

  def parseLog(self):
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
            self.handlePitch() or \
            self.handleRunnerScoresFromThirdSafe() or \
            self.handleRunnerScoresFromThirdOut() or \
            self.handleRunnerScoresFromSecondSafe() or \
            self.handleRunnerScoresFromFirstSafe() or \
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
            self.handleLineIntoDoublePlay() or \
            self.handlePickoffError() or \
            self.handlePickoffThird() or \
            self.handlePickoffSecond() or \
            self.handlePickoffFirst() or \
            self.handleFodder() or \
            self.handleUnhandled()

    for d in self.data:
      print ", ".join(d)

simReplay = SimReplay(693)