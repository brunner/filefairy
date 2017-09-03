#!/usr/bin/env python

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import slack
import time


attachments = [
    {
        "fallback": "Top of the 1st - Chicago White Sox batting - Pitching for the Boston Red Sox : LHP Sean Newcomb",
        "color": "#000000",
        "author_name": "Top of the 1st - Chicago White Sox batting - Pitching for the Boston Red Sox : LHP Sean Newcomb",
        "author_icon": "http://m.mlb.com/shared/images/logos/32x32_cap/145.png",
        "fields": [
            {"value": "Pitching: LHP Sean Newcomb"},
        ]
    }
]
response = slack.postMessage_("testing", "", attachments)
obj = json.loads(response.read())
channel = obj["channel"]
ts = obj["message"]["ts"]

time.sleep(4)
attachments[0]["fields"].append(
    {"value": "Batting: SHB Jacob May", "short": "true"})
attachments[0]["fields"].append(
    {"value": "0-0: Ball\n1-0: Called Strike\n1-1: Bunt for hit - play at first, batter OUT! 4-3", "short": "true"})
response = slack.update_(ts, channel, "", attachments)

time.sleep(4)
attachments[0]["fields"].append(
    {"value": "Batting: LHB Jake Bauers", "short": "true"})
attachments[0]["fields"].append(
    {"value": "0-0: Ball\n1-0: Ball\n2-0: Called Strike\n2-1: Fly out, F8 (Flyball, 8LM)", "short": "true"})
response = slack.update_(ts, channel, "", attachments)

time.sleep(4)
attachments[0]["fields"].append(
    {"value": "Batting: LHB Adam Eaton", "short": "true"})
attachments[0]["fields"].append(
    {"value": "0-0: Swinging Strike\n0-1: Ball\n1-1: Called Strike\n1-2: Ball\n2-2: Foul Ball, location: 2F\n2-2: Strikes out  swinging", "short": "true"})
attachments[0]["footer"] = "Top of the 1st over - 0 run(s), 0 hit(s), " \
    + "0 error(s), 0 left on base; Chicago 0 - Boston 0."
response = slack.update_(ts, channel, "", attachments)

time.sleep(4)
attachments = [
    {
        "fallback": "Bottom of the 1st -  Boston Red Sox batting - Pitching for Chicago White Sox : LHP Junior Reyes",
        "color": "#C60C30",
        "author_name": "Bottom of the 1st -  Boston Red Sox batting - Pitching for Chicago White Sox : LHP Junior Reyes",
        "author_icon": "http://m.mlb.com/shared/images/logos/32x32_cap/111.png",
        "fields": [{"value": "Pitching: LHP Junior Reyes"}]
    }
]
response = slack.postMessage_("testing", "", attachments)
obj = json.loads(response.read())
channel = obj["channel"]
ts = obj["message"]["ts"]

time.sleep(4)
attachments[0]["fields"].append(
    {"value": "Batting: RHB Xander Bogaerts", "short": "true"})
attachments[0]["fields"].append(
    {"value": "0-0: Ball\n1-0: Swinging Strike\n1-1: DOUBLE  (Line Drive, 78XD) - OUT at third base trying to stretch hit.", "short": "true"})
response = slack.update_(ts, channel, "", attachments)

time.sleep(4)
attachments[0]["fields"].append(
    {"value": "Batting: SHB Blake Swihart", "short": "true"})
attachments[0]["fields"].append(
    {"value": "0-0: Swinging Strike\n0-1: Ball\n1-1: Foul Ball, location: 2F\n1-2: Ball\n2-2: Foul Ball, location: 2F\n2-2: Foul Ball, location: 2F\n2-2: Ball\n3-2: Strikes out  looking", "short": "true"})
response = slack.update_(ts, channel, "", attachments)

time.sleep(4)
attachments[0]["fields"].append(
    {"value": "Batting: RHB Connor Harrell", "short": "true"})
attachments[0]["fields"].append(
    {"value": "0-0: Called Strike\n0-1: Ground out 5-3 (Groundball, 25)", "short": "true"})
attachments[0]["footer"] = "Bottom of the 1st over -  0 run(s), 1 hit(s), " \
    + "0 error(s), 0 left on base; Chicago 0 - Boston 0"
response = slack.update_(ts, channel, "", attachments)
