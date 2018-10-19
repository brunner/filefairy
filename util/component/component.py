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


def profile(num, colors):
    color, bg, border, stripes = colors
    if bg == border:
        y1, y2 = 4, 44
    else:
        y1, y2 = 6, 42
    if stripes:
        s = ('<line x1="9" y1="{0}" x2="9" y2="{1}" stroke="{2}"></line>'
             '<line x1="15" y1="{0}" x2="15" y2="{1}" stroke="{2}"></line>'
             '<line x1="21" y1="{0}" x2="21" y2="{1}" stroke="{2}"></line>'
             '<line x1="27" y1="{0}" x2="27" y2="{1}" stroke="{2}"></line>'
             '<line x1="33" y1="{0}" x2="33" y2="{1}" stroke="{2}"></line>'
             '<line x1="39" y1="{0}" x2="39" y2="{1}" stroke="{2}">'
             '</line>').format(y1, y2, stripes)
    else:
        s = ''
    return ('<svg viewBox="0,0,48,48">'
            '<style>.text {{ font: bold 24px sans-serif; }}</style>'
            '<rect x="0" y="0" width="48" height="48" fill="#6c757d" '
            'rx="8" ry="8"></rect>'
            '<rect x="1" y="1" width="46" height="46" fill="{1}" '
            'rx="7" ry="7"></rect>'
            '<rect x="4" y="4" width="40" height="40" fill="{3}" '
            'rx="5" ry="5"></rect>'
            '<rect x="6" y="6" width="36" height="36" fill="{2}" '
            'rx="4" ry="4"></rect>{4}'
            '<text x="50%" y="32" text-anchor="middle" fill="{1}" '
            'class="text">{0}</text>'
            '</svg>').format(num, color, bg, border, s)


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
