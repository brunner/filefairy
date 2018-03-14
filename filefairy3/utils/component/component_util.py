#!/usr/bin/env python
# -*- coding: utf-8 -*-


def card(href='', title='', info='', table=[], ts='', success='', danger=''):
    return {
        'href': href,
        'title': title,
        'info': info,
        'table': table,
        'ts': ts,
        'success': success,
        'danger': danger
    }


def table(head=[], body=[]):
    return {'head': head, 'body': body}
