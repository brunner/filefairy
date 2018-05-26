#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/util/box', '', _path))
from util.team.team import decoding_to_encoding  # noqa
from util.team.team import decoding_to_encoding_sub  # noqa
from util.team.team import encoding_to_decoding  # noqa
from util.team.team import encoding_to_teamid  # noqa
from util.urllib_.urllib_ import urlopen  # noqa

_title = '<title>MLB Box Scores, (.+?) at (.+?), {}</title>'
_row = '<tr style=\"background-color:#FFFFFE;\">(.+?)</tr>'
_team = '<td class="dl">(?:<b>)?([^<]+)(?:</b>)?</td>'
_line = '<td class="dc"><b>(\d+)</b></td>'
_record = '(\w+) \(([^)]+)\)'


def _open(link):
    if link.startswith('http'):
        return urlopen(link).decode('iso-8859-1')
    if os.path.isfile(link):
        with open(link, 'r', encoding='iso-8859-1') as f:
            return f.read()
    return ''


def _value(encoding, before='', after=''):
    return {'encoding': encoding, 'before': before, 'after': after}


def clarify(date, link, encoding):
    content = _open(link)
    fdate = date.strftime('%m/%d/%Y')
    pattern = _title.format(fdate)
    title = re.findall(pattern, content, re.DOTALL)
    if not title:
        return _value(encoding)

    result = re.findall('(\w+) (\d+), (\w+) (\d+)', encoding)
    if not result:
        return _value(encoding)

    tt1, tt2 = title[0]
    ct1, ct2 = tt1, tt2
    et1, er1, et2, er2 = result[0]
    ht1, ht2 = encoding_to_decoding(et1), encoding_to_decoding(et2)

    if ht1 in tt2 and ht2 in tt1:
        tt1, tt2, et1, et2 = tt2, tt1, et2, et1
    if ht1 not in tt1 or ht2 not in tt2:
        return _value(encoding)

    rows = re.findall(_row, content, re.DOTALL)
    if len(rows) != 2:
        return _value(encoding)

    rt1, rt2 = [re.findall(_team, row)[0] for row in rows]
    rr1, rr2 = [re.findall(_line, row)[0] for row in rows]
    if er1 == rr2 and er2 == rr1:
        rt1, rt2, rr1, rr2 = rt2, rt1, rr2, rr1
    if er1 != rr1 or er2 != rr2:
        return _value(encoding)

    if tt1 in rt2 and tt2 in rt1:
        tt1, tt2 = tt2, tt1
    if tt1 not in rt1 or tt2 not in rt2:
        return _value(encoding)

    decoding = '{0} {1}, {2} {3}'.format(tt1, er1, tt2, er2)
    encoding = decoding_to_encoding_sub(decoding)
    ft1, ft2 = decoding_to_encoding(ct1), decoding_to_encoding(ct2)
    before = '{0} @ {1}'.format(et1, et2)
    after = '{0} @ {1}'.format(ft1, ft2)
    return _value(encoding, before=before, after=after)


def records(link):
    ret = {}
    content = _open(link)
    rows = re.findall(_row, content, re.DOTALL)
    if len(rows) != 2:
        return ret

    for r in [re.findall(_team, row)[0] for row in rows]:
        e = decoding_to_encoding_sub(r)
        match = re.findall(_record, e)
        if match:
            encoding, record = match[0]
            ret[encoding_to_teamid(encoding)] = record

    return ret
