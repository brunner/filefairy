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


def elapsed(then, now):
    diff = now - then
    s, d = diff.seconds, diff.days

    if s < 0 or d < 0:
        return elapsed(now, then)

    if d > 0:
        s += 86400 * d

    h, m = s / 3600, (s / 60) % 60
    hm = []
    if h > 0:
        hm.append('{}h'.format(h))
    hm.append('{}m'.format(m))

    return ' '.join(hm)
