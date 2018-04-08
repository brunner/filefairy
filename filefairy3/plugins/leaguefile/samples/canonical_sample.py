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
    'fp': {
        'href': '',
        'title': 'Mar 10',
        'info': '',
        'table': {
            'clazz':
            'table-sm',
            'cols': ['', 'w-100'],
            'head': [],
            'body': [['Time: ', '56m'],
                     ['Size: ', '59,969,530']]
        },
        'ts': '30s ago',
        'success': 'ongoing',
        'danger': ''
    },
    'up': {
        'clazz':
        'border mt-3',
        'cols': ['', '', ''],
        'head': ['Date', 'Time', 'Size'],
        'body': [['Mar 8', '10h 11m', '358,347,534'],
                 ['Mar 6', '9h 34m', '356,922,996']]
    }
}
