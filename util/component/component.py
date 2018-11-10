#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def anchor(url, content):
    return '<a href="{}">{}</a>'.format(url, content)


def bold(text):
    return span(['font-weight-bold'], text)


def card(href='',
         title='',
         info='',
         code='',
         table=None,
         ts='',
         success='',
         danger=''):
    return {
        'href': href,
        'title': title,
        'info': info,
        'code': code,
        'table': table,
        'ts': ts,
        'success': success,
        'danger': danger
    }


def cell(col=None, content=''):
    return {'col': col, 'content': content}


def col(clazz='', colspan=''):
    return {'clazz': clazz, 'colspan': colspan}


def show(trigger, text):
    s = '<a data-toggle="collapse" href="#{0}" role="button" ' + \
        'aria-expanded="false" aria-controls="{0}">{1}</a>'
    return s.format(trigger, text)


def replace(text, replace):
    s = '<a class="repl-toggler" href="#" role="button" data-repl="{}">{}</a>'
    return s.format(replace, text)


def secondary(text):
    return span(['text-secondary'], text)


def span(classes, text):
    return '<span class="{}">{}</span>'.format(' '.join(classes), text)


def table(clazz='border mt-3',
          id_='',
          hcols=None,
          bcols=None,
          fcols=None,
          head=None,
          body=None,
          foot=None):
    return {
        'clazz': clazz,
        'id': id_,
        'hcols': hcols,
        'bcols': bcols,
        'fcols': fcols,
        'head': head,
        'body': body,
        'foot': foot
    }
