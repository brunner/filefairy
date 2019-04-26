#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Common (non-reloadable) util methods for rendering templates."""

FAVICON_LINK = 'https://fairylab.surge.sh/favicon-32x32.png'


def _attr(attributes):
    if attributes is None:
        return ''

    items = sorted(attributes.items())
    return ' ' + ' '.join('{}="{}"'.format(k, v) for k, v in items)


def _trow(t, name, row):
    if row is None:
        return
    if name not in t or t[name] is None:
        t[name] = []
    t[name].append(row)


def cell(col=None, content=''):
    """Builds a cell object, describing a table cell.

    Args:
        col: The col object for this particular cell.
        content: The cell text.

    Returns:
        The cell object.
    """
    obj = {}
    if col:
        obj['col'] = col
    if content:
        obj['content'] = content
    return obj


def col(clazz='', colspan=''):
    """Builds a col object, describing a table column.

    Args:
        clazz: The CSS class(es) to apply to the column.
        colspan: The number of columns that this column should span.

    Returns:
        The col object.
    """
    obj = {}
    if clazz:
        obj['clazz'] = clazz
    if colspan:
        obj['colspan'] = colspan
    return obj


SITELINKS_HCOLS = [col(clazz='font-weight-bold text-dark')]
SITELINKS_BCOLS = [col(clazz='position-relative')]
SITELINKS_TABLES = [
    ('Tasks', [
        ('timer', '/gameday/', 'Gameday'),
        ('people', '/news/', 'News'),
        ('spreadsheet', '/standings/', 'Standings'),
    ]),
    ('Other', [
        ('dashboard', '/dashboard/', 'Dashboard'),
        ('home', '/', 'Home'),
    ]),
]


def anchor(url, content):
    """Builds an anchor element.

    Args:
        url: The link url.
        content: The inner HTML of the anchor element.

    Returns:
        The anchor element.
    """
    return '<a href="{}">{}</a>'.format(url, content)


def dialog(id_='', icon='', tables=None):
    """Builds a dialog object.

    Args:
        id_: The CSS id to set on the root dialog element.
        icon: The icon element to display in the dialog element header.
        tables: The optional list of table elements.

    Returns:
        The dialog object.
    """
    obj = {}
    if id_:
        obj['id'] = id_
    if icon:
        obj['icon'] = icon
    if tables:
        obj['tables'] = tables
    return obj


def icon_img(src, size, classes, id_):
    """Builds an icon element for an image resource.

    Args:
        src: The source of the image.
        size: The size of the image, in pixels.
        classes: The list of CSS classes to apply to the img.
        id_: The CSS id to apply to the img.

    Returns:
        The span element.
    """
    if id_:
        id_ = ' id="{}"'.format(id_)
    classes = ' class="{}"'.format(' '.join(classes)) if classes else ''
    tag = '<img src="{0}" width="{1}" height="{1}" border="0"{2}{3}>'
    return tag.format(src, size, id_, classes)


def icon_span(name='', attributes=None, classes=None):
    """Builds an icon element for an Iconic font span.

    Args:
        name: The name of the icon.
        attributes: The set of data attributes to apply to the span.
        classes: The list of CSS classes to apply to the span.

    Returns:
        The span element.
    """
    if classes is None:
        classes = []
    classes = ['oi', 'oi-' + name, 'absolute-icon'] + classes
    return span(classes=classes, attributes=attributes)


def menu():
    """Builds a menu dialog.

    Returns:
        The menu dialog.
    """
    img = icon_img(FAVICON_LINK, '16', ['absolute-icon', 'left'], '')
    span_ = span(classes=['d-block', 'px-4'], text='Fairylab')
    return dialog(id_='menu', icon=(img + span_), tables=sitelinks(home=True))


def pre(content):
    """Builds a pre element.

    Args:
        content: The inner HTML of the pre element.

    Returns:
        The pre element.
    """
    return '<pre>{}</pre>'.format(content)


def row(cells=None, attributes=None, clazz=''):
    """Builds a row object, describing a table row.

    Args:
        cells: The cells in the row.
        attributes: The set of data attributes to apply to the row.
        clazz: The CSS class(es) to apply to the row.

    Returns:
        The row object.
    """
    obj = {}
    if cells:
        obj['cells'] = cells
    if attributes:
        obj['attr'] = _attr(attributes)
    if clazz:
        obj['clazz'] = clazz
    return obj


def ruleset(selector='', rules=None):
    """Builds a CSS ruleset element.

    Args:
        selector: The CSS selector.
        rules. The list of rules.

    Returns:
        The ruleset element.
    """
    obj = {}
    if selector:
        obj['selector'] = selector
    if rules:
        obj['rules'] = rules
    return obj


def sitelinks(home=False):
    """Builds a list of sitelinks tables.

    Args:
        home: Whether or not to include a Home link in the sitelinks.

    Returns:
        The list of sitelinks tables.
    """
    tables = [topper('Site Links')]
    for head, rows in SITELINKS_TABLES:
        body = []
        for name, href, text in rows:
            if name == 'home' and not home:
                continue
            icon = icon_span(name=name, classes=['left', 'text-secondary'])
            span_ = span(classes=['d-block pl-4'], text=anchor(href, text))
            body.append(row(cells=[cell(content=(icon + span_))]))

        tables.append(
            table(
                clazz='border mb-3',
                hcols=SITELINKS_HCOLS,
                bcols=SITELINKS_BCOLS,
                head=[row(cells=[cell(content=head)])],
                body=body))

    return tables


def span(id_='', classes='', attributes=None, text=''):
    """Builds a span element.

    Args:
        id: The CSS id to apply to the span.
        classes: The list of CSS classes to apply to the span.
        attributes: The set of data attributes to apply to the span.
        content: The inner HTML of the span element.

    Returns:
        The span element.
    """
    attr = _attr(attributes)
    if id_:
        id_ = ' id="{}"'.format(id_)
    if classes:
        classes = ' class="{}"'.format(' '.join(classes))
    return '<span{}{}{}>{}</span>'.format(id_, classes, attr, text)


def table(clazz='',
          id_='',
          attributes=None,
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
        attributes: The set of data attributes to apply to the table.
        hcols: The optional list of CSS classes to apply to each head column.
        bcols: The optional list of CSS classes to apply to each body column.
        fcols: The optional list of CSS classes to apply to each footer column.
        head: The optional list of head rows.
        body: The optional list of body rows.
        foot: The optional list of footer rows.

    Returns:
        The table element.
    """
    obj = {}
    if clazz:
        obj['clazz'] = clazz
    if id_:
        obj['id'] = id_
    if attributes:
        obj['attributes'] = _attr(attributes)
    if hcols:
        obj['hcols'] = hcols
    if bcols:
        obj['bcols'] = bcols
    if fcols:
        obj['fcols'] = fcols
    if head:
        obj['head'] = head
    if body:
        obj['body'] = body
    if foot:
        obj['foot'] = foot
    return obj


def tbody(obj, row):
    """Appends a body row to an existing table.

    Args:
        obj: The table.
        row: The row.
    """
    _trow(obj, 'body', row)


def topper(text):
    """Builds a topper table element.

    Args:
        text: The text of the topper table element.

    Returns:
        The topper table element.
    """
    return table(
        clazz='topper',
        bcols=[col(clazz='border-0 font-weight-bold px-0 text-secondary')],
        body=[row(cells=[cell(content=text)])])


def ts(half, minute, second):
    """Returns a string representing a livesim timestamp.

    Args:
        half: The index of the inning.
        minute: The index of the minute.
        second: The index of the second.

    Returns:
        The timestamp string.
    """
    return '{}.{}.{}'.format(half, minute, second)
