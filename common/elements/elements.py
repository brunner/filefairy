#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Common (non-reloadable) util methods for rendering templates."""


def anchor(url, content):
    """Builds an anchor element.

    Args:
        url: The link url.
        content: The inner HTML of the anchor element.

    Returns:
        The anchor element.
    """
    return '<a href="{}">{}</a>'.format(url, content)


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


def span(classes, text):
    """Builds a span element.

    Args:
        classes: The list of CSS classes to apply to the span.
        content: The inner HTML of the span element.

    Returns:
        The span element.
    """
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
