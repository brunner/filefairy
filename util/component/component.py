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


def profile(num, color, bg, border, stripes):
    if bg == border:
        y1, y2 = 7, 73
    else:
        y1, y2 = 11, 69
    if stripes:
        s = ('<line x1="18" y1="{0}" x2="18" y2="{1}" stroke="{2}"></line>'
             '<line x1="25" y1="{0}" x2="25" y2="{1}" stroke="{2}"></line>'
             '<line x1="32" y1="{0}" x2="32" y2="{1}" stroke="{2}"></line>'
             '<line x1="39" y1="{0}" x2="39" y2="{1}" stroke="{2}"></line>'
             '<line x1="46" y1="{0}" x2="46" y2="{1}" stroke="{2}"></line>'
             '<line x1="53" y1="{0}" x2="53" y2="{1}" stroke="{2}"></line>'
             '<line x1="60" y1="{0}" x2="60" y2="{1}" stroke="{2}">'
             '</line>').format(y1, y2, stripes)
    else:
        s = ''
    return ('<svg viewBox="0,0,78,80">'
            '<style>.text {{ font: bold 32px sans-serif; }}</style>'
            '<rect x="0" y="0" width="78" height="80" fill="#6c757d" '
            'rx="12" ry="12"></rect>'
            '<rect x="1" y="1" width="76" height="78" fill="{1}" '
            'rx="11" ry="11"></rect>'
            '<rect x="7" y="7" width="64" height="66" fill="{3}" '
            'rx="8" ry="8"></rect>'
            '<rect x="11" y="11" width="56" height="58" fill="{2}" '
            'rx="6" ry="6"></rect>{4}'
            '<text x="50%" y="52" text-anchor="middle" fill="{1}" '
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
