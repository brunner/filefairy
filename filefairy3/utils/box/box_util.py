#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/utils/box', '', _path))
from utils.team.team_util import decoding_to_encoding_sub  # noqa
from utils.team.team_util import encoding_to_decoding_sub  # noqa
from utils.urllib.urllib_util import urlopen  # noqa

_title = '<title>MLB Box Scores, (.+?) at (.+?), {}</title>'
_row = '<tr style=\"background-color:#FFFFFE;\">(.+?)</tr>'
_team = '<td class="dl">(?:<b>)?([^<]+)(?:</b>)?</td>'
_line = '<td class="dc"><b>(\d+)</b></td>'


def clarify(date, link, encoding):
    content = urlopen(link)
    fdate = date.strftime('%m/%d/%Y')
    pattern = _title.format(fdate)
    title = re.findall(pattern, content, re.DOTALL)
    if not title:
        return encoding

    text = encoding_to_decoding_sub(encoding)
    left, right = text.split(', ')
    ht1, hr1 = left.rsplit(' ', 1)
    ht2, hr2 = right.rsplit(' ', 1)
    tt1, tt2 = title[0]

    if ht1 in tt2 and ht2 in tt1:
        tt1, tt2 = tt2, tt1
    if ht1 not in tt1 or ht2 not in tt2:
        return encoding

    rows = re.findall(_row, content, re.DOTALL)
    if len(rows) != 2:
        return encoding

    rt1, rt2 = [re.findall(_team, row)[0] for row in rows]
    rr1, rr2 = [re.findall(_line, row)[0] for row in rows]
    if hr1 == rr2 and hr2 == rr1:
        rt1, rt2, rr1, rr2 = rt2, rt1, rr2, rr1
    if hr1 != rr1 or hr2 != rr2:
        return encoding

    if tt1 in rt2 and tt2 in rt1:
        tt1, tt2 = tt2, tt1
    if tt1 not in rt1 or tt2 not in rt2:
        return encoding

    text = '{0} {1}, {2} {3}'.format(tt1, hr1, tt2, hr2)
    return decoding_to_encoding_sub(text)
