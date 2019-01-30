#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Service (reloadable) methods for parsing StatsLab events."""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/services/statslab', '', _path))

from data.event.event import Event  # noqa

EVENT_KWARGS = {
    'base': r'([fsthFST123]\w+)',
    'distance': r'(\d+)',
    'path': r'(F|G|L|P)[\w ]+',
    'player': r'(P\d+)',
    'position': r'(C|1B|2B|3B|SS|LF|CF|RF|P)',
    'scoring': r'([EF]\d|U?[\d-]+)',
    'zone': r'(\w+)'
}

EVENT_MAP = {
    Event.CHANGE_BATTER: (r'^Batting: \w+ {player}$'),
    Event.CHANGE_FIELDER: (r'^Now (?:at|in) {position}: {player}$'),
    Event.CHANGE_PINCH_HITTER: (r'^Pinch Hitting: \w+ {player}$'),
    Event.CHANGE_PINCH_RUNNER: (r'^Pinch Runner at {base} {player}:$'),
    Event.CHANGE_PITCHER: (r'^Pitching: \w+ {player}$'),
    Event.BATTER_SINGLE: (r'^\d-\d: SINGLE \({path}, {zone}\)$'),
    Event.BATTER_SINGLE_APPEAL: (r'^SINGLE, but batter called out on appeal fo'
                                 r'r missing first base!$'),
    Event.BATTER_SINGLE_BUNT: (r'^\d-\d: Bunt for hit to {zone} - play at firs'
                               r't, batter safe!$'),
    Event.BATTER_SINGLE_ERR: (r'^\d-\d: Single, Error in OF, {scoring}, batter'
                              r' to second base \({path}, {zone}\)$'),
    Event.BATTER_SINGLE_INFIELD: (r'^\d-\d: SINGLE \({path}, {zone}\) \(infiel'
                                  r'd hit\)$'),
    Event.BATTER_DOUBLE: (r'^\d-\d: DOUBLE \({path}, {zone}\)$'),
    Event.BATTER_DOUBLE_STRETCH: (r'^\d-\d: DOUBLE \({path}, {zone}\) - OUT at'
                                  r'third base trying to stretch hit\.$'),
    Event.BATTER_TRIPLE: (r'^\d-\d: TRIPLE \({path}, {zone}\)$'),
    Event.BATTER_HOME_RUN: (r'^\d-\d: (?:SOLO|\d-RUN|GRAND SLAM) HOME RUN \({p'
                            r'ath}, {zone}\)\, Distance : {distance} ft$'),
    Event.BATTER_HOME_RUN_INSIDE: (r'^\d-\d: (?:SOLO|\d-RUN|GRAND SLAM) HOME R'
                                   r'UN \({path}, {zone}\)\, \(Inside the Park'
                                   r'\)$'),
    Event.BATTER_REACH_DROPPED: (r'^\d-\d: Reached via error on a dropped thro'
                                 r'w from {position}, {scoring} \(Groundball, '
                                 r'{zone}\)$'),
    Event.BATTER_REACH_FIELDING: (r'^\d-\d: Reached on error, {scoring} \({pat'
                                  r'h}, {zone}\)$'),
    Event.BATTER_FLY: (r'^\d-\d: Fly out, {scoring} \({path}, {zone}\)$'),
    Event.BATTER_FLY_BUNT: (r'^\d-\d: Bunt - Flyout to {zone}! {scoring}$'),
    Event.BATTER_FLY_BUNT_DP: (r'^\d-\d: Bunt - Flyout to {zone} - DP at {base'
                               r'}! {scoring}$'),
    Event.BATTER_GROUND: (r'^\d-\d: Grounds? out,? {scoring} \(Groundball, {zo'
                          r'ne}\)$'),
    Event.BATTER_GROUND_BUNT: (r'^\d-\d: Bunt for hit to {zone} - play at firs'
                               r't, batter OUT! {scoring}$'),
    Event.BATTER_GROUND_DP: (r'^\d-\d: Grounds into (?:double|DOUBLE) play, {s'
                             r'coring} \(Groundball, {zone}\)$'),
    Event.BATTER_GROUND_FC: (r'^\d-\d: Fielders Choice at {base}, {scoring} \('
                             r'Groundball, {zone}\)$'),
    Event.BATTER_GROUND_HOME: (r'^\d-\d: Grounds into fielders choice {scoring'
                               r'} \(Groundball, {zone}\)$'),
    Event.BATTER_SAC_BUNT: (r'^\d-\d: Sac Bunt to {zone} - play at first, batt'
                            r'er OUT! {scoring}$'),
    Event.BATTER_SAC_BUNT_DP: (r'^\d-\d: Sac Bunt - play at {base}, runner OUT'
                               r' -> throw to first, DP!$'),
    Event.BATTER_SAC_BUNT_HIT: (r'^\d-\d: Sac Bunt to {zone} - play at first, '
                                r'batter safe!$'),
    Event.BATTER_SAC_BUNT_OUT: (r'^\d-\d: Sac Bunt to {zone} - play at {base},'
                                r' runner OUT! {scoring}$'),
    Event.BATTER_SAC_BUNT_SAFE: (r'^\d-\d: Sac Bunt to {zone} - play at {base}'
                                 r', runner safe!$'),
    Event.CATCHER_PASSED_BALL: (r'^Passed Ball!$'),
    Event.CATCHER_PICK_OUT: (r'^Pickoff Throw by Catcher to {base} - Out!$'),
    Event.FIELDER_THROWING: (r'^Throwing error, {scoring}$'),
    Event.PITCHER_PICK_ERR: (r'^Pickoff Throw to {base} - Error! {scoring}$'),
    Event.PITCHER_PICK_OUT: (r'^Pickoff Throw to {base} - Out!(?: [\w-]+)?$'),
    Event.PITCHER_BALK: (r'^Balk!$'),
    Event.PITCHER_HIT_BY_PITCH: (r'^\d-\d: Hit by Pitch$'),
    Event.PITCHER_WILD_PITCH: (r'^Wild Pitch!$'),
    Event.PITCHER_BALL: (r'^\d-\d: (?:Ball|Base on Balls)$'),
    Event.PITCHER_WALK: (r'^\d-\d: Intentional Walk$'),
    Event.PITCHER_STRIKE_CALL: (r'^\d-\d: (?:Called Strike|Strikes out looking'
                                r')$'),
    Event.PITCHER_STRIKE_FOUL: (r'^\d-\d: Foul Ball, location: 2F$'),
    Event.PITCHER_STRIKE_FOUL_BUNT: (r'^\d-\d: Bunted foul$'),
    Event.PITCHER_STRIKE_FOUL_ERR: (r'^Error on foul ball, {scoring}$'),
    Event.PITCHER_STRIKE_MISS: (r'^\d-\d: Bunt missed!$'),
    Event.PITCHER_STRIKE_SWING: (r'^\d-\d: (?:Swinging Strike|Strikes out swin'
                                 r'ging)$'),
    Event.PITCHER_STRIKE_SWING_OUT: (r'^\d-\d: Strikes out swinging, 2-3 out a'
                                     r't first.$'),
    Event.PITCHER_STRIKE_SWING_PASSED: (r'^\d-\d: Strikes out swinging passed '
                                        r'ball, reaches first!$'),
    Event.PITCHER_STRIKE_SWING_WILD: (r'^\d-\d: Strikes out swinging wild pitc'
                                      r'h, reaches first!$'),
    Event.RUNNER_STEAL: (r'^{player} steals {base} base(?: \(no throw\))?$'),
    Event.RUNNER_STEAL_HOME_OUT: (r'^Steal of home, {player} is out$'),
    Event.RUNNER_STEAL_OUT: (r'^{player} is caught stealing {base} base {scori'
                             r'ng}$'),
    Event.RUNNER_STEAL_THROWING: (r'^{player} steals {base}, throwing error, E'
                                  r'2$'),
    Event.PLAYER_MOVE: (r'^{player} to {base}$'),
    Event.PLAYER_SCORE: (r'^{player} scores$'),
    Event.BASE_MOVE: (r'^Runner from {base} (?:tags up, SAFE at \w+|tries for '
                      r'[2|3]\w+, SAFE)(?:, no throw by \w+)?$'),
    Event.BASE_MOVE_RUNDOWN: (r'^Runner from {base} tries for [2|3]\w+, SAFE a'
                              r'fter rundown.$'),
    Event.BASE_MOVE_THROW: (r'^Runner from {base} (?:tags up, SAFE at \w+ with'
                            r' throw by \w+|tries for [2|3]\w+, SAFE, throw by'
                            r' \w+ made to \w+)$'),
    Event.BASE_OUT: (r'^Runner from {base} (?:tags up, OUT at \w+!|tries for ['
                     r'2|3]\w+, OUT!|tries for Home, throw by \w+ and OUT!) {s'
                     r'coring}$'),
    Event.BASE_SCORE: (r'^Runner from 3rd (?:tags up, SCORES|tries for Home, S'
                       r'AFE)(?:, no throw by \w+)?$'),
    Event.BASE_SCORE_THROW: (r'^Runner from 3rd (?:tags up, SCORES|tries for H'
                             r'ome, SAFE), throw by \w+(?: to home)?$'),
    Event.BASE_SCORE_TRAIL: (r'^Runner from 3rd tries for Home, SAFE, throw by'
                             r' \w+ to trailing runner, SAFE at third!$'),
    Event.BASE_SCORE_TRAIL_OUT: (r'^Runner from 3rd tries for Home, SAFE, thro'
                                 r'w by \w+ to trailing runner, OUT at third! '
                                 r'{scoring}$'),
    Event.NONE: (r'^(?:\d-\d: Grounds into DOUBLE play, [\w-]+|Batter strikes '
                 r'out\.)$'),
}

MAP = {k: v.format(**EVENT_KWARGS) for k, v in EVENT_MAP.items()}


def get_map():
    return MAP
