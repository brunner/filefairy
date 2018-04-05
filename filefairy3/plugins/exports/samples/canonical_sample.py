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
        'head': ['Team', 'Last 10', 'Streak'],
        'body': [['Atlanta Braves', '10 - 0',
                  'W10'], ['Boston Red Sox', '10 - 0',
                           'W10'], ['Cincinnati Reds', '10 - 0',
                                    'W10'], ['Chicago Cubs', '9 - 1', 'W9'],
                 ['Colorado Rockies', '9 - 1',
                  'W8'], ['Baltimore Orioles', '3 - 7', 'L2']]
    }
}
