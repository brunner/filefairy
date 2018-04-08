#!/usr/bin/env python
# -*- coding: utf-8 -*-

subtitle = ''

tmpl = 'leaguefile.html'

context = {
    'title':
    'leaguefile',
    'breadcrumbs': [{
        'href': '/fairylab/',
        'name': 'Home'
    }, {
        'href': '',
        'name': 'Leaguefile'
    }],
    'fp': {},
    'up': {
        'clazz': 'border mt-3',
        'cols': ['', '', ''],
        'head': ['Date', 'Time', 'Size'],
        'body': [['Mar 10', '4h 56m', '359,969,530'],
                 ['Mar 8', '10h 11m', '358,347,534'],
                 ['Mar 6', '9h 34m', '356,922,996']]
    }
}
