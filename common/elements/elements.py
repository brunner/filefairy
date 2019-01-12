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
    """Builds a card element.

    Args:
        href: The optional title link.
        title: The title text.
        info: The optional description text.
        code: The optional preformatted text.
        table: The optional table content.
        ts: The timestamp to display in the card footer.
        success: The optional green-badge card text.
        danger: The optional red-badge card text.

    Returns:
        The card element.
    """
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
    """Builds a cell object, describing a table cell.

    Args:
        col: The col object for this particular cell.
        content: The cell text.

    Returns:
        The cell object.
    """
    return {'col': col, 'content': content}


def col(clazz='', colspan=''):
    """Builds a col object, describing a table column.

    Args:
        clazz: The CSS class(es) to apply to the column.
        colspan: The number of columns that this column should span.

    Returns:
        The col object.
    """
    return {'clazz': clazz, 'colspan': colspan}


def dialog(id_='', header='', tables=None):
    """Builds a dialog object.

    Args:
        id_: The CSS id to set on the root dialog element.
        header: The header text.
        tables: The optional list of table elements.

    Returns:
        The dialog object.
    """
    if tables is None:
        tables = []
    return {
        'id': id_,
        'header': header,
        'tables': tables,
    }


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
    """Builds a table element.

    Args:
        clazz: The optional CSS class to set on the root table element.
        id_: The optional CSS id to set on the root table element.
        hcols: The optional list of CSS classes to apply to each head column.
        bcols: The optional list of CSS classes to apply to each body column.
        fcols: The optional list of CSS classes to apply to each footer column.
        head: The optional list of head cells.
        body: The optional list of body rows. Each row is a list of cells.
        foot: The optional list of footer cells.

    Returns:
        The table element.
    """
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
