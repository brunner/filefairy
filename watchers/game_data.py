#!/usr/bin/env python

import slack


class Base:
  NONE = 0
  FIRST = 1
  SECOND = 2
  THIRD = 3
  HOME = 4

BASES = [Base.FIRST, Base.SECOND, Base.THIRD]


class Half:
  AWAY = 1
  HOME = 2


class Qualifier:
  BATTING = "Batting"
  PITCHING = "Pitching"


class Stats:
  BATTING = ["H", "AB", "2B", "3B", "HR", "RBI", "BB", "R"]
  PITCHING = ["IP", "O", "H", "R", "BB", "K"]


class Key:
  BATTER = "batter"
  BATS = "bats"
  BATTING = "batting"
  CURRENT = "current"
  FIRST = "first"
  FUTURE = "future"
  LAST = "last"
  NUMBER = "number"
  PITCHER = "pitcher"
  PITCHING = "pitching"
  RUNNER = "runner"
  RUNS = "runs"
  THROWS = "throws"


class GameData(object):

  def __init__(self, away, home):
    self.teams = {}
    self.teams[Half.AWAY] = {Key.NUMBER: away, Key.PITCHER: 0, Key.RUNS: 0}
    self.teams[Half.HOME] = {Key.NUMBER: home, Key.PITCHER: 0, Key.RUNS: 0}
    self.players = {}
    self.ticker = ""

    self.setInning("Top", 1)

  def printInning(self):
    arrow = ":small_red_triangle:" if self.half == Half.AWAY \
        else ":small_red_triangle_down:"
    return "{} {}".format(arrow, self.frame)

  def printTeamRuns(self, half):
    team = self.teams[half]
    return "{} {}".format(slack.getEmoji(team[Key.NUMBER]), team[Key.RUNS])

  def printCount(self):
    return "{}-{}, {} out".format(self.balls, self.strikes, self.outs)

  def printBases(self):
    colors = map(lambda x: "red" if self.bases[x][Key.CURRENT][Key.RUNNER]
                 else "grey", reversed(BASES))
    diamonds = map(lambda x: ":{}diamond:".format(x), colors)
    return "{} {} {}".format(*diamonds)

  def printPlayerName(self, number, short=False):
    if number not in self.players:
      return ""

    player = self.players[number]
    return player["last"] if short else player["first"] + " " + player["last"]

  def printBatterBats(self, number):
    if number not in self.players:
      return ""

    return self.players[number]["bats"]

  def printBatterStats(self, number):
    if number not in self.players:
      return ""

    stats = self.players[number]["batting"]
    sb = ""

    for stat in Stats.BATTING:
      if stat == "H":
        sb = sb + "{}-".format(stats["H"])
      elif stat == "AB":
        sb = sb + str(stats["AB"])
      elif stats[stat]:
        number = str(stats[stat]) + " " if stats[stat] > 1 else ""
        sb = sb + ", {}{}".format(number, stat)

    return "(" + sb + ")"

  def printPitcherThrows(self, number):
    if number not in self.players:
      return ""

    return self.players[number]["throws"]

  def printPitcherStats(self, number):
    if number not in self.players:
      return ""

    stats = self.players[number]["pitching"]
    sb = ""

    for stat in Stats.PITCHING:
      if stat == "IP":
        sb = sb + "{}.".format(stats["IP"])
      elif stat == "O":
        sb = sb + "{} IP".format(stats["O"])
      else:
        sb = sb + ", {} {}".format(stats[stat], stat)

    return "(" + sb + ")"

  def printBox(self):
    lines = []

    inning = self.printInning()
    away = self.printTeamRuns(Half.AWAY)
    home = self.printTeamRuns(Half.HOME)
    count = self.printCount()
    bases = self.printBases()
    lines.append(" :separator: ".join([inning, away, home, count, bases]))

    batter = self.getBatter()
    if batter:
      batting = "{} {} {}".format(self.printBatterBats(self.batter),
                                  self.printPlayerName(self.batter),
                                  self.printBatterStats(self.batter))

      pitcher = self.getPitcher()
      pitching = "{} {} {}".format(self.printPitcherThrows(pitcher),
                                   self.printPlayerName(pitcher),
                                   self.printPitcherStats(pitcher))

      lines.append("*Batting:* {}\n*Pitching:* {}".format(batting, pitching))

    if self.ticker:
      emoji = slack.getEmoji(self.teams[self.half][Key.NUMBER])
      lines.append("{} _{}_".format(emoji, self.ticker))

    return "\n\n".join(lines)

  def addPlayer(self, number, first, last, qualifier, hand):
    if number not in self.players:
      self.players[number] = {Key.FIRST: first, Key.LAST: last,
                              Key.BATTING: {k: 0 for k in Stats.BATTING},
                              Key.PITCHING: {k: 0 for k in Stats.PITCHING},
                              Key.BATS: "", Key.THROWS: ""}

    if qualifier == Qualifier.BATTING:
      self.players[number][Key.BATS] = hand
    else:
      self.players[number][Key.THROWS] = hand

  def getBatter(self):
    return self.batter

  def getPitcher(self):
    team = Half.HOME if self.half == Half.AWAY else Half.AWAY
    return self.teams[team][Key.PITCHER]

  def recordBatterRun(self, batter):
    if batter in self.players:
      stats = self.players[batter][Key.BATTING]
      stats["R"] += 1

  def recordBatterSimpleStats(self, *args):
    batter = self.getBatter()
    if batter in self.players:
      stats = self.players[batter][Key.BATTING]
      for stat in args:
        stats[stat] += 1

  def recordPitcherOut(self):
    pitcher = self.getPitcher()
    if pitcher in self.players:
      stats = self.players[pitcher][Key.PITCHING]
      stats["O"] += 1
      if stats["O"] == 3:
        stats["IP"] += 1
        stats["O"] = 0

  def recordPitcherRun(self, pitcher):
    if pitcher in self.players:
      stats = self.players[pitcher][Key.PITCHING]
      stats["R"] += 1

  def recordPitcherSimpleStats(self, *args):
    pitcher = self.getPitcher()
    if pitcher in self.players:
      stats = self.players[pitcher][Key.PITCHING]
      for stat in args:
        stats[stat] += 1

  def recordStrikeOut(self):
    pitcher = self.getPitcher()
    if pitcher in self.players:
      stats = self.players[pitcher][Key.PITCHING]
      stats["K"] += 1

  def setInning(self, half, frame):
    self.half = Half.AWAY if half == "Top" else Half.HOME
    self.frame = frame

    self.balls, self.strikes, self.outs = 0, 0, 0
    self.bases = {base: {Key.CURRENT: {Key.RUNNER: 0, Key.PITCHER: 0},
                         Key.FUTURE: {Key.RUNNER: 0, Key.PITCHER: 0}} for base in BASES}
    self.batter = 0

  def setBatter(self, number):
    if number in self.players:
      self.batter = number
      self.balls, self.strikes = 0, 0

  def setPitcher(self, number):
    if number in self.players:
      team = Half.HOME if self.half == Half.AWAY else Half.AWAY
      self.teams[team][Key.PITCHER] = number

  def storeBatterToBase(self, base, text):
    batter = self.getBatter()
    value = {Key.RUNNER: batter, Key.PITCHER: self.getPitcher()}
    if self.bases[base][Key.CURRENT][Key.RUNNER]:
      self.bases[base][Key.FUTURE] = value
    else:
      self.bases[base][Key.CURRENT] = value
    self.ticker = text.format(self.printPlayerName(batter))

  def storeRunnerToBase(self, base, previous, text):
    value = self.bases[previous][Key.CURRENT]
    runner = value[Key.RUNNER]
    if base == Base.HOME:
      self.storeRun()
      self.recordBatterSimpleStats("RBI")
      self.recordBatterRun(runner)
      self.recordPitcherRun(value[Key.PITCHER])
    elif self.bases[base][Key.CURRENT][Key.RUNNER]:
      self.bases[base][Key.FUTURE] = value
    else:
      self.bases[base][Key.CURRENT] = value
    self.ticker += " " + text.format(self.printPlayerName(runner))

    if self.bases[previous][Key.FUTURE][Key.RUNNER]:
      self.bases[previous][Key.CURRENT] = self.bases[previous][Key.FUTURE]
      self.bases[previous][Key.FUTURE] = {Key.RUNNER: 0, Key.PITCHER: 0}
    else:
      self.bases[previous][Key.CURRENT] = {Key.RUNNER: 0, Key.PITCHER: 0}

  def storeAllRunnersScore(self):
    for base in reversed(BASES):
      if self.bases[base][Key.CURRENT][Key.RUNNER]:
        self.storeRunnerToBase(Base.HOME, base, "{} scores.")

  def storeBall(self):
    self.balls += 1

  def storeStrike(self):
    self.strikes += 1

  def storeFoul(self):
    if self.strikes < 2:
      self.storeStrike()

  def storeOut(self):
    self.outs += 1

  def storeRun(self):
    self.teams[self.half][Key.RUNS] += 1

  def storeSimpleOut(self, text):
    self.storeOut()
    self.recordPitcherOut()
    self.recordBatterSimpleStats("AB")
    self.ticker = text.format(self.printPlayerName(self.getBatter()))

  def storeStrikeOut(self, text):
    self.storeStrike()
    self.storeOut()
    self.recordBatterSimpleStats("AB")
    self.recordPitcherOut()
    self.recordPitcherSimpleStats("K")
    self.ticker = text.format(self.printPlayerName(self.getBatter()))

  def storeStrikeOutReachesFirst(self):
    self.storeStrike()
    self.storeBatterToBase(Base.FIRST, "{} reaches first.")
    self.recordBatterSimpleStats("AB")
    self.recordPitcherSimpleStats("K")

  def storeWalk(self):
    self.storeBall()
    self.storeBatterToBase(Base.FIRST, "{} walks.")
    self.recordPitcherSimpleStats("BB")

  def storeSingle(self):
    self.storeBatterToBase(Base.FIRST, "{} singles.")
    self.recordBatterSimpleStats("AB", "H")
    self.recordPitcherSimpleStats("H")

  def storeDouble(self):
    self.storeBatterToBase(Base.SECOND, "{} doubles.")
    self.recordBatterSimpleStats("AB", "H", "2B")
    self.recordPitcherSimpleStats("H")

  def storeTriple(self):
    self.storeBatterToBase(Base.THIRD, "{} triples.")
    self.recordBatterSimpleStats("AB", "H", "3B")
    self.recordPitcherSimpleStats("H")

  def storeHomerun(self, text):
    self.ticker = text.format(self.printPlayerName(self.getBatter()))
    self.storeRun()
    self.storeAllRunnersScore()
    self.recordBatterSimpleStats("AB", "H", "HR", "RBI", "R")
    self.recordPitcherSimpleStats("H", "R")