#!/usr/bin/env python
# -*- coding: utf-8 -*-


def card(href='', title='', info='', table=None, ts='', success='', danger=''):
    return {
        'href': href,
        'title': title,
        'info': info,
        'table': table,
        'ts': ts,
        'success': success,
        'danger': danger
    }


def table(clazz='border mt-3', cols=None, head=None, body=None):
    return {'clazz': clazz, 'cols': cols, 'head': head, 'body': body}
