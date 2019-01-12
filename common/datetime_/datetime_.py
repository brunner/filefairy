#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Common (non-reloadable) util methods for datetime objects."""

import datetime
import pytz
import re

EST = pytz.timezone('America/New_York')
CST = pytz.timezone('America/Winnipeg')
PST = pytz.timezone('America/Los_Angeles')


def datetime_as_est(d):
    """Convenience wrapper around datetime.astimezone.

    Adjusts an already localized datetime object to Eastern time.

    Args:
        d: The datetime object.

    Returns:
        The adjusted datetime object.
    """
    return d.astimezone(EST)


def datetime_as_pst(d):
    """Convenience wrapper around datetime.astimezone.

    Adjusts an already localized datetime object to Pacific time.

    Args:
        d: The datetime object.

    Returns:
        The adjusted datetime object.
    """
    return d.astimezone(PST)


def datetime_datetime_est(*args):
    """Localize a naive datetime object so it is Eastern time.

    Args:
        *args: The args accepted by datetime.datetime.

    Returns:
        A Eastern time localized datetime object.
    """
    return EST.localize(datetime.datetime(*args))


def datetime_datetime_cst(*args):
    """Localize a naive datetime object so it is Central time.

    Args:
        *args: The args accepted by datetime.datetime.

    Returns:
        A Central time localized datetime object.
    """
    return CST.localize(datetime.datetime(*args))


def datetime_datetime_pst(*args):
    """Localize a naive datetime object so it is Pacific time.

    Args:
        *args: The args accepted by datetime.datetime.

    Returns:
        A Pacific time localized datetime object.
    """
    return PST.localize(datetime.datetime(*args))


def datetime_now():
    """Convenience wrapper around datetime.datetime.now.

    Returns:
        A Pacific time localized datetime object for the current date and time.
    """
    return PST.localize(datetime.datetime.now())


def decode_datetime(s):
    """Parses an encoded datetime string into a Pacific time localized object.

    Args:
        s: The encoded datetime string.

    Returns:
        A Pacific time localized datetime object for the given string.
    """
    return datetime_datetime_pst(*map(int, re.findall('\d+', s[:-6])))


def encode_datetime(d):
    """Encodes a localized datetime object as an ISO-formatted string.

    Args:
        d: The datetime object.

    Returns:
        A string representation for the given datetime object.
    """
    return datetime_as_pst(d).isoformat()


def suffix(day):
    """Returns the numerical suffix for a given day.

    Args:
        day: The integer representation of the day.

    Returns:
        The numerical suffix.
    """
    return 'th' if 11 <= day <= 13 else {
        1: 'st',
        2: 'nd',
        3: 'rd'
    }.get(day % 10, 'th')


def timedelta(then, now):
    """Returns a string representing the duration between two datetime objects.

    Args:
        then: The first datetime object.
        now: The second datetime object.

    Returns:
        A string showing the number of hours and minutes between then and now.
    """
    diff = now - then
    s, d = diff.seconds, diff.days

    if s < 0 or d < 0:
        return timedelta(now, then)

    if d > 0:
        s += 86400 * d

    h, m = s // 3600, (s // 60) % 60
    hm = []
    if h > 0:
        hm.append('{}h'.format(h))
    hm.append('{}m'.format(m))

    return ' '.join(hm)


def timestamp(d):
    """Returns a display timestamp for a datetime object.

    Args:
        d: The datetime object.

    Returns:
        A display timestamp for the given datetime object.
    """
    return d.strftime('%H:%M:%S %Z (%Y-%m-%d)')
