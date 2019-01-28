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
from common.requests_.requests_ import get  # noqa
from common.teams.teams import decoding_to_encoding_sub  # noqa
from common.teams.teams import encoding_to_hometown  # noqa
from data.event.event import Event  # noqa

EVENT_MAP = {
    Event.CHANGE_BATTER:
    r'^Batting: \w+ (\w+)$',
    Event.CHANGE_FIELDER:
    r'^Now (?:at|in) (\w+): (\w+)$',
    Event.CHANGE_PINCH_HITTER:
    r'^Pinch Hitting: \w+ (\w+)$',
    Event.CHANGE_PINCH_RUNNER:
    r'^Pinch Runner at (\d)\w+ (\w+):$',
    Event.CHANGE_PITCHER:
    r'^Pitching: \w+ (\w+)$',
    Event.BATTER_INFIELD_SINGLE:
    r'^\d-\d: SINGLE \((\w)[\w ]+, (\w+)\) \(infield hit\)$',
    Event.BATTER_SINGLE:
    r'^\d-\d: SINGLE \((\w)[\w ]+, (\w+)\)$',
    Event.BATTER_DOUBLE:
    r'^\d-\d: DOUBLE \((\w)[\w ]+, (\w+)\)$',
    Event.BATTER_TRIPLE:
    r'^\d-\d: TRIPLE \((\w)[\w ]+, (\w+)\)$',
    Event.BATTER_HOME_RUN:
    r'^\d-\d: (?:SOLO|\d-RUN|GRAND SLAM) HOME RUN \((\w)[\w ]+, (\w+)\)\, Distance : (\d+) ft$',
    Event.BATTER_SINGLE_ERROR_IN_OUTFIELD:
    r'^\d-\d: Single, Error in OF, (\w+), batter to second base \((\w)[\w ]+, (\w+)\)$',
    Event.BATTER_SINGLE_MISSED_BASE:
    r'^SINGLE, but batter called out on appeal for missing first base!$',
    Event.BATTER_REACH_ON_DROPPED_THROW:
    r'^\d-\d: Reached via error on a dropped throw from (\w+), (\w+) \(Groundball, (\w+)\)$',
    Event.BATTER_REACH_ON_FIELDING_ERROR:
    r'^\d-\d: Reached on error, (\w+) \((\w)[\w ]+, (\w+)\)$',
    Event.BATTER_BUNT_FLIES_INTO_DOUBLE_PLAY_AT_THIRD:
    r'^\d-\d: Bunt - Flyout to (\w+) - DP at third! ([\w-]+)$',
    Event.BATTER_BUNT_FLY_OUT:
    r'^\d-\d: Bunt - Flyout to (\w+)! (\w+)$',
    Event.BATTER_BUNT_GROUND_OUT:
    r'^\d-\d: Bunt for hit to (\w+) - play at first, batter OUT! ([\w-]+)$',
    Event.BATTER_BUNT_HIT:
    r'^\d-\d: Bunt for hit to (\w+) - play at first, batter safe!$',
    Event.BATTER_FLY_OUT:
    r'^\d-\d: Fly out, ([\w-]+) \((\w)[\w ]+, (\w+)\)$',
    Event.BATTER_GROUND_OUT:
    r'^\d-\d: Grounds? out,? ([\w-]+) \(Groundball, (\w+)\)$',
    Event.BATTER_GROUNDS_INTO_DOUBLE_PLAY:
    r'^\d-\d: Grounds into (?:double|DOUBLE) play, ([\w-]+) \(Groundball, (\w+)\)$',
    Event.BATTER_GROUNDS_INTO_FIELDERS_CHOICE:
    r'^\d-\d: (?:Fielders Choice at 2nd,|Grounds into fielders choice) ([\w-]+) \(Groundball, (\w+)\)$',
    Event.BATTER_SAC_BUNT_OUT_AT_FIRST:
    r'^\d-\d: Sac Bunt to (\w+) - play at first, batter OUT! ([\w-]+)$',
    Event.BATTER_SAC_BUNT_OUT_AT_SECOND:
    r'^\d-\d: Sac Bunt to (\w+) - play at second, runner OUT! ([\w-]+)$',
    Event.BATTER_SAC_BUNT_OUT_AT_SECOND_AT_FIRST:
    r'^\d-\d: Sac Bunt - play at second, runner OUT -> throw to first, DP!$',
    Event.BATTER_SAC_BUNT_OUT_AT_THIRD:
    r'^\d-\d: Sac Bunt to (\w+) - play at third, runner OUT! ([\w-]+)$',
    Event.BATTER_SAC_BUNT_SAFE_AT_FIRST:
    r'^\d-\d: Sac Bunt to (\w+) - play at first, batter safe!$',
    Event.BATTER_STRIKE_OUT:
    r'^Batter strikes out\.$',
    Event.CATCHER_PASSED_BALL:
    r'^Passed Ball!$',
    Event.CATCHER_PICKOFF_FIRST_OUT:
    r'^Pickoff Throw by Catcher to First - Out!$',
    Event.FIELDER_THROWING_ERROR:
    r'^Throwing error, (\w+)$',
    Event.PITCHER_BALK:
    r'^Balk!$',
    Event.PITCHER_BALL:
    r'^\d-\d: (?:Ball|Base on Balls)$',
    Event.PITCHER_CALLED_STRIKE:
    r'^\d-\d: (?:Called Strike|Strikes out looking)$',
    Event.PITCHER_FOULED_BUNT_STRIKE:
    r'^\d-\d: Bunted foul$',
    Event.PITCHER_FOULED_STRIKE:
    r'^\d-\d: Foul Ball, location: 2F$',
    Event.PITCHER_FOULED_STRIKE_WITH_ERROR:
    r'^Error on foul ball, (\w+)$',
    Event.PITCHER_HIT_BY_PITCH:
    r'^\d-\d: Hit by Pitch$',
    Event.PITCHER_INTENTIONAL_WALK:
    r'^\d-\d: Intentional Walk$',
    Event.PITCHER_MISSED_BUNT_STRIKE:
    r'^\d-\d: Bunt missed!$',
    Event.PITCHER_PICKOFF_FIRST_ERROR:
    r'^Pickoff Throw to First - Error! E1$',
    Event.PITCHER_PICKOFF_FIRST_OUT:
    r'^Pickoff Throw to First - Out! 1-3$',
    Event.PITCHER_SWINGING_STRIKE:
    r'^\d-\d: (?:Swinging Strike|Strikes out swinging)$',
    Event.PITCHER_SWINGING_STRIKE_OUT_AT_FIRST:
    r'^\d-\d: Strikes out swinging, 2-3 out at first.$',
    Event.PITCHER_SWINGING_STRIKE_SAFE_PASSED_BALL:
    r'^\d-\d: Strikes out swinging passed ball, reaches first!$',
    Event.PITCHER_SWINGING_STRIKE_SAFE_WILD_PITCH:
    r'^\d-\d: Strikes out swinging wild pitch, reaches first!$',
    Event.PITCHER_WILD_PITCH:
    r'^Wild Pitch!$',
    Event.RUNNER_STEAL_SECOND_OUT:
    r'^(\w+) is caught stealing 2nd base [\w-]+$',
    Event.RUNNER_STEAL_SECOND_SAFE:
    r'^(\w+) steals 2nd base(?: \(no throw\))?$',
    Event.RUNNER_STEAL_SECOND_THROWING_ERROR:
    r'^(\w+) steals 2nd, throwing error, E2$',
    Event.RUNNER_TO_SECOND_NO_THROW:
    r'^(\w+) to second$',
    Event.RUNNER_STEAL_THIRD_OUT:
    r'^(\w+) is caught stealing 3rd base [\w-]+$',
    Event.RUNNER_STEAL_THIRD_SAFE:
    r'^(\w+) steals 3rd base$',
    Event.RUNNER_TO_THIRD_NO_THROW:
    r'^(\w+) to third$',
    Event.RUNNER_SCORES_NO_THROW:
    r'^(\w+) scores$',
    Event.RUNNER_ON_FIRST_TO_SECOND_NO_THROW:
    r'^Runner from 1st tags up, SAFE at 2nd$',
    Event.RUNNER_ON_SECOND_TO_THIRD_NO_THROW:
    r'^Runner from 2nd (?:tags up, SAFE at 3rd|tries for 3rd, SAFE), no throw by \w+$',
    Event.RUNNER_ON_SECOND_TO_THIRD_THROW_MADE:
    r'^Runner from 2nd (?:tags up, SAFE at 3rd with throw by \w+|tries for 3rd, SAFE, throw by \w+ made to third)$',
    Event.RUNNER_ON_SECOND_OUT_AT_THIRD_THROW_MADE:
    r'^Runner from 2nd (?:tags up, OUT at 3rd!|tries for 3rd, OUT!) [\w-]+$',
    Event.RUNNER_ON_THIRD_SCORES_NO_THROW:
    r'^Runner from 3rd (?:tags up, SCORES|tries for Home, SAFE), no throw by \w+$',
    Event.RUNNER_ON_THIRD_SCORES_THROW_MADE:
    r'^Runner from 3rd (?:tags up, SCORES|tries for Home, SAFE), throw by \w+(?: to home)?$',
    Event.RUNNER_ON_THIRD_OUT_AT_HOME_THROW_MADE:
    r'^Runner from 3rd (?:tags up, OUT at HOME!|tries for Home, throw by \w+ and OUT!) [\w-]+$',
    Event.RUNNER_ON_THIRD_SCORES_OUT_AT_THIRD:
    r'^Runner from 3rd tries for Home, SAFE, throw by \w+ to trailing runner, OUT at third! [\w-]+$',
    Event.RUNNER_ON_THIRD_SCORES_SAFE_AT_THIRD:
    r'^Runner from 3rd tries for Home, SAFE, throw by \w+ to trailing runner, SAFE at third!$',
    Event.NONE:
    r'^\d-\d: Grounds into DOUBLE play, [\w-]+$',
}


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
    away, home, match = find(r'(\w+) at (\w+), (\d{2}\/\d{2}\/\d{4})', text)
    if not match:
        return None

    d = datetime.datetime.strptime(match, '%m/%d/%Y')
    d = datetime_datetime_pst(d.year, d.month, d.day)
    if date is not None and date != encode_datetime(d):
        return None

    match = find(r'(?s)Start Time:(.+?)<br>', text).strip(' EST')
    s = datetime.datetime.strptime(match.upper(), '%I:%M %p')

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
        match = find(r'>(\d{2}\/\d{2}\/\d{4})<', text)
        if not match:
            return None

        d = datetime.datetime.strptime(match, '%m/%d/%Y')
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
                match = find(regex, line, force_groups=True)
                if match is not None:
                    events.append(event.encode(*match))
                    break
            else:
                # TODO: Handle this gracefully.
                raise Exception(in_, line)

    data['events'] = events

    with open(out, 'w') as f:
        f.write(dumps(data) + '\n')

    return True
