#!/usr/bin/env python
# -*- coding: utf-8 -*-

subtitle = ''

tmpl = 'exports.html'

context = {
    'title':
    'exports',
    'breadcrumbs': [{
        'href': '/fairylab/',
        'name': 'Home'
    }, {
        'href': '',
        'name': 'Exports'
    }],
    'table': {
        'cols': ['', 'text-center', 'text-center'],
        'head': ['Team', 'Streak', 'Last 10'],
        'body': [['Atlanta Braves', '+19',
                  '10 - 0'], ['Boston Red Sox', '+19',
                              '10 - 0'], ['Cincinnati Reds', '+19', '10 - 0'],
                 ['Chicago Cubs', '+9',
                  '9 - 1'], ['Chicago White Sox', '+8',
                             '9 - 1'], ['Baltimore Orioles', '-2', '3 - 7']]
    }
}
