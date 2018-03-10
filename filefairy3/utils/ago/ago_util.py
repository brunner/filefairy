#!/usr/bin/env python


def delta(then, now, fmt='{} ago'):
    diff = now - then
    s, d = diff.seconds, diff.days

    if s < 0 or d < 0:
        return delta(now, then, fmt='in {}')

    if d == 0:
        if s < 60:
            t = str(s) + 's'
        elif s < 3600:
            t = str(s / 60) + 'm'
        else:
            t = str(s / 3600) + 'h'
    else:
        t = str(d) + 'd'

    return fmt.format(t)
