#!/usr/bin/env python

import json
import slack
import time


boxes = [
  #0
  ":toparrow: 1 :separator: :whitesox: 0 :separator: :redsox: 0 :separator: " \
      + ":outoff::outoff::outoff: :separator: :bottombaseoff::topbaseoff:" \
      + ":bottombaseoff:",

  #1
  ":toparrow: 1 :separator: :whitesox: 0 :separator: :redsox: 0 :separator: " \
      + ":outon::outoff::outoff: :separator: :bottombaseoff::topbaseoff:" \
      + ":bottombaseoff:",

  #2
  ":toparrow: 1 :separator: :whitesox: 0 :separator: :redsox: 0 :separator: " \
      + ":outon::outon::outoff: :separator: :bottombaseoff::topbaseoff:" \
      + ":bottombaseoff:",

  #3
  ":toparrow: 1 :separator: :whitesox: 0 :separator: :redsox: 0 :separator: " \
      + ":outon::outon::outon: :separator: :bottombaseoff::topbaseoff:" \
      + ":bottombaseoff:",

  #4
  ":bottomarrow: 1 :separator: :whitesox: 0 :separator: :redsox: 0 :separator: " \
      + ":outoff::outoff::outoff: :separator: :bottombaseoff::topbaseoff:" \
      + ":bottombaseoff:",

  #5
  ":bottomarrow: 1 :separator: :whitesox: 0 :separator: :redsox: 0 :separator: " \
      + ":outon::outoff::outoff: :separator: :bottombaseoff::topbaseoff:" \
      + ":bottombaseoff:",

  #6
  ":bottomarrow: 1 :separator: :whitesox: 0 :separator: :redsox: 0 :separator: " \
      + ":outon::outon::outon: :separator: :bottombaseoff::topbaseoff:" \
      + ":bottombaseoff:",
]

messages = [
  # 0
  "Top of the 1st.\nPitching: LHP Sean Newcomb",

  #1
  "Batting: SHB Jacob May\n0-0: Ball\n1-0: Called Strike\n1-1: Bunt for " \
      + "hit - play at first, batter OUT! 4-3\n\nBatting: LHB Jake Bauers" \
      + "\n0-0: Ball\n1-0: Ball",

  #2
  "2-0: Called Strike\n2-1:  Fly out, F8  (Flyball, 8LM)\n\nBatting: LHB " \
      + "Adam Eaton\n0-0: Swinging Strike\n0-1: Ball\n1-1: Called Strike",

  #3
  "1-2: Ball\n2-2: Foul Ball, location: 2F\n2-2: Strikes out  swinging",

  #4
  "Top of the 1st over.\n0 run(s), 0 hit(s), 0 error(s), 0 left on base." \
      + "\nChicago 0 - Boston 0.",

  #5
  "Bottom of the 1st.\nPitching: LHP Junior Reyes",

  #6
  "Batting: RHB Xander Bogaerts\n0-0: Ball\n1-0: Swinging strike\n1-1: " \
      + "*DOUBLE* (Line Drive, 78XD) - OUT at third base trying to stretch " \
      + "hit.\n\nBatting: SHB Blake Swihart\n0-0: Swinging strike\n0-1 Ball",

  #7
  "1-1: Foul Ball, location: 2F\n1-2: Ball\n2-2: Foul Ball, location: " \
      + "2F\n2-2: Foul Ball, location: 2F\n2-2: Ball",

  #8
  "3-2: Strikes out looking\n\nBatting: RHB Connor Harrell\n0-0: Called " \
      + "Strike\n0-1: Ground out 5-3 (Groundball, 25)",

  #9
  "Bottom of the 1st over.\n0 run(s), 1 hit(s), 0 error(s), 0 left on base." \
      + "\nChicago 0 - Boston 0."
]

response = slack.postMessage(boxes[0], "testing")
deserialized = json.loads(response.read())
channel = deserialized["channel"]
box_ts = deserialized["ts"]

response = slack.postMessage("Scoring updates:", "testing")
deserialized = json.loads(response.read())
scoring_ts = deserialized["ts"]

response = slack.postMessage("Game log:", "testing")
deserialized = json.loads(response.read())
log_ts = deserialized["ts"]

time.sleep(5)
slack.postMessage(messages[0], channel, log_ts)

time.sleep(5)
slack.postMessage(messages[1], channel, log_ts)
time.sleep(2)
slack.update(boxes[1], channel, box_ts)

time.sleep(5)
slack.postMessage(messages[2], channel, log_ts)
time.sleep(2)
slack.update(boxes[2], channel, box_ts)

time.sleep(5)
slack.postMessage(messages[3], channel, log_ts)
time.sleep(2)
slack.update(boxes[3], channel, box_ts)

time.sleep(5)
slack.postMessage(messages[4], channel, log_ts)

time.sleep(5)
slack.postMessage(messages[5], channel, log_ts)
time.sleep(2)
slack.update(boxes[4], channel, box_ts)

time.sleep(5)
slack.postMessage(messages[6], channel, log_ts)
time.sleep(2)
slack.update(boxes[5], channel, box_ts)
time.sleep(2)
slack.postMessage(":toparrow: 4 :separator: :pirates: 10 " +
    ":separator: :giants: 0\n:pirates: C.J. Hinojosa " +
    "hits a 3-run HR.", channel, scoring_ts)

time.sleep(5)
slack.postMessage(messages[7], channel, log_ts)

time.sleep(5)
slack.postMessage(messages[8], channel, log_ts)
time.sleep(2)
slack.update(boxes[6], channel, box_ts)

time.sleep(5)
slack.postMessage(messages[9], channel, log_ts)