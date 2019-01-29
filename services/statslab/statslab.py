#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Service (reloadable) methods for parsing StatsLab pages."""

import datetime
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/services/statslab', '', _path))

from common.datetime_.datetime_ import datetime_as_est  # noqa
from common.datetime_.datetime_ import datetime_as_pst  # noqa
from common.datetime_.datetime_ import datetime_datetime_est  # noqa
from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.datetime_.datetime_ import encode_datetime  # noqa
from common.encyclopedia.encyclopedia import put_players  # noqa
from common.json_.json_ import dumps  # noqa
from common.re_.re_ import find  # noqa
from common.re_.re_ import findall  # noqa
from common.re_.re_ import match  # noqa
from common.requests_.requests_ import get  # noqa
from common.teams.teams import decoding_to_encoding_sub  # noqa
from common.teams.teams import encoding_to_hometown  # noqa
from data.event.event import Event  # noqa

EVENT_MAP = {
    Event.CHANGE_BATTER: r'^Batting: \w+ {player}$',
    Event.CHANGE_FIELDER: r'^Now (?:at|in) {position}: {player}$',
    Event.CHANGE_PINCH_HITTER: r'^Pinch Hitting: \w+ {player}$',
    Event.CHANGE_PINCH_RUNNER: r'^Pinch Runner at {base} {player}:$',
    Event.CHANGE_PITCHER: r'^Pitching: \w+ {player}$',
    Event.BATTER_SINGLE: r'^\d-\d: SINGLE \({path}, {zone}\)$',
    Event.BATTER_SINGLE_APPEAL: (r'^SINGLE, but batter called out on appeal fo'
                                 r'r missing first base!$'),
    Event.BATTER_SINGLE_BUNT: (r'^\d-\d: Bunt for hit to {zone} - play at firs'
                               r't, batter safe!$'),
    Event.BATTER_SINGLE_ERROR: (r'^\d-\d: Single, Error in OF, {scoring}, batt'
                                r'er to second base \({path}, {zone}\)$'),
    Event.BATTER_SINGLE_INFIELD: (r'^\d-\d: SINGLE \({path}, {zone}\) \(infiel'
                                  r'd hit\)$'),
    Event.BATTER_DOUBLE: r'^\d-\d: DOUBLE \({path}, {zone}\)$',
    Event.BATTER_TRIPLE: r'^\d-\d: TRIPLE \({path}, {zone}\)$',
    Event.BATTER_HOME_RUN: (r'^\d-\d: (?:SOLO|\d-RUN|GRAND SLAM) HOME RUN \({p'
                            r'ath}, {zone}\)\, Distance : {distance} ft$'),
    Event.BATTER_REACH_DROPPED: (r'^\d-\d: Reached via error on a dropped thro'
                                 r'w from {position}, {scoring} \(Groundball, '
                                 r'{zone}\)$'),
    Event.BATTER_REACH_FIELDING: (r'^\d-\d: Reached on error, {scoring} \({pat'
                                  r'h}, {zone}\)$'),
    Event.BATTER_FLY: r'^\d-\d: Fly out, {scoring} \({path}, {zone}\)$',
    Event.BATTER_FLY_BUNT: r'^\d-\d: Bunt - Flyout to {zone}! {scoring}$',
    Event.BATTER_FLY_BUNT_DP: (r'^\d-\d: Bunt - Flyout to {zone} - DP at {base'
                               r'}! {scoring}$'),
    Event.BATTER_GROUND: (r'^\d-\d: Grounds? out,? {scoring} \(Groundball, {zo'
                          r'ne}\)$'),
    Event.BATTER_GROUND_BUNT: (r'^\d-\d: Bunt for hit to {zone} - play at firs'
                               r't, batter OUT! {scoring}$'),
    Event.BATTER_GROUND_DP: (r'^\d-\d: Grounds into (?:double|DOUBLE) play, {s'
                             r'coring} \(Groundball, {zone}\)$'),
    Event.BATTER_GROUND_FC: (r'^\d-\d: Fielders Choice at {base}, {scoring} \(G'
                             r'roundball, {zone}\)$'),
    Event.BATTER_GROUND_HOME: (r'^\d-\d: Grounds into fielders choice {scoring'
                               r'} \(Groundball, {zone}\)$'),
    Event.BATTER_SAC_BUNT: (r'^\d-\d: Sac Bunt to {zone} - play at first, batt'
                            r'er OUT! {scoring}$'),
    Event.BATTER_SAC_BUNT_DP: (r'^\d-\d: Sac Bunt - play at second, runner OUT'
                               r' -> throw to first, DP!$'),
    Event.BATTER_SAC_BUNT_OUT: (r'^\d-\d: Sac Bunt to {zone} - play at {base},'
                                r' runner OUT! {scoring}$'),
    Event.BATTER_SAC_BUNT_SAFE: (r'^\d-\d: Sac Bunt to {zone} - play at first,'
                                 r' batter safe!$'),
    Event.CATCHER_PASSED_BALL: r'^Passed Ball!$',
    Event.CATCHER_PICK_OUT: r'^Pickoff Throw by Catcher to {base} - Out!$',
    Event.FIELDER_THROWING: r'^Throwing error, {scoring}$',
    Event.PITCHER_PICK_ERROR: r'^Pickoff Throw to {base} - Error! {scoring}$',
    Event.PITCHER_PICK_OUT: r'^Pickoff Throw to {base} - Out! {scoring}$',
    Event.PITCHER_BALK: r'^Balk!$',
    Event.PITCHER_HIT_BY_PITCH: r'^\d-\d: Hit by Pitch$',
    Event.PITCHER_WILD_PITCH: r'^Wild Pitch!$',
    Event.PITCHER_BALL: r'^\d-\d: (?:Ball|Base on Balls)$',
    Event.PITCHER_WALK: r'^\d-\d: Intentional Walk$',
    Event.PITCHER_STRIKE_CALL: (r'^\d-\d: (?:Called Strike|Strikes out looking'
                                r')$'),
    Event.PITCHER_STRIKE_FOUL: r'^\d-\d: Foul Ball, location: 2F$',
    Event.PITCHER_STRIKE_FOUL_BUNT: r'^\d-\d: Bunted foul$',
    Event.PITCHER_STRIKE_FOUL_ERROR: r'^Error on foul ball, {scoring}$',
    Event.PITCHER_STRIKE_MISS: r'^\d-\d: Bunt missed!$',
    Event.PITCHER_STRIKE_SWING: (r'^\d-\d: (?:Swinging Strike|Strikes out swin'
                                 r'ging)$'),
    Event.PITCHER_STRIKE_SWING_OUT: (r'^\d-\d: Strikes out swinging, 2-3 out a'
                                     r't first.$'),
    Event.PITCHER_STRIKE_SWING_PASSED: (r'^\d-\d: Strikes out swinging passed '
                                        r'ball, reaches first!$'),
    Event.PITCHER_STRIKE_SWING_WILD: (r'^\d-\d: Strikes out swinging wild pitc'
                                      r'h, reaches first!$'),
    Event.RUNNER_STEAL: r'^{player} steals {base} base(?: \(no throw\))?$',
    Event.RUNNER_STEAL_OUT: (r'^{player} is caught stealing {base} base {scori'
                             r'ng}$'),
    Event.RUNNER_STEAL_THROWING: (r'^{player} steals {base}, throwing error, E'
                                  r'2$'),
    Event.PLAYER_MOVE: r'^{player} to {base}$',
    Event.PLAYER_SCORE: r'^{player} scores$',
    Event.BASE_MOVE: (r'^Runner from {base} (?:tags up, SAFE at \w+|tries for '
                      r'[2|3]\w+, SAFE)(?:, no throw by \w+)?$'),
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

EVENT_KWARGS = {
    'base': r'([fsthFST123]\w+)',
    'distance': r'(\d+)',
    'path': r'(F|G|L|P)[\w ]+',
    'player': r'(P\d+)',
    'position': r'(C|1B|2B|3B|SS|LF|CF|RF|P)',
    'scoring': r'([EF]\d|U?[\d-]+)',
    'zone': r'(\w+)'
}
EVENT_MAP = {k: v.format(**EVENT_KWARGS) for k, v in EVENT_MAP.items()}


def _open(in_):
    text = ''
    if in_.startswith('http'):
        text = get(in_)
    elif os.path.isfile(in_):
        with open(in_, 'r', encoding='iso-8859-1') as f:
            text = f.read()

    text = decoding_to_encoding_sub(text)
    text = re.sub(r'<a href="../\w+/player_(\d+)\.[^<]+</a>', r'P\1', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'</?b>', '', text)
    text = re.sub(r' &nbsp;&nbsp;', '', text)

    return text


def _parse_innings(text, html):
    regex = r'(?s)(\w+) batting - Pitching for (\w+) : \w+ (\w+)(.+?)'
    if html:
        regex += r'</table>'
    else:
        regex += r'\[%T\]'
        text += '[%T]'

    return findall(regex, text)


def _parse_lines(content, html, away_pitcher):
    lines = []
    if html:
        regex = (r'(?s)<td valign="top" width="268px" class="dl">(.+?)</td> <t'
                 r'd class="dl" width="700px">(.+?)</td>')
        for left, right in findall(regex, content):
            lines.append(left)
            for r in right.split('<br>'):
                lines.append(r)
    else:
        lines += findall(r'(?s)[BN]\](.+?)\[%', content + '[%T]')

    return list(filter(bool, lines))


def parse_player(link):
    """Parse a StatsLab player page into a reference-readable format.

    Args:
        link: The StatsLab player page link.

    Returns:
        A data string if the parse was successful, otherwise None.
    """
    text = _open(link)
    number, name = find(r'Player Report for #(\d+) ([^<]+)</title>', text)
    if not number:
        return None
    name = re.sub(r' \'[^\']+\' ', r' ', name)
    subtext = find(r'(?s)class="repsubtitle">(.+?)</div>', text)
    if not subtext:
        return None

    team = find(r'href=\"..\/teams\/team_\d{2}.html">(\w+)</a>', subtext)
    if not team:
        team = 'T??'
    bats, throws = find(r'Bats: (\w)[^T]+Throws: (\w)', text)
    data = [team, number, bats, throws, name]

    if not all(data):
        return None

    return ' '.join(data)


def parse_box(in_, out, date, **services):
    """Parse a StatsLab box score into a task-readable format.

    If the box score is parsed successfully, the resulting data is written to a
    specified file and True is the returned value. Alternatively, if the box
    score is missing or does not match the given date, no JSON data is written
    and None is returned.

    Args:
        in_: The StatsLab box score link or file path.
        out: The file path to write the parsed data to.
        date: The encoded date that the box score is expected to match.
        services: The dictionary of services expected by this method.

    Returns:
        True if the parse was successful, otherwise None.
    """
    jersey_colors = services['jersey_colors']

    text = _open(in_)
    away, home, s = find(r'(\w+) at (\w+), (\d{2}\/\d{2}\/\d{4})', text)
    if not s:
        return None

    d = datetime.datetime.strptime(s, '%m/%d/%Y')
    d = datetime_datetime_pst(d.year, d.month, d.day)
    if date is not None and date != encode_datetime(d):
        return None

    t = find(r'(?s)Start Time:(.+?)<br>', text).strip(' EST')
    s = datetime.datetime.strptime(t.upper(), '%I:%M %p')

    d = datetime_as_est(d)
    date = datetime_datetime_est(d.year, d.month, d.day, s.hour, s.minute)
    date = encode_datetime(datetime_as_pst(date))

    day = d.weekday()
    home_colors = jersey_colors(home, day, 'home', None)
    away_colors = jersey_colors(away, day, 'away', home_colors[0])

    data = {
        'away_colors': ' '.join(away_colors),
        'away_team': away,
        'date': date,
        'home_colors': ' '.join(home_colors),
        'home_team': home,
    }

    for team in ['away', 'home']:
        i = data[team + '_team']
        line = find(r'(?s)<td class="dl">' + i + r'(.+?)</tr>', text)
        data[team + '_record'] = find(r'^\((\d+-\d+)\)', line)

        cols = findall(r'>(\d+|X)<', line)
        if not cols:
            cols = ['0', '0', '0']
        for suffix in ['_errors', '_hits', '_runs']:
            data[team + suffix] = cols.pop(-1)
        data[team + '_line'] = ' '.join(cols)

    data['recap'] = find(
        r'(?s)<!--RECAP_SUBJECT_START-->(.+?)<!--RECAP_SUBJECT_END-->', text)

    blines = findall(r'(?s)>RBI</th>\s*</tr>(.+?)</table>', text)
    plines = findall(r'(?s)>ERA</th>\s*</tr>(.+?)</table>', text)
    if len(blines) != 2 or len(plines) != 2:
        return None

    encodings = set()
    for line in (plines + blines):
        encodings.update(findall(r'>(P\d+) ', text))
    put_players(list(sorted(encodings)))

    batting = findall(r'(?s)BATTING<br>(.+?)</table>', text)
    if len(batting) != 2:
        return None

    for team, btext in zip(['away', 'home'], batting):
        homeruns = []
        container = find(r'(?s)Home Runs:(.+?)<br>', btext)
        if container:
            container = re.sub(r'\s+', ' ', container)
            for s in container.split(') '):
                p, n, total = find(r'^(\w+)(?:\s(\d+))?\s\((\d+),', s)
                if not n:
                    n = '1'
                homeruns.append(' '.join([p, n, total]))
        data[team + '_homeruns'] = ', '.join(homeruns)

    for pitcher in ['winning', 'losing']:
        i = pitcher[0].upper()
        p, line = find(r'(?s)<td class="dl">(\w+) ' + i + r' (.+?)</tr>', text)

        record = find(r'^\((\d+-\d+)\)', line)
        era = find(r'>([^<]+)</td>$', line)
        data[pitcher + '_pitcher'] = ' '.join([p, record, era])

    p, saves = find(r'(?s)<td class="dl">(\w+) SV \((\d+)\)', text)
    data['saving_pitcher'] = ' '.join([p, saves]) if saves else ''

    data['ballpark'] = find(r'(?s)Ballpark:(.+?)<br>', text)

    with open(out, 'w') as f:
        f.write(dumps(data) + '\n')

    return True


def parse_log(in_, out, date):
    """Parse a StatsLab game log into a task-readable format.

    If the game log is parsed successfully, the resulting data is written to a
    specified file and True is the returned value. Alternatively, if the game
    log is missing or does not match the given date, no JSON data is written
    and None is returned.

    Args:
        in_: The StatsLab game log link or file path.
        out: The file path to write the parsed data to.
        date: The encoded date that the game log is expected to match.
        services: The dictionary of services expected by this method.

    Returns:
        True if the parse was successful, otherwise None.
    """
    html = in_.endswith('html')
    text = _open(in_)

    away, home = find(r'(\w+) batting - Pitching for (\w+)', text)
    if not away:
        return None

    if date is not None:
        s = find(r'>(\d{2}\/\d{2}\/\d{4})<', text)
        if not s:
            return None

        d = datetime.datetime.strptime(s, '%m/%d/%Y')
        d = datetime_datetime_pst(d.year, d.month, d.day)
        if date != encode_datetime(d):
            return None

    away_pitcher = find(r'Pitching for ' + away + r' : \w+ (\w+)', text)
    home_pitcher = find(r'Pitching for ' + home + r' : \w+ (\w+)', text)

    data = {
        'away_starter': away_pitcher,
        'away_team': away,
        'home_starter': home_pitcher,
        'home_team': home,
    }

    events = []
    for inning in _parse_innings(text, html):
        events.append(Event.CHANGE_INNING.encode())

        batting, pitching, pitcher, content = inning
        for line in _parse_lines(content, html, away_pitcher):
            for event, regex in EVENT_MAP.items():
                groups = match(regex, line)
                if groups is not None:
                    events.append(event.encode(*groups))
                    break
            else:
                # TODO: Handle this gracefully.
                raise Exception(in_, line)

    data['events'] = events

    with open(out, 'w') as f:
        f.write(dumps(data) + '\n')

    return True
