#!/usr/bin/env python


def card(href='',
         title='',
         info='',
         table=[],
         ts='',
         success='',
         danger=''):
    return {
        'href': href,
        'title': title,
        'info': info,
        'table': table,
        'ts': ts,
        'success': success,
        'danger': danger
    }
