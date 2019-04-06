#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Common (non-reloadable) util methods for interpreting events."""


def get_bag(base):
    if base == 1:
        return '1st'
    if base == 2:
        return '2nd'
    if base == 3:
        return '3rd'
    if base == 4:
        return 'home'


def get_base(base):
    if base == 'F':
        return 1
    if base == 'S':
        return 2
    if base == 'T':
        return 3
    if base == 'H':
        return 4


def get_outcome(path, out):
    if out:
        if path == 'F':
            return 'flies out'
        if path == 'G':
            return 'grounds out'
        if path == 'L':
            return 'lines out'
        return 'pops out'
    if path == 'F':
        return 'fly ball'
    if path == 'G':
        return 'ground ball'
    if path == 'L':
        return 'line drive'
    return 'pop up'


def get_position(zone, outfield):
    if outfield:
        if '8' in zone or 'M' in zone:
            return 'CF'
        if '3' in zone or '4' in zone or '9' in zone:
            return 'RF'
        return 'LF'
    if '1' in zone or 'P' in zone:
        return 'P'
    if '2' in zone:
        return 'C'
    if '3' in zone:
        return '1B'
    if '5' in zone:
        return '3B'
    if '4' in zone:
        return '2B'
    if '7' in zone:
        return 'LF'
    if '8' in zone:
        return 'CF'
    if '9' in zone:
        return 'RF'
    return 'SS'


def get_seats(zone):
    if '78' in zone:
        return 'left center field'
    if '89' in zone:
        return 'right center field'
    if '7' in zone:
        return 'left field'
    if '8' in zone:
        return 'center field'
    return 'right field'


def get_title(position):
    if position == 'P':
        return 'pitcher'
    if position == 'C':
        return 'catcher'
    if position == '1B':
        return 'first baseman'
    if position == '2B':
        return 'second baseman'
    if position == '3B':
        return 'third baseman'
    if position == 'SS':
        return 'shortstop'
    if position == 'LF':
        return 'left fielder'
    if position == 'CF':
        return 'center fielder'
    if position == 'RF':
        return 'right fielder'


def get_written(position):
    if position == 'P':
        return 'pitcher'
    if position == 'C':
        return 'catcher'
    if position == '1B':
        return 'first base'
    if position == '2B':
        return 'second base'
    if position == '3B':
        return 'third base'
    if position == 'SS':
        return 'shortstop'
    if position == 'LF':
        return 'left field'
    if position == 'CF':
        return 'center field'
    if position == 'RF':
        return 'right field'
