#!/usr/bin/env python


def card(href='',
         title='',
         new=False,
         info='',
         table=[],
         ts='',
         success='',
         danger=''):
    return {
        'href': href,
        'title': title,
        'new': new,
        'info': info,
        'table': table,
        'ts': ts,
        'success': success,
        'danger': danger
    }
