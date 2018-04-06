#!/usr/bin/env python
# -*- coding: utf-8 -*-

subtitle = ''

tmpl = 'exports.html'

_t33 = ['BAL', '6-4', 'W1']
_t34 = ['BOS', '10 - 0', 'W10']
_t35 = ['CWS', '9 - 1', 'L1']
_t38 = ['CLE', '8 - 2', 'W2']
_t40 = ['DET', '10 - 0', 'W10']
_t43 = ['KC', '9 - 1', 'W5']
_t47 = ['MIN', '10 - 0', 'W10']
_t48 = ['NYY', '10 - 0', 'W10']
_t57 = ['TB', '10 - 0', 'W10']
_t59 = ['TOR', '9 - 1', 'W4']
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
    'live': {
        'href': '',
        'title': '16 / 30',
        'info': '',
        'table': {
            'clazz':
            'table-sm',
            'cols': ['', 'w-100'],
            'head': [],
            'body': [['Rate: ', '53 %'], [
                'Old: ',
                'BAL, BOS, NYY, TB, TOR, KC, LAA, OAK, MIA, PHI, PIT, ARI, COL, SF'
            ]],
        },
        'ts': '30s ago',
        'success': '',
        'danger': ''
    },
    'standings': [{
        'clazz': 'border mt-3',
        'cols': ['', 'text-center w-25', 'text-center w-25'],
        'head': ['AL East', 'Last 10', 'Streak'],
        'body': [_t34, _t48, _t57, _t59, _t33]
    }, {
        'clazz': 'border mt-3',
        'cols': ['', 'text-center w-25', 'text-center w-25'],
        'head': ['AL Central', 'Last 10', 'Streak'],
        'body': [_t40, _t47, _t43, _t35, _t38]
    }]
}
